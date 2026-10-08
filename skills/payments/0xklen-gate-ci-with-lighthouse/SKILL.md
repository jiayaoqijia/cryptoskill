---
name: gate-ci-with-lighthouse
description: Use when regressions reach production unnoticed. Runs Lighthouse CI per pull request with assertions and a server for trend history.
---

# Gate CI with Lighthouse

A performance gate only works if it runs on every change, on a stable profile, with assertions tight enough to fail. That is Lighthouse CI, configured, not a dashboard nobody opens.

## Procedure

1. Install and configure assertions in `lighthouserc.json`, averaging three runs to damp variance:

       {"ci":{"collect":{"numberOfRuns":3,"url":["https://pr-123.staging.shop.example.com/"],
        "settings":{"preset":"perf","form-factor":"mobile"}},
        "assert":{"preset":"lighthouse:recommended",
          "assertions":{"largest-contentful-paint":["error",{"maxNumericValue":2500}]}},
        "upload":{"target":"temporary-public-storage"}}}

2. Run it locally against the preview URL before pushing the workflow:

       npx @lhci/cli autorun --config=lighthouserc.json

3. In CI, wait for the preview deploy to be ready, then run against that URL, not production.
4. Fail the job on `error`-level assertions; keep informational ones at `warn` so the check stays meaningful.
5. Upload results so the next PR can be compared against the branch baseline, not just absolute thresholds.
6. Re-baseline deliberately when a real design change moves the numbers, and say so in the PR.

## Pitfalls

- Running against production URLs, which change under you and make the check flaky and unreviewable.
- Asserting on the composite performance score, which swings with unrelated audits and blocks unrelated PRs.
- A single run per URL, where a 10-15% jitter turns the gate into coin flips.
- Never re-baselining, so a gate that once failed for a real reason is disabled to unblock a release.
- Testing the staging build with debug bundles, which measures a configuration no user ever sees.

## Verification

    npx @lhci/cli autorun --config=lighthouserc.json; echo "exit=$?"

A non-zero exit means at least one assertion failed. Report the URL tested, the run count, and which assertion gated the build.
