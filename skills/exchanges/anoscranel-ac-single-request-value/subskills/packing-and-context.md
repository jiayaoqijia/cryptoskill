---
name: packing-and-context
domain: prompt-engineering/packing-and-context
trigger: "Loading one request with everything it needs so no second call is required."
anti_trigger: "Not for prompt style in general, and not for retrieval pipelines."
scope: "Loading one request with the evidence, the questions, and the output contract."
status: seedling
---

# Packing and context

## Standard

A request that cannot finish its job in one round trip costs a second request, and under a cap the second request is the failure mode. Packing is the discipline of sending everything the answer needs: the source material verbatim, the definitions that fix what words mean, the format the output must take, and the standard it will be judged against. What the request cannot infer, it must be given.

The trade is context length against round trips, and under a request-binding limit the trade favours packing: a longer request that completes in one call beats two shorter calls that together cost twice the requests and risk the stall. The limit that decides is the model's context window and the provider's token ceiling per request — read from the provider's own documentation — and the packer's job is to fit inside it without dropping the load-bearing material.

Primary sources: <https://docs.cohere.com/docs/rate-limits> and <https://docs.anthropic.com/en/api/rate-limits>.

## Decision rules

- List what the answer depends on before composing: sources, definitions, format, audience, standard.
- Quote source material verbatim rather than summarising it into the request.
- State the output contract explicitly: sections, lengths, the form of each part.
- State the boundary conditions — what to do with gaps, conflicts, or omissions in the material.
- Pack to the context limit that the provider documents, not to a habit length.
- Record what was packed and why, so a weak answer can be traced to a missing input rather than a retry.

## Procedure

1. Inventory the inputs the answer needs, from the task's own definition.
2. Gather the source material and verify it is the complete set.
3. Compose the context block: sources first, then definitions, then the questions.
4. Add the output contract and the boundary conditions.
5. Measure the packed length against the window, and trim the least load-bearing material first.
6. Send once; log the pack list and the response together.

## Anti-patterns

- Summarising the sources to save context and losing the detail the answer needed.
- Sending a question that references material the request does not contain.
- Discovering a missing definition only after the answer comes back wrong.
- Trimming the output contract to fit, leaving the answer's form to chance.
- Packing so tightly that a second round trip becomes inevitable anyway.

## Done checklist

- [ ] Input inventory complete before composing.
- [ ] Sources included verbatim and complete.
- [ ] Definitions and standards stated in the request.
- [ ] Output contract and boundary conditions explicit.
- [ ] Length measured against the documented window.
- [ ] Pack list logged with the response.

## Sources

- Provider limits documentation, Cohere: <https://docs.cohere.com/docs/rate-limits>
- Provider limits documentation, Anthropic: <https://docs.anthropic.com/en/api/rate-limits>
- Prompt engineering guidance, Anthropic: <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering>
