---
name: pin-model-snapshots-and-canary-upgrades
description: Use when a provider ships a new model version or alias. Pin the dated snapshot in production, canary the upgrade on real traffic, and keep a rollback to the last-known-good model.
---

# Pin model snapshots and canary upgrades

`gpt-4o-latest` is a moving target; last Tuesday's prompt behaviour is not guaranteed today. Pin an immutable snapshot and treat a model change as a deploy.

## Procedure

1. In production config, name the dated snapshot, never the floating alias: `gpt-4o-2024-08-06`, `claude-3-5-sonnet-20241022`. An alias silently resolves to something new.

2. Record the pinned snapshot plus the prompt version and eval scores as one release artefact, so you can state exactly what you shipped.

3. When the provider announces a new snapshot, run your golden eval set against old and new side by side before any traffic moves.

4. Canary: send 5-10% of real traffic to the new snapshot and watch task-level metrics — accuracy, schema-fail rate, refusal rate, latency — not just provider status.

5. Promote only when the new snapshot meets or beats the old on your bar; hold if any metric regresses beyond noise.

6. Keep the previous snapshot reachable for a fast rollback — one config flag, not a code revert.

7. Set a calendar reminder for snapshot deprecation; a retired snapshot breaks production without a code change.

8. Keep an allow-list of snapshots your code accepts (`VALID = {"gpt-4o-2024-08-06", ...}`) and reject an unknown model id at startup rather than discovering it in production.

9. Record the canary result even when you do not promote; "tested the new snapshot and held" is evidence the next reviewer wants.

## Pitfalls

- Deploying a floating alias and getting a silent behaviour change at the provider's chosen moment.
- Testing the upgrade only on happy-path cases; new versions often regress on edge formats or refusals.
- Judging the canary on latency alone — a correct-but-slower and a faster-but-wronger model both need the accuracy metric.
- Losing the rollback path because the old snapshot was retired on the provider side.
- Treating an eval pass as permanent; scores drift as traffic and inputs change.
- Letting CI default to whatever `latest` resolves to now, so a green build ships an unpinned model.
- Rolling forward "since the new model is better" without a canary; a provider's claim is not your eval.
- Pinning in config but leaving the fine-tune or adapter unpinned; the base is stable and the layer is not.

## Verification

    grep -rnE 'model\s*=\s*"[a-z0-9.-]+-(latest)"' config/   # must return nothing in prod; all pinned with a date

Report: "prod pinned to gpt-4o-2024-08-06; canary of the 2024-11 snapshot on 8% traffic held accuracy but raised the JSON schema-fail rate (1.1% vs 0.2%) — not promoted; rollback flag points at the old snapshot."
