from enum import Enum

class DatasetType(str, Enum):
    CSV = "CSV"
    EXCEL = "EXCEL"
    JSON = "JSON"
    XML = "XML"
    HTML = "HTML"
    PARQUET = "PARQUET"
