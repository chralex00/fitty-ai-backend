from ..utilities.logging import LOGGER as logging
from ..utilities.mongo_connection import GRIDFS_MONGODB
from ..dtos.model_query_config import ModelQueryConfig
from ..schemas.model import Model
from ..services.model import search_many as search_model, update_one as update_one_model
from ..services.dataset import find_one as find_one_dataset, update_one as update_one_dataset
from ..enums.model_status import ModelStatus
from datetime import datetime
from time import time
from pandas import DataFrame
import pandas as pd
import io
from datetime import datetime

async def to_training_and_trained_status():
    try:
        model_query_config = ModelQueryConfig(
                offset = 0,
                limit = 1,
                status = ModelStatus.DATASET_SPLIT
        )

        logging.debug(f"to_training_and_trained_status(): searching one model in the {ModelStatus.DATASET_SPLIT} statuts")
        search_results = await search_model(model_query_config)

        if len(search_results) != 1:
                logging.debug(f"to_training_and_trained_status(): no model found in the {ModelStatus.DATASET_SPLIT} statuts")
                return

        model_found: Model = search_results[0]
        logging.debug("to_training_and_trained_status(): model with id {} found".format(model_found["_id"]))

        dataset_found = None if model_found["dataset_id"] == None else await find_one_dataset(str(model_found["dataset_id"]))

        if (model_found["dataset_id"] == None) or (dataset_found == None) or (dataset_found["file_splited_object_id"] == None):
            model_found["training_process_logs"].append("to_training_and_trained_status(): the model with id {} has not an associated dataset".format(model_found["_id"]))
            await update_one_model(model_found["_id"], {
                "status": ModelStatus.ERROR,
                "training_process_logs": model_found["training_process_logs"],
                "updated_at": datetime.fromtimestamp(int(time()))
            })
            logging.debug("to_training_and_trained_status(): model with id {} updated to the {} status".format(model_found["_id"], ModelStatus.ERROR))
            return

        try:
            dataset_file: str = GRIDFS_MONGODB.get(dataset_found["file_splited_object_id"]).read()
            df: DataFrame = pd.read_csv(io.BytesIO(dataset_file))

            await update_one_model(model_found["_id"], {
                "status": ModelStatus.TRAINING,
                "training_process_logs": [],
                "updated_at": datetime.fromtimestamp(int(time()))
            })

            # to do - create and training the model
            # to do - save the trained model
        except Exception as error:
            model_found["training_process_logs"].append("to_training_and_trained_status(): error occurred while creating and handling the data frame for model with the id {}, the error is: {}".format(model_found["_id"], error))
            await update_one_model(model_found["_id"], {
                "status": ModelStatus.ERROR,
                "training_process_logs": model_found["training_process_logs"],
                "updated_at": datetime.fromtimestamp(int(time()))
            })
            logging.debug("to_training_and_trained_status(): model with id {} updated to the {} status".format(model_found["_id"], ModelStatus.ERROR))
            return

        await update_one_model(model_found["_id"], {
            "status": ModelStatus.TRAINED,
            "training_process_logs": [],
            "updated_at": datetime.fromtimestamp(int(time()))
        })

        logging.debug("to_training_and_trained_status(): model with id {} updated to the {} status".format(model_found["_id"], ModelStatus.TRAINED))
    except Exception as error:
        logging.error(f"to_training_and_trained_status(): error occurred during the model training process: {error}")
        raise Exception