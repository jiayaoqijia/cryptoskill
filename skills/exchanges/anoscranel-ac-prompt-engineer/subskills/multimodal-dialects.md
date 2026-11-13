---
name: multimodal-dialects
domain: prompt-engineering/multimodal-dialects
trigger: "When prompting image, video, or music generation models whose syntax and fields differ per family and version."
anti_trigger: "Text-LLM prompting (that is the rest of this skill), or choosing which generation vendor to buy."
scope: "Prompting image and video generation models: per-model dialects, negative-field cases, seeds, budgets, and dialect churn."
status: "seedling"
---

# Multimodal prompt dialects

## Standard

Match syntax to model architecture; there is no cross-family prompt grammar. The
operator-maintained dialect registry was sourced per vendor doc (an older cheat-sheet
was stale and was discarded). Key sourced facts:

- **Keyword stacks vs prose.** SDXL-family models parse weighted keyword stacks
 (`(word:1.3)`); FLUX.2 reads full sentences with a published priority order (first
 words weigh most); Midjourney v7 reads prose with parameter flags (`--ar`, `--s`,
 `--style raw`).
- **Negative prompts are three different things.** A real typed field (some SDXL and
 video surfaces; Wan truncates at 500 characters silently), a sentence in the main
 prompt (FLUX.2, GPT-image, which have no field), or a discouraged practice (Google,
 Anthropic: describe what you want instead). Midjourney's `--no` is a -0.5 weight, not
 a mask (vendor doc).
- **Negation can reverse.** On CLIP-family conditioning, negated captions scored better
 than true captions in a 228,246-pair study (WACV 2025, CC-Neg). Never
 rely on negating an unwanted object; describe the desired scene instead.
- **Video is a pipeline, not a prompt.** Prompt-text budgets range from 1,000 to 20,000
 characters across models on one router; duration, aspect, and reference roles are
 fields, not prose (Runway OpenAPI).

Primary sources: <https://ai.google.dev/gemini-api/docs/prompting-strategies> and <https://platform.claude.com/docs>.

## Decision rules

| Situation | Move |
|---|---|
| Unwanted object keeps appearing | Restate the desired scene positively; use the typed negative field only where one exists |
| Text rendering needed | Quote the literal string; prefer models with published text support |
| Repeatable output needed | Fix the seed where the vendor documents one; expect variance where none is published |
| Long multi-shot brief | Split into per-shot prompts and compose, rather than one maximal prompt |

## Procedure

1. Identify the model family and version; dialect behavior changes per version.
2. Look up which fields exist (negative, seed, aspect, reference images) before writing
 prose around them.
3. Put the most important tokens first on position-sensitive models.
4. Hold everything constant and change one variable per generation when iterating.
5. On a model version bump, re-verify the dialect against the vendor page before batch
 runs; behavior can drift silently.

## Anti-patterns

- Writing SDXL keyword stacks for FLUX or prose paragraphs for SDXL.
- `no X` phrasing where the vendor documents negation-as-presence behavior.
- Assuming yesterday's parameter survived this month's version bump.
- Spending prompt budget on style words while the aspect or duration field carries the
 real constraint.

## Done checklist

- [ ] The family, version, and available fields were checked against vendor docs.
- [ ] Negation handling follows the three-case split.
- [ ] Iteration changed one variable at a time.
- [ ] Version bumps trigger dialect re-verification.

## Sources

- <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- <https://platform.claude.com/docs>
