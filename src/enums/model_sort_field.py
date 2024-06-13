from enum import Enum

class ModelSortField(str, Enum):
    NAME = "name"
    TYPE = "type"
    STATUS = "status"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"