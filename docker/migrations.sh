#!/bin/bash

sleep 2
#alembic upgrade head
poetry run alembic -c alembic.ini upgrade head
poetry run alembic -c alembic.ini upgrade head