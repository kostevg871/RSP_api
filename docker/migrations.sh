#!/bin/bash

sleep 5
#alembic upgrade head
alembic -c alembic.ini upgrade head
alembic -c alembic.ini upgrade head