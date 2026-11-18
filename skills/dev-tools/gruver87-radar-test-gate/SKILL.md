---
name: radar-test-gate
description: >-
  Run and interpret DUP Market Radar test_all / go_ready / verify profiles / CI
  gates. Use when debugging red CI, pytest isolation, or asking what green means
  before ops — never equate Quick/Full with 48h soak.
license: MIT
compatibility: Windows PowerShell; dup-market-radar with scripts/verify.ps1, test_all.ps1, go_ready.ps1.
metadata:
  author: dup-labs
  version: "0.1.10"
  product: dup-market-radar
---

# Radar test gate

## When to Use

- CI red, local pytest fails, «прогони тесты / verify»

## Commands

```powershell
cd <path>\dup-market-radar
.\scripts\verify.ps1 -Profile Quick      # gate + pytest + offline smoke — NO soak
.\scripts\verify.ps1 -Profile Full       # + warm/live evidence — still NO soak
.\scripts\test_all.ps1 -SkipBuild
.\scripts\go_ready.ps1 -SkipBuild        # ops-ready ≠ 48h
```

Do **not** start `Soak48h` / PreSoak short soak unless the operator explicitly ordered soak.

## What to watch

1. Pytest must isolate dotenv (`RADAR_DISABLE_DOTENV`) so live `.env` keys do not 401 lab clients.
2. Native prefer flags under `RADAR_NATIVE_*=0` must not resurrect True in live-money tests.
3. Ruff clean on touched Python.
4. `go_ready` PASS ≠ 48h soak. `verify Quick/Full` ≠ soak.

## Output honesty

Report the **actual** exit codes and last failing test node id. Do not claim mesh L1 gate from radar pytest.

## Refuse

- Declaring ops-ready from unit tests alone.
- Starting 48h soak from a casual “прогони тесты”.
- Skipping dotenv isolation “fixes” that re-break CI.
