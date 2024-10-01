from logging import getLogger

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


from src.core.database.models import User
from src.api.users.actions.user import _create_new_user, _delete_user, _get_user_by_id, _update_user
from src.api.users.schemas import DeleteUserResponse, ShowUser, UpdatedUserRequest, UpdatedUserResponse, UserCreate

from src.core.database.session import get_db

logger = getLogger(__name__)

router_users = APIRouter()


@router_users.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(
            status_code=503, detail=f"Пользователь с e-mail: {body.email} уже существует")


@router_users.delete("/", response_model=DeleteUserResponse)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),

) -> DeleteUserResponse:
    delete_user = await _delete_user(user_id, db)
    if delete_user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return DeleteUserResponse(deleted_user_id=delete_user)


@router_users.get("/", response_model=ShowUser)
async def get_user_by_id(user_id: int,
                         db: AsyncSession = Depends(get_db),) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return user


@router_users.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(user_id: int,
                            body: UpdatedUserRequest,
                            db: AsyncSession = Depends(get_db)) -> UpdatedUserResponse:
    updated_user_params = body.model_dump(exclude_none=True)

    if updated_user_params == {}:
        raise HTTPException(
            status_code=404, detail="Выберите хотя бы один параметр для обновления")

    user = await _get_user_by_id(user_id, db)

    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )

    try:
        updated_user_id = await _update_user(updated_user_params=updated_user_params, session=db, user_id=user_id),
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(
            status_code=503, detail=f"Пользователь с e-mail: {body.email} уже существует")
    return UpdatedUserResponse(updated_user_id=updated_user_id[0])
