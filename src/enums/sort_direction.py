from enum import Enum
from pymongo import ASCENDING, DESCENDING

class SortDirection(int, Enum):
    ASC = ASCENDING
    DESC = DESCENDING