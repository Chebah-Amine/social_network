# -d = detached / launch containers in background
# --build = force image rebuild before starting containers
start:
	docker compose -f ./docker/docker-compose.yml up -d --build

stop: 
	docker compose -f ./docker/docker-compose.yml down

logs: 
	docker compose -f ./docker/docker-compose.yml logs -f

exec: 
	docker compose -f ./docker/docker-compose.yml exec web bash