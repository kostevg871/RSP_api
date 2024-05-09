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


class ParameterMode(AvailableSubstance):
    data: list[Substance]


class Property(BaseModel):
    data: list[str]
