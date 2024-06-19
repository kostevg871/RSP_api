from fastapi import HTTPException

from src.core.init import InitRSP


def error_substance_id_count(substanceId: int, count_substance: int):
    raise HTTPException(status_code=400, detail={
        "code": 1,
        "type": "SubstanceNotFound",
        "error_info": "Не правильно указано вещество",
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
        "error_info": "Не правильно указан мод для данного вещества",
        "msg_user_en": "mode={mode} not in substance".format(mode=mode),
        "msg_user_ru": "Мод={mode} не существует для данного вещества".format(mode=mode),
        "request_info": {"available_substances": substaneces_objects_globals.substances_calc_modes_id[substanceId]},
    })
