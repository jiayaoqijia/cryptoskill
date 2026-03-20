---
name: crypto-strategy-suite
description: "BTC/USDT 量化策略套件：含网格、信号、暴跌抄底、合约趋势、合约突破 5 大策略，现货+合约全覆盖。"
version: 1.1.0
user-invocable: true
metadata: {"openclaw":{"emoji":"📈","homepage":"https://skillpay.me","os":["darwin","linux"],"requires":{"env":["EXCHANGE_API_KEY","EXCHANGE_API_SECRET","SKILLPAY_API_KEY"],"bins":["node","curl"]},"primaryEnv":"EXCHANGE_API_KEY","install":[{"kind":"node","package":"ccxt"},{"kind":"node","package":"technicalindicators"}]}}
---

# 📈 Crypto Strategy Suite — BTC/USDT 量化策略套件

> 5 大量化策略一键部署，现货 + 合约全覆盖，Maker 低手续费优化。

## 💰 付费说明（SkillPay）

本 Skill 为付费 Skill，每次调用通过 [SkillPay](https://skillpay.me) 自动计费。

**计费模式：** 按调用次数收费（per-call），BNB Chain 链上结算，95% 收入归开发者。

**使用流程：**

1. 用户运行 `/crypto-strategy-suite`
2. Skill 自动调用 SkillPay `/billing/charge` 接口扣费
3. 扣费成功 → 执行策略逻辑
4. 扣费失败（余额不足）→ 返回充值链接，用户充值后重试

```javascript
// ═══════════════════════════════════════════════════
// SkillPay Billing Integration / 计费接入
// ═══════════════════════════════════════════════════
const BILLING_API_URL = 'https://skillpay.me';
const BILLING_API_KEY = process.env.SKILLPAY_API_KEY;
const SKILL_ID = 'cae1f779-f64b-4ba3-a040-0d0e9911c835';

// ① Check balance / 查余额
async function checkBalance(userId) {
  const resp = await fetch(
    `${BILLING_API_URL}/api/v1/billing/balance?user_id=${userId}`,
    { headers: { 'X-API-Key': BILLING_API_KEY } }
  );
  const data = await resp.json();
  return data.balance;  // USDT amount
}

// ② Charge per call / 每次调用扣费
async function chargeUser(userId) {
  const resp = await fetch(`${BILLING_API_URL}/api/v1/billing/charge`, {
    method: 'POST',
    headers: {
      'X-API-Key': BILLING_API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: userId,
      skill_id: SKILL_ID,
      amount: 0.003,  // USDT per call / 每次调用单价
    }),
  });
  const data = await resp.json();
  if (data.success) {
    return { ok: true, balance: data.balance };
  }
  // 余额不足 → 返回充值链接
  return { ok: false, balance: data.balance, paymentUrl: data.payment_url };
}

// ③ Generate payment link / 生成充值链接
async function getPaymentLink(userId, amount) {
  const resp = await fetch(`${BILLING_API_URL}/api/v1/billing/payment-link`, {
    method: 'POST',
    headers: {
      'X-API-Key': BILLING_API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: userId, amount }),
  });
  const data = await resp.json();
  return data.payment_url;  // BNB Chain USDT 付款链接
}

// ═══════ 使用示例 ═══════
// async function handleRequest(userId) {
//   const result = await chargeUser(userId);
//   if (result.ok) {
//     // ✅ 执行策略逻辑
//     return { success: true };
//   } else {
//     // ❌ 余额不足，返回充值链接
//     return { success: false, paymentUrl: result.paymentUrl };
//   }
// }
```

> 开发者在 [skillpay.me](https://skillpay.me) 注册后获取 `SKILLPAY_API_KEY`，设置单次调用价格，即可开始收费。收入可在 SkillPay Dashboard 实时查看并提现。

---

## 📋 策略列表（全部已启用）

| 序号 | 策略名 | 类型 | 启用 | 说明 |
|------|--------|------|------|------|
| 1 | `grid_trading` | 现货 | ✅ 是 | 网格策略，BTC/USDT，12 层，每层 25 USDT，Maker 模式 |
| 2 | `signal_trading` | 现货 | ✅ 是 | 信号策略，BTC/USDT，EMA+RSI，止盈 5%、止损 3% |
| 3 | `crash_buy` | 现货 | ✅ 是 | 暴跌抄底，BTC/USDT，跌幅 5% 触发，止盈 6%、止损 3% |
| 4 | `futures_trend` | 合约 | ✅ 是 | 合约趋势，BTC/USDT，多空，阶梯入场+时间止损+ATR 门禁 |
| 5 | `futures_breakout` | 合约 | ✅ 是 | 合约突破，BTC/USDT，仅多，consolidation+突破+量比 |

---

## 🔧 环境变量配置

在使用前，请确保已设置以下环境变量：

```bash
# 交易所 API（支持 Binance / OKX / Bybit）
export EXCHANGE_API_KEY="your-api-key"
export EXCHANGE_API_SECRET="your-api-secret"

# SkillPay API Key（在 https://skillpay.me 注册获取）
export SKILLPAY_API_KEY="your-skillpay-api-key"
```

---

## 📊 策略详细说明

### 1. grid_trading — 网格策略（现货）

**原理：** 在价格区间内等分 12 层网格，每层挂 25 USDT 的限价单（Maker），价格下穿买入、上穿卖出，赚取震荡差价。

**参数：**
- 交易对：BTC/USDT
- 网格层数：12
- 每层金额：25 USDT
- 挂单模式：Maker Only（Post-Only）
- 网格间距：自动根据 ATR(14) 计算
- 总投入：约 300 USDT

**适用行情：** 横盘震荡、窄幅波动

---

### 2. signal_trading — 信号策略（现货）

**原理：** 基于 EMA 交叉 + RSI 超卖/超买信号触发买卖。EMA(9) 上穿 EMA(21) 且 RSI < 35 时买入，EMA(9) 下穿 EMA(21) 或 RSI > 70 时卖出。

**参数：**
- 交易对：BTC/USDT
- 快线：EMA(9)
- 慢线：EMA(21)
- RSI 周期：14
- 止盈：5%
- 止损：3%
- K 线周期：15m

**适用行情：** 趋势启动初期、震荡突破

---

### 3. crash_buy — 暴跌抄底（现货）

**原理：** 监控 BTC 短期跌幅，当 15 分钟内跌幅超过 5% 时触发抄底买入，设置止盈 6%、止损 3%。

**参数：**
- 交易对：BTC/USDT
- 触发条件：15min 跌幅 ≥ 5%
- 买入方式：市价单
- 止盈：6%
- 止损：3%
- 冷却时间：60 分钟（防止连续触发）

**适用行情：** 闪崩、恐慌抛售后的 V 型反弹

---

### 4. futures_trend — 合约趋势（合约）

**原理：** 趋势跟踪策略，支持多空双向。阶梯入场分 3 批建仓，降低入场成本；时间止损在持仓超过 4 小时无盈利时自动平仓；ATR 门禁过滤低波动行情。

**参数：**
- 交易对：BTC/USDT 永续合约
- 方向：多空双向
- 杠杆：3x（建议）
- 入场方式：阶梯 3 批（40% / 30% / 30%）
- 时间止损：持仓 > 4h 且浮亏时平仓
- ATR 门禁：ATR(14) > 近 50 周期均值时才开仓
- 止损：ATR 的 1.5 倍
- 止盈：ATR 的 3 倍（盈亏比 2:1）

**适用行情：** 单边趋势、大波动行情

---

### 5. futures_breakout — 合约突破（合约）

**原理：** 识别 BTC 价格 consolidation（收敛整理），当价格向上突破且成交量放大时做多入场。仅做多方向，适合牛市趋势。

**参数：**
- 交易对：BTC/USDT 永续合约
- 方向：仅多
- 杠杆：3x（建议）
- Consolidation 识别：布林带宽度 < 近 20 周期最小值
- 突破确认：收盘价 > 布林上轨
- 量比要求：当前成交量 > MA(20) 成交量的 1.5 倍
- 止损：布林中轨
- 止盈：突破幅度的 2 倍

**适用行情：** 盘整后的趋势启动、牛市回调整理后

---

## ⚠️ 风险提示

- 本策略套件仅供学习和参考，不构成投资建议
- 合约交易具有高杠杆风险，可能导致全部本金损失
- 请使用可承受损失的资金运行策略
- 建议先在测试网 (Testnet) 充分验证后再投入实盘
- 市场极端行情下，止损可能滑点执行

---

## 🚀 快速开始

运行 Skill 后，按照交互提示选择要启用的策略：

```
/crypto-strategy-suite

> 请选择要运行的策略：
> [1] grid_trading   — 网格策略（现货）
> [2] signal_trading  — 信号策略（现货）
> [3] crash_buy       — 暴跌抄底（现货）
> [4] futures_trend   — 合约趋势（合约）
> [5] futures_breakout — 合约突破（合约）
> [A] 全部启用
```

选择后 Skill 将自动配置参数并启动策略监控循环。
