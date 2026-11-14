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

---

## Prompt Comparison

| Prompt instruction | How this project implements it |
|---|---|
| "Use FastAPI with Uvicorn" | `app/main.py` creates a `FastAPI()` app; `uvicorn` is listed in `requirements.txt` |
| "Provide `/health` endpoint" | `GET /health` returns `{"status": "ok"}` |
| "Provide `/calculate` and `/history` endpoints" | `POST /calculate` and `GET /history` in `app/main.py` |
| "Use restricted eval for expressions" | `app/calculator.py` uses `safe_eval()` with `__builtins__={}` |
| "Max 20 history entries" | `MAX_HISTORY = 20` in `app/main.py`; older entries are dropped |
| "Serve frontend at `/`" | `serve_frontend()` mounted at `/` in `app/main.py` |
| "Use Docker with multi-stage build" | `Dockerfile` uses builder + runtime stages |

## Reviewed Correction

During development the following corrections were applied after review:

1. **Docker `pip install --user`** — originally installed packages under `/root/.local` which was inaccessible to the non-root runtime user. Fixed with `ENV PIP_USER=false` and installing into the system site-packages.
2. **`app.js` used local `eval()`** — the frontend originally computed results in-browser. Changed to `fetch('/calculate')` so all arithmetic runs server-side.
3. **Missing `/history` in `app.js`** — history was only stored locally. Added `loadHistory()` to fetch from `GET /history` on page load.
4. **`_add_to_history` ordering** — switched from `insert(0) + pop()` to `append() + pop(0)` so the newest entry is at index `-1`, matching test expectations.

## Allowance Usage

| Component | Lines of code |
|---|---|
| `app/main.py` | ~160 |
| `app/calculator.py` | ~120 |
| `app/models.py` | ~40 |
| `static/app.js` | ~280 |
| `static/index.html` | ~200 |
| `static/style.css` | ~300 |
| `tests/test_api.py` | ~350 |
| `tests/test_calculator.py` | ~300 |
| `Dockerfile` | ~25 |
| `requirements.txt` | ~10 |
| **Total** | **~1725** |

The project was built within the token allowance for a single AI coding session.
