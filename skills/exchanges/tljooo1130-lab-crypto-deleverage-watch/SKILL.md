---
name: crypto-deleverage-watch
description: >
  Monitor whether a crypto perpetual-futures leverage flush looks complete
  using OKX and Binance public APIs: account long/short ratio, open-interest
  drawdown from a running high, top-trader position (notional) ratio, and
  short-vs-long filled liquidations, with near/met thresholds and
  notify-only-on-status-change alerts. Use when the user asks if a dump was
  "just a leverage flush", whether open interest and long-short ratios show
  the cleanup is done, whether retail is still adding longs, or wants a
  30-minute BTC/ETH deleveraging watch. No API keys. Not investment advice.
---

# Crypto deleverage watch / 合约杠杆出清监控

## English summary

This skill watches **BTC and ETH USDT-margined perpetuals** (extendable to other coins) and answers: *has the leverage flush gone far enough, or is crowded long positioning still in place?*

It uses **only public, keyless exchange endpoints** (OKX + Binance). It does **not** use CoinGlass / AiCoin / Blave or any paid aggregator.

**Four scored conditions** (defaults from a live 30-minute watch):

1. **Account long/short ratio** — OKX `long-short-account-ratio` (by `ccy`) and Binance `globalLongShortAccountRatio`. Combined status is conservative: `max(OKX, Binance)`. **Near < 2.3, met < 2.0**.
2. **Open-interest drawdown** from the running high since the window start, **coin-denominated**. OKX `open-interest-history` (`oiCcy`) and Binance `openInterestHist` (`sumOpenInterest`). Update the stored high when OI makes a new high. **Near ≥ 15%, met ≥ 20%**. Coin status uses the larger drop (either venue can trigger).
3. **OKX top-trader position (notional) ratio** — `long-short-position-ratio-contract-top-trader` (**`instId` is required**). **Near ≥ 0.95, met ≥ 1.0**. Binance `topLongShortPositionRatio` is reference and is **flagged if < 1.5**. These two venues can sit on opposite sides of 1; do not treat the thresholds as symmetric.
4. **OKX filled liquidations**, last 1 hour and last 2 hours, short USD vs long USD. **Near** if 2h shorts ≥ 50% of 2h longs; **met** if ≥ 100% **and rising** (last hour short USD > the hour before). Contract value: BTC `0.01`, ETH `0.1`. Binance `allForceOrders` is **not public**.

**Notify** only when a condition **upgrades** (`none→near/met`, `near→met`) or **falls from `met`**. A drop from `near` to `none` stays quiet. If **three or more** conditions are `met` for the same asset, flag **“possibly mostly flushed” /「可能已基本出清」**.

**How to read the numbers**

- Long OI always equals short OI. There is no “long share of OI”. Judge positioning with account and top-trader **ratios**.
- If top traders are flat or net short by notional while OI rises, the new longs are coming from **retail**.
- Common bottom *context* (not a scored condition): account ratio down toward or below 2; OI down 10–20%+ from the high; funding still negative while price stops making new lows.
- Condition 4 at `met` on a bounce is often a **short squeeze**, not proof that longs have been cleared. Always read it next to conditions 1–3.
- Bottoms often wick the prior low first. Do not treat a single bounce as completion.

Always end user-facing answers with: **以上只是信息整理，不构成投资建议.**

Run:

```bash
python3 scripts/watch.py --state ./state.json --tz Asia/Bangkok
```

---

## 用途

在价格急跌或急涨之后，判断这更像「杠杆出清 / 轧空」还是出清还没走完。适用于：

- 用户问「今天这波是不是只是清理杠杆」「出清够不够」
- 要看账户多空比、持仓量回撤、大户仓位比、空头/多头强平对比
- 要做一个每 30 分钟的 BTC/ETH 出清监控，只在状态变化时通知

不要把输出写成买卖建议。数字对不上或接口失败时如实写进 `errors`，不要编造。

## 四个条件与默认阈值

| 条件 | 数据 | 接近 (near) | 满足 (met) | 合并规则 |
|------|------|-------------|------------|----------|
| 1. 账户多空比 | OKX 按 `ccy`；币安 `globalLongShortAccountRatio` | 比值 **< 2.3** | 比值 **< 2.0** | 取 `max(OKX, 币安)`，更保守（更高的比值 = 多头账户仍更拥挤） |
| 2. 持仓量相对窗口内高点的回撤 | 币种计价；OKX `oiCcy`，币安 `sumOpenInterest` | 回撤 **≥ 15%** | 回撤 **≥ 20%** | 任一交易所达到阈值即可（取较大回撤）；两边的百分比都要展示 |
| 3. OKX 大户**仓位金额**多空比 | `long-short-position-ratio-contract-top-trader` | **≥ 0.95** | **≥ 1.0** | 只以 OKX 计官方状态。币安 `topLongShortPositionRatio` 作参考，**< 1.5 就标记** |
| 4. OKX 近 2 小时空头强平对比多头 | 已成交强平，美元名义 | 空头 ≥ 多头的 **50%** | 空头 ≥ 多头的 **100%**，且最近 1 小时空头强平 **大于** 再往前 1 小时 | 只有 OKX；币安逐笔强平不公开 |

说明：

- 条件 3 的 OKX 阈值是「往上靠近 1」，来自实盘监控时 OKX 大户已经净空（比值 < 1）。它表示仓位在回到中性，不是「多头拥挤」。币安大户常常在 2 附近，所以参考阈值是往下跌破 1.5。两个交易所可能方向相反，不要混用同一套对称标准。
- 条件 4 在反弹中被「满足」，通常是小轧空。金额往往不大；必须和条件 1、2 对照。账户比仍在 3 以上、持仓量几乎没降，就不能说多头杠杆已经出清。
- 同一资产有 **3 个或以上** 条件为 `met` 时，输出 `possibly_mostly_flushed.flag_zh = 可能已基本出清`。这仍只是信号组合，不是底部确认。

## 数据源与接口

全部为公开接口，不需要 API key。

### OKX

| 数据 | 方法 | 路径 | 主要参数 | 备注 |
|------|------|------|----------|------|
| 现价 | GET | `https://www.okx.com/api/v5/market/tickers` | `instType=SWAP` | 读 `BTC-USDT-SWAP` / `ETH-USDT-SWAP` 的 `last` |
| 账户多空比 | GET | `https://www.okx.com/api/v5/rubik/stat/contracts/long-short-account-ratio` | `ccy=BTC` 或 `ETH`，`period=5m` | 返回多为 `[ts, ratio]`，新的在前 |
| 持仓量历史 | GET | `https://www.okx.com/api/v5/rubik/stat/contracts/open-interest-history` | `instId=BTC-USDT-SWAP`，`period=5m`，`limit=100`，翻页用 `end` | 用 **`oiCcy`（币数量）**，不要只用张数 |
| 大户仓位金额多空比 | GET | `https://www.okx.com/api/v5/rubik/stat/contracts/long-short-position-ratio-contract-top-trader` | **`instId`（不要用 ccy）**，`period=5m` | 当前接口需要 `instId` |
| 资金费率（仅上下文） | GET | `https://www.okx.com/api/v5/public/funding-rate` | `instId=BTC-USDT-SWAP` | 不计入四个条件 |
| 已成交强平 | GET | `https://www.okx.com/api/v5/public/liquidation-orders` | `instType=SWAP`，`uly=BTC-USDT`，`state=filled`，`limit=100`，翻页 `after=<最后一条 ts>` | 见下 |

强平美元名义：

```
usd = sz * contract_value * bkPx
```

`contract_value`：BTC-USDT-SWAP = **0.01** BTC，ETH-USDT-SWAP = **0.1** ETH。

方向：`posSide=long` 为多头被强平；`posSide=short` 为空头被强平；`posSide=net` 且 `side=sell` 视为多头被强平。

接口可能有延迟（最新 `filled` 时间早于当前几分钟）。分页必须覆盖满最近 2 小时，否则在 `errors` 里写明最早记录时间。

### 币安

| 数据 | 路径（先试 `https://fapi.binance.com`，失败再试 `https://www.binance.com`） | 参数 |
|------|------|------|
| 现价 | `/fapi/v1/ticker/price` | `symbol=BTCUSDT` |
| 全体账户多空比 | `/futures/data/globalLongShortAccountRatio` | `symbol`，`period=5m`，`limit=30`；读最后一条 `longShortRatio` |
| 持仓量历史 | `/futures/data/openInterestHist` | `symbol`，`period=5m`，`limit=500`；用 **`sumOpenInterest`（币数量）** |
| 大户仓位多空比 | `/futures/data/topLongShortPositionRatio` | `symbol`，`period=5m`，`limit=30` |
| 资金费率（上下文） | `/fapi/v1/premiumIndex` | `symbol`；字段 `lastFundingRate` |

注意：

- `fapi.binance.com` 在部分地区会返回 **HTTP 451**。回退到 `https://www.binance.com` 的同类公开路径。把这次用了回退写进输出。
- **`allForceOrders` 不是公开接口**，不要调用，也不要假装有币安逐笔强平。

## 状态文件

默认 `./state.json`，或环境变量 `DELEVERAGE_STATE`。示例见 [`examples/state.example.json`](examples/state.example.json)。

关键字段：

- `window_start`：持仓量高点的窗口起点。默认是 `--tz` 下当天 00:00。跨日会清空 `oi_high`，除非 `--keep-window` 或显式传入 `--window-start`。
- `oi_high` / `oi_high_ts`：各交易所、各币种的运行高点。当前持仓创新高时更新。
- `status`：四个条件在 BTC/ETH 上的 `none` / `near` / `met`。

不要把个人路径、token、会话里的临时对照基准写进仓库里的示例文件。

## 通知规则

对每个（条件, 资产）：

- **要通知**：`none → near`、`none → met`、`near → met`，以及任何从 `met` 回落（`met → near` / `met → none`）
- **不通知**：状态没变；`near → none`（降级但不是从「满足」回落）

脚本把该通知的变化放在 `notify` 数组。例行任务应：**`notify` 为空且没有新的「可能已基本出清」标志时保持沉默**；有条目再组织简短中文汇报（先写结论，再用表格列出四个条件、现价、简要推断）。

## 如何解读（给回复用）

- **多头 OI 永远等于空头 OI。** 不存在「多头占持仓量的比例」。看账户比和大户仓位比。
- **大户仓位比 ≤ 1、同时持仓量在升**：新的多头更可能来自散户。
- **底部常见组合（上下文，不是自动条件）**：账户比降到 2 附近或以下；持仓量从高点掉 10–20% 或更多；资金费率仍为负，但价格不再创新低。
- **先破前低再探底** 在历史上很常见。不要因为一次反弹就宣布出清结束。
- 接口失败、分页不够、451 回退，都要写出来。

结尾必须带：

```
以上只是信息整理，不构成投资建议
```

## 脚本

依赖：`pip install -r requirements.txt`（只需 `requests`）。用系统 `python3` 即可。

```bash
# 主入口：拉数、打分、更新状态、打印 JSON
python3 scripts/watch.py --state ./state.json --tz Asia/Bangkok

# 固定出清窗口（例如从某天 00:00 起算持仓高点，跨日也不重置）
python3 scripts/watch.py --state ./state.json --window-start 2026-11-13 --keep-window

# 只打印、不写状态
python3 scripts/watch.py --no-write-state

# 可选：OKX 已成交强平按小时汇总
python3 scripts/okx_liquidations.py --start 2026-11-13 --tz Asia/Bangkok

# 可选：每日 BTC 杠杆快照和图（需要 matplotlib / numpy）
python3 scripts/daily_leverage.py --data-dir ./data/leverage
```

环境变量：`DELEVERAGE_STATE`、`DELEVERAGE_TZ`、`LEVERAGE_DATA_DIR`。不要在脚本里写死机器路径。

## 定时任务示例

每 30 分钟跑一次，建议允许前后几分钟的弹性；按需 24/7，直到手动取消。

```cron
*/30 * * * * cd /path/to/crypto-deleverage-watch && python3 scripts/watch.py --state ./state.json --tz Asia/Bangkok >> ./watch.log 2>&1
```

智能体侧逻辑：

1. 跑 `scripts/watch.py`。
2. 读 JSON：`notify`、`status`、`possibly_mostly_flushed`、`prices`、`errors`。
3. 仅当 `notify` 非空，或「可能已基本出清」标志新出现时，发一条中文简报。
4. 先写哪一项升到/降到什么状态，再补表格和一句推断（例如「小轧空已经退潮，账户比仍在 3 以上，持仓量几乎没降，清理还没结束」）。
5. 标注时间（Asia/Bangkok, UTC+7）和数据来源。以免责声明结尾。

## 相关但不属于本技能核心的内容

- `scripts/daily_leverage.py`：每日 BTC 杠杆快照（价格、市值、OKX/Hyperliquid 持仓与资金费、CoinGlass 页面汇总等）并出图。用于日更，不是 30 分钟出清打分。
- ZEC/HYPE 与 BTC 的滚动相关不是出清监控，本仓库不收录。
