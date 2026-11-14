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


def negate(value: float) -> float:
    """Negate a number."""
    return -value


def modulus(a: float, b: float) -> float:
    """Return a modulo b. Raises ZeroDivisionError if b is zero."""
    if b == 0:
        raise ZeroDivisionError("Cannot compute modulus with zero")
    return round(a % b, 10)


def parse_and_compute(expression: str) -> float:
    """Parse a simple mathematical expression and compute its result.

    Supports +, -, *, /, ^, %, and sqrt() with parentheses.
    Uses restricted eval for safe evaluation.
    """
    expr = expression.strip()
    if not expr:
        raise ValueError("Empty expression")

    # Replace ^ with ** for power
    safe_expr = expr.replace("^", "**")

    # Gather allowed functions — use our custom divide/modulus so error
    # messages match the individual endpoints ("Cannot divide by zero" etc.)
    allowed = {
        "sqrt": square_root,
        "abs": abs,
        "float": float,
        "int": int,
        "divide": divide,
        "mod": modulus,
    }

    # Replace / and % with divide(...) and mod(...) calls so our
    # custom error messages are raised instead of Python's built-in ones.
    # We use regex to wrap operands around / and % into function calls.
    import re

    # First handle // (integer division) — treat same as /
    safe_expr = re.sub(r'//', '/DIV/', safe_expr)

    # Replace % with mod(a, b) — need to find a % b patterns
    safe_expr = re.sub(r'(\d+\.?\d*)\s*%\s*(\d+\.?\d*)', r'mod(\1, \2)', safe_expr)

    # Replace / with divide(a, b)
    safe_expr = re.sub(r'(\d+\.?\d*)\s*/\s*(\d+\.?\d*)', r'divide(\1, \2)', safe_expr)

    # Restore /DIV/ to divide for integer division
    safe_expr = safe_expr.replace('/DIV/', '/')

    try:
        result = eval(safe_expr, {"__builtins__": {}}, allowed)
    except ZeroDivisionError as e:
        # Re-raise with our standard messages
        if "modulus" in str(e) or "mod" in str(e):
            raise ZeroDivisionError("Cannot compute modulus with zero") from e
        raise ZeroDivisionError("Cannot divide by zero") from e
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}") from e

    if not isinstance(result, (int, float)):
        raise ValueError("Expression did not evaluate to a number")

    # Return int when the result is a whole number
    float_result = float(result)
    if float_result == int(float_result):
        return int(float_result)
    return float_result
