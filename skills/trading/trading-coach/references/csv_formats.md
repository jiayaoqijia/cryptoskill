# 支持的CSV格式

## 富途证券 (中文) - futu_cn

**编码**: UTF-8-BOM  
**分隔符**: 逗号

### 必需字段

| 字段名 | 说明 | 示例 |
|--------|------|------|
| 方向 | 交易方向 | 买入/卖出/卖空/买券还券 |
| 代码 | 股票代码 | AAPL |
| 成交价格 | 成交价格 | 150.50 |
| 成交数量 | 成交股数 | 100 |
| 成交时间 | 成交时间 | 2024/01/15 09:30:00 |
| 市场 | 市场类型 | 美股/港股/沪深 |
| 交易状态 | 订单状态 | 全部成交/部分成交/已撤单 |

### 可选字段

| 字段名 | 说明 |
|--------|------|
| 名称 | 股票名称 |
| 订单价格 | 委托价格 |
| 订单数量 | 委托数量 |
| 币种 | 交易币种 |
| 合计费用 | 总费用 |
| 佣金 | 佣金 |
| 平台使用费 | 平台费 |

---

## 富途证券 (英文) - futu_en

**编码**: UTF-8  
**分隔符**: 逗号

### 必需字段

| Field | Description | Example |
|-------|-------------|---------|
| Side | Trade direction | Buy/Sell/Short Sell/Buy to Cover |
| Symbol | Stock code | AAPL |
| Fill Price | Fill price | 150.50 |
| Fill Qty | Fill quantity | 100 |
| Fill Time | Fill time | 2024/01/15 09:30:00 |
| Market | Market type | US/HK/CN |
| Status | Order status | Filled/Partially Filled/Cancelled |

---

## 老虎证券 - tiger_cn

**编码**: UTF-8  
**分隔符**: 逗号

### 字段映射

| 字段名 | 说明 |
|--------|------|
| 交易方向 | 买入/卖出 |
| 股票代码 | 标的代码 |
| 股票名称 | 标的名称 |
| 成交均价 | 成交价格 |
| 成交数量 | 成交股数 |
| 成交金额 | 成交金额 |
| 成交时间 | 成交时间 |
| 币种 | 交易币种 |
| 手续费 | 总费用 |

---

## 中信证券 - citic_cn

**编码**: GBK  
**分隔符**: 逗号

### 字段映射

| 字段名 | 说明 |
|--------|------|
| 委托方向 | 买入/卖出 |
| 证券代码 | A股代码 |
| 证券名称 | 股票名称 |
| 成交价格 | 成交价格 |
| 成交数量 | 成交股数 |
| 成交金额 | 成交金额 |
| 成交时间 | 成交时间 |
| 手续费 | 佣金 |
| 过户费 | 过户费 |
| 印花税 | 印花税 |
| 席位代码 | 营业部代码 |

---

## 华泰证券 - huatai_cn

**编码**: GBK  
**分隔符**: 逗号

### 字段映射

| 字段名 | 说明 |
|--------|------|
| 买卖方向 | 买入/卖出 或 1/2 |
| 证券代码 | A股代码 |
| 证券名称 | 股票名称 |
| 成交价格 | 成交价格 |
| 成交数量 | 成交股数 |
| 成交金额 | 成交金额 |
| 成交时间 | 成交时间 |
| 佣金 | 佣金 |
| 过户费 | 过户费 |
| 经手费 | 交易所经手费 |
| 证管费 | 证监会征费 |

---

## 添加新券商

如需支持新券商格式，在 `scripts/import_trades.py` 的 `BROKER_CONFIGS` 中添加配置：

```python
"new_broker": {
    "name": "新券商名称",
    "encoding": "utf-8",  # 或 gbk
    "detect_columns": ["特征字段1", "特征字段2"],
    "field_map": {
        "原字段名": "标准字段名",
        # ...
    },
    "direction_map": {"买入": "buy", "卖出": "sell"},
    "status_map": {"已成交": "filled"},
    "market_map": {},
}
```

### 标准字段名

| 字段 | 说明 | 必需 |
|------|------|------|
| symbol | 股票代码 | ✅ |
| symbol_name | 股票名称 | |
| direction | 交易方向 (buy/sell/sell_short/buy_to_cover) | ✅ |
| filled_price | 成交价格 | ✅ |
| filled_quantity | 成交数量 | ✅ |
| filled_amount | 成交金额 | |
| filled_time | 成交时间 | ✅ |
| market | 市场 (us/hk/cn) | |
| currency | 币种 | |
| status | 状态 (filled/cancelled) | |
| total_fee | 总费用 | |
| commission | 佣金 | |
| transfer_fee | 过户费 | |
