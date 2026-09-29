# Maintain or adapt this review skill

Read this when changing the skill or creating another team's domain review.

## Reading order

1. `skill.md` drives shared review steps and points to relevant rule families.
2. `repos/<repository>.md` adds that client's checks and the verdict steps. The standard installer appends it to the shared checklist.
3. `references/shared.md` and the selected client's reference hold the detailed rules. Open the relevant sections as the checklist directs.

An installed skill contains both parts. Farmslot freezes the source bundle and registers the shared file and selected overlay as consecutive child checklists. Both paths execute the same rules. There is no separate review-template catalog.

## Knowledge ownership

Perps maintains its canonical rules in the recipe library's `review/antipatterns.md` and `review/antipatterns.<client>.md`. Update that source, then run:

```sh
node scripts/materialize-review.mjs --library <canonical-library>
node scripts/materialize-review.mjs --library <canonical-library> --check
```

`references/review-sources.json` records the revision and content digests. The generator rejects uncommitted source rules. Do not hand-edit its generated checklist, overlays or references.

For a shell-less consumer, `--analyzer-out <file> --client <client>` produces one self-contained copy with the same rules. Review that consumer change before enabling it.

## Another team's version

Keep the repository's `skill.md` plus `repos/` convention. Replace Perps knowledge and ownership paths with that team's rules; keep the execution contract: frozen diff, applicability inventory, individual rule outcomes, cited evidence and explicit gaps before verdict.

Write rules from observed failures. State what to inspect, where it applies and what would contradict the claim. Put client-specific APIs and tooling in that client's rules. Preserve useful examples; avoid duplicating a shared rule across clients.

A family checkbox is navigation, not blanket approval. Each applicable rule needs its own outcome. Read source and tests before calling a rule passed; missing runtime evidence stays a gap. Feed a retrospective back into the canonical rules only when it changes a future review decision.
