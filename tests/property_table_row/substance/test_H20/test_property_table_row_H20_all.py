import pytest
from src.app import app
from fastapi.testclient import TestClient


client = TestClient(app)

list_name_property = ["G", "H", "JOULETHOMPSON", "KINVIS", "K", "PRANDTLE"]


@pytest.mark.parametrize(
    "property, value_Pa, value_T, dimension_Pa, dimension_T, result_value, dimension, nameProperty, dimension_result",
    [
        ("G", 128000, 300, "Pa", "K", "-5237.194349516704",
         "J*kg^-1", list_name_property[0],
         "J*kg^-1"),
        ("G", 12, 300, "MPa", "°C", "-515916.7376856731",
         "J*kg^-1", list_name_property[0],
         "J*kg^-1"),
        ("G", 12, 300, "kPa", "°F", "-848661.8144192131",
         "J*kg^-1", list_name_property[0],
         "J*kg^-1"),
        ("G", 12, 300, "bar", "°F", "-144341.78288531405",
         "J*kg^-1", list_name_property[0],
         "J*kg^-1"),
        ("G", 12, 300, "MPa", "°C", "-515.9167376856731",
         "kJ*kg^-1", list_name_property[0],
         "J*kg^-1"),
        ("G", 12, 300, "MPa", "°C", "-0.5159167376856731",
         "MJ*kg^-1", list_name_property[0],
         "J*kg^-1"),

        ("H", 128000, 300, "Pa", "K", "112689.60702009771",
         "J*kg^-1", list_name_property[1],
         "J*kg^-1"),
        ("H", 12, 300, "MPa", "°C", "1340927.933819088",
         "J*kg^-1", list_name_property[1],
         "J*kg^-1"),
        ("H", 12, 300, "kPa", "°F", "2780745.7475517127",
         "J*kg^-1", list_name_property[1],
         "J*kg^-1"),
        ("H", 12, 300, "bar", "°F", "627913.4759873614",
         "J*kg^-1", list_name_property[1],
         "J*kg^-1"),
        ("H", 12, 300, "MPa", "°C", "1340.927933819088",
         "kJ*kg^-1", list_name_property[1],
         "J*kg^-1"),
        ("H", 12, 300, "MPa", "°C", "1.340927933819088",
         "MJ*kg^-1", list_name_property[1],
         "J*kg^-1"),

        ("JOULETHOMPSON", 128000, 300, "Pa", "K", "-2.2024222617008712e-07",
         "", list_name_property[2], None),
        ("JOULETHOMPSON", 12, 300, "MPa", "°C", "1.8404348605551601e-07",
         None, list_name_property[2], None),
        ("JOULETHOMPSON", 12, 300, "kPa", "°F", "3.67455389885102e-05",
         "", list_name_property[2], None),
        ("JOULETHOMPSON", 12, 300, "bar", "°F", "-1.4434013979009482e-07",
         "", list_name_property[2], None),

        ("KINVIS", 128000, 300, "Pa", "K", "8.566782314928749e-07",
         "m^2*s^-1", list_name_property[3]),
        ("KINVIS", 12, 300, "MPa", "°C", "1.212175524785805e-07",
         "m^2*s^-1", list_name_property[3]),
        ("KINVIS", 12, 300, "kPa", "°F", "0.00023029375083972556",
         "m^2*s^-1", list_name_property[3]),
        ("KINVIS", 12, 300, "bar", "°F", "2.0061886257087348e-07",
         "m^2*s^-1", list_name_property[3]),

        ("K", 128000, 300, "Pa", "K", "17592.010456360873",
         "", list_name_property[4], None),
        ("K", 12, 300, "MPa", "°C", "53.05606327360655",
         "", list_name_property[4], None),
        ("K", 12, 300, "kPa", "°F", "1.3177044655181127",
         "", list_name_property[4], None),
        ("K", 12, 300, "bar", "°F",  "1654.7550507026367",
         "", list_name_property[4], None),

        ("PRANDTLE", 128000, 300, "Pa", "K", "5.856292422180345",
         "", list_name_property[5], None),
        ("PRANDTLE", 12, 300, "MPa", "°C", "0.8735411923533657",
         "", list_name_property[5], None),
        ("PRANDTLE", 12, 300, "kPa", "°F", "0.9599325318329516",
         "", list_name_property[5], None),
        ("PRANDTLE", 12, 300, "bar", "°F",  "1.1635753697592135",
         "", list_name_property[5], None),
    ]
)
def test_prop_row_substance_PT_200(property, value_Pa, value_T, dimension_Pa, dimension_T, result_value, dimension, nameProperty, dimension_result):
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
                              "property": property,
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
    assert res["data"]["propertyId"] == nameProperty
    assert res["data"]["value"] == result_value
    assert res["data"]["dimension"] == dimension_result
