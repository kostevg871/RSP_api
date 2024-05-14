from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from init import InitRSP
from schemas import *

import rsp


app = FastAPI(
    title="RSP App"
)

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["GET", "POST", "OPTIONS",
                                  "DELETE", "PATCH", "PUT"],
                   allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                                  "Authorization"],)

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
            "value": val
        }
    }


@app.post("/getPropertiesTable", response_model=PropertyTableResponse, description="Запрос для получения таблицы значений по каждому параметру")
def get_properties_table(substanceId: str, modeId: str, parameters: list[float]) -> PropertyTableResponse:
    results = dict(zip(
        app.substaneces_objects_globals.properties[int(
            substanceId)][str(modeId)],
        [None] * len(app.substaneces_objects_globals.properties[int(substanceId)][str(modeId)])))
    for prop in app.substaneces_objects_globals.properties[int(substanceId)][str(modeId)]:
        results[str(prop)] = rsp.callProperty(
            app.substaneces_objects_globals.substances_objects[int(
                substanceId)],
            prop,
            modeId,
            parameters
        )

    print(results)

    return {"data": results}
