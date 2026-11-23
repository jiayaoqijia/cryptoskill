# Applying a cross-cutting output/format change across many cron lanes

Session: 5 Okt 2026. Ask: "rapihin gaya output dong" — one consistent message style across ~21
lanes delivering to three channels (user DM, @HermsNews_Bot, @zemiztradebot).

Do NOT rewrite each report builder. Two levers, in this order:

## 1. Agent jobs (`no_agent=false`) → attach a shared policy skill

```
cronjob(action="update", job_id="…", skills=[…existing…, "new-policy-skill"])
```

Passing `skills` **replaces** the list, so read the current one from `~/.hermes/cron/jobs.json`
first (this user's deep-dive job carries `crypto-narrative-scan`, `data-chart-rendering`).
The job's 9k-char prompt stays untouched, the contract lives in one skill, and it applies from the
next fire. (On the machine: skill `cron-output-style` holds the style contract itself.)

## 2. `no_agent` stdout lanes → filter stdout at the boundary

The scheduler delivers a `no_agent` job's stdout verbatim, so filter there rather than inside the
builder. Two shapes, both proven:

```bash
# A. thin wrapper script, then point the job's `script` field at it
#!/usr/bin/env bash
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
"$HERE/original_lane.sh" | python3 "$HERE/msgstyle.py" --kind warn
```

```bash
# B. inline pipe for an existing .sh lane
python3 "$HOME/.hermes/scripts/news_pause_nudge.py" | python3 "$HOME/.hermes/scripts/msgstyle.py" --kind alert
```

Rules that keep it safe:

- `set -uo pipefail` — a failed producer stays sticky through the pipe (rightmost non-zero wins).
- Empty stdout must stay empty: silent lanes (DB collectors, watchdogs) must not gain a footer or
  timestamp line when they have nothing to say.
- **Never** `exec > >(filter)` process substitution — output can be lost when bash exits.
- **Never** an EXIT trap in a script that `exec`s its real command — the substituted/replaced shell
  means the trap never runs. (Hit this designing `winner_study_cron.sh`: it used `exec python3 …`.)
- Python report scripts: wrap only the final `print()` via a module-level helper that `try/except`s
  and returns the raw text on failure. Formatting must never break an alert.

```python
def _style_alert(text: str) -> str:
    try:
        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from msgstyle import finish
        return finish(text, kind="alert")
    except Exception:
        return text
```

- Shared senders (`news_send.py`, `fm_engine_bot.send_text/send_photo`, `fm_bot_bridge.send`) get
  the style call INSIDE the send function, so every caller inherits it in one edit.
- Photo captions are capped at 1024 chars (Telegram) — style then slice.

## 3. Verify both directions, then sweep

- Run each styled lane with nothing to report → expect **empty stdout** (proves you didn't turn a
  silent lane noisy).
- Force one real payload through it → proves the message path still renders.
- Sweep: list jobs from `jobs.json` and match every `script`/`skills` against the new layer; report
  the deliberately-untouched lanes (silent collectors, `deliver: local` context scripts) explicitly
  so they don't look forgotten.
- Rollback story to tell the user: the `try/except` fallbacks mean deleting the formatter reverts
  every lane to raw output; one file is the single tuning point for future style changes.

## The style layer itself (msgstyle.py)

`~/.hermes/scripts/msgstyle.py` (lib + CLI): `finish(text, kind=…)` with `kind ∈
{alert, card, report, news, info, warn}`; CLI `--kind/--emoji/--title/--no-time/--no-regime`.
Normalizes bullets to `• `, field separators to ` · `, collapses blank lines, preserves 3-space
sub-line indentation, rewrites `Regime:` lines to the `📊` footer form, appends `🕒 … WIB` +
one-line macro regime from `~/.hermes/data/market_regime.json`, and caps only short kinds (alert /
news / info / warn: 8 lines) — anything longer than 18 lines is treated as a report and left uncut
so data-dense output never gets truncated into uselessness.
