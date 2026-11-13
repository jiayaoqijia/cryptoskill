---
name: health-endpoints
domain: software-engineering/health-endpoints
trigger: "Designing health checks that tell the truth."
anti_trigger: "Not for monitoring dashboards, and not for orchestrator tuning."
scope: "Liveness, readiness, and what each check should actually verify."
status: seedling
---

# Health endpoints

## Standard

A health endpoint answers a question, and the question differs by asker. Liveness asks: is this process wedged beyond recovery? The answer justifies a restart, so it must check almost nothing — a wedged process must fail it, and everything else must pass it. Readiness asks: can this instance serve traffic right now? It may check dependencies, cache temperature, and quota headroom, because the consequence of failing is only removal from the load balancer, which is recoverable by the process itself.

The recurring error is depth confusion: a liveness check that queries the database converts a dependency blip into a restart loop, killing every instance in a fleet because one database slowed. The rule is: liveness checks the process, readiness checks the ability to serve, and anything whose failure should not withdraw an instance belongs in monitoring, not in a health endpoint at all.

Primary sources: <https://sre.google/> and <https://kubernetes.io/>.

## Decision rules

- Record each endpoint, its purpose, and the action taken on failure.
- Liveness checks process health only: event loop responsive, not deadlocked.
- Readiness checks serving ability: dependencies reachable, warmup complete, quota present.
- Record what readiness deliberately does not check, to prevent depth creep.
- Record the check timeout: a health check slower than the prober is a false negative.
- Health checks do not cause side effects, allocate heavily, or mutate state.

## Procedure

1. Define liveness and its failure action (restart) and keep its checks minimal.
2. Define readiness and its failure action (withdraw traffic).
3. List what readiness checks and, equally, what it does not.
4. Set check timeouts below the prober's own timeout.
5. Add a startup phase distinction if the runtime supports it.
6. Verify: kill each dependency one at a time and confirm the endpoint and action behaviour.

## Anti-patterns

- Liveness that queries the database, restarting the fleet on a dependency blip.
- One "health" endpoint for both questions.
- A readiness check so slow it fails its own prober.
- Health checks that write logs or mutate state on every probe.
- Checks that only verify the port is bound, proving nothing about serving.

## Done checklist

- [ ] Liveness and readiness separated.
- [ ] Failure action per endpoint recorded.
- [ ] Readiness exclusion list written.
- [ ] Check timeouts set.
- [ ] Startup phase handled.
- [ ] Dependency-kill verification executed.

## Sources

- Health check practice: <https://sre.google/>
- Probe semantics: <https://kubernetes.io/>
- Service patterns: <https://martinfowler.com/>
