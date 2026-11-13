---
name: service-catalogue
domain: software-engineering/service-catalogue
trigger: "Building a catalogue of services that people actually consult."
anti_trigger: "Not for asset inventory compliance, and not for API documentation."
scope: "Ownership metadata, dependencies, and what the catalogue must contain to be used."
status: seedling
---

# Service catalogue

## Standard

A catalogue is only useful if it answers a question someone is asking at the moment they ask it. The questions that recur are: who owns this, what depends on it, where does it run, and how do I reach the owner at three in the morning. A catalogue that lists names and descriptions answers none of them and is therefore not consulted.

Ownership is the field that carries the weight, and it must be a team rather than a person, with an escalation route. Dependencies matter because they answer the blast-radius question during an incident. Runtime location matters because it is the first thing asked when something is unreachable. The catalogue's content should be derived from these questions rather than from what is easy to collect.

Primary sources: <https://sre.google/> and <https://csrc.nist.gov/>.

## Decision rules

- Record the owning team and the escalation route for each service.
- Record the dependencies in both directions, since the upstream question is asked more often than the downstream one.
- Record the runtime environment and region, which answers the reachability question.
- Record the runbook location and whether it is current.
- Record how the metadata is maintained, since a stale catalogue stops being consulted.
- Record whether the data is generated from the repository or entered by hand, since generated data stays current.

## Procedure

1. List the questions the catalogue must answer, from actual incidents.
2. Map each to a field and a source.
3. Record ownership and escalation per service.
4. Record dependencies in both directions.
5. Record the maintenance mechanism, preferring generation over entry.
6. Write the catalogue specification with its questions.

## Anti-patterns

- A catalogue of names and descriptions with no ownership.
- Owner recorded as an individual who may have left.
- Dependencies recorded only downstream, which does not answer the impact question.
- Hand-maintained metadata that decays within a quarter.
- A catalogue with no stated question it exists to answer.

## Done checklist

- [ ] Questions recorded from real incidents.
- [ ] Fields mapped to sources.
- [ ] Ownership and escalation recorded.
- [ ] Bidirectional dependencies recorded.
- [ ] Maintenance mechanism recorded.
- [ ] Specification written.

The catalogue's most-used field during an incident is rarely the one the platform team expects: it is usually whoever to contact, and a catalogue whose ownership field is stale is worse than no catalogue because it sends people to the wrong team with confidence.


## Sources

- Service ownership and reliability practice: <https://sre.google/>
- Security and asset inventory guidance: <https://csrc.nist.gov/>
- Incident management context: <https://sre.google/workbook/table-of-contents/>
