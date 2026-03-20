---
name: binance-price-alerts
description: 设置价格提醒和自动触发交易。每次调用自动扣费 0.001 USDT
version: 1.0.0
author: moson
tags:
  - binance
  - alerts
  - notifications
homepage: https://github.com/moson/binance-price-alerts
metadata:
  clawdbot:
    requires:
      env:
        - SKILLPAY_API_KEY
triggers:
  - "price alerts"
  - "notifications"
  - "price target"
  - "alert me"
config:
  SKILLPAY_API_KEY:
    type: string
    required: true
    secret: true
---

# Binance Price Alerts

设置价格提醒和自动触发交易。

## 功能

价格提醒是交易者的重要工具，帮助捕捉关键价格点位。

### 核心功能

- **价格提醒设置**: 设置目标价格
- **条件触发**: 价格above/below 触发
- **自动交易**: 达到条件自动下单
- **多提醒管理**: 同时设置多个提醒

### 提醒类型

- 价格above目标
- 价格below目标
- 百分比变化
- 成交量异常

## 使用示例

```javascript
// 查看所有提醒
await handler({ action: 'list' });

// 添加提醒
await handler({ 
  action: 'add', 
  pair: 'BTC/USDT', 
  price: 45000,
  condition: 'above'
});

// 移除提醒
await handler({ action: 'remove', alertId: '123' });
```

## 价格

每次调用: 0.001 USDT

## 使用技巧

1. 设置合理的提醒价格
2. 不要设置过于接近当前价格
3. 及时清理已触发提醒
4. 结合技术分析设置
