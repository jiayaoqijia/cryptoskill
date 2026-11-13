---
name: recall-discipline
domain: prompt-engineering/recall-discipline
trigger: "Reading memory before acting, and trusting it at the right level."
anti_trigger: "Not for building the index, and not for writing notes."
scope: "Reading memory before acting, matching query to note, and trust calibration."
status: seedling
---

# Recall discipline

## Standard

Memory that is never consulted is a diary; the recall habit is the memory's point. Before starting work on a familiar topic, the agent searches its own memory for what it already knows — the search-first habit that costs seconds and prevents the re-derivation of what was learned last time. The query borrows the note's title vocabulary: a well-titled corpus makes recall a match, not an archaeology.

Trust is the calibrated half. A recalled note earns exactly as much confidence as its provenance permits: a verified primary-source fact stands until contradicted; an inference stands as an inference; a note carried as provisional stays provisional until a session promotes it. Recalled memory is read as evidence about the past, not as a command about the present — the fact made sense when written, and the recall checks whether the world it described still exists.

Primary sources: <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents> and <https://en.wikipedia.org/wiki/Knowledge_management>.

## Decision rules

- Search memory before re-deriving anything on a familiar topic.
- Match the query to the title vocabulary; retry with synonyms before concluding absence.
- Calibrate trust to the note's provenance: primary, verified, inference, or provisional.
- Check whether a recalled fact still applies before acting on it.
- An absence of recall is recorded as absence, not as a negative fact.
- Record where a recalled claim entered the working context, so later output can cite it.

## Procedure

1. Before the substantive work, query memory with the topic's key terms.
2. Read the strongest matches; note provenance and dates.
3. Retry the search with phrasing variations before concluding the memory is absent.
4. Weigh the recalled facts against the present situation.
5. Act with the recalled context attached, citing the notes used.
6. Record the recall absence if a topic one would expect known was not found.

## Anti-patterns

- Deriving from scratch on a familiar topic without checking memory first.
- Treating every recalled note as current fact without reading its date or provenance.
- Trusting recall so much that contradicting present evidence is ignored.
- One query with no synonym retries before giving up.
- Treating the absence of a recall as confirmation the fact is false.

## Done checklist

- [ ] Memory searched before re-derivation.
- [ ] Synonym retries made before concluding absence.
- [ ] Provenance-checked readings of matches.
- [ ] Dates read before acting.
- [ ] Recalled context attached to output.
- [ ] Recall absences recorded.

## Sources

- Context engineering for agents: <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- Knowledge retrieval practice: <https://en.wikipedia.org/wiki/Knowledge_management>
- Durable note practice: <https://en.wikipedia.org/wiki/Commonplace_book>
