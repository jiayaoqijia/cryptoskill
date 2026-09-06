# Script API Reference

## consensus_engine

Orchestrates parallel multi-agent analysis using SpoonOS StateGraph.

**Input (JSON via stdin):**
```json
{
  "query": "Analyze this smart contract for security vulnerabilities: ...",
  "agents": 3,
  "providers": ["openai", "anthropic", "deepseek"],
  "domain": "smart-contract",
  "threshold": 0.6
}
```

**Output (JSON via stdout):**
```json
{
  "agent_results": [
    {
      "agent_id": "agent-1",
      "provider": "openai",
      "verdict": "VULNERABLE",
      "confidence": 0.85,
      "findings": ["reentrancy in withdraw()", "unchecked return value"],
      "reasoning": "..."
    }
  ],
  "metadata": {
    "total_agents": 3,
    "execution_time_ms": 4500,
    "domain": "smart-contract"
  }
}
```

## voting_aggregator

Aggregates agent results with weighted voting and confidence scoring.

**Input (JSON via stdin):**
```json
{
  "agent_results": [...],
  "domain": "smart-contract",
  "threshold": 0.6
}
```

**Output (JSON via stdout):**
```json
{
  "consensus": {
    "verdict": "CONSENSUS_REACHED",
    "confidence": 0.87,
    "agreed_findings": [...],
    "disputed_findings": [...],
    "unique_findings": [...]
  },
  "agreement_map": {
    "agreed": 5,
    "disputed": 1,
    "unique": 2
  }
}
```
