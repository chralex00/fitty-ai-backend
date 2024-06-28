from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from ..enums.dataset_type import DatasetType

class Dataset(BaseModel):
    # General
    name: str = Field()
    description: str = Field()
    type: Optional[DatasetType] = Field(default = None)
    tags: List[str] = Field()
    file_object_id: Optional[str] = Field(default = None)

    # Test & Train Subsets
    primary_key_column_name: str = Field()
    target_column_name: str = Field()
    test_samples_size: float = Field()
    file_splited_object_id: Optional[str] = Field(default = None)

    # Timing
    created_at: datetime = Field()
    updated_at: datetime = Field()

    class Config:
        json_schema_extra = {
            "example": {
                "name": "MyTestingDataset",
                "description": "A generic dataset for testing purposes",
                "type": "CSV",
                "tags": (
                    "test",
                    "machine learning",
                    "dataset",
                    "ai"
                ),
                "file_object_id": "mongo_id",
                "primary_key_column_name": "id",
                "target_column_name": "y",
                "test_samples_size": "0.25",
                "file_splited_object_id": "mongo_id",
                "created_at": "0",
                "updated_at": "0"
            }
        }