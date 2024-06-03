from math import copysign
from fastapi import HTTPException

from core.init import InitRSP, rsp_callProperty
from helpers.constants import PROPERTY_AVAILABE_DIM, PROPERTY_DIMENSION_SI
from schemas import RowParams

from unit_converter.converter import convert, converts
from unit_converter.exceptions import UnConsistentUnitsError, UnitDoesntExistError

# check mode calculation


def in_mode_on_substance(substaneces_objects_globals: InitRSP, substanceId: int, mode: str) -> None:
    if mode not in substaneces_objects_globals.properties[substanceId]:
        raise HTTPException(status_code=441,
                            detail={"error_message": "mode={mode} not in substance".format(mode=mode),
                                    "available_modes": substaneces_objects_globals.substances_calc_modes_id[substanceId],
                                    "status_code": 441})

# check count substance_id


def check_count_substance_id(substanceId: int, count_substance: int) -> None:
    if substanceId < 0 or substanceId > count_substance-1:
        raise HTTPException(status_code=400, detail="substanceId = {substanceId} be in the range from 0 to {count_substance}".format(
            substanceId=substanceId, count_substance=count_substance-1))

# check property


def check_property(substaneces_objects_globals: InitRSP, substanceId: int, mode: str, property: list[str]) -> None:
    if not property in substaneces_objects_globals.properties[substanceId][mode]:
        raise HTTPException(status_code=443,
                            detail={"error_message": "property= {property} not in substance".format(property=property),
                                    "available_property_dimensions": list(substaneces_objects_globals.properties[substanceId][mode]),
                                    "status_code": 443})


# Check params

def check_params(substaneces_objects_globals: InitRSP, substanceId: int, mode: str, param_value: list[str]):
    params_global: list[str] = substaneces_objects_globals.mode_descriptions[
        substanceId][mode]

    if not (len(param_value) == len(params_global)):
        raise HTTPException(
            status_code=400, detail="parameters must contain " + str(len(params_global)) + " parameters "
            + str(list(params_global))[1: -1])


# check_dimension and params
def check_dimension(substaneces_objects_globals: InitRSP, substanceId: int, mode: str, params: RowParams, property: str, available_param_dimensions: list[list[str]]):
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

        return val_dim

    except (UnConsistentUnitsError, UnitDoesntExistError) as e:
        raise HTTPException(
            status_code=442, detail={"message": 'Dimensions error: {}'.format(e),
                                     "available_param_dimensions": available_param_dimensions,
                                     "available_property_dimensions": PROPERTY_AVAILABE_DIM.get(params.property)})
    except Exception as e:
        raise HTTPException(
            status_code=442, detail={"message": "Core error: {}".format(e),
                                     "available_param_dimensions": available_param_dimensions,
                                     "available_property_dimensions": PROPERTY_AVAILABE_DIM.get(params.property)})
