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


class CalculateRequest(BaseModel):
    """Request body for the unified calculate endpoint."""
    expression: str = Field(..., description="Mathematical expression string")


class CalculateResponse(BaseModel):
    """Response for the unified calculate endpoint."""
    expression: str = Field(..., description="Original expression sent by the client")
    result: int | float = Field(..., description="Computed numeric result")


class HistoryEntry(BaseModel):
    """A single history entry."""
    expression: str
    result: int | float
    timestamp: str


class HistoryResponse(BaseModel):
    """List of history entries."""
    history: list[HistoryEntry]
