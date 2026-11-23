# No-agent watchdog design + how to test one safely

For `no_agent` cron jobs that watch a live system (silent-when-healthy alerts). Learned
while hardening the FlowMetrix live watchdog; the pattern is generic.

## The delivery contract (drives every design choice)

- **Non-empty stdout is delivered to the user VERBATIM. Empty stdout is silent.** So the
  script must print nothing when healthy, and print exactly the message text when not.
- **A recurring condition must be state-deduped.** A watchdog that re-prints a true-but-
  unchanged finding every run spams the user on every tick — misread as "the system is
  broken again". Keep state in `/tmp/<name>_state.*`, compare, and alert only on a
  status CHANGE (e.g. "bot dead" once per 6 h, then a single "✅ normal lagi" on recovery).
- **Echo a short machine tag for local logs** ("dd alert", "exit alert") and the human
  message via the notify function. The tag goes to cron output; the message goes to chat.

## What a live-money watchdog should cover

1. process alive / API responds
2. mode regression (configured live vs reported dry-run)
3. drawdown vs the pinned baseline + position count changes
4. NEW error lines since a watermark (never "no new error" ⇒ assume healthy)
5. stateful dependency liveness (e.g. the command bot), read from the LOG TAIL, not a
   watermark — otherwise "no new error" fakes "healthy"
6. **the exit path**: for every open position — is it still being checked (stall), has
   it overrun its max age, and did any position CLOSE (report the close + PnL + reason).
   Without this, the user learns about a stop-loss only by luck.
7. on-chain truth (what the DB cannot see), for systems where money can leave the book

## Testing a watchdog without touching the live system

Extract the logic block from the script itself (don't test a copy), then feed it a COPY
of the production DB and a temp state path:

```bash
python3 - "$WD" "$T/logic.py" <<'PY'
import re, sys
src = open(sys.argv[1]).read()
m = re.search(r"<<'PY' 2>/dev/null\n(.*?)\nPY\n\)", src, re.S)   # the embedded python
open(sys.argv[2], "w").write(m.group(1) + "\n")
PY
cp /path/to/production.db "$T/test.db"      # NEVER test against the live DB
```

Then synthesise the states you care about in the copy: open + stale heartbeat, open +
over max age, then flip a row to its closed status and assert the close alert fires,
then delete everything and assert silence.

**Pitfall that produced a FALSE PASS:** inserting a test row without satisfying every
`NOT NULL` column raises, the row never lands, the script prints nothing — and "printed
nothing" is indistinguishable from "correctly silent". Build the INSERT from
`PRAGMA table_info(...)` (fill every notnull column with a type-appropriate value, then
override the fields you care about), and assert the row count after inserting. Always
confirm the happy-path branch by making it print something once before trusting silence.

Also verify the real script in the live run after the change (`bash <script>` → empty
output + exit 0) and that the live DB is still untouched.
