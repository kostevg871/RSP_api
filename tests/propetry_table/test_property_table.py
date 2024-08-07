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
                "dimension": "",
                "propertyId": "JOULETHOMPSON",
                "value": "-2.20242891312057205288266127814200689982726544258184731006622314453125E-7",
                "available_dimensions": [
                    ""
                ]
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
                "dimension": "",
                "propertyId": "K",
                "value": "22221.7957777002520742826163768768310546875",
                "available_dimensions": [
                    ""
                ]
            },
            {
                "dimension": "",
                "propertyId": "PRANDTLE",
                "value": "5.85655774372549142725574711221270263195037841796875",
                "available_dimensions": [
                    ""
                ]
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
                "dimension": "Wt*m^-1",
                "propertyId": "THERMCOND",
                "value": "0.6095012841120712732134734324063174426555633544921875",
                "available_dimensions": [
                    "Wt*m^-1",
                    "kWt*m^-1",
                    "MWt*m^-1"
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
