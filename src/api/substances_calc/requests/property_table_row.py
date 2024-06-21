from src.api.substances_calc.requests.verification_data.verification import check_count_substance_id, check_dimension, check_params, check_property, check_property_negative, check_property_params, in_mode_on_substance
from src.core.init import InitRSP
from src.helpers.constants import PROPERTY_AVAILABE_DIM
from schemas import PropertyRowTableResponse, RowParams


def property_table_row(substances_objects_globals: InitRSP,
                       substanceId: int, modeId: str, property: str, params: RowParams) -> PropertyRowTableResponse:

    count_substance = len(
        substances_objects_globals.data_get_substances_list)

    mode = modeId.upper()

    property = property.upper()

    check_count_substance_id(substanceId=substanceId,
                             count_substance=count_substance)

    in_mode_on_substance(
        substaneces_objects_globals=substances_objects_globals,  substanceId=substanceId, mode=mode)

    check_property(substaneces_objects_globals=substances_objects_globals,
                   substanceId=substanceId, mode=mode, property=params.property)

    for avail_param in substances_objects_globals.data_get_calc_modes_info[substanceId]:
        if avail_param.value == mode:
            available_params_dimension = avail_param.available_param_dimension
            break

    check_property_params(substances_objects_globals=substances_objects_globals,
                          substanceId=substanceId, mode=mode, param_value_dimen=params.param_dimensions)

    check_params(substances_objects_globals=substances_objects_globals,
                 substanceId=substanceId, mode=mode, param_value=params.param_values)

    check_property_negative(params=params, params_global=substances_objects_globals.mode_descriptions[
        substanceId][mode])

    val_dim = check_dimension(substaneces_objects_globals=substances_objects_globals, substanceId=substanceId,
                              mode=mode, params=params, property=property,
                              available_param_dimensions=available_params_dimension)

    return {
        "available_param_dimensions": available_params_dimension,
        "data":
        {
            "dimension": params.property_dimension,
            "propertyId": str(substances_objects_globals.properties[substanceId][mode][property]),
            "value": str(val_dim),
            "available_property_dimensions": PROPERTY_AVAILABE_DIM.get(params.property)
        }
    }
