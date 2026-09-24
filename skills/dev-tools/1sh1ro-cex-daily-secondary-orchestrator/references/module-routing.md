# 日报模块路由

所有模块必须显式传入同一个 Asia/Shanghai 日期，并输出统一 JSON：`module`、`target_date`、`status`、`data`、`data_gaps`、`source_warnings`、`sources`。

| 模块 | 单模块命令 | 主要数据源 | 主要输出 |
|---|---|---|---|
| `market` | `run_daily_module.py --module market` | CMC、CoinGecko/CoinPaprika、Binance/Binance.US | 全市场、Top10、市值集中度、交易所、BTC/ETH |
| `derivatives` | `run_daily_module.py --module derivatives` | Deribit、OKX、Binance Futures | Funding、OI、DVOL、非 DeFi carry |
| `yields` | `run_daily_module.py --module yields` | DefiLlama、Aave、Compound、Morpho、CEX 借币、Bitcompare | 稳定币收益和借币成本 |
| `rwa` | `run_daily_module.py --module rwa` | RWA.xyz 公开页、Binance Web3 | RWA 类别、tokenized stocks、聪明钱覆盖 |
| `sentiment` | `run_daily_module.py --module sentiment` | Alternative.me/CMC、可选 OKX CLI | F&G、可选交易员与新闻情绪 |

查看机器可读来源注册表：

```bash
python3 scripts/run_daily_module.py --describe
```

运行单模块：

```bash
python3 scripts/run_daily_module.py \
  --module rwa \
  --date 2026-07-26 \
  --out /tmp/rwa-module.json
```

单模块用于诊断、补数和定向研究；完整日报仍运行 `run_cex_daily_orchestrator.py`。总编排器调用相同模块实现，并把模块状态写入 `daily_manifest.json -> coverage.modules`。

`yields` 中的 Bybit 公共借币接口可通过 `BYBIT_MIHOMO_*` 环境变量在单次请求期间临时选择日本 Mihomo 节点；实现必须加锁并在 `finally` 中恢复原选择器。OKX 等其他非 Binance 来源不参与该临时切换。

所有 `*.binance.com` 公共请求通过 `BINANCE_MIHOMO_*` 使用同一临时路由机制，覆盖现货、合约、借币、RWA 与 Web3；`api.binance.us` fallback 不切换。Bybit 与 Binance 都默认使用 `JP-Dedicated-B1-1`，且不得把节点选择长期留在 `GLOBAL`。
