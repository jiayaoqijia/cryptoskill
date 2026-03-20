# OpenClaw Agent Adoption Plan for Algotrading Role

## Objective
Make this suite operationally useful for OpenClaw agents to:
- align trading to user goals, risk tolerance, and autonomy mode
- run repeatable paper-trading loops with measurable efficacy
- produce overnight market/hypothesis reports
- self-optimize from retained performance data
- graduate to controlled live autonomy only after passing gates

## Current State (Summary)
- Strong scaffold: autonomy policy, strategy gates, adapter registry, persistence schema, overnight report pipeline.
- Major gap: most components are framework-level only (mock adapters, no real orchestration loop, no optimization engine, no goal planner).

## Phase 1: Agent Contract and Goal Alignment (P0)
### Deliverables
- Add a formal `TradingMandate` model:
  - target goals (for example `target_net_pnl_day`)
  - max daily loss
  - risk tolerance and autonomy mode
  - allowed assets/venues and session windows
- Add mandate validation and a persisted `mandates` table.
- Add a per-session "plan of record" object linking mandate -> strategies -> risk budgets.

### Acceptance Criteria
- Agent can load one mandate and produce a deterministic session plan.
- Invalid mandates fail fast with explicit reason codes.

## Phase 2: Production-Ready Paper Execution Loop (P0)
### Deliverables
- Implement scheduler-driven loop:
  - pre-market/session-start scan
  - periodic signal checks
  - post-session reconciliation
- Replace direct mock usage with adapter interface wiring + provider config.
- Add execution safety checks before order submit:
  - qty/price/side validation
  - position/exposure limits
  - duplicate-order guard/idempotency key
  - retry + fail-closed handling
- Add order lifecycle updates (submitted/partially filled/filled/canceled/rejected).

### Acceptance Criteria
- End-to-end paper loop runs for at least 10 sessions without manual DB edits.
- Every order has a full status transition trace.
- Safety checks block malformed or over-budget orders.

## Phase 3: Risk and Autonomy Hardening (P0)
### Deliverables
- Extend autonomy policy to include:
  - exposure cap checks
  - per-strategy drawdown checks
  - daily loss circuit breaker
  - confidence floor gating
- Make `free-agent` mode still enforce hard catastrophic-risk guardrails.
- Add policy decision audit payloads (inputs + outputs + reason code lineage).

### Acceptance Criteria
- Policy regression tests cover all autonomy modes and breach combinations.
- Circuit breaker blocks further execution after configured loss/drawdown events.

## Phase 4: Overnight Intelligence and Morning Brief (P1)
### Deliverables
- Upgrade overnight pipeline from static summaries to structured outputs:
  - market regime snapshot
  - top opportunity candidates
  - top risk alerts
  - unresolved hypothesis gaps
- Add source attribution fields (headline URL/source/time/sentiment confidence).
- Add diff vs previous report (what changed overnight).
- Generate "action queue" tasks for next session.

### Acceptance Criteria
- Daily report includes machine-readable JSON + human markdown.
- Agent can consume previous-night report and create next-session priorities automatically.

## Phase 5: Self-Optimization Loop (P1)
### Deliverables
- Implement analytics jobs:
  - rolling expectancy and win-rate drift
  - regime-specific edge tracking
  - strategy scorecards by version
- Implement champion-vs-challenger workflow:
  - candidate generation (parameter/model variants)
  - backtest/walk-forward evaluation
  - promotion decision with thresholds
- Persist model/parameter lineage and promotion decisions.

### Acceptance Criteria
- System can automatically propose at least one challenger when drift thresholds breach.
- Promotions require explicit, logged pass of acceptance gates.

## Phase 6: Paper-to-Live Graduation Program (P1)
### Deliverables
- Add graduation service that consumes:
  - gate metrics
  - policy requirements
  - incident history
- Add staged live rollout:
  - micro-notional phase
  - capped daily trade count
  - auto-rollback triggers
- Add live kill switch + manual override protocol.

### Acceptance Criteria
- No strategy can enter live mode without gate evidence bundle.
- Live rollback triggers are tested and auditable.

## Phase 7: Agent UX and Skill Packaging (P2)
### Deliverables
- Add task-oriented skill entrypoints:
  - `create_hypothesis`
  - `run_paper_cycle`
  - `overnight_research`
  - `review_performance`
  - `propose_optimization`
  - `evaluate_live_promotion`
- Provide concise action schemas so agents can call flows reliably.
- Add "first-run bootstrap" command to initialize DB, strategy config, and runtime folders.

### Acceptance Criteria
- A new OpenClaw agent can execute the full paper lifecycle using only documented skill entrypoints.

## Testing and Reliability Workstream (Runs Across All Phases)
- Add integration tests for full paper loop and overnight pipeline with fixture adapters.
- Add failure-mode tests (adapter timeout, bad data, partial fills, DB lock contention).
- Add migration tests for schema evolution.
- Add reproducible backtest fixtures for regression.

## Suggested 90-Day Sequencing
1. Weeks 1-3: Phase 1 + Phase 2 foundations.
2. Weeks 4-5: Phase 3 hardening.
3. Weeks 6-7: Phase 4 overnight intelligence.
4. Weeks 8-10: Phase 5 optimization loop.
5. Weeks 11-12: Phase 6 graduation controls.
6. Week 13: Phase 7 packaging and docs polish.

## North-Star KPIs
- Paper trading: win rate, expectancy, max drawdown, rule adherence.
- Operations: execution error rate, report completeness, alert precision.
- Optimization: challenger promotion hit-rate, post-promotion stability.
- Goal alignment: progress toward user target (for example `$1000/day`) under risk constraints.
