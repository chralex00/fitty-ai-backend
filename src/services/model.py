from ..schemas.model import Model
from ..utilities.mongo_connection import MODEL_MONGODB_COLLECTION
from bson.objectid import ObjectId
from pymongo.results import DeleteResult
import logging
from ..dtos.create_model_dto import CreateModelDto
from ..dtos.model_query_config import ModelQueryConfig
from typing import Dict, List
from datetime import datetime
from time import time
from pymongo import ReturnDocument
from ..constants.constants import DEFAULT_PAGINATION_OFFSET, DEFAULT_PAGINATION_LIMIT, DEFAULT_PAGINATION_SORT_NAME, DEFAULT_PAGINATION_SORT_DIRECTION

async def count_many(model_query_config: ModelQueryConfig) -> Dict[str, any]:
    try:
        count_query: Dict[str, any] = {}
        
        if model_query_config.name != None:
            count_query["name"] = { "$regex": model_query_config.name, "$options": "i" }

        if model_query_config.type != None:
            count_query["type"] = model_query_config.type

        if model_query_config.classifier_type != None:
            count_query["classifier_type"] = model_query_config.classifier_type

        if model_query_config.status != None:
            count_query["status"] = model_query_config.status

        if model_query_config.tags != None:
            count_query["tags"] = { "$in": list(model_query_config.tags) }

        if (model_query_config.created_at_min != None) or (model_query_config.created_at_max != None):
            created_at_min = datetime.fromtimestamp(model_query_config.created_at_min or 0)
            created_at_max = datetime.fromtimestamp(model_query_config.created_at_max or int(time()))
            count_query["created_at"] = {
                "$gte": created_at_min,
                "$lte": created_at_max
            }

        if (model_query_config.updated_at_min != None) or (model_query_config.updated_at_max != None):
            updated_at_min = datetime.fromtimestamp(model_query_config.updated_at_min or 0)
            updated_at_max = datetime.fromtimestamp(model_query_config.updated_at_max or int(time()))
            count_query["updated_at"] = {
                "$gte": updated_at_min,
                "$lte": updated_at_max
            }

        if (model_query_config.training_process_started_at_min != None) or (model_query_config.training_process_started_at_max != None):
            training_process_started_at_min = datetime.fromtimestamp(model_query_config.training_process_started_at_min or 0)
            training_process_started_at_max = datetime.fromtimestamp(model_query_config.training_process_started_at_max or int(time()))
            count_query["training_process_started_at"] = {
                "$gte": training_process_started_at_min,
                "$lte": training_process_started_at_max
            }

        if (model_query_config.training_process_ended_at_min != None) or (model_query_config.training_process_ended_at_max != None):
            training_process_ended_at_min = datetime.fromtimestamp(model_query_config.training_process_ended_at_min or 0)
            training_process_ended_at_max = datetime.fromtimestamp(model_query_config.training_process_ended_at_max or int(time()))
            count_query["training_process_ended_at"] = {
                "$gte": training_process_ended_at_min,
                "$lte": training_process_ended_at_max
            }

        count = await MODEL_MONGODB_COLLECTION.count_documents(count_query)
        
        return {
            "count": count
        }
    except Exception as error:
        logging.error(f"Error occurred counting the Model(s): {error}")
        raise Exception

async def create_one(model: CreateModelDto) -> Model:
    try:
        new_model = await MODEL_MONGODB_COLLECTION.insert_one(model.model_dump(by_alias = True))

        created_model = await MODEL_MONGODB_COLLECTION.find_one({ "_id": ObjectId(f"{new_model.inserted_id}") })
        created_model["_id"] = str(created_model["_id"])
        
        return created_model
    except Exception as error:
        logging.error(f"Error occurred during the Model creation: {error}")
        raise Exception

async def search_many(model_query_config: ModelQueryConfig) -> List[Model]:
    try:
        search_query: Dict[str, any] = {}
        
        if model_query_config.name != None:
            search_query["name"] = { "$regex": model_query_config.name, "$options": "i" }

        if model_query_config.type != None:
            search_query["type"] = model_query_config.type

        if model_query_config.classifier_type != None:
            search_query["classifier_type"] = model_query_config.classifier_type
        
        if model_query_config.status != None:
            search_query["status"] = model_query_config.status

        if model_query_config.tags != None:
            search_query["tags"] = { "$in": list(model_query_config.tags) }

        if (model_query_config.created_at_min != None) or (model_query_config.created_at_max != None):
            created_at_min = datetime.fromtimestamp(model_query_config.created_at_min or 0)
            created_at_max = datetime.fromtimestamp(model_query_config.created_at_max or int(time()))
            search_query["created_at"] = {
                "$gte": created_at_min,
                "$lte": created_at_max
            }

        if (model_query_config.updated_at_min != None) or (model_query_config.updated_at_max != None):
            updated_at_min = datetime.fromtimestamp(model_query_config.updated_at_min or 0)
            updated_at_max = datetime.fromtimestamp(model_query_config.updated_at_max or int(time()))
            search_query["updated_at"] = {
                "$gte": updated_at_min,
                "$lte": updated_at_max
            }

        if (model_query_config.training_process_started_at_min != None) or (model_query_config.training_process_started_at_max != None):
            training_process_started_at_min = datetime.fromtimestamp(model_query_config.training_process_started_at_min or 0)
            training_process_started_at_max = datetime.fromtimestamp(model_query_config.training_process_started_at_max or int(time()))
            search_query["training_process_started_at"] = {
                "$gte": training_process_started_at_min,
                "$lte": training_process_started_at_max
            }

        if (model_query_config.training_process_ended_at_min != None) or (model_query_config.training_process_ended_at_max != None):
            training_process_ended_at_min = datetime.fromtimestamp(model_query_config.training_process_ended_at_min or 0)
            training_process_ended_at_max = datetime.fromtimestamp(model_query_config.training_process_ended_at_max or int(time()))
            search_query["training_process_ended_at"] = {
                "$gte": training_process_ended_at_min,
                "$lte": training_process_ended_at_max
            }

        results = await (MODEL_MONGODB_COLLECTION
            .find(search_query)
            .sort(
                model_query_config.sort_field or DEFAULT_PAGINATION_SORT_NAME,
                model_query_config.sort_direction or DEFAULT_PAGINATION_SORT_DIRECTION
            )
            .skip(model_query_config.offset or DEFAULT_PAGINATION_OFFSET)
            .limit(model_query_config.limit or DEFAULT_PAGINATION_LIMIT)
            .to_list(model_query_config.limit or DEFAULT_PAGINATION_LIMIT))
        
        for result in results:
            result["_id"] = str(result["_id"])

        return results
    except Exception as error:
        logging.error(f"Error occurred counting the Model(s): {error}")
        raise Exception

async def find_one(id: str) -> Model | None:
    try:
        found_model = await MODEL_MONGODB_COLLECTION.find_one({ "_id": ObjectId(f"{id}") })
        
        if found_model:
            found_model["_id"] = str(found_model["_id"])
        
        return found_model
    except Exception as error:
        logging.error(f"Error occurred during the Model retrieving: {error}")
        raise Exception

async def update_one(id: str, model: Dict[str, any]) -> Model:
    try:
        return await MODEL_MONGODB_COLLECTION.find_one_and_update(
            { "_id": ObjectId(f"{id}") },
            { "$set": model },
            return_document = ReturnDocument.AFTER
        )
    except Exception as error:
        logging.error(f"Error occurred updating the Model: {error}")
        raise Exception

async def delete_one(id: str) -> DeleteResult:
    try:
        return await MODEL_MONGODB_COLLECTION.find_one_and_delete({ "_id": ObjectId(id) })
    except Exception as error:
        logging.error(f"Error occurred during the Model deletion: {error}")
        raise Exception