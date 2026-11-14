FROM python:3.13-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# --- runtime ---

FROM python:3.13-slim AS runtime

ARG BUILD_DATE
ARG BUILD_REF

LABEL org.opencontainers.image.title="Calculator API"
LABEL org.opencontainers.image.description="A calculator API with FastAPI and a dark-theme frontend"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.created=$BUILD_DATE
LABEL org.opencontainers.image.revision=$BUILD_REF
LABEL org.opencontainers.image.licenses="MIT"

RUN groupadd -r calculator && useradd --no-log-init -r -g calculator calculator

EXPOSE 8000

WORKDIR /app

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY . .

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

USER calculator

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]