#!/bin/bash

echo "Установка rsp"

poetry run python3.12 rsp_install.py 

echo "Запуск миграций..."

sleep 3
poetry run alembic -c alembic.ini upgrade head


echo "Запуск приложения..."

poetry run gunicorn src.app:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000