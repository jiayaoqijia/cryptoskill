# Level-crossing (entry-zone) alerts for CEX tokens (2 Okt 2026)

Class of ask: *"kasih tau kalau harga masuk zona entry / tembus invalidation"* — a watch on a **level**,
not on a delta. Distinct from change-gated alerts (`delta-gated-alerts-and-member-removal.md`): the
trigger is a price crossing a static band, so the state is a small boolean set per symbol, not a
snapshot of metrics.

Raised after an ILV/IMX entry plan was written: rather than promising "gw pantau", wire the lane and say
it is live. Full working example: `~/.hermes/scripts/gaming_entry_alert.py`, cron `8af0b0275137`,
`*/30 * * * *`, `no_agent=true`, `deliver=origin`.

## Script contract (`no_agent=true`)

- **Silent by default.** Empty stdout = no message to the user. Print *only* on a crossing.
- **One message per crossing.** State per symbol: `{"in_zone": false, "warned_inv": false}` in
  `~/.hermes/data/<lane>_state.json`; flip `in_zone=true` on entry and stay quiet while price is inside.
- **Re-arm on exit only.** Reset `in_zone=false` once price is back **above** the band top. Resetting on
  any out-of-band price makes a symbol oscillating at the edge alert on every tick.
- **Invalidation is its own flag** (`warned_inv`) so a dead thesis is stated once; clear it again when
  price recovers above the invalidation level.
- **Never edit the production state file by hand** to unstick a lane — it manufactures or suppresses
  alerts on the next tick. Delete it only for a deliberate cold run.

## Don't let a fetch failure become an alert

A `no_agent` script that raises exits non-zero → the scheduler sends the user an **error alert**. On a
30-minute price lane that turns a transient API hiccup into spam, which the user reads as "alert gak
berguna". So: retry the fetch 3× with backoff, write the failure to `~/.hermes/data/<lane>.log`, and
`return` with **zero stdout, exit 0** when there is no data. Accepted trade-off: a totally broken lane
goes quiet (check the log). A lane guarding money must invert this and fail loud.

## Price source: match the venue the user executes on

Binance public API is keyless and generous — use it as primary for CEX-listed picks:

```
https://api.binance.com/api/v3/ticker/24hr?symbols=["ILVUSDT","IMXUSDT"]
# -> lastPrice, priceChangePercent, highPrice, lowPrice   (data-api.binance.vision = same path, fallback)
```

- **400 Bad Request trap:** the `symbols` JSON array must contain **no spaces**. Python's default
  `json.dumps(["A","B"])` emits `["A", "B"]` → 400 that looks like an invalid symbol. Use
  `json.dumps(syms, separators=(",", ":"))`, then `urllib.parse.quote`.
- **CoinGecko `simple/price` as fallback only** — a few calls from one IP get 429'd, so it cannot be the
  primary of a 30-min lane. Keep a symbol→CoinGecko-id map for the fallback path.
- Quote levels from the user's execution venue so the zone is tradeable (and say when the book is thin
  enough that only limit orders in tranches make sense).

## Test the state machine before scheduling (state-safe)

Don't hand-edit production state. Write a throwaway test script (via `write_file` — inline heredocs
containing shell-significant punctuation can trip the terminal's backgrounding guard), load the module,
override `m.STATE = "/tmp/…json"`, loosen/tighten the bands, then assert four cases while capturing
stdout:

1. price outside every band → **0 bytes**
2. price inside a band → exactly one message for that symbol
3. immediate re-run → **0 bytes** (this silence is the deliverable)
4. price leaves the band and returns → message again (proves re-arm works)

Print `fetch_prices()` live values first: otherwise a "pass" on case 1 is indistinguishable from a silent
fetch failure.
