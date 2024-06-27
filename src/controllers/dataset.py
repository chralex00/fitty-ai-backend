from ..schemas.dataset import Dataset
from fastapi import APIRouter, status, HTTPException, Body, UploadFile
from fastapi.responses import JSONResponse
from ..dtos.create_dataset_dto import CreateDatasetDto
from fastapi.encoders import jsonable_encoder
from ..dtos.dataset_query_config import DatasetQueryConfig
from ..dtos.update_dataset_dto import UpdateDatasetDto
from ..enums.dataset_type import DatasetType
from time import time
from ..services.dataset import update_one as update_one_dataset, search_many as search_many_datasets, create_one as create_dataset, find_one as find_one_dataset, delete_one as delete_one_dataset, count_many as count_many_datasets
from ..utilities.logging import LOGGER as logging
from datetime import datetime
from ..utilities.mongo_connection import GRIDFS_MONGODB
from ..constants.constants import NOT_FOUND_HTTP_EXCEPTION, INTERNAL_SERVER_ERROR_HTTP_EXCEPTION, EXCEL_FILE_EXTENSIONS

dataset_router = APIRouter()

@dataset_router.get(
    "/datasets/count",
    response_description = "Count a dataset by query config",
    response_model = Dataset,
    status_code = status.HTTP_200_OK,
    response_model_by_alias = False
)
async def count_many(dataset_query_config: DatasetQueryConfig = Body()) -> JSONResponse:
    try:
        result = await count_many_datasets(dataset_query_config)
        return JSONResponse(content = jsonable_encoder(result))
    except Exception as error:
        logging.error(f"Error occurred during the Dataset retrieving: {error}")
        raise INTERNAL_SERVER_ERROR_HTTP_EXCEPTION

@dataset_router.post(
    "/datasets/create",
    response_description = "Add a new dataset",
    response_model = Dataset,
    status_code = status.HTTP_201_CREATED,
    response_model_by_alias = False
)
async def create_one(createDatasetDto: CreateDatasetDto = Body()) -> JSONResponse:
    try:
        dataset = Dataset(
            name = createDatasetDto.name,
            description = createDatasetDto.description,
            tags = list(createDatasetDto.tags),
            primary_key_column_name = createDatasetDto.primary_key_column_name,
            target_column_name = createDatasetDto.target_column_name,
            test_samples_size = createDatasetDto.test_samples_size,
            created_at = datetime.fromtimestamp(int(time())),
            updated_at = datetime.fromtimestamp(int(time()))
        )

        created_dataset = await create_dataset(dataset)
        
        return JSONResponse(content = jsonable_encoder(created_dataset))
    except Exception as error:
        logging.error(f"Error occurred during the Dataset creation: {error}")
        raise INTERNAL_SERVER_ERROR_HTTP_EXCEPTION
    
@dataset_router.post(
    "/datasets/upload/{id}",
    response_description = "Upload new dataset file",
    status_code = status.HTTP_201_CREATED
)
async def upload_dataset(id: str, file: UploadFile) -> JSONResponse:
    try:
        file_type = file.filename.rsplit(".")[-1].upper()
        dataset_types = [ e.value for e in DatasetType ]

        if file_type == EXCEL_FILE_EXTENSIONS:
            file_type = DatasetType.EXCEL

        if not(file_type in dataset_types):
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = {
                    "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                    "message": "UNPROCESSABLE ENTITY",
                    "detail": f"Only {dataset_types} format are supported",
                    "error": True
                }
            )

        found_dataset = await find_one_dataset(id)

        if found_dataset is None:
            raise NOT_FOUND_HTTP_EXCEPTION

        file_id = GRIDFS_MONGODB.put(file.file)

        await update_one_dataset(id, {
            "file_object_id": file_id,
            "type": file_type
        })

        return JSONResponse(content = jsonable_encoder({
            "file_name": file.filename,
            "file_type": file_type,
            "file_size": file.size,
            "uploaded": True
        }))
    except HTTPException as http_exception:
        raise http_exception
    except Exception as error:
        logging.error(f"Error occurred uploading the Dataset: {error}")
        raise INTERNAL_SERVER_ERROR_HTTP_EXCEPTION

@dataset_router.get(
    "/datasets/search",
    response_description = "Search a dataset by query config",
    response_model = Dataset,
    status_code = status.HTTP_200_OK,
    response_model_by_alias = False
)
async def search_many(dataset_query_config: DatasetQueryConfig = Body()) -> JSONResponse:
    try:
        countResult = await count_many_datasets(dataset_query_config)
        searchResults = await search_many_datasets(dataset_query_config)

        print(searchResults)

        for result in searchResults:
            result["_id"] = str(result["_id"])
            result["file_object_id"] = str(result["file_object_id"])

        return JSONResponse(content = jsonable_encoder({
            "count": countResult["count"],
            "results": searchResults
        }))
    except Exception as error:
        logging.error(f"Error occurred during the Dataset retrieving: {error}")
        raise INTERNAL_SERVER_ERROR_HTTP_EXCEPTION

@dataset_router.get(
    "/datasets/find/{id}",
    response_description = "Find a dataset by ID",
    response_model = Dataset,
    status_code = status.HTTP_200_OK,
    response_model_by_alias = False
)
async def find_one(id: str) -> JSONResponse:
    try:
        found_dataset = await find_one_dataset(id)

        if found_dataset is None:
            raise NOT_FOUND_HTTP_EXCEPTION
        
        return JSONResponse(content = jsonable_encoder(found_dataset))
    except HTTPException as http_exception:
        raise http_exception
    except Exception as error:
        logging.error(f"Error occurred during the Dataset retrieving: {error}")
        raise INTERNAL_SERVER_ERROR_HTTP_EXCEPTION

@dataset_router.get(
    "/datasets/load/{id}",
    response_description = "Load a dataset file by ID",
    status_code = status.HTTP_201_CREATED
)
async def load_dataset(id: str) -> JSONResponse:
    try:
        found_dataset = await find_one_dataset(id)

        if found_dataset is None:
            raise NOT_FOUND_HTTP_EXCEPTION

        file_content = GRIDFS_MONGODB.get(found_dataset["file_object_id"]).read()

        return JSONResponse(content = jsonable_encoder({
            "file_id": str(found_dataset["file_object_id"]),
            "file_content": file_content
        }))
    except HTTPException as http_exception:
        raise http_exception
    except Exception as error:
        logging.error(f"Error occurred uploading the Dataset: {error}")
        raise INTERNAL_SERVER_ERROR_HTTP_EXCEPTION

@dataset_router.patch(
    "/datasets/update/{id}",
    response_description = "Update a dataset by ID",
    response_model = Dataset,
    status_code = status.HTTP_200_OK,
    response_model_by_alias = False
)
async def update_one(id: str, updateDatasetDto: UpdateDatasetDto = Body()) -> JSONResponse:
    try:
        dict_without_none_values = { k: v for k, v in dict(updateDatasetDto).items() if v != None }
        
        if ("tags" in dict_without_none_values) and (dict_without_none_values["tags"] != None):
            dict_without_none_values["tags"] = list(dict_without_none_values["tags"])
        
        updated_dataset = await update_one_dataset(id, dict_without_none_values)

        if updated_dataset == None:
            raise NOT_FOUND_HTTP_EXCEPTION
        
        updated_dataset["_id"] = str(updated_dataset["_id"])
        updated_dataset["file_object_id"] = str(updated_dataset["file_object_id"])
        
        return JSONResponse(content = jsonable_encoder(updated_dataset))
    except HTTPException as http_exception:
        raise http_exception
    except Exception as error:
        logging.error(f"Error occurred updating the Dataset: {error}")
        raise INTERNAL_SERVER_ERROR_HTTP_EXCEPTION

@dataset_router.delete(
    "/datasets/delete/{id}",
    response_description = "Delete a dataset by ID",
    response_model = Dataset,
    status_code = status.HTTP_200_OK,
    response_model_by_alias = False
)
async def delete_one(id: str) -> JSONResponse:
    try:
        found_dataset = await delete_one_dataset(id)

        if found_dataset is None:
            raise NOT_FOUND_HTTP_EXCEPTION
        
        found_dataset["_id"] = str(found_dataset["_id"])
        
        return JSONResponse(content = jsonable_encoder(found_dataset))
    except HTTPException as http_exception:
        raise http_exception
    except Exception as error:
        logging.error(f"Error occurred during the Dataset deletion: {error}")
        raise INTERNAL_SERVER_ERROR_HTTP_EXCEPTION