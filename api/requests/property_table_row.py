from math import copysign
from fastapi import HTTPException
from api.requests.exception.exception import in_mode_on_substance
from core.init import InitRSP, rsp_callProperty
from helpers.constants import PROPERTY_AVAILABE_DIM, PROPERTY_DIMENSION_SI
from schemas import PropertyRowTableResponse

from unit_converter.converter import convert, converts
from unit_converter.exceptions import UnConsistentUnitsError, UnitDoesntExistError


def property_table_row(substaneces_objects_globals: InitRSP,
                       substanceId: int, modeId: str, property: str, params: list[str]) -> PropertyRowTableResponse:

    count_substance = len(
        substaneces_objects_globals.data_get_substances_list)
    mode = modeId.upper()
    property = property.upper()

    if substanceId < 0 or substanceId > count_substance-1:
        raise HTTPException(status_code=400, detail=str(substanceId) + " be in the range from 0 to " +
                            str(count_substance-1))

    in_mode_on_substance(
        substaneces_objects_globals=substaneces_objects_globals,  substanceId=substanceId, mode=mode)

    if not property in substaneces_objects_globals.properties[substanceId][mode]:
        raise HTTPException(status_code=400, detail="property= " +
                            property + " not in substance")

    params_global: list[str] = substaneces_objects_globals.mode_descriptions[
        substanceId][mode]

    if not (len(params.param_values) == len(params_global)):
        raise HTTPException(
            status_code=400, detail="parameters must contain " + str(len(params_global)) + " parameters "
            + str(list(params_global))[1: -1])

    for avail_param in substaneces_objects_globals.data_get_calc_modes_info[substanceId]:
        if avail_param.value == mode:
            available_params_dimension = avail_param.available_param_dimension
            break
    try:
        params_in_SI = [
            copysign(float(convert(str(abs(v)) + ' ' + d, PROPERTY_DIMENSION_SI[l])), v) for v, d, l in zip(
                params.param_values,
                params.param_dimensions,
                substaneces_objects_globals.substances_calc_modes_literals[substanceId][mode])]

        val = rsp_callProperty(
            substaneces_objects_globals.substances_objects[
                substanceId],
            property,
            mode,
            params_in_SI)
        val_dim = copysign(float(converts(str(abs(
            val)) + ' ' + PROPERTY_DIMENSION_SI[property], params.property_dimension)), val)

    except (UnConsistentUnitsError, UnitDoesntExistError) as e:
        raise HTTPException(
            status_code=442, detail={"message": 'Dimensions error: {}'.format(e),
                                     "available_param_dimensions": available_params_dimension,
                                     "available_property_dimensions": PROPERTY_AVAILABE_DIM.get(params.property)})
    except:
        raise HTTPException(
            status_code=442, detail={"message": "Dimension error/ Check param and property dimension",
                                     "available_param_dimensions": available_params_dimension,
                                     "available_property_dimensions": PROPERTY_AVAILABE_DIM.get(params.property)})

    return {
        "available_param_dimensions": available_params_dimension,
        "data":
        {
            "dimension": params.property_dimension,
            "propertyId": str(substaneces_objects_globals.properties[substanceId][mode][property]),
            "value": float(val_dim),
            "available_property_dimensions": PROPERTY_AVAILABE_DIM.get(params.property)
        }
    }
