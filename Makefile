up:
	docker compose -f docker-compose-local.yaml up -d
	poetry run bash docker/migrations.sh

down:
	docker compose -f docker-compose-local.yaml down && docker network prune --force

test:
	docker compose -f docker-compose-local.yaml up -d
	sleep 3
	poetry run bash docker/test.sh
	docker compose -f docker-compose-local.yaml down && docker network prune --force

download:
	bash docker/rsp-download.sh
	poetry run python3.12 rsp_install.py

run:
	docker compose -f docker-compose-local.yaml up -d
	bash docker/migrations.sh
	poetry run uvicorn src.app:app --reload

start:
	docker compose -f docker-compose-ci.yaml --env-file .env_rsp up 

build:
	docker compose -f docker-compose-ci.yaml --env-file .env_rsp build

stop:
	docker compose -f docker-compose-local.yaml down && docker network prune --force
	docker compose -f docker-compose-ci.yaml down && docker network prune --force