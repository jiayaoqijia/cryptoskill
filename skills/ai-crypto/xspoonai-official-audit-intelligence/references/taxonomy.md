# Vulnerability Taxonomy (for Audit Intelligence)

This taxonomy is used to normalize output labels from Solodit findings and pattern matching.

## Severity

- `CRITICAL`: catastrophic loss possible without privileged assumptions
- `HIGH`: direct fund loss / permanent lock / privilege takeover
- `MEDIUM`: meaningful impact with conditions
- `LOW`: limited impact or hard-to-exploit issues
- `INFO`: non-blocking hardening advice

## Categories

1. `access-control`
   - Missing auth checks
   - Dangerous admin flows

2. `reentrancy`
   - External interaction before state update
   - Cross-function reentrancy paths

3. `oracle-manipulation`
   - Spot-price dependency
   - Insufficient TWAP / sanity checks

4. `precision-loss`
   - Division truncation
   - Decimal mismatch

5. `upgradeability-risk`
   - Uninitialized proxy
   - Storage slot collision

6. `dos-griefing`
   - Unbounded loops
   - Forced revert vectors

7. `unsafe-external-call`
   - unchecked call return
   - untrusted delegatecall target

## Mapping Notes

- If source severity is unknown, default to `UNKNOWN` and avoid over-claiming risk.
- Keep original source text in report for traceability.
- For agent-facing summaries, present no more than top-5 categories unless explicitly requested.
