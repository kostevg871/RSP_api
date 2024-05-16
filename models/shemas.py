import datetime
from pydantic import BaseModel


class RoleBase(BaseModel):
    id: int
    name: str
    permission: dict


class UserBase(BaseModel):
    id: int
    email: str
    username: str
    password: str
    register_at: datetime
    role: RoleBase
