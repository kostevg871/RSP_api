#!/bin/bash


alembic -c alembic_test.ini upgrade head

pytest tests/test_users --tb=long -vv 