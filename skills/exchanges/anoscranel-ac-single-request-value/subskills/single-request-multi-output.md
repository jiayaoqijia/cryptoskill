---
name: single-request-multi-output
domain: prompt-engineering/single-request-multi-output
trigger: "Designing one response to serve several deliverables by contract."
anti_trigger: "Not for parsing luck, and not for style alone."
scope: "One response structured into several deliverables by design, not parsing luck."
status: seedling
---

# Single-request multi-output

## Standard

When one body of work needs several artefacts — a summary, a risk list, a rewritten paragraph, a set of Titles — the request-hungry habit asks for each artefact separately. The single-request alternative fixes the outputs' order and form in the request itself, so one response arrives already divided: section one the summary, section two the risks, each under its own heading with its own stated length. The division is a contract written before the call, not a parse discovered after it.

The craft is in the specification. Each output needs its own form declaration — bullets or prose, its maximum length, its audience — and the outputs need an explicit order so that nothing in the response is ambiguous about where one artefact ends and the next begins. A multi-output request that specifies all this returns deliverables that need no rework; one that does not returns a wall of text that must be re-requested, spending the second request the design was meant to save.

Primary sources: <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering> and <https://12factor.net/>.

## Decision rules

- Name each artefact the work needs before composing the request.
- Declare each artefact's form: heading, structure, audience, maximum length.
- Order the artefacts explicitly and number them in the output contract.
- State what each artefact may assume from the others and what it must repeat standalone.
- Require the response top-to-bottom completeness: every named artefact present, in order.
- Check the returned response against the contract on receipt; a missing artefact is a follow-up target, not a re-request of everything.

## Procedure

1. List the artefacts the task must produce.
2. Write a form specification for each: heading, structure, length, audience.
3. Order them by dependence, and state the order in the request.
4. Compose the shared context once, above the artefact specifications.
5. Add the completeness requirement to the contract.
6. Send once; verify each artefact against its specification before use.

## Anti-patterns

- Asking for "a summary, risks, and a rewrite" with no forms or boundaries.
- A response that satisfies three of five artefacts and gets re-requested whole.
- Artefact specifications without lengths, so one artefact starves the rest.
- An implicit order that differs between requester and response.
- Treating a missing artefact as a failed request rather than a targeted gap.

## Done checklist

- [ ] Artefacts listed with forms and lengths.
- [ ] Order stated explicitly in the request.
- [ ] Shared assumptions declared.
- [ ] Completeness requirement in the contract.
- [ ] Response verified artefact by artefact.
- [ ] Gaps handled as follow-ups, not full re-requests.

## Sources

- Prompt engineering guidance, Anthropic: <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering>
- The twelve-factor app: <https://12factor.net/>
- Batch processing guidance, Anthropic: <https://docs.anthropic.com/en/docs/build-with-claude/batch-processing>
