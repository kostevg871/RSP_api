import pytest
from src.app import app
from fastapi.testclient import TestClient


client = TestClient(app)


@pytest.mark.parametrize(
    "value_Pa, value_T, dimension_Pa, dimension_T, result_value, dimension",
    [
        (128000, 300, "Pa", "K", "-5237.194349516704", "J*kg^-1"),
        (612, 0.00001, "Pa", "K", "-632128.053918913", "J*kg^-1"),
        (10000, 500, "Pa", "K", "-1574285.4504253063", "J*kg^-1"),

        (10000, 500, "Pa", "K", "-1.5742854504253063", "MJ*kg^-1"),
        (10000, 500, "Pa", "K", "-1574.2854504253064", "kJ*kg^-1"),
        (100, 500, "MPa", "K", "-202918.26101543", "J*kg^-1"),
        (100, 500, "kPa", "K", "-1043783.5760100512", "J*kg^-1"),
        (100, 500, "bar", "K", "-306282.8155175421", "J*kg^-1"),
        (100, 500, "MPa", "K", "-202918.26101543", "J*kg^-1"),
        (100, 500, "MPa", "°C", "-1178630.2151640404", "J*kg^-1"),
        (100, 500, "MPa", "°F", "-288226.598327208", "J*kg^-1"),
        (100, -200, "MPa", "°C", "-295580.98670041945", "J*kg^-1"),
        (100, -200, "MPa", "°F", "91075.82925165482", "J*kg^-1"),
    ]
)
def test_prop_row_substance_PT_G_200(value_Pa, value_T, dimension_Pa, dimension_T, result_value, dimension):
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "G",
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
    assert res["data"]["propertyId"] == "Specific Gibbs energy"
    assert res["data"]["value"] == result_value
    assert res["data"]["dimension"] == dimension


@pytest.mark.parametrize(
    "value_Pa, value_T, msg_user, error",
    [
        # min Pa
        (1, 300, "Выход из диапозона вычисления: P < Pmin, параметр должен быть больше 611.65",
         "500: RSP core error: IF97: Value out of range in function GPT: pressure out of range: \"P < Pmin: 1.000000 < 611.657000\" "),
        # max Pa
        (10000000000, 0.00001, "Выход из диапозона вычисления: P > Pmax, параметр должен быть меньше 100000000.00",
         "500: RSP core error: IF97: Value out of range in function GPT: pressure out of range: P > Pmax: 10000000000.000000 > 100000000.000000"),
        # max T
        (10000, 5000, "Выход из диапозона вычисления: T > Tmax, параметр должен быть меньше 2273.15",
         "500: RSP core error: IF97: Value out of range in function GPT: temperature out of range: T > Tmax: 5000.000000 > 2273.150000"),
        # max T and max P
        (10000000000, 5000, "Выход из диапозона вычисления: T > Tmax, параметр должен быть меньше 2273.15",
         "500: RSP core error: IF97: Value out of range in function GPT: temperature out of range: T > Tmax: 5000.000000 > 2273.150000"),
    ]
)
def test_prop_row_substance_PT_G_400_out_of_range(value_Pa, value_T, msg_user, error):
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": "G",
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
