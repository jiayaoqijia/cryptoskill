# Funding-chain follow (self-growing watchlists) + offline tests for quiet cron scripts

Two lessons from building "track this entity's wallets" monitors (worked example:
`~/.hermes/scripts/hl_insider_track.py`, cron `*/10 * * * *`, `no_agent`).

---

## 1. The follow must chain, and it must be gated

A watchlist that never grows is useless the moment the entity rotates wallets. A watchlist that
grows on every transfer is useless too — it fills up with exchanges. The rule that survives real
data:

| Destination | Test | Action |
|---|---|---|
| Fresh wallet (nonce ≤ ~3) | could not have traded before | **follow**: add to watchlist, then treat it exactly like any other tracked wallet (scan its outflows too) |
| Established address (nonce in the hundreds/thousands) | working address / venue | **report only**: alert the transfer, do NOT add — it is an exchange / bridge / OTC desk, not the entity |

Observed 7 Oct 2026 (arbitrum + Hyperliquid insider-short cluster): a hub funded a fresh wallet
(nonce 2) with **$5.00M USDC**; three minutes later that wallet forwarded the whole $5.00M to a
`nonce 247,662` EOA that burns USDC out (bridge pattern). The label matters: "wallet baru (fresh,
nonce 2)" and "alamat aktif (nonce 247.662) → nggak diikutin" are two different findings, and
calling the second one "wallet baru" is a factual error the user will catch.

Other design points that paid off:

- **Scan every tracked wallet as a sender**, including ones added minutes ago — otherwise the chain
  dies at hop 1. (The original bug: outflows were scanned only from the seed hubs and the 4 seed
  traders.)
- **Probe the new wallet's position immediately at discovery**, not on the next tick; store the
  result as the baseline so subsequent open/close/flip alerts stay correct instead of false-flagging
  a pre-existing position as a new open.
- **Cap depth and breadth** (`MAX_HOP=5`, `MAX_WATCH=30`) and append a skip line + a log entry when
  the cap bites. Report the skip — silence looks like "nothing happened".
- **Legacy rows need a default**: wallets added before a `hop` column existed must be treated as
  hop 1 (`hop_of()` returns a default by tag) rather than mutating the live state file, which races
  the cron that rewrites it atomically every tick.
- **A no-change run must print nothing** (empty stdout = no message). A `--dry-run` that prints
  nothing against live state is the cheapest proof the new branch has no false positives.

---

## 2. Offline scenario tests for a network-heavy cron script

Production output is not a test harness. Load the script as a module, replace the network layer,
drive the scenarios, assert on text + state.

```python
import importlib.util, io, json, os, sys, contextlib

spec = importlib.util.spec_from_file_location("hlit", os.path.expanduser("~/.hermes/scripts/hl_insider_track.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

# fake the chain layer (behaviour driven by the args the script passes)
def fake_usdc_logs(from_blk, to_blk, to_addrs=None, from_addrs=None):
    if to_addrs:                       # a different query shape -> different result set
        return []
    out = []
    if WATCH in from_addrs:            # scenario: watched wallet rotates again
        out.append({"from": WATCH, "to": FRESH_DST, "usdc": 6000.0, "block": 1000, "tx": "0xdead"})
        out.append({"from": WATCH, "to": OLD_DST,   "usdc": 500000.0, "block": 1000, "tx": "0xcafe"})
    return out

m.usdc_logs   = fake_usdc_logs
m.hl_snapshot = lambda addr: (POSITION if addr == FRESH_DST else ({}, 0.0, [], []))
m.latest_block = lambda: 1000
m.nonce_of     = lambda a, blk="latest": (1 if a == FRESH_DST else (247000 if a == OLD_DST else 5))
m.block_ts     = lambda blk, now=None: 1791350000

def run_case(hop_cap):
    m.MAX_HOP = hop_cap
    st = make_state()                                  # seed state: seeds + one watched wallet
    with open(STATE, "w") as f: json.dump(st, f)
    cap = {}
    m.save_state = lambda p, s: cap.update(s)           # capture in-memory state
    m.log        = lambda e: None                       # never touch the real log
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = m.run(STATE, dry=False)                    # NOT dry: see pitfall below
    return rc, buf.getvalue(), cap
```

Scenario matrix that has earned its keep (all 20 asserts passed):

1. watched wallet → fresh address **with** a position ⇒ alert "PINDAH WALLET LAGI (hop 2)" +
   "ADA POSISI DI WALLET BARU", and the position detail (size, entry, leverage, liq, uPnL) is in
   the text;
2. same transfer with `MAX_HOP` lowered ⇒ "tidak diikutin", no hop alert;
3. hub → fresh wallet (flat) ⇒ "PENDANAAN BARU" + "WALLET BARU DIPANTAU … posisi kosong", wallet
   present in state with `hop == 1`;
4. watched wallet → established address (nonce 247k) ⇒ "PINDAH KE ALAMAT AKTIF", **and the address
   is absent from state** (the assert that actually catches watchlist pollution).

### Pitfalls hit while writing these tests

- **`--dry-run` does not save state.** Asserting on the state *file* after a dry run reads the seed
  you wrote yourself — the test passes or fails for the wrong reason (in this session: two asserts
  failed for exactly this). Capture the state dict by patching `save_state` and run non-dry.
- Patch `log` too, or the test appends junk to the production JSONL log.
- **`pkill -f "chrome-headless"` kills the shell running it** — the pattern matches the command line
  of your own bash process. Use a non-self-matching pattern: `pkill -f "chrome[-]headless"`.
- Keep the test as a permanent sibling of the script (`~/.hermes/scripts/test_<script>.py`) so the
  next change to the same script re-runs the same matrix. Point its temp state at `/tmp`, never at
  `~/.hermes/data/`.
- Dry-run the patched script against **live** state once as the final gate: exit 0 with no output
  (or exactly the one real event) = no false positives introduced.
