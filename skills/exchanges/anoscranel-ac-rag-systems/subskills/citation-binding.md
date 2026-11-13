---
name: citation-binding
domain: prompt-engineering/citation-binding
trigger: "Binding each generated claim to the passage that supports it."
anti_trigger: "Not for the grounding prompt, and not for chunking."
scope: "Binding each generated claim to the passage that supports it."
status: seedling
---

# Citation binding

## Standard

A citation is a claim about provenance: this sentence in the answer is supported by that passage in the corpus. The binding is only trustworthy if it is made at the level where support actually exists — the chunk that was retrieved — and if the answer is generated from passages that carry stable chunk identifiers. Citation generated after the fact, from an answer already written, decorates; citation bound at generation, from identified chunks, evidences.

The mechanics follow from the design. Each retrieved passage carries an identifier that survives into the prompt, the answer's claims reference those identifiers, and the rendering layer maps identifiers back to their source text for the user. What makes the binding real rather than ornamental is that it starts at the chunk: a claim that cannot point to the chunk that supports it is either unsupported or supported by a passage the pipeline never retrieved — both are verification failures, and the distinction is exactly what verification exists to make.

Primary sources: <https://docs.anthropic.com/en/docs/build-with-claude/citations> and <https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview>.

## Decision rules

- Every retrieved passage carries a stable identifier into the prompt, not just into the log.
- Claims cite at chunk granularity — document-level citations hide which passage actually supports a claim.
- The rendering layer maps identifiers back to real source text, verified in testing.
- Chunk metadata travels with the passage: source document, location, version, date.
- Chunk boundaries and citation granularity are chosen together in the retrieval skill; the record states both.
- Spot-check bindings in production: answers with citations that point to passages that do not support the claim are worse than uncited answers.

## Procedure

1. Ensure every retrieved passage arrives with a stable identifier and metadata.
2. Generate with instructions to cite the identifier for each claim.
3. Render citations back to source text at the interface layer.
4. Spot-audit: sample cited claims and verify the cited passage supports them.
5. Feed misbinding failures back to the retrieval granularity or the prompt, as diagnosed.
6. Record the binding failure rate with the rest of the system's numbers.

## Anti-patterns

- Document-level citations for chunk-level claims.
- Generating the answer first and attaching citations after.
- Rendered citation text that the system never verified against the source.
- Dropping passage metadata when the passage enters the prompt.
- Never auditing whether the cited passage supports the citing claim.

## Done checklist

- [ ] Passage identifiers present in prompt and output.
- [ ] Claims cite at chunk granularity.
- [ ] Rendering maps identifiers to real text, tested.
- [ ] Metadata intact end to end.
- [ ] Spot-audit misbinding rate measured.
- [ ] Failures fed back with a diagnosed cause.

## Sources

- Citations API mechanics: <https://docs.anthropic.com/en/docs/build-with-claude/citations>
- RAG architecture overview: <https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview>
- Original RAG paper: <https://arxiv.org/abs/2005.11401>
