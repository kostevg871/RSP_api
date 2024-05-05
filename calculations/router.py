from enum import Enum
from fastapi import APIRouter
from pydantic import BaseModel, ValidationError
import rsp

router = APIRouter(
    prefix="/calculations",
    tags=["Calculating"]
)


# @router.get("/")
# def calculation():
#    h2o = rsp.createSubstance("H2O_IF97")
#    # h2o =
#    data = rsp.callProperty(h2o, "D", "PT", [101325, 300])
#    return {"data": data}


@router.get("/")
def init():
    try:
        h2o = rsp.createSubstance("H2O_IF96")
        h2o_info = rsp.info.SubstanceInfo()
        rsp.info.getSubstanceInfo(h2o, h2o_info)
        modes = rsp.VectorString()
        h2o_info.getCalcModesInfo(modes)
        return {"data": {"h20": {"calc_modes": list(modes)}}, "status": "200"}
    except RuntimeError as e:
        print(e)
        return {"data": {}, "status": "201"}
    # h2o = rsp.createSubstance("H2O_IF92")
    # for mode in modes:
    #     result = []
    #     result.append(mode)
    #     return result
