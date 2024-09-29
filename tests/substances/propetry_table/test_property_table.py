import pytest
from app import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_get_property_table_200_0_PT_DYNVIS():
    res = client.post("/getPropertiesTable", json={
        "substanceId": 0,
        "modeId": "PT",
        "params": {
            "param_values": [
                101325, 300.0
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
        "data": [
            {
                "dimension": "J*kg^-1*K^-1",
                "propertyId": "CP",
                "value": "4181.09732677412102930247783660888671875",
                "available_dimensions": [
                    "J*kg^-1*K^-1"
                ]
            },
            {
                "dimension": "J*kg^-1*K^-1",
                "propertyId": "CV",
                "value": "4130.685100382877863012254238128662109375",
                "available_dimensions": [
                    "J*kg^-1*K^-1"
                ]
            },
            {
                "dimension": "kg*m^-3",
                "propertyId": "D",
                "value": "996.558076096375089036882854998111724853515625",
                "available_dimensions": [
                    "kg*m^-3"
                ]
            },
            {
                "dimension": "Pa*s",
                "propertyId": "DYNVIS",
                "value": "0.000853742256229957498063487530970405714469961822032928466796875",
                "available_dimensions": [
                    "Pa*s"
                ]
            },
            {
                "dimension": "J*kg^-1",
                "propertyId": "F",
                "value": "-5365.636276923120021820068359375",
                "available_dimensions": [
                    "J*kg^-1",
                    "kJ*kg^-1",
                    "MJ*kg^-1"
                ]
            },
            {
                "dimension": "J*kg^-1",
                "propertyId": "G",
                "value": "-5263.961319456602723221294581890106201171875",
                "available_dimensions": [
                    "J*kg^-1",
                    "kJ*kg^-1",
                    "MJ*kg^-1"
                ]
            },
            {
                "dimension": "J*kg^-1",
                "propertyId": "H",
                "value": "112665.043418539789854548871517181396484375",
                "available_dimensions": [
                    "J*kg^-1",
                    "kJ*kg^-1",
                    "MJ*kg^-1"
                ]
            },
            {
                "dimension": None,
                "propertyId": "JOULETHOMPSON",
                "value": "-2.20242891312057205288266127814200689982726544258184731006622314453125E-7",
                "available_dimensions": None
            },
            {
                "dimension": "m^2*s^-1",
                "propertyId": "KINVIS",
                "value": "8.56690921189618472472173359155700467226779437623918056488037109375E-7",
                "available_dimensions": [
                    "m^2*s^-1"
                ]
            },
            {
                "dimension": None,
                "propertyId": "K",
                "value": "22221.7957777002520742826163768768310546875",
                "available_dimensions": None
            },
            {
                "dimension": None,
                "propertyId": "PRANDTLE",
                "value": "5.85655774372549142725574711221270263195037841796875",
                "available_dimensions": None
            },
            {
                "dimension": "J*kg^-1*K^-1",
                "propertyId": "S",
                "value": "393.096682459987960100988857448101043701171875",
                "available_dimensions": [
                    "J*kg^-1*K^-1",
                    "kJ*kg^-1*K^-1",
                    "MJ*kg^-1*K^-1"
                ]
            },
            {
                "dimension": "W*m^-1",
                "propertyId": "THERMCOND",
                "value": "0.6095012841120712732134734324063174426555633544921875",
                "available_dimensions": [
                    "W*m^-1",
                    "kW*m^-1",
                    "MW*m^-1"
                ]
            },
            {
                "dimension": "J*kg^-1",
                "propertyId": "U",
                "value": "112563.368461073274374939501285552978515625",
                "available_dimensions": [
                    "J*kg^-1",
                    "kJ*kg^-1",
                    "MJ*kg^-1"
                ]
            },
            {
                "dimension": "m^3*kg^-1",
                "propertyId": "V",
                "value": "0.001003453811660537896288669656996717094443738460540771484375",
                "available_dimensions": [
                    "m^3*kg^-1"
                ]
            },
            {
                "dimension": "m*s^-1",
                "propertyId": "W",
                "value": "1503.130114303818800181034021079540252685546875",
                "available_dimensions": [
                    "m*s^-1"
                ]
            }
        ]
    }

    # assert res.status_code == 400
    # res = res.json()
    # assert res["detail"]["code"] == 11
    # assert res["detail"]["error_info"] == "\"Units ('Pa', 1) are not of the same dimension !\""
    # assert res["detail"]["msg_user_ru"] == "Единица измерения ('Pa') не верна, ожидается ['K', '°C', '°F']"


def test_get_property_table_400_Out_Of_range_1():
    res = client.post("/getPropertiesTable", json={
        "substanceId": 0,
        "modeId": "PT",
        "params": {
            "param_values": [
                1000000000, 300.0
            ],
            "param_dimensions": [
                "Pa", "K"
            ]
        }
    }
    )

    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 13
    assert res["detail"]["error_info"] == "IF97: Value out of range in function CPPT: pressure out of range: P > Pmax: 1000000000.000000 > 100000000.000000"
    assert res["detail"]["msg_user_ru"] == "Выход из диапозона вычисления: P > Pmax, параметр должен быть меньше 100000000.00"


def test_get_property_table_400_Out_Of_range_2():
    res = client.post("/getPropertiesTable", json={
        "substanceId": 0,
        "modeId": "PT",
        "params": {
            "param_values": [
                1, 300.0
            ],
            "param_dimensions": [
                "Pa", "K"
            ]
        }
    }
    )

    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 13
    assert res["detail"]["error_info"] == "IF97: Value out of range in function CPPT: pressure out of range: \"P < Pmin: 1.000000 < 611.657000\" "
    assert res["detail"]["msg_user_ru"] == "Выход из диапозона вычисления: P < Pmin, параметр должен быть больше 611.65"


def test_get_property_table_400_Out_Of_range_3():
    res = client.post("/getPropertiesTable", json={
        "substanceId": 0,
        "modeId": "PT",
        "params": {
            "param_values": [
                1, 0
            ],
            "param_dimensions": [
                "Pa", "K"
            ]
        }
    }
    )

    assert res.status_code == 400
    res = res.json()

    assert res["detail"]["code"] == 13
    assert res["detail"]["error_info"] == "IF97: Value out of range in function CPPT: pressure out of range: \"P < Pmin: 1.000000 < 611.657000\" "
    assert res["detail"]["msg_user_ru"] == "Выход из диапозона вычисления: P < Pmin, параметр должен быть больше 611.65"


def test_prop_row_substance_error_UnphysicalTwoPhase_table():
    res = client.post("/getPropertiesTable",
                      json={
                          "substanceId": 0,
                          "modeId": "PH",
                          "params": {

                              "param_values": [
                                  128851.478, 558034.329
                              ],
                              "param_dimensions": [
                                  "Pa", "J*kg^-1"
                              ]
                          }
                      }
                      )
    assert res.status_code == 200
    res = res.json()
    assert res["data"][0]["value"] == "NaN: IF97: isobaric heat capacity is unphysical in two-phase region, function CPSTX"


def test_prop_row_substance_error_Nan_table():
    res = client.post("/getPropertiesTable",
                      json={
                          "substanceId": 0,
                          "modeId": "PT",
                          "params": {
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
    assert res["detail"]["msg_user_ru"] == "Ошибка вычисления, используйте другие данные"


def test_prop_row_substance_error_unknown_12():
    res = client.post("/getPropertiesTable",
                      json={
                          "substanceId": 0,
                          "modeId": "PH",
                          "params": {
                              "property": "CP",
                              "property_dimension": "J*kg^-1*K^-1",
                              "param_values": [
                                  128851.478, 0
                              ],
                              "param_dimensions": [
                                  "Pa", "J*kg^-1"
                              ]
                          }
                      }
                      )
    assert res.status_code == 400
    res = res.json()

    assert res["detail"]["code"] == 12
    assert res["detail"][
        "error_info"] == "bad_function_call"
    assert res["detail"]["msg_user_ru"] == "Неизвестная ошибка, измените параметры расчета"


@pytest.mark.parametrize(
    "substance, modeId, values,  dimensions, count_result_1, result_value_1, count_result_2, result_value_2, ",
    [
        (0, "PT", [700, 0.0000000001],  ["Pa", "K"],
         3, "Infinity", 10, "NaN"),
        (0, "PT", [700, -0.0000000001],  ["Pa", "°C"],
         0, "2096.71055530725288917892612516880035400390625", 1, "-9545.186238230473463772796094417572021484375"),
        (0, "PT", [700, -0.0000000001],  ["Pa", "°F"],
         0, "1932.9566641795781833934597671031951904296875", 1, "1471.315166277382331827539019286632537841796875"),
        (1, "TX", [100, 0.0000000001],  ["K",  " "],
         0, "2176.61268772477706079371273517608642578125", 1, "689.3755530267420681411749683320522308349609375"),

    ]
)
def test_prop_substance_200(substance, modeId, values,  dimensions, result_value_1, result_value_2, count_result_1, count_result_2):
    res = client.post("/getPropertiesTable",
                      json={
                          "substanceId": substance,
                          "modeId": modeId,
                          "params": {
                              "param_values": values,
                              "param_dimensions": dimensions
                          }
                      }
                      )
    assert res.status_code == 200
    res = res.json()
    assert res["data"][count_result_1]["value"] == result_value_1
    assert res["data"][count_result_2]["value"] == result_value_2


def test_get_property_table_400_empty_dimension():
    res = client.post("/getPropertiesTable", json={
        "substanceId": 0,
        "modeId": "PT",
        "params": {
            "param_values": [
                128000, 300.0
            ],
            "param_dimensions": [
                "Pa", " "
            ]
        }
    }
    )

    assert res.status_code == 400
    res = res.json()
    assert res["detail"]["code"] == 11
    assert res["detail"]["error_info"] == "\"Units (' ', 1) are not of the same dimension !\""
    assert res["detail"]["msg_user_ru"] == "Единица измерения (' ') не верна, ожидается ['K', '°C', '°F']"
