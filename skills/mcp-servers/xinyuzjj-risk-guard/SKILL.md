---
name: risk-guard
description: |
  下单前风险护栏：1) plan —— 按固定风险百分比计算仓位大小（资金/风险%/入场价/止损价 →
  数量、名义值、保证金、强平距离估算与警告）；2) check —— 查 CEX 当前敞口（资产快照、
  挂单、订单跟踪）。任何真实下单（现货买/合约开仓）之前必须先跑本技能。
  触发词：仓位、该买多少、下单前检查、风控、position sizing、risk check。
metadata:
  author: bazz-agent
  version: "1.0"
---

# Risk Guard Skill（下单前护栏）

## 命令

| 命令 | 说明 |
|---|---|
| `plan <capitalUsd> <riskPct> <entry> <stop> [lev=1]` | 固定风险仓位计算：数量 / 名义值 / 保证金 / 强平距离估算 / 警告 |
| `check [symbol]` | CEX 当前敞口：资产快照 + 挂单 + 订单跟踪（未连接 CEX 时给出提示） |

示例：

```
run_skill risk-guard "plan 1000 1 0.42 0.38"        # $1000 资金，单笔风险 1%，0.42 进 0.38 止损
run_skill risk-guard "plan 1000 2 0.42 0.38 5"      # 5 倍杠杆版本
run_skill risk-guard "check WLDUSDT"
```

## plan 的数学

- 风险金额 `risk_usd = capital × riskPct / 100`
- 止损距离 `stop_dist_pct = |entry − stop| / entry × 100`
- 数量 `qty = risk_usd / |entry − stop|`；名义 `notional = qty × entry`
- 保证金（lev>1）`margin = notional / lev`
- 强平估算 `liq_est ≈ 100 / lev %`（单向线性近似，仅参考）—— **若 stop_dist_pct ≥ liq_est，说明止损先于强平被打穿前可能已触发强平风险，会输出警告**

## 下单前 Checklist（agent 必须逐条过）

1. `plan` 算仓 —— 风险百分比默认 ≤1%，激进 ≤2%，禁止更高
2. `market-data bundle` —— 资金费率是否极端拥挤、OI 是否异常放大
3. `query-token-audit`（链上币）—— 合约安全检查
4. `check` —— 当前敞口 + 挂单是否冲突
5. 明确失效条件（作废价）后再 `propose_trade`，并把止损价写进订单

## Agent 使用约定

- 用户催促"直接买"也必须先跑 `plan` + `check`，用一行说明为什么（合规风控）。
- `check` 返回的资产/持仓仅作参考快照，不作为唯一依据。
