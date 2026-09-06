---
name: flaky-test-detection
description: >
  Detect, prevent, and fix flaky Jest unit tests in MetaMask Mobile before they
  reach CI. Use this skill when: reviewing a PR diff or changed test files for
  flakiness risk, fixing an intermittently failing Jest test, reproducing a flaky
  test locally, or auditing GitHub Actions history to rank historically flaky unit
  tests by failure rate.
---

# Flaky Test Detection

```
Task → Which mode?
├─ Reviewing changed test files / PR diff for risk patterns  → Review mode
├─ Fixing a known flaky Jest unit test                       → Review mode + local reproduce loop
└─ Auditing CI history to rank flaky tests by failure rate   → open references/gh-analysis.md
```

## Constraints

All proposed fixes must comply with `mms-mobile-testing` (unit path) and `mms-coding-guidelines`. Key rules:
- Use `jest.mocked(fn)` — never `fn as jest.Mock`
- Use `toBeOnTheScreen()` — never `toBeTruthy()` / `toBeDefined()` for element presence
- Use `yarn` commands — never npm or npx
- No `toMatchSnapshot()` — use explicit assertions or `toMatchInlineSnapshot()`

## Review mode

1. Scan changed `.test.ts(x)` files against the pattern table (J1–J10).
2. Classify each hit (async / timing / isolation / mock / state).
3. Propose the fix for each hit using the ✅ pattern from the matching section — apply only on explicit confirmation.
4. Run the local reproduction loop to confirm the fix holds.

## Audit mode

Query GitHub Actions run history to produce a ranked list of historically flaky unit test files with failure rates and suggested fix categories.

Open [references/gh-analysis.md](references/gh-analysis.md) for the full procedure.
