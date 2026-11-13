---
name: staleness-and-review
domain: prompt-engineering/staleness-and-review
trigger: "Reviewing memory so old facts age out honestly instead of going wrong quietly."
anti_trigger: "Not for first-draft notes, and not for building stores."
scope: "Lifecycle states for facts, review cadences, and pruning."
status: seedling
---

# Staleness and review

## Standard

A fact's lifetime is set by what it describes. A stable configuration fact lives until the configuration changes; a dated figure lives until the counting period passes; a claim about the world lives until the world moves. Each note is labelled with its decay class at writing — evergreen, slow, fast, or point-in-time — because staleness is only detectable against an expectation of how long the fact was supposed to hold.

Review is the enforcement arm. On a stated cadence — per-domain, quarterly, or triggered by events — the memory is read against the world: does the fact still describe what it names? The review marks the note current, supersedes it, or archives it; a note left unmarked past its decay class is treated as stale on read, whatever its original confidence. Memory that is never reviewed is not a knowledge base — it is a museum of past beliefs.

Primary sources: <https://en.wikipedia.org/wiki/Knowledge_management> and <https://en.wikipedia.org/wiki/Spaced_repetition>.

## Decision rules

- Label each note with a decay class at write time.
- Set a review cadence per domain; the memory record holds the schedule.
- Treat unreviewed notes past their decay class as stale on read.
- Reviews mark notes current, superseded, or archived — never silently leave them.
- Facts tied to a version or a date carry that qualifier in their first sentence.
- Event-driven triggers (a change, a failure, a correction) override calendar review for the notes they touch.

## Procedure

1. Tag decay classes at write time: evergreen, slow, fast, point-in-time.
2. Set the per-domain review cadence in the memory record.
3. On review, sample the domain's notes test-first: check the world, then the note.
4. Mark each reviewed note: current, superseded, or archived, with a date.
5. Let event triggers pull affected notes forward for immediate review.
6. Track the review coverage in the memory record.

## Anti-patterns

- No decay class; every note read as if written yesterday.
- Review that only adds notes and never marks or archives any.
- A one-time review followed by years of silent accretion.
- Deleting a stale note instead of marking it; the deletion destroys the history.
- Reviewing by rereading notes only; the world must be checked too.

## Done checklist

- [ ] Decay classes tagged at write time.
- [ ] Per-domain review cadence set.
- [ ] Review runs check the world against the note.
- [ ] Marks recorded with dates.
- [ ] Event triggers wired to affected notes.
- [ ] Stale-on-read default applied past due notes.

## Sources

- Knowledge life-cycle and review: <https://en.wikipedia.org/wiki/Knowledge_management>
- Retention and review-spacing research: <https://en.wikipedia.org/wiki/Spaced_repetition>
- Improving-with-age documents: <https://www.gwern.net/About-This-Website>
