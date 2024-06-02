from fastapi import APIRouter
from typing_extensions import Annotated

from api.requests.available_substances import available_substances
from api.requests.calc_model_substanse import calc_model_substanse
from api.requests.exception.exception_schemas import HTTPError, Schemas_exception_441, Schemas_exception_442, Schemas_exception_443
from api.requests.properties_list import properties_list
from api.requests.property_table import property_table
from api.requests.property_table_row import property_table_row


from schemas import *


router_substances = APIRouter()

substaneces_objects_globals = InitRSP()


@router_substances.get("/getAvailableSubstances", response_model=AvailableSubstance,
                       description="Получение всех доступных веществ")
def get_available_substances() -> AvailableSubstance:
    response = available_substances(substaneces_objects_globals)
    return response


@router_substances.get("/getCalcModesInfo", response_model=ParameterMode,
                       description="Запрос для получения Режима параметров")
def get_calc_model_substanse(id: Annotated[int, Query(ge=0, lt=len(substaneces_objects_globals.data_get_substances_list))]) -> ParameterMode:
    response = calc_model_substanse(substaneces_objects_globals, id)
    return response


@router_substances.get("/getPropertiesLists", responses={
    200: {"model": Property},
    441: {
        "model": Schemas_exception_441,
    }
},
    description="Запрос для получения возможных Параметров для выбранного вещества и режима")
def get_properties_list(substanceId: Annotated[int, Query(ge=0, lt=len(substaneces_objects_globals.data_get_substances_list))],
                        modeId: str) -> Property:

    response = properties_list(
        substaneces_objects_globals, substanceId, modeId)
    return response


@router_substances.post("/getPropertiesTableRow",
                        responses={
                            200: {"model": PropertyRowTableResponse},
                            400: {
                                "model": HTTPError,
                            },
                            441: {
                                "model": Schemas_exception_441,
                            },
                            442: {
                                "model": Schemas_exception_442,
                            },
                            443: {
                                "model": Schemas_exception_443,
                            }


                        },
                        description="Запрос для получения строки таблицы по параметру")
def get_properties_table_row(request: PropertyRowTableRequest) -> PropertyRowTableResponse:
    response = property_table_row(substaneces_objects_globals, request.substanceId, request.modeId,
                                  request.params.property, request.params)
    return response


@router_substances.post("/getPropertiesTable",
                        responses={
                            200: {"model": PropertyRowTableResponse},
                            400: {
                                "model": HTTPError,
                            },
                            442: {
                                "model": Schemas_exception_442,
                            }

                        },
                        description="Запрос для получения таблицы значений по каждому параметру")
def get_properties_table(request: PropertyTableRequest) -> PropertyTableResponse:
    response = property_table(substaneces_objects_globals=substaneces_objects_globals,
                              substanceId=request.substanceId,
                              modeId=request.modeId,
                              params=request.params)
    return response
