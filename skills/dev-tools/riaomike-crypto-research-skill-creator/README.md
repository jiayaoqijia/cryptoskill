# crypto-research-skill-creator

A harness-agnostic meta-skill for creating, auditing, and refactoring reusable research skills for cryptography, zero-knowledge proofs (ZKPs), and lattice-based cryptography.

It is designed around the common Agent Skills convention: a directory with a required `SKILL.md`, plus optional `references/`, `scripts/`, and examples. The portable core does not assume Codex, Claude Code, DeepSeek Harness, subagents, web search, or a specific citation database.

## What it enforces

- precise triggers, non-triggers, scope, inputs, outputs, and success criteria;
- explicit failure modes, stopping rules, missing-capability behavior, and uncertainty;
- citation and source-version verification;
- separation of theorem, proof, reduction, assumption, empirical, security, and novelty claims;
- ZKP-specific model, setup, relation, soundness, knowledge, zero-knowledge, Fiat-Shamir, composition, and cost checks;
- lattice-specific problem, distribution, norm, reduction, parameter, failure-probability, and attack-estimate checks;
- symbolic and concrete parameter/complexity accounting;
- a strict ban on fabricated references and overclaimed novelty.

## Directory layout

```text
crypto-research-skill-creator/
├── SKILL.md
├── README.md
├── references/
│   ├── design-principles.md
│   ├── crypto-research-conventions.md
│   ├── validation-checklist.md
│   └── skill-template.md
├── examples/
│   ├── theorem-review/
│   └── literature-search/
├── scripts/
│   └── validate_skill.py
└── tests/
    └── test_validate_skill.py
```

## Installation

Copy the whole `crypto-research-skill-creator` directory into a skill directory recognized by the target harness. Common locations include:

- shared Agent Skills: `~/.agents/skills/`;
- Codex personal skills: `~/.codex/skills/`;
- Claude Code personal skills: `~/.claude/skills/`;
- DeepSeek or another harness: its configured skill/plugin directory.

If a harness uses different metadata or tool declarations, keep this directory as the portable core and add a thin adapter outside it. Do not rewrite core research rules around one vendor's tool names.

## Use

Ask the agent to use `crypto-research-skill-creator` in one of three modes:

- **Create:** build a new crypto research skill from representative requests and desired outputs.
- **Audit:** report trigger, scope, portability, research-integrity, and domain-specific findings without modifying the skill.
- **Refactor:** repair a skill while preserving valid behavior and recording changes.

Example request:

```text
Use crypto-research-skill-creator to create a skill for reviewing knowledge-soundness proofs in Fiat-Shamir-transformed protocols. It must distinguish ROM from QROM claims and report reduction loss and concrete soundness error.
```

## Validate

The bundled validator uses only the Python standard library:

```text
python scripts/validate_skill.py PATH/TO/SKILL
python -m unittest discover -s tests -v
```

It checks structure and contract headings. It cannot decide whether a theorem is true, a proof is complete, a search is exhaustive, or a security parameter is adequate. Apply `references/validation-checklist.md` for those judgments.

## Examples are skeletons

`examples/theorem-review/EXAMPLE.md` and `examples/literature-search/EXAMPLE.md` are intentionally compact patterns, not certified production skills. They deliberately do not use the `SKILL.md` filename, so recursive harness discovery cannot mistake them for installed skills. Before deployment, copy an example into a new top-level skill directory as `SKILL.md`, then adapt the scope, sources, threat model, output schema, and behavioral tests to the intended research workflow.

## Portability contract

A generated skill must degrade honestly when a capability is missing. For example, if the harness cannot browse or access a cited paper, the output should mark the citation and claim support as unverified; it must not infer bibliographic details or claim that verification occurred.

