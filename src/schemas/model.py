from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict
from ..enums.model_type import ModelType
from ..enums.classifier_type import ClassifierType
from ..enums.model_status import ModelStatus

class Model(BaseModel):
    # General
    name: str = Field()
    description: str = Field()
    type: ModelType = Field()
    classifier_type: ClassifierType = Field()
    status: ModelStatus = Field()
    tags: List[str] = Field()
    dataset_id: Optional[str] = Field(default = None)
    hyperparameters: Dict = Field(default = {})

    # Training Process
    trained_model_file_id: Optional[str] = Field(default = None)

    # Timing
    created_at: datetime = Field()
    updated_at: datetime = Field()

    # Logging
    training_process_started_at: Optional[datetime] = Field(default = None)
    training_process_ended_at: Optional[datetime] = Field(default = None)
    training_process_logs: Optional[List[str]] = Field(default = None)

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "name": "MyTestingClassificationModel",
                "description": "A classification model for testing purposes",
                "type": "CLASSIFICATION",
                "classifier_type": "LOGISTIC_CLASSIFIER",
                "status": "CREATED",
                "tags": (
                    "test",
                    "classification",
                    "perceptron",
                    "ai"
                ),
                "dataset_id": "mongo_id",
                "hyperparameters": {
                    "max_iter": "500"
                },
                "trained_model_file_id": "mongo_id",
                "created_at": "0",
                "updated_at": "0"
            }
        }