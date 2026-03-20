#!/usr/bin/env bash
# One-command initialization for universal-account-example.
# Usage:
#   ./init.sh new [--target <dir>] [--skip-smoke]
#   ./init.sh import <PRIVATE_KEY> [--target <dir>] [--skip-smoke]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${UNIVERSAL_ACCOUNT_EXAMPLE_DIR:-universal-account-example}"
RUN_SMOKE_TEST=1
ACTION=""
PRIVATE_KEY=""

print_usage() {
    echo "Usage:"
    echo "  ./init.sh new [--target <dir>] [--skip-smoke]"
    echo "  ./init.sh import <PRIVATE_KEY> [--target <dir>] [--skip-smoke]"
}

while [ "$#" -gt 0 ]; do
    case "$1" in
        new)
            ACTION="new"
            shift
            ;;
        import)
            ACTION="import"
            shift
            if [ "$#" -eq 0 ]; then
                echo "Missing private key for import."
                print_usage
                exit 1
            fi
            PRIVATE_KEY="$1"
            shift
            ;;
        --target)
            shift
            if [ "$#" -eq 0 ]; then
                echo "Missing value for --target."
                print_usage
                exit 1
            fi
            TARGET_DIR="$1"
            shift
            ;;
        --skip-smoke)
            RUN_SMOKE_TEST=0
            shift
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        *)
            echo "Unknown argument: $1"
            print_usage
            exit 1
            ;;
    esac
done

if [ -z "$ACTION" ]; then
    ACTION="new"
fi

echo "Step 1/4: Bootstrap project"
bash "$SCRIPT_DIR/bootstrap-example.sh" "$TARGET_DIR"

echo "Step 2/4: Patch trade defaults"
bash "$SCRIPT_DIR/patch-trade-defaults.sh" "$TARGET_DIR"

echo "Step 3/4: Create .env"
(
    cd "$TARGET_DIR"
    if [ "$ACTION" = "new" ]; then
        bash "$SCRIPT_DIR/setup-wizard.sh" new
    else
        bash "$SCRIPT_DIR/setup-wizard.sh" import "$PRIVATE_KEY"
    fi
)

if [ "$RUN_SMOKE_TEST" = "1" ]; then
    echo "Step 4/4: Smoke test"
    (
        cd "$TARGET_DIR"
        npx tsx examples/get-primary-asset.ts
    )
else
    echo "Step 4/4: Smoke test skipped (--skip-smoke)"
fi

echo ""
echo "Initialization complete."
echo "Project directory: $TARGET_DIR"
