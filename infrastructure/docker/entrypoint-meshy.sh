#!/bin/bash
# Entrypoint for Meshy Worker

set -e

echo "Starting Meshy Worker..."

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

# Create output directory
mkdir -p /workspace/assets/3d/generated/models
mkdir -p /workspace/assets/3d/generated/textures
mkdir -p /workspace/assets/3d/generated/animations

# Keep container running or run the worker
exec "$@"