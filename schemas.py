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


class Model(Substance):
    value: str
    label: str

# запрос 3
class ParameterMode(AvailableSubstance):
    data: list[str]


class Property(BaseModel):
    data: list[str]


# ~~~ жесть для запроса 4
class Params(BaseModel):
    propertyId: str
    value: list[float]
    dimensionId: str

class PropertyTableRequest(BaseModel):
    substanceId: str # id выбранного вещества
    modeId: str # id выбранного режима
    params: Params

class PropertyTableResponse(BaseModel):
    propertyId: str
    value: str
    dimensionId: str

# class PropertyTable(BaseModel):
#         data: PropertyTableResponse
