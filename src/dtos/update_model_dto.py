from pydantic import BaseModel, Field
from typing import Optional, Set
from ..enums.model_type import ModelType
from ..enums.classifier_type import ClassifierType

class UpdateModelDto(BaseModel):
    name: Optional[str] = Field(default = None, min_length = 1, max_length = 128)
    description: Optional[str] = Field(default = None, min_length = 1, max_length = 1024)
    type: Optional[ModelType] = Field(default = None)
    classifier_type: Optional[ClassifierType] = Field(default = None)
    tags: Optional[Set[str]] = Field(default = None, min_length = 0, max_length = 15)
    dataset_id: Optional[str] = Field(default = None)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "MyTestingClassificationModel",
                "description": "A classification model for testing purposes",
                "type": "CLASSIFICATION",
                "classifier_type": "LOGISTIC_CLASSIFIER",
                "tags": (
                    "test",
                    "classification",
                    "perceptron",
                    "ai"
                )
            }
        }