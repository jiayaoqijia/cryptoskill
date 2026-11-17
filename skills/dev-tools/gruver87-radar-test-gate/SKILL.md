---
name: radar-test-gate
description: >-
  Run and interpret DUP Market Radar test_all / go_ready / CI gates. Use when
  debugging red CI, pytest isolation, or asking what green means before ops.
license: MIT
compatibility: Windows PowerShell; dup-market-radar with scripts/test_all.ps1 and go_ready.ps1.
metadata:
  author: dup-labs
  version: "0.1.6"
  product: dup-market-radar
---

# Radar test gate

## When to Use

- CI red, local pytest fails, «прогони тесты»

## Commands

```powershell
cd <path>\dup-market-radar
.\scripts\test_all.ps1 -SkipBuild   # or full with native build
.\scripts\go_ready.ps1 -SkipBuild
```

## What to watch

1. Pytest must isolate dotenv (`RADAR_DISABLE_DOTENV`) so live `.env` keys do not 401 lab clients.
2. Native prefer flags under `RADAR_NATIVE_*=0` must not resurrect True in live-money tests.
3. Ruff clean on touched Python.
4. `go_ready` PASS ≠ 48h soak.

## Output honesty

Report the **actual** exit codes and last failing test node id. Do not claim mesh L1 gate from radar pytest.

## Refuse

- Declaring ops-ready from unit tests alone.
- Skipping dotenv isolation “fixes” that re-break CI.
