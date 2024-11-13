up:
	docker compose -f docker-compose-local.yaml up -d
	poetry run bash docker/migrations.sh

down:
	docker compose -f docker-compose-local.yaml down && docker network prune --force

test:
	poetry run bash docker/test.sh

download:
	bash docker/rsp-download.sh
	poetry run python3.12 rsp_install.py

run local:
	poetry run uvicorn src.app:app --reload
