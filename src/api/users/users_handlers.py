from logging import getLogger

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


from src.api.users.actions.user import _create_new_user
from src.api.users.schemas import ShowUser, UserCreate

from src.core.database.session import get_db

logger = getLogger(__name__)

router_users = APIRouter()


@router_users.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
