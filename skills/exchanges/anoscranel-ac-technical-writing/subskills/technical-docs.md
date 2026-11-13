---
name: technical-docs
domain: writing/technical-docs
trigger: "\"write a README\", \"structure the docs\", \"tutorial or how-to\", \"docs are a mess\"."
anti_trigger: "One procedure or SOP (subskills/procedures-sops.md); in-product strings (subskills/ui-microcopy.md)."
scope: "Diátaxis types: tutorial, how-to, reference, explanation; README"
status: "seedling"
---

# Technical docs — types

## Standard

- **The Diátaxis framework** (Daniele Procida, https://diataxis.fr/) sorts every doc on two axes — theory versus practice, action versus reflection — into four non-overlapping types. Tutorials give a newcomer one reproducible first success, no decision forks. How-to guides walk a competent user through one real task. Reference is an austere, machine-mirrored catalogue. Explanation is discursive context and trade-offs (<https://diataxis.fr/>).
- **Cross-linking is fixed by direction:** Reference and how-tos link out to explanation for theory. Explanation links down to reference. Tutorials never link to deep reference mid-flight.
- **Docs live with the code.** The git-backed model keeps docs in the repo, so a feature commit cannot merge without its documentation commit. A headless CMS fails here — no branching, no code-diff review.
- **CI gates are named:** Vale prose linting against a style pack (Google developer documentation style: active voice, second person, sentence case; Microsoft Writing Style Guide), markdownlint for structure, Lychee for links, and doc-tests that execute snippets — `cargo test --doc`, `pytest --doctest-glob="*.md"`.
- **API docs run on specs:** OpenAPI 3.1.x for REST, AsyncAPI 3.0 for events. Renderers (Scalar, Redocly, Stoplight Elements) draw reference from the canonical spec, so doc and spec cannot drift. Errors follow RFC 9457 Problem Details.

## Decision rules

1. Name the type before writing. Setup steps inside reference tables, or theory inside a runbook, are the two documented contamination patterns — split the page.
2. Navigation depth is three levels: category, topic, article.
3. README order: what the project is, the first successful run, the main task paths, where full docs live, how to contribute, the licence.
4. Prose anchors to a published guide — Google's developer documentation style or the Microsoft Writing Style Guide — enforced in CI.
5. Index search by version; indexing every version routes users to outdated pages.

## Procedure

1. List the reader's tasks. Map each to a type: learning, doing, looking up, understanding.
2. Write one page per type per topic, in separate files with separate titles.
3. Draft the tutorial as a strict recipe: one outcome, every step verified, zero branches. Test on a newcomer.
4. Draft how-tos with preconditions first and the outcome before step one.
5. Draft reference as tables and signatures, no narrative. Pull from the spec where one exists.
6. Write explanation last, discursive prose, linking down to reference.
7. Wire the gates: Vale, markdownlint, Lychee, doc-tests. Keep snippets runnable with mocked network.
8. Add the feedback loop: a "was this helpful" micro-survey and a weekly zero-hit-search report.
## Anti-patterns

- A tutorial disguised as reference: setup steps buried in API tables.
- A runbook interrupted by architecture theory.
- Code snippets nobody executes; they bit-rot silently.
- Docs that live only in a CMS with no branch and no review.

## Done checklist

- [ ] Each page carries one Diátaxis type.
- [ ] Cross-links follow the fixed directions.
- [ ] Tutorial tested on a newcomer; how-tos state outcome first.
- [ ] Reference is austere and spec-derived.
- [ ] Vale, markdownlint, Lychee and doc-tests run in CI.
- [ ] Navigation is three levels.
- [ ] Feedback and zero-hit report wired.

## Sources

- <https://diataxis.fr/>
- https://diataxis.fr/
- https://developers.google.com/style · https://learn.microsoft.com/en-us/style-guide/
- https://spec.openapis.org/oas/v3.1.0 · https://www.rfc-editor.org/rfc/rfc9457.html
