---
name: airdrop-hunter
description: 空投猎人，自动发现潜在空投机会，追踪已参与项目状态。每次调用收费0.001 USDT。触发词：空投、airdrop、撸毛、白名单、空投查询。
---

# 空投猎人

每次调用收费 0.001 USDT。收款钱包: 0x64f15739932c144b54ad12eb05a02ea64f755a53

## 功能

- **空投发现**: 扫描最新空投机会
- **参与追踪**: 记录已参与的空投
- **快照检查**: 检查地址是否符合条件
- **收益统计**: 计算空投总收益

## 使用方法

```bash
# 查看当前空投机会
python scripts/airdrop_hunter.py

# 检查地址是否符合某空投
python scripts/airdrop_hunter.py <ADDRESS>
```

## 输出示例

```
🎁 空投猎人
━━━━━━━━━━━━━━━━
🔥 热门空投:
1. LayerZero (预计Q2)
   状态: 快照完成
   预估: $500-2000

2. zkSync Era
   状态: 进行中
   条件: 桥接+交互

3. Starknet
   状态: 已发放
   领取: ✅ 已领取 $350

📊 空投总收益: $2,450

✅ 已扣费 0.001 USDT
```
