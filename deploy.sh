#!/bin/bash
set -e

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "Deploying to $PI_USER@$PI_HOST at $REMOTE_DIR"
rsync -avz --delete --exclude='.venv' --exclude='.vscode' ./ "$PI_USER@$PI_HOST:$REMOTE_DIR/"

ssh "$PI_USER@$PI_HOST" << ENDSSH

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
