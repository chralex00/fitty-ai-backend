from pydantic import BaseModel, Field
from typing import Optional, Set

class UpdateDatasetDto(BaseModel):
    name: Optional[str] = Field(min_length = 1, max_length = 128)
    description: Optional[str] = Field(min_length = 1, max_length = 1024)
    tags: Optional[Set[str]] = Field(min_length = 0, max_length = 15)

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