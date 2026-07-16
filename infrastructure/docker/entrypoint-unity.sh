#!/bin/bash
# Entrypoint for Unity Builder

set -e

echo "Starting Unity Builder..."

# Unity license handling
if [ -n "$UNITY_LICENSE" ]; then
    echo "Activating Unity license..."
    echo "$UNITY_LICENSE" > /tmp/unity_license.ulf
    /opt/unity/Editor/Unity -batchmode -quit -logfile - -username "$UNITY_USERNAME" -password "$UNITY_PASSWORD" -serial "$UNITY_SERIAL" || true
fi

# Set project path
export UNITY_PROJECT_PATH="/project"

# Build target handling
BUILD_TARGET="${BUILD_TARGET:-StandaloneWindows64}"
BUILD_OUTPUT_PATH="${BUILD_OUTPUT_PATH:-/builds}"

echo "Building for target: $BUILD_TARGET"
echo "Output path: $BUILD_OUTPUT_PATH"

mkdir -p "$BUILD_OUTPUT_PATH"

# Keep container running or run build
exec "$@"