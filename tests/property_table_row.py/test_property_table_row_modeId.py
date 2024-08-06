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
