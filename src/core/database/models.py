from datetime import datetime, timezone
from sqlalchemy import TIMESTAMP, Boolean, Column, String, Integer
from sqlalchemy.orm import declarative_base

##############################
# BLOCK WITH DATABASE MODELS #
##############################

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)
    registered_at = Column(TIMESTAMP(timezone=True),
                           default=lambda: datetime.now(timezone.utc))
