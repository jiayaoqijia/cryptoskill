# 证据与数据口径

每条证据有 evidence_id、kind、URL、observed_at（来源或采样观测时间）、retrieved_at（取得时间）、状态、raw_path、数据和哈希。来源未给数据时点则observed_at为null；接口返回当下快照可注明采样时间，但不能宣称来源内部更新延迟已知。帖子发布时间不是采集时间。

结论级证据（0.1.3）：报告摘要中的每条实质结论在判断JSON的claims[]里登记，逐来源记录source_url、observed_at（数据本身时间；未知则null并写observed_at_unknown_reason）、fetched_at（抓取时间，与证据包retrieved_at一致）、raw_path（存在的原始文件）。判断另记data_cutoff（所用数据最晚取得时间）与analysis_completed_at（判断完成时间），二者不能合并成一个as_of。旧材料缺失的时间写legacy/unknown，不补造。

采集状态 ok/error/unavailable 与数值null/0分开。旧缓存保留原取得时间；动态数据默认不缓存复用（cache_ttl=0），静态资料可指定不超过86400秒。公开源免费不代表稳定；失败记缺口，不用摘要补造精确数字。

事实来源按问题选：官方/链浏览器确认资产，项目文档及实际产品确认功能，治理/链上执行核验机制，市场原始接口核验行情，原帖核验言论。模型识别同源转载、宣传、利益关系和反证；单一来源明确归属。每条报告结论引用证据ID/URL、数据时间；推断注明依据与不确定性。

## 不用训练记忆当事实（0.1.6）

事实陈述只能引用本次运行抓取、带 fetched_at（请求时刻，UTC 秒）的证据。模型记忆只能用于假设和搜索词。以前运行的证据未重新抓取时：claim 来源写 `freshness: "stale"`，保留原 evidence_ref 与原 fetched_at，不与本次证据包比对；只有 stale 来源的 claim 不能标 fact。没有任何来源的内容用 label `unverified`（未验证）并写 unverified_reason。`record` 对 0.1.6 新判断执行这些规则；本次证据包里被引用但缺 fetched_at/retrieved_at 的记录写入 validation_warnings。已登记的旧记录不重验、不改。快速核查同样适用，见 [factcheck.md](factcheck.md)。

## 已实现适配

| kind | 用途/限制 |
|---|---|
| web | HTTPS原文，提取文字并保留完整响应；JS/PDF不可读时由宿主浏览器/文档工具补证 |
| dex-search / dex-pairs / dex-orders | 搜索候选、按链+合约取池、推广购买记录；不是完整持有人/OHLC/安全扫描 |
| llama-protocol / llama-stablecoins | 协议与链资金环境，保留来源指标定义 |
| binance-ticker / binance-depth / binance-klines | 已核对symbol的只读行情、深度、K线；交易所覆盖不等于全部市场 |
| binance-funding / binance-oi | 可访问时的只读衍生品数据；受地区和接口限制 |
| rpc | 下列明确只读方法；接口和查询由模型选择，节点可能限流/缺历史 |
| coingecko | 可选COINGECKO_DEMO_API_KEY，未配置标记unavailable |
| brave-search | 可选既有BRAVE_SEARCH_API_KEY；未配置使用宿主搜索导入，不要求购买 |
| native导入 | 宿主X/网页/专业工具真实结果，保留工具名、URL、原始内容和时间 |

RPC允许 eth_blockNumber/eth_getBlockByNumber/eth_getBalance/eth_getCode/eth_call/eth_getLogs、getTokenSupply/getTokenLargestAccounts/getAccountInfo/getSignaturesForAddress/getTransaction/getSlot。不包含交易发送或签名。eth_call也不等于真实交易一定可成功。EVM余额原始单位/decimals及Solana账户与最终持有人差别需模型明确。

## 信号与评估报价

BUY/SELL记录需要报告前15分钟以内的报价；底层数据时效无法确认时披露，必要时WATCH/UNDETERMINED。报价需包含资产、USD价格、观测时间、venue、instrument、evidence_refs。USDT等报价转换为USD时给转换证据。脚本校验引用存在，但数值是否与来源相符仍需模型核对。

选择常用、可持续取得历史数据的主要交易场所；建立基线时冻结venue/instrument/计价/数据口径。脚本拒绝用另一场所或instrument计算原判断的正式命中率。如原场所永久无数据，保留新来源的辅助观察，但原评估标不可评估并说明差异。不要把污染/僵尸池价格当真实结果。

## 公开原始文档

- https://docs.dexscreener.com/api/reference
- https://defillama.com/data-definitions
- https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints
- https://docs.coingecko.com/
- https://solana.com/docs/rpc/http
- https://ethereum.org/en/developers/docs/apis/json-rpc/

这些链接供核对接口；实现覆盖以脚本及doctor的实测为准。凭据只从已授权环境变量读取，脚本不回显、不存响应请求头、不读取浏览器cookies。
