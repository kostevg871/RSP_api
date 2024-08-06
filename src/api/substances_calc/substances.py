from fastapi import APIRouter
from typing_extensions import Annotated

from src.api.substances_calc.requests.available_substances import available_substances
from src.api.substances_calc.requests.calc_model_substanse import calc_model_substanse
from src.api.substances_calc.requests.properties_list import properties_list
from src.api.substances_calc.requests.property_table import property_table
from src.api.substances_calc.requests.property_table_row import property_table_row

from src.api.substances_calc.response_model import model_error_400, model_error_441, model_error_442, model_error_443, model_error_444


from src.schemas import *


router_substances = APIRouter()

substaneces_objects_globals = InitRSP()


@router_substances.get("/getAvailableSubstances",
                       response_model=AvailableSubstance,
                       description="Получение всех доступных веществ")
def get_available_substances() -> AvailableSubstance:
    return available_substances(substaneces_objects_globals)


@router_substances.get("/getCalcModesInfo",
                       responses={
                           200: {"model": ParameterMode},
                           400: model_error_400
                       },
                       description="Запрос для получения Режима параметров")
def get_calc_model_substanse(id: int) -> ParameterMode:
    return calc_model_substanse(substaneces_objects_globals, id)


@router_substances.get("/getPropertiesLists",
                       responses={
                           200: {"model": Property},
                           400: model_error_400
                       },
                       description="Запрос для получения возможных Параметров для выбранного вещества и режима")
def get_properties_list(substanceId: int,
                        modeId: str) -> Property:
    return properties_list(substaneces_objects_globals, substanceId, modeId)


@router_substances.post("/getPropertiesTableRow",
                        responses={
                            200: {"model": PropertyRowTableResponse},
                            400: model_error_400,
                        },
                        description="Запрос для получения строки таблицы по параметру")
def get_properties_table_row(request: PropertyRowTableRequest) -> PropertyRowTableResponse:
    return property_table_row(substaneces_objects_globals,
                              request.substanceId,
                              request.modeId,
                              request.params.property,
                              request.params)


@router_substances.post("/getPropertiesTable",
                        responses={
                            200: {"model": PropertyRowTableResponse},
                            400: model_error_400,
                        },
                        description="Запрос для получения таблицы значений по каждому параметру")
def get_properties_table(request: PropertyTableRequest) -> PropertyTableResponse:
    return property_table(substaneces_objects_globals=substaneces_objects_globals,
                          substanceId=request.substanceId,
                          modeId=request.modeId,
                          params=request.params)
