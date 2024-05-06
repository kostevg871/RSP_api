from fastapi import APIRouter
import rsp


from calculations.schemas import AvailableSubstance
from initialization import substaneces_objects_globals

router = APIRouter(
    prefix="/calculations",
    tags=["Calculating"],
)


@router.get("/get_available_substances", description="Получение всех доступных веществ")
def get_available_substances():
    return {"data": substaneces_objects_globals.data_get_substances_list}


@router.get("/get_calc_model_substances/{substance}", description="Получение всех режимов расчетов для одной substance")
def get_calc_model_substanse(substance: str):
    return {"data": substaneces_objects_globals.data_get_calc_modes_info[int(substance)]}
