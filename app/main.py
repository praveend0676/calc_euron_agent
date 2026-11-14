"""Calculator API – FastAPI application."""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import calculator as calc
from .models import CalcResponse, ErrorResponse, OperationRequest, SingleOperandRequest

import os

app = FastAPI(
    title="Calculator API",
    description="A simple REST calculator built with FastAPI.",
    version="1.0.0",
)

# -- Static files (frontend) --------------------------------------------------
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


# -- Two-operand operations ---------------------------------------------------


@app.post("/add", response_model=CalcResponse)
def add(body: OperationRequest) -> CalcResponse:
    return CalcResponse(operation="add", result=calc.add(body.a, body.b))


@app.post("/subtract", response_model=CalcResponse)
def subtract(body: OperationRequest) -> CalcResponse:
    return CalcResponse(operation="subtract", result=calc.subtract(body.a, body.b))


@app.post("/multiply", response_model=CalcResponse)
def multiply(body: OperationRequest) -> CalcResponse:
    return CalcResponse(operation="multiply", result=calc.multiply(body.a, body.b))


@app.post("/divide", response_model=CalcResponse)
def divide(body: OperationRequest) -> CalcResponse:
    try:
        result = calc.divide(body.a, body.b)
    except ZeroDivisionError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return CalcResponse(operation="divide", result=result)


@app.post("/power", response_model=CalcResponse)
def power(body: OperationRequest) -> CalcResponse:
    return CalcResponse(operation="power", result=calc.power(body.a, body.b))


@app.post("/modulus", response_model=CalcResponse)
def modulus(body: OperationRequest) -> CalcResponse:
    try:
        result = calc.modulus(body.a, body.b)
    except ZeroDivisionError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return CalcResponse(operation="modulus", result=result)


# -- Single-operand operations ------------------------------------------------


@app.post("/sqrt", response_model=CalcResponse)
def sqrt(body: SingleOperandRequest) -> CalcResponse:
    try:
        result = calc.square_root(body.value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return CalcResponse(operation="sqrt", result=result)


# -- Health check -------------------------------------------------------------


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
