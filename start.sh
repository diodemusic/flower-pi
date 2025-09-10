#!/bin/bash

echo "Activating virtual environment"
source .venv/bin/activate

echo "Starting API server"
export PYTHONPATH=$(pwd)
fastapi dev src/main.py
