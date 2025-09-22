#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

echo "Waiting for PostgreSQL to become available..."

while ! (echo > /dev/tcp/$POSTGRES_HOST/$POSTGRES_PORT) >/dev/null 2>&1; do
  sleep 0.1
done

echo "PostgreSQL is now available to execute your queries and instructions..."
exec "$@"