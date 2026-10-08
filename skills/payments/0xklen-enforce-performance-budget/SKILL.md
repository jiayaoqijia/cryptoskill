---
name: enforce-performance-budget
description: Use when perf regressions ship unnoticed. Encodes byte and timing budgets as config, wires them into CI, and fails the build on breach.
---

# Enforce Performance Budget

A budget nobody can breach by accident is worth ten dashboards. Encode the limits as files that CI reads and that fail the pull request.

## Procedure

1. Write the bundle budget with `size-limit`, which measures the built artifact:

       // .size-limit.json
       [{"path":"dist/assets/*.js","limit":"170 kB","gzip":true},
        {"path":"dist/assets/*.css","limit":"24 kB","gzip":true}]

2. Run it locally and read the numbers it prints per file:

       npx size-limit

3. Write the timing budget into `lighthouserc.json` using assertions, averaging runs to damp noise:

       {"ci":{"collect":{"numberOfRuns":3,"url":["https://staging.shop.example.com/"]},
        "assert":{"assertions":{"largest-contentful-paint":["error",{"maxNumericValue":2500}],
        "total-blocking-time":["error",{"maxNumericValue":200}]}}}}

4. Gate the PR in CI so a breach is a red check, not a comment:

       npx size-limit && npx @lhci/cli autorun

5. Set the number from the current p75 plus headroom, not from an aspirational target nobody meets; a budget you routinely override trains the team to ignore it.
6. Ratchet: when a metric improves, lower the limit in the same commit so the win cannot slide back.

## Pitfalls

- Budgeting only bytes and ignoring INP/LCP, so a small bundle with a slow main thread still passes.
- Averaging a single Lighthouse run; variance between runs is easily 10-15% and turns the gate into flaky noise.
- Gating on the whole Lighthouse performance score, a weighted composite that moves for reasons unrelated to your diff.
- Setting a limit so loose it never fires, which is worse than no budget because it looks like coverage.
- Measuring source files instead of the built, gzipped artifact that actually ships.

## Verification

    npx size-limit --json | jq '.[] | {name, size, passed}'

Every entry must report `passed: true`. Report the limit, the measured size, and the CI job that enforces it.
