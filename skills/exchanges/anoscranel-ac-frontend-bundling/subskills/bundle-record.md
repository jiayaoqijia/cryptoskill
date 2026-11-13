---
name: bundle-record
domain: software-engineering/bundle-record
trigger: "Writing down the output shape a build is required to keep."
anti_trigger: "Not for the build log itself, and not for release notes."
scope: "The written record of output shape and its budgets."
status: seedling
---

# Bundle record

## Standard

The bundle record states the entry points, the splitting boundaries, the budgets with their thresholds, and the exposure decisions that attach to the output. It exists because build output drifts silently: a dependency adds a side effect, a route grows a heavy component, an asset doubles — and none of it surfaces in review unless a budget fails or a user complains.

Its second purpose is continuity between the people who set the budgets and the people who hit them. A breach without a record produces an argument; a breach with a record produces a lookup. The record names the baseline each threshold came from and the approved way to change a threshold, which converts a size dispute into a dated decision.

Primary source: <https://web.dev/learn>.

## Decision rules

- Record entry points, eager chunks, and split boundaries with their triggers.
- Record every budget with its baseline, threshold, and warning band.
- Record the source-map exposure decision per environment.
- Record the asset naming scheme and cache-control classes.
- Record every threshold change with the date, the reason, and the approver.
- Review the record at each release where output size moved by more than the warning band.

## Procedure

1. Record the output shape: entries, chunks, split triggers.
2. Record budgets and baselines.
3. Record map exposure per environment.
4. Record naming and caching classes.
5. Append each change with date, reason, and approver.
6. Review on any breach or band-crossing and record the finding.

## Anti-patterns

- Thresholds recorded without the baseline that justified them.
- A record updated only when someone remembers.
- Output-shape decisions kept in a config file nobody reads.
- Map exposure decided differently in each deploy with no note.
- No review trigger, so drift accumulates below the failure line.

## Done checklist

- [ ] Output shape recorded.
- [ ] Budgets and baselines recorded.
- [ ] Map exposure recorded per environment.
- [ ] Naming and caching recorded.
- [ ] Change log kept with approver.
- [ ] Review trigger set on band-crossing.

The record should also carry the compression ratio per entry: a bundle that ships two hundred kilobytes of script may be sixty on the wire, and a budget stated in one measure while the alert computes the other produces arguments that the record was supposed to prevent. Naming both, plus the gzip level assumed, removes the ambiguity.

## Sources

- Performance budgets practice: <https://web.dev/learn>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- HTTP caching reference: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching>
