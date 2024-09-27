from envparse import Env

env = Env()

REAL_DATA_BASE = env.str(
    "REAL_DATA_BASE_URL",
    default="postgresql+asyncpg://${DB_USER}:${DB_PASS}@${DB_HOST_REAL_DB}:${DB_PORT}/${DB_NAME}"
)
