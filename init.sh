#!/bin/bash

VENV_DIR=".venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created in $VENV_DIR"
else
    echo "Virtual environment already exists in $VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
echo "Virtual environment activated"

echo "Installing dependencies"
pip install -r requirements.txt

echo "Installing fastapi"
pip install fastapi[standard]
