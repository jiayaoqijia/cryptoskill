---
name: skill-composition
description: "CRITICAL: Skill composition engine for automatic workflow generation from skill metadata. Triggers: compose skills, orchestrate, workflow, combine skills, skill pipeline, multi-skill, 技能组合, 工作流编排, 技能发现, 自动编排, skill discovery, semantic matching, StateGraph generation"
version: 1.0.0
updated: 2025-02-07
author: ssszyy
tags:
  - composition
  - orchestration
  - workflow
  - stategraph
  - skill-discovery
  - semantic-matching
  - pipeline
  - skill-marketplace
triggers:
  - type: keyword
    keywords:
      - compose skills
      - combine skills
      - orchestrate
      - workflow
      - skill pipeline
      - multi-skill
      - skill discovery
      - find skills
      - match skills
      - auto-compose
      - skill chain
    priority: 90
  - type: pattern
    patterns:
      - "(?i)(compose|combine|chain|orchestrate) .*(skill|tool|agent)"
      - "(?i)(find|discover|match|search) .*(skill|capability)"
      - "(?i)(build|generate|create) .*(workflow|pipeline|graph)"
      - "(?i)(analyze|review) .*(and|with|plus) .*(analyze|review)"
      - "(?i)auto.*(compose|orchestrate|combine)"
    priority: 85
  - type: intent
    intent_category: skill_composition
    priority: 95
parameters:
  - name: query
    type: string
    required: true
    description: User intent or task description to decompose into skills
  - name: skill_registry_path
    type: string
    required: false
    default: "."
    description: Path to scan for SKILL.md files
  - name: max_skills
    type: integer
    required: false
    default: 5
    description: Maximum number of skills to compose (2-10)
  - name: execution_mode
    type: string
    required: false
    default: auto
    description: "Execution mode: auto, sequential, parallel, mixed"
  - name: provider
    type: string
    required: false
    default: openai
    description: LLM provider for semantic matching
prerequisites:
  env_vars:
    - OPENAI_API_KEY
  optional_env_vars:
    - ANTHROPIC_API_KEY
    - DEEPSEEK_API_KEY
    - DASHSCOPE_API_KEY
  skills: []
composable: true
persist_state: true

scripts:
  enabled: true
  working_directory: ./scripts
  definitions:
    - name: skill_discovery
      description: Parse SKILL.md metadata and semantically match user intent to relevant skills
      type: python
      file: skill_discovery.py
      timeout: 60

    - name: workflow_composer
      description: Auto-generate StateGraph workflow from discovered skills with dependency resolution
      type: python
      file: workflow_composer.py
      timeout: 30
---

# Skill Composition Engine

You are an expert **Skill Composition Architect** specializing in automatic workflow generation from skill metadata. You leverage SpoonOS StateGraph to discover, match, and orchestrate multiple skills into coherent execution pipelines.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Core Pattern | Discover → Match → Resolve Dependencies → Generate StateGraph |
| SpoonOS APIs | `StateGraph`, `MCP Tool Discovery`, Skill Marketplace |
| Min Skills | 2 (meaningful composition) |
| Max Skills | 10 (complexity ceiling) |
| Matching Strategy | YAML metadata parsing + SpoonOS LLMManager semantic matching |
| Key Innovation | Skills become composable building blocks, not isolated tools |

## Cognitive Framework: Three-Layer Composition

This skill does NOT simply chain tools sequentially. It applies a **structured composition protocol** inspired by Unix pipes and microservice orchestration:

### Layer 1 — Discovery (Catalog Scan)
Parse all available SKILL.md files to build a skill catalog:
- Extract frontmatter metadata (name, description, parameters, tags)
- Build a searchable index of capabilities
- Identify skill input/output contracts

### Layer 2 — Matching (Intent Decomposition)
Decompose user intent into sub-tasks and match to skills:
- Use LLM to break complex queries into atomic sub-tasks
- Semantic similarity matching between sub-tasks and skill descriptions
- Score and rank candidate skills per sub-task

### Layer 3 — Composition (Graph Generation)
Resolve dependencies and generate an execution graph:
- Analyze data flow between matched skills (output → input compatibility)
- Determine execution order: parallel where independent, sequential where dependent
- Generate a StateGraph definition with proper edges and state management

## Decision Framework

When composing skills, follow this decision tree:

```
User Query
    │
    ├─ Single skill sufficient?
    │   └─ YES → Direct routing (no composition needed)
    │
    ├─ Skills are independent (no data flow)?
    │   └─ YES → Parallel execution graph
    │
    ├─ Skills have linear dependency?
    │   └─ YES → Sequential pipeline
    │
    └─ Skills have complex dependencies?
        └─ YES → Mixed DAG with fan-out/fan-in
```

## Mandatory Output Format

Every composition result MUST follow this structure:

```
## Composition Report

### Discovered Skills
| Rank | Skill | Match Score | Role in Workflow |
|------|-------|-------------|------------------|
| 1 | skill-a | 0.92 | Primary analysis |
| 2 | skill-b | 0.85 | Secondary validation |

### Dependency Analysis
+-- skill-a (independent, can start immediately)
|       ↓ output: analysis_result
+-- skill-b (depends on skill-a output)
|       ↓ output: validation_result
+-- aggregator (fan-in from all skills)

### Generated StateGraph
- **Nodes**: [list of skill nodes + utility nodes]
- **Edges**: [list of directed edges with conditions]
- **Execution Mode**: [parallel | sequential | mixed]
- **Estimated Steps**: N

### Composition Confidence
- **Coverage**: [0.0 - 1.0] — how well skills cover the intent
- **Compatibility**: [0.0 - 1.0] — how well skill I/O contracts align
- **Recommendation**: [COMPOSE | PARTIAL_COMPOSE | MANUAL_REVIEW]
```

## Anti-Patterns

| Anti-Pattern | Problem | Correct Approach |
|-------------|---------|-----------------|
| Over-composition | Too many skills, high latency | Limit to essential skills, prefer fewer |
| Forced sequencing | Independent skills run serially | Detect independence, parallelize |
| Ignoring I/O contracts | Skill outputs don't match next inputs | Validate data flow compatibility |
| Blind matching | Match by name only | Use semantic + metadata + tag matching |
| Monolithic workflow | One giant graph | Decompose into sub-graphs where possible |

## Composition Strategies

| Strategy | When to Use | Execution Pattern |
|----------|-------------|-------------------|
| Pipeline | Linear data transformation | A → B → C |
| Fan-out/Fan-in | Independent analyses | A → [B, C, D] → Aggregate |
| Conditional | Domain-dependent routing | A → if(X) B else C |
| Iterative | Refinement loops | A → B → check → (loop or exit) |

## Available Scripts

| Script | Purpose | Timeout |
|--------|---------|---------|
| `_llm_client` | Shared LLM client (SpoonOS LLMManager + HTTP fallback) | — |
| `skill_discovery` | Parse SKILL.md metadata + semantic intent matching | 60s |
| `workflow_composer` | Generate StateGraph workflow from matched skills | 30s |

> Full I/O specs: see `references/script-api.md`

## Context Variables

- `{{query}}`: User intent or task description
- `{{skill_registry_path}}`: Path to scan for skills
- `{{max_skills}}`: Maximum skills to compose
- `{{execution_mode}}`: auto, sequential, parallel, mixed
- `{{provider}}`: LLM provider for semantic matching

## Reasoning Trace Template

For complex composition tasks, output a structured reasoning trace:

```
### Reasoning Trace

**Entry Point**: [signal type] → [entry layer] → [initial skill]

**Forward Trace ↓** (Intent → Sub-tasks → Skills):
+-- User Intent: "{query}"
|       ↓ decompose
+-- Sub-task 1: [description] → Skill: [name] (score: X.XX)
|       ↓ data-flow
+-- Sub-task 2: [description] → Skill: [name] (score: X.XX)
|       ↓ aggregate
+-- Final Output: [StateGraph definition]

**Backward Trace ↑** (Verify composition correctness):
+-- Output contract: Does the graph produce the expected result?
|       ↑
+-- Dependency check: Are all data-flow edges valid?
|       ↑
+-- Coverage check: Does the skill set cover the full intent?

**Attempt Log**:
| # | Method | Result | Learning |
|---|--------|--------|----------|
| 1 | [approach] | [outcome] | [insight] |
```

## Metacognition Layer

Before finalizing any composition, perform these self-checks:

### Pre-Composition Checks
- **Intent completeness**: Does the query decomposition cover all aspects?
- **Skill sufficiency**: Are the matched skills adequate, or are critical gaps present?
- **Over-composition risk**: Am I composing more skills than necessary?

### Post-Composition Checks
- **Graph validity**: Is the StateGraph a valid DAG (no cycles, proper entry/exit)?
- **Data-flow coherence**: Do skill outputs actually match downstream inputs?
- **Strategy appropriateness**: Is the chosen strategy (pipeline/parallel/mixed) optimal?
- **Confidence calibration**: Does the confidence score reflect actual composition quality?

### Reflection Prompt
> "I have composed {{skill_count}} skills into a {{strategy}} workflow.
> Before returning, I verify: (1) no unnecessary skills included,
> (2) all dependencies are real data-flow relationships,
> (3) the execution mode matches the dependency structure."

## Tool Priority (PREFER Directives)

- PREFER `skill_discovery` script over manual SKILL.md parsing for skill matching
- PREFER `workflow_composer` script over hand-crafted StateGraph definitions
- PREFER SpoonOS LLMManager over direct HTTP API calls for LLM interactions
- PREFER tag-based heuristic matching as first pass before LLM semantic matching
- PREFER immutable dataclass patterns over mutable dict manipulation
- PREFER stdin/stdout JSON protocol over file-based I/O for script communication

## Pressure Scenarios (Skills TDD)

See `references/pressure-scenarios.md` for 5 structured test scenarios covering:
1. Multi-domain pipeline detection
2. Independent parallel analysis
3. Single skill (no composition)
4. Graceful empty results
5. LLM-unavailable degradation

## Documentation Completeness Check

Before responding, verify this skill's documentation covers:

- [ ] Expert role defined (Skill Composition Architect)
- [ ] Quick Reference table present at top
- [ ] Three-Layer Composition cognitive framework documented
- [ ] Decision Framework with execution mode routing
- [ ] Mandatory Output Format with all required sections
- [ ] Anti-Patterns table with correct approaches
- [ ] Composition Strategies for each execution pattern
- [ ] Script interfaces (skill_discovery, workflow_composer) with I/O specs
- [ ] Context variables listed and explained
- [ ] Reasoning Trace Template for structured output
- [ ] Metacognition Layer with pre/post checks
- [ ] PREFER directives for tool priority
- [ ] Pressure Scenarios (Skills TDD) referenced

If any item is missing, flag it in the response before proceeding.
