"""Tests for the calculator math module (pure functions)."""

import pytest
from app.calculator import add, subtract, multiply, divide, power, square_root, modulus


# -- Addition -----------------------------------------------------------------


def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-1, -1) == -2


def test_add_zero():
    assert add(0, 0) == 0


def test_add_floats():
    assert add(0.1, 0.2) == pytest.approx(0.3)


# -- Subtraction --------------------------------------------------------------


def test_subtract_positive():
    assert subtract(5, 3) == 2


def test_subtract_negative():
    assert subtract(-1, -3) == 2


def test_subtract_zero():
    assert subtract(0, 0) == 0


# -- Multiplication -----------------------------------------------------------


def test_multiply_positive():
    assert multiply(3, 4) == 12


def test_multiply_by_zero():
    assert multiply(5, 0) == 0


def test_multiply_negative():
    assert multiply(-2, 3) == -6


def test_multiply_floats():
    assert multiply(1.5, 2.0) == pytest.approx(3.0)


# -- Division -----------------------------------------------------------------


def test_divide_positive():
    assert divide(10, 2) == 5


def test_divide_floats():
    assert divide(7, 2) == pytest.approx(3.5)


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(10, 0)


def test_divide_negative():
    assert divide(-6, 2) == -3


# -- Power --------------------------------------------------------------------


def test_power_positive():
    assert power(2, 3) == 8


def test_power_zero_exponent():
    assert power(5, 0) == 1


def test_power_negative_exponent():
    assert power(2, -1) == pytest.approx(0.5)


# -- Square root --------------------------------------------------------------


def test_sqrt_positive():
    assert square_root(9) == 3


def test_sqrt_float():
    assert square_root(2) == pytest.approx(1.4142135623730951)


def test_sqrt_zero():
    assert square_root(0) == 0


def test_sqrt_negative():
    with pytest.raises(ValueError, match="Cannot take the square root of a negative number"):
        square_root(-4)


# -- Modulus ------------------------------------------------------------------


def test_modulus_basic():
    assert modulus(10, 3) == 1


def test_modulus_zero_divisor():
    with pytest.raises(ZeroDivisionError, match="Cannot compute modulus with zero"):
        modulus(10, 0)
