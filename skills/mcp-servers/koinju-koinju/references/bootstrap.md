# Bootstrap a Koinju Python project

> **First, try the bundled `scripts/setup.sh`** — `bash ~/.claude/skills/koinju/scripts/setup.sh [target-dir]` does everything in this doc in a single idempotent shell call (cwd probe + uv/venv probe + scaffold + install + seed `main.py` + create `.koinju.env` + `.gitignore`). Only fall through to this doc if you need to customize, debug, or can't run the script.

Two triggers fire the bootstrap; both end at the same project state (a uv or venv Python project with deps installed, `main.py` seeded, `.koinju.env` created).

## Triggers

### A — Proactive: user explicitly asks for project setup

Examples: "help me set up a python project to work with the koinju api", "scaffold a koinju starter project", "create a project I can use to call koinju". Go **straight to the bootstrap commands below** — no probing needed; this IS the proposal. The bootstrap auto-picks the destination by probing cwd: in-place if cwd is empty (apart from `.git`), `./koinju-demo/` otherwise. Confirm only if the user already named a different folder.

For this trigger, **seed `main.py` from `scripts/welcome_btc_usdt.py`** — it gives a working BTC-USDT candlestick chart out of the box, which is a much better "first run" than the minimal text starter.

### B — Reactive: missing deps OR missing credentials block a SQL task

Two failure modes route here, and the same setup flow handles both at once (deps + creds + working project structure):

1. `python3 -c "import clickhouse_connect"` raises `ModuleNotFoundError`, OR
2. One or more `KOINJU_*` env vars are unset (auth check in SKILL.md step 3 failed).

Probe everything in one shot:

```bash
bash ~/.claude/skills/koinju/scripts/probe-env.sh
# → uv:ok pyproject:none venv:none deps:missing:clickhouse_connect,tabulate creds:missing:KOINJU_API_KEY,KOINJU_DB_HOST project_env:none home_env:none
```

(Or, if for some reason the helper isn't available, the inline equivalent:)

```bash
python3 -c "import clickhouse_connect" 2>/dev/null || echo "deps MISSING"
[ -n "${KOINJU_API_KEY:-}" ] && [ -n "${KOINJU_DB_HOST:-}" ] && \
[ -n "${KOINJU_DB_USER:-}" ] && [ -n "${KOINJU_DB_PASSWORD:-}" ] || echo "creds MISSING"
```

If either prints `MISSING`, critically:

- **DO NOT** run `pip install` in the current shell. The user's system pip may be broken (mismatched Python, missing `tomllib`, no write perms) and you'll burn turns debugging it.
- **DO NOT** hunt for an alternative Python (`/usr/bin/python3`, `python3.10`, `python3.12`) that happens to have the package. That "works" by accident, leaves the user confused about where their code is actually running, and doesn't scale to the next missing dep.
- **DO NOT** fix only the dep when creds are also missing, or vice versa — the user will hit the other blocker the next turn. Bundle both into one setup flow.

Ask once, tailoring to what's actually missing:

> "[`clickhouse_connect` isn't installed / `KOINJU_*` env vars aren't set / both]. I can scaffold a clean `uv` project at `./koinju-demo/` that handles it: installs `clickhouse-connect`, `pandas`, `plotly`, generates a `.env.example` with the right vars, and points you at https://koinju.io/pricing for credentials. Want me to go ahead?"

- **Yes** → run the bootstrap commands below; seed `main.py` from the minimal template in this file (the user came here mid-query, not for a demo).
- **No / declined** → **print the code you would have run as a fenced block**, plus a one-line https://koinju.io/pricing pointer if creds were the missing piece. Don't try to coerce their current env into working.
- **Different folder or already has a `pyproject.toml`** → adapt — see "Variations" below.

## Default bootstrap

**Where to scaffold** — pick by probing cwd:

```bash
[ -z "$(ls -A 2>/dev/null | grep -v '^\.git$')" ] && echo "cwd empty → in-place" || echo "cwd has files → use ./koinju-demo/"
```

- **cwd empty** → scaffold **in-place**. The project IS your cwd; no `cd` afterwards.
- **cwd has files** (anything other than `.git`) → scaffold inside `./koinju-demo/` so we don't pollute the existing workspace.

`.git` is treated as empty because `git init && claude` is a common pre-bootstrap pattern.

**Prefer `uv`** — it's faster, lockfile-aware, and skips the venv-activation dance. Probe first:

```bash
command -v uv >/dev/null 2>&1 && echo "uv ok" || echo "uv MISSING"
```

### With `uv` (preferred)

```bash
# In-place (cwd empty) — `uv init .`:
uv init . --python 3.12
uv add clickhouse-connect pandas plotly tabulate
# run later with: uv run python main.py

# OR subfolder (cwd has files):
uv init koinju-demo --python 3.12
cd koinju-demo
uv add clickhouse-connect pandas plotly tabulate
# run later with: uv run python main.py
```

### Without `uv` — `venv` + `pip` fallback

```bash
# In-place (cwd empty):
python3 -m venv .venv
source .venv/bin/activate
pip install clickhouse-connect pandas plotly tabulate
# run later with: python main.py    (venv already active)

# OR subfolder (cwd has files):
mkdir koinju-demo
cd koinju-demo
python3 -m venv .venv
source .venv/bin/activate
pip install clickhouse-connect pandas plotly tabulate
# run later with: python main.py
```

(`tabulate` is needed for `df.to_markdown()` — the default rendering for small results.)

**Don't** fall through to `pip install --user` or system pip — that's how queries end up running under whichever Python happens to have the package (the exact antipattern called out in [Triggers > B](#b--reactive-missing-deps-or-missing-credentials-block-a-sql-task)). If the user wants `uv` for next time, the one-line installer is `curl -LsSf https://astral.sh/uv/install.sh | sh`.

Then create `main.py` and `.koinju.env` from the templates below (and append `.koinju.env` to `.gitignore`). A table of BTC-USDT hourly candles printing to stdout means the bootstrap worked.

## Starter `main.py`

```python
"""Minimal koinju demo: pull the last 24h of BTC-USDT 1h candles and print them."""

from __future__ import annotations

import os

import clickhouse_connect


REQUIRED = ("KOINJU_DB_HOST", "KOINJU_DB_USER", "KOINJU_DB_PASSWORD")


def _autosource_koinju_env() -> None:
    for path in (".koinju.env", os.path.expanduser("~/.koinju.env")):
        if not os.path.isfile(path):
            continue
        with open(path) as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("export "):
                    line = line[7:]
                if "=" not in line:
                    continue
                key, _, value = line.partition("=")
                value = value.strip().strip('"').strip("'")
                os.environ.setdefault(key.strip(), value)


def main() -> None:
    _autosource_koinju_env()
    missing = [v for v in REQUIRED if not os.environ.get(v)]
    if missing:
        raise SystemExit(
            f"Missing env vars: {', '.join(missing)}. "
            "Don't have credentials? Sign up at https://koinju.io/pricing — "
            "you'll receive an email with a https://dataroom.koinju.io/ link."
        )

    client = clickhouse_connect.get_client(
        host=os.environ["KOINJU_DB_HOST"],
        port=int(os.environ.get("KOINJU_DB_PORT", "8443")),
        secure=True,
        username=os.environ["KOINJU_DB_USER"],
        password=os.environ["KOINJU_DB_PASSWORD"],
        database=os.environ.get("KOINJU_DB_DATABASE", "api"),
    )
    df = client.query_df("""
        SELECT start, open, high, low, close, volume
        FROM api.ohlcv_1h
        WHERE exchange = 'binance' AND market = 'BTC-USDT'
          AND start >= now() - INTERVAL 24 HOUR
        ORDER BY start
    """)
    print(df.to_markdown(index=False))


if __name__ == "__main__":
    main()
```

## Project `.koinju.env`

Create `koinju-demo/.koinju.env` with the four required vars (and any optionals). The auto-source helper loads this when scripts run from inside `koinju-demo/`, with `~/.koinju.env` as the global fallback (project-local wins per-var).

```bash
cat > .koinju.env <<'EOF'
# Koinju credentials for this project — fill in below, then chmod 600.
# Don't commit this file. (Bootstrap adds it to .gitignore.)
export KOINJU_API_KEY=
export KOINJU_DB_HOST=
export KOINJU_DB_USER=
export KOINJU_DB_PASSWORD=
EOF
chmod 600 .koinju.env
echo '.koinju.env' >> .gitignore
```

Tell the user to open `.koinju.env` and paste in their values from https://dataroom.koinju.io/ (see [`auth.md`](auth.md)). If they already have `~/.koinju.env` globally with the same values, the project file can stay empty or hold only per-project overrides — the auto-source merges both.

## Variations

| Situation | What to do |
|---|---|
| User already has a `pyproject.toml` or active venv | Skip the scaffolding step. With uv: `uv add clickhouse-connect pandas plotly tabulate`. Without uv: activate their venv first, then `pip install clickhouse-connect pandas plotly tabulate` |
| User wants plotting in the starter | Copy `scripts/welcome_btc_usdt.py` from the skill as `main.py` instead — it already includes the Plotly candlestick |
| User wants a backtest starter | Copy `scripts/backtest_buy_and_hold.py` instead |
| User wants a different folder name | Use their name verbatim; `koinju-demo` is just the default for the non-empty-cwd path |

## Don'ts

- Don't `pip install` system-wide without asking.
- Don't write into the user's home directory or any path outside cwd unless they ask.
- Don't overwrite an existing `main.py` / `pyproject.toml` without confirming.
- Don't add deps the user didn't approve. Three packages (`clickhouse-connect`, `pandas`, `plotly`) is the minimum needed for the bundled scripts; everything else is opt-in.
