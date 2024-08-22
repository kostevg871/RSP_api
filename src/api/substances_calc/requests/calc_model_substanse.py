from src.api.substances_calc.requests.verification_data.verification import check_count_substance_id
from src.core.init import InitRSP
from src.schemas import ParameterMode


def calc_model_substanse(substaneces_objects: InitRSP, id: int) -> ParameterMode:
    count_substance = len(
        substaneces_objects.data_get_substances_list)

    check_count_substance_id(substanceId=id, count_substance=count_substance)

    return {"data": substaneces_objects.data_get_calc_modes_info[int(id)]}
