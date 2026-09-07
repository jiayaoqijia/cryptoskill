# Design Principles for Portable Research Skills

Use this reference when defining or revising a skill's activation boundary, contract, structure, portability, or evaluation strategy.

## 1. Start from decisions, not prose

A useful skill changes decisions an already-capable agent would otherwise get wrong or make inconsistently. Before writing instructions, define this contract:

| Field | Required question |
|---|---|
| Trigger | Which observable requests or artifacts should load the skill? |
| Non-trigger | Which nearby requests belong to another workflow? |
| Scope | What work is authorized, and what is explicitly outside the task? |
| Inputs | What evidence, artifacts, parameters, and user choices are required? |
| Outputs | What inspectable files, tables, reports, or decisions are returned? |
| Success | What can a reviewer observe to decide the task succeeded? |
| Failure | What missing evidence or capability forces a stop, downgrade, or partial result? |
| Risk | Which errors would corrupt research conclusions rather than merely reduce style quality? |

Do not begin with a long workflow and retrofit this contract afterward. The contract determines the workflow.

## 2. Design discriminating triggers

The `description` is discovery metadata, not a miniature instruction manual.

- Begin with `Use when` and describe concrete triggering situations.
- Include domain keywords that distinguish the skill: theorem review, knowledge soundness, lattice parameters, literature search, citation verification, and similar terms.
- Avoid catchalls such as “research tasks” or “helps with cryptography.”
- Put process detail in the body, not the description.
- State non-trigger cases in the body when neighboring skills could be confused.

Test triggers with at least three positive requests, three close negatives, and one ambiguous request. The ambiguous case should lead to a bounded clarification or a stated safe assumption.

## 3. Make scope operational

Scope is not a topic label. It determines which actions and conclusions are permitted.

A scope statement should cover:

- task boundary: create, analyze, verify, edit, or advise;
- artifact boundary: supplied paper, repository, bibliography, proof, or parameter set;
- evidence boundary: sources that may be searched or inspected;
- mutation boundary: whether the skill may modify files or only report findings;
- conclusion boundary: what the output may and may not certify.

For example, “review a proof” must say whether the task checks local derivations, reconstructs omitted arguments, checks mechanized artifacts, or evaluates only presentation completeness.

## 4. Use observable success criteria

Avoid criteria such as “high quality,” “rigorous,” or “comprehensive” without observable tests. Prefer:

- every claim is assigned a claim type and evidence status;
- every citation has a verified identity or is explicitly marked unverified;
- every parameter symbol has a definition, unit/domain, and consistent value;
- every complexity claim names its cost model and regime;
- every blocking issue has a location, consequence, and required evidence for resolution;
- the output separates verified conclusions from assumptions and open questions.

Success criteria should remain valid across harnesses. “Called tool X” is not a research outcome; “verified the DOI against a primary landing page” is.

## 5. Specify failure behavior before the happy path

Research workflows often fail because evidence is missing, not because syntax is invalid. Define what happens when:

- a source is inaccessible or only a snippet is available;
- multiple versions of a paper disagree;
- theorem numbering differs across versions;
- a proof omits a lemma or uses undefined notation;
- parameters are incomplete or inconsistent;
- a security model is unstated;
- a literature search lacks database access, date coverage, or citation chaining;
- a mechanized proof/checker cannot be executed;
- the user asks for certainty that the evidence cannot support.

Choose one response per condition: stop, ask, narrow the claim, mark unverified, or return a partial result. Never silently infer research-critical facts.

## 6. Progressive disclosure

Keep `SKILL.md` focused on routing, shared invariants, the main contract, and the minimum workflow. Move conditional detail into references.

Use a reference when it is:

- needed only for one mode, domain, or output type;
- long enough to obscure the main workflow;
- a maintained schema, checklist, protocol, or convention;
- useful to consult independently.

Every reference must be linked from `SKILL.md` or another referenced file, with a sentence explaining when to read it. Do not duplicate the same rule in several files; choose one authoritative location.

## 7. Portable core, optional adapters

The portable core should describe capabilities rather than vendor-specific tools.

| Portable instruction | Non-portable coupling |
|---|---|
| Search primary scholarly indexes and record queries. | Call a particular proprietary search connector. |
| Inspect the exact cited version or mark it unavailable. | Assume browser session state exists. |
| Run an available proof checker and retain its output. | Require a named IDE command. |
| Parallelize independent searches when supported. | Require a fixed number of subagents. |

Portability rules:

- use UTF-8 Markdown and relative paths;
- do not depend on shell type, operating system, or home-directory layout;
- do not assume network, browser, PDF parser, theorem prover, or reference manager access;
- list optional dependencies beside the step that needs them;
- define an honest degraded mode when an optional capability is absent;
- keep harness metadata and permission declarations in optional adapters;
- use deterministic scripts only when they materially improve repeatability, and document runtime/dependencies.

## 8. Match instruction strength to research risk

Use absolute language for integrity and category errors:

- never fabricate sources or verification;
- never turn a proof sketch into a proved theorem;
- never claim novelty from an undocumented or narrow search;
- never compare costs with incompatible models without qualification.

Use decision criteria rather than rigid sequences where legitimate methods vary. Literature sources, proof techniques, estimators, and theorem provers evolve; the skill should specify evidence requirements and version recording rather than freeze one tool forever.

## 9. Separate mechanical and judgment checks

Mechanical checks belong in a script when stable:

- folder/frontmatter naming;
- required sections;
- broken relative links;
- unresolved scaffold tokens;
- encoding or parse errors.

Judgment checks belong in instructions/checklists:

- whether a proof establishes the stated notion;
- whether a reduction loss is acceptable;
- whether a parameter set meets a target security level;
- whether a search supports a bounded novelty statement;
- whether a citation actually supports the nearby claim.

A passing linter never means a research skill is correct.

## 10. Create, audit, and refactor modes

### Create

1. Elicit representative positive/negative requests and desired artifacts.
2. Define the contract table.
3. Identify research-integrity risks and domain checks.
4. Choose the smallest useful file structure.
5. Instantiate the template and replace every intentional token.
6. Validate structurally and with realistic scenarios.

### Audit

1. Preserve the original files.
2. Report findings by severity, each with evidence and consequence.
3. Distinguish missing instruction, contradictory instruction, non-portable coupling, and domain error.
4. Do not rewrite unless requested.

### Refactor

1. Record observable behavior and correct user choices to preserve.
2. Fix blocking findings before style or concision.
3. Remove duplication and move conditional detail into references.
4. Re-run the same scenarios and report behavior changes.

## 11. Behavioral evaluation

Static validation is necessary but insufficient. Test the skill with realistic requests in a fresh context when the harness supports it.

Minimum scenario set:

- a normal in-scope request;
- a close non-trigger request;
- incomplete evidence;
- conflicting paper versions;
- pressure to give a definitive novelty/security verdict;
- a ZKP request with an unstated model;
- a lattice parameter set with ambiguous norm/distribution;
- a capability gap such as no web or no proof checker.

Record whether the agent triggered correctly, requested only material clarification, preserved uncertainty, avoided fabrication, and produced the promised output shape. Do not claim behavioral validation if no independent run occurred.

## 12. Common design failures

| Failure | Consequence | Repair |
|---|---|---|
| Broad description | Skill activates on unrelated research | Add concrete triggers and non-triggers |
| Topic-only scope | Agent expands task or certifies too much | Add action, artifact, evidence, mutation, and conclusion boundaries |
| Process-only success | Agent follows steps but produces unverifiable output | Define observable artifacts and evidence status |
| Tool-specific core | Skill breaks on another harness | Express capability outcome; move tool mapping to adapter |
| Citation reminder without protocol | Plausible but false references survive | Require identity, version, access, and claim-support verification |
| One generic “proof check” | Theorem, reduction, and security notions blur | Apply the claim taxonomy and domain matrices |
| Static linter treated as certification | Semantically wrong skill passes | Add judgment checklist and behavioral scenarios |

