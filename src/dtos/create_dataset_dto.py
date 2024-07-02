from pydantic import BaseModel, Field
from typing import Set

class CreateDatasetDto(BaseModel):
    # General
    name: str = Field(min_length = 1, max_length = 128)
    description: str = Field(min_length = 1, max_length = 1024)
    tags: Set[str] = Field(min_length = 0, max_length = 15)

    # Test & Train Subsets
    primary_key_column_name: str = Field(min_length = 1, max_length = 256)
    features_column_names: Set[str] = Field(min_length = 0, max_length = 10)
    target_column_name: str = Field(min_length = 1, max_length = 256)
    test_samples_size: float = Field(min = 0, max = 1)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "MyTestingDataset",
                "description": "A generic dataset for testing purposes",
                "tags": (
                    "test",
                    "machine learning",
                    "dataset",
                    "ai"
                ),
                "primary_key_column_name": "id",
                "features_column_names": [
                    "feature_1",
                    "feature_2",
                    "feature_3",
                    "...",
                    "feature_n"
                ],
                "target_column_name": "y",
                "test_samples_size": "0.25"
            }
        }