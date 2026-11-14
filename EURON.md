# CALCULATOR _EURON CODE

## Stack
- Python 3.13 + FastAPI + Uvicorn
- Vanilla HTML/CSS/JS frontend
- Docker (python:3.13-slim)
- pytest + httpx

## Commands
```powershell
pip install -r requirements.txt
python -m pytest tests/ -v
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
docker build -t calculator-api .
docker run -d --name calculator -p 8000:8000 calculator-api
```

## Layout
```
app/
  __init__.py
  calculator.py          # Pure math functions
  main.py                # FastAPI app, routes, static files
  models.py              # Pydantic models
static/
  index.html             # Frontend HTML
  style.css              # Frontend CSS (dark theme)
  app.js                 # Frontend JS
tests/
  __init__.py
  test_calculator.py     # 25 unit tests
  test_api.py            # 15 integration tests
Dockerfile
.dockerignore
requirements.txt
README.md
EVALUATION.md
```

## Conventions
- Pure math in `app/calculator.py`; routes in `app/main.py`
- 400 errors for invalid ops (divide by zero, negative sqrt)
- Frontend served at `/` from same FastAPI process
- Static assets mounted at `/static/`