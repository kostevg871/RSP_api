from app import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_get_available_substances():
    responce = client.get("/getAvailableSubstances")
    assert responce.status_code == 200
    assert responce.json() == {
        "data": [
            {
                "value": "0",
                "label": "H2O_IF97"
            },
            {
                "value": "1",
                "label": "N2"
            },
            {
                "value": "2",
                "label": "O2"
            },
            {
                "value": "3",
                "label": "C3H8"
            },
            {
                "value": "4",
                "label": "CO2"
            }
        ]
    }
