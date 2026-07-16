#!/bin/bash
# Entrypoint for Minimax Worker

set -e

echo "Starting Minimax Worker..."

# Wait for Agent Brain
if [ -n "$AGENT_BRAIN_URL" ]; then
    echo "Waiting for Agent Brain at $AGENT_BRAIN_URL..."
    until curl -sf "$AGENT_BRAIN_URL/health" > /dev/null; do
        sleep 2
    done
    echo "Agent Brain is ready!"
fi

# Set up project key
export PROJECT_KEY="${PROJECT_KEY:-}"

# Add Python path
export PYTHONPATH="/workspace/tools/python:$PYTHONPATH"

# Create output directories
mkdir -p /workspace/assets/video/generated
mkdir -p /workspace/assets/audio/generated

# Keep container running or run the worker
exec "$@"