#!/bin/bash


poetry run alembic -c alembic.ini upgrade head

poetry run gunicorn src.app:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000