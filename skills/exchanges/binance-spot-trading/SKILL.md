---
name: binance-spot-trading
description: 币安现货交易支持。每次调用自动扣费 0.001 USDT
version: 1.0.0
author: moson
tags:
  - binance
  - spot
  - trading
homepage: https://github.com/moson/binance-spot-trading
metadata:
  clawdbot:
    requires:
      env:
        - SKILLPAY_API_KEY
triggers:
  - "spot trading"
  - "binance spot"
  - "buy crypto"
config:
  SKILLPAY_API_KEY:
    type: string
    required: true
    secret: true
---

# Binance Spot Trading

币安现货交易支持。

## 什么是现货交易？

现货交易是指立即买入或卖出数字资产的交易方式。

### 核心功能

- 实时价格查询
- 买入卖出订单
- 账户余额查看

## 使用示例

{ action: 'price', pair: 'BTC/USDT' }
{ action: 'buy', pair: 'BTC/USDT', amount: 0.01 }

## 价格

每次调用: 0.001 USDT
