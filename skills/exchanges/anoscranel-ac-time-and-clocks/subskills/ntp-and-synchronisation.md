---
name: ntp-and-synchronisation
domain: software-engineering/ntp-and-synchronisation
trigger: "Understanding what time synchronisation fixes and what it does not."
anti_trigger: "Not for choosing an NTP vendor product."
scope: "What NTP does and does not fix, and its own failure modes."
status: seedling
---

# NTP and synchronisation

## Standard

A synchronisation protocol like NTP keeps a host's clock close to a reference, by small gradual corrections where possible and by hard steps where the drift is large. The important word is "close": after synchronisation the clock is accurate within a bounded error, never exact, and a host that has lost its synchronisation source silently keeps its own time — drifting further with every day and reporting no error while it does.

Two failure modes deserve design attention. The step correction: when the daemon corrects a large offset at once, processes reading the wall clock see time jump, which is precisely the event the monotonic rule protects durations from. The silent divergence: a misconfigured or unreachable source leaves the clock free-running, so any trust placed in that host's timestamps decays over days. Both argue for monitoring the synchronisation state itself, not just the clock value.

## Decision rules

- Record which synchronisation sources each class of host uses.
- Monitor synchronisation state — stratum, offset, reachability — not merely the time value.
- Alert when a host loses its source or its offset exceeds tolerance.
- Prefer gradual correction (slewing) over stepping where the configuration allows the choice.
- Do not compute durations from the wall clock on any host, synchronised or not.
- Re-verify configuration after image or node changes, since defaults drift with rebuilds.

## Procedure

1. Inventory the time sources used by production hosts.
2. Check the current synchronisation status on a sample of hosts.
3. Add or verify monitoring of synchronisation state and offset.
4. Configure alerting on lost source and excess offset.
5. Confirm correction behaviour — slew versus step — in the configuration.
6. Record sources and behaviour in the time policy record.

## Anti-patterns

- Trusting a clock because "NTP is installed", without monitoring its state.
- Reading wall-clock time to measure a duration on a host that steps.
- One time source for everything, including its own failure mode.
- Rebuilding images and inheriting a default synchronisation configuration silently.
- No alert when the source becomes unreachable.

## Done checklist

- [ ] Sources inventoried.
- [ ] Synchronisation state monitored.
- [ ] Offset alerting live.
- [ ] Correction mode known and recorded.
- [ ] Sample of hosts verified.
- [ ] Policy updated with sources and behaviour.

## Sources

- NTP protocol and behaviour: <https://www.rfc-editor.org/rfc/rfc5905>
- Operational timekeeping guidance: <https://www.nist.gov/pml/time-and-frequency-division/>
- Linux time synchronisation services: <https://www.kernel.org/doc/html/latest/>
