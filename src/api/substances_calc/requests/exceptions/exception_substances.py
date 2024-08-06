
from fastapi import HTTPException

from src.schemas import RowParams
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


def error_property(property: str, substanceId: int, substances_objects_globals: InitRSP, mode: str):
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


def error_dimension_call_property(params: RowParams, available_param_dimensions: InitRSP, e: str):
    e = str(e)
    split_error = e.split(":")
    len_split_error = len(split_error)-2
    result_param = str(split_error[len_split_error]).replace('"', "")
    if ">" in e:
        len_split = len(e.split(">"))
        find_value = e.split(">")[len_split-1]
        operator = "меньше "
    else:
        len_split = len(e.split("<"))
        find_value = e.split("<")[len_split-1]
        operator = "больше "
    index = find_value.strip().find(".")
    find_value = find_value.strip()[:index+3]

    raise HTTPException(
        status_code=400, detail={
            "code": 8,
            "type": "OutOfRange",
            "error_info": e,
            "msg_user_en": "Out of range:" + str(split_error[len_split_error]) + ", boundary condition=" + str(find_value),
            "msg_user_ru": "Выход из диапозона вычисления:" + result_param + ", параметр должен быть " + operator + str(find_value),
            "request_info": {
                "available_param_dimensions": available_param_dimensions,
                "available_property_dimensions": PROPERTY_AVAILABE_DIM.get(params.property),
                "boundary_condition": find_value
            }
        })


def error_value_core(params: RowParams, available_param_dimensions: InitRSP, e: str):

    raise HTTPException(
        status_code=400, detail={
            "code": 9,
            "type": "CoreValueError",
            "error_info": "Calculation error in rsp, try other parameters ({e})".format(e=e),
            "msg_user_en": "Calculation error, use different input data",
            "msg_user_ru": "Ошибка вычисления, используйте другие данные",
            "request_info": {
                    "available_param_dimensions": available_param_dimensions,
                    "available_property_dimensions": PROPERTY_AVAILABE_DIM.get(params.property),
            }
        })


def error_count_param_dimension(params_global: list[str], substanceId: int, substances_objects_globals: InitRSP,
                                available_param_dimensions: list[list[str]]):

    count = str(len(params_global))
    list_params = str(list(params_global))[1: -1]

    raise HTTPException(
        status_code=400, detail={
            "code": 10,
            "type": "InvalidDimensionParametrs",
            "error_info": "Неправильно указано количество единиц измерения для расчета, ожидается `{count}`".format(count=count),
            "msg_user_en": "Unit must contain " + count + " parameters " + list_params,
            "msg_user_ru": "Поле с единицами измерения должно содержать " + count + " параметр(а) " + list_params,
            "request_info": {"available_substances": substances_objects_globals.substances_calc_modes_id[substanceId],
                             "available_param_dimensions": available_param_dimensions},
        })


def error_dimension_table(available_param_dimensions: InitRSP, e: str):

    e_change = e[e.find("(") + 1: e.rfind(")")].split(",")

    raise HTTPException(
        status_code=400, detail={
            "code": 11,
            "type": "InvalidDimensionTable",
            "error_info": e,
            "msg_user_en": "Unit ({dim}) invalid, expected {ap}".format(dim=e_change[0], ap=available_param_dimensions[int(e_change[1])]),
            "msg_user_ru": "Единица измерения ({dim}) не верна, ожидается {ap}".format(dim=e_change[0], ap=available_param_dimensions[int(e_change[1])]),
            "request_info": {
                    "available_param_dimensions": available_param_dimensions,
                    "loc": e_change[0]
            }
        })


def error_unknown(params: RowParams, available_param_dimensions: InitRSP, e: str):

    raise HTTPException(
        status_code=400, detail={
            "code": 12,
            "type": "UnknownError",
            "error_info": str(e),
            "msg_user_en": "Unknown error",
            "msg_user_ru": "Неизвестная ошибка, измените параметры расчета",
            "request_info": {
                    "available_param_dimensions": available_param_dimensions,
                    "available_property_dimensions": PROPERTY_AVAILABE_DIM.get(params.property),
                    "loc": str(e)
            }
        })


def error_dimension_call_property_table(available_param_dimensions: InitRSP, e: str):
    # !!! find value переводить в единицу измерения в которой был отправлен запрос
    e = str(e)
    split_error = e.split(":")
    len_split_error = len(split_error)-2

    if ">" in e:
        len_split = len(e.split(">"))-1
        find_value = e.split(">")[len_split]
        operator = "меньше "
    else:
        len_split = len(e.split("<"))-1
        find_value = e.split("<")[len_split]
        operator = "больше "

    index = find_value.strip().find(".")
    find_value = find_value.strip()[:index+3]

    raise HTTPException(
        status_code=400, detail={
            "code": 13,
            "type": "OutOfRange",
            "error_info": e,
            "msg_user_en": "Out of range:" + str(split_error[len_split_error]) + ", boundary condition=" + str(find_value),
            "msg_user_ru": "Выход из диапозона вычисления:" + str(split_error[len_split_error]) + ", параметр должен быть " + operator + str(find_value),
            "request_info": {
                "available_param_dimensions": available_param_dimensions,
                "boundary_condition": find_value
            }
        })


def unphysical_two_phase(e: str):

    raise HTTPException(
        status_code=400, detail={
            "code": 14,
            "type": "UnphysicalTwoPhase ",
            "error_info": e,
            "msg_user_en": "Isobaric heat capacity is unphysical in two-phase region",
            "msg_user_ru": "Изобарная теплоемкость нефизична в двухфазной области",
            "request_info": {
                    "loc": str(e)
            }
        })


def error_dimension_row_table(params: RowParams, available_param_dimensions: list[list[str]]):

    if params.property_dimension.strip() == "":
        result = "Укажите единицу измерения, ожидается {avail}".format(
            avail=PROPERTY_AVAILABE_DIM.get(params.property))
    else:
        result = "Единица измерения ({dim}) не верна, ожидается {avail}".format(
            dim=params.property_dimension, avail=PROPERTY_AVAILABE_DIM.get(params.property))

    raise HTTPException(
        status_code=400, detail={
            "code": 15,
            "type": "InvalidDimension",
            "error_info": "Не правильно указаны единицы измерения",
            "msg_user_en": "Unit ({dim}) invalid".format(dim=params.property_dimension),
            "msg_user_ru": result,
            "request_info": {
                    "available_param_dimensions": available_param_dimensions,
                    "available_property_dimensions": PROPERTY_AVAILABE_DIM.get(params.property),
                    "loc": ""
            }
        })
