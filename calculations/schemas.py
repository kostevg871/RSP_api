from pydantic import BaseModel


class AvailableSubstance(BaseModel):
    data: list[str]
    count: int
