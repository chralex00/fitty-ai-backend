from typing import Final, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class EnvVars(BaseSettings):
    MICROSERVICE_PORT: int
    MICROSERVICE_NAME: str
    MICROSERVICE_VERSION: str
    MICROSERVICE_API_PREFIX: str
    MICROSERVICE_WEB_WORKERS: int

    MODELS_CRONJOB_ENABLED: bool
    MODELS_CRONJOB_REPEATED_EVERY: int

    MONGODB_URL: str
    
    DOCKER_MONGODB_CONTAINER_EXPOSED_PORT: Optional[int]
    DOCKER_MONGOEXPRESS_CONTAINER_EXPOSED_PORT: Optional[int]

    DOCKER_MICROSERVICE_IMAGE_NAME: Optional[str]
    DOCKER_MICROSERVICE_CONTAINER_NAME: Optional[str]
    DOCKER_MICROSERVICE_CONTAINER_EXPOSED_PORT: Optional[int]

    model_config = SettingsConfigDict(env_file = ".env")

ENV_VARS: Final[EnvVars] = EnvVars()