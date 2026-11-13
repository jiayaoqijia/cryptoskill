---
name: code-docs
domain: software-engineering/code-docs
trigger: "\"document this function\", \"add docstrings\", \"generate the API reference\", \"docs drifted from the code\"."
anti_trigger: "The decision record; user-facing prose such as READMEs, tutorials and release notes; agent instruction files; a design spec written before code."
scope: "Docs-as-code inside the repo: comments, docstrings, generated API reference, docs-in-same-PR"
status: "seedling"
---

# Code Docs

## Standard

- **Docs-as-code**: prose lives in the repository as Markdown, is reviewed in a PR, and is built and versioned with the release. Google's tech-writing canon is the reference (https://developers.google.com/tech-writing).
- **Comments explain why, not what**. The code says what it does; the comment records the constraint, the bug, or why the obvious fix was wrong.
- **Generated reference beats hand-written**: reference pages come from the spec or the source, because hand-written pages drift.
- **Diátaxis** (https://diataxis.fr): each page answers exactly one need — tutorial, how-to, reference or explanation.
- **Docs in the same PR**: a change that alters behaviour updates its docs in the same change.

## Decision rules

1. A comment that restates the code is deleted. A comment that records a constraint is kept.
2. A docstring documents the contract: parameters, return, errors raised, invariants.
3. Reference pages are generated. Never hand-maintain a list a tool can emit.
4. Delete a wrong comment. It costs more than no comment.
5. Mark a known gap with ⚠️ and name what would settle it.
6. Each page has one quadrant. A page that teaches and references is split.
7. Docs for removed behaviour are deleted, not archived in place.
8. Doc changes ship in the same PR as the behaviour change.

## Procedure

1. For each public surface, check the docstring against the current signature.
2. Write or fix it:
   ```python
   def charge(amount_minor: int, idem_key: str) -> Receipt:
       """Charge a card.

       Args:
           amount_minor: positive amount in minor units.
           idem_key: durable client key; the same key replays the result.

       Raises:
           CardDeclined: the payment method was refused.
       """
   ```
3. Replace any comment that repeats the line below it.
4. Move decision prose into a decision record (out of scope for this leaf: the record format).
5. Generate the reference from the spec: `npx @redocly/cli build-docs openapi.yaml -o docs/api.html`.
6. Build the docs in CI, so a broken page fails like broken code.
7. Add a docs checkbox to the PR template.
8. Audit the doc tree: merge duplicates, delete orphans.
9. Run one generated example against the live API, to prove the samples work.

## Anti-patterns

- Commented-out code left as documentation.
- A docstring listing a parameter the function no longer takes.
- A hand-written endpoint list beside a generated one.
- A page that teaches and references in one breath.
- Docs updated a release later, from memory.
- A stale page archived instead of deleted.

## Done checklist

- [ ] Every public surface has a matching docstring.
- [ ] No comment restates the code.
- [ ] Reference generated from source or spec, built in CI.
- [ ] Doc updates ride the same PR.
- [ ] No orphan or duplicate pages.

## Sources

- <https://developers.google.com/tech-writing>
- <https://go.dev/blog>
- https://diataxis.fr
