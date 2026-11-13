---
name: build-record
domain: software-engineering/build-record
trigger: "Writing the record of build health, cache behaviour, and known gaps."
anti_trigger: "Not for CI configuration, and not for dependency policy."
scope: "The written record: graph health, cache hit rate, and known gaps."
status: seedling
---

# Build record

## Standard

The build record states the graph's health, the cache's behaviour, the known declaration gaps, and the reproducibility status, with dates and versions. Its value is that build health degrades silently: a build that takes twenty minutes is normal after a year of small additions, and no single change looks like the cause.

The gaps section is what makes the record actionable. A target with an incomplete declaration, a generator that is not deterministic, and a cache key that omits a toolchain version are all facts that are invisible in a passing build and decisive in an intermittent failure. Recording them with owners converts a set of suspicions into a work list.

Primary sources: <https://bazel.build/> and <https://reproducible-builds.org/>.

## Decision rules

- The record states build duration, its trend, and the slowest targets.
- Cache hit rate is recorded alongside its scope and its known wrong-hit incidents.
- Declaration gaps are listed per target with an owner and a date.
- Reproducibility status is recorded, with the method used to verify it.
- The toolchain versions in use are recorded.
- Review triggers are dated: toolchain upgrade, new codegen, cache change, duration regression.

## Procedure

1. Record duration, trend, and the slowest targets.
2. Record cache hit rate, scope, and incidents.
3. List declaration gaps with owners.
4. Record reproducibility verification and its result.
5. Record toolchain versions.
6. Review at each trigger and re-record.

## Anti-patterns

- Recording build duration without the slowest targets.
- A hit rate quoted without its scope.
- Gaps listed without owners.
- Claiming reproducibility without a verification method.
- No trigger, so the record describes a toolchain that has been upgraded since.

## Done checklist

- [ ] Duration, trend, slowest targets recorded.
- [ ] Cache hit rate and incidents recorded.
- [ ] Gaps with owners recorded.
- [ ] Reproducibility verified and recorded.
- [ ] Toolchain versions recorded.
- [ ] Triggers dated.

The record's trend line is its quietest asset: build duration that rose from five to twenty minutes over a year did so through changes nobody would have approved as a package, and a recorded trend is the only artefact that makes the accumulation visible before it becomes a complaint.


The toolchain section is worth recording even when nothing has changed, because an upgrade is the event that invalidates every cached result and every reproducibility claim at once, and a record that predates one is a record about a build system that no longer runs.


## Sources

- Build system and cache documentation: <https://bazel.build/>
- Reproducible builds reference: <https://reproducible-builds.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
