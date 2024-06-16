from pydantic import BaseModel

# Ошибка с описанием


class Schemas_exception_400(BaseModel):
    detail: str

# 441 Неправильный запрос параметра mode


class Schema_exception_441_info(BaseModel):
    message: str
    available_modes: list[str]
    status_code: int


class Schemas_exception_441(BaseModel):
    detail: Schema_exception_441_info

# 442 неправильный расчет или запрос размерностей


class Schema_exception_442_info(BaseModel):
    message: str
    available_param_dimensions: list[list[str]]
    available_property_dimensions: list[list[str]]


class Schemas_exception_442(BaseModel):
    detail: Schema_exception_442_info


class Schema_exception_443_info(BaseModel):
    message: str
    available_property_dimensions: list[list[str]]


class Schemas_exception_443(BaseModel):
    detail: Schema_exception_443_info

# 444 Ошибка при переводе и непаладках в расчете таблицы


class Schema_exception_444_info(BaseModel):
    message: str
    available_param_dimensions: list[list[str]]


class Schemas_exception_444(BaseModel):
    detail: Schema_exception_444_info
