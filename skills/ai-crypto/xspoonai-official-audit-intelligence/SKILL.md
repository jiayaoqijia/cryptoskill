---
name: audit-intelligence
description: Query Solodit audit knowledge to review smart contracts with evidence-backed findings, severity summaries, and remediation guidance. Use for contract audit prep, vulnerability triage, and secure coding reviews.
version: 1.0.0
author: Community Contributor
tags: [web3, security, audit, solodit]
---

# Audit Intelligence

Use Solodit findings as a structured knowledge layer for smart contract auditing.

## Quick Start

```python
from spoon_ai.agents import SpoonReactSkill

agent = SpoonReactSkill(
    name="audit_agent",
    skill_paths=["./web3-data-intelligence"],
    scripts_enabled=True
)
await agent.activate_skill("audit-intelligence")

result = await agent.run("Find recent HIGH reentrancy audit findings and summarize mitigations")
print(result)
```

## Scripts

| Script | Purpose |
|--------|---------|
| [solodit_client.py](scripts/solodit_client.py) | Shared Solodit API client and schema normalization |
| [solodit_search.py](scripts/solodit_search.py) | Query findings by keyword/severity |
| [solodit_contract_findings.py](scripts/solodit_contract_findings.py) | Aggregate findings for a project or contract |
| [audit_pattern_matcher.py](scripts/audit_pattern_matcher.py) | Pattern match Solidity snippets + fetch similar findings |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SOLODIT_API_KEY` | Yes | Solodit API key |
| `SOLODIT_API_BASE` | No | API base URL. Default: `https://api.solodit.xyz/v1` |
| `SOLODIT_TIMEOUT_SECONDS` | No | Request timeout seconds. Default: `20` |

## Best Practices

1. Search findings first, then run project-level aggregation for context.
2. Always include source links when reporting risks to users.
3. Combine pattern matching with manual review for critical contracts.
4. Prefer actionable remediation text over generic warnings.