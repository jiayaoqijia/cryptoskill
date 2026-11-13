---
name: when-to-offer
domain: writing/doc-coauthoring
trigger: "Author starting a substantial document without structure; user asking for a proposal, spec, PRD, design doc, or RFC"
anti_trigger: "Quick notes, casual chats, single-paragraph emails, or documents already fully drafted and entering line-editing"
scope: "Deciding when to offer a structured co-authoring workflow versus freeform generation; gaining author consent before imposing process"
status: "seedling"
---

# When to Offer

## Standard

Co-authoring is a staged collaborative loop between an author and an agent for building substantial structured documents. This leaf governs when to propose the co-authoring workflow rather than generating text immediately. The standard requires that whenever an author requests a complex deliverable such as a proposal, technical specification, product requirement document (PRD), design document, or Request for Comments (RFC), the agent pauses single-shot generation and offers the structured loop. Co-authoring is unnecessary for short, transient notes or single-question answers where overhead outweighs value. The goal is to align expectations and secure explicit consent before introducing multi-stage dependencies. According to Anthropic's public research on doc-coauthoring workflows, upfront alignment reduces downstream revision cycles by establishing shared intent before drafting begins.

## Decision rules

1. Offer co-authoring whenever a prompt requests a multi-section document, formal proposal, technical specification, or architecture record.
2. Skip the offer and proceed directly to single-shot generation for short memos, single-paragraph summaries, or informal scratchpad notes.
3. Never force the workflow without author consent; if the user declines structured co-ops and requests raw drafting, respect the choice immediately.
4. Distinguish between brand-new documents requiring discovery and existing drafts needing revision; co-authoring applies exclusively to creation and iterative structuring.
5. Keep the offer brief: name the stages (context gathering, section planning, iterative building, reader testing) and ask for permission to proceed step by step.

## Procedure

1. Inspect the incoming request to evaluate document complexity, expected length, and structural requirements.
2. If the document requires more than a single section or represents a formal artifact (PRD, RFC, proposal), draft a concise offer message.
3. State the proposed co-authoring sequence clearly, highlighting the benefit of upfront context gathering and section planning.
4. Ask the author whether they want to use the structured workflow or prefer direct generation.
5. Wait for user confirmation before launching Stage 1; if confirmed, immediately invoke the context-gathering protocol.

## Anti-patterns

- Forcing the structured workflow on a user who explicitly asked for a quick first draft.
- Launching into multi-stage questioning without explaining the overall process or seeking consent.
- Treating casual brainstorming sessions as formal specification projects requiring heavy upfront gates.
- Assuming silence means agreement rather than seeking explicit confirmation to begin the co-authoring loop.

## Done checklist

- [ ] Document complexity assessed against multi-section criteria.
- [ ] Co-authoring offer formulated with clear stage descriptions.
- [ ] Explicit consent or preference obtained from the author.
- [ ] Transition executed cleanly into either structured co-authoring or direct drafting.

## Sources

- Anthropic public doc-coauthoring skill specification and research repository: https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring
- ISO 24495-1 Plain language guidelines on author-reader alignment and structured communication: https://www.iso.org/standard/78907.html
