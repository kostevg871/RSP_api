from typing import Tuple
from pydantic import BaseModel

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
    label: list[str]


# запрос 3


class ParameterMode(AvailableSubstance):
    data: list[ModelCalcInfo]


class Property(BaseModel):
    data: dict[str, str]


# Для запроса 4
class Params(BaseModel):
    propertyId: str
    value: list[float]
    dimensionId: str


class PropertyTableRequest(BaseModel):
    substanceId: str  # id выбранного вещества
    modeId: str  # id выбранного режима
    params: Params


class PropertyRowDataResponse(BaseModel):
    dimensionId: str
    property: str
    value: float


class PropertyRowTableResponse(BaseModel):
    data: PropertyRowDataResponse

    
class PropertyTableResponse(BaseModel):
    data: dict[str, float]
