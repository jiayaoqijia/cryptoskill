---
name: side-channels-and-limits
domain: software-engineering/side-channels-and-limits
trigger: "Understanding what the sandbox boundary does not cover."
anti_trigger: "Not for general threat modelling, and not for network security."
scope: "What the boundary does not cover: timing, resources, and speculative leakage."
status: seedling
---

# Side channels and limits

## Standard

The sandbox's guarantee is spatial: the guest cannot touch memory it was not given. It is not a guarantee about time, about resources, or about the host's own behaviour. A guest that measures how long a host function takes learns something about the host's state; a guest that allocates until the limit learns the limit; a guest that shares a host process with other tenants shares caches, branches, and scheduling with them.

The design responses are separation and accounting. Time-sensitive paths can be made constant-shape where they carry secrets; resource consumption is metered per guest and enforced with hard caps; tenants whose data must not correlate are placed in separate processes or separate machines, because no in-process sandbox isolates a shared cache. The honest position is that these are host responsibilities wearing sandbox assumptions, and a deployment that has not written them down has inherited the defaults silently.

Primary sources: <https://webassembly.github.io/spec/> and <https://www.brendangregg.com/linuxperf.html>.

## Decision rules

- Record which host functions carry secret-dependent branches or timings.
- Make secret-dependent host operations shape-constant where feasible; record what is not.
- Meter per-guest execution: fuel, memory, and wall time, each with a cap.
- Place tenants that must not correlate in separate processes or machines.
- Record the sharing model: what a guest shares with which other guests.
- Treat any new host import as a new channel surface; audit it with the import set.

## Procedure

1. List the resources a guest can consume and set caps for each.
2. Identify host functions that touch secrets, and their timing or branching patterns.
3. Apply shape-constant implementations where the risk justifies it.
4. Decide the placement policy for mutually sensitive tenants.
5. Record the sharing and resource model.
6. Re-audit on every import-set change.

## Anti-patterns

- Trusting the sandbox to contain timing or resource side effects.
- Unlimited fuel or memory per guest.
- Sensitive tenants in one process, justified by the instruction-set guarantee.
- Adding imports without re-auditing the channel surface.
- Leaving the sharing model undocumented.

## Done checklist

- [ ] Resource caps per guest set.
- [ ] Secret-dependent host paths identified.
- [ ] Shape-constant measures applied or justified.
- [ ] Tenant placement policy recorded.
- [ ] Sharing model documented.
- [ ] Channel audit on import-set changes.

Fuel metering has a further honest use beyond eviction: the consumed-fuel profile of a well-behaving guest is a baseline, and a sudden change in that profile without a workload change is a diagnostic signal visible to the host, which is one of the few observations a sandboxed boundary does support.

## Sources

- Execution model boundaries: <https://webassembly.github.io/spec/>
- System measurement and metering: <https://www.brendangregg.com/linuxperf.html>
- Sandbox concepts: <https://webassembly.org/specs/>
