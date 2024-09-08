import pytest
from src.app import app
from fastapi.testclient import TestClient


client = TestClient(app)

list_name_property = ["JOULETHOMPSON", "K", "PRANDTLE"]


@pytest.mark.parametrize(
    "value_1, value_2, dimension_1, dimension_2,  nameProperty, dimension_result, available_dimensions",
    [
        (10, 10, "J*kg^-1", "J*kg^-1*K^-1",
         list_name_property,
         None, None),
    ]
)
def test_prop_row_substance_HS_200(value_1, value_2, dimension_1, dimension_2,  nameProperty, dimension_result, available_dimensions):
    res = client.post("/getPropertiesTable",
                      json={
                          "substanceId": 0,
                          "modeId": "HS",
                          "params": {

                              "param_values": [
                                  value_1, value_2
                              ],
                              "param_dimensions": [
                                  dimension_1, dimension_2
                              ]
                          }
                      }
                      )
    assert res.status_code == 200
    res = res.json()
    assert res["data"][5]["propertyId"] == nameProperty[0]
    assert res["data"][5]["dimension"] == dimension_result
    assert res["data"][5]["available_dimensions"] == available_dimensions

    assert res["data"][6]["propertyId"] == nameProperty[1]
    assert res["data"][6]["dimension"] == dimension_result
    assert res["data"][6]["available_dimensions"] == available_dimensions

    assert res["data"][7]["propertyId"] == nameProperty[2]
    assert res["data"][7]["dimension"] == dimension_result
    assert res["data"][7]["available_dimensions"] == available_dimensions
