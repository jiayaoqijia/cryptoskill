---
name: portfolio-review
description: |
  资产快照 + 周期复盘：拉取币安 CEX 账户非零余额与估值、近 N 天真实成交
  （买卖笔数 / 金额 / 净流向 / 分币种汇总）、挂单与订单跟踪，自动生成
  Markdown 周报落盘 workspace/复盘/。用户提到「资产怎么样、复盘、周报、
  盈亏统计、portfolio、review」时使用。需已连接币安 CEX（设置 → 币安 CEX）。
  触发词：资产快照、复盘、周报、成交统计、portfolio、account review。
metadata:
  author: bazz-agent
  version: "1.0"
---

# Portfolio Review（资产快照与复盘）

数据来自本机 BAZZ.AGENT 后端（端口 `BAZZ_PORT`，默认 8080）：
`/api/wallet/cex/summary`（非零余额 + USDT 估值）、`/api/wallet/cex/trades`
（真实历史成交，自动聚合全部 USDT 交易对）、`/api/orders/track`（订单跟踪）。
只读签名查询，不会下单。**前提：已在「设置 → 币安 CEX」连接 API Key**，否则命令返回
`not_configured` 提示。

## 命令

| 命令 | 说明 |
|---|---|
| `snap` | 资产快照：非零余额 TOP（按 USDT 估值排序）+ 总估值 + 更新时间 |
| `week [days=7]` | 周期复盘：近 N 天成交统计（买卖笔数 / 金额 / 净流向 / 分币种）+ 挂单与跟踪概况 + **写 Markdown 周报到 `复盘/资产周报_*.md`** |

## Agent 使用约定

1. 先跑 `snap` 确认连接与资产概况，再跑 `week` 出报告；
2. 周报里「数据事实」由本技能填写，「分析与建议」由 Agent 基于事实补写，不要编造数字；
3. 未连接 CEX 时按返回的 `message` 引导用户去设置页连接，不要重试。

## 环境变量

- `BAZZ_PORT`：后端端口（默认 8080，备选 8081 自动探测）
- `BAZZ_AUTH_TOKEN`：打包态鉴权 token（可选）
