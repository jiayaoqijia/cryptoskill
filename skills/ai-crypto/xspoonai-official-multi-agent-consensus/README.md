# Multi-Agent Consensus Engine

> **Byzantine Fault Tolerant** multi-model analysis for SpoonOS — reduce LLM hallucinations through parallel agent consensus.

## Problem

Single-LLM analysis suffers from:
- **Hallucination blind spots** — one model's confident error goes unchallenged
- **Provider bias** — each LLM has systematic strengths/weaknesses
- **No confidence calibration** — a single model can't self-assess reliability

## Solution

Inspired by **Byzantine Fault Tolerance (BFT)**, this skill runs the same query across multiple LLM providers in parallel, then aggregates results through weighted voting. Just as BFT tolerates up to ⌊(n-1)/3⌋ faulty nodes, our consensus engine tolerates minority hallucinations.

```
┌─────────────────────────────────────────────────────┐
│                   StateGraph Flow                    │
│                                                      │
│  entry → fan_out → ┬─ agent_1 (OpenAI/analytical)   │
│                    ├─ agent_2 (Anthropic/adversarial)│
│                    ├─ agent_3 (DeepSeek/pragmatic)   │
│                    └─ agent_n (Gemini/domain_expert) │
│                         │                            │
│                    fan_in → voting_aggregator         │
│                         │                            │
│                    consensus_result                   │
└─────────────────────────────────────────────────────┘
```

## Architecture

### Two-Script Pipeline

| Script | Role | SpoonOS Mapping |
|--------|------|-----------------|
| `consensus_engine.py` | Parallel multi-agent orchestration | StateGraph fan-out/fan-in |
| `voting_aggregator.py` | Weighted voting & agreement analysis | Post-processing node |

### Cognitive Diversity

Each agent receives a different **perspective prompt** to maximize viewpoint diversity:

| Perspective | Focus | Best For |
|-------------|-------|----------|
| Analytical | Systematic decomposition | General analysis |
| Adversarial | Attack surface, edge cases | Security audits |
| Pragmatic | Real-world impact, feasibility | DeFi review |
| Domain Expert | Deep technical knowledge | Smart contracts |
| Generalist | Broad patterns, cross-domain | Exploratory |

### Four Consensus Modes

| Mode | Strategy | Domain |
|------|----------|--------|
| `majority` | Weighted majority vote | General |
| `conservative` | Any risk flag → escalate | Security, Smart Contracts |
| `union` | Merge all findings, deduplicate | DeFi |
| `diversity` | Preserve all perspectives | Exploratory |

## Usage

### Prerequisites

- Python 3.11+
- API keys for at least 2 LLM providers (set as environment variables):

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="sk-..."        # optional
export GEMINI_API_KEY="AIza..."          # optional
```

### Running the Consensus Engine

```bash
echo '{
  "query": "Analyze this Solidity function for reentrancy vulnerabilities:\n\nfunction withdraw(uint amount) public {\n    require(balances[msg.sender] >= amount);\n    (bool success, ) = msg.sender.call{value: amount}(\"\");\n    require(success);\n    balances[msg.sender] -= amount;\n}",
  "agents": 3,
  "providers": ["openai", "anthropic", "deepseek"],
  "domain": "smart-contract",
  "threshold": 0.6
}' | python3 scripts/consensus_engine.py
```

### Running the Voting Aggregator

Pipe the engine output directly into the aggregator:

```bash
echo '{...engine output...}' | python3 scripts/voting_aggregator.py
```

Or chain them in a full pipeline:

```bash
echo '{"query": "...", "agents": 3}' \
  | python3 scripts/consensus_engine.py \
  | python3 scripts/voting_aggregator.py
```

### Example Output

```json
{
  "success": true,
  "domain": "smart-contract",
  "consensus": {
    "verdict": "CRITICAL_RISK",
    "confidence": 0.92,
    "method": "conservative",
    "escalation_triggers": 2
  },
  "agreement_map": {
    "agreed": [
      {
        "canonical": "Classic reentrancy: state update after external call",
        "sources": ["agent-1", "agent-2", "agent-3"],
        "count": 3,
        "avg_confidence": 0.91
      }
    ],
    "disputed": [],
    "unique": [
      {
        "canonical": "Potential gas griefing via fallback function",
        "sources": ["agent-2"],
        "count": 1,
        "avg_confidence": 0.65
      }
    ]
  },
  "statistics": {
    "total_agents": 3,
    "valid_votes": 3,
    "error_agents": 0,
    "total_findings": 5,
    "finding_clusters": 3,
    "agreed_findings": 2,
    "disputed_findings": 0,
    "unique_findings": 1
  }
}
```

## SpoonOS Integration

### StateGraph Mapping

The consensus engine maps directly to SpoonOS StateGraph primitives:

```python
# Production SpoonOS integration (conceptual)
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver

graph = StateGraph(ConsensusState)
graph.add_node("fan_out", build_agent_configs_node)
graph.add_node("agent_1", agent_node_factory("agent-1"))
graph.add_node("agent_2", agent_node_factory("agent-2"))
graph.add_node("agent_3", agent_node_factory("agent-3"))
graph.add_node("fan_in", aggregate_node)

graph.add_edge("fan_out", "agent_1")
graph.add_edge("fan_out", "agent_2")
graph.add_edge("fan_out", "agent_3")
graph.add_edge("agent_1", "fan_in")
graph.add_edge("agent_2", "fan_in")
graph.add_edge("agent_3", "fan_in")

compiled = graph.compile(checkpointer=MemorySaver())
```

### LLMManager Integration

The multi-provider abstraction aligns with SpoonOS LLMManager:

| Feature | This Skill | SpoonOS LLMManager |
|---------|-----------|-------------------|
| Multi-provider | OpenAI, Anthropic, DeepSeek, Gemini | Same + custom providers |
| Fallback chains | Per-agent error handling | Automatic provider fallback |
| Rate limiting | Concurrent async calls | Built-in rate limiter |
| Checkpointing | SHA-256 checkpoint IDs | MemorySaver / PostgresSaver |

## Design Principles

This skill follows the **Cognitive Scaffold** approach from the SpoonOS Skill Design Principles:

1. **Not a knowledge dump** — The skill provides a *thinking framework* (multi-perspective analysis + weighted consensus), not just facts
2. **Three-Layer Cognitive Framework** — Surface errors → Structural patterns → Domain-specific rules
3. **Forced Output Format** — Mandatory reasoning chain with verdict, confidence, findings, and reasoning
4. **Anti-Pattern Awareness** — Built-in guards against single-model reliance, confirmation bias, and unweighted averaging
5. **Domain-Specific Weights** — Provider expertise varies by domain (e.g., Anthropic excels at security analysis)

## File Structure

```
multi-agent-consensus/
├── SKILL.md                    # Skill definition with CSO-optimized metadata
├── README.md                   # This file
└── scripts/
    ├── consensus_engine.py     # Parallel multi-agent orchestration (~600 lines)
    └── voting_aggregator.py    # Weighted voting & agreement analysis (~430 lines)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | *required* | The analysis question or code to review |
| `agents` | integer | 3 | Number of parallel agents (2-5) |
| `providers` | string[] | `["openai","anthropic","deepseek"]` | LLM providers to use |
| `threshold` | float | 0.6 | Consensus confidence threshold (0.0-1.0) |
| `domain` | string | `"general"` | Analysis domain: general, smart-contract, defi, security |

## License

MIT
