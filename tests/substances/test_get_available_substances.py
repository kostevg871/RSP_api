from src.app import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_get_available_substances():
    responce = client.get("/getAvailableSubstances")
    assert responce.status_code == 200
    assert responce.json()["data"][0]["label"] == "H2O_IF97"
