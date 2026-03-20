---
name: binance-futures-trading
description: 币安合约交易支持，包括杠杆和合约订单。每次调用自动扣费 0.001 USDT
version: 1.0.0
author: moson
tags:
  - binance
  - futures
  - trading
  - leverage
homepage: https://github.com/moson/binance-futures-trading
metadata:
  clawdbot:
    requires:
      env:
        - SKILLPAY_API_KEY
triggers:
  - "binance futures"
  - "futures trading"
  - "leverage"
config:
  SKILLPAY_API_KEY:
    type: string
    required: true
    secret: true
---

# Binance Futures Trading

币安合约交易支持，包括杠杆和合约订单管理。

## 功能

- 账户余额查询
- 持仓信息查看
- 开仓平仓操作
- 杠杆管理

## 使用示例

{ action: 'balance' }
{ action: 'position' }

## 风险提示

合约交易风险高，可能损失全部本金。

## 价格

每次调用: 0.001 USDT
