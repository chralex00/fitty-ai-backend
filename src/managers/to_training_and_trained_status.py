from ..utilities.logging import LOGGER as logging
from ..utilities.mongo_connection import GRIDFS_MONGODB
from ..dtos.model_query_config import ModelQueryConfig
from ..schemas.model import Model
from ..services.model import search_many as search_model, update_one as update_one_model
from ..services.dataset import find_one as find_one_dataset, update_one as update_one_dataset
from ..enums.classifier_type import ClassifierType
from ..enums.model_status import ModelStatus
from datetime import datetime
from time import time
from pandas import DataFrame
import pandas as pd
import pickle
import io
from typing import Dict
from datetime import datetime
from .classifiers import logistic_classifier, multilayer_perceptron_classifier, decision_tree_classifier
from .regressors import linear_regressor, lasso_regressor, ridge_regressor, elastic_network_regressor, knn_regressor, linear_support_vector_machine_regressor, decision_tree_regressor, random_forest_regressor, neural_network_regressor

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

            global trained_model

            hyperparameters: Dict = model_found["hyperparameters"]
            X_columns = dataset_found["features_column_names"]
            y_column = dataset_found["target_column_name"]

            # for classification
            if model_found["classifier_type"] == ClassifierType.LOGISTIC_CLASSIFIER:
                trained_model = logistic_classifier(
                    df,
                    hyperparameters["random_state"],
                    X_columns,
                    y_column
                )
            elif model_found["classifier_type"] == ClassifierType.MULTILAYER_PERCEPTRON_CLASSIFIER:
                trained_model = multilayer_perceptron_classifier(
                    df,
                    hyperparameters["random_state"],
                    hyperparameters["hidden_layer_sizes"],
                    hyperparameters["max_iter"],
                    X_columns,
                    y_column
                )
            elif model_found["classifier_type"] == ClassifierType.DECISION_TREE_CLASSIFIER:
                trained_model = decision_tree_classifier(
                    df,
                    hyperparameters["random_state"],
                    hyperparameters["max_depth"],
                    hyperparameters["class_weight"],
                    X_columns,
                    y_column
                )

            # for regression
            if model_found["classifier_type"] == ClassifierType.LINEAR_REGRESSOR:
                trained_model = linear_regressor(
                    df,
                    X_columns,
                    y_column
                )
            elif model_found["classifier_type"] == ClassifierType.LASSO_REGRESSOR:
                trained_model = lasso_regressor(
                    df,
                    hyperparameters["alpha"],
                    X_columns,
                    y_column
                )
            elif model_found["classifier_type"] == ClassifierType.RIDGE_REGRESSOR:
                trained_model = ridge_regressor(
                    df,
                    hyperparameters["alpha"],
                    X_columns,
                    y_column
                )
            elif model_found["classifier_type"] == ClassifierType.ELASTIC_NETWORK_REGRESSOR:
                trained_model = elastic_network_regressor(
                    df,
                    hyperparameters["alpha"],
                    hyperparameters["l1_ratio"],
                    X_columns,
                    y_column
                )
            elif model_found["classifier_type"] == ClassifierType.KNN_REGRESSOR:
                trained_model = knn_regressor(
                    df,
                    hyperparameters["n_neighbors"],
                    hyperparameters["weights"],
                    hyperparameters["metric"],
                    X_columns,
                    y_column
                )
            elif model_found["classifier_type"] == ClassifierType.DECISION_TREE_REGRESSOR:
                trained_model = decision_tree_regressor(
                    df,
                    hyperparameters["random_state"],
                    hyperparameters["max_depth"],
                    X_columns,
                    y_column
                )
            elif model_found["classifier_type"] == ClassifierType.LINEAR_SUPPORT_VECTOR_MACHINE:
                trained_model = decision_tree_regressor(
                    df,
                    hyperparameters["random_state"],
                    hyperparameters["max_depth"],
                    X_columns,
                    y_column
                )
            elif model_found["classifier_type"] == ClassifierType.RANDOM_FOREST_REGRESSOR:
                trained_model = random_forest_regressor(
                    df,
                    hyperparameters["random_state"],
                    hyperparameters["max_depth"],
                    hyperparameters["n_estimators"],
                    X_columns,
                    y_column
                )
            elif model_found["classifier_type"] == ClassifierType.MULTILAYER_PERCEPTRON_REGRESSOR:
                trained_model = multilayer_perceptron_classifier(
                    df,
                    hyperparameters["random_state"],
                    hyperparameters["hidden_layer_sizes"],
                    hyperparameters["max_iter"],
                    X_columns,
                    y_column
                )
        except Exception as error:
            model_found["training_process_logs"].append("to_training_and_trained_status(): error occurred while creating and handling the data frame for model with the id {}, the error is: {}".format(model_found["_id"], error))
            await update_one_model(model_found["_id"], {
                "status": ModelStatus.ERROR,
                "training_process_logs": model_found["training_process_logs"],
                "updated_at": datetime.fromtimestamp(int(time()))
            })
            logging.debug("to_training_and_trained_status(): model with id {} updated to the {} status".format(model_found["_id"], ModelStatus.ERROR))
            return

        buffer = io.BytesIO()
        pickle.dump(trained_model, buffer)
        buffer.seek(0)

        trained_model_file_id = GRIDFS_MONGODB.put(buffer)

        await update_one_model(model_found["_id"], {
            "status": ModelStatus.TRAINED,
            "trained_model_file_id": trained_model_file_id,
            "training_process_logs": [],
            "updated_at": datetime.fromtimestamp(int(time()))
        })

        logging.debug("to_training_and_trained_status(): model with id {} updated to the {} status".format(model_found["_id"], ModelStatus.TRAINED))
    except Exception as error:
        logging.error(f"to_training_and_trained_status(): error occurred during the model training process: {error}")
        raise Exception