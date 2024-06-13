from enum import Enum

class ModelType(str, Enum):
    REGRESSION = "REGRESSION"
    CLASSIFICATION = "CLASSIFICATION"