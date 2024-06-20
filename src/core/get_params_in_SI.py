from unit_converter.converter import convert
from decimal import Decimal


from src.core.init import InitRSP
from src.helpers.constants import PROPERTY_AVAILABE_DIM, PROPERTY_DIMENSION_SI, PROPERTY_MIN_DIM
from schemas import RowParams

from unit_converter.exceptions import UnitDoesntExistError, UnConsistentUnitsError


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

    results = []

    for v, d, l, index in zip(
            params.param_values,
            params.param_dimensions,
            substaneces_objects_globals.substances_calc_modes_literals[substanceId][mode],
            range(len(
                substaneces_objects_globals.substances_calc_modes_literals[substanceId][mode]))
    ):

        if d.strip() != "":
            if d.strip() not in PROPERTY_AVAILABE_DIM[substaneces_objects_globals.substances_calc_modes_literals[substanceId][mode][index]]:
                raise UnConsistentUnitsError(str(d))
            results.append(
                float(convert(str(Decimal(v)) + ' ' + d, PROPERTY_DIMENSION_SI[l])))
        else:
            results.append(float(str(Decimal(v))))

    return results
