#!/bin/bash

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "Starting API server"
export PYTHONPATH=$(pwd)
fastapi dev src/main.py --host $FASTAPI_HOST
