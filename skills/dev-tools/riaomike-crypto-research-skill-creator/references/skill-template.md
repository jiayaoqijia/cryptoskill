# Portable Crypto Research Skill Template

Use this reference in **create** mode. Copy the fenced content into a new `SKILL.md`, replace every double-bracket token, and delete sections that are genuinely inapplicable. Double-bracket tokens are intentional only in this template; none may remain in a deployed `SKILL.md`.

```markdown
---
name: [[lowercase-hyphen-name]]
description: Use when [[concrete triggering requests, artifacts, and domain symptoms; describe when, not the workflow]].
---

# [[Human-Readable Skill Name]]

[[One paragraph: what research outcome this skill enables and the core integrity principle.]]

## Scope

In scope:

- [[authorized actions and target artifacts]]
- [[evidence/source boundary]]
- [[permitted conclusion level]]

Out of scope:

- [[nearby tasks that should not activate this skill]]
- [[claims the workflow cannot certify]]
- [[external mutations or decisions requiring separate authorization]]

## Required Inputs

- [[research question, claim, paper, proof, repository, or parameter set]]
- [[security notion/model and domain-specific context]]
- [[required primary sources or acceptable evidence classes]]
- [[output audience/format when material]]

Ask only when missing information would materially change correctness or scope. Otherwise state assumptions.

## Success Criteria

- [[observable output artifact or report fields]]
- [[claim/evidence status coverage]]
- [[parameter/complexity consistency condition]]
- [[citation/version verification condition]]
- [[domain-specific completion condition]]

## Failure Modes

- If [[critical evidence missing]], then [[stop / ask / narrow / mark unverified / partial result]].
- If [[versions conflict]], then [[preserve both, reconcile, or report discrepancy]].
- If [[capability unavailable]], then [[safe degraded behavior]].
- If the requested conclusion exceeds the evidence, return the strongest supported bounded conclusion and state the gap.

Never invent references, theorem details, proof steps, parameter values, verification runs, or novelty.

## Workflow

1. Classify the request and confirm it is in scope.
2. Inventory inputs, versions, notation, assumptions, parameters, and missing capabilities.
3. Classify consequential claims: definition, assumption, theorem, proof sketch, proof, reduction, security, empirical, heuristic, or novelty.
4. [[Domain-specific analysis steps, each with an evidence requirement.]]
5. Verify citations and source/version identity before relying on them.
6. Check parameter consistency, probability/failure terms, and symbolic/concrete complexity.
7. Apply [[linked validation protocol or checklist]].
8. Return verified conclusions, limitations, unresolved questions, and evidence status separately.

## Domain Checks

### Security and proof

- [[security notion, game/model, adversary, setup, assumption, reduction, and loss]]
- [[statement validity versus proof completeness versus protocol implication]]

### ZKP (remove if inapplicable)

- [[relation/setup; completeness; soundness/knowledge; ZK; ROM/QROM; composition; costs]]

### Lattice (remove if inapplicable)

- [[problem variant; distributions/norms; reductions; parameters; failures; estimator/attacks]]

## Output Contract

```text
Verdict/status:
Scope and evidence inspected:
Claim-by-claim findings:
Parameter and complexity findings:
Citations and versions:
Blocking gaps:
Unverified items:
Bounded conclusion:
```

## References

- Read `references/[[focused-reference]].md` when [[observable condition]].
```

## Optional supporting structure

Add only directories the skill actually uses:

```text
[[skill-name]]/
├── SKILL.md
├── references/     # detailed protocols, schemas, domain rules
├── scripts/        # deterministic reusable validation/processing
├── assets/         # files copied into user-facing outputs
└── agents/         # optional harness adapter, never required by portable core
```

## Template completion checks

- Replace every `[[...]]` token.
- Make the folder name equal the frontmatter `name`.
- Keep the description discriminating and workflow-free.
- Link only files that exist.
- Preserve all applicable integrity rules from `crypto-research-conventions.md`.
- Add at least one success criterion that can fail visibly.
- Add failure behavior for missing sources and missing capabilities.
- Validate positive triggers, close negatives, incomplete evidence, and pressure to overclaim.

