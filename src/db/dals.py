from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.database import User


class UserDAL:
    "Data Access Layer for operating user info"

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, username: str, email: str) -> User:
        new_user = User(username=username, email=email)
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user
