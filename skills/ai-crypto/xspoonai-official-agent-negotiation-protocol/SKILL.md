---
name: agent-negotiation-protocol
description: |
  CRITICAL: You are an expert in multi-agent negotiation, game theory, and automated settlement protocols.
  Use this skill for designing and implementing agent-to-agent negotiation workflows with x402 payment settlement.
  Triggers on: negotiation, bargaining, agent trade, service agreement, SLA, price negotiation,
  x402 settlement, agent economy, "agents negotiate", "how do agents negotiate prices",
  "implement agent bargaining", "multi-round negotiation", "automated deal-making",
  "自动谈判", "智能体协商", "服务协议", "价格谈判", "多轮协商", "agent 经济"
version: 1.0.0
author: bonujel
tags: [negotiation, x402, stategraph, multi-agent, game-theory, settlement]
updated: 2025-01-01
---

# Agent Negotiation Protocol

## Quick Reference

| Aspect | Detail |
|--------|--------|
| **Pattern** | StateGraph multi-round cyclic workflow |
| **Parties** | Buyer agent ↔ Seller agent |
| **Strategy** | Progressive concession (game-theoretic ZOPA convergence) |
| **Settlement** | x402 payment protocol (HTTP 402 → sign → verify → pay) |
| **Reputation** | ERC-8004 identity scoring (exponential moving average) |
| **Max Rounds** | 5 (configurable) |
| **Scripts** | `scripts/negotiation_engine.py`, `scripts/x402_settlement.py` |
| **Examples** | `examples/basic_negotiation.py`, `examples/custom_strategy.py` |

## Decision Framework

When implementing agent negotiation, follow this layered reasoning:

### Layer 1 — Parameter Validation & Sanity Checks

Before starting any negotiation, verify:

1. **Budget feasibility**: Is `buyer_budget > 0` and `seller_base_price > 0`?
2. **ZOPA existence**: Can the buyer's max concession ceiling ever reach the seller's min floor?
   - Buyer ceiling at round N: `budget × (1 + 0.15 × (N-1))`
   - Seller floor at round N: `base_price × (1 - 0.12 × (N-1))`
   - If ceiling never ≥ floor within max_rounds → negotiation will always fail
3. **Intent clarity**: Are `buyer_intent` and `seller_capability` specific enough for LLM reasoning?

### Layer 2 — Strategy & Workflow Design

Choose the negotiation topology:

| Scenario | Recommended Approach |
|----------|---------------------|
| Simple price-only | Direct concession model (default) |
| Multi-dimensional (price + SLA + delivery) | Weighted utility scoring |
| Adversarial / untrusted parties | Add reputation threshold gate before negotiation |
| High-value transactions | Add human-in-the-loop approval before settlement |

Design the StateGraph workflow:

```
buyer_propose → seller_evaluate → [settle | buyer_decide | abort]
                                    buyer_decide → [settle | seller_evaluate | abort]
```

Key routing decisions:
- **Accept**: Counterparty's offer meets or exceeds threshold → route to `settle`
- **Counter**: Gap exists but within concession range → route back to negotiation loop
- **Reject/Timeout**: Gap too large or max rounds exceeded → route to `abort`

### Layer 3 — Domain Constraints & Game Theory

Apply these domain-specific rules:

1. **Concession asymmetry**: Buyer concedes faster (15%) than seller (12%) — this models real-world power dynamics where buyers typically have more alternatives
2. **ZOPA convergence**: The Zone of Possible Agreement naturally emerges around round 3:
   ```
   Round 1: Buyer $50.00 ←── gap ──→ Seller $80.00
   Round 2: Buyer $57.50 ←─ gap ─→ Seller $70.40
   Round 3: Buyer $65.00 ← → Seller $60.80  ← ZOPA overlap!
   ```
3. **Reputation gating**: PREFER filtering counterparties with `score < 0.3` before entering negotiation
4. **Settlement atomicity**: x402 payment must be atomic — either fully settled or fully rolled back

## Anti-Patterns

| Anti-Pattern | Problem | Correct Approach |
|-------------|---------|-----------------|
| Fixed-price offers | No convergence, wastes rounds | Use progressive concession with configurable rates |
| Unlimited rounds | Resource waste, no termination guarantee | Set `max_rounds` (default: 5) |
| Trusting all counterparties | Vulnerable to reputation manipulation | Gate on `reputation.score ≥ threshold` |
| Hardcoded concession rates | Inflexible across different deal sizes | Scale rates by deal magnitude or use adaptive rates |
| Skipping settlement verification | Payment may fail silently | Always check `SettlementResult.status == "confirmed"` |
| Mutable state in negotiation | Race conditions, debugging difficulty | Use frozen dataclasses, return new state per round |

## Required Output Format

When reporting negotiation results, enforce this structure:

```
### Negotiation Trace
+-- Layer 1: [Parameter validation result]
|       ↓
+-- Layer 2: [Strategy selected, workflow topology]
|       ↓
+-- Layer 3: [Domain constraints applied, ZOPA analysis]

### Round-by-Round Log
| Round | Role   | Action  | Price   | SLA      | Reasoning |
|-------|--------|---------|---------|----------|-----------|
| 1     | buyer  | propose | $50.00  | standard | ...       |
| 1     | seller | counter | $75.00  | premium  | ...       |
| ...   | ...    | ...     | ...     | ...      | ...       |

### Settlement
- Status: [agreed/rejected/timeout]
- Final Price: $X.XX
- TX Hash: 0x...
- Reputation Update: buyer=X.XX, seller=X.XX
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DASHSCOPE_API_KEY` | Yes | — | Qwen API key ([get one](https://dashscope.console.aliyun.com/apiKey)) |
| `QWEN_MODEL` | No | `qwen-plus` | Qwen model name |

## Completeness Checklist

Before considering a negotiation implementation complete, verify:

- [ ] ZOPA feasibility checked before starting negotiation
- [ ] Max rounds configured and enforced
- [ ] Concession rates appropriate for deal size
- [ ] LLM JSON parsing has error handling with retry
- [ ] Settlement result status verified (not assumed)
- [ ] Reputation updated for both parties after settlement
- [ ] Failed negotiations also update reputation (with `success=False`)
- [ ] No hardcoded API keys in source code
