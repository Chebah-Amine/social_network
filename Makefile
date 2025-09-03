# -d = detached / launch containers in background
# --build = force image rebuild before starting containers
start:
	docker compose up -d --build

stop: 
	docker compose down

logs: 
	docker compose logs -f

exec: 
	docker compose exec web bash