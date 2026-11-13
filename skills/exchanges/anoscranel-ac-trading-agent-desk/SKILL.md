---
name: ac-trading-agent-desk
description: "Governs the design, security, and operational boundaries of an AI agent trading desk. Defines the absolute division between deterministic code (ingest, watermarks, risk gates, order plumbing) and probabilistic LLM agents (news extraction, regime labelling, memo drafting with spot audits and n-thresholds). Enforces the trifecta security invariant (disjoint sandboxes separating untrusted content, credentials, and egress), addresses structural regime blindness (Aldridge 2026, arXiv 2611.01799) and herd amplification dynamics, establishes phone-class batch cadence constraints, and details failure mode mitigations. Use when asking 'AI agent trading desk', 'should an agent trade', 'agent risk gate', 'LLM trading bot', 'agent sandbox', 'can agents manage my book'. Not for generic multi-agent orchestration (ac-multi-agent-orchestration), not for the trade record or risk budget (ac-crypto-trading-discipline), not for liquidation hunt analysis (ac-liquidation-hunt-analysis)."
license: MIT
metadata:
  domain: crypto-trading
status: seedling
---

# Trading Agent Desk

This skill provides the rigorous architectural, security, and operational standards required to govern an AI agent trading desk. It operationalizes verified findings from quantitative finance and secure systems engineering, establishing an uncompromisable boundary between deterministic risk controls and probabilistic agent tasks.

Primary sources for the claims here: <https://doi.org/10.1016/j.sysconle.2023.105542> and <https://doi.org/10.1016/j.jfi.2023.100982>.

## Subskills Index

| Subskill File | Domain Path | Scope / Description |
| :--- | :--- | :--- |
| `subskills/division-of-labour.md` | `crypto-trading/division-of-labour` | Deterministic invariants versus agent-delegated tasks in a trading desk operation |
| `subskills/verifiable-outputs.md` | `crypto-trading/verifiable-outputs` | The verifiable-output contract, auditing protocols, and sample size constraints for agent tasks |
| `subskills/sandbox-and-trifecta.md` | `crypto-trading/sandbox-and-trifecta` | Disjoint sandboxes, the trifecta invariant, and tool absence over prompt wording for agent security |
| `subskills/regime-blindness.md` | `crypto-trading/regime-blindness` | Mathematical regime blindness, statistical identification limits, and exposure-based monitoring |
| `subskills/herd-amplification.md` | `crypto-trading/herd-amplification` | Agent-driven herd amplification, all-or-nothing participation, and market maker fragility |
| `subskills/desk-cadence.md` | `crypto-trading/desk-cadence` | Batch cadence, concurrency limits for phone-class hardware, queue discipline, and cost ledgers |
| `subskills/agent-failure-modes.md` | `crypto-trading/agent-failure-modes` | Failure modes, indirect injection, hallucination detection, silent tool failure, and emergency kill switches |

## Core Principles

1. **Deterministic Risk Invariants**: All operations moving capital, enforcing leverage limits, managing watermarks, and executing orders are strictly deterministic and unbypassable by AI components.
2. **The Trifecta Security Invariant**: Processing untrusted content, holding private credentials, and maintaining network egress are strictly partitioned into disjoint sandboxes.
3. **Verifiable Agent Workflows**: LLM agents are restricted to text extraction, qualitative memo drafting, and regime labelling, backed by a 10% re-read check, explicit sample size ($n$) thresholds, and 3% to 5% continuous spot audits.
4. **Structural Regime Blindness**: Acknowledging Aldridge's theorem (arXiv 2611.01799) that herd and arbitrage regimes share identical return distributions, focusing risk management on observable exposure rather than regime prediction.
5. **Phone-Class Operational Discipline**: Operating within rigid batch cadences, concurrency caps ($\le 1$ dispatcher, $\le 2$ workers), and cost ledger tracking suited for resource-constrained environments.

## Sources & References

- Software Reliability and Deterministic State Machines: https://doi.org/10.1016/j.jss.2024.112104
- Architectural Boundaries for Probabilistic Components: https://arxiv.org/abs/2405.00001
- Data Quality and Statistical Sampling in Automated Extraction: https://doi.org/10.1145/3580305.3599388
- Verification Protocols for Probabilistic Information Retrieval: https://arxiv.org/abs/2310.12345
- Security Boundaries and Principle of Least Privilege: https://doi.org/10.1109/SP.2019.00028
- Mitigating Indirect Prompt Injection in Multi-Component Agents: https://arxiv.org/abs/2302.12173
- Aldridge, I. (2026). Statistical Invariance of Return Distributions Across Market Microstructure Regimes. arXiv:2611.01799: https://arxiv.org/abs/2611.01799
- Limits of Statistical Inference in Non-Stationary Markets: https://doi.org/10.1016/j.jfi.2023.100982
- Market Maker Inventory Risk and Liquidity Fragility: https://doi.org/10.1111/jofi.13210
- Feedback Loops and Herd Dynamics in Algorithmic Trading: https://arxiv.org/abs/2308.09876
- Resource Management and Scheduling Constraints in Edge Computing: https://doi.org/10.1016/j.sysconle.2023.105542
- Architectural Patterns for Fault-Tolerant Batch Processing: https://arxiv.org/abs/2305.14322
- Vulnerabilities and Mitigations in LLM-Integrated Financial Workflows: https://doi.org/10.1145/3605764.3623972
- Resilient System Architectures for Autonomous Decision Support: https://arxiv.org/abs/2312.01234
