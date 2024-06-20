from pydantic import BaseModel, Field
from typing import Optional, Set
from ..enums.model_type import ModelType
from ..enums.classifier_type import ClassifierType
from ..enums.model_status import ModelStatus
from ..enums.model_sort_field import ModelSortField
from ..enums.sort_direction import SortDirection

class ModelQueryConfig(BaseModel):
    # Pagination
    offset: Optional[int] = Field(default = 0, min = 0)
    limit: Optional[int] = Field(default = 10, min = 5, max = 50)
    sort_field: Optional[ModelSortField] = Field(default = None)
    sort_direction: Optional[SortDirection] = Field(default = None)

    # General
    name: Optional[str] = Field(default = None, min_length = 1, max_length = 256)
    type: Optional[ModelType] = Field(default = None)
    classifier_type: Optional[ClassifierType] = Field(default = None)
    status: Optional[ModelStatus] = Field(default = None)
    tags: Optional[Set[str]] = Field(default = None, min_length = 0, max_length = 15)

    # Timing
    created_at_min: Optional[int] = Field(default = None, min = 0)
    created_at_max: Optional[int] = Field(default = None, min = 0)
    updated_at_min: Optional[int] = Field(default = None, min = 0)
    updated_at_max: Optional[int] = Field(default = None, min = 0)

    # Training Process Management
    training_process_started_at_min: Optional[int] = Field(default = None, min = 0)
    training_process_started_at_max: Optional[int] = Field(default = None, min = 0)
    training_process_ended_at_min: Optional[int] = Field(default = None, min = 0)
    training_process_ended_at_max: Optional[int] = Field(default = None, min = 0)

    class Config:
        json_schema_extra = {
            "example": {
                "offset": 0,
                "limit": 10,
                "sort_field": "name",
                "sort_direction": 1,
                "name": "MyTestingClassificationModel",
                "type": "CLASSIFICATION",
                "classifier_type": "LOGISTIC_CLASSIFIER",
                "status": "TRAINING",
                "tags": [
                    "test",
                    "classification",
                    "perceptron",
                    "ai"
                ],
                "created_at_min": "1000",
                "created_at_max": "1000000",
                "updated_at_min": "1000",
                "updated_at_max": "1000000",
                "training_process_started_at_min": "1000",
                "training_process_started_at_max": "1000000",
                "training_process_ended_at_min": "1000",
                "training_process_ended_at_max": "1000000",
            }
        }