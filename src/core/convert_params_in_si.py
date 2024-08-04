from math import copysign, isinf, isnan
from unit_converter.converter import converts
from decimal import Decimal


from src.helpers.help_func import float_to_str
from src.api.substances_calc.requests.exceptions.global_exception import error_calculating_core
from src.core.init import InitRSP, rsp_callProperty
from src.helpers.constants import PROPERTY_DIMENSION_SI
from schemas import RowParams
from src.core.get_params_in_SI import get_params_in_SI


def convert_params_in_SI(substaneces_objects_globals: InitRSP,
                         substanceId: int, mode: str, params: RowParams,
                         property: str) -> float:

    params_in_SI = get_params_in_SI(params=params, substaneces_objects_globals=substaneces_objects_globals,
                                    substanceId=substanceId, mode=mode)

    val = rsp_callProperty(
        substaneces_objects_globals.substances_objects_no_info[
            substanceId],
        property,
        mode,
        params_in_SI)

    if isnan(val):
        return error_calculating_core()
    if isinf(val):
        val_dim = str(Decimal(val))
        return val_dim

    if params.property_dimension.strip() == "":
        val_dim = val
    else:
        val_dimension = float_to_str(val)
        if str(val) in "E" or "e":
            if float(val) >= 0:
                val_dim = copysign(float(converts(str(
                    val_dimension) + ' ' + PROPERTY_DIMENSION_SI[property], params.property_dimension)), val)
            else:
                val_dim = copysign(float(converts(float_to_str(abs(
                    val)) + ' ' + PROPERTY_DIMENSION_SI[property], params.property_dimension)), val)
        else:
            val_dim = copysign(float(converts(str(abs(
                val)) + ' ' + PROPERTY_DIMENSION_SI[property], params.property_dimension)), val)

    return val_dim
