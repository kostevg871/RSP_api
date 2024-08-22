import pytest
from src.app import app
from fastapi.testclient import TestClient


client = TestClient(app)


@pytest.mark.parametrize(
    "value_Pa, value_T, dimension_Pa, dimension_T, result_value, dimension",
    [
        (128000, 300, "Pa", "K", "112689.60702009771", "J*kg^-1"),
        (612, 0.00001, "Pa", "K", "-632128.0871922886", "J*kg^-1"),

        (10000, 500, "Pa", "K", "2931967.281061654", "J*kg^-1"),
        (10000, 500, "Pa", "K", "2.931967281061654", "MJ*kg^-1"),
        (10000, 500, "Pa", "K", "2931.967281061654", "kJ*kg^-1"),

        (100, 500, "MPa", "K", "1015393.6760197142", "J*kg^-1"),
        (100, 500, "kPa", "K", "2928585.332824713", "J*kg^-1"),
        (100, 500, "bar", "K", "977213.9101189049", "J*kg^-1"),

        (100, 500, "MPa", "°C", "2316227.7742722193", "J*kg^-1"),
        (100, 500, "MPa", "°F", "1155610.7062877498", "J*kg^-1"),
        (100, -200, "MPa", "°C", "-503894.842275367", "J*kg^-1"),
        (100, -200, "MPa", "°F", "-256875.71103206312", "J*kg^-1"),
    ]
)
def test_prop_row_substance_PT_H_200(value_Pa, value_T, dimension_Pa, dimension_T, result_value, dimension):
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "H",
                              "property_dimension": dimension,
                              "param_values": [
                                  value_Pa, value_T
                              ],
                              "param_dimensions": [
                                  dimension_Pa, dimension_T
                              ]
                          }
                      }
                      )
    assert res.status_code == 200
    res = res.json()
    assert res["data"]["propertyId"] == "Specific enthropy"
    assert res["data"]["value"] == result_value
    assert res["data"]["dimension"] == dimension





def test_prop_row_substance_PT_F_400_property_dimension():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "F",
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
    assert res["detail"]["code"] == 15
    assert res["detail"]["error_info"] == "Не правильно указаны единицы измерения"
    assert res["detail"][
        "msg_user_ru"] == "Единица измерения (Nan) не верна, ожидается ['J*kg^-1', 'kJ*kg^-1', 'MJ*kg^-1']"


def test_prop_row_substance_PT_F_400_negative():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "F",
                              "property_dimension": "J*kg^-1",
                              "param_values": [
                                  -128000, 300
                              ],
                              "param_dimensions": [
                                  "Pa", "K"
                              ]
                          }
                      }
                      )
    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 5
    assert res["detail"]["error_info"] == "Параметр не может быть отрицательным"
    assert res["detail"][
        "msg_user_ru"] == "Параметр Pressure(Pa) не может быть отрицательным"


def test_prop_row_substance_PT_F_400_invalid_dim():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "F",
                              "property_dimension": "J*kg^-1",
                              "param_values": [
                                  128000, 300
                              ],
                              "param_dimensions": [
                                  "Nan", "K"
                              ]
                          }
                      }
                      )
    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 7
    assert res["detail"]["error_info"] == "Не правильно указаны единицы измерения"
    assert res["detail"][
        "msg_user_ru"] == "Единица измерения (Nan) не верна"


def test_prop_row_substance_PT_F_400_zero_T():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "F",
                              "property_dimension": "J*kg^-1",
                              "param_values": [
                                  128000, 0
                              ],
                              "param_dimensions": [
                                  "Pa", "K"
                              ]
                          }
                      }
                      )
    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 9
    assert res["detail"][
        "error_info"] == "Calculation error in rsp, try other parameters (Error calculating core!!!, change the source data)"
    assert res["detail"][
        "msg_user_ru"] == "Ошибка вычисления, используйте другие данные"


def test_prop_row_substance_PT_F_400_negative_T():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "F",
                              "property_dimension": "J*kg^-1",
                              "param_values": [
                                  128000, -10
                              ],
                              "param_dimensions": [
                                  "Pa", "K"
                              ]
                          }
                      }
                      )
    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 5
    assert res["detail"][
        "error_info"] == "Параметр не может быть отрицательным"
    assert res["detail"][
        "msg_user_ru"] == "Параметр Temperature(K) не может быть отрицательным"


@pytest.mark.parametrize(
    "value_Pa, value_T, msg_user, error",
    [
        # min Pa
        (1, 300, "Выход из диапозона вычисления: P < Pmin, параметр должен быть больше 611.65",
         "500: RSP core error: IF97: Value out of range in function FPT: pressure out of range: \"P < Pmin: 1.000000 < 611.657000\" "),
        # max Pa
        (10000000000, 0.00001, "Выход из диапозона вычисления: P > Pmax, параметр должен быть меньше 100000000.00",
         "500: RSP core error: IF97: Value out of range in function FPT: pressure out of range: P > Pmax: 10000000000.000000 > 100000000.000000"),
        # max T
        (10000, 5000, "Выход из диапозона вычисления: T > Tmax, параметр должен быть меньше 2273.15",
         "500: RSP core error: IF97: Value out of range in function FPT: temperature out of range: T > Tmax: 5000.000000 > 2273.150000"),
        # max T and max P
        (10000000000, 5000, "Выход из диапозона вычисления: T > Tmax, параметр должен быть меньше 2273.15",
         "500: RSP core error: IF97: Value out of range in function FPT: temperature out of range: T > Tmax: 5000.000000 > 2273.150000"),
    ]
)
def test_prop_row_substance_PT_F_400_out_of_range(value_Pa, value_T, msg_user, error):
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "F",
                              "property_dimension": "J*kg^-1",
                              "param_values": [
                                  value_Pa, value_T
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
    assert res["detail"]["error_info"] == error
    assert res["detail"][
        "msg_user_ru"] == msg_user
