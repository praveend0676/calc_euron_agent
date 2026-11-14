"""Calculator math logic – pure functions, no side-effects."""


def add(a: float, b: float) -> float:
    """Add two numbers."""
    return round(a + b, 10)


def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return round(a - b, 10)


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return round(a * b, 10)


def divide(a: float, b: float) -> float:
    """Divide a by b. Raises ZeroDivisionError if b is zero."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return round(a / b, 10)


def power(base: float, exp: float) -> float:
    """Raise base to the power of exp."""
    return round(base ** exp, 10)


def square_root(value: float) -> float:
    """Return the square root of value. Raises ValueError if negative."""
    if value < 0:
        raise ValueError("Cannot take the square root of a negative number")
    return round(value ** 0.5, 10)


def modulus(a: float, b: float) -> float:
    """Return a modulo b. Raises ZeroDivisionError if b is zero."""
    if b == 0:
        raise ZeroDivisionError("Cannot compute modulus with zero")
    return round(a % b, 10)
