from fastapi import HTTPException
from typing_extensions import Annotated

from init import rsp_callProperty, property_dim_si, property_availabe_dim
from app import app
from schemas import *
from math import *
import uvicorn

from unit_converter.converter import convert, converts
from unit_converter.exceptions import UnConsistentUnitsError, UnitDoesntExistError

import rsp


@app.get("/getAvailableSubstances", response_model=AvailableSubstance, description="Получение всех доступных веществ")
def get_available_substances() -> AvailableSubstance:
    return {"data": app.substaneces_objects_globals.data_get_substances_list}


@app.get("/getCalcModesInfo", response_model=ParameterMode, description="Запрос для получения Режима параметров")
def get_calc_model_substanse(id: Annotated[int, Query(ge=0, lt=len(app.substaneces_objects_globals.data_get_substances_list))]) -> ParameterMode:

    return {"data": app.substaneces_objects_globals.data_get_calc_modes_info[int(id)]}


@app.get("/getPropertiesLists", response_model=Property,  description="Запрос для получения возможных Параметров для выбранного вещества и режима")
def get_calc_model_substanse(substanceId: Annotated[int, Query(ge=0, lt=len(app.substaneces_objects_globals.data_get_substances_list))],
                             modeId: str) -> Property:
    mode = modeId.upper()
    if mode not in app.substaneces_objects_globals.properties[substanceId]:
        raise HTTPException(status_code=422, detail="mode=" +
                            mode + " not in substance")
    return {"data": app.substaneces_objects_globals.properties[substanceId][mode]}


@app.post("/getPropertiesTableRow", response_model=PropertyRowTableResponse, description="Запрос для получения строки таблицы по параметру")
def get_properties_table_row(request: PropertyRowTableRequest) -> PropertyRowTableResponse:
    count_substance = len(
        app.substaneces_objects_globals.data_get_substances_list)
    mode = request.modeId.upper()
    property = request.params.property.upper()

    if request.substanceId < 0 or request.substanceId > count_substance-1:
        raise HTTPException(status_code=422, detail=str(request.substanceId) + " be in the range from 0 to " +
                            str(count_substance-1))

    if mode not in app.substaneces_objects_globals.properties[request.substanceId]:
        raise HTTPException(status_code=422, detail="mode=" +
                            mode + " not in substance")
    if not property in app.substaneces_objects_globals.properties[request.substanceId][mode]:
        raise HTTPException(status_code=422, detail="property=" +
                            property + " not in substance")
    params = app.substaneces_objects_globals.mode_descriptions[
        request.substanceId][mode]

    if not (len(request.params.param_values) == len(params)):
        raise HTTPException(
            status_code=422, detail="parameters must contain " + str(len(params)) + " parameters " + str(list(params))[1: -1])
    for avail_param in app.substaneces_objects_globals.data_get_calc_modes_info[request.substanceId]:
        if avail_param.value == mode:
            available_params_dimension = avail_param.available_param_dimension
            break
    try:
        params_in_SI = [
            copysign(float(convert(str(abs(v)) + ' ' + d, property_dim_si[l])), v) for v, d, l in zip(
                request.params.param_values,
                request.params.param_dimensions,
                app.substaneces_objects_globals.substances_calc_modes_literals[request.substanceId][mode])]

        val = rsp_callProperty(
            app.substaneces_objects_globals.substances_objects[
                request.substanceId],
            property,
            mode,
            params_in_SI)
        val_dim = copysign(float(converts(str(abs(
            val)) + ' ' + property_dim_si[property], request.params.property_dimension)), val)
    except UnConsistentUnitsError as e:
        raise HTTPException(
            status_code=422, detail={"message": 'Dimensions error: {}'.format(e),
                                     "available_param_dimensions": available_params_dimension,
                                     "available_property_dimensions": property_availabe_dim.get(request.params.property)})
    except UnitDoesntExistError as e:
        raise HTTPException(
            status_code=422, detail={"message": 'Dimensions error: {}'.format(e),
                                     "available_param_dimensions": available_params_dimension,
                                     "available_property_dimensions": property_availabe_dim.get(request.params.property)})

    return {
        "available_param_dimensions": available_params_dimension,
        "data":
        {
            "dimension": request.params.property_dimension,
            "propertyId": str(app.substaneces_objects_globals.properties[request.substanceId][mode][property]),
            "value": float(val_dim),
            "available_property_dimensions": property_availabe_dim.get(request.params.property)
        }
    }


@ app.post("/getPropertiesTable", response_model=PropertyTableResponse, description="Запрос для получения таблицы значений по каждому параметру")
def get_properties_table(request: PropertyTableRequest) -> PropertyTableResponse:
    count_substance = len(
        app.substaneces_objects_globals.data_get_substances_list)
    if request.substanceId < 0 or request.substanceId > count_substance-1:
        raise HTTPException(status_code=422, detail=str(request.substanceId) + " be in the range from 0 to " +
                            str(count_substance-1))

    mode = request.modeId.upper()
    available_params_dimension: list

    if mode not in app.substaneces_objects_globals.properties[request.substanceId]:
        raise HTTPException(status_code=422, detail="mode=" +
                            mode + " not in substance")
    params = app.substaneces_objects_globals.mode_descriptions[
        request.substanceId][mode]

    for avail_param in app.substaneces_objects_globals.data_get_calc_modes_info[request.substanceId]:
        if avail_param.value == mode:
            available_params_dimension = avail_param.available_param_dimension
            break

    if not (len(request.params.param_values) == len(params)):
        raise HTTPException(
            status_code=422, detail="parameters must contain " + str(len(params)) + " parameters " + str(list(params))[1: -1])

    results = []

    try:
        params_in_SI = [
            copysign(float(convert(str(abs(v)) + ' ' + d, property_dim_si[l])), v) for v, d, l in zip(
                request.params.param_values,
                request.params.param_dimensions,
                app.substaneces_objects_globals.substances_calc_modes_literals[request.substanceId][mode])]
    except UnConsistentUnitsError as e:
        raise HTTPException(
            status_code=422, detail={"message": 'Dimensions error: {}'.format(e), "available_param_dimensions": available_params_dimension})
    except UnitDoesntExistError as e:
        raise HTTPException(
            status_code=422, detail={"message": 'Dimensions error: {}'.format(e), "available_param_dimensions": available_params_dimension})

    try:

        for prop in app.substaneces_objects_globals.properties[int(request.substanceId)][mode].keys():
            try:
                results.append(
                    PropertyRowDataResponseTable(
                        dimension=property_dim_si[prop],
                        propertyId=str(prop),
                        value=rsp.callProperty(
                            app.substaneces_objects_globals.substances_objects[int(
                                request.substanceId)],
                            prop,
                            mode,
                            params_in_SI
                        ),
                        available_dimensions=property_availabe_dim.get(
                            str(prop)),
                    )
                )
            except rsp.exceptions.ExceptionUnphysicalFunc as e:
                results.append(
                    PropertyRowDataResponseTable(
                        dimension=property_dim_si[prop],
                        propertyId=str(prop),
                        value=str('NaN: {}'.format(e)),
                        available_dimensions=property_availabe_dim.get(
                            str(prop))
                    ))
    except RuntimeError as e:
        raise HTTPException(
            status_code=500, detail='RSP core error: {}'.format(e))

    try:
        response = PropertyTableResponse(
            available_param_dimensions=available_params_dimension, data=results)
    except ValueError as e:
        raise HTTPException(
            status_code=500, detail='Unknown error: {}'.format(e))

    return response


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
