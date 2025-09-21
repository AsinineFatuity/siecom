# Use slim image for smaller size
FROM python:3.13-slim AS base

# Set environment variables (Python runs in "production mode")
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Install system deps first (needed for psycopg2, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Install uv globally
RUN pip install --no-cache-dir uv

# Copy lockfile first to leverage caching
COPY uv.lock pyproject.toml ./

# Sync dependencies into .venv
RUN uv sync --frozen --no-cache

# Copy rest of project
COPY . .

# Avoid path issues with entrypoint script
COPY ./docker/*.sh /

# Fix Line endings and permissions for shell scripts
RUN sed -i 's/\r$//g' /*.sh && \
    chmod +x /*.sh

# Expose port 8000 for the Django app
EXPOSE 8000

# Set the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]