from fastapi import HTTPException

from schemas import RowParams
from src.helpers.constants import PROPERTY_AVAILABE_DIM, PROPERTY_MIN_DIM
from src.core.init import InitRSP


def error_substance_id_count(substanceId: int, count_substance: int):
    raise HTTPException(status_code=400, detail={
        "code": 1,
        "type": "SubstanceNotFound",
        "error_info": "Неправильно указано вещество",
        "msg_user_ru": "substanceId={substanceId} должно быть в промежутке от 0 до {count_substance}"
        .format(substanceId=substanceId, count_substance=count_substance-1),
        "msg_user_en": "substanceId={substanceId} be in the range from 0 to {count_substance}"
        .format(substanceId=substanceId, count_substance=count_substance-1),
        "request_info": None
    })


def error_substance_mode(substaneces_objects_globals: InitRSP, substanceId: int, mode: str):
    raise HTTPException(status_code=400, detail={
        "code": 2,
        "type": "ModeNotFound",
        "error_info": "Неправильно указан мод для данного вещества",
        "msg_user_en": "mode={mode} not in substance".format(mode=mode),
        "msg_user_ru": "Мод={mode} не существует для данного вещества".format(mode=mode),
        "request_info": {"available_substances": substaneces_objects_globals.substances_calc_modes_id[substanceId]},
    })


def error_parameters(params_global: list[str], substanceId: int, substances_objects_globals: InitRSP):

    count = str(len(params_global))
    list_params = str(list(params_global))[1: -1]

    raise HTTPException(status_code=400, detail={
        "code": 3,
        "type": "InvalidParametrs",
        "error_info": "Неправильно указано количество параметров для расчета",
        "msg_user_en": "Parameters must contain " + count + " parameters " + list_params,
        "msg_user_ru": "Поле параметры должно содержать " + count + " параметр(а) " + list_params,
        "request_info": {"available_substances": substances_objects_globals.substances_calc_modes_id[substanceId]},
    })

# !! Перевести параметры на русский


def error_dimension(property: list[str], substanceId: int, substances_objects_globals: InitRSP, mode: str):
    raise HTTPException(status_code=400, detail={
        "code": 4,
        "type": "PropetryNotFound",
        "error_info": "Неправильно указано свойство для расчета, не существует для данного вещества",
        "msg_user_en": "property={property} not in substance".format(property=property),
        "msg_user_ru": "Свойство={property} не существует для данного вещества".format(property=property),
        "request_info": {"available_property_dimensions": list(substances_objects_globals.properties[substanceId][mode])}
    })

# !! Перевести параметры на русский


def error_params_negative(params_global: str, index: int, dimens: str):

    raise HTTPException(status_code=400, detail={
        "code": 5,
        "type": "ParameterNotNegative",
        "error_info": "Параметр не может быть отрицательным",
        "msg_user_en": "Parameters {param}({dimens}) there can't be negative".format(param=params_global[index], dimens=dimens),
        "msg_user_ru": "Параметр {param}({dimens}) не может быть отрицательным".format(param=params_global[index], dimens=dimens),
        "request_info": None
    })

# !! Перевести параметры на русский


def error_params_min_value(dimens: str, curr_param: str):

    min_value = PROPERTY_MIN_DIM.get(dimens)

    raise HTTPException(status_code=400, detail={
        "code": 6,
        "type": "ParameterLessMinValue",
        "error_info": "Параметр меньше минимального значения",
        "msg_user_en": "Parameters {dimens} there can't be less {value}".format(dimens=dimens, value=min_value),
        "msg_user_ru": "Параметр {param} ({dimens}) не может быть меньше {value}".format(param=curr_param, dimens=dimens, value=min_value),
        "request_info": {"min_value": min_value}
    })


def error_dimension(params: RowParams, available_param_dimensions: InitRSP, e: str):

    e = e[e.find("'") + 1: e.rfind(",")-1]

    raise HTTPException(
        status_code=400, detail={
            "code": 7,
            "type": "InvalidDimension",
            "error_info": "Не правильно указаны единицы измерения",
            "msg_user_en": "Unit ({dim}) invalid".format(dim=e),
            "msg_user_ru": "Единица измерения ({dim}) не верна".format(dim=e),
            "request_info": {
                    "available_param_dimensions": available_param_dimensions,
                    "available_property_dimensions": PROPERTY_AVAILABE_DIM.get(params.property),
                    "loc": e
            }
        })
