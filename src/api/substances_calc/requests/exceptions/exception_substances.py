from fastapi import HTTPException


def error_substance_id_count(substanceId: int, count_substance: int):
    raise HTTPException(status_code=400, detail={
        "code": 1,
        "type": "SubstanceNotFound",
        "error_info": "Не правильно указано вещество",
        "msg_user_ru": "substanceId={substanceId} должно быть в промежутке от 0 до {count_substance}"
        .format(substanceId=substanceId, count_substance=count_substance-1),
        "msg_user_en": "substanceId={substanceId} be in the range from 0 to {count_substance}"
        .format(substanceId=substanceId, count_substance=count_substance-1)})
