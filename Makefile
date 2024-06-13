include .env

docker-up-db:
	docker-compose -f docker-compose-db.yml up -d

docker-build:
	docker build -t ${DOCKER_MICROSERVICE_IMAGE_NAME} .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f ${DOCKER_MICROSERVICE_CONTAINER_NAME} --tail=50

clean:
	find . | grep -E "\(/__pycache__$|\.pyc$|\.pyo$\)" | xargs rm -rf