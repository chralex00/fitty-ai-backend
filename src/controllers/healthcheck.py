from fastapi import APIRouter, status, HTTPException
from ..utilities.env_vars import ENV_VARS
from typing import Dict
from ..utilities.logging import LOGGER as logging
from ..constants.constants import INTERNAL_SERVER_ERROR_HTTP_EXCEPTION

healthcheck_router = APIRouter()

@healthcheck_router.get("/healthcheck", tags = [ "Healthcheck" ])
async def healthcheck() -> Dict[str, str | int]:
    try:
        return {
            "microservice_name": ENV_VARS.MICROSERVICE_NAME,
            "microservice_version": ENV_VARS.MICROSERVICE_VERSION,
            "status": "on"
        }
    except Exception as error:
        logging.error(f"Error occurred during the Model creation: {error}")
        raise INTERNAL_SERVER_ERROR_HTTP_EXCEPTION