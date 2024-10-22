import asyncio
import os
from datetime import timedelta
from typing import Any
from typing import Generator

import asyncpg
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

import settings
from src.core.database.session import get_db
from src.app import app


CLEAN_TABLES = [
    "users",
]


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                table_for_cleaning = text(
                    f"TRUNCATE TABLE {table_for_cleaning};")
                await session.execute(table_for_cleaning)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(
        settings.TEST_DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


async def _get_test_db():
    try:
        # create async engine for interaction with database
        test_engine = create_async_engine(
            settings.TEST_DATABASE_URL, future=True, echo=True
        )

        # create session for the interaction with database
        test_async_session = sessionmaker(
            test_engine, expire_on_commit=False, class_=AsyncSession
        )
        yield test_async_session()
    finally:
        pass


@pytest.fixture(scope="session")
async def client():
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(
        "".join(settings.TEST_DATABASE_URL.split("+asyncpg"))
    )
    try:
        yield pool
    finally:
        await pool.close()


@pytest.fixture
async def get_user_from_database(asyncpg_pool):
    async def get_user_from_database_by_int(user_id: int):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch(
                "SELECT * FROM users WHERE user_id = $1;", user_id
            )

    return get_user_from_database_by_int


@pytest.fixture
async def create_user_in_database(asyncpg_pool):
    async def create_user_in_database(
        user_id: str,
        name: str,
        email: str,
        hashed_password: str,

    ):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                """INSERT INTO users VALUES ($1, $2, $3, $4)""",
                user_id,
                name,
                email,
                hashed_password,
            )

    return create_user_in_database
