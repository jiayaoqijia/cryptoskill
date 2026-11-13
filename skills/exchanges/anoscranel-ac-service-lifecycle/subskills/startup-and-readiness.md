---
name: startup-and-readiness
domain: software-engineering/startup-and-readiness
trigger: "Making a service refuse traffic until it can actually serve."
anti_trigger: "Not for orchestrator tuning, and not for steady-state failover."
scope: "Startup ordering, readiness versus liveness, and refusing traffic until able."
status: seedling
---

# Startup and readiness

## Standard

Alive and ready are different claims. Liveness says the process runs; readiness says the process can serve traffic now. A service that is alive but not ready — still loading cache, still connecting to its database, still warming JIT and pools — must not receive requests, and the only reliable way to express that is a readiness signal the traffic layer obeys, plus a listener that does not open until the basic dependencies have resolved.

The startup sequence is an ordering problem. Load and validate configuration first: a misconfigured service should fail before it binds a port, not after it has accepted traffic. Then establish the minimum dependency set — the things without which no request can succeed. Then warm what benefits from warming, either in the background or under a bounded concurrent traffic ramp. A service that skips ordering races its own dependencies on every restart, and the race is lost precisely when a dependency is itself restarting.

Primary sources: <https://sre.google/> and <https://martinfowler.com/>.

## Decision rules

- Record the startup steps in order: config load, validation, minimum dependencies, then listener open.
- Record what "minimum dependencies" means: the set without which no request succeeds.
- Record the readiness condition as a checkable statement, not a fixed sleep.
- Record the warmup path: background warm, bounded ramp, or full-traffic-on-ready.
- A config validation failure must exit before the port binds.
- Record the behaviour when a minimum dependency is absent at startup.

## Procedure

1. List the startup steps and impose an order.
2. Define the minimum dependency set and its per-dependency failure behaviour.
3. Define the readiness condition as an explicit check.
4. Choose the warmup strategy and its bounds.
5. Move config validation ahead of port binding.
6. Test with each minimum dependency absent, one at a time.

## Anti-patterns

- A fixed startup sleep instead of a readiness condition.
- The port open before configuration is validated.
- Everything declared a startup dependency, so nothing starts until everything does.
- Warmup on the request path with no ramp, stampeding the cache on restart.
- A readiness check that ignores the database because it is "usually there".

## Done checklist

- [ ] Startup steps ordered and recorded.
- [ ] Minimum dependency set defined.
- [ ] Readiness condition checkable.
- [ ] Warmup strategy bounded.
- [ ] Config validates before the port binds.
- [ ] Absent-dependency test executed.

## Sources

- Service startup and health practice: <https://sre.google/>
- Deployment and release patterns: <https://martinfowler.com/>
- Distributed systems references: <https://www.distributed-systems.net/>
