from ..schemas.dataset import Dataset
from ..utilities.mongo_connection import DATASET_MONGODB_COLLECTION
from bson.objectid import ObjectId
from pymongo.results import DeleteResult
from ..utilities.logging import LOGGER as logging
from ..dtos.create_dataset_dto import CreateDatasetDto
from ..dtos.dataset_query_config import DatasetQueryConfig
from typing import Dict, List
from datetime import datetime
from time import time
from pymongo import ReturnDocument
from ..constants.constants import DEFAULT_PAGINATION_OFFSET, DEFAULT_PAGINATION_LIMIT, DEFAULT_PAGINATION_SORT_NAME, DEFAULT_PAGINATION_SORT_DIRECTION

async def count_many(dataset_query_config: DatasetQueryConfig) -> Dict[str, any]:
    try:
        count_query: Dict[str, any] = {}
        
        if dataset_query_config.name != None:
            count_query["name"] = { "$regex": dataset_query_config.name, "$options": "i" }

        if dataset_query_config.type != None:
            count_query["type"] = dataset_query_config.type

        if dataset_query_config.tags != None:
            count_query["tags"] = { "$in": list(dataset_query_config.tags) }

        if dataset_query_config.primary_key_column_name != None:
            count_query["primary_key_column_name"] = { "$regex": dataset_query_config.primary_key_column_name, "$options": "i" }
        
        if dataset_query_config.features_column_names != None:
            count_query["features_column_names"] = { "$in": list(dataset_query_config.features_column_names) }

        if dataset_query_config.target_column_name != None:
            count_query["target_column_name"] = { "$regex": dataset_query_config.target_column_name, "$options": "i" }

        if (dataset_query_config.test_samples_size_min != None) or (dataset_query_config.test_samples_size_max != None):
            test_samples_size_min = dataset_query_config.test_samples_size_min or 0
            test_samples_size_max = dataset_query_config.test_samples_size_max or 1
            count_query["test_samples_size"] = {
                "$gte": test_samples_size_min,
                "$lte": test_samples_size_max
            }

        if (dataset_query_config.created_at_min != None) or (dataset_query_config.created_at_max != None):
            created_at_min = datetime.fromtimestamp(dataset_query_config.created_at_min or 0)
            created_at_max = datetime.fromtimestamp(dataset_query_config.created_at_max or int(time()))
            count_query["created_at"] = {
                "$gte": created_at_min,
                "$lte": created_at_max
            }

        if (dataset_query_config.updated_at_min != None) or (dataset_query_config.updated_at_max != None):
            updated_at_min = datetime.fromtimestamp(dataset_query_config.updated_at_min or 0)
            updated_at_max = datetime.fromtimestamp(dataset_query_config.updated_at_max or int(time()))
            count_query["updated_at"] = {
                "$gte": updated_at_min,
                "$lte": updated_at_max
            }

        count = await DATASET_MONGODB_COLLECTION.count_documents(count_query)
        
        return {
            "count": count
        }
    except Exception as error:
        logging.error(f"Error occurred counting the Dataset(s): {error}")
        raise Exception

async def create_one(dataset: CreateDatasetDto) -> Dataset:
    try:
        new_dataset = await DATASET_MONGODB_COLLECTION.insert_one(dataset.model_dump(by_alias = True))

        created_dataset = await DATASET_MONGODB_COLLECTION.find_one({ "_id": ObjectId(f"{new_dataset.inserted_id}") })
        created_dataset["_id"] = str(created_dataset["_id"])
        
        return created_dataset
    except Exception as error:
        logging.error(f"Error occurred during the Dataset creation: {error}")
        raise Exception

async def search_many(dataset_query_config: DatasetQueryConfig) -> List[Dataset]:
    try:
        search_query: Dict[str, any] = {}
        
        if dataset_query_config.name != None:
            search_query["name"] = { "$regex": dataset_query_config.name, "$options": "i" }

        if dataset_query_config.type != None:
            search_query["type"] = dataset_query_config.type

        if dataset_query_config.tags != None:
            search_query["tags"] = { "$in": list(dataset_query_config.tags) }

        if dataset_query_config.primary_key_column_name != None:
            search_query["primary_key_column_name"] = { "$regex": dataset_query_config.primary_key_column_name, "$options": "i" }
        
        if dataset_query_config.target_column_name != None:
            search_query["target_column_name"] = { "$regex": dataset_query_config.target_column_name, "$options": "i" }

        if (dataset_query_config.test_samples_size_min != None) or (dataset_query_config.test_samples_size_max != None):
            test_samples_size_min = dataset_query_config.test_samples_size_min or 0
            test_samples_size_max = dataset_query_config.test_samples_size_max or 1
            search_query["test_samples_size"] = {
                "$gte": test_samples_size_min,
                "$lte": test_samples_size_max
            }

        if (dataset_query_config.created_at_min != None) or (dataset_query_config.created_at_max != None):
            created_at_min = datetime.fromtimestamp(dataset_query_config.created_at_min or 0)
            created_at_max = datetime.fromtimestamp(dataset_query_config.created_at_max or int(time()))
            search_query["created_at"] = {
                "$gte": created_at_min,
                "$lte": created_at_max
            }

        if (dataset_query_config.updated_at_min != None) or (dataset_query_config.updated_at_max != None):
            updated_at_min = datetime.fromtimestamp(dataset_query_config.updated_at_min or 0)
            updated_at_max = datetime.fromtimestamp(dataset_query_config.updated_at_max or int(time()))
            search_query["updated_at"] = {
                "$gte": updated_at_min,
                "$lte": updated_at_max
            }

        results = await (DATASET_MONGODB_COLLECTION
            .find(search_query)
            .sort(
                dataset_query_config.sort_field or DEFAULT_PAGINATION_SORT_NAME,
                dataset_query_config.sort_direction or DEFAULT_PAGINATION_SORT_DIRECTION
            )
            .skip(dataset_query_config.offset or DEFAULT_PAGINATION_OFFSET)
            .limit(dataset_query_config.limit or DEFAULT_PAGINATION_LIMIT)
            .to_list(dataset_query_config.limit or DEFAULT_PAGINATION_LIMIT))
        
        for result in results:
            result["_id"] = str(result["_id"])

        return results
    except Exception as error:
        logging.error(f"Error occurred counting the Dataset(s): {error}")
        raise Exception

async def find_one(id: str) -> Dataset | None:
    try:
        found_dataset = await DATASET_MONGODB_COLLECTION.find_one({ "_id": ObjectId(f"{id}") })
        
        if found_dataset:
            found_dataset["_id"] = str(found_dataset["_id"])
        
        return found_dataset
    except Exception as error:
        logging.error(f"Error occurred during the Dataset retrieving: {error}")
        raise Exception

async def update_one(id: str, dataset: Dict[str, any]) -> Dataset:
    try:
        return await DATASET_MONGODB_COLLECTION.find_one_and_update(
            { "_id": ObjectId(f"{id}") },
            { "$set": dataset },
            return_document = ReturnDocument.AFTER
        )
    except Exception as error:
        logging.error(f"Error occurred updating the Dataset: {error}")
        raise Exception

async def delete_one(id: str) -> DeleteResult:
    try:
        return await DATASET_MONGODB_COLLECTION.find_one_and_delete({ "_id": ObjectId(id) })
    except Exception as error:
        logging.error(f"Error occurred during the Dataset deletion: {error}")
        raise Exception