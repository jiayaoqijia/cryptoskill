---
name: output-enforcer
description: "Validate AI agent tool outputs against pydantic schemas with auto-retry, disk-backed persistence, and circuit breaker protection. Hardened for production deployments."
---

# Output Enforcer

A middleware plugin for the GenTech Agent Kit that validates every tool output against its declared pydantic schema. Designed for production: survives VPS reboots, process crashes, and API failures.

## Installation

Already included in the Agent Kit. Plugin auto-discovered at startup.

## Usage

```python
from gentech_agent_kit.plugins.output_enforcer import validated_output
from gentech_agent_kit.plugins.output_enforcer.schemas import QuoteResponse

@mcp.tool()
@validated_output(QuoteResponse)
def get_quote(symbol: str) -> str:
    ...
```

## Features

### Schema Validation
Tool output is parsed as JSON and validated against a pydantic BaseModel. If the output doesn't match the schema, the enforcer retries (default: 1 retry) before returning a structured error.

### Disk-Backed Storage
All violations are persisted to `~/.agent-kit/data/output-enforcer/violations.json`. Survives VPS reboots and process crashes. Atomic writes (temp file + rename) prevent corruption.

### Circuit Breaker
If a tool fails validation 5 consecutive times, the circuit breaker trips:
- 60s cooldown (doubles per breach, max 1 hour)
- Tool returns "temporarily unavailable" instead of burning retries
- Auto-recovers after cooldown expires

### Audit Tools

| Tool | Description |
|------|-------------|
| `output_enforcer_status()` | Plugin health, violation count, broken tools |
| `output_enforcer_violations(tool, hours)` | Recent violations with filter |
| `output_enforcer_clear()` | Reset all violations |
| `output_enforcer_breakers()` | Circuit breaker state per tool |

## Available Schemas

| Schema | For Tool |
|--------|----------|
| `QuoteResponse` | `get_quote()` |
| `ListingsResponse` | `get_listings()` |
| `SearchResponse` | `search_token()` |
| `TrendingResponse` | `get_trending()` |
| `DexPairsResponse` | `get_dex_pairs()` |
| `KitInfoResponse` | `kit_info()` |

## Best Practices

- Start with `max_retries=1` (default). Increase only for flaky API-based tools.
- Use strict schemas for payment-gated tools (you don't want to bill for bad data).
- Check `output_enforcer_breakers()` weekly to spot chronically failing tools.
- Combine with the Agent Kit's error handling for full production hardening.
