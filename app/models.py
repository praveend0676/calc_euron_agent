"""Pydantic request/response models for the calculator API."""

from pydantic import BaseModel, Field


class OperationRequest(BaseModel):
    """Request body for two-operand operations."""
    a: float = Field(..., description="First operand")
    b: float = Field(..., description="Second operand")


class SingleOperandRequest(BaseModel):
    """Request body for single-operand operations."""
    value: float = Field(..., description="Operand")


class CalcResponse(BaseModel):
    """Standard response wrapping a result."""
    operation: str = Field(..., description="Name of the operation performed")
    result: float = Field(..., description="Numeric result")


class ErrorResponse(BaseModel):
    """Error response body."""
    detail: str = Field(..., description="Human-readable error message")
