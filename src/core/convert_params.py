from decimal import Decimal
from math import copysign, isinf, isnan

from fastapi import params

from api.substances_calc.requests.exceptions.global_exception import error_calculating_core
from helpers.constants import PROPERTY_DIMENSION_SI

from unit_converter.converter import converts


def convert_params(val: int):
    if isnan(val):
        return error_calculating_core()
    if isinf(val):
        val_dim = str(Decimal(val))
        return val_dim

    if params.property_dimension.strip() == "":
        return val
    else:
        return copysign(float(converts(str(abs(
            val)) + ' ' + PROPERTY_DIMENSION_SI[property], params.property_dimension)), val)
