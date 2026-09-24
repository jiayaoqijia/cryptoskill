---
name: cex-daily-secondary-orchestrator
description: 生成单日中文二级市场日报的 Markdown、图表、数据底稿与 manifest，或按 market、derivatives、yields、rwa、sentiment 单独刷新和诊断模块；发布到 GitBook 由 gitbook-publisher 负责。
---

# 二级市场日报总控

一条命令生成单日二级市场日报（非月报）。本 skill 只负责本地产物；远端发布交给 `gitbook-publisher`。

## 职责边界

1. `cex-daily-secondary-orchestrator`：采集、计算、写作、图表和 `daily_manifest.json`。
2. `gitbook-publisher`：把已生成日报整理进 `gitbook/` 并触发 GitBook 导入。
3. `notion_import_md_with_images.py`：仅在用户明确要求 Notion 时使用，不是默认发布链路。

若请求还包括 RWA Night Desk 网站、站内归档、Sites 发布或订阅通知，日报验证后必须交给 `$rwa-report-site-orchestrator` 继续执行；本地日报生成不能作为整个任务的终点。

日期契约：调用方必须按运行时 Asia/Shanghai 日期显式传入 `--date YYYY-MM-DD`，生成、发布和验证始终使用同一个日期。禁止依赖隐式日期或复用旧目录。

## 快速开始

```bash
export COINGECKO_API_KEY="<your-key>"
export CMC_API_KEY="<your-key>"
export COINGECKO_API_TIER=demo

python3 ~/.claude/skills/cex-daily-secondary-orchestrator/scripts/run_cex_daily_orchestrator.py \
  --date 2026-03-01
```

说明：
- `--date` 为必填参数。
- 未传 `--outdir` 时，输出到 `./reports/YYYY-MM-DD/secondary_daily_cn`（每天一个新目录）。

## 模块化调用

完整日报由 `market`、`derivatives`、`yields`、`rwa`、`sentiment` 五个模块组成。需要只刷新或诊断一个模块时调用：

```bash
python3 ~/.claude/skills/cex-daily-secondary-orchestrator/scripts/run_daily_module.py \
  --module rwa \
  --date 2026-03-01 \
  --out /tmp/rwa-module.json
```

用 `run_daily_module.py --describe` 查看模块与真实数据源的机器可读映射。完整日报入口复用相同模块，并把状态写入 `daily_manifest.json -> coverage.modules`。具体路由见 [module-routing.md](references/module-routing.md)。

## 产出文件

- `daily_secondary_report.md`
- `daily_manifest.json`
- `charts/chart_market_snapshot_levels.png`
- `charts/chart_market_daily_change.png`
- `charts/chart_market_breadth_snapshot.png`
- `charts/chart_exchange_24h_change.png`
- `charts/chart_top10_assets_24h.png`
- `charts/chart_exchange_spot_deriv_structure.png`
- `charts/chart_sentiment_snapshot.png`
- `charts/chart_btc_eth_24h_trend.png`（新增：BTC/ETH 近24h（1h）归一化路径）
- `data/*.csv`
- `data/btc_eth_24h_trend.csv`（新增：BTC/ETH 24h 简单趋势判断底稿）
- `data/btc_eth_24h_1h_series.csv`（新增：BTC/ETH 1h 序列底稿）
- `data/stablecoin_yields_extended_defillama.csv`（新增：DefiLlama 扩展稳定币样本）
- `data/stablecoin_cefi_rates_bitcompare.csv`（兼容文件名：Bitcompare 稳定币平台 APY，混合 CeFi/DeFi/Hybrid）
- `data/rwa_asset_class_snapshot.csv`（新增：RWA.xyz 公开资产类别快照）
- `data/rwa_token_movers.csv`（tokenized stocks 异动、技术指标、链上流向、聪明钱信号与映射溢折价）
- `data/taoli_binance_margin_rates.csv`（新增：taoli 口径对齐的 Binance 借币年化）
- `notion_import/daily_secondary_report_import.md`（用于 Notion 导入的本地 md）
- `notion_import/charts/*.png`（导入 md 对应图片）
- `notion_import/README_IMPORT.md`（导入说明）
- `notion_import_bundle.zip`（md+charts 打包文件）

## 严格验证

生成后必须用同一个显式日期运行验证器：

```bash
python3 ~/.claude/skills/cex-daily-secondary-orchestrator/scripts/validate_daily_output.py \
  --dir ./reports/2026-03-01/secondary_daily_cn \
  --date 2026-03-01
```

验证器会检查 manifest 与报告标题日期、精确上海采集时间、关键文件、Markdown 图片真实存在、完整来源登记、至少一条可用 RWA 异动和至少一个可解析 RWA 类别。它还会阻断缺少核心市场数据时的方向性结论、稳定币或质押映射被计入风险广度、RWA 来源未披露日期却冒充当日、份额倍率缺失仍计算溢价、单位未验证的链上流量写成美元、稳定币 Total APY 与 Supply+Rewards 不一致、BTC/ETH 窗口未区分、量纲混合雷达图及误导性套利利差。`coverage_status` 为 `complete`、`partial` 或 `degraded`；`data_gaps` 与 `source_warnings` 必须结构化，原始错误不得泄漏到正文。

## GitBook 发布（默认）

本地生成成功后，用同一个显式日期调用：

```bash
python3 ~/.claude/skills/gitbook-publisher/scripts/publish_daily_report_to_gitbook.py \
  --repo-root . \
  --date 2026-03-01 \
  --json
```

`status=imported` 只表示导入已触发。完成前还必须确认产物已到 `origin/main`，并按报告标题或正文特征验证公开的当日详情页；详情页日期不符或仍为 fallback/404 均视为失败。

## Notion 导入（可选）

生成器仍会保留 `notion_import` 包以兼容旧流程，但只有用户明确指定 Notion 时才使用，不得在 GitBook 凭据缺失或发布失败时自动回退。

## Notion API 直传流程（可选）

当需要把图片直接托管到 Notion（非外链）时，可用 API 直传脚本：

```bash
export NOTION_API_TOKEN="secret_xxx"

python3 ~/.claude/skills/cex-daily-secondary-orchestrator/scripts/notion_import_md_with_images.py \
  --md ./reports/2026-03-02/secondary_daily_cn/notion_import/daily_secondary_report_import.md \
  --page-id "<notion-page-id>"
```

可选模式（新建子页面）：

```bash
python3 ~/.claude/skills/cex-daily-secondary-orchestrator/scripts/notion_import_md_with_images.py \
  --md ./reports/2026-03-02/secondary_daily_cn/notion_import/daily_secondary_report_import.md \
  --parent-page-id "<notion-parent-page-id>" \
  --title "二级市场日报（2026-03-02）"
```

说明：
- `--page-id` 模式默认会清空该页面现有内容后重写（可加 `--no-clear-existing` 改为追加）。
- 图片通过 Notion `file_upload` 流程上传，最终为 Notion 内部托管文件。

## 日报风格

- 参考 KuCoin 等前排交易所的日报节奏：
  - 当日脉冲
  - 交易所资金流
  - 衍生品风险
  - 情绪读数
  - 未来 24h 观察点
- 结论前置，短段落，避免冗余图号叙述。
- 输出包含 4 层写作结构：`状态判断 -> 驱动解读 -> 图表证据 -> 交易含义`，避免只做数字复述。
- 每张图默认给出 3 句以上：`数据现象` + `机制解释` + `对下一交易日的含义`。
- 正文新增 `BTC/ETH 24h 趋势判断` 小节，口径保持简洁（价格、24h 涨跌、日内区间位置、一句话结论）。
- 正文默认不展示“数据来源”或采集错误；来源映射、未填补缺口和可恢复告警分别保留在 manifest 的 `source_registry`、`data_gaps`、`source_warnings` 中用于复核。

## 图表风格规范（默认）

- 默认采用“简约混合图”，避免整份报告全是柱状图。
- 同一页内尽量控制 2 张以上同类图，优先使用更直观的结构图与定位图。
- 所有图表保持统一主题：同一配色、网格、字体、标注逻辑。
- 具体映射与降级规则见 `references/chart-style.md`。

## 指标路由

1. 市场脉冲（总市值/24h 成交/BTC.D）：CMC Global 历史日频。
2. 头部风险资产 24h 参与度：CoinGecko `/coins/markets`，缺 key 或请求失败时回退 CoinPaprika `/v1/tickers`；稳定币、质押及信用映射只保留在市值集中度图，不计入风险涨跌家数。
3. 交易所流量：CMC `exchange/quotes/latest`（前排交易所样本）。
4. 衍生品：Deribit ticker（funding/OI）+ Deribit DVOL 日内收盘；ticker 失败时用 OKX 公共 Funding/OI，DVOL 不做非等价替代。
5. 情绪：Alternative.me F&G，失败时回退 CoinMarketCap F&G；允许使用最近 2 日内最新值并显式记录实际日期。
6. BTC/ETH 24h 趋势：Binance Global `ticker/24hr` + `klines` 1h；地区限制或网络失败时回退 Binance.US 公共接口。
7. 稳定币跨源对比（默认启用）：
   - 链上主表：DefiLlama + Aave/Compound/Morpho 官方接口。
   - 扩展样本：DefiLlama 全量稳定币池（筛选口径：`TVL>=30M`、`0.2%<=APY<=20%`、去除与主表高度重叠协议），正文展示 Top20。
   - 平台 APY 对比：Bitcompare 的 CeFi/DeFi/Hybrid 稳定币 APY vs taoli 口径 Binance 借币年化；因期限、容量和风险口径不同，不直接计算套利利差。
8. RWA 结构观察：RWA.xyz 公开资产类别页（U.S. Treasuries、Credit、Tokenized Stocks、Non-U.S. Government Debt、Active Strategies、Real Estate），用于观察 RWA 是否从持有型收益资产转向可交易资产映射。
9. RWA tokenized stocks 异动雷达（默认启用）：
   - 默认观察池：AAPL、AMZN、AMD、AVGO、COIN、CRCL、GOOGL、HOOD、IBIT、MARA、META、MSFT、MSTR、NFLX、NVDA、PLTR、QQQ、RIOT、SPY、TSLA。
   - 可用 `RWA_EQUITY_TICKERS=AAPL,NVDA,...` 覆盖观察池；不扫描全部低活跃映射资产。
   - 第一阶段按 24h 绝对涨跌筛出前 5；第二阶段仅对异动标的拉取 48 根 1h K 线和链上流向。
   - 技术面：RSI14、SMA6/SMA24、24h 振幅。
   - 链上面：只有来源字段能通过买卖分项一致性与相对市值尺度检查时，才标记为美元成交额/净买入；否则只保留 raw 值与异常状态。
   - 聪明钱覆盖：Binance Web3 公共 Smart Money Signal 为主源，不需要 Agentic Wallet 登录。逐标的区分 `active_signal`、`no_matching_signal`、`source_unavailable` 与 `unsupported_chain`；未命中不得写成零地址。
   - Agentic Wallet 仅用于 自有钱包监控和交易执行，不作为公共市场聪明钱数据源，也不把自有钱包行为包装成聚合信号。
   - OKX 交易员榜单与新闻情绪默认关闭，仅在显式设置 `OKX_SMARTMONEY_ENABLED=1` / `OKX_NEWS_SENTIMENT_ENABLED=1` 时作为可选增强；失败不影响 Binance Web3 主覆盖。
   - 映射面：用 `token price / sharesMultiplier` 与底层美股价格计算溢折价，不能直接假设 1 token = 1 share。
   - 事件面：优先使用资产状态中的 earnings、dividend、split、merger、pause 等可验证事件；无明确事件源时只写“相关性/待验证假设”，不伪造因果。
   - 24×7 解释：美股休市时把 tokenized stock 视为提前定价与价格发现代理，同时提示底层套利锚缺失、链上流动性变薄及开盘回归风险。

环境变量要求：
- `COINGECKO_API_KEY`：从环境变量读取；不可用时回退 CoinPaprika，只有 fallback 也失败才写入 `data_gaps`。
- `CMC_API_KEY`：从环境变量读取；不可用时将相关缺口写入 `data_gaps`。
- `COINGECKO_API_TIER`：可选，`demo`（默认）、`pro` 或 `auto`（先 `pro` 后 `demo`）。
- `CEX_HTTP_TRANSPORT`：可选，`auto`（默认）、`curl` 或 `urllib`；代理环境下 `auto` 优先使用 curl。
- `BYBIT_MIHOMO_MODE`：可选，`auto`（默认）、`off` 或 `required`。`auto` 在本机 Mihomo Party 可用时临时切换 Bybit 请求，失败则保留原网络路径并登记告警；`required` 在无法切换时直接把 Bybit 标记失败。
- `BYBIT_MIHOMO_PROXY`：Bybit 请求使用的 Mihomo 节点，默认 `JP-Dedicated-B1-1`。
- `BYBIT_MIHOMO_SELECTOR`：临时切换的选择器，默认 `GLOBAL`。调用完成或抛错时必须恢复原选择。
- `BYBIT_MIHOMO_SOCKET`：可选的 Mihomo Unix 控制 socket；未设置时自动发现 `/tmp/mihomo-party-*.sock`。
- `BINANCE_MIHOMO_MODE`、`BINANCE_MIHOMO_PROXY`、`BINANCE_MIHOMO_SELECTOR`、`BINANCE_MIHOMO_SOCKET`：与 Bybit 配置同义；默认对 `*.binance.com` 的现货、合约、借币、RWA 和 Web3 公共请求临时使用 `JP-Dedicated-B1-1`。`api.binance.us` 不参与该路由。
- 默认行为：若 CoinGecko key 无效，Top10 资产章节使用 CoinPaprika；BTC/ETH 行情在 Binance Global 不可用时使用 Binance.US。
- `RWA_API_KEY`：当前日报 RWA 面板默认使用 RWA.xyz 公开页，不强依赖 key；如后续切换到官方 API，可按 RWA.xyz 文档设置该变量。

## 失败策略

- 单一数据源失败不应导致整份日报失败。
- Bybit 只在单次接口调用期间临时选择配置的日本节点，并通过进程锁避免并发切换；不得把日本节点长期留在全局选择器中。
- Binance Global 也只在单次 HTTP 调用期间使用配置的日本节点；Binance.US fallback 保持原路由。每次调用结束都必须恢复原选择器。
- 无法由等价 fallback 或其他有效样本补齐的指标写入 `data_gaps`；已恢复的来源故障写入 `source_warnings`，并继续输出可用部分。
- 若 Bitcompare 不可用，保留链上稳定币主表与扩展样本。
- 若 taoli 对齐数据不可用，平台 APY 表内对应列显示 `N/A`，但不阻断日报生成。

## 参考

- [daily-benchmark-frame.md](references/daily-benchmark-frame.md)
- [metric-routing.md](references/metric-routing.md)
- [module-routing.md](references/module-routing.md)
- [chart-style.md](references/chart-style.md)
- [coinmetrics reference](https://coinmetrics.substack.com/p/state-of-the-network-issue-348)
