#!/usr/bin/env bash
# Koinju project bootstrap — full setup in one shot.
#
# Usage:
#   bash setup.sh             # cwd if empty (ignoring .git), else ./koinju-demo
#   bash setup.sh <dir>       # explicit target directory (created if needed)
#
# What it does:
#   - Probes for uv; falls back to venv + pip if not installed
#   - uv init (or python3 -m venv) and installs deps
#   - Seeds main.py from welcome_btc_usdt.py (always overwrites)
#   - Creates .koinju.env from the bundled template if missing (chmod 600)
#   - Appends .koinju.env to .gitignore (idempotent)
#   - Prints the credential URL and run command
#
# Idempotent: safe to re-run.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Resolve target dir
if [ $# -ge 1 ]; then
    TARGET="$1"
elif [ -z "$(ls -A 2>/dev/null | grep -v '^\.git$' || true)" ]; then
    TARGET="."
else
    TARGET="koinju-demo"
fi

if [ "$TARGET" != "." ]; then
    mkdir -p "$TARGET"
    cd "$TARGET"
fi
PROJ_DIR="$(pwd)"

# Detect uv
if command -v uv >/dev/null 2>&1; then
    USE_UV=1
    BACKEND="uv"
else
    USE_UV=0
    BACKEND="venv+pip"
    echo "[setup] uv not found — using venv + pip (install uv with: curl -LsSf https://astral.sh/uv/install.sh | sh)"
fi

# Scaffold + install
if [ $USE_UV -eq 1 ]; then
    if [ ! -f pyproject.toml ]; then
        uv init . --python 3.12 2>/dev/null || uv init .
    fi
    uv add clickhouse-connect pandas plotly tabulate
    RUN_CMD="uv run python main.py"
else
    if ! command -v python3 >/dev/null 2>&1; then
        cat >&2 <<'EOF'
[setup] Neither uv nor python3 is available — install one:
  uv (recommended): curl -LsSf https://astral.sh/uv/install.sh | sh
  python3:
    macOS: xcode-select --install   (or `brew install python`)
    Linux: apt install python3-venv   (or your distro's equivalent)
EOF
        exit 1
    fi
    if [ ! -d .venv ]; then
        python3 -m venv .venv
    fi
    # shellcheck disable=SC1091
    source .venv/bin/activate
    pip install --quiet clickhouse-connect pandas plotly tabulate
    RUN_CMD="source .venv/bin/activate && python main.py"
fi

# Seed main.py (always overwrite — bootstrap intent is a fresh starter)
cp "$SKILL_DIR/scripts/welcome_btc_usdt.py" main.py

# Seed .koinju.env only if missing (don't clobber existing creds)
if [ ! -f .koinju.env ]; then
    cp "$SKILL_DIR/references/koinju.env.example" .koinju.env
    chmod 600 .koinju.env
fi

# Append to .gitignore (idempotent)
touch .gitignore
grep -qxF '.koinju.env' .gitignore || echo '.koinju.env' >> .gitignore

cat <<EOF

[setup] Koinju project ready at: $PROJ_DIR ($BACKEND)

Next steps:
  1. Edit .koinju.env and fill in your credentials.
     Don't have any yet? Sign up at https://koinju.io/pricing —
     Koinju emails you a link to https://dataroom.koinju.io/ where the
     REST API key and ClickHouse host / user / password live.
  2. Run: $RUN_CMD
     (Plotly will open a BTC-USDT candlestick chart in your default browser.)

EOF
