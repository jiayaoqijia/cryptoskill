# Maintain or adapt this review skill

Read this when changing the skill or creating another team's domain review. `design-decisions.md` explains why the checklist looks like this.

## Reading order

1. `skill.md` drives shared review steps and points to relevant rule families.
2. `repos/<repository>.md` adds that client's checks and the verdict steps. The standard installer appends it to the shared checklist.
3. `references/shared.md` and the selected client's reference hold the detailed rules. Open the relevant sections as the checklist directs.

An installed skill contains both parts. There is no separate review-template catalog.

`scripts/review-task.mjs` runs every review, launched by hand or by a host such as Farmslot. `start` creates `temp/tasks/review/<target>/r<N>` with the checklist, a ledger section per row and `review.json`, and `finish` refuses unfinished work. With mm-harness the rows are timed marks that `mm-harness status --watch` shows; without it the checklist is a plain file. A later round is warm when the earlier one finished, the rules are the same and its head is part of the branch. It compares what the PR changes, so a merge from the default branch adds nothing. The folder stays on one machine, and nothing is posted.

## Knowledge ownership

Perps maintains its canonical rules in the recipe library's `review/antipatterns.md` and `review/antipatterns.<client>.md`. Update that source, then run:

```sh
node scripts/materialize-review.mjs --library <canonical-library>
node scripts/materialize-review.mjs --library <canonical-library> --check
```

`references/team.json` holds the Perps name, clients and row display: a plainer row title, the failure it prevents, and the clients that can meet it. A check keeps its anchor when its row is renamed, and one row covers one check. Recheck `clients` when a client gains the surface, such as Pro mode outside Mobile.

`references/review-sources.json` records the revision and content digests. The generator rejects uncommitted source rules. Do not hand-edit its generated checklist, overlays or references.

`references/pack.json` is the machine-readable rule pack generated from the same families. It lists each family's anchor, reference file, areas, class and status, plus each rule with its cause (`pre-0073` until an edit records one). A family from a client file names that client in `clients`, so a hosted review never expects its row in another client's checklist. A direct invocation does not read the pack.

For a shell-less consumer, `--analyzer-out <file> --client <client>` produces one self-contained copy with the same rules. Review that consumer change before enabling it.

## Add your team's review

Copy the Perps layout. You write the rules, and the generator writes everything else. Your library can live in your skill (shown here), in your recipe library or in another repository. Name an owner for it.

1. Create `domains/<team>/skills/<team>-review-pr/references/rules/` with:
   - `team.json`: domain, name, clients and docs. Copy `references/team.json` here and drop `rows`, which only renames existing Perps rows.
   - `owned-paths.json`: `{"domain": "<team>", "repos": {"mobile": ["app/..."]}}`. Clients are `mobile`, `extension`, `core` and `terminal`.
   - `review/antipatterns.md`, plus `review/antipatterns.<client>.md` for checks only one client needs.
   - `review/requirements.md` and `review/requirements.<client>.md`, if you have any.
   - `review/parity.md` and `review/shared-packages.md`, if clients share code.
2. Write each check as one `##` section. It becomes one checklist row, and its first sentence is the row text.

   ```md
   ## Quote freshness

   A quote is never submitted after it expires.

   - **Stale quote submitted**: reject a quote older than its expiry at submit time.
   ```

3. Generate, then commit the rules and the output together. The repository tests reject stale or hand-edited output.

   ```sh
   node domains/perps/skills/perps-review-pr/scripts/materialize-review.mjs --library domains/<team>/skills/<team>-review-pr/references/rules
   ```

   For a library in another repository, put `team.json` at its root, commit the rules and pass `--out domains/<team>/skills/<team>-review-pr`.

4. Add your team to `.github/CODEOWNERS` if it has no line.

There are two types of rule:

- **Antipatterns** are bad patterns people and agents keep reproducing. Add one only from a failure someone confirmed.
- **Requirements** are what your team chooses to check. Each has a `Why:` line, and `Class: advisory` if it must not block.

`mm-harness review checklist` lists antipatterns only.

## Writing rules

Write rules from observed failures. State what to inspect, where it applies and what would contradict the claim. Put client-specific APIs and tooling in that client's rules. Preserve useful examples; avoid duplicating a shared rule across clients.

A family checkbox is navigation, not blanket approval. Each applicable rule needs its own outcome. Read source and tests before calling a rule passed; missing runtime evidence stays a gap. Feed a retrospective back into the canonical rules only when it changes a future review decision.

Canonical `> Delegate: Run ...` entries become complete checklist actions, not summaries. Each names its owning skill and says to skip the call when Perps runs under `pr-workflow/review-pr`. Delegation-only sections do not create empty criterion rows.

`review/report-template.md` owns the compact posted-review format and verdict policy. The generator copies it into `references/`; the full rule ledger is a separate run artifact.
