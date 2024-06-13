from typing import Final
from pymongo import ASCENDING

DEFAULT_PAGINATION_OFFSET: Final[int] = 0
DEFAULT_PAGINATION_LIMIT: Final[int] = 10
DEFAULT_PAGINATION_SORT_NAME: Final[str] = "created_at"
DEFAULT_PAGINATION_SORT_DIRECTION: Final[int] = ASCENDING