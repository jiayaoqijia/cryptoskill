---
name: polymarket-api
description: 查询Polymarket预测市场数据 / Query Polymarket prediction markets
metadata:
  version: 1.0.0
---

# Polymarket API

查询Polymarket预测市场的公共API（无需认证）。

Query Polymarket prediction market data via public API (no auth required).

## 功能 / Functions

- 📈 热门市场 / Top markets
- 🔍 市场搜索 / Market search
- 📊 特定市场详情 / Market details
- 📅 事件列表 / Event list

## 使用示例 / Usage

```bash
# 热门市场 by 24h volume
python3 scripts/polymarket.py --top

# 搜索市场
python3 scripts/polymarket.py --search "trump"

# 获取指定市场
python3 scripts/polymarket.py --slug "will-trump-win-the-2024-election"

# 事件列表
python3 scripts/polymarket.py --events
```

## 参数 / Options

- `--top`: 热门市场 / Top markets
- `--search`, `-s`: 搜索关键词 / Search query
- `--slug`: 市场slug / Market slug
- `--events`, `-e`: 事件列表 / List events
- `--json`: 输出JSON / Output JSON
