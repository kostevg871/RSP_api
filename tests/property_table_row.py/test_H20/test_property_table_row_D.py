from src.app import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_prop_row_substance_PT_D_1():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "D",
                              "property_dimension": "kg*m^-3",
                              "param_values": [
                                  128000, 200
                              ],
                              "param_dimensions": [
                                  "Pa", "K"
                              ]
                          }
                      }
                      )
    assert res.status_code == 200
    res = res.json()
    assert res["data"]["value"] == "926.1343613037452"
    assert res["data"]["propertyId"] == "Density"


def test_prop_row_substance_PT_D_2_empty_dimension():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "D",
                              "property_dimension": "",
                              "param_values": [
                                  700, 0.0000000001
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
    assert res["detail"]["msg_user_ru"] == "Укажите единицу измерения, ожидается ['kg*m^-3']"


def test_prop_row_substance_PT_D_dimension_error():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "D",
                              "property_dimension": "str",
                              "param_values": [
                                  700, -0.0000000001
                              ],
                              "param_dimensions": [
                                  "Pa", "°C"
                              ]
                          }
                      }
                      )
    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 15
    assert res["detail"]["msg_user_ru"] == "Единица измерения (str) не верна, ожидается ['kg*m^-3']"


def test_prop_row_substance_PT_D_3():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "D",
                              "property_dimension": "kg*m^-3",
                              "param_values": [
                                  700, -273.14444
                              ],
                              "param_dimensions": [
                                  "Pa", "°C"
                              ]
                          }
                      }
                      )
    assert res.status_code == 200
    res = res.json()
    assert res["data"]["value"] == "933.7869293793412"
    assert res["data"]["propertyId"] == "Density"
    assert res["data"]["dimension"] == "kg*m^-3"


def test_prop_row_substance_PT_D_Pa_Less_C():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "D",
                              "property_dimension": "kg*m^-3",
                              "param_values": [
                                  600, -273.14444
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
    assert res["detail"]["type"] == "OutOfRange"
    assert res["detail"]["msg_user_ru"] == "Выход из диапозона вычисления: P < Pmin, параметр должен быть больше 611.65"


def test_prop_row_substance_PT_D_Pa_More_C():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "D",
                              "property_dimension": "kg*m^-3",
                              "param_values": [
                                  100000000, -273.14444
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
    assert res["detail"]["type"] == "OutOfRange"
    assert res["detail"]["msg_user_ru"] == "Выход из диапозона вычисления: P > Pmax, параметр должен быть меньше 100000000.00"


def test_prop_row_substance_PT_D_C_Negative():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "D",
                              "property_dimension": "kg*m^-3",
                              "param_values": [
                                  100000000, -273.300
                              ],
                              "param_dimensions": [
                                  "MPa", "°C"
                              ]
                          }
                      }
                      )
    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 6
    assert res["detail"]["type"] == "ParameterLessMinValue"
    assert res["detail"]["msg_user_ru"] == "Параметр Temperature (°C) не может быть меньше -273.15"


def test_prop_row_substance_PT_D_C_More_Pa_More():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "D",
                              "property_dimension": "kg*m^-3",
                              "param_values": [
                                  100000000, 15000
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
    assert res["detail"]["type"] == "OutOfRange"
    assert res["detail"]["msg_user_ru"] == "Выход из диапозона вычисления: T > Tmax, параметр должен быть меньше 2273.15"


def test_prop_row_substance_PT_D_C_Less_Pa_Less():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "D",
                              "property_dimension": "kg*m^-3",
                              "param_values": [
                                  700, 0.00000000001
                              ],
                              "param_dimensions": [
                                  "Pa", "K"
                              ]
                          }
                      }
                      )
    assert res.status_code == 200
    res = res.json()
    assert res["data"]["propertyId"] == "Density"
    assert res["data"]["value"] == '933.7869293793411'
    assert res["data"]["dimension"] == "kg*m^-3"


def test_prop_row_substance_PT_D_C_More_Pa_Less():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "D",
                              "property_dimension": "kg*m^-3",
                              "param_values": [
                                  0, 100000
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
    assert res["detail"]["type"] == "OutOfRange"
    assert res["detail"]["error_info"] == "500: RSP core error: IF97: Value out of range in function DPT: pressure out of range: \"P < Pmin: 0.000000 < 611.657000\" temperature out of range: T > Tmax: 100000.000000 > 2273.150000"
    assert res["detail"]["msg_user_ru"] == "Выход из диапозона вычисления: T > Tmax, параметр должен быть меньше 2273.15"


def test_prop_row_substance_PT_D_C_Less_Pa_More():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "D",
                              "property_dimension": "kg*m^-3",
                              "param_values": [
                                  10000000, -20
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
    assert res["detail"]["type"] == "ParameterNotNegative"
    assert res["detail"]["error_info"] == "Параметр не может быть отрицательным"
    assert res["detail"]["msg_user_ru"] == "Параметр Temperature(K) не может быть отрицательным"


def test_prop_row_substance_PT_D_C_Less():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "D",
                              "property_dimension": "kg*m^-3",
                              "param_values": [
                                  1000, 3000
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
    assert res["detail"]["type"] == "OutOfRange"
    assert res["detail"]["msg_user_ru"] == "Выход из диапозона вычисления: T > Tmax, параметр должен быть меньше 2273.15"


def test_prop_row_substance_PT_D_400_P_less():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "D",
                              "property_dimension": "kg*m^-3",
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


def test_prop_row_substance_PT_D_400_P_more_and_MPa():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "D",
                              "property_dimension": "kg*m^-3",
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


def test_prop_row_substance_PT_D_400_T_more():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "D",
                              "property_dimension": "kg*m^-3",
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


def test_prop_row_substance_PT_D_200_T_less_and_C():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "D",
                              "property_dimension": "kg*m^-3",
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
    assert res["data"]["value"] == "933.8617746435223"
    assert res["data"]["dimension"] == "kg*m^-3"


def test_prop_row_substance_PT_D_400_T_more():
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "D",
                              "property_dimension": "kg*m^-3",
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
