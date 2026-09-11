---
name: track-monitor
description: |
  妖币追踪定时复查：拉取所有进行中（pending）的妖币追踪记录，逐币取最新价，计算
  自发现以来的涨跌幅，超过阈值（默认 ±15%）标记 暴涨/暴跌 预警。配合 schedule_task
  定时任务可实现"启动前记录 → 后续监控暴涨暴跌"全自动盯盘（app 关着也跑）。
  触发词：盯盘、妖币复查、追踪监控、check tracks、妖币有动静吗。
metadata:
  author: bazz-agent
  version: "1.0"
---

# Track Monitor Skill（妖币追踪复查）

## 命令

| 命令 | 说明 |
|---|---|
| `check [threshold_pct=15]` | 拉取 pending 追踪记录 → 逐币现价对比发现价 → 输出涨跌 + 预警标记 |

示例：`run_skill track-monitor "check"` 或 `run_skill track-monitor "check 10"`

## 输出字段

- `rows[].chg_pct`：现价相对发现价涨跌（%）
- `rows[].alert`：`"moon"`（≥ 阈值暴涨）/ `"dump"`（≤ −阈值暴跌）/ null
- `rows[].max_gain_pct / max_drop_pct`：后端已记录的历史极值
- `summary`：pending 数、预警数

## 搭配定时任务（全自动盯盘）

在对话中让 agent 创建定时任务（agent 的 `schedule_task` 工具，后端守护线程执行，app 关着也跑）：

```
任务名：妖币盯盘
频率：每 2 小时
提示词：运行技能 track-monitor "check 15"。若 summary.alerts > 0，把 alert 非空的
币种明细（symbol / chg_pct / max_gain / max_drop）完整报告给我；否则只回一行汇总。
```

## Agent 使用约定

1. 定时任务里**必须设定"无预警时简短回复"**，避免刷屏。
2. 出现 `moon` 预警时可提示用户止盈参考（结合 `market-data` 的费率/OI 判断拥挤度）；出现 `dump` 预警时提示止损。
3. 追踪记录由行情页「妖币追踪」自动写入，本技能只读不写。
