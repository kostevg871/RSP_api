from fastapi import APIRouter

from src.api.users.shemas import UserRead, UserUpdate
from src.api.users.users_router import fastapi_users


router_users = APIRouter(
    prefix="/users",
    tags=["Users"]

)

# /me
# /{id}
router_users.include_router(
    router=fastapi_users.get_users_router(UserRead, UserUpdate)
)
