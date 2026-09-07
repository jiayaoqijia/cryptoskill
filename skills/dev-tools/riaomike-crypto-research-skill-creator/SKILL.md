---
name: crypto-research-skill-creator
description: Use when creating, auditing, or refactoring reusable agent skills for cryptography, zero-knowledge proofs, lattice research, theorem review, security claims, or citation-sensitive literature work.
---

# Crypto Research Skill Creator

Create research skills whose triggers are precise, conclusions are traceable to evidence, and cryptographic claims are not stronger than their proofs or sources.

## Scope

Use this meta-skill to create, audit, or refactor a research skill. It defines the skill contract and quality gate; it does not perform the target research task unless the user separately asks for that task.

Keep the core portable across agent harnesses. Do not require a named tool, subagent model, hidden memory, proprietary metadata, or a particular directory outside the skill itself. A harness-specific adapter may be added only as an optional layer.

## Required Inputs

Obtain or infer, without blocking on low-risk details:

- representative requests that should and should not trigger the skill;
- the research task, expected deliverables, and intended audience;
- required evidence sources and permitted verification capabilities;
- the relevant cryptographic domain and threat/security model;
- target harness constraints, if any.

If a missing choice would materially change correctness or scope, ask for it. Otherwise state the assumption and continue.

## Success Criteria

A finished skill has:

- discriminating trigger metadata and explicit non-trigger boundaries;
- in-scope and out-of-scope work, required inputs, and observable outputs;
- success criteria, failure modes, stopping conditions, and uncertainty behavior;
- domain checks appropriate to its claims, parameters, and complexity measures;
- citation/version verification rules when external sources are used;
- valid relative links, no unfinished scaffold tokens, and no silent harness dependency;
- an audit result with blocking, major, and minor findings.

## Failure Modes

Stop or downgrade the result when required evidence cannot be inspected, a citation cannot be verified, notation or parameters are under-specified, or the requested conclusion exceeds the available proof. Never fill gaps with plausible-looking references, theorem details, security reductions, parameter values, or novelty claims.

When a capability is unavailable, report exactly what was not verified and provide only the safe partial result. “Not verified” is a valid outcome; fabricated certainty is not.

## Workflow

1. Select a mode: **create**, **audit**, or **refactor**.
2. Read [design-principles.md](references/design-principles.md) to define the trigger, scope, contract, structure, and portability boundary.
3. Read [crypto-research-conventions.md](references/crypto-research-conventions.md) whenever the skill handles papers, proofs, reductions, security claims, ZKPs, lattices, parameters, complexity, citations, or novelty.
4. For creation, instantiate [skill-template.md](references/skill-template.md), remove irrelevant sections, and keep conditional detail in focused references.
5. For audit or refactor, preserve correct user choices and observable interfaces. Change only what a concrete finding justifies.
6. Apply [validation-checklist.md](references/validation-checklist.md). Resolve all blocking findings; disclose unresolved major findings.
7. Run `python scripts/validate_skill.py PATH` when Python is available. Treat it as a structural check, not a substitute for domain review.
8. Return the skill directory plus a concise audit report: verdict, evidence checked, changes made, unresolved risks, and unverified items.

## Research-Integrity Invariants

- Label definitions, assumptions, conjectures, theorem statements, proof sketches, complete proofs, reductions, empirical observations, and engineering heuristics distinctly.
- A theorem's mathematical conclusion is not automatically an end-to-end protocol security claim.
- A proof sketch is not a checked proof; a machine-readable artifact is not machine-verified unless a checker was actually run successfully.
- State security notions, adversary powers, setup/model assumptions, parameter regime, and reduction loss before asserting security.
- Keep symbolic complexity, concrete cost, communication, memory, preprocessing, amortization, and failure probabilities separate.
- Verify bibliographic identity and claim support before citing a source. Never invent authors, titles, venues, identifiers, quotations, or theorem numbers.
- Treat novelty as a bounded search conclusion, not a fact. Use wording such as “no earlier result was found within the searched sources and dates,” together with search coverage and limitations.

## Output Contract

For **create**, return a ready-to-copy skill folder and a validation report. For **audit**, return findings before suggested edits. For **refactor**, return the revised folder, a change summary, preserved behaviors, and remaining risks.

Use the examples only as structural guides:

- [theorem-review](examples/theorem-review/EXAMPLE.md)
- [literature-search](examples/literature-search/EXAMPLE.md)

