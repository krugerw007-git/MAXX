#!/bin/bash
# Entrypoint for Claude Code Runner

set -e

echo "Starting Claude Code Runner..."

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

# Keep container running
exec "$@"