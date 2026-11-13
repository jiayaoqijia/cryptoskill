---
name: claim-files
domain: skill-authoring/claim-files
trigger: "Checking the factual sentences in a README, changelog, or proof file before a release; a page whose counts, links, names, or 'no X' lines turned out false"
anti_trigger: "Running gates on the final bytes; auditing the claim set independently; repairing findings and auditing the delta"
scope: "Building the claim inventory for user-facing release files and proving each count, name, link, tag, and negation against the bytes that ship"
status: "seedling"
---

# Claim Files

## Standard

- **SLSA provenance**: a release ships with verifiable statements about the artifact; a README is that document in prose. <https://slsa.dev/spec/v1.0/provenance>
- **GNU coreutils**: a count is a command output and a search is a set of lines. Both reproduce; memory does not. <https://www.gnu.org/software/coreutils/manual/html_node/wc-invocation.html>
- **Keep a Changelog 1.1.0**: a changelog entry claims a behaviour change and gets the same proof as the README. <https://keepachangelog.com/en/1.1.0/>
- **SemVer 2.0.0**: a version number is a compatibility promise, so a version tag in prose is a testable claim. <https://semver.org>
- ⚠️ House convention: a negative sentence ("no scripts") is a claim and needs the same proof.

## Decision rules

1. A sentence is a claim if it holds a number, name, path, link, version, or negation.
2. Count over the whole shipping tree, never from `head`, `tail`, or a scrolled view.
3. A count names its command and its scope.
4. A "no X" claim needs a recorded pattern and an empty result.
5. A link is a claim: resolve relative links locally, fetch external links once.
6. A version tag is checked against the tag list and the changelog, not against intent.
7. Seal the claim set with the tree; sealing one before the other guarantees drift.

## Procedure

1. Freeze the shipping tree; record a hash of its file list and date the table against it.
2. Read every user-facing file end to end with line numbers.
3. Build a four-column table: `file:line`, claim, proof command, observed result.
4. Run the counts over the frozen tree:

   ```
   find . -type f -not -path './.git/*' | wc -l
   find scripts -type f | wc -l
   grep -rc 'pattern' .
   ```

5. Run each negation as a scoped search, e.g. `grep -rni 'network\|curl\|http' .`; record the pattern.
6. Resolve links from each file's own directory. Fetch each external link once and record the status.
7. Check tags: `git tag --list` plus the changelog section. A prose tag absent from the list is false.
8. Rewrite every failed claim narrower and true; cut one that will not prove.
9. Re-read after the edits: a rewrite makes new sentences, which are new claims.

A README written from memory shipped seven false claims, including a wrong file count, a "no scripts" line over four scripts, two dead links, and a tag that never existed. Each took a minute to check.

## Anti-patterns

- **Counting from a partial view.** `head -40` hides the fifth script. Fix: count the tree.
- **Prose from memory.** This is how the seven false claims shipped. Fix: one command per claim.
- **Negation by assumption.** "No dependencies" because none were added deliberately. Fix: search the manifest and imports.
- **Link checked once, at write time.** The target moved since. Fix: resolve at freeze time and after the push.
- **Changelog exempted.** It is the most-read claim file. Fix: inventory it like the README.

## Done checklist

- [ ] Every user-facing file read end to end with line numbers.
- [ ] Every count, and every "no X" claim, carries a command and a result.
- [ ] Every link resolved at freeze time.
- [ ] Every version tag exists in the tag list and the changelog.
- [ ] Table dated and tied to a tree hash.

## Sources

- SLSA provenance: <https://slsa.dev/spec/v1.0/provenance>
- GNU coreutils `wc`: <https://www.gnu.org/software/coreutils/manual/html_node/wc-invocation.html>
- Keep a Changelog 1.1.0: <https://keepachangelog.com/en/1.1.0/>
- SemVer 2.0.0: <https://semver.org>
