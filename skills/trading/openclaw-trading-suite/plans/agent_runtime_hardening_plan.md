# Agent Runtime Hardening Plan

## 2. Exception Handling Logic Plan
### Scope
- `orchestration.evaluate_and_execute`
- `research.run_overnight_research`
- adapter call surfaces

### Logic
1. Wrap every external adapter call with retry + fallback handling.
2. On adapter failure:
   - persist a structured failed-order/failed-report event
   - return a machine-readable failure reason
   - do not proceed to fill creation or downstream assumptions
3. On internal runtime failure:
   - return explicit `unexpected_*` reason
   - keep audit trail durable
4. Keep all failure reasons deterministic for tests and agent remediation.

### Success Criteria
- No uncaught adapter exception can crash the execution loop.
- Every failure returns typed reason codes and attempt history.

## 5. Production Nightly Research Plan
### Goals
- Replace static/mock-only summaries with actionable overnight intelligence.
- Generate both human markdown and machine JSON payloads.

### Production Logic
1. Resolve preferred adapters (market/news) with fallback chains.
2. For each symbol:
   - fetch quote snapshot
   - record adapter used and timestamp
3. For each topic:
   - fetch headlines with sentiment labels
   - include source metadata when available
4. Build output artifacts:
   - `while-you-were-sleeping-<date>.md`
   - `while-you-were-sleeping-<date>.json`
5. Persist summary in `overnight_reports`.
6. On failure, emit structured `overnight_report_failed` payload and non-zero exit code.

### Next Production Upgrades
- add source URL/time/confidence normalization contract
- add cross-day diff section ("what changed since yesterday")
- add opportunity/risk ranking score

## 6. Goal Alignment Mechanism Plan (Intent-Align Compatible)
### Goal
Allow agents to target performance outcomes while keeping constraints explicit and flexible.

### Data Model
- `mandates` table: goal target + risk mode + constraints + `intent_align_ref`
- `mandate_progress` table: periodic target progress snapshots

### Logic
1. Define mandate targets:
   - examples: `net_pnl/day >= 1000`, `max_drawdown/month <= 0.08`
2. Evaluate periodic actual metrics against targets.
3. Derive effective risk budget from:
   - strategy base limit
   - mandate risk mode (`fixed`, `agent_defined`, `hybrid`)
   - target progress
4. Persist progress and expose to strategy/promotion decisions.

### Intent-Align Integration
- use `intent_align_ref` in mandate records to link external intent definitions
- keep evaluator independent so intent-align can own upstream intent negotiation

## 7. Paper-to-Promotion Flow Plan
### Goal
Tie paper-trading performance and goal progress into one promotion decision.

### Decision Flow
1. Evaluate strategy maturity gates (`paper_to_live` thresholds).
2. If gates fail -> block promotion with gate reasons.
3. If gates pass:
   - evaluate mandate goal progress
   - optionally require minimum progress ratio
4. Return promotion decision with reason codes (`goal_progress_not_met`, etc.).

### Success Criteria
- Promotion decisions are reproducible and fully auditable.
- Gate pass alone is insufficient when goal-progress requirements are enabled.
