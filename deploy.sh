#!/bin/bash

set -e

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "Deploying to $PI_USER@$PI_HOST at $REMOTE_DIR"

rsync -avz --delete ./ $PI_USER@$PI_HOST:$REMOTE_DIR

ssh $PI_USER@$PI_HOST << 'ENDSSH'
cd ~/flower-pi
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install fastapi[standard]
sudo chmod u+x start.sh

echo "Deployment complete"
