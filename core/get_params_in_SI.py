from unit_converter.converter import convert, converts
from decimal import Decimal


from api.requests.exception.global_exception import error_calculating_core
from core.init import InitRSP
from helpers.constants import PROPERTY_DIMENSION_SI, PROPERTY_MIN_DIM
from schemas import RowParams


def get_params_in_SI(params: RowParams, substaneces_objects_globals: InitRSP, substanceId: int, mode: str):
    for index, dimens in enumerate(params.param_dimensions):
        if dimens in PROPERTY_MIN_DIM.keys():
            if params.param_values[index] <= 0:
                value = params.param_values[index]

                if params.param_dimensions[index] == "°C":
                    params.param_values[index] = value + \
                        abs(PROPERTY_MIN_DIM.get("°C"))
                    params.param_dimensions[index] = "K"
                if params.param_dimensions[index] == "°F":
                    params.param_values[index] = value + \
                        abs(PROPERTY_MIN_DIM.get("°F"))
                    params.param_dimensions[index] = "K"
    return [
        float(convert(str(Decimal(v)) + ' ' + d, PROPERTY_DIMENSION_SI[l])) for v, d, l in zip(
            params.param_values,
            params.param_dimensions,
            substaneces_objects_globals.substances_calc_modes_literals[substanceId][mode])]
