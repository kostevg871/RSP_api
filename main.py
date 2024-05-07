from typing import Union

from fastapi import FastAPI

from init import InitRSP
from schemas import AvailableSubstance, ParameterMode


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
