from src.app import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_get_available_substances_422_not_req():
    res = client.get("/getPropertiesLists")
    assert res.status_code == 422
    assert res.json() == {
        "detail": {
            "status_code": 422,
            "description": "Field required",
            "msg": "Не правильно введены данные!"

        }}


def test_get_available_substances_422_bad_req():
    res = client.get("/getPropertiesLists?substanceId=ss&modeId=ss")
    assert res.status_code == 422
    assert res.json() == {
        "detail": {
            "status_code": 422,
            "description": "Input should be a valid integer, unable to parse string as an integer",
            "msg": "Не правильно введены данные!"

        }}


def test_get_available_substances_200_subs_1_mode_PT():
    res = client.get("/getPropertiesLists?substanceId=1&modeId=PT")
    assert res.status_code == 200
    assert res.json() == {
        "data": {
            "CP": "Isobaric heat capacity",
            "CV": "Isochoric heat capacity",
            "D": "Density",
            "DYNVIS": "Dynamic viscosity",
            "F": "Specific Helmholtz energy",
            "G": "Specific Gibbs energy",
            "H": "Specific enthropy",
            "JOULETHOMPSON": "Joule-Thompson coefficient",
            "KINVIS": "Kinematic viscosity",
            "K": "Isoenthropic coefficient",
            "PRANDTLE": "Prandtl number",
            "S": "Specific enthalpy",
            "THERMCOND": "Thermal conductivity",
            "U": "Specific internal energy",
            "V": "Specific volume",
            "W": "Speed of sound"
        }
    }


def test_get_available_substances_200_sub_1_mode_TX():
    res = client.get("/getPropertiesLists?substanceId=1&modeId=tx")
    assert res.status_code == 200
    assert res.json() == {
        "data": {
            "CVS": "Isochoric heat capacity",
            "DS": "Density",
            "DYNVISS": "Dynamic viscosity",
            "FS": "Specific Helmholtz energy",
            "GS": "Specific Gibbs energy",
            "KINVISS": "Kinematic viscosity",
            "KS": "Isoenthropic coefficient",
            "PRANDTLES": "Prandtl number",
            "THERMCONDS": "Thermal conductivity",
            "US": "Specific internal energy",
            "VS": "Specific volume",
            "WS": "Speed of sound"
        }
    }


def test_get_available_substances_400_sub_fail_mode_fail():
    id = 5
    res = client.get(
        "/getPropertiesLists?substanceId={id}&modeId=fail".format(id=id))
    assert res.status_code == 400
    assert res.json() == {
        "detail": {
            "code": 1,
            "type": "SubstanceNotFound",
            "error_info": "Неправильно указано вещество",
            "msg_user_ru": "substanceId={id} должно быть в промежутке от 0 до 4".format(id=id),
            "msg_user_en": "substanceId={id} be in the range from 0 to 4".format(id=id),
            "request_info": None
        }
    }


def test_get_available_substances_400_sub_0_mode_fail():
    mode = "DT"
    res = client.get(
        "/getPropertiesLists?substanceId=0&modeId={mode}".format(mode=mode))
    assert res.status_code == 400
    assert res.json() == {
        "detail": {
            "code": 2,
            "type": "ModeNotFound",
            "error_info": "Неправильно указан мод для данного вещества",
            "msg_user_en": "mode={mode} not in substance".format(mode=mode.upper()),
            "msg_user_ru": "Мод={mode} не существует для данного вещества".format(mode=mode.upper()),
            "request_info": {
                "available_substances": [
                    'HS',
                    'P',
                    'PH',
                    'PS',
                    'PT',
                    'T',
                    'TX',
                ]
            }
        }
    }
