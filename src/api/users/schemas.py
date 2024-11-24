from datetime import datetime
import re
from typing import Optional

from pydantic import BaseModel, ConfigDict

from pydantic import EmailStr
from pydantic import field_validator

from src.api.users.validate_users.validate_users import validate_email, validate_name

#########################
# BLOCK WITH API MODELS #
#########################


class TunedModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ShowUser(TunedModel):
    user_id: int
    name: str
    email: str
    is_active: bool
    registered_at: datetime
    roles: list[str]


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

    @field_validator("name")
    def validate_name_wrapper(cls, value):
        return validate_name(value)

    @field_validator("email")
    def validate_email_wrapper(cls, value):
        return validate_email(value)


class DeleteUserResponse(BaseModel):
    deleted_user_id: int


class UpdatedUserResponse(BaseModel):
    updated_user_id: int


class UpdatedUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

    @field_validator("name")
    def validate_name_wrapper(cls, value):
        return validate_name(value)

    @field_validator("email")
    def validate_email_wrapper(cls, value):
        return validate_email(value)


class Token(BaseModel):
    access_token: str
    token_type: str
