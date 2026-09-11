---
name: coin-report
description: |
  一键生成标准代币研报并落盘 workspace/妖币/<SYMBOL>_研报_*.md。自动拉取 90 日 K 线、
  24h/7d/30d 动量、区间位置与收盘分位、资金费率、OI、大户多空比、恐惧贪婪、妖币追踪
  战绩，写入结构化 Markdown；「结论与计划」留白由 agent 基于事实填写。
  触发词：研报、生成报告、分析报告、写份分析、coin report、存到妖币文件夹。
metadata:
  author: bazz-agent
  version: "1.0"
---

# Coin Report Skill（标准研报）

## 命令

| 命令 | 说明 |
|---|---|
| `report <SYMBOL> [market=futures]` | 生成研报 → `workspace/妖币/<SYMBOL>_研报_<时间戳>.md`，stdout 返回报告路径 + 关键数字摘要 |

示例：`run_skill coin-report "report WLDUSDT"`（合约）/ `run_skill coin-report "report RAYUSDT spot"`

## 报告结构（自动填充的事实部分）

1. **快照**：现价、24h/7d/30d 涨跌、24h 波动区间
2. **90 日结构**：区间、现价区间位置（%）、收盘分位（%）、距 90d 高/低点
3. **衍生品**（合约才有）：资金费率、OI 与 USD 名义、大户多空比、背离标记
4. **市场环境**：恐惧贪婪指数（值 + 分类）
5. **追踪战绩**（若该币在妖币追踪中）：发现价/现价、最大涨幅/回撤、结局
6. **结论与计划**（agent 填写）：趋势方向、关键支撑阻力、入场思路、失效条件 —— 必须区分事实与推测

## Agent 使用约定

1. 生成后**读一遍报告文件**，把「结论与计划」补充完整再告知用户。
2. 深入分析可再配合 `market-data` 技能取 4h/1h 细化结构，配合 `query-token-audit` 做合约安全检查。
3. 研报仅供参考，不构成投资建议 —— 涉及下单前先走 `risk-guard`。
