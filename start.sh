#!/bin/bash

echo "Starting API server"
export PYTHONPATH=$(pwd)
fastapi dev src/main.py
