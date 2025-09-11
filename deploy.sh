#!/bin/bash
set -e

# Load .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "Deploying to $PI_USER@$PI_HOST at $REMOTE_DIR"

rsync -avz --delete ./ "$PI_USER@$PI_HOST:$REMOTE_DIR"

ssh "$PI_USER@$PI_HOST" << ENDSSH
cd "$REMOTE_DIR"

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install fastapi[standard]

# Make start.sh executable
sudo chmod u+x start.sh

echo "Deployment complete!"
ENDSSH
