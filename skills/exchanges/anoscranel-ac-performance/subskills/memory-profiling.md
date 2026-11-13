---
name: memory-profiling
domain: software-engineering/memory-profiling
trigger: "\"memory leak in production\", \"heap keeps growing\", \"OOM in prod\", \"allocation profile\"."
anti_trigger: "Exhaustion diagnosis curves and OOM kill records (ac-resource-exhaustion-diagnosis); GC tuning as a vendor exercise."
scope: "Allocation profiling and heap snapshots: finding what allocates, what retains, and what leaks."
status: "seedling"
---

# Memory profiling

## Standard

Memory profiling answers two different questions with two different tools. "What allocates?" — an allocation profile ranks creation sites, and it finds churn: the hot paths manufacturing garbage that the collector must then sweep. "What retains?" — a heap snapshot (or a diff of two) ranks what is still reachable, and it finds leaks: objects the program can still reach and never will again.

The leak-hunting method that works is the snapshot diff. Take a heap snapshot, wait or drive load, take another, and diff: a leak is a type whose count and size grow while the workload that creates it has ended. The single-snapshot approach fails because the biggest retained object is usually legitimate cache or state — the diff is what separates growth from size.

## Decision rules

1. Classify the symptom first: churn (GC pressure, pauses) → allocation profile; growth (rising floor) → snapshot diff.
2. An allocation profile ranks creation sites: fix the top makers before micro-managing small ones.
3. For a suspected leak: two snapshots with a known workload between them; diff by type.
4. A type that grows across the diff while its workload stopped is the leak; verify its retention path.
5. Long-lived allocation in a loop is the common shape: read the allocation site's scope.
6. In managed runtimes, a "leak" is usually an unintended reference: the retain path names the holder.

## Procedure

1. Classify: churn or growth (see ac-resource-exhaustion-diagnosis for the curve).
2. For churn: run an allocation profile under representative load; rank creation sites.
3. For growth: snapshot heap, drive one workload cycle, snapshot again.
4. Diff the snapshots by type; list the growers.
5. For each grower, trace the retention path to the holding reference.
6. Fix the holder, re-run the diff, and record the result.

## Anti-patterns

- Reading a single snapshot's largest objects as leak evidence.
- Optimising allocation sites that are not in the top rank of the profile.
- Assuming a managed runtime cannot leak: unintended references leak fine.
- Tuning the collector for a leak; that buys hours, not a fix.
- Profiling in a load-shape that never matches production.

## Done checklist

- [ ] Symptom classified churn versus growth.
- [ ] Correct tool run (allocation profile or snapshot diff).
- [ ] Creation sites ranked or growers listed.
- [ ] Retention path traced for each grower.
- [ ] Fix applied at the holder.
- [ ] Re-run diff confirms; result recorded.

## Sources

- JVM heap analysis tooling: <https://docs.oracle.com/en/java/javase/21/troubleshoot/>
- Memory profiling methodology: <https://learn.microsoft.com/en-us/visualstudio/>
- GC behaviour and allocation: <https://docs.oracle.com/en/java/javase/21/gctuning/>
