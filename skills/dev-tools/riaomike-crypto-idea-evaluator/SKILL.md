---
name: crypto-idea-evaluator
description: Use when turning a cryptography, ZKP, or lattice idea into a research question, claim map, feasibility assessment, evidence plan, risk register, or go/no-go decision.
---

# Crypto Idea Evaluator

Convert an informal idea into falsifiable research claims and a decision-ready brief. Do not assume significance, novelty, correctness, security, or performance.

## Scope

In scope: problem/claim formalization, baseline and threat-model selection, assumption/parameter inventory, proof and experiment obligations, feasibility/significance risks, ethics, and kill criteria.

Out of scope: declaring novelty without search, proving theorems, inventing results, writing a finished paper, or submitting/publishing anything.

## Required Inputs

- the proposed construction, technique, observation, or target improvement;
- intended primitive/protocol, security notion/model, adversary, and use case;
- expected difference from known baselines;
- available theory, implementation, data, compute, and time constraints.

Ask for missing information only when it changes the core research question. Otherwise state assumptions.

## Success Criteria

- The idea becomes explicit research questions and falsifiable claims.
- Functionality, security, efficiency, usability, and novelty claims are separated.
- Each claim has required proof, literature, parameter, or experimental evidence.
- Baselines, closest-work search needs, assumptions, threat model, parameters, and ethical risks are visible.
- Feasibility risks and kill/pivot criteria are concrete.
- The recommendation is proceed, proceed with prerequisites, pivot, or stop—never “promising” without evidence.

## Failure Modes

- Vague idea: return alternative formalizations and request the decisive missing delta.
- Unstated security model: block security conclusions and list candidate models.
- Novelty premise: mark unverified and require a bounded prior-art search.
- Unavailable resources: propose a smaller falsifiable study or mark infeasible.
- Ethical/responsible-disclosure risk: require human review before data collection, attack execution, or disclosure.
- Contradictory goals: expose the tradeoff and request a priority decision.

Never fabricate prior art, proof obligations already discharged, benchmark results, parameters, or reviewer interest.

## Workflow

1. Apply [protocol.md](references/protocol.md) to formalize the object, claim map, baselines, model, assumptions, and evidence obligations.
2. Create adversarial alternative explanations and fastest falsification tests.
3. Define minimum viable theorem/prototype/experiment and kill criteria.
4. Produce a staged research brief with dependencies and human decisions.
5. Use [evaluation-scenarios.md](references/evaluation-scenarios.md) for future independent evaluation; do not claim it ran unless outputs were inspected.

## Output Contract

Return: idea statement; research questions; claim-evidence matrix; threat/setup model; baselines and novelty-search brief; proof/parameter/experiment plan; significance and ethics analysis; risks; kill/pivot criteria; next three actions; bounded recommendation.

