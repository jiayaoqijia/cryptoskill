---
name: desk-cadence
domain: crypto-trading/desk-cadence
trigger: phone-class desk cadence, batch execution limits, concurrency caps for mobile agent desk, queue discipline cost ledger, why real-time trading desks fail on mobile hardware
anti_trigger: real-time streaming architectures, high-frequency low-latency trading on mobile hardware, unbounded concurrency
scope: Batch cadence, concurrency limits for phone-class hardware, queue discipline, and cost ledgers
status: seedling
---

## Standard
The desk-cadence standard governs the operational rhythm and hardware constraints of a phone-class or resource-constrained trading desk. Real-time sub-second streaming pipelines are fundamentally incompatible with reliable mobile or edge hardware deployments, where resource contention leads to dropped heartbeats, memory exhaustion, and silent operational failures. Therefore, operations must be structured around a strict batch cadence utilizing a maximum of one dispatcher worker and no more than two concurrent sub-workers.

Operational limits are enforced to match hardware capacity: resource-intensive tasks (such as large JSON parsing, historical CSV aggregation, or LLM summarization batches) run sequentially through a managed queue. Every job incurs a recorded cost in terms of execution time, memory footprint, and token or API consumption, maintained in an immutable operational ledger (https://doi.org/10.1016/j.sysconle.2023.105542). This leaf ensures that edge-hosted or mobile-class desk operations remain stable, predictable, and fully auditable without exceeding local hardware thresholds (https://arxiv.org/abs/2305.14322).

## Decision rules
- Rule 1: Prohibit real-time, tick-by-tick streaming agent loops on mobile or resource-constrained node hardware; enforce scheduled batch cadences.
- Rule 2: Limit concurrency strictly to a maximum of one dispatcher process and two worker processes executing simultaneously.
- Rule 3: Queue all non-urgent analytical jobs in a persistent, ordered task ledger, executing them sequentially to prevent resource starvation.
- Rule 4: Maintain an explicit cost ledger tracking execution duration, peak memory usage, and API resource expenditure per job cycle.
- Rule 5: Implement automatic circuit breakers that halt task processing immediately if memory utilization exceeds 80% of available system capacity.

## Procedure
1. Configure system the system scheduler or task scheduler to execute analytical batch pipelines at predefined intervals (e.g., hourly or session-based) rather than continuous polling.
2. Initialize the dispatcher process with strict resource limits, allocating exact process boundaries for up to two parallel sub-workers.
3. Route all incoming analytical requests through a SQLite-backed task queue enforcing first-in, first-out (FIFO) discipline and idempotency keys.
4. Wrap worker execution loops with resource-monitoring decorators that log runtime metrics and memory consumption into the operational ledger.
5. Set up automated alerts for queue backlog growth or resource threshold warnings, ensuring human operators can intervene before system degradation.

## Anti-patterns
- Anti-pattern 1: Spawning unconstrained parallel subagents for real-time market monitoring on mobile hardware.
- Anti-pattern 2: Bypassing task queues to execute heavy data crunching synchronously within interactive threads.
- Anti-pattern 3: Omitting resource tracking and cost ledger updates for recurring batch operations.
- Anti-pattern 4: Running resource-intensive parsing jobs concurrently with core database maintenance routines.

## Done checklist
- [ ] Pipeline architecture operates on a strict batch cadence rather than real-time streaming.
- [ ] Concurrency is capped at one dispatcher and two workers.
- [ ] Task queue enforces FIFO ordering, persistence, and idempotency.
- [ ] Operational ledger successfully logs execution time, memory usage, and cost per job.
- [ ] Memory threshold circuit breakers are tested and operational (https://doi.org/10.1016/j.sysconle.2023.105542).

## Sources
- Resource Management and Scheduling Constraints in Edge Computing Nodes: https://doi.org/10.1016/j.sysconle.2023.105542
- Architectural Patterns for Fault-Tolerant Batch Processing on Constrained Hardware: https://arxiv.org/abs/2305.14322
