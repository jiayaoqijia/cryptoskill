# Skill Composition Engine

> **Automatic workflow orchestration** for SpoonOS — discover, match, and compose multiple skills into executable StateGraph pipelines.

## Problem

As the SpoonOS skill ecosystem grows, users face:
- **Discovery friction** — finding the right skills for complex, multi-domain tasks
- **Manual orchestration** — hand-wiring skill pipelines is error-prone and tedious
- **Composition blindness** — no visibility into data-flow dependencies between skills

## Solution

Inspired by **Unix pipes** and **microservice orchestration**, this skill automatically discovers relevant skills via semantic matching, analyzes their data-flow dependencies, and generates a StateGraph DAG that SpoonOS can execute directly.

```
┌──────────────────────────────────────────────────────────┐
│                    Composition Pipeline                    │
│                                                           │
│  User Query                                               │
│      │                                                    │
│      ▼                                                    │
│  ┌─────────────────┐   Three-Layer Matching               │
│  │ skill_discovery  │   1. Keyword filter                 │
│  │                  │   2. Tag scoring                    │
│  │                  │   3. LLM semantic match             │
│  └────────┬────────┘                                      │
│           │ matched skills                                │
│           ▼                                               │
│  ┌─────────────────┐   Dependency Analysis                │
│  │workflow_composer │   • Tag-based heuristics            │
│  │                  │   • LLM semantic analysis           │
│  │                  │   • Strategy auto-detection         │
│  └────────┬────────┘                                      │
│           │ StateGraph DAG                                │
│           ▼                                               │
│  SpoonOS Runtime Execution                                │
└──────────────────────────────────────────────────────────┘
```

## Architecture

### Three-Script Architecture

| Script | Role | SpoonOS Mapping |
|--------|------|-----------------|
| `_llm_client.py` | Shared LLM client (SpoonOS LLMManager + HTTP fallback) | LLM abstraction layer |
| `skill_discovery.py` | Parse SKILL.md metadata + semantic intent matching | `graph.add_node("discover", ...)` |
| `workflow_composer.py` | Dependency analysis + StateGraph DAG generation | `graph.add_node("compose", ...)` |

### Three-Layer Skill Matching

```
Layer 1 — Keyword Filter (fast, zero-cost)
    Jaccard-inspired token overlap between query and skill metadata

Layer 2 — Tag Scoring (fast, zero-cost)
    Curated tag taxonomy matching against skill metadata tags

Layer 3 — LLM Semantic Match (accurate, API cost)
    Multi-provider LLM analysis of intent-to-skill alignment

Final Score = 0.4 × base_score + 0.6 × llm_score
```

### Composition Strategies

| Strategy | Pattern | When Detected |
|----------|---------|---------------|
| Direct | `A` | Single skill sufficient |
| Pipeline | `A → B → C` | Linear data dependencies |
| Fan-out/Fan-in | `[A, B, C] → Aggregate` | Independent parallel analyses |
| Mixed DAG | Complex graph | Multiple dependency patterns |

## Usage

### Pipeline Mode (discovery → composition)

```bash
echo '{"query": "analyze DeFi protocol security and profitability"}' \
  | python scripts/skill_discovery.py \
  | python scripts/workflow_composer.py
```

### Direct Composition (with pre-matched skills)

```bash
echo '{
  "query": "audit smart contract and generate report",
  "matches": [
    {
      "skill_name": "Smart Contract Auditor",
      "score": 0.92,
      "tier": "semantic",
      "metadata": {
        "description": "Automated smart contract security analysis",
        "tags": ["security", "audit", "smart-contract"],
        "composable": true,
        "scripts": ["audit_engine.py"],
        "parameters": []
      }
    },
    {
      "skill_name": "Report Generator",
      "score": 0.85,
      "tier": "tag",
      "metadata": {
        "description": "Generate structured audit reports",
        "tags": ["report", "documentation"],
        "composable": true,
        "scripts": ["report_gen.py"],
        "parameters": []
      }
    }
  ],
  "execution_mode": "auto"
}' | python scripts/workflow_composer.py
```

### Output Example

```json
{
  "success": true,
  "query": "audit smart contract and generate report",
  "skill_count": 2,
  "strategy": "pipeline",
  "execution_mode": "sequential",
  "graph": {
    "nodes": [
      {"id": "__start__", "type": "entry"},
      {"id": "smart_contract_auditor", "type": "skill"},
      {"id": "report_generator", "type": "skill"},
      {"id": "__end__", "type": "terminal"}
    ],
    "edges": [
      {"source": "__start__", "target": "smart_contract_auditor"},
      {"source": "smart_contract_auditor", "target": "report_generator"},
      {"source": "report_generator", "target": "__end__"}
    ]
  },
  "confidence": {
    "coverage": 0.885,
    "compatibility": 0.8,
    "recommendation": "COMPOSE"
  }
}
```

## SpoonOS Integration

### StateGraph Mapping

```python
from langgraph.graph import StateGraph

graph = StateGraph(CompositionState)
graph.add_node("discover", run_skill_discovery)
graph.add_node("compose", run_workflow_composer)
graph.add_edge("__start__", "discover")
graph.add_edge("discover", "compose")
graph.add_edge("compose", "__end__")
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | For LLM matching | OpenAI API key |
| `ANTHROPIC_API_KEY` | For LLM matching | Anthropic API key |
| `DEEPSEEK_API_KEY` | For LLM matching | DeepSeek API key |

> At least one API key is needed for LLM-enhanced matching. Without any key, the engine falls back to keyword + tag matching only.

## Design Principles

| Principle | Implementation |
|-----------|---------------|
| **SpoonOS native** | Integrates LLMManager with stdlib HTTP fallback (three-level degradation) |
| **Immutable state** | All domain types use `@dataclass(frozen=True)` |
| **Composable I/O** | stdin/stdout JSON protocol, Unix pipe compatible |
| **Graceful degradation** | SpoonOS → HTTP fallback → heuristic-only matching |
| **Multi-provider** | OpenAI, Anthropic, DeepSeek — auto-detect from env |
| **DRY** | Shared `_llm_client.py` eliminates duplicate LLM code |

## File Structure

```
skill-composition/
├── SKILL.md                    # Skill metadata + cognitive framework
├── README.md                   # This file
├── scripts/
│   ├── _llm_client.py         # Shared LLM client (SpoonOS + HTTP fallback)
│   ├── skill_discovery.py      # Three-layer skill matching
│   └── workflow_composer.py    # StateGraph DAG generation
└── references/
    └── script-api.md           # Script I/O specification
```

