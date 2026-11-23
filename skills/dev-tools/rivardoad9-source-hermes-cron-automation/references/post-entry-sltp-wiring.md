# Post-entry SL/TP wiring (CEX position) — 2 Okt 2026

Extends `level-crossing-entry-zone-alerts.md` (the entry lane, `gaming_entry_alert.py`). This one covers
what happens **after the user says "oke gw entry X"**: the exit side is what needs monitoring, and the
scope of the lane grows from one band to three levels per symbol.

## Three levels per symbol, not one band

| field | meaning | fire rule |
|---|---|---|
| `lo`/`hi` | entry band | once while price is inside; re-arm only above `hi` |
| `break_up` | the shelf/reclaim level that turns "watch" into "valid" | once above it; re-arm only below `break_up * 0,99` |
| `inv` | invalidation | once below it; re-arm once back above |

**Hysteresis is not optional** on `break_up`: without the `* 0,99` re-arm band a price oscillating on the
level re-alerts on every tick. The invalidation message must state the *action*, not just the level
("KELUAR — jangan average down, tunggu struktur baru").

Keep a one-line `note` per symbol **inside** the ZONES dict so each level travels with its rationale and
dated catalyst ("post-spike flag 28 Sep … katalis: IDTrust masuk IBM Cloud Catalog 23 Sep"). A bare
"HBAR $0.1040" alert is noise; a plan is not.

## The exit side lives in the holdings watchdog

`~/.hermes/scripts/holdings_watch.py` — cron `*/15`, `no_agent`, delta-only, SENYAP unless a threshold is
crossed. Add optional explicit position fields so a manual CEX entry gets SL/TP pings:

```python
"hedera-hashgraph": {"sym": "HBAR", "binance": "HBARUSDT", "cg": "hedera-hashgraph",
                     "move": 10.0, "hi": None, "lo": None, "ma": 20,
                     "entry": 0.1063, "sl": 0.0975, "tp": [0.1229, 0.1310]},
```

- Leave `hi`/`lo` at `None` when `sl`/`tp` exist, or the same level fires twice from two code paths.
- Print the position context in the message (`entry $0.1063, −8,7%`) so the user sees the damage or the gain
  without opening a chart.
- Separate cooldowns and separate state keys per trigger: SL 6h, each TP 12h, keys `HBAR_sl`,
  `HBAR_tp0.1229` — one flag per level, never one flag for "position alerted".
- On a pump-after-fill the same script covers the ladder: TP1 = trim, TP2 = trim again, remainder trails.

## Test by monkeypatching — never by editing production state

Load the module, redirect its state/log paths to a temp dir, and drive synthetic prices through the fetch
function. For the zone lane that is `m.STATE`; for the watchdog `m.STATE_F`/`m.LOG_F`, plus
`m.binance_ticker`, `m.cg_prices`, `m.binance_closes`:

```python
spec = importlib.util.spec_from_file_location("hw", os.path.expanduser("~/.hermes/scripts/holdings_watch.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.STATE_F = os.path.join(tempfile.mkdtemp(), "state.json")
m.binance_ticker = lambda s: {"price": 0.0970 if s == "HBARUSDT" else 0.5, "chg24": 1.0, "quote_vol": 5e6}
m.cg_prices = lambda ids: {};  m.binance_closes = lambda s, limit=30: [0.1] * 30
# capture stdout per case
```

Cases that must all pass:

1. normal price → **0 bytes**
2. price at SL → exactly one 🔴 (`KENA SL`); immediate re-run → **0 bytes**
3. price at TP1 then TP2 → one 🟢 each
4. price back to normal → nothing (proves cooldown/re-arm, not merely silence)

Then run the script's own `--debug` once to print the live table, so a "silent" result on the real run can
be told apart from a broken fetch. Assert on the alert text, not on prose. Write the harness with
`write_file` (inline heredocs with shell-significant punctuation trip the terminal's backgrounding guard).
