---
name: binance-grid-trading
description: 网格交易策略 - 自动化低买高卖。每次调用自动扣费 0.001 USDT
version: 1.0.0
author: moson
tags:
  - binance
  - grid
  - trading
  - bot
homepage: https://github.com/moson/binance-grid-trading
metadata:
  clawdbot:
    requires:
      env:
        - SKILLPAY_API_KEY
triggers:
  - "grid trading"
  - "binance grid"
  - "range trading"
  - "automated trading"
config:
  SKILLPAY_API_KEY:
    type: string
    required: true
    secret: true
---

# Binance Grid Trading

在指定价格区间内自动网格交易，低买高卖。

## 什么是网格交易？

网格交易是一种自动化交易策略，将价格区间分成若干网格，在每个网格价格自动买入或卖出。

### 核心功能

- **区间设置**: 自定义价格上限和下限
- **网格数量**: 可调整网格密度（5-100格）
- **自动套利**: 价格触网格自动买卖
- **利润追踪**: 实时显示已获利金额

### 策略参数

- 价格区间: 用户自定义（如 $42,000-$45,000）
- 网格数量: 5-100
- 订单类型: 限价单
- 止盈策略: 可选

## 使用示例

```javascript
// 查看网格状态
await handler({ action: 'status' });

// 创建新网格
await handler({ 
  action: 'start', 
  pair: 'BTC/USDT', 
  min: 42000, 
  max: 45000,
  grids: 10 
});

// 停止网格
await handler({ action: 'stop' });
```

## 价格

每次调用: 0.001 USDT

## 风险提示

1. 震荡市场效果最好
2. 单边趋势可能导致亏损
3. 需充足资金覆盖所有网格
4. 建议设置止盈止损
5. 价格突破区间需要手动干预

## 网格交易技巧

1. 选择震荡剧烈的币种
2. 合理设置价格区间
3. 预估资金需求
4. 定期检查和调整
5. 设置自动止损

## 适合人群

- 不想时刻盯盘的投资者
- 喜欢稳健收益的交易者
- 对市场有区间判断能力的用户
