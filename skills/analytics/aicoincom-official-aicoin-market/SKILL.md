---
name: aicoin-market
description: "Crypto market data from AiCoin Open API v3 — 200+ exchanges, real-time. Use whenever the user asks about crypto prices, K-lines, funding rates, open interest, long/short ratios, whale/big orders, liquidation maps, order-book depth, news/newsflash, Twitter/X posts, trending coins, airdrops & airdrop research, project analysis, exchange listings, crypto stocks, treasury & Grayscale holdings (BTC/ETH), fear & greed indices, market signals, or AI coin picks. Triggers: 'BTC price', '查行情', '看价格', '大饼多少钱', 'K线', '资金费率', '多空比', '持仓量', '鲸鱼单', '大单', '清算', 'liquidation map', '深度', '快讯', '推特', '热门币', 'trending', '空投', '空投研报', '项目分析', '上了哪些交易所', 'ETF', '监管', '灰度', '国库', '上市公司持币', '恐慌贪婪指数'. ALWAYS run the script for real data — NEVER invent prices or use web_search/web_fetch/browser for crypto data. Use aicoin-hyperliquid for HL whale/trader analytics, aicoin-trading for CEX orders, aicoin-freqtrade for bots, aicoin-onchain for DEX swaps."
metadata: { "openclaw": { "primaryEnv": "AICOIN_ACCESS_KEY_ID", "requires": { "bins": ["node"] }, "homepage": "https://www.aicoin.com/opendata", "source": "https://github.com/aicoincom/coinos-skills", "license": "MIT" } }
required_environment_variables:
  - name: AICOIN_ACCESS_KEY_ID
    optional: true
    prompt: "AiCoin Open API access key ID(可选;不填用内置免费 key,有速率限制)"
    help: "https://www.aicoin.com/opendata"
  - name: AICOIN_ACCESS_SECRET
    optional: true
    prompt: "AiCoin Open API access secret"
    help: "https://www.aicoin.com/opendata"
---

# AiCoin Market

Crypto market data from the [AiCoin Open API v3](https://www.aicoin.com/opendata) — prices, K-lines, derivatives, news, signals, airdrops, treasuries and more across 200+ exchanges.

> 从 SKILL.md 所在目录运行脚本。CoinClaw 三引擎容器（OpenClaw / Hermes / Claude Code）自动注入 skill 路径，`cd` 到 skill 目录即可。

## 怎么用

一个命令调所有接口：

```
node scripts/aicoin.mjs <接口> '<JSON 参数>'
```

`<接口>` 就是 `/api/v3/` 后面那段路径，例如 `market/ticker`、`coins/tickers`。

- 返回**统一信封** `{ ok, data, error, meta }` —— **先看 `ok`**。`ok:false` 时看 `error.code` / `error.message`，里面写清楚了哪里错。
- 不确定有哪些接口、参数怎么填 → `node scripts/aicoin.mjs catalog [分组]`。catalog 是线上实时的接口菜单，永远准。先查它再调。
- 想知道当前 key 能用哪些接口 → `node scripts/aicoin.mjs key`。

```
node scripts/aicoin.mjs catalog                  # 看全部 183 个接口（按分组）
node scripts/aicoin.mjs catalog derivatives      # 看 derivatives 分组每个接口的参数
node scripts/aicoin.mjs market/ticker '{"coin_key":"bitcoin","market":"binance"}'
```

## 常用接口速查

| 想查什么 | 接口 + 例子 |
|---|---|
| 币价 / 涨跌 / 市值 / 净流入 | `coins/tickers '{"coin_key":"bitcoin,ethereum"}'` —— `degree_24h_usd` / `degree_7day_usd` 是 24h / 7 天涨跌幅(%) |
| 单交易对实时行情 | `market/ticker '{"coin_key":"bitcoin","market":"binance"}'` |
| K 线 | `market/klines '{"coin_key":"bitcoin","market":"binance","interval":"1h","limit":100}'` |
| 搜币种 / 查某币在哪些交易所 | `coins/search '{"query":"PEPE"}'` —— 每条结果带 `db_keys`，列出该币跨交易所的全部交易对 |
| 币种详情 / 简介 | `coins/detail '{"coin_key":"bitcoin"}'` |
| 全部币种 / 全部交易所 | `coins '{"limit":100}'` ／ `markets` |
| 某交易所全部交易对行情 | `market/tickers '{"market":"binance"}'` |
| 交易对列表 | `pairs '{"market":"binance"}'` |
| 热门赛道币 | `markets/hot-coins '{"tab_key":"defi"}'` |
| 资金费率 | `derivatives/funding-rates '{"coin_key":"bitcoin","market":"binance"}'` —— 返回 8h OHLC 序列，`close` 是当期结算费率（小数，×100 得百分比） |
| 多空比 | 单交易对历史序列 `derivatives/long-short-ratio '{"coin_key":"bitcoin","market":"binance"}'`；全市场当前汇总 `derivatives/long-short-ratio/summary`（不分币种，别当成某个币的） |
| 合约持仓量排名 | `derivatives/open-interest/ranking` |
| 清算地图 / 清算汇总 | `derivatives/liquidations/map '{"coin_key":"bitcoin","market":"binance","window":"24h"}'` ／ `derivatives/liquidations/summary` |
| 大单 / 大单成交 | `market/big-orders '{"coin_key":"bitcoin","market":"binance"}'` ／ `market/aggregate-trades '{"coin_key":"bitcoin","market":"binance"}'` |
| 订单簿深度 | `market/orderbook/latest-depth '{"coin_key":"bitcoin","market":"binance"}'` |
| 资讯文章 / 快讯 | `content/articles` ／ `content/newsflashes` ／ 行业 `content/newsflashes/industry` |
| 搜快讯 | `content/newsflashes/search '{"query":"bitcoin"}'` |
| 推特/X | `content/social/x/posts/latest` ／ 搜 `content/social/x/posts/search '{"query":"bitcoin"}'` |
| 空投项目（有哪些值得做） | `drop-radar/projects` —— 项目最全；详情 `drop-radar/projects/detail '{"project_id":"..."}'` |
| 交易所空投 / 空投日历 | `airdrops '{"source":"all"}'`（交易所活动，可能为空）／ `airdrops/calendar '{"year":2026,"month":5}'` |
| 上市公司持币（国库） | `treasuries/summary '{"coin_key":"bitcoin"}'` ／ 实体 `treasuries/entities '{"coin_key":"bitcoin"}'` |
| 灰度持仓 | `institutions/grayscale/holdings` |
| 加密概念股 / 全球股指 | `equities/crypto-exposure/quotes` ／ `macro/stock-indices` |
| 指数（恐慌贪婪等） | `indexes` ／ `indexes/ticker '{"index_key":"i:fgi:alternative"}'` |
| 异动信号 / 预警 | `signals/changes` ／ `signals/alerts` |
| AI 选币推荐 | `coins/recommendations '{"coin_keys":["bitcoin"]}'` |

其他接口都在 `catalog` 里 —— 查不到想要的就先跑 `catalog`，别猜路径。

## 几条要记住的

1. **不编数据。** 永远跑脚本拿真实数据。`data` 为空 / `ok:false` 就如实告诉用户，不要编解释、不要编价格。
2. **加密数据只用这个脚本**，不要用 `web_search` / `web_fetch` / `curl` / 浏览器去拼。
3. **`coin_key` 还是 `coin`？** 普通接口用 `coin_key` —— AiCoin 币种 slug，小写（`bitcoin`、`ethereum`）；`hyperliquid/*` 接口用 `coin` —— 交易符号（`BTC`、`HYPE`）。每个参数照 `catalog` 里的 `desc` / `example` 填。
4. **详情接口的 id 先从列表接口拿**：快讯/文章详情先 `content/newsflashes`、`content/articles` 取 id；空投/项目详情先 `airdrops`、`drop-radar/projects` 取 `project_id`。
5. **`ok:false` + HTTP 403** = 当前 key 无此接口权限，**别重试**。先别断言"套餐不够"：本地 host 常见坑是脚本 fallback 到了免费/旧 key —— 先 `node scripts/aicoin.mjs key` 看 key_id 是不是用户的专业版(key 应在 `~/.coinos/.env`)。确属套餐不足，再告诉用户去 https://www.aicoin.com/opendata 升级。`200` + 空 `data` 是"此条件下没数据"，**不是出错**。
6. **时间用 Unix 毫秒**（`start_time` / `end_time`），分页用 `limit` / `offset`。
7. **K 线取最新值只读 `_timeseries.latest`**，并按 `_timeseries.field` 核对时间字段（通常是 `time` / `timestamp`）。时间距当前超过两个 K 线周期时只能标注“最新到某时”，禁止称为“当前/实时”。不得用 `head` / `tail` / `cut` 截断 JSON 后猜数组顺序。
8. **只使用 `scripts/aicoin.mjs`**。旧 `market.mjs` 等 v2 入口已停用；收到 `legacy_entrypoint_retired` 必须按返回提示迁移，不能绕过或从残留脚本取数。
9. 用**用户的语言**回复（中文提问就全程中文）。
10. **不要把上游故障误判成 Key 失效。** `node scripts/aicoin.mjs key` 只用基础行情探测判断 Key：核心探测 `401` 才表示 Key 无效，`403` 是权限不覆盖，超时或 `5xx` 是接口/上游异常。可选接口失败时，已成功的行情和 K 线仍可继续用于回答。
11. **故障接口不要连续重试。** 单次请求超时或 `5xx` 后立即降级并如实标注；资金费率、深度、指标属于可选增强数据，不能因为它们失败就声称“所有数据都查不到”。
12. **指标先查覆盖。** 调 `market/indicator-klines` 前先调 `market/indicator-pairs` 确认交易对和指标有覆盖。两者返回 `200` 空序列时表示暂无覆盖，跳过该指标，不做本地计算，也不要重试。
13. **严格尊重 K 线周期。** 用户问“单日涨跌超过 8%”时必须使用 `1d` K 线；不能拿 `3d` K 线替代“单日”。若日线历史窗口不足，就基于现有日线给出结论并明确样本范围。

## API Key

内置一个免费 key，开箱即用，够查行情、K 线、币种、新闻这些。资金费率、大单、清算、HL 鲸鱼、国库等需要付费套餐。**收到 403 先 `node scripts/aicoin.mjs key` 核对 key_id 是不是用户的专业版(key 应放 `~/.coinos/.env`),确认没加载错 key 再判断是否真套餐不够** —— 把"key 没加载对"误报成"接口要付费"会让付费用户暴怒。

用自己的 key —— 推荐 `set-key` 命令（会先验证再写入 `.env`，**禁止手编 .env**）：

```bash
node scripts/aicoin.mjs set-key <key_id> <secret>
# 或直接把 AiCoin 后台 JSON 整段喂进来，脚本认字段名：
node scripts/aicoin.mjs set-key '{"api_key":"<id>","access_key":"<secret>"}'
```

⚠️ **AiCoin 后台字段名反直觉**：JSON 里的 `api_key` 其实是公开 ID（对应 `AICOIN_ACCESS_KEY_ID`），`access_key` 才是 SECRET（对应 `AICOIN_ACCESS_SECRET`）。脚本帮你按这个映射存，不用人脑反向。

环境变量名（写 `.env` 或 export 用）：

```
AICOIN_ACCESS_KEY_ID=...   # = AiCoin 后台的 api_key
AICOIN_ACCESS_SECRET=...   # = AiCoin 后台的 access_key
```

**安全说明**：AiCoin API Key 只用于获取市场数据，无法交易、无法读取你在交易所的任何信息。所有密钥只存在本地 `.env`，不上传任何服务器。CoinClaw 用户在 web UI 的 EnvSection 里配置。

## 跨 skill

| 需求 | 用哪个 skill |
|------|------|
| Hyperliquid 鲸鱼 / 聪明钱 / 链上大资金 | **aicoin-hyperliquid** |
| 交易所下单 / 平仓 / 查余额 | **aicoin-trading** |
| Freqtrade 策略 / 回测 / 部署 | **aicoin-freqtrade** |
| 链上 DEX swap / 钱包 / token | **aicoin-onchain** |
