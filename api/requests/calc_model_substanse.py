from core.init import InitRSP
from schemas import ParameterMode


def calc_model_substanse(substaneces_objects: InitRSP, id: int) -> ParameterMode:
    return {"data": substaneces_objects.data_get_calc_modes_info[int(id)]
            }
