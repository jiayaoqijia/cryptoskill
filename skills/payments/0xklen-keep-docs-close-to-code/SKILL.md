---
name: keep-docs-close-to-code
description: Use when documentation keeps drifting from source or lives far from what it describes. Co-locates docs with code, generates what can be generated, and enforces updates in the same PR.
---

# Keep Docs Close to Code

Docs drift because they live in a separate place updated by a separate process. Put them where the change happens and make the update part of the diff.

## Procedure

1. Co-locate a module's doc beside it (`module.py` next to `module.md`) or in a `docs/` tree with a strict mirror of the source layout.
2. Generate reference material from source: docstrings, OpenAPI, `--help`. Never hand-write what the code can emit.
3. Add a docs check to CI that fails when a public signature changes without a docs change: compare `git diff --name-only` against the touched source.
4. Require the same PR to update docs; a bot comment linking the affected page is the minimum.
5. Keep long-form guides in `docs/` but link them from the code comment so the code names its own doc.
6. Use a single source of truth for examples: extract from `examples/` into docs at build time.
7. Add a `CODEOWNERS` entry so the docs owner is requested when their page's code changes.
8. Version docs with the code (a `docs/` folder per tag) rather than a wiki that shows only the latest.
9. Run the drift check on a schedule even for repos without PR gates: `make docs-check`.
10. Delete docs that duplicate generated output to shrink what can drift.
11. Put the docs update in the same commit as the code change, so it appears in review together.

## Pitfalls

- A wiki edited by hand that no reviewer sees, so it diverges with no signal.
- Generated reference checked into the repo and regenerated only occasionally.
- A docs check that compares timestamps instead of content, failing on no-op edits.
- Co-locating so aggressively that source directories fill with markdown and become unnavigable.
- Assuming proximity is enough; without the CI gate, colocation still drifts.
- A help string and a doc page that both describe the flag and disagree with each other.
- Moving code without moving its co-located doc, orphaning the page.

## Verification

    git diff --name-only HEAD~1 | grep -E '\.(py|ts)$' > /tmp/src.txt
    git diff --name-only HEAD~1 | grep -E 'docs/|\.md$' > /tmp/doc.txt

A source change touching a documented symbol must show a matching doc change. Report whether the last N PRs that changed public APIs also changed their docs, from `git log --name-only`.
