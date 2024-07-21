from app import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_get_calc_modes_info_422():
    res = client.get("/getCalcModesInfo")
    assert res.status_code == 422
    assert res.json() == {
        "detail": {
            "status_code": 422,
            "description": "Field required",
            "msg": "Не правильно введены данные!"

        }}


def test_get_calc_modes_info_id_1_200():
    res = client.get("/getCalcModesInfo?id=1")
    assert res.status_code == 200
    assert res.json() == {
        "data": [
            {
                "value": "DT",
                "filter_params": [
                    "Density",
                    "Temperature"
                ],
                "param_literals": [
                    "D",
                    "T"
                ],
                "param_dimensions": [
                    "kg*m^-3",
                    "K"
                ],
                "available_param_dimension": [
                    [
                        "kg*m^-3"
                    ],
                    [
                        "K",
                        "°C",
                        "°F"
                    ]
                ]
            },
            {
                "value": "HS",
                "filter_params": [
                    "Enthalpy",
                    "Enthropy"
                ],
                "param_literals": [
                    "H",
                    "S"
                ],
                "param_dimensions": [
                    "J*kg^-1",
                    "J*kg^-1*K^-1"
                ],
                "available_param_dimension": [
                    [
                        "J*kg^-1",
                        "kJ*kg^-1",
                        "MJ*kg^-1"
                    ],
                    [
                        "J*kg^-1*K^-1",
                        "kJ*kg^-1*K^-1",
                        "MJ*kg^-1*K^-1"
                    ]
                ]
            },
            {
                "value": "P",
                "filter_params": [
                    "Saturation pressure"
                ],
                "param_literals": [
                    "PS"
                ],
                "param_dimensions": [
                    "Pa"
                ],
                "available_param_dimension": [
                    [
                        "Pa",
                        "kPa",
                        "MPa",
                        "bar"
                    ]
                ]
            },
            {
                "value": "PH",
                "filter_params": [
                    "Pressure",
                    "Enthalpy"
                ],
                "param_literals": [
                    "P",
                    "H"
                ],
                "param_dimensions": [
                    "Pa",
                    "J*kg^-1"
                ],
                "available_param_dimension": [
                    [
                        "Pa",
                        "kPa",
                        "MPa",
                        "bar"
                    ],
                    [
                        "J*kg^-1",
                        "kJ*kg^-1",
                        "MJ*kg^-1"
                    ]
                ]
            },
            {
                "value": "PS",
                "filter_params": [
                    "Pressure",
                    "Enthropy"
                ],
                "param_literals": [
                    "P",
                    "S"
                ],
                "param_dimensions": [
                    "Pa",
                    "J*kg^-1*K^-1"
                ],
                "available_param_dimension": [
                    [
                        "Pa",
                        "kPa",
                        "MPa",
                        "bar"
                    ],
                    [
                        "J*kg^-1*K^-1",
                        "kJ*kg^-1*K^-1",
                        "MJ*kg^-1*K^-1"
                    ]
                ]
            },
            {
                "value": "PT",
                "filter_params": [
                    "Pressure",
                    "Temperature"
                ],
                "param_literals": [
                    "P",
                    "T"
                ],
                "param_dimensions": [
                    "Pa",
                    "K"
                ],
                "available_param_dimension": [
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
                ]
            },
            {
                "value": "T",
                "filter_params": [
                    "Saturation temperature"
                ],
                "param_literals": [
                    "TS"
                ],
                "param_dimensions": [
                    "K"
                ],
                "available_param_dimension": [
                    [
                        "K",
                        "°C",
                        "°F"
                    ]
                ]
            },
            {
                "value": "TX",
                "filter_params": [
                    "Saturation temperature",
                    "Steam mass fraction"
                ],
                "param_literals": [
                    "TS",
                    "X"
                ],
                "param_dimensions": [
                    "K",
                    ""
                ],
                "available_param_dimension": [
                    [
                        "K",
                        "°C",
                        "°F"
                    ],
                    [
                        ""
                    ]
                ]
            }
        ]
    }


def test_get_calc_modes_info_id_0_200():
    res = client.get("/getCalcModesInfo?id=0")
    assert res.status_code == 200
    assert res.json() == {
        "data": [
            {
                "data": [
                    {
                        "value": "HS",
                        "filter_params": [
                            "Enthalpy",
                            "Enthropy"
                        ],
                        "param_literals": [
                            "H",
                            "S"
                        ],
                        "param_dimensions": [
                            "J*kg^-1",
                            "J*kg^-1*K^-1"
                        ],
                        "available_param_dimension": [
                            [
                                "J*kg^-1",
                                "kJ*kg^-1",
                                "MJ*kg^-1"
                            ],
                            [
                                "J*kg^-1*K^-1",
                                "kJ*kg^-1*K^-1",
                                "MJ*kg^-1*K^-1"
                            ]
                        ]
                    },
                    {
                        "value": "P",
                        "filter_params": [
                            "Saturation pressure"
                        ],
                        "param_literals": [
                            "PS"
                        ],
                        "param_dimensions": [
                            "Pa"
                        ],
                        "available_param_dimension": [
                            [
                                "Pa",
                                "kPa",
                                "MPa",
                                "bar"
                            ]
                        ]
                    },
                    {
                        "value": "PH",
                        "filter_params": [
                            "Pressure",
                            "Enthalpy"
                        ],
                        "param_literals": [
                            "P",
                            "H"
                        ],
                        "param_dimensions": [
                            "Pa",
                            "J*kg^-1"
                        ],
                        "available_param_dimension": [
                            [
                                "Pa",
                                "kPa",
                                "MPa",
                                "bar"
                            ],
                            [
                                "J*kg^-1",
                                "kJ*kg^-1",
                                "MJ*kg^-1"
                            ]
                        ]
                    },
                    {
                        "value": "PS",
                        "filter_params": [
                            "Pressure",
                            "Enthropy"
                        ],
                        "param_literals": [
                            "P",
                            "S"
                        ],
                        "param_dimensions": [
                            "Pa",
                            "J*kg^-1*K^-1"
                        ],
                        "available_param_dimension": [
                            [
                                "Pa",
                                "kPa",
                                "MPa",
                                "bar"
                            ],
                            [
                                "J*kg^-1*K^-1",
                                "kJ*kg^-1*K^-1",
                                "MJ*kg^-1*K^-1"
                            ]
                        ]
                    },
                    {
                        "value": "PT",
                        "filter_params": [
                            "Pressure",
                            "Temperature"
                        ],
                        "param_literals": [
                            "P",
                            "T"
                        ],
                        "param_dimensions": [
                            "Pa",
                            "K"
                        ],
                        "available_param_dimension": [
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
                        ]
                    },
                    {
                        "value": "T",
                        "filter_params": [
                            "Saturation temperature"
                        ],
                        "param_literals": [
                            "TS"
                        ],
                        "param_dimensions": [
                            "K"
                        ],
                        "available_param_dimension": [
                            [
                                "K",
                                "°C",
                                "°F"
                            ]
                        ]
                    },
                    {
                        "value": "TX",
                        "filter_params": [
                            "Saturation temperature",
                            "Steam mass fraction"
                        ],
                        "param_literals": [
                            "TS",
                            "X"
                        ],
                        "param_dimensions": [
                            "K",
                            ""
                        ],
                        "available_param_dimension": [
                            [
                                "K",
                                "°C",
                                "°F"
                            ],
                            [
                                ""
                            ]
                        ]
                    }
                ]
            }
        ]
    }


def test_get_calc_modes_info_id_bad_request():
    id = 6
    res = client.get("/getCalcModesInfo?id={id}".format(id=id))
    assert res.status_code == 400
    assert res.json() == {
        "detail": {
            "code": 1,
            "type": "SubstanceNotFound",
            "error_info": "Неправильно указано вещество",
            "msg_user_ru": "substanceId={id} должно быть в промежутке от 0 до 4".format(id=id),
            "msg_user_en": "substanceId={id} be in the range from 0 to 4".format(id=id),
            "request_info": None
        }
    }
