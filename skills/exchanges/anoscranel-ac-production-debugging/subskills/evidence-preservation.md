---
name: evidence-preservation
domain: software-engineering/evidence-preservation
trigger: "Capturing process state before a restart destroys it."
anti_trigger: "Not for postmortem writing (that is ac-reliability's incident response)."
scope: "Capturing state before a restart: dumps, thread lists, heap histograms, and configuration."
status: seedling
---

# Evidence preservation

## Standard

The first human instinct in an incident is to restart the service, and the restart destroys most of the evidence: thread states, heap contents, open connections, environment variables all disappear. Evidence preservation is the few minutes spent before the restart capturing what will be impossible to recover afterwards — and the discipline of deciding in one minute what to take, not deciding while panicking.

What to take follows a short checklist for each failure type. For a hang: a thread dump repeated a few seconds apart. For an out-of-memory signal: a heap histogram and the kernel's record of the kill. For a wrong result: request and response logs with the correlation ID. For a restart loop: the log tail and the exit codes. Everything should carry the timestamp and the host, because later analysis runs across machines.

## Decision rules

- Capture before restarting; a minute of capture is worth hours of guessing.
- Capture repeated thread dumps for hangs — a single snapshot shows a pose, two show movement.
- Record the exact exit status and signal pattern of any crash.
- Sanitise captures of credentials: thread dumps and environment snapshots can contain secrets.
- Label every capture with host, process, timestamp, and the trigger that prompted it.
- Verify the capture actually wrote: disk pressure and rotation can silently drop it.

## Procedure

1. Decide the failure class and its capture checklist.
2. Take the captures to local disk, checking each is written.
3. Record exit status, signal, and restart history.
4. Sanitise captures of secrets if they will be shared.
5. Label and timestamp everything.
6. Then restart, and note the exact time of the restart.

## Anti-patterns

- Restarting first because the pager is loud.
- Taking one thread dump where two would show movement.
- Storing captures in the default rotated-away directory.
- Sharing an unsanitised environment snapshot.
- No record of when the restart happened, losing the before/after boundary.

## Done checklist

- [ ] Capture checklist matched to the failure class.
- [ ] Captures verified written.
- [ ] Exit status and signals recorded.
- [ ] Captures sanitised.
- [ ] Labels with host, process, timestamp present.
- [ ] Restart time recorded.

For services running under an orchestrator, the capture target is also worth checking on its own terms: a pod's ephemeral filesystem disappears with the pod, so a capture must be copied off before any automatic restart, and a termination grace period measured in seconds has to cover the whole checklist.

## Sources

- Thread dumps and JVM hang analysis: <https://docs.oracle.com/en/java/javase/21/troubleshoot/>
- Linux out-of-memory killer records: <https://www.kernel.org/doc/html/latest/admin-guide/mm/consumer.html>
- Kubernetes crashLoopBackOff state: <https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/>
