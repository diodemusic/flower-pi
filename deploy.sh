#!/bin/bash
set -e

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "Deploying to $PI_USER@$PI_HOST at $REMOTE_DIR"
rsync -avz --delete ./ "$PI_USER@$PI_HOST:$REMOTE_DIR/"

echo "Deployment complete!"
