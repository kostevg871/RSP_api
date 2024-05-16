from envparse import Env

env = Env()

REAL_DATA_BASE = env.str(
    "REAL_DATA_BASE_URL",
    default="postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
)
