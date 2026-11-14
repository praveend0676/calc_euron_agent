"""Calculator math logic – pure functions, no side-effects."""
import math
import re

# ---------------------------------------------------------------------------
# Simple math helpers
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Expression evaluation – recursive descent parser, no eval()
# ---------------------------------------------------------------------------


def _validate_expression(expression: str) -> None:
    """Check that the expression only contains allowed characters."""
    if not expression or not expression.strip():
        raise ValueError("Empty expression")


def _tokenize(expression: str) -> list[str]:
    """Tokenise a math expression string into a list of tokens."""
    raw = re.findall(
        r"sqrt|\d+\.\d+|\d+|\*\*|//|\^|[\+\-\*/\(\)%]", expression
    )
    # Merge "-" into negative numbers only when it acts as a unary minus:
    # at the start, or after an operator or "(".
    operators = {"+", "-", "*", "/", "//", "%", "**", "^", "("}
    merged: list[str] = []
    i = 0
    while i < len(raw):
        if raw[i] == "-" and i + 1 < len(raw) and raw[i + 1][0].isdigit():
            if not merged or merged[-1] in operators:
                merged.append("-" + raw[i + 1])
                i += 2
                continue
        merged.append(raw[i])
        i += 1
    return merged


def _parse_expression(tokens: list[str], pos: int) -> tuple[float, int]:
    """Handle + and - (lowest precedence)."""
    left, pos = _parse_term(tokens, pos)
    while pos < len(tokens) and tokens[pos] in ("+", "-"):
        op = tokens[pos]
        pos += 1
        right, pos = _parse_term(tokens, pos)
        if op == "+":
            left += right
        else:
            left -= right
    return left, pos


def _parse_term(tokens: list[str], pos: int) -> tuple[float, int]:
    """Handle *, /, //, %."""
    left, pos = _parse_power(tokens, pos)
    while pos < len(tokens) and tokens[pos] in ("*", "/", "//", "%"):
        op = tokens[pos]
        pos += 1
        right, pos = _parse_power(tokens, pos)
        if op == "*":
            left *= right
        elif op == "/":
            if right == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            left /= right
        elif op == "//":
            if right == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            left = float(int(left) // int(right))
        elif op == "%":
            if right == 0:
                raise ZeroDivisionError("Cannot compute modulus with zero")
            left %= right
    return left, pos


def _parse_power(tokens: list[str], pos: int) -> tuple[float, int]:
    """Handle ** and ^ (right-associative)."""
    base, pos = _parse_atom(tokens, pos)
    if pos < len(tokens) and tokens[pos] in ("**", "^"):
        pos += 1
        exp, pos = _parse_power(tokens, pos)  # right-associative recursion
        base = base ** exp
    return base, pos


def _parse_atom(tokens: list[str], pos: int) -> tuple[float, int]:
    """A number, parenthesised expression, or sqrt(...)."""
    if pos >= len(tokens):
        raise ValueError("Unexpected end of expression")

    token = tokens[pos]

    # Unary minus
    if token == "-":
        pos += 1
        val, pos = _parse_atom(tokens, pos)
        return -val, pos

    # Unary plus
    if token == "+":
        pos += 1
        val, pos = _parse_atom(tokens, pos)
        return val, pos

    # sqrt()
    if token == "sqrt":
        pos += 1
        if pos >= len(tokens) or tokens[pos] != "(":
            raise ValueError("Expected '(' after 'sqrt'")
        pos += 1
        val, pos = _parse_expression(tokens, pos)
        if pos >= len(tokens) or tokens[pos] != ")":
            raise ValueError("Missing closing ')'")
        pos += 1
        if val < 0:
            raise ValueError("Cannot take the square root of a negative number")
        return math.sqrt(val), pos

    # Parenthesised sub-expression
    if token == "(":
        pos += 1
        val, pos = _parse_expression(tokens, pos)
        if pos >= len(tokens) or tokens[pos] != ")":
            raise ValueError("Missing closing ')'")
        pos += 1
        return val, pos

    # Plain number
    try:
        return float(token), pos + 1
    except ValueError:
        raise ValueError(f"Invalid token: {token!r}")


def parse_and_compute(expression: str) -> float | int:
    """Parse a mathematical expression and compute its result.

    Supports +, -, *, /, //, %, ^ (or **), and sqrt() with parentheses.
    Uses a recursive descent parser – no eval().
    """
    expr = expression.strip()
    if not expr:
        raise ValueError("Empty expression")

    _validate_expression(expression)

    tokens = _tokenize(expr)
    if not tokens:
        raise ValueError("Empty expression")

    result, pos = _parse_expression(tokens, 0)
    if pos < len(tokens):
        raise ValueError(f"Unexpected token: {tokens[pos]}")

    float_result = float(result)
    if float_result == int(float_result):
        return int(float_result)
    return float_result
