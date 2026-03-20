---
name: binance-stat-arb-monitor
description: |
  Binance 统计套利监控系统。基于 ETH/BTC 永续合约价格比率计算 z-score，生成均值回归交易信号并推送到 Telegram 或飞书。
  
  使用场景：
  (1) 监控统计套利机会（ETH/BTC 比率偏离均值）
  (2) 计算 z-score 判断开仓/平仓时机
  (3) 生成交易信号（OPEN/CLOSE）
  (4) 通过 Telegram Channel 或飞书推送信号
  (5) 记录信号历史用于回测分析
  
  数据来源：Binance USDT 合约公共 API（无需认证即可获取行情数据）
metadata:
  version: "1.0.0"
  author: SR_CAO
  license: MIT
---

# Binance Stat Arb Monitor

## Overview

统计套利（Statistical Arbitrage）监控工具，基于 Binance USDT 永续合约市场数据，监控 ETH/BTC 价格比率的偏离程度，当出现均值回归机会时生成交易信号并推送通知。

## Strategy Explanation

### 什么是统计套利？

统计套利是一种基于数学模型的量化交易策略，利用资产价格的统计相关性进行套利。其核心假设是：两个相关资产的价格比率会围绕均值波动，当偏离均值时，未来有回归均值的趋势。

### ETH/BTC 比率策略

1. **观察 ETH/BTC 价格比率**
   - 比率 = ETH 价格 / BTC 价格
   - 历史均值约 0.0293（数据来源：Binance ETHUSDT/BTCUSDT）

2. **计算 z-score**
   - z = (当前比率 - 历史均值) / 历史标准差
   - z-score 衡量当前价格偏离均值的程度（标准差倍数）

3. **交易信号逻辑**
   - z-score < -3.0：ETH 相对 BTC 偏低 → 做多 ETH + 做空 BTC
   - z-score > +3.0：ETH 相对 BTC 偏高 → 做空 ETH + 做多 BTC
   - z-score 回归至 ±1.0：平仓止盈
   - z-score 触及 ±4.5：止损

## Quick Start

### 1. 配置

```bash
# 复制配置模板
cp config.example.json config.json

# 编辑配置（必须）
vim config.json
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行监控

```bash
# 手动运行一次
python scripts/monitor.py

# 或设置定时任务（每5分钟检查）
*/5 * * * * cd /path/to/skill && python scripts/monitor.py >> /var/log/stat_arb.log 2>&1
```

### 4. 查看输出

```bash
# 查看最新信号
cat data/latest_signal.json

# 查看信号历史
cat data/signals.json
```

## Configuration

### config.json 完整配置

```json
{
  "binance": {
    "base_url": "https://fapi.binance.com",
    "timeout": 10
  },
  "strategy": {
    "symbol1": "ETHUSDT",
    "symbol2": "BTCUSDT",
    "lookback_period": 720,
    "interval": "1h",
    "entry_threshold": 3.0,
    "exit_threshold": 1.0,
    "stop_loss": 4.5,
    "min_zscore_for_signal": 2.5,
    "position_size_usd": 1000
  },
  "notification": {
    "enabled": true,
    "telegram": {
      "enabled": true,
      "bot_token": "YOUR_BOT_TOKEN",
      "chat_id": "YOUR_CHANNEL_CHAT_ID"
    },
    "feishu": {
      "enabled": false,
      "webhook_url": ""
    }
  },
  "storage": {
    "data_dir": "data",
    "signals_file": "data/signals.json",
    "latest_file": "data/latest_signal.json",
    "log_file": "data/monitor.log"
  }
}
```

### 配置说明

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `binance.base_url` | string | Binance API 地址（测试网：https://demo-fapi.binance.com） |
| `strategy.symbol1` | string | 分子交易对（ETHUSDT） |
| `strategy.symbol2` | string | 分母交易对（BTCUSDT） |
| `strategy.lookback_period` | int | 历史数据点数（720 = 30天 x 24小时） |
| `strategy.interval` | string | K线间隔（1h, 4h, 1d） |
| `strategy.entry_threshold` | float | 开仓阈值（z-score 绝对值） |
| `strategy.exit_threshold` | float | 平仓阈值（z-score 回归点） |
| `strategy.stop_loss` | float | 止损阈值 |
| `strategy.min_zscore_for_signal` | float | 最小信号阈值（避免噪音） |
| `notification.telegram.bot_token` | string | Telegram Bot Token（@BotFather 创建） |
| `notification.telegram.chat_id` | string | Channel Chat ID（@username_to_id_bot 获取） |

## Telegram Bot 设置

### 1. 创建 Bot

1. 打开 Telegram，搜索 @BotFather
2. 发送 `/newbot` 创建新机器人
3. 获取 Bot Token

### 2. 获取 Channel Chat ID

1. 创建 Telegram Channel
2. 将 Bot 添加为管理员
3. 使用 @username_to_id_bot 获取 Channel 的 chat_id（格式：-100xxxxxxxxxx）

### 3. 配置

将 Token 和 Chat ID 填入 config.json

## Output Format

### Signal JSON

```json
{
  "timestamp": "2026-03-14T19:00:00+08:00",
  "signal_type": "OPEN",
  "direction": "LONG_ETH_SHORT_BTC",
  "zscore": -3.51,
  "ratio": 0.029257,
  "mean": 0.029305,
  "std": 0.000315,
  "threshold": {
    "entry": 3.0,
    "exit": 1.0,
    "stop_loss": 4.5
  },
  "prices": {
    "eth": 2063.45,
    "btc": 70528.50
  },
  "recommendation": {
    "action": "LONG ETH-PERP + SHORT BTC-PERP",
    "eth_entry": 2063.45,
    "btc_entry": 70528.50,
    "position_size_usd": 1000
  },
  "estimate": {
    "expected_return": 0.00118,
    "fees_taker": 0.00140,
    "net_pnl": -0.00022
  },
  "strength": 4,
  "volatility": "normal"
}
```

### Telegram Message Format

```
🟢 [OPEN] 统计套利开仓信号

ETH/BTC z-score: -3.51 (偏低，均值回归概率大)
比率: 0.029257 (均值: 0.029305)
动态阈值: 开仓 ±3.00 / 止损 ±4.50
z波动率: 0.65 正常

建议操作:
 • LONG ETH-PERP (市价) @ ~$2,063.45
 • SHORT BTC-PERP (市价) @ ~$70,528.50

预估 (每腿 $1000):
 预期利润: $1.18 (0.118%)
 手续费: $1.40 (taker x4)
 净利润: $-0.22

信号强度: ★★★★☆
```

## Risk Warning

⚠️ **重要风险提示**

1. 统计套利并非无风险策略
2. 极端市场条件下价差可能持续扩大
3. 手续费对收益影响显著
4. 建议使用测试网充分验证后再实盘
5. 本工具仅供参考，不构成投资建议

## API Reference

### Binance Futures API（公共接口）

| Endpoint | 说明 | 认证 |
|----------|------|------|
| `/fapi/v1/ticker/price` | 当前价格 | 否 |
| `/fapi/v1/klines` | K线数据 | 否 |
| `/fapi/v1/premiumIndex` | 资金费率 | 否 |
| `/fapi/v1/fundingRate` | 资金费率历史 | 否 |
| `/fapi/v1/openInterest` | 未平仓合约 | 否 |
| `/fapi/v1/ticker/24hr` | 24小时行情 | 否 |

详细文档：https://binance-docs.github.io/apidocs/futures/cn/

## File Structure

```
binance-stat-arb-monitor/
├── SKILL.md                    # 本文档
├── config.example.json         # 配置模板
├── config.json                 # 运行时配置（不提交）
├── requirements.txt            # Python 依赖
├── scripts/
│   ├── __init__.py
│   ├── monitor.py             # 主入口
│   ├── fetcher.py              # Binance API 获取
│   ├── calculator.py           # z-score 计算
│   ├── formatter.py            # 消息格式化
│   └── notifier.py             # 通知推送
├── references/
│   ├── stat_arb_theory.md     # 策略理论
│   └── binance_api.md         # API 参考
└── data/
    ├── signals.json            # 信号历史
    ├── latest_signal.json     # 最新信号
    └── monitor.log            # 运行日志
```

## Troubleshooting

### 问题：获取数据失败

- 检查网络连接
- 确认 Binance API 可访问
- 尝试切换到测试网

### 问题：Telegram 推送失败

- 确认 Bot Token 正确
- 确认 Bot 已添加到 Channel
- 确认 Chat ID 格式正确（-100 开头）

### 问题：z-score 计算异常

- 检查 lookback_period 是否足够（建议 ≥100）
- 确认数据获取完整

## Changelog

### v1.0.0 (2026-03-14)
- 初始版本
- 支持 ETH/BTC 统计套利监控
- 支持 Telegram/飞书推送
- 支持信号历史记录
