---
name: openclaw-trading-suite
description: Unified OpenClaw skill for autonomous algo and swing trading workflows: hypothesis generation, screening, technical/sentiment analysis, strategy-specific risk controls, execution gating, P&L and win-rate planning, and self-improvement loops backed by persistent trade data for ML/RL retraining.
---

# OpenClaw Trading Suite

Use this skill when the user asks for end-to-end trading-agent behavior across analysis, hypothesis creation, risk management, execution, and continuous optimization.

## Scope

- Strategy styles: swing-first, with optional intraday and event-driven variants.
- Assets: equities and crypto by default.
- Lifecycle: research -> hypothesis -> validate -> size risk -> execute -> review -> retrain.
- Data retention: all decisions, signals, fills, outcomes, and model versions are logged for later analysis.

## Core workflow

1. Ingest market, technical, and optional lightweight sentiment/event data.
2. Run screeners to generate candidate tickers/coins for strategy hypotheses.
3. Build trade hypotheses with explicit entry, exit, invalidation, and confidence.
4. Apply strategy-specific risk profile (not global static policy).
5. Gate execution based on drawdown, exposure, and confidence thresholds.
6. Log every step to persistent storage (research, signals, orders, fills, P&L).
7. Run periodic review: win rate, expectancy, drawdown, and regime-fit diagnostics.
8. Feed outcomes into optimization/retraining loop with champion-vs-challenger testing.

## Strategy catalog

Load [references/strategy_profiles.md](references/strategy_profiles.md) when a user asks for concrete strategies or wants to include the "4 bots competition" approaches.

## Data model and retention

Load [references/data_retention_schema.md](references/data_retention_schema.md) when implementing storage, analytics, or RL/ML training.

## Autonomy modes

Load [references/autonomy_modes.md](references/autonomy_modes.md) when implementing user-selected autonomy behavior and approvals.

## Adapter extension contract

Load [references/adapter_plugin_contract.md](references/adapter_plugin_contract.md) when adding venues, data feeds, or research tools.

## Strategy builder and gates

Load [references/strategy_builder_and_gates.md](references/strategy_builder_and_gates.md) when user/agent-defined thresholds are needed for paper-to-live graduation.

## Secrets handling

Load [references/secrets_management.md](references/secrets_management.md) when adding providers, credentials, or runtime configuration.

## Orchestration

Load [references/system_orchestration.md](references/system_orchestration.md) when wiring agents/tools, heartbeat cadence, and execution triggers.

## Execution policy defaults

- Start in paper mode unless user explicitly requests live mode.
- Require per-hypothesis approval for first live deployment of any new strategy.
- Enforce strategy-local risk budgets and portfolio-level circuit breakers.
- Halt strategy if live or paper performance breaches configured drawdown limits.

## Reuse notes for this repository

- Existing modules to reuse first: `market-data-aggregator`, `technical-analysis-engine`, `risk-position-manager`, `strategy-optimizer`, `trade-signal-processor-executor`, `performance-reporter-learner`, `profit-forecaster`, and `temp-rl-proto`.
- Treat older module `SKILL.md` files as component-level docs; this suite is the orchestrator skill.
- Nightly research entry point: `scripts/nightly_research.py`.
