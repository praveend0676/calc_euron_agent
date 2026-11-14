"""Tests for the FastAPI calculator endpoints."""

import pytest
from fastapi.testclient import TestClient
from app import calculator as calc
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def _clear_history():
    """Clear in-memory history before and after each test."""
    from app.main import _history
    _history.clear()
    yield
    _history.clear()


# -- Health check -------------------------------------------------------------


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


# -- Addition -----------------------------------------------------------------


def test_add():
    resp = client.post("/add", json={"a": 2, "b": 3})
    assert resp.status_code == 200
    data = resp.json()
    assert data["operation"] == "add"
    assert data["result"] == 5


# -- Subtraction --------------------------------------------------------------


def test_subtract():
    resp = client.post("/subtract", json={"a": 10, "b": 4})
    assert resp.status_code == 200
    assert resp.json()["result"] == 6


# -- Multiplication -----------------------------------------------------------


def test_multiply():
    resp = client.post("/multiply", json={"a": 3, "b": 7})
    assert resp.status_code == 200
    assert resp.json()["result"] == 21


# -- Division -----------------------------------------------------------------


def test_divide():
    resp = client.post("/divide", json={"a": 10, "b": 2})
    assert resp.status_code == 200
    assert resp.json()["result"] == 5


def test_divide_by_zero():
    resp = client.post("/divide", json={"a": 10, "b": 0})
    assert resp.status_code == 400
    assert "Cannot divide by zero" in resp.json()["detail"]


# -- Power --------------------------------------------------------------------


def test_power():
    resp = client.post("/power", json={"a": 2, "b": 8})
    assert resp.status_code == 200
    assert resp.json()["result"] == 256


# -- Modulus ------------------------------------------------------------------


def test_modulus():
    resp = client.post("/modulus", json={"a": 17, "b": 5})
    assert resp.status_code == 200
    assert resp.json()["result"] == 2


def test_modulus_by_zero():
    resp = client.post("/modulus", json={"a": 10, "b": 0})
    assert resp.status_code == 400
    assert "Cannot compute modulus with zero" in resp.json()["detail"]


# -- Square root --------------------------------------------------------------


def test_sqrt():
    resp = client.post("/sqrt", json={"value": 16})
    assert resp.status_code == 200
    assert resp.json()["result"] == 4


def test_sqrt_negative():
    resp = client.post("/sqrt", json={"value": -9})
    assert resp.status_code == 400
    assert "Cannot take the square root of a negative number" in resp.json()["detail"]


# -- Negate -------------------------------------------------------------------


def test_negate():
    resp = client.post("/negate", json={"value": 42})
    assert resp.status_code == 200
    assert resp.json()["result"] == -42


def test_negate_negative():
    resp = client.post("/negate", json={"value": -42})
    assert resp.status_code == 200
    assert resp.json()["result"] == 42


def test_negate_zero():
    resp = client.post("/negate", json={"value": 0})
    assert resp.status_code == 200
    assert resp.json()["result"] == 0


# -- Modulus edge cases -------------------------------------------------------


def test_modulus_floats():
    resp = client.post("/modulus", json={"a": 7.5, "b": 2.5})
    assert resp.status_code == 200
    assert resp.json()["result"] == 0.0


def test_modulus_by_one():
    resp = client.post("/modulus", json={"a": 100, "b": 1})
    assert resp.status_code == 200
    assert resp.json()["result"] == 0.0


# -- Validation ---------------------------------------------------------------


def test_missing_fields():
    resp = client.post("/add", json={"a": 2})
    assert resp.status_code == 422  # validation error


def test_wrong_content_type():
    resp = client.get("/add")
    assert resp.status_code == 405  # method not allowed


# -- Frontend -----------------------------------------------------------------


def test_frontend_home():
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Calculator" in resp.content


def test_frontend_css():
    resp = client.get("/static/style.css")
    assert resp.status_code == 200
    assert b"body" in resp.content


def test_frontend_js():
    resp = client.get("/static/app.js")
    assert resp.status_code == 200
    assert b"displayEl" in resp.content  # XSS-safe: textContent, not innerHTML


# -- POST /calculate endpoint -------------------------------------------------


def test_calculate_simple_addition():
    resp = client.post("/calculate", json={"expression": "2 + 3"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["result"] == 5
    assert data["expression"] == "2 + 3"


def test_calculate_subtraction():
    resp = client.post("/calculate", json={"expression": "10 - 4"})
    assert resp.status_code == 200
    assert resp.json()["result"] == 6


def test_calculate_multiplication():
    resp = client.post("/calculate", json={"expression": "3 * 5"})
    assert resp.status_code == 200
    assert resp.json()["result"] == 15


def test_calculate_division():
    resp = client.post("/calculate", json={"expression": "10 / 2"})
    assert resp.status_code == 200
    assert resp.json()["result"] == 5


def test_calculate_division_by_zero():
    resp = client.post("/calculate", json={"expression": "10 / 0"})
    assert resp.status_code == 400
    assert "Cannot divide by zero" in resp.json()["detail"]


def test_calculate_power():
    resp = client.post("/calculate", json={"expression": "2 ^ 8"})
    assert resp.status_code == 200
    assert resp.json()["result"] == 256


def test_calculate_modulus():
    resp = client.post("/calculate", json={"expression": "17 % 5"})
    assert resp.status_code == 200
    assert resp.json()["result"] == 2


def test_calculate_modulus_by_zero():
    resp = client.post("/calculate", json={"expression": "10 % 0"})
    assert resp.status_code == 400
    assert "Cannot compute modulus with zero" in resp.json()["detail"]


def test_calculate_sqrt():
    resp = client.post("/calculate", json={"expression": "sqrt(16)"})
    assert resp.status_code == 200
    assert resp.json()["result"] == 4


def test_calculate_sqrt_negative():
    resp = client.post("/calculate", json={"expression": "sqrt(-9)"})
    assert resp.status_code == 400
    assert "Cannot take the square root of a negative number" in resp.json()["detail"]


def test_calculate_complex_expression():
    resp = client.post("/calculate", json={"expression": "2 + 3 * 4"})
    assert resp.status_code == 200
    assert resp.json()["result"] == 14


def test_calculate_expression_with_parentheses():
    resp = client.post("/calculate", json={"expression": "(2 + 3) * 4"})
    assert resp.status_code == 200
    assert resp.json()["result"] == 20


def test_calculate_negative_numbers():
    resp = client.post("/calculate", json={"expression": "-5 + 3"})
    assert resp.status_code == 200
    assert resp.json()["result"] == -2


def test_calculate_floats():
    resp = client.post("/calculate", json={"expression": "1.5 + 2.3"})
    assert resp.status_code == 200
    assert abs(resp.json()["result"] - 3.8) < 0.001


def test_calculate_empty_expression():
    resp = client.post("/calculate", json={"expression": ""})
    assert resp.status_code == 400
    assert "Empty expression" in resp.json()["detail"]


def test_calculate_invalid_expression():
    resp = client.post("/calculate", json={"expression": "2 + * 3"})
    assert resp.status_code == 400


def test_calculate_missing_expression_field():
    resp = client.post("/calculate", json={})
    assert resp.status_code == 422  # validation error


def test_calculate_unsafe_expression():
    resp = client.post("/calculate", json={"expression": "import os"})
    assert resp.status_code == 400


# -- GET /history endpoint ----------------------------------------------------


def test_history_empty():
    resp = client.get("/history")
    assert resp.status_code == 200
    data = resp.json()
    assert "history" in data
    assert isinstance(data["history"], list)


def test_history_after_calculate():
    # First do a calculation
    client.post("/calculate", json={"expression": "5 + 3"})
    # Then check history
    resp = client.get("/history")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["history"]) >= 1
    # The last entry should be our calculation
    last_entry = data["history"][-1]
    assert last_entry["expression"] == "5 + 3"
    assert last_entry["result"] == 8


def test_history_multiple_calculations():
    client.post("/calculate", json={"expression": "1 + 1"})
    client.post("/calculate", json={"expression": "2 * 3"})
    client.post("/calculate", json={"expression": "10 - 4"})

    resp = client.get("/history")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["history"]) >= 3
    assert data["history"][-1]["expression"] == "10 - 4"
    assert data["history"][-1]["result"] == 6


def test_history_max_entries():
    # Add more than MAX_HISTORY (20) entries
    for i in range(25):
        client.post("/calculate", json={"expression": f"{i} + 1"})

    resp = client.get("/history")
    assert resp.status_code == 200
    data = resp.json()
    # Should be limited to 20 entries
    assert len(data["history"]) <= 20


def test_history_includes_failed_calculations():
    # Even failed calculations might be logged (or not, depending on implementation)
    # This test just ensures history endpoint works after errors
    client.post("/calculate", json={"expression": "10 / 0"})  # This will fail
    client.post("/calculate", json={"expression": "5 + 2"})   # This will succeed

    resp = client.get("/history")
    assert resp.status_code == 200
    data = resp.json()
    # At least the successful one should be in history
    assert any(entry["expression"] == "5 + 2" for entry in data["history"])
