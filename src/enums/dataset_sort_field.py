from enum import Enum

class DatasetSortField(str, Enum):
    NAME = "name"
    TYPE = "type"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"