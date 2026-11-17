# Radar claim matrix (honesty)

| Claim | Needs on disk |
|-------|----------------|
| Unit green | pytest / CI |
| Ops-ready | `READY_OPS.json` `ops_ready=true` |
| Short soak | soak pack `hard_fails=0` (not 48h) |
| 48h soak | `approx_48h_claim_ok=true` AND `hard_fails=0` |
| Live money preflight | `go_live_money.ps1` PASS |

Missing pack ⇒ **not claimed** / ⏳. Never invent PASS.
