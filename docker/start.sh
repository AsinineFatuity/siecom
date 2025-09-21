#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset
# Apply database migrations and start the server
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn siecom.wsgi:application --bind 0.0.0.0:8000 --reload