from math import copysign
from unit_converter.converter import convert, converts

from core.init import InitRSP, rsp_callProperty
from helpers.constants import PROPERTY_DIMENSION_SI, PROPERTY_MIN_DIM
from schemas import RowParams


def convert_params_in_SI(substaneces_objects_globals: InitRSP, substanceId: int, mode: str, params: RowParams, property: str) -> float:

    #!!! Двойная проверка надо что то придумать будет
    # converter temperature

    for index, dimens in enumerate(params.param_dimensions):
        if dimens in PROPERTY_MIN_DIM.keys():
            if params.param_values[index] <= 0:
                value = params.param_values[index]

                if params.param_dimensions[index] == "°C":
                    params.param_values[index] = value + 273.15
                    params.param_dimensions[index] = "K"
                if params.param_dimensions[index] == "°F":
                    params.param_values[index] = value + 459.67
                    params.param_dimensions[index] = "K"

    params_in_SI = [
        float(convert(str(v) + ' ' + d, PROPERTY_DIMENSION_SI[l])) for v, d, l in zip(
            params.param_values,
            params.param_dimensions,
            substaneces_objects_globals.substances_calc_modes_literals[substanceId][mode])]

    val = rsp_callProperty(
        substaneces_objects_globals.substances_objects[
            substanceId],
        property,
        mode,
        params_in_SI)

    # Если будет приходить отрицательные значения температур и тп
    # надо будет проверять
    val_dim = copysign(float(converts(str(
        abs(val)) + ' ' + PROPERTY_DIMENSION_SI[property], params.property_dimension)), val)

    return val_dim
