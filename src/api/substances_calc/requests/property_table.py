from fastapi import HTTPException
from src.api.substances_calc.requests.verification_data.verification import check_count_substance_id, check_params, check_property_negative, check_table_dimension, in_mode_on_substance
from src.core.init import InitRSP
from schemas import PropertyTableResponse


def property_table(substaneces_objects_globals: InitRSP, substanceId: int, modeId: str, params: list[str]):

    count_substance = len(
        substaneces_objects_globals.data_get_substances_list)

    check_count_substance_id(substanceId=substanceId,
                             count_substance=count_substance)

    mode = modeId.upper()
    available_params_dimension: list

    in_mode_on_substance(
        substaneces_objects_globals=substaneces_objects_globals,  substanceId=substanceId, mode=mode)

    for avail_param in substaneces_objects_globals.data_get_calc_modes_info[substanceId]:
        if avail_param.value == mode:
            available_params_dimension = avail_param.available_param_dimension
            break

    check_params(substaneces_objects_globals=substaneces_objects_globals,
                 substanceId=substanceId, mode=mode, param_value=params.param_values)

    check_property_negative(params=params, params_global=substaneces_objects_globals.mode_descriptions[
        substanceId][mode])

    results = check_table_dimension(params=params, substaneces_objects_globals=substaneces_objects_globals,
                                    substanceId=substanceId, mode=mode, available_param_dimensions=available_params_dimension)

    try:
        response = PropertyTableResponse(
            available_param_dimensions=available_params_dimension, data=results)
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail={"status_code": 400, "msg": "Unknown error: {}".format(e)})

    return response
