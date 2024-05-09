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
def get_available_substances():
    return {"data": app.substaneces_objects_globals.data_get_substances_list}


@app.get("/getCalcModesInfo", response_model=ParameterMode, description="Запрос для получения Режима параметров")
def get_calc_model_substanse(id):
    return {"data": app.substaneces_objects_globals.data_get_calc_modes_info[int(id)]}

@app.get("/getPropertiesLists", response_model=Property, description="Запрос для получения возможных Параметров для выбранного вещества и режима")
def get_calc_model_substanse(substanceId, modeId):
    return {"data": list(app.substaneces_objects_globals.available_properties[int(substanceId)][str(modeId)])}

# надо аккуратно сделать PropertyTableResponse
@app.post("/getPropertiesTable", description="Запрос для получения Таблицы")
def get_properties_table(request: PropertyTableRequest):
    val = rsp.callProperty(
        app.substaneces_objects_globals.substances_objects[int(request.substanceId)], 
        request.params.propertyId, 
        request.modeId,
        request.params.value)

    # response = PropertyTableResponse()
    # response.dimensionId = "SI" # надо продумать
    # response.propertyId = str(request.params.propertyId)
    # response.value = str(val)

    return {"data": {"dimensionId": "SI", "propertyId": str(request.params.propertyId), "value": str(val)}}