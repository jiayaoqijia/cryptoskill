---
name: aicoin-trading
description: "**CEX 中心化交易所**(Binance / OKX / Bybit / Bitget 等)的下单交易工具。严格规则:(1) 所有订单必须通过 node scripts/exchange.mjs create_order 执行,禁止写自定义代码下单 (2) create_order 分两步:第一次返回预览,展示给用户等确认,用户说确认后第二次加 confirmed=true 执行 (3) 禁止自动确认,禁止跳过预览 (4) 平仓必须用 close_position,禁止用 create_order 构建平仓单。Trigger 关键词: 'buy on okx', 'sell on binance', '在 OKX 买 BTC', '在 Binance 下单', '做多 BTC 永续', '杠杆做空 ETH', '平掉我的 SOL 仓位', 'CEX 下单', '现货买入', '合约开仓', '永续平仓', '止盈止损', 'long', 'short', 'leverage', '买', '卖', '下单', '做多', '做空', '开仓', '平仓', '平掉', '关仓'. **路由提示**: 用户说“链上 swap / Uniswap / DEX 买 PEPE / Solana 上买”是**链上 DEX 交易**,应走 `aicoin-onchain` 而不是本 skill. Hyperliquid 上的下单也走 aicoin-onchain(HL 是链上 perp DEX),不是这里. 本 skill **只**处理 CEX 现货 + 永续合约下单。"
metadata: { "openclaw": { "primaryEnv": "AICOIN_ACCESS_KEY_ID", "requires": { "bins": ["node"] }, "homepage": "https://www.aicoin.com/opendata", "source": "https://github.com/aicoincom/coinos-skills", "license": "MIT" } }
required_environment_variables:
  - name: OKX_API_KEY
    optional: true
    prompt: "OKX 交易所 API key(在 OKX 下单才需要)"
    help: "其他交易所同理:BINANCE_API_KEY / BYBIT_API_KEY / BITGET_API_KEY 等,均配套 _API_SECRET"
  - name: OKX_API_SECRET
    optional: true
    prompt: "OKX 交易所 API secret"
  - name: OKX_PASSWORD
    optional: true
    prompt: "OKX API passphrase(OKX/Bitget 等需要)"
  - name: BINANCE_API_KEY
    optional: true
    prompt: "Binance API key(在 Binance 下单才需要)"
  - name: BINANCE_API_SECRET
    optional: true
    prompt: "Binance API secret"
---

> **运行脚本**: 从 SKILL.md 所在目录运行 `node scripts/exchange.mjs <action>`. 三引擎(OpenClaw / Hermes / Claude Code)容器自动加载 skill, 直接 `cd` 到 skill 目录即可.

# AiCoin Trading — 下单专用

## ⛔ 铁律（违反任何一条都是严重错误）

1. **禁止写代码下单。** 不准写 `import ccxt`、`new ccxt.okx()`、`fetch("https://...")` 或任何自定义代码来下单。所有订单只能通过 `node scripts/exchange.mjs create_order` 执行。
2. **禁止自动确认。** `create_order` / `close_position` 第一次调用返回预览（含风险提示），你必须把预览完整展示给用户，等用户回复"确认"或"yes"后，才能第二次调用加 `"confirmed":"true"` 执行。
3. **禁止修改用户参数。** 余额不够就告诉用户，不准自动调整数量或杠杆。
4. **禁止主动平仓。** 除非用户明确要求。
5. **平仓必须用 `close_position`。** 禁止用 `create_order` 构建平仓单（容易开反向单）。
6. **杠杆 / 保证金模式改动必须先确认。** `set_trading_params` 和 `set_leverage` 不是只读操作 — 它们改交易所账户的合约配置，直接影响后续所有订单的保证金占用、爆仓价、强平距离。100x 杠杆和 5x 杠杆的爆仓距离差 20 倍，用户没明确说改之前不准 silent set。**调用前必须**：用自然语言告诉用户你准备把哪个交易所、哪个交易对的杠杆 / margin_mode 从什么改成什么、影响是什么，等用户回复"确认"或"yes"才能执行。

> **反例 ❌**：用户说"开 100x 多 BTC"，你不反问杠杆是不是写错了直接 `set_trading_params leverage=100` 然后下单 — 用户可能是口误想说 10x，100x 直接 silent 设了风险极高。
> **正确 ✅**：先回"100x 杠杆爆仓距离只有约 0.95%（不算手续费），BTC 一根 5 分钟 K 线就能扫掉。确认是 100x 还是想说 10x？"，等用户明确回答再 set。

## 下单流程（两步，不可跳过）

```
步骤1: node scripts/exchange.mjs create_order '{"exchange":"okx","symbol":"BTC/USDT:USDT","type":"market","side":"buy","amount":1,"market_type":"swap"}'
→ 返回预览（交易对、方向、数量、价格、杠杆、保证金、风险提示）
→ 你必须把所有字段展示给用户

步骤2: 用户确认后
node scripts/exchange.mjs create_order '{"exchange":"okx","symbol":"BTC/USDT:USDT","type":"market","side":"buy","amount":1,"market_type":"swap","confirmed":"true"}'
→ 实际下单
```

## 平仓流程（两步，不可跳过）

**平仓必须用 `close_position`，禁止用 `create_order` 手动构建平仓单（容易开反向单）。**

```
步骤1: node scripts/exchange.mjs close_position '{"exchange":"okx","market_type":"swap"}'
→ 返回所有持仓预览（交易对、方向、张数、盈亏）
→ 展示给用户

步骤2: 用户确认后
node scripts/exchange.mjs close_position '{"exchange":"okx","market_type":"swap","confirmed":"true"}'
→ 市价平掉所有持仓（自动 reduceOnly）

步骤3: 执行后必须验证 + 总结（不可省略）
node scripts/exchange.mjs positions '{"exchange":"okx","market_type":"swap"}'
→ 确认仓位已清空，然后用一句话告诉用户结果（平了什么、盈亏多少）
```
指定交易对只平部分：加 `"symbol":"BTC/USDT:USDT"`

> **为什么有步骤3**: close_position 的返回有时被 streaming 截断，用户看不到结果。多查一次 positions 既能确认平仓成功，又能把结论写进最终消息让用户看到。

## 止盈止损 / 条件单流程（两步，不可跳过）

**给已有仓位挂止损 / 止盈，必须用 `set_stop`，禁止手搓 `create_order` 的 `STOP_MARKET`+原始 params。**`set_stop` 会从交易所**真实持仓**自动推导方向、`reduceOnly` / `posSide` / `positionSide`（币安双向持仓、OKX、Bybit 各自适配），并校验触发价在现价正确一侧——手搓极易开成反向单或方向搞反。

```
步骤1: node scripts/exchange.mjs set_stop '{"exchange":"binance","symbol":"HYPE/USDT:USDT","market_type":"swap","stop_loss":63.5,"take_profit":66.5}'
→ 返回预览（持仓方向、触发价、触发后动作、平仓模式、方向校验结果）
→ 你必须把预览展示给用户

步骤2: 用户确认后
node scripts/exchange.mjs set_stop '{"exchange":"binance","symbol":"HYPE/USDT:USDT","market_type":"swap","stop_loss":63.5,"take_profit":66.5,"confirmed":"true"}'
→ 实际挂条件单

步骤3: 执行后复核（不可省略）
node scripts/exchange.mjs stop_orders '{"exchange":"binance","symbol":"HYPE/USDT:USDT","market_type":"swap"}'
→ 确认条件单已挂上，再把结论告诉用户
```

- 参数：`stop_loss`（止损触发价）/ `take_profit`（止盈触发价）至少给一个，可同时给；只给单一 `trigger_price` 会按方向自动归类为止损或止盈。`amount` 可选，默认全仓，超过持仓自动 clamp。`side`（`long`/`short`）：当同一交易对**同时持有多空两个仓**（双向持仓）时必须指定，否则 `set_stop` 会报错让你选边，绝不替你猜。
- **多单**：止损 < 现价、止盈 > 现价；**空单**反之。设反会被 `set_stop` 拦下报错（防瞬间触发）。拿不到当前价时默认中止（无法校验方向），确需跳过校验可传 `"force":true` 自负风险。
- **双向持仓（hedge mode）全自动适配**：开仓自动补方向参数（币安 `positionSide`、OKX `posSide`、Bybit `positionIdx`），止损/止盈/平仓从真实持仓推导方向 —— 币安/OKX/Bybit/Bitget/HTX 双向账户都无需手动指定。其中 Bitget/HTX 平仓由 ccxt 翻成 `tradeSide:Close`/`offset:close`（纯 `reduceOnly` 在它们的双向模式会被当反向开仓，已专门处理）；Bitget 持仓模式万一识别不出会**中止并报错**而非冒险反向开仓。`set_stop` 挂的止损/止盈是交易所条件/算法单（`stop_orders` 可查），平仓后用 `cancel_order` 可一并清掉残留条件单。
- 确认执行前 `set_stop` 会**再读一次持仓**把数量校准到当前仓位；若确认期间仓位已被平掉/反手，会直接报告“持仓已不存在”而不挂废单。
- **为什么有步骤3**：条件单在部分交易所（OKX 等）属算法/委托单，**不出现在普通 `open_orders` 列表**，只能用 `stop_orders` 或交易所 APP 的「条件委托」栏查到。别用 `open_orders` 误判“没挂上”。
- **兜底**：ccxt 跨所条件单细节有差异（币安触发用标记价/最新价、OKX algo 单等），若 `set_stop` 某条返回失败，如实告诉用户失败原因，并建议去交易所 APP 手动挂——不要谎报已挂上。
- **条件单支持矩阵（ccxt 4.5.47 实测）**：止损/止盈/触发单 在 **Binance / OKX / Bybit / Bitget / Gate / HTX 6 家 CEX 全部支持**（各映射到该所 native 条件单）。下单前有**安全网**：若触发价被某所静默丢弃（会变成立即成交的市价单），`placeOrder` 会直接拒绝而非误下单。每次升级 ccxt 后跑 `npm run verify-orders`（请求体黄金矩阵）确认没漂移。Hyperliquid 走 trigger、属边角（USDC，多路由到 aicoin-onchain），以实盘为准。

## 下单前准备

| 步骤 | 命令 | 是否需要确认 |
|------|------|------------|
| 设置杠杆+保证金模式 | `node scripts/exchange.mjs set_trading_params '{"exchange":"okx","symbol":"BTC/USDT:USDT","leverage":10,"margin_mode":"isolated","market_type":"swap"}'` | **需要**（见铁律 #6） |
| 单独设杠杆 | `node scripts/exchange.mjs set_leverage '{"exchange":"okx","symbol":"BTC/USDT:USDT","leverage":10,"market_type":"swap"}'` | **需要**（见铁律 #6） |
| 查合约信息 | `node scripts/exchange.mjs markets '{"exchange":"okx","market_type":"swap","base":"BTC"}'` | 不需要（只读） |

**杠杆 / 保证金确认模板**（直接照抄换数字）：
> "我准备把 OKX BTC/USDT 永续杠杆改为 **{N}x**，margin_mode = **{isolated/cross}**。这会影响后续这个交易对所有订单的保证金占用和爆仓距离（{N}x 杠杆爆仓约 {1/N*100}% 不计手续费）。确认改吗？"

确认后再实际调 `set_trading_params` / `set_leverage`。如果用户说"算了"、"先别"、"我再想想"，**不要**调脚本。

## 其他命令

| 操作 | 命令 |
|------|------|
| 平仓（全部或指定） | `node scripts/exchange.mjs close_position '{"exchange":"okx","market_type":"swap"}'` — 加 `"symbol":"BTC/USDT:USDT"` 只平单个 |
| 止盈止损（给已有仓位挂保护单） | `node scripts/exchange.mjs set_stop '{"exchange":"binance","symbol":"HYPE/USDT:USDT","market_type":"swap","stop_loss":63.5,"take_profit":66.5}'` — 两步确认，见上方「止盈止损流程」 |
| 查条件单/算法委托 | `node scripts/exchange.mjs stop_orders '{"exchange":"binance","symbol":"HYPE/USDT:USDT","market_type":"swap"}'` — 普通 `open_orders` 查不到的条件单用这个 |
| 取消订单 | `node scripts/exchange.mjs cancel_order '{"exchange":"okx","symbol":"BTC/USDT","order_id":"xxx"}'` — 也能取消条件单 |
| 存交易所 key（本地，用户在 chat 给了 key 时） | `node scripts/exchange.mjs save_key '{"exchange":"binance","api_key":"...","api_secret":"..."}'` — 写进 `~/.coinos/.env`、`chmod 600`、不回显 secret（OKX/Bitget 还要 `"password":"..."`）。容器内引导用户去 web UI EnvSection，别在 chat 收 key |

## 数量

**合约自动换算：** `amount` 一律是用户说的**币数量**（如 0.01 BTC、1000 DOGE），脚本统一按 `amount / contractSize` 自动换算成张数 —— 整数也按币数量算（旧版"整数=张数"的约定在 OKX/Gate 等 contractSize≠1 的所会把张数算错几个数量级，已废除）。**确实要直接传张数**时加 `"amount_unit":"contracts"`。
**用 USDT 金额下单：** 当用户说"用10U做多"或"花10 USDT开仓"，传 `cost=10`（合约=USDT保证金金额，按价格+杠杆算张数；现货市价买入=花多少 USDT，按现价反算币数量），不要传 amount。
**现货：** `amount` = 币数量；或用 `cost` 按 USDT 金额买入。

**格式：** 现货 `BTC/USDT`，合约 `BTC/USDT:USDT`，Hyperliquid 用 USDC: `BTC/USDC:USDC`。

**交易所：** Binance, OKX, Bybit, Bitget, Gate.io, HTX, Pionex, Hyperliquid。
