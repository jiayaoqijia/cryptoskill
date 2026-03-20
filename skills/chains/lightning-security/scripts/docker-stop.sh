#!/usr/bin/env bash
# Stop the remote signer container.
#
# Usage:
#   docker-stop.sh                  # Stop (preserve data)
#   docker-stop.sh --clean          # Stop and remove volumes

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/../templates"
CLEAN=false

# Parse arguments.
while [[ $# -gt 0 ]]; do
    case $1 in
        --clean|-v)
            CLEAN=true
            shift
            ;;
        -h|--help)
            echo "Usage: docker-stop.sh [options]"
            echo ""
            echo "Stop the remote signer container."
            echo ""
            echo "Options:"
            echo "  --clean, -v  Remove volumes (clean state)"
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Check if the signer container is running.
if ! docker ps --format '{{.Names}}' 2>/dev/null | grep -qx 'litd-signer'; then
    echo "Signer container is not running."
    exit 0
fi

cd "$TEMPLATE_DIR"

echo "Stopping signer container..."

if [ "$CLEAN" = true ]; then
    docker compose -f docker-compose-signer.yml down -v
    echo "Stopped and removed volumes."
else
    docker compose -f docker-compose-signer.yml down
    echo "Stopped (volumes preserved)."
fi
