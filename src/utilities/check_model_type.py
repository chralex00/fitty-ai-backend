from ..enums.model_type import ModelType
from ..enums.classifier_type import ClassifierType
from fastapi import HTTPException, status

def check_model_type(model_type: ModelType, classifier_type: ClassifierType):
    classification_types = [
        ClassifierType.LOGISTIC_CLASSIFIER.value,
        ClassifierType.DECISION_TREE_CLASSIFIER.value,
        ClassifierType.MULTILAYER_PERCEPTRON_CLASSIFIER.value
    ]
    if (model_type == ModelType.CLASSIFICATION) and not(classifier_type in classification_types):
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = {
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": "UNPROCESSABLE ENTITY",
                "detail": f"classifier_type must be one of the following: {classification_types}",
                "error": True
            }
        )
    
    regression_types = [
        ClassifierType.LINEAR_REGRESSOR.value,
        ClassifierType.LASSO_REGRESSOR.value,
        ClassifierType.RIDGE_REGRESSOR.value,
        ClassifierType.ELASTIC_NETWORK_REGRESSOR.value,
        ClassifierType.KNN_REGRESSOR.value,
        ClassifierType.DECISION_TREE_REGRESSOR.value,
        ClassifierType.RANDOM_FOREST_REGRESSOR.value,
        ClassifierType.MULTILAYER_PERCEPTRON_REGRESSOR.value
    ]
    if (model_type == ModelType.REGRESSION) and not(classifier_type in regression_types):
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = {
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": "UNPROCESSABLE ENTITY",
                "detail": f"classifier_type must be one of the following: {regression_types}",
                "error": True
            }
        )