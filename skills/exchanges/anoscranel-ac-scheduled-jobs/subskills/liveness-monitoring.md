---
name: liveness-monitoring
domain: software-engineering/liveness-monitoring
trigger: "Detecting a scheduled job that stopped running without any error."
anti_trigger: "Not for the job's internal metrics (that is ac-reliability's observability)."
scope: "Detecting a job that stopped without erroring — dead-man's-switch design."
status: seedling
---

# Liveness monitoring

## Standard

A request-driven system fails loudly: users complain and errors surface. A scheduled job fails silently: it is removed by mistake, its trigger never fires after a migration, the node it lives on was decommissioned — and nothing errors. The only signal is an absence: the data is stale, and nobody notices until a dashboard looks wrong. Liveness monitoring is the dead-man's switch that turns that absence into an alert.

The design pattern is simple: each run heartbeats an observable signal — a metric incremented, a row updated, a key touched — and a separate monitor checks that signal's freshness against the job's interval. The critical property is independence: the monitor must not depend on the scheduler's own report of "the job ran", because the failure modes that silence the job often silence that report too.

## Decision rules

- Every job must emit a heartbeat on each successful run, in a form an external check can read.
- The monitor that checks heartbeat freshness must live outside the scheduler's own state.
- Alert on the combination "no heartbeat AND heartbeat expected by now".
- Distinguish never-ran from failed-ran: a row with an error is a different signal from no row.
- Include expected-run time in the job's definition so the check knows when to expect freshness.
- Test the dead-man's switch by stopping the job and confirming the alert fires.

## Procedure

1. Define the heartbeat signal per job — metric, row, or key — and emit it on each run.
2. Record expected run times in the schedule definition.
3. Build or configure the freshness check against the heartbeat.
4. Alert on the absence, with the job and the last successful run in the message.
5. Distinguish stoppage from failure in the alert text.
6. Test with a deliberately stopped job.

## Anti-patterns

- Trusting the scheduler's "last run" field, which is written by the same system that failed.
- Heartbeat written before the work instead of after it.
- An alert for the heartbeat that names the monitor, not the job.
- Bundle-of-jobs checks that hide which one stopped.
- Never testing the switch.

## Done checklist

- [ ] Heartbeat signal defined and emitted after work.
- [ ] Expected times in the definition.
- [ ] Independent freshness check live.
- [ ] Stoppage alert fires and names the job.
- [ ] Stoppage distinguished from failure.
- [ ] Switch tested with a stopped job.

## Sources

- Dead-man's switch monitoring: <https://sre.google/sre-book/monitoring-distributed-systems/>
- Health probes and liveness patterns: <https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/>
- Alert design principles: <https://learn.microsoft.com/en-us/azure/well-architected/>
