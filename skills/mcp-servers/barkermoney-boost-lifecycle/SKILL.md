---
name: boost-lifecycle
version: 0.1.1
description: >
  Full-lifecycle playbook for Barker boost campaigns: deposit with reward attribution,
  expiry reminders, reward claiming, redemption, and risk monitoring —
  every money-moving step via campaign-bound execution intents with explicit user confirmation.
  Powered by Barker (https://barker.money) — The Stablecoin Yield Map.
---

# Boost Campaign Lifecycle

## When to Activate

关键词：boost 活动、参与活动、全程参与、活动奖励、领奖、claim、到期赎回、活动到期、
campaign、锁定期、赎回期、活动收益、帮我管理活动。

## Knowledge Base

### Boost 活动机制（必须先懂再动手）

- boost 活动 = 「存入指定金库 + 按归因份额计奖 + merkle 领取」。奖励口径 min(D, C)：
  D = 经 Barker 入口归因的累计存入份额；C = 钱包链上真实份额。**不带 campaign_id 的存入只涨 C
  不涨 D，不计奖**——这是所有 boost 执行必须绑定 campaign_id 的原因。
- 活动关键字段（get_campaign_detail / 活动列表返回）：campaign_id（绑定 id，如 lp_4）、
  锁定期 lock_days、赎回期 redemption_days、start/end 时间、opening_apy、奖励 token。
- 奖励发放：后端按期（epoch）生成 merkle root 上链，用户按 proof 领取；可领 = 累计 − 已领。
  root 未上链（root_pending）/ 本期无记录（no_proof）/ 领取暂停（paused）都属正常中间态，
  如实转述，不要当成故障。

### 五个功能的工具组合配方

1. **参与/存入**：**query_boost_campaigns 拿活动与条款**（含未开始的预告活动；
   query_active_campaigns 看不到 scheduled 的 boost）→ 查 portfolio（红线：实时）→
   资产不符时先 execution_quote_swap 换币 → **复述条款（锁定期/赎回期/奖励口径/结束时间/金额）
   并获用户明确"确认"** → execution_prepare_vault_action(create_intent=true, campaign_id=活动绑定id)
   → 授权按钮。
2. **到期提醒**：schedule_monitoring_task（到期前 N 天提醒）。
3. **领奖 claim**：execution_campaign_rewards(campaign_id) 查可领 → status=claimable 且用户
   确认 → execution_create_intent(action=claim, campaign_id) → 授权按钮 → 广播回 tx。
4. **到期赎回**：确认赎回期已开 → execution_prepare_vault_action(action=redeem,
   create_intent=true, campaign_id) → 授权按钮。排队赎回类协议暂不支持 agent 执行，
   降级为提醒 + boost 页链接。
5. **风控盯盘**：schedule_monitoring_task（盯脱锚 / APY 下滑 / TVL 变化）。触发时**提醒 + 给一键赎回入口**，绝不自动赎回（每笔都要用户当轮确认）。

### 活动未开始（预告期）的正确姿势

query_boost_campaigns 返回 start 在未来 / apy_kind=opening 的活动 = 预告期：如实告知开始时间与
预期开盘 APY，先搭方案（save_yield_plan）+ 开始提醒（schedule_monitoring_task），**开始后**再建
存入凭证。**绝不因 query_active_campaigns 查不到就说活动不存在**。

### 硬边界（违反即事故）

- 所有 boost 存入/赎回/领奖必须带 campaign_id（campaign 专属 intent）；活动结束/暂停时后端拒绝
  存入，**不要**改成普通存款绕过（不计奖，坑用户）。
- 条款确认 + 授权按钮 = 双重确认，缺一不可；定时任务/方案步骤永远不静默建 boost intent。
- 绝不声称已存入/已领取/已赎回——广播只在用户点授权按钮后发生。
