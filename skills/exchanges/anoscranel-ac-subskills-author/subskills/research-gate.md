---
name: research-gate
domain: skill-authoring/research-gate
trigger: Before authoring any skill-with-subskills — verify the domain is thoroughly researched.
anti_trigger: The domain dossier already exists and passed this gate for this skill in this session.
scope: Deciding whether the domain is researched enough to author; halts the pipeline if not.
status: seedling
---

# Research Gate (pipeline step 1)

A skill-with-subskills may not be created until its domain is thoroughly researched — the
operator's binding constraint #3. An unresearched skill encodes a guess as a standard,
the worst outcome this pipeline exists to prevent. This gate runs FIRST and **halts the
pipeline** if any check fails.

## Standard

Three minimum-evidence checks, all must PASS:

1. **Dossier exists.** A `research/<slug>/` dossier (or the operator's own notes store) covers
   the domain's decomposition, verified against primary sources. Cite its path.
2. **Closed subdomain map is possible.** You can enumerate the domain's subdomains such
   that each is claimed by exactly one candidate leaf, with no orphan content and no
   cross-scope claim.
3. **Notes-first dedup.** A search of the operator's notes and of the installed skills directory
   confirms whether an existing skill or note already covers the domain.

## Decision rules

Check 3 routes, never blocks:

- **Our own artifact exists (a note or a skill we authored) → EXTEND it, never fork.**
- **Coverage in any other skill, full or partial, never blocks and never becomes a
  reference:** the new skill covers its full domain itself, re-researched from primary
  sources. Log that coverage as a collision to test at entrance-eval time.
- **None → author new.**

## Procedure

1. **Dossier check.** If none exists → **FAIL, do the research first.**
2. **Closed-map check.** If the domain resists a clean closed map (overlapping concerns
   you cannot separate), that signals insufficient understanding → **FAIL, research more.**
3. **Dedup — decide, don't ask:** decide extend-vs-new with no pause to ask; the
   decision is logged, not gated. Extend a copy in a staging dir (e.g.
   `~/.local/share/skill-staging/<skill>/`), never the installed tree. A self-authored
   skill installs only after audit-skill, and then only on human approval or through the
   operator's fail-closed gate. If the existing skill was not gate-installed, the gate cannot
   update it (name collision): stage the update, run audit-skill and a
   gate scan-only check, and log it in the run log. A live swap
   replaces an installed skill, so it is an install: it happens only on a human's explicit
   approval or through the operator's fail-closed gate, with backup → apply → lint →
   routing-eval regression, and restore on any failure. Record the decision and its reason in the run
   log so the operator can audit it.

## Anti-patterns

- Proceeding to domain-map on a check-1 or check-2 FAIL.
- Forking our own artifact instead of extending it.
- Pausing to ask about the dedup decision — it is logged, not gated.

## Done checklist

A one-line verdict per check (PASS/FAIL + evidence path). FAIL on check 1 or 2 → **stop
and report the gap to the operator; never author past an unpassed research gate.**

## Sources

- House standard for skills-with-subskills (unpublished).
- <https://github.com/>
- <https://osf.io/prereg/>
