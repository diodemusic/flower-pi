#!/bin/bash
set -e

# Load .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "Deploying to $PI_USER@$PI_HOST at $REMOTE_DIR"

ssh "$PI_USER@$PI_HOST" << ENDSSH

rm -rf $REMOTE_DIR

git clone $GIT_REPO

cd $REMOTE_DIR

# Create venv if missing
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source $VENV_DIR/bin/activate

pip install -r requirements.txt
pip install fastapi[standard]

chmod u+x start.sh

echo "Deployment complete!"
ENDSSH
