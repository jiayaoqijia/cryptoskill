# Agent Negotiation Protocol

> Automated multi-round negotiation between AI agents, powered by SpoonOS
> StateGraph and settled via x402 payment protocol.

## Overview

This skill implements a **game-theoretic negotiation protocol** where two AI
agents (buyer and seller) autonomously negotiate price, SLA tier, and delivery
terms through multiple rounds. Upon agreement, the transaction is settled via
the x402 payment protocol with reputation updates for both parties.

**Key Innovation**: Brings mechanism design and bargaining theory into the
AI agent economy — agents are not just tools, they are economic participants
with their own utility functions.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    StateGraph Workflow                       │
│                                                             │
│  ┌──────────┐     ┌──────────────┐     ┌──────────────┐   │
│  │  Buyer   │────→│   Seller     │────→│   Settle     │   │
│  │ Propose  │     │  Evaluate    │     │  (x402 pay)  │   │
│  └──────────┘     └──────┬───────┘     └──────────────┘   │
│       ▲                  │                                  │
│       │           ┌──────▼───────┐                         │
│       └───────────│    Buyer     │                         │
│                   │   Decide     │                         │
│                   └──────────────┘                         │
│                                                             │
│  Conditional routing: accept → settle, counter → loop,     │
│  reject/timeout → abort                                    │
└─────────────────────────────────────────────────────────────┘
```

## SpoonOS Features Used

| Feature | Usage |
|---------|-------|
| **StateGraph** | Multi-round cyclic workflow with conditional routing |
| **x402 Protocol** | Automated USDC payment on agreement |
| **ERC-8004 Identity** | Agent reputation scoring and trust verification |
| **LLM Integration** | Qwen (DashScope) for agent decision-making |

## Installation

```bash
# Install dependencies
pip install httpx python-dotenv

# Configure API key
cp .env.example .env
# Edit .env and set your DASHSCOPE_API_KEY
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DASHSCOPE_API_KEY` | Yes | — | Qwen API key from [DashScope](https://dashscope.console.aliyun.com/apiKey) |
| `QWEN_MODEL` | No | `qwen-plus` | Qwen model to use |

## Usage

### Run Demo

```bash
cd scripts
python negotiation_engine.py
```

### Examples

See the `examples/` directory for complete usage patterns:

- **`basic_negotiation.py`** — Minimal negotiation with default settings
- **`custom_strategy.py`** — ZOPA pre-check + custom parameters + x402 settlement

### Programmatic Usage

```python
import asyncio
from scripts.negotiation_engine import NegotiationEngine

async def main():
    engine = NegotiationEngine(max_rounds=5)
    result = await engine.run_negotiation(
        buyer_intent="On-chain data analysis for 100 wallets",
        seller_capability="Batch wallet profiling service",
        buyer_budget=50.0,
        seller_base_price=80.0,
    )
    print(f"Status: {result.status.value}")
    print(f"Agreed Price: ${result.agreed_price}")

asyncio.run(main())
```

## File Structure

```
agent-negotiation/
├── SKILL.md                          # Skill definition (cognitive scaffold)
├── README.md                         # This file
├── .env.example                      # API key template
├── .gitignore                        # Excludes .env and caches
├── scripts/
│   ├── negotiation_engine.py         # StateGraph negotiation state machine
│   └── x402_settlement.py            # x402 payment + reputation tracking
└── examples/
    ├── basic_negotiation.py          # Minimal usage example
    └── custom_strategy.py            # ZOPA check + settlement example
```

## API Reference

### NegotiationEngine

| Method | Parameters | Returns |
|--------|-----------|---------|
| `run_negotiation()` | `buyer_intent`, `seller_capability`, `buyer_budget`, `seller_base_price` | `NegotiationResult` |

### X402Settlement

| Method | Parameters | Returns |
|--------|-----------|---------|
| `execute_settlement()` | `agreed_price`, `buyer_id`, `seller_id`, `sla_tier` | `SettlementResult` |
| `create_challenge()` | `seller_id`, `amount`, `asset`, `network` | `PaymentChallenge` |

### Data Models

| Model | Key Fields |
|-------|-----------|
| `NegotiationResult` | `status`, `agreed_price`, `agreed_sla`, `rounds_taken`, `history` |
| `SettlementResult` | `tx_hash`, `amount`, `buyer_reputation_after`, `seller_reputation_after` |
| `AgentReputation` | `agent_id`, `score`, `total_deals`, `successful_deals`, `total_volume` |

## Production Migration

To deploy on SpoonOS production:

```python
# Replace SimpleStateGraph with SpoonOS native
from spoon_ai.graph import StateGraph, END

# Replace mock settlement with real x402
from spoon_ai.payments import X402Client

# Replace mock reputation with ERC-8004
from spoon_ai.identity import IdentityRegistry
```

## License

MIT
