
from fastapi_users import FastAPIUsers

from src.api.auth.user_manger import get_user_manager
from src.api.auth.database import User
from src.core.authentication.backend import authentication_backend


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [authentication_backend],
)
