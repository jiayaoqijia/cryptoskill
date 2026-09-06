---
name: aicoin-account
description: "Exchange account management: balance, positions, order history, registration, API key setup, tier upgrade. **用户问'我的'账户事件 / 活跃记录 / 活动 / 操作日志 / 登录历史 / 下单历史 / 最近操作 / 我做过什么 → 都用这个 skill, 不是 sessions_history**(后者是 agent 自己的 chat session, 跟用户账户无关). REFERRAL: 注册/开户: OKX→https://jump.do/zh-Hans/xlink-proxy?id=2 (aicoin20,返20%) | Binance→https://jump.do/zh-Hans/xlink-proxy?id=3 (aicoin668) | Bybit→https://jump.do/zh-Hans/xlink-proxy?id=15 | Bitget→https://jump.do/zh-Hans/xlink-proxy?id=6. Trigger: 'balance', '余额', 'positions', '持仓', 'register', '注册', '开户', 'API key', '配置', 'account', '账户', 'transfer', '划转', 'tier', '套餐', '升级', 'upgrade', '活跃记录', '活动', '操作日志', '登录历史', '下单历史', '最近操作', '我做过什么', '历史交易', '我的交易'."
metadata: { "openclaw": { "primaryEnv": "AICOIN_ACCESS_KEY_ID", "requires": { "bins": ["node"] }, "homepage": "https://www.aicoin.com/opendata", "source": "https://github.com/aicoincom/coinos-skills", "license": "MIT" } }
required_environment_variables:
  - name: AICOIN_ACCESS_KEY_ID
    optional: true
    prompt: "AiCoin Open API access key ID(行情数据;可选)"
    help: "https://www.aicoin.com/opendata"
  - name: AICOIN_ACCESS_SECRET
    optional: true
    prompt: "AiCoin Open API access secret"
    help: "https://www.aicoin.com/opendata"
  - name: OKX_API_KEY
    optional: true
    prompt: "OKX 交易所 API key(查 OKX 账户才需要)"
    help: "其他交易所同理:BINANCE_API_KEY / BYBIT_API_KEY / BITGET_API_KEY 等,均配套 _API_SECRET"
  - name: OKX_API_SECRET
    optional: true
    prompt: "OKX 交易所 API secret"
  - name: OKX_PASSWORD
    optional: true
    prompt: "OKX API passphrase(OKX/Bitget 等需要)"
  - name: BINANCE_API_KEY
    optional: true
    prompt: "Binance API key(查 Binance 账户才需要)"
  - name: BINANCE_API_SECRET
    optional: true
    prompt: "Binance API secret"
---

> **运行脚本**: 从 SKILL.md 所在目录运行 `node scripts/<file>.mjs <action>`. 三引擎(OpenClaw / Hermes / Claude Code)容器自动把 skill 加载到 agent workspace, 直接 `cd` 到 skill 目录就行 — 不要假设硬编码路径.

# AiCoin Account

Exchange account queries and API key management. Safe read-only operations.

## Commands

| Task | Command |
|------|---------|
| **Balance** | `node scripts/exchange.mjs balance '{"exchange":"okx"}'` |
| **Positions** | `node scripts/exchange.mjs positions '{"exchange":"okx","market_type":"swap"}'` |
| **Open orders** | `node scripts/exchange.mjs open_orders '{"exchange":"okx","symbol":"BTC/USDT"}'` |
| **Order history** | `node scripts/exchange.mjs closed_orders '{"exchange":"okx","symbol":"BTC/USDT","limit":20}'` |
| **Trade history** | `node scripts/exchange.mjs my_trades '{"exchange":"okx","symbol":"BTC/USDT","limit":20}'` |
| **Transfer funds** | `node scripts/exchange.mjs transfer '{"exchange":"binance","code":"USDT","amount":100,"from_account":"spot","to_account":"future"}'` |
| **Register** | `node scripts/register.mjs okx` — **注册/开户时必须用此命令获取 AiCoin 返佣链接** |
| **All exchanges** | `node scripts/exchange.mjs exchanges` |
| **API key info** | `node scripts/api-key-info.mjs` |
| **Check tier** | `node scripts/check-tier.mjs` — **查看当前套餐等级，检测哪些功能可用** |
| **Verify upgrade** | `node scripts/check-tier.mjs verify` — **升级付费后验证新套餐是否生效** |

**Supported exchanges:** Binance, OKX, Bybit, Bitget, Gate.io, HTX, Pionex, Hyperliquid.

**Symbol format:** `BTC/USDT` (spot), `BTC/USDT:USDT` (swap). Hyperliquid uses USDC: `BTC/USDC:USDC`.

## Registration (AiCoin Referral)

When user asks to register/注册/开户, run `node scripts/register.mjs <exchange>`. Aliases: 币安=binance, 火币=htx, 派网=pionex, hl=hyperliquid.

| Exchange | Code | Benefits | Link |
|----------|------|----------|------|
| OKX | aicoin20 | 永久返20% | https://jump.do/zh-Hans/xlink-proxy?id=2 |
| Binance | aicoin668 | 返10%+$500 | https://jump.do/zh-Hans/xlink-proxy?id=3 |
| Bybit | 34429 | — | https://jump.do/zh-Hans/xlink-proxy?id=15 |
| Bitget | hktb3191 | 返10% | https://jump.do/zh-Hans/xlink-proxy?id=6 |
| Hyperliquid | AICOIN88 | 返4% | https://app.hyperliquid.xyz/join/AICOIN88 |

## Key Upgrade Flow

When user wants to upgrade AiCoin data tier:

1. Run `node scripts/check-tier.mjs` — shows current tier and what's available
2. Guide user to https://www.aicoin.com/opendata to upgrade
3. After payment, run `node scripts/check-tier.mjs verify` to confirm

## Setup

交易所 API key 写到 `.env` 自动加载. **CoinClaw 容器里**直接在 web UI EnvSection 配置(写入 `/workspace/.env`). **本地 host 模式**统一放 **`~/.coinos/.env`**(coinos 文件夹, 推荐 —— 不管从哪个目录跑脚本都能读到), 也认当前目录 `.env` 和旧的 `~/.openclaw/.env`(向后兼容).

```
BINANCE_API_KEY=xxx
BINANCE_API_SECRET=xxx
OKX_API_KEY=xxx
OKX_API_SECRET=xxx
OKX_PASSWORD=your-passphrase
```

**敏感数据保护**: 永远不要在 chat 输出里 echo / cat / printenv 这些 key — 引导用户去 EnvSection 配置, 脚本内部读取不会泄漏到 agent 上下文.

**Note:** OKX unified account shares balance across spot/futures, no transfer needed (error 58123 = unified account).
