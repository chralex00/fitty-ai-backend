from ..utilities.logging import LOGGER as logging
from ..dtos.model_query_config import ModelQueryConfig
from ..schemas.model import Model
from ..services.model import search_many as search_model, update_one as update_one_model
from ..services.dataset import find_one as find_one_dataset
from ..enums.model_status import ModelStatus
from datetime import datetime
from time import time

async def to_dataset_linked_status():
    try:
        model_query_config = ModelQueryConfig(
                offset = 0,
                limit = 1,
                status = ModelStatus.PROCESS_STARTED
        )

        logging.debug(f"to_dataset_linked_status(): searching one model in the {ModelStatus.PROCESS_STARTED} statuts")
        search_results = await search_model(model_query_config)

        if len(search_results) != 1:
                logging.debug(f"to_dataset_linked_status(): no model found in the {ModelStatus.PROCESS_STARTED} statuts")
                return

        model_found: Model = search_results[0]
        model_status: ModelStatus = ModelStatus.DATASET_LINKED
        training_process_logs = []
        logging.debug("to_dataset_linked_status(): model with id {} found".format(model_found["_id"]))

        if model_found["dataset_id"] == None:
                log = "to_dataset_linked_status(): the model with id {} has not an associated dataset".format(model_found["_id"])
                logging.debug(log)
                training_process_logs.append(log)
                model_status = ModelStatus.ERROR
        else:
            dataset_found = await find_one_dataset(str(model_found["dataset_id"]))

            if dataset_found == None:
                    log = "to_dataset_linked_status(): the model with id {} has not an associated dataset".format(model_found["_id"])
                    logging.debug(log)
                    training_process_logs.append(log)
                    model_status = ModelStatus.ERROR

        await update_one_model(model_found["_id"], {
            "status": model_status,
            "training_process_logs": training_process_logs,
            "updated_at": datetime.fromtimestamp(int(time()))
        })
        
        logging.debug("to_dataset_linked_status(): model with id {} updated to the {} status".format(model_found["_id"], model_status))
    except Exception as error:
        logging.error(f"to_dataset_linked_status(): error occurred during the model training process: {error}")
        raise Exception