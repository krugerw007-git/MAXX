#!/bin/bash
# Entrypoint for Codex Runner

set -e

echo "Starting Codex Runner..."

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

# Keep container running
exec "$@"