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

Primary sources for the claims here: <https://ai.meta.com/blog/practical-ai-agent-security/> and <https://arxiv.org/abs/2611.01799>.

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

- Meta AI, Agents Rule of Two: A Practical Approach to AI Agent Security: <https://ai.meta.com/blog/practical-ai-agent-security/>
- Greshake et al. (2023), Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection: <https://arxiv.org/abs/2302.12173>
- Beurer-Kellner et al. (2025), Design Patterns for Securing LLM Agents against Prompt Injections: <https://arxiv.org/abs/2506.08837>
- Aldridge, I. (2026). Learning AI Agents, Market Makers, and Stress in Automated Markets. arXiv:2611.01799: <https://arxiv.org/abs/2611.01799>
- Cemri et al. (2025), Why Do Multi-Agent LLM Systems Fail? (MAST failure taxonomy): <https://arxiv.org/abs/2503.13657>
- Manakul et al. (2023), SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection: <https://arxiv.org/abs/2303.08896>
- Ye et al. (2026), The Alpha Illusion: Reported Alpha from LLM Trading Agents Should Not Be Treated as Deployment Evidence: <https://arxiv.org/abs/2605.16895>
- NIST AI Risk Management Framework: <https://www.nist.gov/itl/ai-risk-management-framework>
- Android developers, Keep background work alive with a lean process: <https://developer.android.com/topic/performance/memory/guide/process-splitting>
- Android developers, Processes and threads overview: <https://developer.android.com/guide/components/processes-and-threads>
