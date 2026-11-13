---
name: ci-pipeline
domain: software-engineering/ci-pipeline
trigger: "\"Set up CI\", \"add a GitHub Actions workflow\", \"speed up the pipeline\", \"which checks should be required\", \"cache dependencies in CI\", \"pin our actions\"."
anti_trigger: "A red pipeline to triage; rollout to production (subskills/deployment.md); branch protection and merge queues; which tests to run."
scope: "Pipeline-as-code, gate order, caching, required checks"
status: "seedling"
---

# CI Pipeline

## Standard

- **Deployment pipeline** (Humble & Farley, *Continuous Delivery*, 2010): commit stage → automated acceptance → manual or exploratory → release. Every commit leaves main releasable.
- **Stages for a small team**: `lint → test → build → deploy → verify`, one linear chain.
- **Build once**: build one artifact, pass it by digest between jobs; never rebuild per job.
- **Hardening** after real incidents (tj-actions, CVE-2025-30066): pin actions to a full commit SHA; default `permissions: contents: read`; never `pull_request_target` with an untrusted checkout; namespace caches per trigger.
- **Cloud auth** from CI uses short-lived OIDC tokens, not stored long-lived keys.

## Decision rules

1. Pipeline lives in the repo as code, reviewed like code.
2. Order gates cheap and fast first: format and lint → typecheck → unit → build → integration → security scans → e2e smoke.
3. Required checks on main: every pre-merge gate. A red check blocks merge.
4. Pre-merge wall time about 10 minutes. ⚠️ House budget. Over it → cache, parallelise, shard, or move slow jobs to post-merge.
5. Cache dependency directories keyed on the lockfile hash. Never restore a pull-request cache in a release job.
6. Cancel stale runs on the same branch.
7. Matrix only for supported OS and runtime versions. Cap its size.
8. Secrets: least privilege, masked, never echoed. A leaked secret is rotated; rotation is **human-gated**.
9. Retries in CI: test retries capped at 2 and reported as flaky.

## Procedure

1. Write the workflow:
   ```yaml
   name: ci
   on: { pull_request: {}, push: { branches: [main] } }
   permissions: { contents: read }
   concurrency:
     group: ci-${{ github.ref }}
     cancel-in-progress: true
   jobs:
     check:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@<full-sha>   # pin by SHA
           with: { persist-credentials: false }
         - uses: actions/setup-node@<full-sha>
           with: { node-version: 22, cache: npm }
         - run: npm ci
         - run: npm run lint && npm run typecheck
         - run: npm test -- --coverage
         - run: npm run build
         - uses: actions/upload-artifact@<full-sha>
           with: { name: dist, path: dist }
   ```
2. Add later jobs that download the same artifact; they never rebuild.
3. Turn on required status checks for main in branch protection.
4. Measure p50 and p95 pipeline time, slowest jobs, cache hit rate, flake rate.
5. Speed up in order: cache → parallel jobs → shard tests → move slow suites to post-merge or nightly.
6. Add dependency update automation (Dependabot or Renovate) and an action-pinning check.
7. Review monthly against the time budget.

## Anti-patterns

- Mutable tags (`@v4`, `@main`) on third-party actions.
- Rebuilding the artifact in every job.
- One cache shared by PR and release workflows.
- Long-lived cloud keys in repo secrets.
- Branching logic in YAML instead of scripts.

## Done checklist

- [ ] Workflow in repo; actions pinned by SHA.
- [ ] Least-privilege permissions; no untrusted `pull_request_target`.
- [ ] Gates ordered cheap first; required on main.
- [ ] One artifact built and passed on.
- [ ] Pre-merge time within budget; stale runs cancelled.

## Sources

- <https://www.informit.com/store/continuous-delivery-reliable-software-releases-through-9780321670229>
- <https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction>
- https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions
