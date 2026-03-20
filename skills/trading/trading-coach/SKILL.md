---
name: trading-coach
description: |
  🏆 AI交易复盘教练 — 把你的券商CSV变成可执行的改进洞察！
  自动FIFO配对持仓，8维度质量评分(入场/出场/趋势/风险...)，10维度AI洞察。
  支持富途(中/英)、老虎、中信、华泰等主流券商。
  触发条件: 用户提供交易CSV、要求分析交易表现、评估交易质量、生成复盘报告、
  计算盈亏统计、识别交易模式问题、"帮我复盘"、"分析我的交易"。
---

# 🏆 Trading Coach — AI交易复盘教练

> 别再凭感觉交易了。让数据告诉你哪里做对了，哪里需要改进。

将券商导出的CSV交易记录，转化为**专业级复盘报告**和**可执行的改进建议**。

## ✨ 核心能力

- 🔄 **智能导入** — 自动识别5种券商格式，一键导入
- 📊 **FIFO配对** — 自动把买卖配对成完整持仓周期
- 🎯 **8维度评分** — 入场、出场、趋势、风险、行为...全面诊断
- 💡 **AI洞察** — 10维度分析，找出你的交易盲点

## 🚀 快速开始

```bash
# 首次安装
git clone https://github.com/BENZEMA216/tradingcoach.git ~/tradingcoach
cd ~/tradingcoach
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && cp config_template.py config.py

# 一键复盘
python scripts/import_trades.py /path/to/trades.csv  # 导入
python scripts/run_matching.py                        # 配对
python scripts/score_positions.py --all               # 评分
python scripts/analyze_scores.py                      # 报告
```

## 📈 支持券商

| 券商 | 编码 | 自动检测 |
|------|------|----------|
| 富途(中文) | UTF-8-BOM | ✅ 方向、代码、成交时间 |
| 富途(英文) | UTF-8 | ✅ Side、Symbol、Fill Time |
| 老虎证券 | UTF-8 | ✅ 交易方向、股票代码 |
| 中信证券 | GBK | ✅ 买卖标志、证券代码 |
| 华泰证券 | GBK | ✅ 操作、证券代码 |

详见 [references/csv_formats.md](references/csv_formats.md)

## 🎯 评分体系

8个维度，每个都有权重：

| 维度 | 权重 | 评估内容 |
|------|------|----------|
| 入场质量 | 18% | RSI/MACD/布林带配合度 |
| 出场质量 | 17% | 止盈止损执行 |
| 趋势把握 | 14% | 顺势/逆势、ADX强度 |
| 风险管理 | 12% | R:R比率、MAE/MFE |
| 市场环境 | 11% | 市场状态适配 |
| 交易行为 | 11% | 纪律性、冲动检测 |
| 新闻契合 | 7% | 新闻背景一致性 |
| 执行质量 | 5% | 滑点、成交效率 |

**等级**: A(90+) / B(80-89) / C(70-79) / D(60-69) / F(<60)

详见 [references/scoring_system.md](references/scoring_system.md)

## 💡 AI洞察

10个维度深度分析你的交易模式：入场质量、出场时机、风险控制、持仓周期、费用侵蚀、历史对比、模式识别、根因分析、事件关联、改进建议

详见 [references/insight_dimensions.md](references/insight_dimensions.md)

## 📊 输出示例

```
总持仓: 150笔 | 胜率: 62.5% | 总盈亏: $12,500 | 平均评分: 72.3 (C)

⚠️ 在超买区域做多 — 入场时RSI=75.2，建议避免RSI>70时追涨
✅ 止损执行良好 — 平均亏损控制在2.3%，纪律性强
💡 持仓时间偏短 — 平均持仓2.3天，考虑延长持有优质标的
```

---

## ☕ 支持作者

如果这个工具帮到了你，请考虑请我喝杯咖啡！

- **GitHub Sponsors**: [@BENZEMA216](https://github.com/sponsors/BENZEMA216)
- **Buy Me a Coffee**: [buymeacoffee.com/benzema216](https://buymeacoffee.com/benzema216)
- **USDC (Base)**: `0x...` *(联系获取地址)*

你的支持是我持续改进的动力 🚀