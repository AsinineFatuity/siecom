#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Run connect to db script 
/connect_to_db.sh 

exec "$@"