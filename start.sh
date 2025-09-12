#!/bin/bash

echo "Starting API server"
source .venv/bin/activate
export PYTHONPATH=$(pwd)
fastapi dev src/main.py --host 0.0.0.0 --port 8000 --reload
