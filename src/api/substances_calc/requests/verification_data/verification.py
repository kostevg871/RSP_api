from decimal import Decimal


from src.api.substances_calc.requests.exceptions.exception_substances import error_count_param_dimension, error_dimension, error_dimension_call_property, error_dimension_call_property_table, error_dimension_table, error_parameters, error_params_min_value, error_params_negative, error_property, error_substance_id_count, error_substance_mode, error_unknown, error_value_core, unphysical_two_phase
from src.core.get_params_in_SI import get_params_in_SI_table
from src.core.init import InitRSP
from src.helpers.constants import PROPERTY_AVAILABE_DIM, PROPERTY_DIMENSION_SI, PROPERTY_MIN_DIM
from schemas import PropertyRowDataResponseTable, RowParams


from unit_converter.exceptions import UnConsistentUnitsError, UnitDoesntExistError
from src.core.convert_params_in_si import convert_params_in_SI

import rsp


# check mode calculation


def in_mode_on_substance(substaneces_objects_globals: InitRSP, substanceId: int, mode: str) -> None:
    if mode not in substaneces_objects_globals.substances_calc_modes_id[substanceId]:
        error_substance_mode(substaneces_objects_globals=substaneces_objects_globals,
                             substanceId=substanceId,
                             mode=mode)


# check count substance_id


def check_count_substance_id(substanceId: int, count_substance: int) -> None:
    if substanceId < 0 or substanceId > count_substance-1:
        error_substance_id_count(
            substanceId=substanceId, count_substance=count_substance)

# check property


def check_property(substaneces_objects_globals: InitRSP, substanceId: int, mode: str, property: list[str]) -> None:
    if not property in substaneces_objects_globals.properties[substanceId][mode]:
        error_property(property=property, substanceId=substanceId, substances_objects_globals=substaneces_objects_globals,
                       mode=mode)

# Check params


def check_params(substances_objects_globals: InitRSP,
                 substanceId: int, mode: str, param_value: list[str]):

    params_global: list[str] = substances_objects_globals.mode_descriptions[
        substanceId][mode]

    if not (len(param_value) == len(params_global)):
        error_parameters(params_global=params_global,
                         substanceId=substanceId, substances_objects_globals=substances_objects_globals)


def check_property_params(substances_objects_globals: InitRSP,
                          substanceId: int, mode: str, param_value_dimen: list[str], available_param_dimensions: list[list[str]]):

    params_global: list[str] = substances_objects_globals.mode_descriptions[
        substanceId][mode]

    if not (len(param_value_dimen) == len(params_global)):
        error_count_param_dimension(params_global=params_global,
                                    substanceId=substanceId, substances_objects_globals=substances_objects_globals,
                                    available_param_dimensions=available_param_dimensions)


# Cheak negative value and convert temprature
def check_property_negative(params: RowParams, params_global: list[str]) -> None:
    for index, dimens in enumerate(params.param_dimensions):
        if params.param_values[index] < 0:
            if dimens in PROPERTY_MIN_DIM.keys():
                if params.param_values[index] < PROPERTY_MIN_DIM.get(dimens):
                    error_params_min_value(
                        dimens=dimens, curr_param=params_global[index])
            else:
                error_params_negative(
                    params_global=params_global, index=index, dimens=dimens)


# check_dimension and params


def check_dimension(substaneces_objects_globals: InitRSP, substanceId: int, mode: str, params: RowParams, property: str, available_param_dimensions: list[list[str]]):
    try:
        return convert_params_in_SI(substaneces_objects_globals=substaneces_objects_globals,
                                    substanceId=substanceId, mode=mode, params=params, property=property)

    except (UnConsistentUnitsError, UnitDoesntExistError) as e:
        error_dimension(params, available_param_dimensions, str(e))

    except ValueError as e:
        error_value_core(params, available_param_dimensions, str(e))

    except Exception as e:
        if str(e).find("out of range") != -1:
            error_dimension_call_property(
                params, available_param_dimensions, e)
        if str(e).find("two-phase") != -1:
            unphysical_two_phase(e)
        error_unknown(params, available_param_dimensions, e)


def check_table_dimension(substaneces_objects_globals: InitRSP, substanceId: int, mode: str, params: RowParams,
                          available_param_dimensions: list[list[str]]):
    results = []

    try:
        params_in_SI = get_params_in_SI_table(substaneces_objects_globals=substaneces_objects_globals,
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

    except (UnConsistentUnitsError, UnitDoesntExistError) as e:
        error_dimension_table(available_param_dimensions, str(e))

    except ValueError as e:
        error_value_core(params, available_param_dimensions, str(e))

    except Exception as e:
        if str(e).find("out of range"):
            error_dimension_call_property_table(
                available_param_dimensions, e)
        error_unknown(params, available_param_dimensions, e)

    return results
