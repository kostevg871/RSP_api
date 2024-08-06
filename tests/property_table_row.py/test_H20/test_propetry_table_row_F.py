import pytest
from src.app import app
from fastapi.testclient import TestClient


client = TestClient(app)


@pytest.mark.parametrize(
    "value_Pa, value_T, dimension_Pa, dimension_T, result_value, dimension",
    [
        (128000, 300, "Pa", "K", "-5365.634897243392", "J*kg^-1"),
        (612, 0.00001, "Pa", "K", "-632128.7093146846", "J*kg^-1"),
        (10000, 500, "Pa", "K", "-1804954.3660445986", "J*kg^-1"),
        (10000, 500, "Pa", "K", "-1.8049543660445986", "MJ*kg^-1"),
        (10000, 500, "Pa", "K", "-1804.9543660445986", "kJ*kg^-1"),
        (100, 500, "MPa", "K", "-314127.6589532308", "J*kg^-1"),
        (100, 500, "kPa", "K", "-1273599.4759990084", "J*kg^-1"),
        (100, 500, "bar", "K", "-318215.51166032744", "J*kg^-1"),
        (100, 500, "MPa", "K", "-314127.6589532308", "J*kg^-1"),
        (100, 500, "MPa", "°C", "-1344473.1228465552", "J*kg^-1"),
        (100, 500, "MPa", "°F", "-403635.06409560586", "J*kg^-1"),
        (100, -200, "MPa", "°C", "-401723.6524352464", "J*kg^-1"),
        (100, -200, "MPa", "°F", "-16566.45014419791", "J*kg^-1"),
    ]
)
def test_prop_row_substance_PT_F_200(value_Pa, value_T, dimension_Pa, dimension_T, result_value, dimension):
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "F",
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
    assert res["data"]["propertyId"] == "Specific Helmholtz energy"
    assert res["data"]["value"] == result_value
    assert res["data"]["dimension"] == dimension


def test_prop_row_substance_PT_F_400_modeId_error():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
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


def test_prop_row_substance_PT_F_400_param_value_count():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "F",
                              "property_dimension": "J*kg^-1",
                              "param_values": [
                                  128000
                              ],
                              "param_dimensions": [
                                  "Pa", "K"
                              ]
                          }
                      }
                      )
    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 3
    assert res["detail"]["error_info"] == "Неправильно указано количество параметров для расчета"
    assert res["detail"][
        "msg_user_ru"] == "Поле параметры должно содержать 2 параметр(а) 'Pressure', 'Temperature'"


def test_prop_row_substance_PT_F_400_param_dimension_count():
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
                                  "Pa"
                              ]
                          }
                      }
                      )
    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 10
    assert res["detail"]["error_info"] == "Неправильно указано количество единиц измерения для расчета, ожидается `2`"
    assert res["detail"][
        "msg_user_ru"] == "Поле с единицами измерения должно содержать 2 параметр(а) 'Pressure', 'Temperature'"


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
