from app import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_prop_row_substance():
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
            "propertyId": "Density",
            "value": "996.5700260976184",
            "available_property_dimensions": [
                "kg*m^-3"
            ]
        }
    }
