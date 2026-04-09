FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN python -m pip install --no-cache-dir "uv==0.11.3"

COPY pyproject.toml uv.lock README.md ./
COPY src/ src/

RUN uv sync --frozen --no-dev

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NEWSDOM_MINERU_BIN=mineru \
    PATH="/app/.venv/bin:${PATH}"

WORKDIR /app

RUN useradd --create-home --home-dir /home/newsdom --shell /usr/sbin/nologin newsdom

COPY --from=builder /app /app

RUN chown -R newsdom:newsdom /app

USER newsdom

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=5 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health').read()"

CMD ["uvicorn", "newsdom_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
