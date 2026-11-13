<!--
  Imported from: https://github.com/quantskills/agent-ssquant
  Source Path: skills/ssquant/SKILL.md
  Curated for awesome-quant-skills
-->

---
name: ssquant-agent
description: Compatibility skill entry for the SSQuant Agent futures workflow. Use when an agent runtime only discovers local capabilities through SKILL.md but the actual public QUANTSKILLS package is quantskills/agent-ssquant with AGENTS.md as the main contract.
quantSkills:
  organization: https://github.com/quantskills
  repository: quantskills/agent-ssquant
  repository_url: https://github.com/quantskills/agent-ssquant
  project_type: skill
  collection: ssquant
  license: GPL-3.0
  category: tooling
  tags: [ssquant, agent, futures, ctp, backtest, data-server, reporting]
  platforms: [claude-code, codex, openclaw, cursor, workbuddy]
  language: zh-en
  status: stable
  validation_level: runnable
  maintainer_type: community
  requires: []
  summary_zh: "\u672c\u5730\u517c\u5bb9\u5165\u53e3\uff1a\u5c06\u0043\u006f\u0064\u0065\u0078\u7b49\u0053\u004b\u0049\u004c\u004c\u52a0\u8f7d\u5668\u8def\u7531\u5230\u0053\u0053\u0051\u0075\u0061\u006e\u0074\u0020\u0041\u0067\u0065\u006e\u0074\u3002"
  summary_en: Local compatibility entry that routes SKILL-based runtimes to the SSQuant Agent.
---

# SSQuant Agent Compatibility Skill

Use this compatibility skill only when the runtime discovers capabilities through `SKILL.md`. The public QUANTSKILLS package is `quantskills/agent-ssquant`, and the main execution contract is the repository root `AGENTS.md`.

## First Steps

1. Locate the active SSQuant project from the user's path, current working directory, editable install, or explicit repo path.
2. Inspect the local project before claiming behavior. Prefer current source and command output over memory.
3. Run the doctor when project state is unclear:

```powershell
$env:PYTHONUTF8='1'
python ../../scripts/ssquant_doctor.py --project <ssquant-root>
```

4. Choose exactly one primary lane from the routing table.
5. Compile, validate, and run real evidence when the user asks whether something works.

## Routing Table

| User intent | Load these files |
| --- | --- |
| StrategyAPI return types, project boundaries, validation gates | `../../references/core/api-return-types.md`, `../../references/core/project-contract.md`, `../../references/core/verification.md` |
| Futures strategy generation, backtesting, continuous contracts, costs, rollover cost | `../../references/futures/futures-workflow.md`, `../../references/futures/rollover-cost.md` |
| data_server, cache, SQLite, raw vs adjusted prices, async history tasks | `../../references/data/raw-and-adjustment.md`, `../../references/data/cache-and-missing-data.md`, `../../references/data/async-history-tasks.md` |
| SIMNOW, real CTP, account config, live K-line source, auto roll, guarded process checks | `../../references/live-ctp/live-guardrails.md`, `../../references/live-ctp/rollover-and-kline-source.md` |
| Backtest metrics, Chinese HTML/Markdown reports, chart/report bugs | `../../references/reporting/chinese-report-template.md`, `../../references/reporting/report-debugging.md` |

## Non-Negotiable Boundaries

- Generated strategy code stays inside `StrategyAPI`, `initialize(api)`, `strategy(api)`, `get_config()`, `UnifiedStrategyRunner`, and `RunMode`.
- Do not call low-level CTP modules, generated binary adapters, `DataSource`, `BacktestCore`, or account internals from user strategies.
- Do not place data-server credentials, SIMNOW passwords, real CTP passwords, `app_id`, `auth_code`, or raw account dictionaries in strategies, reports, screenshots, commits, or chat summaries.
- Do not claim a strategy, data service, report, or live process works without command output, report files, logs, browser/API evidence, or another concrete artifact.
- Do not migrate a profitable backtest to SIMNOW or real trading automatically. Runtime migration is a separate gated task.

## Shared SSQuant Facts

- A data source is `symbol + period + adjust_type + range/limit`.
- Use `data_sources=[...]` for multi-symbol or multi-period work. Do not teach comma-separated `symbol="rb888,hc888"` unless the local project proves it.
- `data_server` may return raw bars. SSQuant can apply local adjustment according to `adjust_type`.
- Strategy continuity may use adjusted prices, while execution/accounting should use raw prices when the framework supports that split.
- In current SSQuant forks, `api.get_price()` is a scalar current strategy price; `api.get_close()`, `api.get_open()`, `api.get_high()`, `api.get_low()`, and `api.get_volume()` return pandas Series.

## Validation Commands

```powershell
$env:PYTHONUTF8='1'
python ../../scripts/ssquant_doctor.py --project <ssquant-root>
python -m py_compile <strategy.py>
python ../../scripts/validate_strategy.py <strategy.py>
```

Use real backtests, real local data inspection, or real API probes when the user asks for proof.

## Agent Contract

Read `../../AGENTS.md` before running multi-step SSQuant coding, migration, publishing, or live-operation tasks. It defines the agent execution contract, evidence requirements, and live-trading gates.
