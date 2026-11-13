#!/usr/bin/env bash
# One-shot probe of the Koinju setup state.
#
# Output (single line, space-separated tokens):
#   uv:<ok|missing>
#   pyproject:<found|none>
#   venv:<active|present|none>
#   deps:<ok|missing:name1,name2,...>
#   creds:<ok|missing:NAME1,NAME2,...>
#   project_env:<found|none>          (./.koinju.env)
#   home_env:<found|none>             (~/.koinju.env)
#
# The probe auto-sources .koinju.env (cwd) then ~/.koinju.env so the `creds:`
# token reflects what the bundled helpers will actually see at run-time.
#
# Use this in place of multiple separate bash invocations when deciding
# whether to bootstrap.

set -u

command -v uv >/dev/null 2>&1 && UV="uv:ok" || UV="uv:missing"

[ -f pyproject.toml ] && PYPROJ="pyproject:found" || PYPROJ="pyproject:none"

if [ -n "${VIRTUAL_ENV:-}" ]; then
    VENV="venv:active"
elif [ -d .venv ]; then
    VENV="venv:present"
else
    VENV="venv:none"
fi

# Auto-source so creds reflect what helpers will see
# shellcheck disable=SC1091
[ -f .koinju.env ] && source .koinju.env 2>/dev/null || true
# shellcheck disable=SC1091
[ -f "$HOME/.koinju.env" ] && source "$HOME/.koinju.env" 2>/dev/null || true

# deps (python imports)
MISSING_DEPS=""
for pkg in clickhouse_connect pandas plotly tabulate; do
    python3 -c "import $pkg" 2>/dev/null || MISSING_DEPS="${MISSING_DEPS:+$MISSING_DEPS,}$pkg"
done
[ -z "$MISSING_DEPS" ] && DEPS="deps:ok" || DEPS="deps:missing:$MISSING_DEPS"

# creds (env vars)
MISSING_CREDS=""
for v in KOINJU_API_KEY KOINJU_DB_HOST KOINJU_DB_USER KOINJU_DB_PASSWORD; do
    [ -n "${!v:-}" ] || MISSING_CREDS="${MISSING_CREDS:+$MISSING_CREDS,}$v"
done
[ -z "$MISSING_CREDS" ] && CREDS="creds:ok" || CREDS="creds:missing:$MISSING_CREDS"

[ -f .koinju.env ] && PROJENV="project_env:found" || PROJENV="project_env:none"
[ -f "$HOME/.koinju.env" ] && HOMEENV="home_env:found" || HOMEENV="home_env:none"

# Suggest copying project .koinju.env → ~/.koinju.env for cross-session reuse,
# but only if the project file is populated (creds:ok) and the home file is absent.
if [ -f .koinju.env ] && [ ! -f "$HOME/.koinju.env" ] && [ -z "$MISSING_CREDS" ]; then
    SUGGEST="suggest_save_global:yes"
else
    SUGGEST="suggest_save_global:no"
fi

echo "$UV $PYPROJ $VENV $DEPS $CREDS $PROJENV $HOMEENV $SUGGEST"
