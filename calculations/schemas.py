from pydantic import BaseModel


class AvailableSubstance(BaseModel):
    data: list[str]
    count: int


class CalcModel(BaseModel):
    calc_modes: list[str]


class CalcModelResponce(BaseModel):
    data: CalcModel
    count: int
