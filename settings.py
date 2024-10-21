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


TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default=f"postgresql+asyncpg://postgres_test:postgres_test@0.0.0.0:5433/postgres_test"
)


SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")

ALGORITHM: str = env.str("ALGORITHM", default="HS256")

ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int(
    "ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
