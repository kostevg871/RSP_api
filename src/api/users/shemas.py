import uuid
from fastapi import HTTPException
from pydantic import ConfigDict, BaseModel, EmailStr, field_validator

from src.helpers.letter_match_pattern import LETTER_MATCH_PATTERN


class TunedModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ShowUser(TunedModel):
    user_id: int
    username: str
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    username: str
    email: EmailStr

    @field_validator("username")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="UserName should contains only letters"
            )
        return value
