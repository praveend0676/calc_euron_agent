# Calculator Application

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-40%20passing-brightgreen)](tests/)

A full-stack calculator application built with **FastAPI** (backend), **Docker** (containerization), and **vanilla HTML/CSS/JS** (frontend).

---

## Features

- **REST API** with calculator operations: add, subtract, multiply, divide, power, square root, modulus
- **Web frontend** with a clean dark-theme calculator UI
- **Keyboard support** for desktop use
- **Docker support** — run the entire app in a single container
- **40 passing tests** — unit tests for math logic, integration tests for API and frontend

---

## Quick Start

### Local (without Docker)

```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open `http://localhost:8000` in your browser.

### With Docker

```powershell
docker build -t calculator-api .
docker run -d --name calculator -p 8000:8000 calculator-api
```

Then open `http://localhost:8000` in your browser.

### Run Tests

```powershell
pip install pytest httpx
python -m pytest tests/ -v
```

---

## Project Structure

```
calculator/
├── app/
│   ├── __init__.py
│   ├── calculator.py      # Pure math functions
│   ├── main.py             # FastAPI app & routes
│   └── models.py           # Pydantic request/response models
├── static/
│   ├── index.html          # Frontend HTML
│   ├── style.css           # Frontend CSS (dark theme)
│   └── app.js              # Frontend JavaScript
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py  # Unit tests for math functions (25 tests)
│   └── test_api.py         # Integration tests for API & frontend (15 tests)
├── Dockerfile              # Docker image definition
├── .dockerignore           # Docker build exclusions
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── EVALUATION.md           # Euron Code Agent evaluation report
```

---

## API Endpoints

All POST endpoints accept JSON bodies. The API auto-generates OpenAPI docs at `http://localhost:8000/docs`.

| Endpoint | Method | Body | Description |
|---|---|---|---|
| `/health` | `GET` | — | Health check (`{"status":"ok"}`) |
| `/add` | `POST` | `{"a": float, "b": float}` | a + b |
| `/subtract` | `POST` | `{"a": float, "b": float}` | a - b |
| `/multiply` | `POST` | `{"a": float, "b": float}` | a × b |
| `/divide` | `POST` | `{"a": float, "b": float}` | a ÷ b |
| `/power` | `POST` | `{"a": float, "b": float}` | a ^ b |
| `/sqrt` | `POST` | `{"value": float}` | √value |
| `/modulus` | `POST` | `{"a": float, "b": float}` | a % b |

### Example Requests

```bash
# Add
curl -X POST http://localhost:8000/add \
     -H "Content-Type: application/json" \
     -d '{"a": 10, "b": 5}'
# → {"operation":"add","result":15.0}

# Divide (error case)
curl -X POST http://localhost:8000/divide \
     -H "Content-Type: application/json" \
     -d '{"a": 10, "b": 0}'
# → {"error":"Division by zero is not allowed"} (HTTP 400)

# Square root (error case)
curl -X POST http://localhost:8000/sqrt \
     -H "Content-Type: application/json" \
     -d '{"value": -4}'
# → {"error":"Cannot compute square root of a negative number"} (HTTP 400)
```

---

## Frontend

The frontend is a single-page app served from `http://localhost:8000` that calls the API endpoints via `fetch()`.

**Keyboard shortcuts:**
| Key | Action |
|---|---|
| `0`–`9` | Digit input |
| `.` | Decimal point |
| `+` `-` `*` `/` `^` `%` | Two-operand operation |
| `s` | Square root |
| `c` | Clear |
| `Escape` | Clear |
| `Enter` | Clear |

---

## Testing

```
tests/
├── test_calculator.py   # 25 unit tests for pure math functions
├── test_api.py          # 15 integration tests (API + frontend serving)
```

Run the full suite:

```powershell
python -m pytest tests/ -v
```

Expected output: **40 passed**

---

## Docker

```powershell
# Build
docker build -t calculator-api .

# Run
docker run -d --name calculator -p 8000:8000 calculator-api

# Test health check
curl http://localhost:8000/health

# Stop & clean up
docker stop calculator
docker rm calculator
```

---

## Evaluation

See [EVALUATION.md](EVALUATION.md) for a full analysis of the AI-assisted development workflow, including what went well, issues encountered, and lessons learned.
