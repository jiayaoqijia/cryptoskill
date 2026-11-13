---
name: dependency-ordering
domain: software-engineering/dependency-ordering
trigger: "Starting against dependencies that are not ready."
anti_trigger: "Not for steady-state resilience alone, and not for orchestrator choice."
scope: "Starting against dependencies that are slow, absent, or flapping."
status: seedling
---

# Dependency ordering

## Standard

A service starts when it is told to start, and its dependencies start when they are told to start, and nothing guarantees the two orders agree. In practice every service must be able to boot into an environment where its database is still recovering, its cache is absent, and its downstream peers are mid-deploy. The startup code must therefore distinguish two questions: can I start at all, and what will I do about each dependency that is not yet there.

The distinction is per dependency. The minimum set — the dependencies without which no request can succeed — blocks readiness until reachable; a service that marks itself ready with an unreachable core dependency fails every request it receives, and the failure surfaces as customer error rather than as a delayed start. The enhancement set — cache, secondary stores, optional peers — should not block startup but should degrade the readiness report so the operator can see the truth while traffic waits elsewhere.

Primary sources: <https://sre.google/> and <https://martinfowler.com/>.

## Decision rules

- Split dependencies into minimum and enhancement, with the reason each is where it is.
- Minimum dependencies block readiness; enhancement dependencies are degraded-not-failed.
- A dependency that becomes unavailable after startup follows the steady-state plan, not the startup plan.
- Reconnect attempts during startup are bounded and logged.
- Waiting is visible: logs say which dependency is blocking readiness and for how long.
- Startup handles the "dependency flaps up and down" case, not only the "absent" case.

## Procedure

1. List all upstream and downstream dependencies.
2. Classify each as minimum or enhancement with a reason.
3. Write the readiness rule: block on minimum, degrade on enhancement.
4. Bound and log reconnect attempts.
5. Define the post-startup failure path per dependency.
6. Test with each dependency down at boot, and with one that flaps during boot.

## Anti-patterns

- Startup that loops forever on one absent dependency, blocking the whole deployment.
- Marking readiness with the database unreachable, then failing every request.
- Treating a flapping dependency as absent once and never rechecking.
- Startup ordering solved by a deployed sleep tuned to the slowest dependency.
- Waiting only checked into code, never tested against a genuinely slow environment.

## Done checklist

- [ ] Dependencies listed and classified.
- [ ] Readiness rule written.
- [ ] Reconnect bounded and logged.
- [ ] Post-startup failure path defined.
- [ ] Absent-dependency boot test executed.
- [ ] Flapping-dependency boot test executed.

## Sources

- Service initialisation practice: <https://sre.google/>
- Dependency patterns: <https://martinfowler.com/>
- Distributed systems references: <https://www.distributed-systems.net/>
