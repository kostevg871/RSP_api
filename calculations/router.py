from fastapi import APIRouter
import rsp

from calculations.helpers import get_calc_model_subs
from calculations.schemas import AvailableSubstance

router = APIRouter(
    prefix="/calculations",
    tags=["Calculating"],
)


@router.get("/get_available_substances", response_model=AvailableSubstance, description="Получение всех доступных веществ")
def get_available_substances():
    substances = get_calc_model_subs()
    count = len(substances)
    return {"data": substances, "count": count}


@router.get("/get_calc_model_substances/{substance}", description="Получение всех моделей расчетов для одной substance")
def get_calc_model_substanse(substance: str):
    curr_substance = rsp.createSubstance(substance)
    substance_info = rsp.info.SubstanceInfo()
    rsp.info.getSubstanceInfo(curr_substance, substance_info)
    modes = rsp.VectorString()
    substance_info.getCalcModesInfo(modes)
    count = len(list(modes))
    return {"data": {"calc_modes": list(modes)}, "count": count}
