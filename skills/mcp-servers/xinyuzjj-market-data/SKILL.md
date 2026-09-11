---
name: market-data
description: |
  本地行情数据网关：K线收盘价（1d/1h/4h，最多 90+ 根）、资金费率、合约持仓量 OI、
  大户多空比、爆仓流、恐惧贪婪指数、市场综述。分析任何代币（WLD/RAY/PEPE 等）时
  必须优先用本技能取历史行情与衍生品数据 —— 走本机后端（自带 5 分钟缓存 + 代理池出口），
  不要直连币安 API（会被 15s 超时 / 输出截断卡住）。
  触发词：分析代币、研报、走势、K线、资金费率、持仓量、OI、多空比、爆仓、恐惧贪婪、
  klines、funding、open interest、fear greed。
metadata:
  author: bazz-agent
  version: "1.0"
---

# Market Data Skill（本地行情网关）

数据来自本机 BAZZ.AGENT 后端 `127.0.0.1`（端口 `BAZZ_PORT`，默认 8080）。
后端统一走代理池访问币安，K线/OI/恐惧贪婪均带 5 分钟缓存 —— 快且稳。

## 命令

| 命令 | 说明 |
|---|---|
| `klines <SYMBOL> [interval] [limit] [market]` | 收盘价数组（旧→新）+ 涨跌/区间统计。interval: 1h/4h/1d；market: spot/futures |
| `bundle <SYMBOL> [market=futures]` | **分析包**：90d 日K 统计 + 24h 统计 + 恐惧贪婪 + 资金费率 + OI + 大户多空比（spot 时自动省略衍生品项） |
| `fng` | 恐惧贪婪指数（当前值 + 8 天历史） |
| `oi <SYM[,SYM...]>` | 合约持仓量（币本位 OI × 最新价 = USD 名义） |
| `longshort [SYMBOL]` | 大户多空比 / 全球多空比 / 背离标记（全量时仅返回关键字段） |
| `liq [SYMBOL] [limit] [window]` | 近 5 分钟爆仓流（可按币筛选，含多空统计） |
| `overview` | 市场综述：涨跌宽度 / 资金费率拥挤与翻转 / 成交额 TOP |

## 用法示例

```
run_skill market-data "bundle WLDUSDT"
run_skill market-data "klines RAYUSDT 1d 90 spot"
run_skill market-data "liq BTCUSDT 100"
```

## 分析约定

1. **先 `bundle` 后下结论**：任何代币分析必须包含 90d 区间位置、收盘分位、资金费率、OI。
2. 区间位置 = (现价−90d最低)/(90d最高−90d最低)，<33% 低位 / >66% 高位。
3. 收盘分位 = 90 天里收在现价之下的天数占比（区分"低位区间"与"长期低价区"）。
4. 资金费率 >0.05%/8h 多头拥挤、<-0.05% 空头拥挤；接近 0 为中性。
5. 报告中明确区分 **事实**（本技能返回的数字）与 **推测**（你的判断）。
