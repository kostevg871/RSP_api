from src.api.users.schemas import ShowUser
from src.api.users.schemas import UserCreate
from src.core.database.dals import UserDAL


async def _create_new_user(body: UserCreate, session) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            name=body.name,
            email=body.email,
        )
        return ShowUser(
            user_id=user.user_id,
            name=user.name,
            email=user.email,
            is_active=user.is_active,
            registered_at=user.registered_at
        )
