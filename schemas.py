from fastapi import Query
from typing_extensions import Annotated
from pydantic import BaseModel


from init import InitRSP
# Схемы ответов
# схема вещества


class Substance(BaseModel):
    value: str
    label: str

# Схема ответа для вещества


class AvailableSubstance(BaseModel):
    data: list[Substance]

# Схема расчета


class ModelCalcInfo(BaseModel):
    value: str
    filter_params: list[str]


# запрос 3


class ParameterMode(AvailableSubstance):
    data: list[ModelCalcInfo]


class Property(BaseModel):
    data: dict[str, str]


# Для запроса 4
class Params(BaseModel):
    property: str
    value: list[float]
    dimension: str


init = InitRSP()


class PropertyTableRequest(BaseModel):
    substanceId: int  # id выбранного вещества
    modeId: str  # id выбранного режима
    params: Params


class PropertyRowDataResponse(BaseModel):
    dimension: str
    propertyId: str
    value: float


class PropertyRowTableResponse(BaseModel):
    data: PropertyRowDataResponse


class PropertyTableResponse(BaseModel):
    data: list[PropertyRowDataResponse]
        
