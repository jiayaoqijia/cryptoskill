---
name: decision-records
domain: writing/doc-coauthoring
trigger: "Making substantive choices during co-authoring; recording alternatives, rejections, and rationale alongside the document"
anti_trigger: "Leaving final document text without rationale; deleting rejected alternatives so future readers repeat past debates"
scope: "Managing the document decision trail; recording chosen options, rejected alternatives, trade-offs, and open questions to preserve institutional rationale"
status: "seedling"
---

# Decision Records

## Standard

Substantive documents must carry an explicit decision trail rather than orphaned certainty. Grounded in the Architecture Decision Record (ADR) tradition, this leaf governs capturing what was decided, what alternatives were evaluated and rejected, the trade-offs accepted, and any open questions remaining at session close. The standard requires that decision rationale lives alongside the document—either in dedicated inline sections, an appended log, or linked structured records—so future reviewers understand *why* the text reads the way it does without reconstructing lost debates.

## Decision rules

1. Record every major architectural, strategic, or design choice made during the co-authoring loop immediately when finalized.
2. Document at least one viable rejected alternative for every key decision, stating explicitly why it was set aside.
3. Capture trade-off parameters (cost, complexity, speed, risk) associated with each selected option.
4. Maintain a clear list of open questions and deferred items so ongoing uncertainties remain visible.
5. Place decision records in a transparent, accessible format either within the document body or as a dedicated companion appendix.

## Procedure

1. Identify critical choice points as they arise during section planning and iterative building stages.
2. Prompt the author to articulate the core trade-offs and alternative approaches considered during the choice.
3. Draft a concise decision record entry covering context, decision, consequences, and rejected paths.
4. Integrate the decision record into the designated appendix or inline log section of the document.
5. Review the decision log during final reader testing to ensure all rationale claims are fully substantiated.

## Anti-patterns

- Documenting only the final decision while erasing all context regarding rejected alternatives and trade-offs.
- Hiding critical rationale in ephemeral chat transcripts rather than persistent document storage.
- Using vague justifications like best practice without stating specific technical or business criteria.
- Leaving open questions unresolved or unlisted at session completion.

## Done checklist

- [ ] Major document decisions captured with explicit rationale.
- [ ] Rejected alternatives and associated trade-offs documented.
- [ ] Open questions and deferred uncertainties inventoried.
- [ ] Decision records integrated into the document structure for permanent reference.

## Sources

- Architecture Decision Record (ADR) GitHub repository and standard practice guides: https://adr.github.io
- ISO/IEC/IEEE 42010 Systems and software engineering — Architecture description guidelines for rationale capture: https://www.iso.org


⚠️ Note: Decision records capture point-in-time choices; subsequent strategic pivots require explicit amendments.