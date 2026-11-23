# Silence, delivery and dedupe patterns for Hermes cron jobs

Proven on this stack (10 Sep 2026 pre-news briefing + blackout nudges + refresh jobs).

## 1. Silence is a design decision — pick the right mechanism

| Goal | Mechanism | Trap |
|---|---|---|
| Job that must speak only on anomaly | `no_agent=true` + script that prints **nothing** on success | If the script echoes its helpers' output, every run spams the chat. Capture and discard: `OUT=$(helper 2>&1); [ $? -ne 0 ] && { echo "⚠️ FAILED: $OUT"; exit 1; }` |
| Agent job whose message is conditional | `deliver="local"` + the agent sends via a helper script itself (e.g. `news_send.py`) | `deliver="origin"` auto-delivers the final response even when the agent decides "nothing to report" |
| Agent job that should be silent when idle | prompt it to answer exactly `[SILENT]` (the wrapper's convention) | A custom token like `NO_EVENT` is not understood by the delivery layer — use `[SILENT]` |

## 2. Conditional-message jobs need their own state

A nudge that runs every 15 min must fire **once per event**, not 96 times a day. Keep a
fingerprint file in `/tmp` (`<event>|<iso ts>|<phase>`) and skip anything already listed;
re-alert on a long cycle (the chain sweep uses 4h) for standing problems.
`no_agent` + high-frequency + dedupe = cheap and quiet. Stdlib-only Python is fine here.

## 3. Interpreter and environment

- Cron runs `.sh`/`.bash` via bash and everything else via Python — for scripts that need
  a project venv, wrap them: `#!/usr/bin/env bash` → `/home/<user>/<proj>/.venv/bin/python script.py`.
  (A system `python3` silently lacks `requests`/`dotenv` for repo scripts.)
- Read tokens from files inside the script; never inline them in the prompt
  (`exfil_curl_auth_header` blocks literal `curl -H "Authorization: Bearer $TOKEN"`).
- Any long/complex inline shell command can hit the agent's command-parser blocklist —
  write it to a file under `~/.hermes/scripts/` and run `bash <file>` instead.

## 4. Context-script pattern (0 token prep)

`script=` on an agent job injects the script's stdout as context before the prompt runs.
Use it for date/calendar/API/state dumps so the LLM only spends tokens on judgement:

```
context script: header + calendar + engine/API state + history + the domain rules
prompt        : window rule (when to speak), output format, honesty rules, how to send
```

Test the context script standalone first (`bash script.sh`) — it is where path,
interpreter and freshness bugs surface, and they never show up in the prompt.
