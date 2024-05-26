from fastapi import Query
from typing_extensions import Annotated
from pydantic import BaseModel


from init import InitRSP

init = InitRSP()
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
    param_literals: list[str]
    param_dimensions: list[str]


# запрос 3


class ParameterMode(AvailableSubstance):
    data: list[ModelCalcInfo]


class Property(BaseModel):
    data: dict[str, str]


# Для запроса 4
class RowParams(BaseModel):
    property: str
    property_dimension: str
    param_values: list[float]
    param_dimensions: list[str]

class PropertyRowTableRequest(BaseModel):
    substanceId: int  # id выбранного вещества
    modeId: str  # id выбранного режима
    params: RowParams


class PropertyRowDataResponse(BaseModel):
    dimension: str
    propertyId: str
    value: float


class PropertyRowTableResponse(BaseModel):
    data: PropertyRowDataResponse

# Для запроса 5
class TableParams(BaseModel):
    param_values: list[float]
    param_dimensions: list[str]

class PropertyTableRequest(BaseModel):
    substanceId: int  # id выбранного вещества
    modeId: str  # id выбранного режима
    params: TableParams

class PropertyTableResponse(BaseModel):
    data: list[PropertyRowDataResponse]
        
