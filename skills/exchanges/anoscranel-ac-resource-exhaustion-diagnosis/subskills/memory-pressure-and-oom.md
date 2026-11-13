---
name: memory-pressure-and-oom
domain: software-engineering/memory-pressure-and-oom
trigger: "Diagnosing memory exhaustion and the kernel's out-of-memory kill."
anti_trigger: "Not for heap tuning of a specific runtime by vendor guide."
scope: "Heap curves, the kernel's kill decision, and reading the OOM record."
status: seedling
---

# Memory pressure and the OOM kill

## Standard

Memory exhaustion announces itself in one of three ways, and each says something different. A process may fail its own allocation with a null or an exception — that is the runtime's limit, set where it was set. A managed runtime may spend nearly all its time in garbage collection while the heap crawls toward its ceiling — the death spiral visible as GC time before any error appears. Or the kernel may kill the process outright — the page cache is not the same as free memory, and the out-of-memory killer selects a victim by its own scoring from the processes present.

The kernel kill is the one most often misread, because the process simply vanishes. The kernel writes its accounting before the kill, and that record names the victim, its score, and the memory state at the moment — but only into the system log, where it scrolls away unremarked. Reading production memory failures therefore begins with knowing where that record lands and capturing it before rotation takes it.

## Decision rules

- Determine which of the three failures occurred: runtime allocation error, GC spiral, or kernel kill.
- For a kernel kill, capture the kernel's record promptly — it names the victim and score.
- For a GC spiral, capture the GC time series before the death; the spiral is visible in advance.
- Record whether the process limit is set below the machine's memory deliberately, and by whom.
- For containerized runs, check the memory limit separately — the container limit can kill before the kernel does.
- Plot heap or resident usage across days; the shape decides leak versus growth-versus-limit.

## Procedure

1. Identify the failure class from the symptom and the process's disappearance or error.
2. Capture the kernel or container kill record with its name and score.
3. Pull the memory time series for the days before the failure.
4. Classify the curve: steady climb, sawtooth with rising floor, or single spike.
5. Record the applicable limit — runtime, container, or machine — and its setting source.
6. Record the verdict with the evidence attached.

## Anti-patterns

- Calling the kernel killer "a crash" and reading a stack trace that does not exist.
- Reading the page cache as free memory and concluding capacity was ample.
- Raising the machine's memory without finding whether the container limit killed first.
- Restoring the service without capturing the kernel log entry.
- Plotting only since the restart, which resets the leak's curve.

## Done checklist

- [ ] Failure class identified.
- [ ] Kernel or container record captured.
- [ ] Memory time series pulled.
- [ ] Curve classified.
- [ ] Applicable limit and its source recorded.
- [ ] Verdict tied to the evidence.

## Sources

- Out-of-memory killer accounting: <https://www.kernel.org/doc/html/latest/admin-guide/mm/>
- Container memory limits: <https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/>
- Linux memory reporting: <https://www.kernel.org/doc/html/latest/filesystems/proc.html>
