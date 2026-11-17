# Claim matrix

## Radar

| Claim | Needs |
|-------|--------|
| Unit green | pytest / CI |
| Ops-ready | READY_OPS.json ops_ready=true |
| Short soak | hard_fails=0 |
| 48h | approx_48h_claim_ok=true AND hard_fails=0 |
| Live preflight | go_live_money PASS |

## absolute-trading-bot

| Claim | Needs |
|-------|--------|
| Protocol status | `docs/PROTOCOL_STATUS.md` in-tree |
| Entries unlocked | **Refuse** while status says v1 stopped / SPOT_ENTRIES off |
| MEASUREMENT edge | Historical only — do not silently rewrite for PASS |
| Gate PASS unlock | Old eight-median gate does **not** unlock entries |

## L1

Cite `dup-protocol` / `dup-protocol-experimental` docs only — never radar packs as mesh soak.
