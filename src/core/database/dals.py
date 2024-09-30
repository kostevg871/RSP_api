from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession


from src.core.database.models import User


###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self,
        name: str,
        email: str,

    ) -> User:
        new_user = User(
            name=name,
            email=email,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user
