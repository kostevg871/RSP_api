import sys
from typing_extensions import Annotated

from fastapi import FastAPI, HTTPException, Query
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
    "https://real-substance-properties.netlify.app",
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
def get_calc_model_substanse(id: Annotated[int, Query(ge=0, lt=len(app.substaneces_objects_globals.data_get_substances_list))]) -> ParameterMode:

    return {"data": app.substaneces_objects_globals.data_get_calc_modes_info[int(id)]}


@app.get("/getPropertiesLists", response_model=Property,  description="Запрос для получения возможных Параметров для выбранного вещества и режима")
def get_calc_model_substanse(substanceId: Annotated[int, Query(ge=0, lt=len(app.substaneces_objects_globals.data_get_substances_list))],
                             modeId: str) -> Property:
    mode = modeId.upper()
    if mode not in app.substaneces_objects_globals.properties[substanceId]:
        raise HTTPException(status_code=422, detail="mode=" +
                            mode + " not in substance")
    return {"data": app.substaneces_objects_globals.properties[substanceId][mode]}


@app.post("/getPropertiesTableRow", response_model=PropertyRowTableResponse, description="Запрос для получения строки таблицы по параметру")
def get_properties_table_row(request: PropertyTableRequest) -> PropertyRowTableResponse:
    count_substance = len(
        app.substaneces_objects_globals.data_get_substances_list)
    mode = request.modeId.upper()
    property = request.params.property.upper()
    if request.substanceId < 0 or request.substanceId > count_substance-1:
        raise HTTPException(status_code=422, detail=str(request.substanceId) + " be in the range from 0 to " +
                            str(count_substance))

    if mode not in app.substaneces_objects_globals.properties[request.substanceId]:
        raise HTTPException(status_code=422, detail="mode=" +
                            mode + " not in substance")
    if not (len(request.params.value) == 2):
        raise HTTPException(
            status_code=422, detail="parameters must contain 2 parameters pressure or temperature")
    if not property in app.substaneces_objects_globals.properties[request.substanceId][mode]:
        raise HTTPException(status_code=422, detail="property=" +
                            property + " not in substance")
     # ! добавить условия при которых давление или температура неверны
        # ! библиотеки ошибка обьект я так понял нет таких функций в библиотеке{
#  "substanceId":3,
#  "modeId": "pt",
#  "params": {
#    "property": "d",
#    "value": [
#      130000, 400
#    ],
#    "dimensionId": "1"
#  }
# }
    try:
        val = rsp.callProperty(
            app.substaneces_objects_globals.substances_objects[
                request.substanceId],
            property,
            mode,
            request.params.value)
    except RuntimeError as e:
        raise HTTPException(
            status_code=500, detail='InitRSP error: {}'.format(e))

    return {
        "data":
        {
            "dimensionId": "SI",
            "property": str(app.substaneces_objects_globals.properties[request.substanceId][mode][property]),
            "value": val
        }
    }


@app.post("/getPropertiesTable", response_model=PropertyTableResponse, description="Запрос для получения таблицы значений по каждому параметру")
def get_properties_table(substanceId: Annotated[int, Query(ge=0, lt=len(app.substaneces_objects_globals.data_get_substances_list))],
                         modeId: str, parameters: list[float]) -> PropertyTableResponse:
    mode = modeId.upper()
    if mode not in app.substaneces_objects_globals.properties[substanceId]:
        raise HTTPException(status_code=422, detail="mode=" +
                            mode + " not in substance")
    if not (len(parameters) == 2):
        raise HTTPException(
            status_code=422, detail="parameters must contain 2 parameters pressure or temperature")

       # ! добавить условия при которых давление или температура неверны
    try:
        results = dict(zip(
            app.substaneces_objects_globals.properties[int(
                substanceId)][mode],
            [None] * len(app.substaneces_objects_globals.properties[int(substanceId)][mode])))
        for prop in app.substaneces_objects_globals.properties[int(substanceId)][mode]:
            results[str(prop)] = rsp.callProperty(
                app.substaneces_objects_globals.substances_objects[int(
                    substanceId)],
                prop,
                mode,
                parameters
            )
    except RuntimeError as e:
        raise HTTPException(
            status_code=500, detail='InitRSP error: {}'.format(e))

    return {"data": results}
