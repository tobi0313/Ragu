from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_divide():
    response = client.get("/divide?a=10&b=2")
    assert response.status_code == 200
    assert response.json()["result"] == 5


def test_login():
    response = client.get("/login?username=test")
    assert response.status_code == 200
    assert response.json()["user"] is not None


def test_calc():
    response = client.get("/calc", params={"expr": "1+1"})
    assert response.status_code == 200
    assert response.json()["result"] == 2
