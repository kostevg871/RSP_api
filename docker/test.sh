#!/bin/bash


alembic -c alembic_test.ini upgrade head

pytest --tb=long -vv 