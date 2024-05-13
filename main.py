from typing import Union

from fastapi import FastAPI

from init import InitRSP
from schemas import *

import rsp


app = FastAPI(
    title="RSP App"
)

app.substaneces_objects_globals = InitRSP()


@app.get("/getAvailableSubstances", response_model=AvailableSubstance, description="Получение всех доступных веществ")
def get_available_substances() -> AvailableSubstance:
    return {"data": app.substaneces_objects_globals.data_get_substances_list}


@app.get("/getCalcModesInfo", response_model=ParameterMode, description="Запрос для получения Режима параметров")
def get_calc_model_substanse(id: str) -> ParameterMode:
    return {"data": app.substaneces_objects_globals.data_get_calc_modes_info[int(id)]}


@app.get("/getPropertiesLists", response_model=Property,  description="Запрос для получения возможных Параметров для выбранного вещества и режима")
def get_calc_model_substanse(substanceId: str, modeId: str) -> Property:
    return {"data": app.substaneces_objects_globals.properties[int(substanceId)][str(modeId)]}


@app.post("/getPropertiesTableRow", response_model=PropertyRowTableResponse, description="Запрос для получения строки таблицы по параметру")
def get_properties_table(request: PropertyTableRequest) -> PropertyRowTableResponse:
    val = rsp.callProperty(
        app.substaneces_objects_globals.substances_objects[int(
            request.substanceId)],
        request.params.propertyId,
        request.modeId,
        request.params.value)

    return {
        "data":
        {
            "dimensionId": "SI",
            "property": str(app.substaneces_objects_globals.properties[int(request.substanceId)][str(request.modeId)][request.params.propertyId]),
            "value": str(val)
        }
    }
