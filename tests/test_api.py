"""Tests for the FastAPI calculator endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


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
    assert b"API_BASE" in resp.content
