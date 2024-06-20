from typing import Final
from fastapi import HTTPException, status
from pymongo import ASCENDING

# Default Values
DEFAULT_PAGINATION_OFFSET: Final[int] = 0
DEFAULT_PAGINATION_LIMIT: Final[int] = 10
DEFAULT_PAGINATION_SORT_NAME: Final[str] = "created_at"
DEFAULT_PAGINATION_SORT_DIRECTION: Final[int] = ASCENDING

# HTTP Exceptions
NOT_FOUND_HTTP_EXCEPTION: Final[HTTPException] = HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = {
    "status_code": status.HTTP_404_NOT_FOUND,
    "message": "NOT FOUND",
    "error": True
})

INTERNAL_SERVER_ERROR_HTTP_EXCEPTION: Final[HTTPException] = HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = {
    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
    "message": "INTERNAL SERVER ERROR",
    "error": True
})