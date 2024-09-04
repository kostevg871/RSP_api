from fastapi import APIRouter

from src.api.users.shemas import UserCreate, UserRead
from src.api.users.users_router import fastapi_users
from src.core.authentication.backend import authentication_backend


router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"]

)

# /login
# /logout
router_auth.include_router(
    router=fastapi_users.get_auth_router(authentication_backend)
)

# /register
router_auth.include_router(
    router=fastapi_users.get_register_router(UserRead, UserCreate),
)
