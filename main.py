import re
from typing import Union

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import EmailStr, field_validator
from sqlalchemy import Boolean, Column, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uvicorn
import settings

import uuid

from init import InitRSP
from schemas import *

import rsp


# db

engine = create_async_engine(settings.REAL_DATA_BASE, future=True, echo=True)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)


# db models

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)

# interaction with database in bussines context


class UserDAL:
    "Data Access Layer for operating user info"

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, name: str, surname: str, email: str) -> User:
        new_user = User(name=name, surname=surname, email=email,)
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user


# api models

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        """pydantic to convert even non dict obj to json"""

        from_attributes = True


class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr

    @field_validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


# api
app = FastAPI(
    title="RSP api"
)

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://real-substance-properties.netlify.app",
]

app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["GET", "POST", "OPTIONS",
                                  "DELETE", "PATCH", "PUT"],
                   allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                                  "Authorization"],)

app.substaneces_objects_globals = InitRSP()

substance_router = APIRouter()


@substance_router.get("/getAvailableSubstances", response_model=AvailableSubstance, description="Получение всех доступных веществ")
def get_available_substances() -> AvailableSubstance:
    return {"data": app.substaneces_objects_globals.data_get_substances_list}


@substance_router.get("/getCalcModesInfo", response_model=ParameterMode, description="Запрос для получения Режима параметров")
def get_calc_model_substanse(id: str) -> ParameterMode:
    return {"data": app.substaneces_objects_globals.data_get_calc_modes_info[int(id)]}


@substance_router.get("/getPropertiesLists", response_model=Property,  description="Запрос для получения возможных Параметров для выбранного вещества и режима")
def get_calc_model_substanse(substanceId: str, modeId: str) -> Property:
    return {"data": app.substaneces_objects_globals.properties[int(substanceId)][str(modeId)]}


@substance_router.post("/getPropertiesTableRow", response_model=PropertyRowTableResponse, description="Запрос для получения строки таблицы по параметру")
def get_properties_table(request: PropertyTableRequest) -> PropertyRowTableResponse:
    val = rsp.callProperty(
        app.substaneces_objects_globals.substances_objects[int(
            request.substanceId)],
        request.params.propertyId,
        request.modeId,
        request.params.value)

    return {
        "data":
        {
            "dimensionId": "SI",
            "property": str(app.substaneces_objects_globals.properties[int(request.substanceId)][str(request.modeId)][request.params.propertyId]),
            "value": val
        }
    }


@substance_router.post("/getPropertiesTable", response_model=PropertyTableResponse, description="Запрос для получения таблицы значений по каждому параметру")
def get_properties_table(substanceId: str, modeId: str, parameters: list[float]) -> PropertyTableResponse:
    results = dict(zip(
        app.substaneces_objects_globals.properties[int(
            substanceId)][str(modeId)],
        [None] * len(app.substaneces_objects_globals.properties[int(substanceId)][str(modeId)])))
    for prop in app.substaneces_objects_globals.properties[int(substanceId)][str(modeId)]:
        results[str(prop)] = rsp.callProperty(
            app.substaneces_objects_globals.substances_objects[int(
                substanceId)],
            prop,
            modeId,
            parameters
        )

    print(results)

    return {"data": results}


user_router = APIRouter()


async def _create_new_user(body: UserCreate) -> ShowUser:
    async with async_session() as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email,
            )
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active,
            )


@user_router.post("/user", response_model=ShowUser)
async def create_user(body: UserCreate) -> ShowUser:
    return await _create_new_user(body)


main_api_router = APIRouter()
main_api_router.include_router(user_router, tags=["user"])
main_api_router.include_router(
    substance_router, tags=["substance"])

app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
