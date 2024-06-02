
from math import copysign
from fastapi import HTTPException
from core.init import InitRSP
from helpers.constants import PROPERTY_AVAILABE_DIM, PROPERTY_DIMENSION_SI
from schemas import PropertyRowDataResponseTable, PropertyTableResponse

import rsp

from unit_converter.converter import convert
from unit_converter.exceptions import UnConsistentUnitsError, UnitDoesntExistError


def property_table(substaneces_objects_globals: InitRSP, substanceId: int, modeId: str, params: list[str]):

    try:
        count_substance = len(
            substaneces_objects_globals.data_get_substances_list)
        if substanceId < 0 or substanceId > count_substance-1:
            raise HTTPException(status_code=400, detail=str(substanceId) + " be in the range from 0 to " +
                                str(count_substance-1))

        mode = modeId.upper()
        available_params_dimension: list

        if mode not in substaneces_objects_globals.properties[substanceId]:
            raise HTTPException(status_code=400, detail="mode=" +
                                mode + " not in substance")

        paramsGlobal = substaneces_objects_globals.mode_descriptions[
            substanceId][mode]

        for avail_param in substaneces_objects_globals.data_get_calc_modes_info[substanceId]:
            if avail_param.value == mode:
                available_params_dimension = avail_param.available_param_dimension
                break

        if not ((len(params.param_values) and (len(params.param_dimensions))) == len(paramsGlobal)):
            raise HTTPException(
                status_code=400, detail="parameters must contain " + str(len(paramsGlobal)) + " parameters " + str(list(paramsGlobal))[1: -1])

        results = []
        params_in_SI = [
            copysign(float(convert(str(abs(v)) + ' ' + d, PROPERTY_DIMENSION_SI[l])), v) for v, d, l in zip(
                params.param_values,
                params.param_dimensions,
                substaneces_objects_globals.substances_calc_modes_literals[substanceId][mode])]
    except (UnConsistentUnitsError, UnitDoesntExistError) as e:
        raise HTTPException(
            status_code=419, detail={"details": 'Dimensions error: {}'.format(e), "available_param_dimensions": available_params_dimension})
    

    try:
        for prop in substaneces_objects_globals.properties[int(substanceId)][mode].keys():
            try:
                results.append(
                    PropertyRowDataResponseTable(
                        dimension=PROPERTY_DIMENSION_SI[prop],
                        propertyId=str(prop),
                        value=rsp.callProperty(
                            substaneces_objects_globals.substances_objects[int(
                                substanceId)],
                            prop,
                            mode,
                            params_in_SI
                        ),
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

    try:
        response = PropertyTableResponse(
            available_param_dimensions=available_params_dimension, data=results)
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail='Unknown error: {}'.format(e))

    return response
