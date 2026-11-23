# Extending a live `no_agent` alert script — three traps

Sibling of `funding-chain-follow-and-script-tests.md` (the watchlist that grows on its own) and
`alert-script-testing-safe.md` (offline test harnesses). These are the traps hit 9 Oct 2026 while
adding a new alert branch to `~/.hermes/scripts/hl_insider_track.py` (`*/10 * * * *`, `no_agent`)
— a script that had been running in production for days.

## (a) The flush-order trap — a new branch can be silently dropped

The script accumulates alert strings into a local `blocks` list, then one pass converts them:

```python
            for b in blocks:
                events.append((1, b))
            if new_ledger:            # other sections append to `events` directly
```

A new branch appended **after** that loop compiles, runs, produces no error, writes nothing to the
log, and no-ops forever. It is invisible to a dry run against live state (which should print
nothing anyway) — the change *looks* shipped. Always insert the new mutation **before** the flush,
then prove it fires:

1. copy the live state, `pop()` the one baseline field the new branch keys on for a single entity,
2. write it to `/tmp` and run `--state /tmp/x.json --dry-run` → the branch **must** print its alert,
3. run the same script against live state → must stay silent (no false positives).

Symptom to recognise: "I added the condition, the code is right, and it never triggers."

## (b) Backfill the new baseline silently — and only the new field

Any code path that adopts *existing* entities into the tracked set makes the next tick report every
pre-existing holding as brand new (the diff sees `old == {}`). Write the baseline rows into the state
before the next tick — reusing the script's own `save_state` gives you the atomic
write-to-tmp + `os.replace` for free:

```python
st = m.load_state(m.DEFAULT_STATE)
for a in newly_adopted:
    pos, acct, ledger, fills, spot = m.hl_snapshot(a)     # fetch ONCE, use as baseline
    st["wallets"][a] = {..., "pos": pos, "spot": spot, "last_fill": …, "ledger_seen": [...]}
m.save_state(m.DEFAULT_STATE, st)
```

Backfill **only the field you just added**. Do not refresh `pos` / `last_fill` / `last_ledger` while
you are in there — those baselines are the reference the next diff compares against, so refreshing
them swallows the real changes that happened since the last tick.

## (c) Verify in production — a dry run is not the gate

`no_agent` scripts return no chat reply, so a silent run is indistinguishable from a dead job. After
the edit, wait for the **next tick** and read three things:

- the state file's `last_run` advanced past the edit (and `block`/counter fields moved);
- the tracked-entity count includes the new cohort (`wallets`, plus the new field you added);
- the JSONL log gained `muted-moves` / no `alert` rows — i.e. it ran, and stayed quiet.

Only then tell the user it is live. Also check the job's own `last_status` in the cron list; a
`last_fire_error` there is the other way a silent script lies.

## (d) API budget: adding tracked entities is not free

Hyperliquid `/info` weights differ by endpoint — `clearinghouseState` ≈2, but `userFills` and
`userNonFundingLedgerUpdates` are ≈20 each, so one tracked wallet costs ≈42 weight per tick. Going
from 34 to 60 tracked wallets took a dry run from **27s to 38s**. Measure wall-clock before/after and
say the number when you add a cohort; growing a watchlist by an order of magnitude is what turns a
comfortable 10-minute job into a rate-limited one (and this host shares the IP with other HL jobs).
