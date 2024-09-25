#!/bin/bash

alembic upgrade head

cd src 

CMD gunicorn src:app --workers 4 --workers-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000