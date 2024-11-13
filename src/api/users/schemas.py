from datetime import datetime
import re
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, constr

from pydantic import EmailStr
from pydantic import field_validator

#########################
# BLOCK WITH API MODELS #
#########################

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ShowUser(TunedModel):
    user_id: int
    name: str
    email: EmailStr
    is_active: bool
    registered_at: datetime
    roles: list[str]


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value


class DeleteUserResponse(BaseModel):
    deleted_user_id: int


class UpdatedUserResponse(BaseModel):
    updated_user_id: int


class UpdatedUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

    @field_validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value


class Token(BaseModel):
    access_token: str
    token_type: str
