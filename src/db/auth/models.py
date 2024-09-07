from datetime import datetime, timezone

from sqlalchemy import MetaData, TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Table


metadata = MetaData()


user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False, unique=True),
    Column("username", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("registered_at", TIMESTAMP(timezone=True),
           default=lambda: datetime.now(timezone.utc)),

    Column("is_active", Boolean, default=True),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)

access_token = Table(
    "accesstoken",
    metadata,
    Column("user_id", Integer, ForeignKey(
        user.c.id, ondelete="cascade"), nullable=False),
    Column("token", String, nullable=False, unique=True),
    Column("created_at", TIMESTAMP(timezone=True),
           default=lambda: datetime.now(timezone.utc))
)
