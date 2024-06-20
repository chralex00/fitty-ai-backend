from pydantic import BaseModel, Field
from typing import Optional, Set
from ..enums.dataset_type import DatasetType
from ..enums.dataset_sort_field import DatasetSortField
from ..enums.sort_direction import SortDirection

class DatasetQueryConfig(BaseModel):
    # Pagination
    offset: Optional[int] = Field(default = 0, min = 0)
    limit: Optional[int] = Field(default = 10, min = 5, max = 50)
    sort_field: Optional[DatasetSortField] = Field(default = None)
    sort_direction: Optional[SortDirection] = Field(default = None)

    # General
    name: Optional[str] = Field(default = None, min_length = 1, max_length = 256)
    type: Optional[DatasetType] = Field(default = None)
    tags: Optional[Set[str]] = Field(default = None, min_length = 0, max_length = 15)
    
    # Test & Train Subsets
    primary_key_column_name: Optional[str] = Field(default = None, min_length = 1, max_length = 256)
    target_column_name: Optional[str] = Field(default = None, min_length = 1, max_length = 256)
    test_samples_size_min: Optional[float] = Field(default = None, min = 0, max = 1)
    test_samples_size_max: Optional[float] = Field(default = None, min = 0, max = 1)

    # Timing
    created_at_min: Optional[int] = Field(default = None, min = 0)
    created_at_max: Optional[int] = Field(default = None, min = 0)
    updated_at_min: Optional[int] = Field(default = None, min = 0)
    updated_at_max: Optional[int] = Field(default = None, min = 0)

    class Config:
        json_schema_extra = {
            "example": {
                "offset": 0,
                "limit": 10,
                "sort_field": "name",
                "sort_direction": 1,
                "name": "MyTestingDataset",
                "type": "CSV",
                "tags": [
                    "test",
                    "classification",
                    "dataset",
                    "ai"
                ],
                "primary_key_column_name": "id",
                "target_column_name": "y",
                "test_samples_size_min": "0.25",
                "test_samples_size_max": "0.55",
                "created_at_min": "1000",
                "created_at_max": "1000000",
                "updated_at_min": "1000",
                "updated_at_max": "1000000"
            }
        }