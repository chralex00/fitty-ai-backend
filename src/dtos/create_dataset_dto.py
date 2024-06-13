from pydantic import BaseModel, Field
from typing import Set

class CreateDatasetDto(BaseModel):
    name: str = Field(min_length = 1, max_length = 128)
    description: str = Field(min_length = 1, max_length = 1024)
    tags: Set[str] = Field(min_length = 0, max_length = 15)

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
                )
            }
        }