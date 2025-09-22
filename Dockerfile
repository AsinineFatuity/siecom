# snippets and rationale from https://gist.github.com/adamghill/419d02e95b1563ad76b0c36995e829b8
FROM python:3.13-slim-bookworm AS base

FROM base AS builder
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    VIRTUAL_ENV=/opt/venv

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update --fix-missing && \
    apt-get install --no-install-recommends -y \
    build-essential\
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY ./pyproject.toml .

RUN --mount=type=cache,target=/root/.cache/pip --mount=type=cache,target=/root/.cache/uv \
    python -m pip config --user set global.progress_bar off && \
    python -m pip install --upgrade pip uv && \
    uv venv /opt/venv && \
    uv pip install --requirement pyproject.toml

# --- final image ---
FROM base

COPY . /app
COPY --from=builder /opt/venv /opt/venv
 
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
 && rm -rf /var/lib/apt/lists/*


COPY ./docker/*.sh /
RUN sed -i 's/\r$//g' /*.sh && chmod +x /*.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]