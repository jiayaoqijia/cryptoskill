---
name: radar-ops-status
description: >-
  Honest DUP Market Radar readiness language — ops-ready vs short soak vs 48h
  claim vs live money. Use when the user asks if radar is ready, green, soaked,
  PASS, or production-ready.
license: MIT
compatibility: Requires local clone of dup-market-radar for gate scripts; Windows PowerShell preferred.
metadata:
  author: dup-labs
  version: "0.1.6"
  product: dup-market-radar
---

# Radar ops status (fail-closed)

## When to Use

- User asks «готов / ready / green / soak passed / можно в прод»
- Writing README/CHANGELOG claims about radar readiness

## Invariants

1. **Ops-ready** = `go_ready.ps1` PASS + `data/evidence/READY_OPS.json` with `ops_ready=true`. Not a 48h claim.
2. **48h soak PASS** only if pack has `approx_48h_claim_ok=true` **and** `hard_fails=0`.
3. **Live money** is separate — skill `radar-live-money-gate`.
4. Futures data/watch OK; futures **auto** never — skill `no-futures-auto`.

## Steps

1. Prefer real command output over memory.
2. Run or cite:

```powershell
cd <path>\dup-market-radar
.\scripts\test_all.ps1 -SkipBuild
.\scripts\go_ready.ps1 -SkipBuild
```

3. Answer with the **exact** gate that passed (pytest / go_ready / soak fields).

## Examples

- User: «soak прошёл?» → Check pack; if missing/`approx_48h_claim_ok=false` → **not claimed**.
- User: «ops ready?» → Only if `READY_OPS.json` says `ops_ready=true`.

## Refuse

- Painting green without output or pack paths.
- Mixing L1 mesh soak with radar packs — see `l1-boundary`.

## References

- [Evidence matrix language](references/evidence-matrix.md)
