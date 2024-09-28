from envparse import Env
from dotenv import load_dotenv

import os

load_dotenv()

env = Env()
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")
DB_HOST_REAL_DB = os.environ.get("DB_HOST_REAL_DB")

REAL_DATA_BASE = env.str(
    "REAL_DATA_BASE_URL",
    default=f"postgresql+asyncpg://{DB_USER}:{
        DB_PASS}@{DB_HOST_REAL_DB}:{DB_PORT}/{DB_NAME}"
)
