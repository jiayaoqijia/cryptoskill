---
name: memory-record
domain: prompt-engineering/memory-record
trigger: "Writing the inventory of what the agent remembers and how it is maintained."
anti_trigger: "Not for the notes themselves, and not for the search layer."
scope: "The inventory of what is remembered, reviewed on a cadence."
status: seedling
---

# Memory record

## Standard

The memory record is the memory's own map: what domains are covered, how many notes in each, the review cadence and the last review date, the export cadence and the last export, the supersession history, and the recall absences that surprised a session. It is one page, and it exists so that a new session can answer "what do I know?" without a full corpus read.

The record also holds the policies: the promote rule, the decay classes, the trust vocabulary, the format contract. These are the memory's constitution — written down, versioned, and changed deliberately. A session that invents its own note style memory cannot be found; a session that invents its own trust rule recalls wrongly with confidence.

Primary sources: <https://en.wikipedia.org/wiki/Knowledge_management> and <https://osf.io/prereg/>.

## Decision rules

- The record states domains covered, note counts, and counts by provenance class.
- The promote rule, decay classes, trust vocabulary, and format contract are stated, versioned.
- Review cadences and last-review-dates per domain are recorded.
- Export cadence and last-restore-check date recorded.
- Supersession history and recall absences recorded as they occur.
- The record is stored where a session reads it before its first memory search.

## Procedure

1. Write the policy sections: promote rule, decay classes, trust vocabulary, format contract.
2. Inventory the domains and their note counts.
3. Record the review and export cadences with their last-run dates.
4. Log supersessions and recall absences as they occur, dated.
5. Read the record at session start before the first memory search.
6. Amend, never overwrite; the record's own history is part of the memory.

## Anti-patterns

- No record; each session rediscovers what the memory holds by brute search.
- Policies implied but unwritten, so each session improvises.
- A record updated only when memory is built, never when reviewed.
- Overwriting the record rather than amending it.
- Keeping the record where no session reads it.

## Done checklist

- [ ] Policy sections written and versioned.
- [ ] Domain inventory with counts.
- [ ] Review cadence and last-review date recorded.
- [ ] Export cadence and restore-check date recorded.
- [ ] Supersessions and absences logged dated.
- [ ] Record read before first search each session.

A record with these fields also settles disputes cheaply: when a session disagrees with a recalled fact, the record's provenance and dates decide who must re-verify, rather than the louder of the two impressions winning by default.

## Sources

- Knowledge inventory and audit: <https://en.wikipedia.org/wiki/Knowledge_management>
- Pre-registration practice for stated policies: <https://osf.io/prereg/>
- Review discipline: <https://en.wikipedia.org/wiki/Spaced_repetition>
