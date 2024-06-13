import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from .env_vars import ENV_VARS
from typing import Final
from pymongo import MongoClient
from pymongo.database import Database
from gridfs import GridFS

fittyaidb_client: Final[AsyncIOMotorDatabase] = motor.motor_asyncio.AsyncIOMotorClient(ENV_VARS.MONGODB_URL).fittyaidb

MODEL_MONGODB_COLLECTION: Final[AsyncIOMotorCollection] = fittyaidb_client.get_collection("models")
DATASET_MONGODB_COLLECTION: Final[AsyncIOMotorCollection] = fittyaidb_client.get_collection("datasets")

fittyaidb_database: Final[Database] = MongoClient(ENV_VARS.MONGODB_URL).fittyaidb
GRIDFS_MONGODB: Final[any] = GridFS(fittyaidb_database)