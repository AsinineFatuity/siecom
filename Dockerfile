FROM python:3.13-slim-bookworm AS builder
COPY --from=ghcr.io/astral-sh/uv:0.8.13 /uv /uvx /bin/

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

COPY uv.lock pyproject.toml ./
RUN uv sync --frozen --no-cache --python=/usr/local/bin/python

COPY . .

# --- final image ---
FROM python:3.13-slim AS runtime

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app /app
COPY ./docker/*.sh /
RUN sed -i 's/\r$//g' /*.sh && chmod +x /*.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]