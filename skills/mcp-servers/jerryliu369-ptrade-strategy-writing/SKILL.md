<!--
  Imported from: https://github.com/xxbbzy/ptrade-agent-skills
  Source Path: skills/ptrade-strategy-writing/SKILL.md
  Curated for awesome-quant-skills
-->

---
name: ptrade-strategy-writing
description: Write, review, migrate, debug, and explain Ptrade quantitative trading strategies for 回测 or 交易. Use for Ptrade event functions, market-data APIs, order APIs, ETF/LOF/convertible-bond, margin, futures, persistence, live-trading restart safety, API availability, or converting other strategies to Ptrade-compatible Python.
---

# Ptrade Strategy Writing

## Overview

Use this skill to write, review, migrate, and debug Ptrade strategies that match the Ptrade event engine, API scope, market-data formats, order behavior, and live-trading constraints documented in the bundled Ptrade references.

Read references as needed:

- `references/runtime-and-writing-rules.md`: Ptrade strategy lifecycle, event timing, live-trading persistence/restart rules, code suffixes, data objects, and safety checks.
- `references/api-map.md`: compact API navigation grouped by setup, scheduling, market data, security info, account/position/order, trading, margin, futures, indicators, and utilities.
- `references/api-index.md`: high-risk/common API index with availability, event-placement, and live-trading notes.
- `references/example-patterns.md`: patterns extracted from the bundled Ptrade example strategies.
- `references/ptrade-full.md`: full original Ptrade API document. Search this when exact signatures, return fields, restrictions, or examples matter.
- `references/examples/*.py`: original example strategy files copied from the local Ptrade examples.
- `scripts/check_ptrade_strategy.py`: static checker for event signatures, API placement, target environment mismatches, and common live-trading hazards.

Reference loading guide:

- For any live-trading, tick, restart, callback, margin, or futures task, read `runtime-and-writing-rules.md` first.
- For exact API choice, read `api-map.md`, then `api-index.md`; search `ptrade-full.md` only for exact signatures, return fields, restrictions, or examples.
- For factor, rotation, intraday, pair-trading, or basket strategies, read `example-patterns.md` and then the closest file under `references/examples/`, but use examples only to understand Ptrade structure and API patterns.
- When reviewing an existing strategy file, run `python scripts/check_ptrade_strategy.py <strategy.py>` from this skill directory when local file access is available.

## Hard Requirements

- Treat bundled examples strictly as references. Do not directly reuse example strategy logic, stock/fund pools, thresholds, timing, parameters, comments, or risk settings unless the user explicitly provides or requests those exact details.
- Generated strategies must be driven by the strategy writer's requirements and user-provided materials. If required inputs are missing, make conservative assumptions and state them clearly instead of filling gaps from an example strategy.
- Generated strategy code must include complete Chinese comments explaining strategy intent, key parameters, data windows, signal conditions, risk controls, order logic, and any live-trading safeguards.
- Keep comments useful and specific to the generated strategy. Do not paste generic comments from bundled examples.

## Authoring Workflow

When writing or migrating a strategy:

1. Identify the target scene: 回测, 普通股票交易, tick 交易, ETF/LOF/可转债, 融资融券, or 期货.
2. Choose the event mechanism:
   - Use `handle_data(context, data)` for day/minute strategies.
   - Add `before_trading_start(context, data)` for daily universe refresh, filters, factor data, or per-day flags.
   - Add `after_trading_end(context, data)` for post-close logs, reconciliation, or end-of-day persistence.
   - Use `run_daily` for fixed-time tasks and `run_interval` for live interval tasks.
   - Use `tick_data` and `order_tick` only for tick-level live trading.
   - Use `on_order_response` / `on_trade_response` only for live order/trade push handling and guard against callback order loops.
3. Map the user's rules and provided materials into explicit universe selection, data windows, signal calculation, sizing, execution, and duplicate-order controls.
4. Put one-time setup in `initialize`; put per-day preparation in `before_trading_start`; keep trade decisions in the selected runtime event.
5. Use examples only to verify event/API idioms. Do not copy example strategy rules or parameters into the generated strategy unless they are also present in the user's request or materials.
6. Add Chinese comments while writing the code, especially around parameters, data retrieval, signal calculation, trade sizing, order submission, and risk/restart safeguards.
7. Use `g` for global strategy state, but design live-trading state with Ptrade persistence and restart semantics in mind.
8. Verify every API call is legal in the target event and target module by checking `references/api-map.md` and, for exact details, `references/ptrade-full.md`.
9. For generated strategy files, run `scripts/check_ptrade_strategy.py` if possible and fix any errors before finalizing.
10. Include a short readiness note for assumptions that cannot be proven from code: strategy frequency, benchmark, initial capital, commission/slippage settings, data permissions, broker/counter support, and live account synchronization.

## Strategy Skeletons

Minimal day/minute strategy:

```python
def initialize(context):
    # 设置本策略关注的交易标的，并注册到 Ptrade 股票池。
    g.security = "600570.SS"
    set_universe(g.security)


def handle_data(context, data):
    # 从当前 BarData 中读取最新收盘价，可在此处接入用户定义的信号逻辑。
    price = data[g.security].close
    log.info("price: %s" % price)
```

Daily rebalance strategy:

```python
def initialize(context):
    # 策略参数：指数股票池、目标持仓数量、调仓周期和调仓状态。
    g.index = "000300.XBHS"
    g.hold_num = 10
    g.rebalance_days = 20
    g.day_count = 0
    g.need_rebalance = False


def before_trading_start(context, data):
    # 盘前判断今天是否需要调仓，并按用户规则准备候选股票池。
    g.need_rebalance = (g.day_count % g.rebalance_days == 0)
    if g.need_rebalance:
        stocks = get_index_stocks(g.index)
        # 剔除 ST、停牌和退市整理标的，避免无法交易或风险异常的股票进入候选池。
        g.candidates = filter_stock_by_status(
            stocks, filter_type=["ST", "HALT", "DELISTING"], query_date=None
        )
    g.day_count += 1


def handle_data(context, data):
    # 非调仓日直接返回，避免重复计算和重复下单。
    if not g.need_rebalance:
        return
    # 根据用户定义的排序规则计算目标持仓，先卖出不再符合条件的标的，再买入或调仓到目标权重。
    g.need_rebalance = False
```

Live tick strategy:

```python
def initialize(context):
    # tick 交易需要更强的重复下单保护；此处用标记位记录是否已经发过委托。
    g.security = "600570.SS"
    g.sent_order = False
    set_universe(g.security)
    # 实盘重启时避免自动重复交易，并按需关闭 L2 tick 数据。
    set_parameters(tick_data_no_l2="1", not_restart_trade="1", server_restart_not_do_before="1")


def tick_data(context, data):
    # 已经发出委托后直接返回，避免同一信号在 tick 回调中重复下单。
    if g.sent_order:
        return
    tick = data[g.security]["tick"]
    last_px = tick["last_px"][0]
    if last_px > 0:
        # 股票限价保留 2 位小数；真实策略应结合用户要求设置价格保护和委托数量。
        order_tick(g.security, 100, limit_price=round(float(last_px), 2))
        g.sent_order = True


def handle_data(context, data):
    # tick 策略仍需保留 Ptrade 必选的 handle_data 函数。
    pass
```

## Ptrade-Specific Rules

- Always define `initialize(context)` and `handle_data(context, data)`.
- Use Ptrade code suffixes: Shanghai securities can use `.SS` or `.XSHG`, Shenzhen `.SZ` or `.XSHE`, indices use `.XBHS`, and CFFEX futures use `.CCFX`.
- Treat `set_universe` as mainly the default `security_list` for `get_history`; `data[security]` only contains subscribed universe data.
- Use `context.blotter.current_dt` and `context.previous_date` for engine time. In examples, daily date guards often use `context.blotter.current_dt.strftime("%Y%m%d")`.
- In live trading, `context.portfolio` and `Position` data have synchronization latency, commonly around 6 seconds depending on broker setup. Do not rely on immediate position updates after an order.
- Use `order_target` and `order_target_value` freely in backtests, but be cautious in live trading because delayed position synchronization can cause repeated orders.
- Round limit prices by product precision: stocks 2 decimals, convertible bonds/ETF/LOF 3 decimals, stock index futures 1 decimal.
- Prefer explicit flags and order tracking before placing live orders. Store order ids and check `get_open_orders`, `get_orders`, callbacks, or broker state before sending another order.
- Do not put live order submission in `initialize` or restart-sensitive `before_trading_start` without strong duplicate-order protection.
- For live restart safety, use `set_parameters(not_restart_trade="1", server_restart_not_do_before="1")` when appropriate and design persisted `g` values carefully.
- Handle missing data, suspended stocks, ST/delisting status, limit-up/limit-down, and empty API returns explicitly.

## Review Workflow

When reviewing or debugging Ptrade code, check in this order:

1. Static checks: run `scripts/check_ptrade_strategy.py <strategy.py>` when possible; address errors before relying on manual review.
2. Event structure: required functions, selected frequency, legal API calls in each event, no accidental tick-only APIs in `handle_data`.
3. Data correctness: no lookahead, correct `include` behavior, correct `count`/date windows, suspension handling, `is_dict`/DataFrame return shape, and code suffix compatibility.
4. Trading correctness: order size units, lot rounding, limit price precision, live duplicate-order risk, unavailable `enable_amount`, and limit-up/limit-down handling.
5. Live resilience: persistence, restart behavior, callback loop prevention, broker/counter API support, and account/position synchronization.
6. Backtest realism: benchmark, commission, slippage, volume limits, `set_limit_mode`, initial positions, and whether target APIs are backtest-only or trading-only.

## Reference Search

Use `rg` against `references/ptrade-full.md` before relying on memory for exact API details. Helpful searches:

```bash
rg -n "#### order_target_value|order_target_value\\(" references/ptrade-full.md
rg -n "#### get_history|include|fill|is_dict" references/ptrade-full.md
rg -n "initialize\\(必选\\)|before_trading_start|handle_data\\(必选\\)|tick_data" references/ptrade-full.md
rg -n "set_parameters|not_restart_trade|server_restart_not_do_before|持久化" references/ptrade-full.md
rg -n "交易模块可用|回测模块可用|仅在交易模块" references/ptrade-full.md
```
