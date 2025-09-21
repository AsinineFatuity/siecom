#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


if [ "$LOAD_DB_DATA" != "1" ]; then
    python3 manage.py migrate
fi
uv run gunicorn siecom.wsgi:application --bind 0.0.0.0:8000