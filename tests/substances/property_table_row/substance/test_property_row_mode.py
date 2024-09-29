import pytest
from src.app import app
from fastapi.testclient import TestClient


client = TestClient(app)


@pytest.mark.parametrize(
    "substanceId, modeId, count, name_dimension, property, param_dimension, param_value",
    [
        (0, "HS", 2, "'Enthalpy', 'Enthropy'", "CP", ["Pa"], [100, 200]),
        (0, "P", 1,  "'Saturation pressure'", "TS", ["MPa", "Pa"], [100]),
        (0, "PS",  2, "'Pressure', 'Enthropy'", "CP", ["MPa"], [100, 200]),
        (0, "PT",  2, "'Pressure', 'Temperature'", "CP", ["MPa"], [100, 200]),
        (0, "T", 1,  "'Saturation temperature'", "CPSS", ["MPa", "Pa"], [100]),
        (0, "TX", 2, "'Saturation temperature', 'Steam mass fraction'",
         "GS", ["Pa"], [100, 200]),

        (1, "DT", 2, "'Density', 'Temperature'", "CP", ["Pa"], [100, 200]),
        (1, "HS", 2, "'Enthalpy', 'Enthropy'", "CP", ["Pa"], [100, 200]),
        (1, "P", 1,  "'Saturation pressure'", "TS", ["MPa", "Pa"], [100]),
        (1, "PH", 2, "'Pressure', 'Enthalpy'", "CP", ["Pa"], [100, 200]),
        (1, "PS",  2, "'Pressure', 'Enthropy'", "CP", ["MPa"], [100, 200]),
        (1, "PT",  2, "'Pressure', 'Temperature'", "CP", ["MPa"], [100, 200]),
        (1, "T", 1,  "'Saturation temperature'", "CPSS", ["MPa", "Pa"], [100]),
        (1, "TX", 2, "'Saturation temperature', 'Steam mass fraction'",
         "GS", ["Pa"], [100, 200]),

        (2, "DT", 2, "'Density', 'Temperature'", "CP", ["Pa"], [100, 200]),
        (2, "T", 1,  "'Saturation temperature'", "CPSS", ["MPa", "Pa"], [100]),
        (2, "TX", 2, "'Saturation temperature', 'Steam mass fraction'",
         "GS", ["Pa"], [100, 200]),

        (3, "DT", 2, "'Density', 'Temperature'", "CP", ["Pa"], [100, 200]),
        (3, "PT",  2, "'Pressure', 'Temperature'", "CP", ["MPa"], [100, 200]),
        (3, "T", 1,  "'Saturation temperature'", "CPSS", ["MPa", "Pa"], [100]),
        (3, "TX", 2, "'Saturation temperature', 'Steam mass fraction'",
         "GS", ["Pa"], [100, 200]),

        (4, "DT", 2, "'Density', 'Temperature'", "CP", ["Pa"], [100, 200]),
        (4, "P", 1,  "'Saturation pressure'", "TS", ["MPa", "Pa"], [100]),
        (4, "PH", 2, "'Pressure', 'Enthalpy'", "CP", ["Pa"], [100, 200]),
        (4, "PS",  2, "'Pressure', 'Enthropy'", "CP", ["MPa"], [100, 200]),
        (4, "PT",  2, "'Pressure', 'Temperature'", "CP", ["MPa"], [100, 200]),
        (4, "T", 1,  "'Saturation temperature'", "CPSS", ["MPa", "Pa"], [100]),
        (4, "TX", 2, "'Saturation temperature', 'Steam mass fraction'",
         "GS", ["Pa"], [100, 200]),
    ]
)
def test_prop_row_substance_PT_F_400_param_dimension_count(substanceId, modeId, count, name_dimension, property, param_dimension, param_value):
    res = client.post("/getPropertiesTableRow",
                      json={
                          "substanceId": substanceId,
                          "modeId": modeId,
                          "params": {
                              "property": property,
                              "property_dimension": "Nan",
                              "param_values":
                                  param_value,
                              "param_dimensions":
                                  param_dimension

                          }
                      }
                      )
    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 10
    assert res["detail"]["error_info"] == "Неправильно указано количество единиц измерения для расчета, ожидается `{count}`".format(
        count=count)
    assert res["detail"][
        "msg_user_ru"] == "Поле с единицами измерения должно содержать {count} параметр(а) {name_dimension}".format(count=count, name_dimension=name_dimension)
