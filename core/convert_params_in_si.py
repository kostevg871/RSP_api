from math import copysign, isnan, nan
from unit_converter.converter import convert, converts
from decimal import Decimal


from api.requests.exception.global_exception import error_calculating_core
from core.init import InitRSP, rsp_callProperty
from helpers.constants import PROPERTY_DIMENSION_SI, PROPERTY_MIN_DIM
from schemas import RowParams
from core.get_params_in_SI import get_params_in_SI


def convert_params_in_SI(substaneces_objects_globals: InitRSP,
                         substanceId: int, mode: str, params: RowParams,
                         property: str | None) -> float:

    # не очень понятно что делать с большими числами
    params_in_SI = get_params_in_SI(params=params, substaneces_objects_globals=substaneces_objects_globals,
                                    substanceId=substanceId, mode=mode)

    val = rsp_callProperty(
        substaneces_objects_globals.substances_objects[
            substanceId],
        property,
        mode,
        params_in_SI)

    if isnan(val):
        return error_calculating_core()

    # Если будет приходить отрицательные значения температур и тп
    # надо будет проверять
    val_dim = copysign(float(converts(str(
        abs(val)) + ' ' + PROPERTY_DIMENSION_SI[property], params.property_dimension)), val)

    return val_dim
