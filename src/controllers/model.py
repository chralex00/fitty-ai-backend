from ..schemas.model import Model
from fastapi import APIRouter, status, HTTPException, Body
from fastapi.responses import JSONResponse
from ..dtos.create_model_dto import CreateModelDto
from fastapi.encoders import jsonable_encoder
from ..enums.model_status import ModelStatus
from ..dtos.model_query_config import ModelQueryConfig
from ..dtos.update_model_dto import UpdateModelDto
from time import time
from ..services.model import update_one as update_one_model, search_many as search_model, create_one as create_model, find_one as find_one_model, delete_one as delete_one_model, count_many as count_model
from ..services.dataset import find_one as find_one_dataset
import logging
from datetime import datetime
from ..utilities.check_model_type import check_model_type
from ..utilities.check_model_status import check_model_status
from ..constants.constants import NOT_FOUND_HTTP_EXCEPTION, INTERNAL_SERVER_ERROR_HTTP_EXCEPTION

model_router = APIRouter()

@model_router.get(
    "/models/count",
    response_description = "Count a model by query config",
    response_model = Model,
    status_code = status.HTTP_200_OK,
    response_model_by_alias = False
)
async def count_many(model_query_config: ModelQueryConfig = Body()) -> JSONResponse:
    try:
        result = await count_model(model_query_config)
        return JSONResponse(content = jsonable_encoder(result))
    except Exception as error:
        logging.error(f"Error occurred during the Model retrieving: {error}")
        raise INTERNAL_SERVER_ERROR_HTTP_EXCEPTION

@model_router.post(
    "/models/create",
    response_description = "Add a new model",
    response_model = Model,
    status_code = status.HTTP_201_CREATED,
    response_model_by_alias = False
)
async def create_one(createModelDto: CreateModelDto = Body()) -> JSONResponse:
    try:
        check_model_type(model_type = createModelDto.type, classifier_type = createModelDto.classifier_type)

        dataset_id = None

        if createModelDto.dataset_id != None:
            try:
                dataset_found = await find_one_dataset(createModelDto.dataset_id)
                dataset_id = dataset_found["_id"] if dataset_found != None else None
            except:
                raise NOT_FOUND_HTTP_EXCEPTION

        model = Model(
            name = createModelDto.name,
            description = createModelDto.description,
            type = createModelDto.type,
            classifier_type = createModelDto.classifier_type,
            status = ModelStatus.CREATED.value,
            tags = list(createModelDto.tags),
            created_at = datetime.fromtimestamp(int(time())),
            updated_at = datetime.fromtimestamp(int(time())),
            dataset_id = dataset_id
        )

        created_model = await create_model(model)
        
        return JSONResponse(content = jsonable_encoder(created_model))
    except HTTPException as http_exception:
        raise http_exception
    except Exception as error:
        logging.error(f"Error occurred during the Model creation: {error}")
        raise INTERNAL_SERVER_ERROR_HTTP_EXCEPTION
    
@model_router.patch(
    "/models/start-training-process/{id}",
    response_description = "Start training process of a model by ID",
    response_model = Model,
    status_code = status.HTTP_200_OK,
    response_model_by_alias = False
)
async def start_training_process(id: str) -> JSONResponse:
    try:
        model_found = await find_one_model(id)

        if model_found is None:
            raise NOT_FOUND_HTTP_EXCEPTION
        
        check_model_status(model_found["status"])
        
        updated_model = await update_one_model(id, {
            "status": ModelStatus.PROCESS_STARTED,
            "training_process_started_at": datetime.fromtimestamp(int(time())),
            "training_process_logs": []
        })

        if updated_model == None:
            raise NOT_FOUND_HTTP_EXCEPTION

        updated_model["_id"] = str(updated_model["_id"])
        updated_model["dataset_id"] = str(updated_model["dataset_id"])
        
        return JSONResponse(content = jsonable_encoder(updated_model))
    except HTTPException as http_exception:
        raise http_exception
    except Exception as error:
        logging.error(f"Error occurred starting the Model training process: {error}")
        raise INTERNAL_SERVER_ERROR_HTTP_EXCEPTION

@model_router.get(
    "/models/search",
    response_description = "Search a model by query config",
    response_model = Model,
    status_code = status.HTTP_200_OK,
    response_model_by_alias = False
)
async def search_many(model_query_config: ModelQueryConfig = Body()) -> JSONResponse:
    try:
        countResult = await count_model(model_query_config)
        searchResults = await search_model(model_query_config)

        return JSONResponse(content = jsonable_encoder({
            "count": countResult["count"],
            "results": searchResults
        }))
    except Exception as error:
        logging.error(f"Error occurred during the Model retrieving: {error}")
        raise INTERNAL_SERVER_ERROR_HTTP_EXCEPTION

@model_router.get(
    "/models/find/{id}",
    response_description = "Find a model by ID",
    response_model = Model,
    status_code = status.HTTP_200_OK,
    response_model_by_alias = False
)
async def find_one(id: str) -> JSONResponse:
    try:
        found_model = await find_one_model(id)

        if found_model is None:
            raise NOT_FOUND_HTTP_EXCEPTION
        
        return JSONResponse(content = jsonable_encoder(found_model))
    except HTTPException as http_exception:
        raise http_exception
    except Exception as error:
        logging.error(f"Error occurred during the Model retrieving: {error}")
        raise INTERNAL_SERVER_ERROR_HTTP_EXCEPTION

@model_router.patch(
    "/models/update/{id}",
    response_description = "Update a model by ID",
    response_model = Model,
    status_code = status.HTTP_200_OK,
    response_model_by_alias = False
)
async def update_one(id: str, updateModelDto: UpdateModelDto = Body()) -> JSONResponse:
    try:
        check_model_type(model_type = updateModelDto.type, classifier_type = updateModelDto.classifier_type)

        model_found = await find_one_model(id)

        if model_found == None:
            raise NOT_FOUND_HTTP_EXCEPTION

        check_model_status(model_found["status"])

        dict_without_none_values = { k: v for k, v in dict(updateModelDto).items() if v != None }
        
        if ("tags" in dict_without_none_values) and (dict_without_none_values["tags"] != None):
            dict_without_none_values["tags"] = list(dict_without_none_values["tags"])
        
        dataset_id = model_found["dataset_id"]

        if updateModelDto.dataset_id != None:
            try:
                dataset_found = await find_one_dataset(updateModelDto.dataset_id)
                dataset_id = dataset_found["_id"] if dataset_found != None else None
            except:
                raise NOT_FOUND_HTTP_EXCEPTION

        dict_without_none_values["dataset_id"] = dataset_id

        updated_model = await update_one_model(id, dict_without_none_values)

        if updated_model == None:
            raise NOT_FOUND_HTTP_EXCEPTION
        
        updated_model["_id"] = str(updated_model["_id"])
        updated_model["dataset_id"] = str(updated_model["dataset_id"])
        
        return JSONResponse(content = jsonable_encoder(updated_model))
    except HTTPException as http_exception:
        raise http_exception
    except Exception as error:
        logging.error(f"Error occurred updating the Model: {error}")
        raise INTERNAL_SERVER_ERROR_HTTP_EXCEPTION

@model_router.delete(
    "/models/delete/{id}",
    response_description = "Delete a model by ID",
    response_model = Model,
    status_code = status.HTTP_200_OK,
    response_model_by_alias = False
)
async def delete_one(id: str) -> JSONResponse:
    try:
        model_found = await delete_one_model(id)

        if model_found is None:
            raise NOT_FOUND_HTTP_EXCEPTION
        
        check_model_status(model_found["status"])
        
        model_found["_id"] = str(model_found["_id"])

        return JSONResponse(content = jsonable_encoder(model_found))
    except HTTPException as http_exception:
        raise http_exception
    except Exception as error:
        logging.error(f"Error occurred during the Model deletion: {error}")
        raise INTERNAL_SERVER_ERROR_HTTP_EXCEPTION