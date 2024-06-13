# Fitty AI

A FastAPI project that uses Pandas, ScikitLearn and other dependencies to prepare and train machine learning models.

### Prerequisites

The following dependencies are required to run this microservice in a local environment:
- Python ^3.11.6
- Pip ^23.2.1

The following dependencies are required to run this microservice in a staging, or preprod environment:
- Docker ^24.0.6
- Docker Compose ^2.22.0

These dependencies are optional, but are still very convenient:
- GNU Make ^3.81

### Prepare the Python VENV

First, open any shell (zsh, bash, or other) and create a Python VENV (Virtual ENVironment) with this command:

```bash
python3 -m venv .venv
```

Then, actiavate the Python VENV with the command:

```bash
# MacOS, Linux
source ./.venv/bin/activate

# Windows
.venv\Scripts\activate
```

You can deactivate the Python VENV with the command:

```bash
deactivate
```

**IMPORTANT: Note that it's very important to run all `pip` and `python` commands into the Python VENV.**

### Configuring

This microservice requires a configuration file called `.env`. You can easily create the `.env` file by the `env_example` file, with the following command:

```bash
cp env_example .env
```

The `env_example` file is an example contains a simple template of the `.env` file.

The contents of the .env file must include the following env variables:
- `MICROSERVICE_PORT` (required, `int`): the listening port, preferably between `8000` and `9000`, like `8080`, or `8090`.
- `MICROSERVICE_NAME` (required, `str`): the descriptive name of the microservice, or the brand name, like `fitty-ai-backend`.
- `MICROSERVICE_VERSION` (required, `str`): the microservice's version, strictly respecting semver (semantic versioning), like `v0.0.1-rc.1`.
- `MICROSERVICE_API_PREFIX` (required, `str`): the API's prefix exposed by this microserfice, like `/api`, or `/api/v1`.
- `MICROSERVICE_WEB_WORKERS` (optional, `int`): the number of web workers (or web processes). In local environment it should be set to `1`. Default value is `1`.
- `MONGODB_URL` (required, `str`): the connection string to allow the microservice to connect to the MongoDB server. The connection string must be expressed in the following format: `mongodb://{username}:{password}@{host}:{port}/{dbname}`. I fyou starting this microservice locally, the username and password of the MongoDB under Docker are `user` and `password`, while the database name is `fittyaidb`.
- `MODELS_CRONJOB_ENABLED` (required, boolean): a boolean value enables (or disables) the machine learning models management process. This process prepare, fit and test the machine learning models and it's managed by a simple cronjob. It can be `true`, or `false`.
- `MODELS_CRONJOB_REPEATED_EVERY` (required, int): an int values that specifies the time interval (expressed in seconds) between the cronjob execution and the next, like `10`, `30`, or `60`.

The following env variables are used for docker:
- `DOCKER_MICROSERVICE_IMAGE_NAME` (optional for local env, required for docker): the docker image name, like `fitty-ai-backend`.
- `DOCKER_MICROSERVICE_CONTAINER_NAME` (optional for local env, required for docker): the docker container name, like `fitty-ai-backend`.
- `DOCKER_MICROSERVICE_CONTAINER_EXPOSED_PORT` (optional for local env, required for docker): the listening port of the docker container, like `8090`, or `9000`.
- `DOCKER_MONGODB_CONTAINER_EXPOSED_PORT` (optional for local env, required for docker): the listening port of the MongoDB docker container name, like `28018`.
- `DOCKER_MONGOEXPRESS_CONTAINER_EXPOSED_PORT` (optional for local env, required for docker): the listening port of the Mongo Express docker container name, like `8082`.

### Installing

To install all required Python dependencies of this project, run the following command:

```bash
pip install -r requirements.txt
```

Sometimes, you may need to run the following command, if you install some new Python dependencies:

```bash
pip freeze > requirements.txt
```

### Running

##### Start mongodb as docker container

If you start this microservice in an on-premises environment, first of all, you need to start a MongoDB instance. You can do it easily like this:

```bash
# Directly using Docker Compose
docker-compose up -f docker-compose-db.yml -d

# Or using Makefile
make docker-up-db
```

##### Running microservice without docker

You can easily run this microservice through the following command:

```bash
python main.py
```

Once the microservice is started, you can see the docs (Swagger UI) at the `http://127.0.0.1:{MICROSERVICE_PORT}/docs` URL, while the API endpoint is `http://127.0.0.1:{MICROSERVICE_PORT}/api/v1`.

##### Running microservice with docker

First of all, you need to build the docker image of this microservice. So, run one of the following commands:

```bash
# Directly using Docker
docker build -t ${DOCKER_MICROSERVICE_IMAGE_NAME} .

# Or using the Makefile
make docker-build
```

Next, you can create and run the docker container:

```bash
# Directly using Docker Compose
docker-compose up -d

# Or using the Makefile
make docker-run
```

You can see the last `50` logs of the docker container with one of the following commands:

```bash
# Directly using Docker Compose
docker-compose logs -f ${DOCKER_MICROSERVICE_CONTAINER_NAME} --tail=50

# Or using the Makefile
make docker-logs
```

Finally, you can stop the docker service imn this way:

```bash
# Directly using Docker Compose
docker-compose down

# Or using the Makefile
make docker-down
```

### Cleaning

Usually, in Python VENV cache directories called `__pycache__` are created in each folder of the project in which there is at least one `.py` file. To easily delete these folders, just use the following command:

```bash
# Directly using the find command
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf

# Or using the Makefile
make clean
```