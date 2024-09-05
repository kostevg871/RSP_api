from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    role_id: int | None
    username: str


class UserCreate(schemas.BaseUserCreate):
    username: str


class UserUpdate(schemas.BaseUserUpdate):
    username: str
