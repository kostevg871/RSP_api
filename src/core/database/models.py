from sqlalchemy import Boolean, Column, String, Integer
from sqlalchemy.orm import declarative_base

##############################
# BLOCK WITH DATABASE MODELS #
##############################

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)
