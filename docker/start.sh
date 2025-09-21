#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset
# Apply database migrations and start the server
uv run python manage.py migrate
uv run gunicorn siecom.wsgi:application --bind 0.0.0.0:8000