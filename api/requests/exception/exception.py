from decimal import Decimal
from math import isnan
from fastapi import HTTPException


from core.get_params_in_SI import get_params_in_SI
from core.init import InitRSP
from helpers.constants import PROPERTY_AVAILABE_DIM, PROPERTY_DIMENSION_SI, PROPERTY_MIN_DIM
from schemas import PropertyRowDataResponseTable, RowParams


from unit_converter.exceptions import UnConsistentUnitsError, UnitDoesntExistError
from core.convert_params_in_si import convert_params_in_SI

import rsp

# check range substance

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


# Cheak negative value and convert temprature
def check_property_negative(params: RowParams, params_global: list[str]) -> None:
    for index, dimens in enumerate(params.param_dimensions):
        if params.param_values[index] < 0:
            if dimens in PROPERTY_MIN_DIM.keys():
                if params.param_values[index] < PROPERTY_MIN_DIM.get(dimens):
                    raise HTTPException(
                        status_code=400, detail="Parameters {dimens} there can't be less {value}".format(dimens=dimens, value=PROPERTY_MIN_DIM.get(dimens)))
            else:
                raise HTTPException(
                    status_code=400, detail="Parameters {param}({dimens}) there can't be negative".format(param=params_global[index],
                                                                                                          dimens=dimens))


# check_dimension and params


def check_dimension(substaneces_objects_globals: InitRSP, substanceId: int, mode: str, params: RowParams, property: str, available_param_dimensions: list[list[str]]):
    try:

        return convert_params_in_SI(substaneces_objects_globals=substaneces_objects_globals,
                                    substanceId=substanceId, mode=mode, params=params, property=property)

    except (UnConsistentUnitsError, UnitDoesntExistError) as e:
        raise HTTPException(
            status_code=442, detail={"message": 'Dimensions error: {}'.format(e),
                                     "available_param_dimensions": available_param_dimensions,
                                     "available_property_dimensions": PROPERTY_AVAILABE_DIM.get(params.property)})
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail={"message": 'Core error: {}'.format(e)}
        )

    except Exception as e:
        raise HTTPException(
            status_code=442, detail={"message": "{}".format(e),
                                     "available_param_dimensions": available_param_dimensions,
                                     "available_property_dimensions": PROPERTY_AVAILABE_DIM.get(params.property)})


def check_table_dimension(substaneces_objects_globals: InitRSP, substanceId: int, mode: str, params: RowParams,
                          available_param_dimensions: list[list[str]]):
    results = []
    try:
        params_in_SI = get_params_in_SI(substaneces_objects_globals=substaneces_objects_globals,
                                        substanceId=substanceId, mode=mode, params=params)

        for prop in substaneces_objects_globals.properties[int(substanceId)][mode].keys():
            try:
                results.append(
                    PropertyRowDataResponseTable(
                        dimension=PROPERTY_DIMENSION_SI[prop],
                        propertyId=str(prop),
                        value=str(Decimal(rsp.callProperty(
                            substaneces_objects_globals.substances_objects[int(
                                substanceId)],
                            prop,
                            mode,
                            params_in_SI
                        ))),
                        available_dimensions=PROPERTY_AVAILABE_DIM.get(
                            str(prop)),
                    )
                )

            except rsp.exceptions.ExceptionUnphysicalFunc as e:
                results.append(
                    PropertyRowDataResponseTable(
                        dimension=PROPERTY_DIMENSION_SI[prop],
                        propertyId=str(prop),
                        value=str('NaN: {}'.format(e)),
                        available_dimensions=PROPERTY_AVAILABE_DIM.get(
                            str(prop))
                    ))

    except RuntimeError as e:
        raise HTTPException(
            status_code=400, detail='RSP core error: {}'.format(e))

    except (UnConsistentUnitsError, UnitDoesntExistError) as e:
        raise HTTPException(
            status_code=444, detail={"message": 'Dimensions error: {}'.format(e),
                                     "available_param_dimensions": available_param_dimensions})
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail={"message": 'Core error: {}'.format(e)}
        )

    except Exception as e:
        raise HTTPException(
            status_code=444, detail={"message": "{}".format(e),
                                     "available_param_dimensions": available_param_dimensions})

    return results
