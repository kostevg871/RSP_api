from src.app import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_prop_row_substance_PT_D():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "Pt",
                          "params": {
                              "property": "D",
                              "property_dimension": "kg*m^-3",
                              "param_values": [
                                  128000, 300
                              ],
                              "param_dimensions": [
                                  "Pa", "K"
                              ]
                          }
                      }
                      )
    assert res.status_code == 200
    assert res.json() == {
        "available_param_dimensions": [
            [
                "Pa",
                "kPa",
                "MPa",
                "bar"
            ],
            [
                "K",
                "°C",
                "°F"
            ]
        ],
        "data": {
            "dimension": "kg*m^-3",
            "propertyId": "D",
            "propertyName": "Density",
            "value": "996.5700260976184",
            "available_property_dimensions": [
                "kg*m^-3"
            ]
        }
    }


def test_prop_row_substance_PT_CP_200_1():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "CP",
                              "property_dimension": "J*kg^-1*K^-1",
                              "param_values": [
                                  650, 2200
                              ],
                              "param_dimensions": [
                                  "Pa", "K"
                              ]
                          }
                      }
                      )
    assert res.status_code == 200
    res = res.json()
    assert res["data"]["value"] == "2907.8370093776625"
    assert res["data"]["available_property_dimensions"] == ["J*kg^-1*K^-1"]


def test_prop_row_substance_PT_CP_400_P_less():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "CP",
                              "property_dimension": "J*kg^-1*K^-1",
                              "param_values": [
                                  1, 1
                              ],
                              "param_dimensions": [
                                  "Pa", "°C"
                              ]
                          }
                      }
                      )
    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 8
    assert res["detail"]["msg_user_ru"] == "Выход из диапозона вычисления: P < Pmin, параметр должен быть больше 611.65"


def test_prop_row_substance_PT_CP_400_P_more_and_MPa():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "CP",
                              "property_dimension": "J*kg^-1*K^-1",
                              "param_values": [
                                  12000, 1
                              ],
                              "param_dimensions": [
                                  "MPa", "°C"
                              ]
                          }
                      }
                      )
    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 8
    assert res["detail"]["msg_user_ru"] == "Выход из диапозона вычисления: P > Pmax, параметр должен быть меньше 100000000.00"


def test_prop_row_substance_PT_CP_400_T_more_Pa_min():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "CP",
                              "property_dimension": "J*kg^-1*K^-1",
                              "param_values": [
                                  1, 3000
                              ],
                              "param_dimensions": [
                                  "MPa", "°C"
                              ]
                          }
                      }
                      )
    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 8
    assert res["detail"]["msg_user_ru"] == "Выход из диапозона вычисления: T > Tmax, параметр должен быть меньше 2273.15"


def test_prop_row_substance_PT_CP_200_T_less_and_C():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "CP",
                              "property_dimension": "J*kg^-1*K^-1",
                              "param_values": [
                                  1, -237.010101010101010101001010101
                              ],
                              "param_dimensions": [
                                  "MPa", "°C"
                              ]
                          }
                      }
                      )
    assert res.status_code == 200
    res = res.json()
    assert res["data"]["value"] == "297.67712051632094"


def test_prop_row_substance_PT_CP_400_T_more():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "CP",
                              "property_dimension": "J*kg^-1*K^-1",
                              "param_values": [
                                  128000, 5000
                              ],
                              "param_dimensions": [
                                  "Pa", "K"
                              ]
                          }
                      }
                      )
    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 8
    assert res["detail"]["msg_user_ru"] == "Выход из диапозона вычисления: T > Tmax, параметр должен быть меньше 2273.15"
