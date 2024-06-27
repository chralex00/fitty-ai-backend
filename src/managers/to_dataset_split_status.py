from ..utilities.logging import LOGGER as logging
from ..utilities.mongo_connection import GRIDFS_MONGODB
from ..dtos.model_query_config import ModelQueryConfig
from ..schemas.model import Model
from ..services.model import search_many as search_model, update_one as update_one_model
from ..services.dataset import find_one as find_one_dataset, update_one as update_one_dataset
from ..enums.model_status import ModelStatus
from ..enums.dataset_type import DatasetType
from datetime import datetime
from time import time
from pandas import DataFrame
import pandas as pd
import io
from typing import List
from sklearn import model_selection
import random
from datetime import datetime

async def to_dataset_split_status():
    try:
        model_query_config = ModelQueryConfig(
                offset = 0,
                limit = 1,
                status = ModelStatus.DATASET_LINKED
        )

        logging.debug(f"to_dataset_split_status(): searching one model in the {ModelStatus.DATASET_LINKED} statuts")
        search_results = await search_model(model_query_config)

        if len(search_results) != 1:
                logging.debug(f"to_dataset_split_status(): no model found in the {ModelStatus.DATASET_LINKED} statuts")
                return

        model_found: Model = search_results[0]
        logging.debug("to_dataset_split_status(): model with id {} found".format(model_found["_id"]))

        dataset_found = None if model_found["dataset_id"] == None else await find_one_dataset(str(model_found["dataset_id"]))

        if (model_found["dataset_id"] == None) or (dataset_found == None) or (dataset_found["file_object_id"] == None):
            model_found["training_process_logs"].append("to_dataset_split_status(): the model with id {} has not an associated dataset".format(model_found["_id"]))
            await update_one_model(model_found["_id"], {
                "status": ModelStatus.ERROR,
                "training_process_logs": model_found["training_process_logs"],
                "updated_at": datetime.fromtimestamp(int(time()))
            })
            logging.debug("to_dataset_split_status(): model with id {} updated to the {} status".format(model_found["_id"], ModelStatus.ERROR))
            return

        try:
            dataset_file: str = GRIDFS_MONGODB.get(dataset_found["file_object_id"]).read()
            df: DataFrame = DataFrame()

            if dataset_found["type"] == DatasetType.CSV:
                df = pd.read_csv(io.BytesIO(dataset_file))
            elif dataset_found["type"] == DatasetType.EXCEL:
                df = pd.read_excel(io.BytesIO(dataset_file))
            elif dataset_found["type"] == DatasetType.HTML:
                dfs: List[DataFrame] = pd.read_html(io.BytesIO(dataset_file))
                df = dfs[0] if len(dfs) > 0 else df
            elif dataset_found["type"] == DatasetType.JSON:
                df = pd.read_json(io.BytesIO(dataset_file))
                df.to_parquet(path = "/Users/christian.alessandro.atzeni/OneDrive - EY/Desktop/diabetes.paraquet")
            elif dataset_found["type"] == DatasetType.PARQUET:
                df = pd.read_parquet(io.BytesIO(dataset_file))
            elif dataset_found["type"] == DatasetType.XML:
                df = pd.read_xml(io.BytesIO(dataset_file))

            random.seed(int(datetime.now().timestamp()))

            df_train, df_test, y_train, y_test = model_selection.train_test_split(
                df[dataset_found["primary_key_column_name"]].values,
                df[dataset_found["target_column_name"]].values,
                test_size = dataset_found["test_samples_size"],
                random_state = random.randint(1, 100 + 1)
            )

            df["is_train_sample"] = df[dataset_found["primary_key_column_name"]].isin(df_train)
            df["is_test_sample"] = df[dataset_found["primary_key_column_name"]].isin(df_test)

            byte_io = io.BytesIO()
            df.to_csv(byte_io)

            file_id = GRIDFS_MONGODB.put(byte_io)

            await update_one_dataset(dataset_found["_id"], {
                "file_splited_object_id": file_id
            })
        except Exception as error:
            model_found["training_process_logs"].append("to_dataset_split_status(): error occurred while creating and handling the data frame for model with the id {}, the error is: {}".format(model_found["_id"], error))
            await update_one_model(model_found["_id"], {
                "status": ModelStatus.ERROR,
                "training_process_logs": model_found["training_process_logs"],
                "updated_at": datetime.fromtimestamp(int(time()))
            })
            logging.debug("to_dataset_split_status(): model with id {} updated to the {} status".format(model_found["_id"], ModelStatus.ERROR))
            return

        await update_one_model(model_found["_id"], {
            "status": ModelStatus.DATASET_SPLIT,
            "training_process_logs": [],
            "updated_at": datetime.fromtimestamp(int(time()))
        })

        logging.debug("to_dataset_split_status(): model with id {} updated to the {} status".format(model_found["_id"], ModelStatus.DATASET_SPLIT))
    except Exception as error:
        logging.error(f"to_dataset_split_status(): error occurred during the model training process: {error}")
        raise Exception