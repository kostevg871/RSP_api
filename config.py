from dotenv import load_dotenv

import os

from pydantic import BaseModel

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
VERIFICATION_TOKEN_SECRET = os.environ.get(
    "APP_CONFIG__ACCESS_TOKEN__VERIFICATION_TOKEN_SECRET")
RESET_PASSWORD_TOKEN_SECRET = os.environ.get(
    "APP_CONFIG__ACCESS_TOKEN__RESET_PASSWORD_TOKEN_SECRET")


REPEAT_TOKEN = os.environ.get("APP_REPEAT_TOKEN")


LIFETIME_SECONDS: int = 3600
