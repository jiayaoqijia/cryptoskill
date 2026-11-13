---
name: gate-review
domain: skill-authoring/gate-review
trigger: "Release evidence is assembled and someone must decide whether to push; a gate that returned caveats instead of a verdict; a HALT list to close"
anti_trigger: "Producing the evidence; repairing findings; the mechanics of the push itself"
scope: "Reading the full release evidence chain and issuing one SHIP or HALT verdict that licenses the push and nothing else"
status: "seedling"
---

# Gate Review

## Standard

- **SLSA**: a release decision rests on evidence attached to the artifact, not a verbal assurance. <https://slsa.dev>
- **NIST SP 800-53 Rev. 5, AC-5**: the party that approves is not the party that produced. <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
- **SemVer 2.0.0**: a version number is a public compatibility promise; publishing one is what this gate protects. <https://semver.org>
- ⚠️ House convention: one verdict with two values. Most processes allow conditional approval; this gate does not.

## Decision rules

1. The verdict is SHIP or HALT. A caveat is either a HALT item or it is closed.
2. The reviewer reads the chain in order: claim table, gate transcript, audit, repair log, delta audit, tree hash.
3. Missing evidence is HALT; an absent audit is not a clean audit.
4. The reviewer re-runs two spot checks rather than trusting pasted output.
5. Every earlier blocker is closed with evidence or accepted in writing by the owner, never silently.
6. HALT items are fixed and the gate runs again on the new bytes; a partial re-review is a new full review.
7. The verdict licenses the push and nothing else; the owner's go-ahead is still required. It does not license a force-push, tag move, scope change, or later edit.

## Procedure

1. Assemble the packet in order, each item carrying the hash it was produced against.
2. Check the hash. If the packet describes a different tree, stop at HALT.
3. Walk the claim table: every FAIL shows a fix and a re-proof, or a written acceptance.
4. Walk the findings the same way. Open and closed blocker counts must agree with the table.
5. Re-run two proofs chosen at random; paste the output.
6. Check the tags: every tag named in prose exists, and every tag about to be published points at the final commit.
7. Check the changelog section for this version, and the version against SemVer relative to the last published tag.
8. Write the verdict: date, tree hash, SHIP or HALT, one-line reason. For HALT, list each item with file, line, and replacement. Archive the packet beside the release record.

A HALT item must be actionable outside the conversation. "Fix the README" fails; "README.md:22 says five files, the tree has seven, replace five with seven" passes.

## Anti-patterns

- **Gate after the push.** The verdict becomes a comment on history. Fix: gate before the irreversible step.
- **Gate by the writer.** The author signs off on the author. Fix: a different reviewer, every time.
- **Signature on a summary.** The reviewer read the report, not the evidence. Fix: open the files and commands.
- **"Ship it and fix next release" for a false claim.** The claim stays live for a cycle. Fix: HALT, repair, re-gate.
- **HALT list without exact strings.** The repairer guesses. Fix: file, line, replacement.

## Done checklist

- [ ] Packet assembled in order; every item hashed; hash matches the tree under review.
- [ ] Every claim FAIL closed by a fix and re-proof, or accepted in writing; blocker counts agree.
- [ ] Two spot checks re-run; tags exist and point at the final commit.
- [ ] Changelog and SemVer check passed.
- [ ] Verdict written with date, hash, value, and reason.
- [ ] HALT items carry file, line, and replacement.

## Sources

- SLSA: <https://slsa.dev>
- NIST SP 800-53 Rev. 5, AC-5: <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
- SemVer 2.0.0: <https://semver.org>
