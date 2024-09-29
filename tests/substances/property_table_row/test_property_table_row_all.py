import pytest
from src.app import app
from fastapi.testclient import TestClient


client = TestClient(app)


@pytest.mark.parametrize(
    "substanceId",
    argvalues=[0, 1, 2, 3, 4]
)
def test_prop_row_substance_PT_property_400_modeId_error_2(substanceId):
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": substanceId,
                          "modeId": "Nan",
                          "params": {
                              "property": "Nan",
                              "property_dimension": "Nan",
                              "param_values": [
                                  128000, 300
                              ],
                              "param_dimensions": [
                                  "Pa", "K"
                              ]
                          }
                      }
                      )
    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 2
    assert res["detail"]["error_info"] == "Неправильно указан мод для данного вещества"
    assert res["detail"]["msg_user_ru"] == "Мод=NAN не существует для данного вещества"


@pytest.mark.parametrize(
    "substanceId",
    argvalues=[-1, -5, 5, 10]
)
def test_prop_row_substance_PT_property_400_modeId_error_1(substanceId):
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": substanceId,
                          "modeId": "Nan",
                          "params": {
                              "property": "Nan",
                              "property_dimension": "Nan",
                              "param_values": [
                                  128000, 300
                              ],
                              "param_dimensions": [
                                  "Pa", "K"
                              ]
                          }
                      }
                      )
    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 1
    assert res["detail"]["error_info"] == "Неправильно указано вещество"
    assert res["detail"]["msg_user_ru"] == "substanceId={substanceId} должно быть в промежутке от 0 до 4".format(
        substanceId=substanceId)


def test_prop_row_substance_error_UnphysicalTwoPhase():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PH",
                          "params": {
                              "property": "CP",
                              "property_dimension": "J*kg^-1*K^-1",
                              "param_values": [
                                  128851.478, 558034.329
                              ],
                              "param_dimensions": [
                                  "Pa", "J*kg^-1"
                              ]
                          }
                      }
                      )
    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 14
    assert res["detail"]["error_info"] == "500: RSP core error: IF97: isobaric heat capacity is unphysical in two-phase region, function CPSTX"
    assert res["detail"]["msg_user_ru"] == "Изобарная теплоемкость нефизична в двухфазной области"


@pytest.mark.parametrize(
    "modeId",
    argvalues=["HS",
               "P",
               "PH",
               "PS",
               "PT",
               "T",
               "TX"]
)
def test_prop_row_substance_all_400_modeId_error(modeId):
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": modeId,
                          "params": {
                              "property": "Nan",
                              "property_dimension": "J*kg^-1",
                              "param_values": [
                                  128000, 300
                              ],
                              "param_dimensions": [
                                  "Pa", "K"
                              ]
                          }
                      }
                      )
    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 4
    assert res["detail"]["error_info"] == "Неправильно указано свойство для расчета, не существует для данного вещества"
    assert res["detail"]["msg_user_ru"] == "Свойство=Nan не существует для данного вещества"


def test_prop_row_substance_all_400_error_12():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PH",
                          "params": {
                              "property": "CP",
                              "property_dimension": "J*kg^-1*K^-1",
                              "param_values": [
                                  128851.478, 0
                              ],
                              "param_dimensions": [
                                  "Pa", "J*kg^-1"
                              ]
                          }
                      }
                      )
    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 12
    assert res["detail"]["error_info"] == "500: RSP core error: bad_function_call"
    assert res["detail"]["msg_user_ru"] == "Неизвестная ошибка, измените параметры расчета"


def test_prop_row_substance_check_verification_Prandle():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "PRANDTLE",
                              "property_dimension": "",
                              "param_values": [
                                  100, 200
                              ],
                              "param_dimensions": [
                                  "MPa", "K"
                              ]
                          }
                      }
                      )
    assert res.status_code == 200
    res = res.json()
    assert res["data"]["dimension"] == None
