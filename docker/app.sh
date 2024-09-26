#!/bin/bash


alembic upgrade head
#uvicorn src.app:app --reload
#gunicorn src.app:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

gunicorn src.app:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000