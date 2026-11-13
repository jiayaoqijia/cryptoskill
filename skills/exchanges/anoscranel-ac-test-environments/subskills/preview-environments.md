---
name: preview-environments
domain: software-engineering/preview-environments
trigger: "Giving each change its own throwaway place to run."
anti_trigger: "Not for production deployment, and not for staging data strategy."
scope: "A throwaway environment per change, and its cost."
status: seedling
---

# Preview environments

## Standard

A preview environment is a disposable instance per change: the branch is deployed to its own isolated world — service, data, maybe a URL — and disposed of when the change merges or dies. What it buys is integrity: the change is tested against the world it will actually join, and it cannot interfere with any other change being tested at the same time, because no two share anything.

The cost is the reason to design deliberately. Each preview carries the full footprint of a running system, which on a large application is expensive to create and expensive to leave running; environments that leak — created per branch and never destroyed — quietly become the largest line in the infrastructure bill. The design decisions are what to include (whole system, or only the changed service with stubs beside it), what data to seed, and what destroys the environment and when.

Primary source: <https://martinfowler.com/>.

## Decision rules

- Record what the preview contains: full stack, changed services only, or service plus stubs.
- Record the seed data policy and how the preview gets realistic state.
- Record the lifecycle: creation trigger, retention period, automatic destruction.
- Verify that teardown actually destroys data volumes, not just compute.
- Measure the concurrent-preview ceiling and set a cap with queueing, not failure.
- Record who pays for idle previews, since idle previews are the whole cost.

## Procedure

1. Choose the preview's scope and justify it against the application's size.
2. Define the seed policy: full copy, synthetic, or masked subset.
3. Wire creation and automated teardown with the retention period stated.
4. Test teardown on a real idle preview and verify volumes are gone.
5. Simulate the concurrent ceiling and set the cap.
6. Record the scope, the lifecycle, and the measured cost per preview-day.

## Anti-patterns

- Previews that only the pipeline can create and nothing destroys.
- Full-stack previews for a one-service change.
- Production data copied into previews unmasked.
- Teardown deleting compute and orphaning volumes.
- No idle cost accounting, so previews run for months.

## Done checklist

- [ ] Scope chosen and justified.
- [ ] Seed policy defined.
- [ ] Lifecycle and retention recorded.
- [ ] Teardown verified to destroy data.
- [ ] Concurrency cap set.
- [ ] Cost per preview-day measured.

The scope decision interacts with the seed policy in a way worth recording: a changed-service-with-stubs preview needs synthetic data whose shapes the stubs agree to produce, and a full-stack preview can carry masked realism, so the two decisions are one decision made in two places and should be made together.

## Sources

- Continuous delivery environments: <https://martinfowler.com/articles/continuousIntegration.html>
- Deployment practice: <https://martinfowler.com/bliki/DeploymentPipeline.html>
- Container lifecycle: <https://docs.docker.com/>
