# 指标路由（日报）

## 必选指标

- 全市场总市值/24h 成交/BTC.D：CMC `global-metrics/quotes/historical`（日度变化）
- Top10 资产 24h 涨跌：CoinGecko `/coins/markets`（Key Auth）-> CoinPaprika `/v1/tickers`（免 Key）
- 前排交易所 24h 变化与现货/衍生品结构：CMC `exchange/quotes/latest`
- 永续 Funding + OI 快照：Deribit `public/ticker`（POST -> GET）-> OKX Funding/OI 公共接口
- DVOL 当日收盘：Deribit `public/get_volatility_index_data`（小时级）
- 情绪读数：Alternative.me `/fng/` -> CoinMarketCap Fear & Greed 公共图表接口
- BTC/ETH 24h 与 1h K 线：Binance Global -> Binance.US 公共市场接口
- 稳定币收益主表：DefiLlama `/pools` + Aave/Compound/Morpho 官方接口
- 稳定币扩展样本：DefiLlama `/pools`（`TVL>=30M`、`0.2%<=APY<=20%`、去除重叠协议）
- 稳定币平台 APY（CeFi/DeFi/Hybrid）：Bitcompare `/lending-rates?page=N`
- taoli 对齐借币年化：Binance margin 借币利率（用于 Bitcompare 横向利差）

## API Key 配置

```bash
export COINGECKO_API_KEY="<your-key>"
export CMC_API_KEY="<your-key>"
export COINGECKO_API_TIER=demo
```

- `demo`：直接按 Demo Key 路径请求（推荐）。
- `auto`：先尝试 `pro` 头，再尝试 `demo` 头（都带 key）。
- 未配置 key：相关付费源不使用内置凭据；有等价公共源时使用 fallback，否则写入 `data_gaps`。

代理环境下默认优先使用 `curl`，避免 Python TLS 在部分代理链路中出现 EOF/handshake timeout。可用 `CEX_HTTP_TRANSPORT=auto|curl|urllib` 显式覆盖。

## 降级策略

- CoinGecko 缺 key 或请求失败：用 CoinPaprika Top10；只有两者均失败才标注“头部资产数据缺失”。稳定币、质押及信用映射不得计入方向性风险广度。
- Deribit ticker 失败：先改用同源 GET，再用 OKX 公共 Funding/OI；DVOL 不使用非等价波动率代理。
- Alternative.me 失败：使用 CoinMarketCap F&G；当日尚未发布时允许最近 2 日内最新值，并保留真实 `as_of` 和 `lag_days`。
- Binance Global 因地区限制或网络失败：BTC/ETH 行情与 K 线使用 Binance.US；不把 Binance.US 数据标成 Global。
- Bitcompare 失败：平台 APY 对比表降级为链上扩展样本。
- Binance 借币年化失败：平台 APY 对比表保留 Bitcompare 列，taoli 列置空。

`daily_manifest.json` 中，无法填补的指标进入 `data_gaps`；主源失败但备用源或其他可用样本已覆盖的诊断进入 `source_warnings`，不在日报正文展示。来源页没有 `as_of` 时必须写 `null + source_date_unavailable`，不可使用抓取日代替来源日期；单位未验证的链上数值只保留 raw 字段。

## RWA 聪明钱路由

- 主源：Binance Web3 公共 Smart Money Signal（BSC / Solana），不依赖 Agentic Wallet 登录。
- `active_signal`：公开信号页命中该合约，可展示方向、地址数和信号金额。
- `no_matching_signal`：接口成功但当前页未命中该合约；数值保持空，不得解释为零。
- `source_unavailable`：接口失败，精确错误只写入 manifest `data_gaps`。
- `unsupported_chain`：该链不在 Binance Web3 信号支持范围。
- OKX 榜单/仓位是显式可选增强，不参与 RWA 主覆盖通过条件。

## 前排交易所样本

- binance
- coinbase-exchange
- upbit
- okx
- bybit
- bitget
- gate
- kucoin
- mexc
- htx
