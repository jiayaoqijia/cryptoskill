---
name: news-sentiment
description: |
  加密新闻抓取 + 关键词情绪统计（零 Key）：中文快讯（PANews）+ 英文头条
  （CoinDesk / Cointelegraph RSS）。命令：latest 拉最新新闻、coin 按币过滤、
  sentiment 看多/看空比例统计。用户提到「新闻、情绪、舆论、news、sentiment、
  市场在讨论什么」时使用；分析代币时可与 market-data 组合补上消息面。
  触发词：新闻、快讯、情绪、舆论、利好利空、news、sentiment。
metadata:
  author: bazz-agent
  version: "1.0"
---

# News & Sentiment（新闻与情绪面）

零依赖抓取公开新闻源（无需任何 API Key）：

- **中文快讯**：PANews flash（`api.panewslab.com`）
- **英文头条**：CoinDesk RSS、Cointelegraph RSS

情绪为**关键词启发式**（涨/突破/利好/买入/增持 vs 跌/暴跌/清算/爆仓/诉讼 等，
中英双语词表），只做粗粒度参考 —— **不是投资建议，也非精确 NLP**。
网络：直连失败时自动读 `HTTPS_PROXY/HTTP_PROXY` 环境变量（代理池启用后
agent 子进程经 proxy-preload 自动走池）。

## 命令

| 命令 | 说明 |
|---|---|
| `latest [n=20]` | 三源混合最新新闻（标题 / 来源 / 时间 / 链接） |
| `coin <SYM> [n=15]` | 只看与某币相关的标题（支持 BTC/SOL/WLD 等，含常见项目名匹配） |
| `sentiment [n=40]` | 情绪统计：看多 / 看空 / 中性占比 + 最多空代表标题 + 高频币种 |

## Agent 使用约定

1. `sentiment` 结果只作消息面参考，与 K 线/资金费率等硬数据冲突时以后者为准；
2. 引用新闻标题时注明来源与时间，不要虚构不在返回列表里的头条；
3. 某源失败是常态（网络/限流），返回里会标注 `failed_sources`，别当致命错误。
