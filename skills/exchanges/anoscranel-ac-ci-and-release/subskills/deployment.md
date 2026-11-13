---
name: deployment
domain: software-engineering/deployment
trigger: "\"Deploy safely\", \"set up a canary\", \"blue-green deploy\", \"roll back the release\", \"add post-deploy checks\", \"GitOps with Argo CD\"."
anti_trigger: "Exposure switches after deploy (subskills/feature-flags.md); version cut and launch checklist (subskills/release-launch.md); infrastructure and containers (subskills/environments-config.md); live schema changes."
scope: "Progressive delivery: canary, blue-green, health gates, rollback"
status: "seedling"
---

# Deployment

## Standard

- **Techniques**: canary (shift a small share of traffic, compare, ramp), blue-green (two identical environments, router flip), rings (inner users outward), dark launch (code live but unreachable).
- **Verification stages**: smoke (0–2 min), canary analysis (5–30 min), business metrics, synthetic checks. ⚠️ Practitioner sources.
- **GitOps** (OpenGitOps, CNCF): declarative, versioned, pulled automatically, reconciled continuously; Argo CD, Flux (https://opengitops.org).
- **Rollback doctrine**: prefer flag-off or forward-fix over binary rollback; an untested rollback fails twice.
- **DORA**: change lead time, deployment frequency, failed deployment recovery time, change fail rate, deployment rework rate. Read as a set; they are gameable (https://dora.dev/guides/dora-metrics/).

## Decision rules

1. Production deploy is **human-gated**: a human approves or triggers it, or approves the automated policy that does.
2. Deploy the exact artifact CI built and tested, by digest.
3. Default to canary. Use blue-green when you need instant full switch-back and can afford two environments.
4. Canary ramp: 1–5% → bake → 25% → 50% → 100%. ⚠️ Steps and bake time are house defaults; size them to traffic volume.
5. Trip the canary when its error rate exceeds 2× baseline for N intervals, or p99 latency regresses past budget. ⚠️ Practitioner threshold.
6. Any tripped gate → automatic rollback, then page a human.
7. Schema changes deploy expand-first, so old and new code both run (out of scope for this leaf: the migration mechanics).
8. Rehearse rollback in staging before you rely on it.
9. Freeze deploys during an active incident unless the deploy is the fix.

## Procedure

1. Pre-deploy: CI green, artifact digest recorded, migration plan checked, rollback note written.
2. Deploy to staging. Run smoke tests: health endpoint 200, login, the core flow, migration applied.
3. Get human approval for production.
4. Start the canary. Argo Rollouts example:
   ```yaml
   strategy:
     canary:
       steps:
         - setWeight: 5
         - pause: { duration: 10m }
         - analysis: { templates: [{ templateName: error-rate }] }
         - setWeight: 50
         - pause: { duration: 10m }
   ```
5. Compare canary against baseline: error rate, p99 latency, saturation, one business metric.
6. Pass → ramp to 100%. Fail → roll back:
   ```bash
   kubectl argo rollouts abort <app>      # or: kubectl rollout undo deploy/<app>
   ```
7. Post-deploy: synthetic checks run; watch dashboards for the bake window.
8. Record the deploy: version, time, approver, result. Feed DORA metrics.

## Anti-patterns

- Rebuilding for production instead of promoting the tested artifact.
- Big-bang deploy to 100% with no bake.
- Rollback path never exercised.
- Contract-first schema change in the same deploy as the code.
- Agent self-approving a production deploy.
- No post-deploy verification.

## Done checklist

- [ ] Tested artifact deployed by digest.
- [ ] Human approval recorded.
- [ ] Smoke and canary gates passed with metrics compared.
- [ ] Rollback path rehearsed and documented.
- [ ] Deploy logged for DORA metrics.

## Sources

- <https://launchdarkly.com/blog/what-are-feature-flags>
- <https://www.ainformat.com/detail/2777>
- https://dora.dev/guides/dora-metrics/ · https://opengitops.org · https://argoproj.github.io/argo-rollouts/
