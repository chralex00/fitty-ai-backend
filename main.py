import uvicorn
from fastapi import FastAPI
from src.utilities.env_vars import ENV_VARS
from src.controllers.healthcheck import healthcheck_router
from src.controllers.model import model_router
from src.controllers.dataset import dataset_router
from src.managers.training_process import TRAINING_PROCESS_MANAGER
from fastapi_utilities import repeat_every

app = FastAPI()

app.include_router(healthcheck_router, prefix = ENV_VARS.MICROSERVICE_API_PREFIX)
app.include_router(model_router, prefix = ENV_VARS.MICROSERVICE_API_PREFIX)
app.include_router(dataset_router, prefix = ENV_VARS.MICROSERVICE_API_PREFIX)

@app.on_event("startup")
@repeat_every(wait_first = 5, seconds = ENV_VARS.MODELS_CRONJOB_REPEATED_EVERY)
async def manage_models_cronjob():
    if TRAINING_PROCESS_MANAGER.running == False:
        await TRAINING_PROCESS_MANAGER.training_process()

if __name__ == "__main__":
    config = uvicorn.Config(
        app,
        host = "localhost",
        port = ENV_VARS.MICROSERVICE_PORT,
        workers = ENV_VARS.MICROSERVICE_WEB_WORKERS
    )
    uvicorn.Server(config).run()