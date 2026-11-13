---
name: ledger-and-leverage
domain: collaboration/ledger-and-leverage
trigger: "Tracking multi-agent operation costs, retries, and leverage ratios; enforcing human gates on irreversible acts"
anti_trigger: "Running autonomous multi-agent loops indefinitely with no cost tracking; automating irreversible actions without gates"
scope: "Running the loop: per-task cost and retry records; irreversible acts stay human-gated; sequential heavy jobs; leverage ratio measurement"
status: seedling
---

# Ledger and Leverage

## Standard

- **House multi-agent governance standard**: every multi-agent operation must maintain a structured ledger recording token costs, retry counts, interrupt events, and leverage ratios. ⚠️ House threshold.
- **Irreversible action invariant**: destructive operations, spending, releases, and permission changes remain strictly human-gated regardless of agent autonomy level or loop duration.
- **Heavy-job serialization rule**: heavy tasks (downloads, heavy parsing, build compilation, browser automation) must execute sequentially rather than in parallel to prevent system resource exhaustion. ⚠️ House threshold.

## Decision rules

1. Maintain an operation ledger recording agent dispatches, model tiers, retry counts, and estimated token costs for every multi-agent run.
2. Irreversible actions (file deletion, git pushes, credential exposure, financial transactions) must always pause for explicit human sign-off.
3. Never run more than one heavy resource-intensive job in parallel; queue heavy tasks sequentially.
4. Calculate operational leverage as displaced human time divided by supervisory time; if leverage drops below one, terminate the multi-agent loop.
5. Set a maximum iteration or retry ceiling for autonomous loops to prevent infinite agent runaways.
6. Record all failure signatures and repair actions in the ledger to inform future agent runs.

## Procedure

1. Initialize the operation ledger at the start of any multi-agent task.
2. Log each agent dispatch with timestamp, role, model tier, and expected deliverable.
3. Record retry events, failure classes, and recovery actions as they occur.
4. Enforce the heavy-job serial queue rule when scheduling resource-intensive tasks.
5. Pause execution at any human-gate boundary (irreversible acts) and await explicit operator confirmation.
6. Compute the final leverage ratio and total cost upon task completion, archiving the ledger in the session record.

## Anti-patterns

- **Unwatched autopilot.** Running multi-agent loops overnight with no iteration limits or cost tracking. Fix: set hard caps and ledgers.
- **Autonomous destruction.** Allowing an agent group to delete files or push code without human approval. Fix: enforce human gates.
- **Parallel resource starvation.** Launching five heavy data parsing agents at the same time, crashing system memory. Fix: serialize heavy jobs.
- **Phantom leverage.** Spending ten hours supervising agents to produce a two-hour task. Fix: measure and prune negative leverage.

## Done checklist

- [ ] Operation ledger initialized and updated.
- [ ] Irreversible actions protected by human gates.
- [ ] Heavy jobs serialized rather than parallelized.
- [ ] Iteration and retry ceilings enforced.
- [ ] Leverage ratio and total cost calculated at completion.

## Sources

- Internal operational standards for multi-agent ledgers, leverage measurement, and human safety gates.
- Architectural guidelines on resource serialization and autonomous run safety limits.
