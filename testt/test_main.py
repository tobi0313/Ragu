import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# --- Add and Subtract ---

@pytest.mark.parametrize("a,b,expected", [
    (3, 5, 8),
    (-2, 7, 5),
    (0, 0, 0),
    (1.5, 2.5, 4.0),
])
def test_add(a, b, expected):
    response = client.get("/add", params={"a": a, "b": b})
    assert response.status_code == 200
    assert response.json() == {"result": expected}


@pytest.mark.parametrize("a,b,expected", [
    (10, 4, 6),
    (-2, -3, 1),
    (0, 5, -5),
    (2.5, 1.5, 1.0),
])
def test_subtract(a, b, expected):
    response = client.get("/subtract", params={"a": a, "b": b})
    assert response.status_code == 200
    assert response.json() == {"result": expected}


# --- Multiply ---

@pytest.mark.parametrize("a,b,expected", [
    (6, 7, 42),
    (0, 10, 0),
    (-3, 3, -9),
    (1.5, 2, 3.0),
])
def test_multiply(a, b, expected):
    response = client.get("/multiply", params={"a": a, "b": b})
    assert response.status_code == 200
    assert response.json() == {"result": expected}


# --- Divide ---

@pytest.mark.parametrize("a,b,expected", [
    (20, 5, 4),
    (7, -1, -7),
    (1.5, 0.5, 3.0),
])
def test_divide(a, b, expected):
    response = client.get("/divide", params={"a": a, "b": b})
    assert response.status_code == 200
    assert response.json() == {"result": expected}


@pytest.mark.parametrize("a,b", [
    (10, 0),
    (-5, 0),
])
def test_divide_by_zero(a, b):
    response = client.get("/divide", params={"a": a, "b": b})
    assert response.status_code == 200
    assert response.json() == {"error": "Cannot divide by zero"}


# --- Power ---

@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 8),
    (5, 0, 1),
    (-2, 2, 4),
    (2, 0.5, 2 ** 0.5),
])
def test_power(a, b, expected):
    response = client.get("/power", params={"a": a, "b": b})
    assert response.status_code == 200
    assert response.json() == {"result": expected}


# --- Modulo ---

@pytest.mark.parametrize("a,b,expected", [
    (10, 3, 1),
    (5, 2, 1),
    (-5, 3, 1),  
])
def test_modulo(a, b, expected):
    response = client.get("/modulo", params={"a": a, "b": b})
    assert response.status_code == 200
    assert response.json() == {"result": expected}


@pytest.mark.parametrize("a,b", [
    (10, 0),
    (-3, 0),
])
def test_modulo_by_zero(a, b):
    response = client.get("/modulo", params={"a": a, "b": b})
    assert response.status_code == 200
    assert response.json() == {"error": "Cannot modulo by zero"}


# --- Average ---

@pytest.mark.parametrize("a,b,expected", [
    (10, 20, 15),
    (-10, 10, 0),
    (0, 0, 0),
    (1.5, 2.5, 2.0),
])
def test_average(a, b, expected):
    response = client.get("/average", params={"a": a, "b": b})
    assert response.status_code == 200
    assert response.json() == {"result": expected}