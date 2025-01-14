from ..enums.model_status import ModelStatus
from fastapi import HTTPException, status

def check_model_status(model_status: ModelStatus):
    if model_status != ModelStatus.CREATED.value:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = {
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": "UNPROCESSABLE ENTITY",
                "detail": f"The model cannot be modified once it has begun the training process",
                "error": True
            }
        )