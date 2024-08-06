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
