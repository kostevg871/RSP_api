from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


metadata = MetaData()


role = Table(
    "role",
    metadata,

    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permison", JSON),
)


user = Table(
    "user",
    metadata,

    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False, unique=True),
    Column("username", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.now),
    Column("role_id", Integer, ForeignKey(role.c.id)),

    Column("is_active", Boolean, default=True),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False)
)
