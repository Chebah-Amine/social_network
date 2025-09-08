# -d = detached / launch containers in background
# --build = force image rebuild before starting containers

DOCKERFILE_PATH = ./docker/docker-compose.yml

start:
	docker compose -f ${DOCKERFILE_PATH} up -d --build

stop: 
	docker compose -f ${DOCKERFILE_PATH} down

logs: 
	docker compose -f ${DOCKERFILE_PATH} logs -f

exec: 
	docker compose -f ${DOCKERFILE_PATH} exec web bash

test:
	docker compose -f ${DOCKERFILE_PATH} exec web sh -c "coverage run --source=network -m pytest && coverage report -m --include='*/network/views.py'"

format:
	docker compose -f ${DOCKERFILE_PATH} exec web black .

lint:
	docker compose -f ${DOCKERFILE_PATH} exec web flake8 --max-line-length=120 --statistics .

safety:
	docker compose -f ${DOCKERFILE_PATH} exec web safety check --full-report

bandit:
	docker compose -f ${DOCKERFILE_PATH} exec web bandit -r ./app/network
