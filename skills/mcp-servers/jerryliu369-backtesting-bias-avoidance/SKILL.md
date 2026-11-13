<!--
  Imported from: https://github.com/quantskills/skill-backtesting-bias-avoidance
  Source Path: SKILL.md
  Curated for awesome-quant-skills
-->

---
name: backtesting-bias-avoidance
name_zh: 回测引擎构建与偏差规避
description: Build a correct, look-ahead-free backtest and audit a strategy for the
  biases that make backtests lie — look-ahead bias, survivorship bias, overfitting
  and data-snooping — while modeling realistic transaction costs and validating with
  out-of-sample and walk-forward testing and a full set of performance metrics. Use
  when the user asks for 回测引擎、回测偏差排查、前视偏差、幸存者偏差、过拟合检验、样本外/前推检验、交易成本建模、夏普/索提诺/最大回撤计算,
  or a one-stop strategy backtest-and-bias-audit dossier.
description_zh: 构建一个无前视偏差的正确回测引擎，并对策略做偏差审计——前视偏差、幸存者偏差、过拟合与数据窥探——同时建模含市场冲击的真实交易成本，并用夏普显著性检验（t值/95%置信区间，Lo 2002）、CSCV 过拟合概率(PBO)、去通胀夏普(DSR，多重检验校正)、样本外与滚动前推检验和完整绩效指标加以验证。适用于回测引擎搭建、回测偏差排查、前视/幸存者偏差、过拟合检验(PBO)、显著性检验、样本外检验、交易成本与市场冲击建模、夏普/最大回撤计算等场景。
metadata:
  organization: QuantSkills
  organization_url: https://github.com/quantskills
  repository: skill-backtesting-bias-avoidance
  repository_url: https://github.com/quantskills/skill-backtesting-bias-avoidance
  project_type: skill
  collection: backtesting-bias-avoidance
quantSkills:
  project_type: skill
  category: research
  tags:
  - backtesting
  - bias-avoidance
  - look-ahead-bias
  - survivorship-bias
  - overfitting
  - walk-forward
  - performance-metrics
  platforms:
  - claude-code
  - codex
  - openclaw
  - cursor
  status: stable
  validation_level: runnable
  maintainer_type: community
  summary_zh: 构建无前视偏差的回测引擎，并审计前视/幸存者/过拟合等偏差：含市场冲击的成本建模、夏普显著性(t值/CI)、CSCV过拟合概率(PBO)、去通胀夏普(DSR)、样本外检验一应俱全，一次验明回测是真是假。
  summary_en: A backtesting skill that builds a look-ahead-free engine and audits a
    strategy for look-ahead, survivorship, and overfitting biases, with cost modeling,
    out-of-sample and walk-forward validation, and full performance metrics.
  license: GPL-3.0-only
  requires: []
---

# Backtesting & Bias Avoidance

Use this skill to build a correct, look-ahead-free backtest of a trading strategy and audit it for the biases that make backtests lie — look-ahead bias, survivorship bias, overfitting and data-snooping — with realistic transaction costs, out-of-sample and walk-forward validation, and a full performance profile.

The single most important job of this skill is **deciding whether a backtest's edge is real or an artifact**. The most undervalued and error-prone step in quant research is exactly this: a strategy can look spectacular in-sample purely because of a forgotten lag, a survivorship-cleaned universe, or a parameter mined over hundreds of trials. Default to assuming the edge is fake until it survives a clean, out-of-sample test net of costs.

## Core Workflow

1. Normalize the setup. Capture the universe/asset, the signal rule, the study period, the train/test split, and the cost assumptions. If the user has no strategy in mind, default to a momentum demonstration on controlled synthetic data so the "true" edge is known and bias detection is unambiguous. Ask only when a required element is missing.
2. Confirm assumptions. Default to next-bar execution (signals act on the bar after they are known), a chronological train/test split with the most recent ~30% held out, realistic round-trip costs, and a 252-day annualization unless the user specifies otherwise. State every assumption.
3. Read `references/backtest-guide.md` before the first dossier in a session. Use it for the engine-construction rules, the bias taxonomy and how each is tested, the default audit thresholds, the report blueprint, and the appendix requirements.
4. Compute with the bundled `scripts/run_backtest.py`. It is offline by default (synthetic data) and can also read real prices via yfinance: it builds a clean engine with a linear-plus-market-impact cost model; demonstrates and quantifies look-ahead bias; attaches Newey-West HAC t-statistics and 95% CIs to every Sharpe (reporting the variance-inflation factor, effective sample size `N_eff = T/factor`, and a per-bet/per-segment significance check); measures overfitting with CSCV's Probability of Backtest Overfitting (PBO) plus a bootstrap CI; deflates the Sharpe for multiple testing (Deflated Sharpe Ratio, reported as an optimistic upper bound since the trial universe is a lower bound on researcher degrees of freedom); runs hundreds of independent synthetic AR(1) paths to turn PBO/DSR/out-of-sample-Sharpe point values into distributions and a false-discovery rate; draws an equity-and-drawdown chart; and reports the full metric set. Install dependencies with `pip install numpy pandas scipy matplotlib` (add `yfinance` only for real data).
5. Separate the clean result from the biased one. Always report the look-ahead-free, out-of-sample, net-of-cost number as the headline, and present any in-sample or gross figure only as a contrast that shows how much the bias inflates it.
6. Produce Markdown by default. If the user asks for Word, PDF, or a polished deliverable, generate the analytical content here first, then use the relevant document skill for final layout.

## Analysis Rules

- Separate the honest result from the inflated one. Label every figure as in-sample vs. out-of-sample, gross vs. net, and look-ahead-free vs. leaky, and never present an in-sample/gross/leaky number as the headline.
- Enforce no look-ahead. Signals must use only information available at decision time; execution happens on the next bar; the report must state the lag and execution convention explicitly.
- Report significance with corrected standard errors, not iid ones. Every Sharpe must carry a t-statistic and 95% CI computed with a HAC (Newey-West) estimator, since overlapping-window and long-holding P&L is serially correlated; also report the effective sample size / variance-inflation factor and a per-bet (per-holding-segment) significance check, because the daily count overstates the number of independent bets. An out-of-sample Sharpe whose CI contains zero is "no significant edge," not proof of a working strategy.
- Measure overfitting with multiple paths, not one. Use CSCV/PBO (with a bootstrap CI) rather than a single train/test result, and — for synthetic data, where you control the generating process — run hundreds of independent paths to report the distribution of PBO/DSR and a false-discovery rate, since single-path point values are themselves draws from that distribution. Deflate the Sharpe for the number of trials (DSR), and state that DSR is an optimistic upper bound because the disclosed trial count (window scan) omits other researcher degrees of freedom (cost, bandwidth, long/short rules).
- Discipline the wording. When the out-of-sample result is not significant, write "无显著净边际" (no significant net edge) — never "策略无效" (the strategy is invalid). The former is what the data supports; the latter is over-interpretation.
- Model costs as evidence. State commission, spread, and slippage assumptions, and report gross and net side by side plus the cost level at which the edge disappears.
- Survivorship and point-in-time cannot be auto-checked on a single series; include them as explicit qualitative checklist items and state whether the universe included delisted names and whether data was point-in-time.
- Use high/medium/low audit levels only when a rule in `references/backtest-guide.md` or a user-provided rule is triggered. Include the triggering rule text beside each flag.
- End every report with this disclaimer: `本报告基于公开数据与规则化分析生成，仅供研究参考，不构成任何投资建议。`

## Resource Guide

- `references/backtest-guide.md`: engine-construction rules, bias taxonomy and tests, audit thresholds, report blueprint, and final QA checklist.
- `scripts/run_backtest.py`: runnable backbone — clean look-ahead-free engine with a linear-plus-impact cost model, a quantified look-ahead demonstration, Sharpe significance (t-stat and 95% CI), CSCV/PBO overfitting probability, the Deflated Sharpe Ratio for multiple testing, a cost-sensitivity sweep, the full metric set, the bias-audit rules, and the Markdown report writer. Offline by default; optional yfinance for real data.

## Quality Bar

- The headline number must be look-ahead-free, out-of-sample, and net of all costs (linear + market impact, consistent with the cost table), and must carry a HAC t-statistic, 95% CI, effective sample size, and a per-bet significance check.
- Overfitting must be assessed with CSCV/PBO (multi-path), not a single split; any scanned/optimized parameter must report the number of trials, its out-of-sample result, and a Deflated Sharpe Ratio.
- Performance must be reported with multiple metrics (Sharpe, Sortino, max drawdown, Calmar, hit rate, turnover), not a single number or a raw return.
- Do not overstate an edge or its absence. Use "样本外扣费后无显著净边际" (not "策略无效"), "PBO 高，疑似过拟合", and "DSR 校正后不显著" when the data is only indicative, and never use buy/sell language.
