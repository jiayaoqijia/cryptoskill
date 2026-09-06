---
name: aicoin-freqtrade
description: "Use when user asks about Freqtrade — strategy creation, backtest, hyperopt, switching strategies / pairs / dry-run mode, querying live bot status / balance / open positions / 盈亏. Trigger words: 'write strategy', 'create strategy', 'backtest', 'switch strategy', 'switch to live', 'open positions', 'P&L', '写策略', '创建策略', '回测', '部署策略', '切策略', '切实盘', '当前持仓', '今天赚多少', '盈亏'. In CoinClaw containers (OpenClaw / Hermes / Claude Code) freqtrade is a supervisord-managed daemon on :8080 — this skill auto-detects engine + paths via lib/coinclaw-env.mjs and never spawns competing freqtrade processes. Outside CoinClaw it falls back to host mode (clone freqtrade + nohup). For prices/charts use aicoin-market. For exchange trading use aicoin-trading. For Hyperliquid use aicoin-hyperliquid."
metadata: { "openclaw": { "primaryEnv": "AICOIN_ACCESS_KEY_ID", "requires": { "bins": ["node"] }, "homepage": "https://www.aicoin.com/opendata", "source": "https://github.com/aicoincom/coinos-skills", "license": "MIT" } }
required_environment_variables:
  - name: AICOIN_ACCESS_KEY_ID
    optional: true
    prompt: "AiCoin Open API access key ID(策略取数;可选)"
    help: "https://www.aicoin.com/opendata"
  - name: AICOIN_ACCESS_SECRET
    optional: true
    prompt: "AiCoin Open API access secret"
    help: "https://www.aicoin.com/opendata"
---

# AiCoin Freqtrade

Freqtrade 策略 / 回测 / 部署 / 实时控制 — 跨 CoinClaw 三引擎自动适配。

## 关键原则(读完再动手)

### 一、CoinClaw 容器里 freqtrade 是常驻 daemon

OpenClaw / Hermes / Claude Code 三个引擎容器都通过 supervisord 把 freqtrade 起为常驻进程, 监听 `127.0.0.1:8080`, 默认跑 `NoOpStrategy`(空跑). **不要自己起 freqtrade 进程** — 会跟 daemon 抢端口, dashboard 立刻 offline.

正确流程是: 写策略文件 → 调 `ft-deploy.mjs deploy {"strategy":"..."}` → 脚本改 config + 重启 daemon. dashboard 会自动刷出新策略.

`scripts/ft.mjs` + `scripts/ft-deploy.mjs` 内置三引擎自动识别(`lib/coinclaw-env.mjs`), 路径 / auth / supervisord socket 都自动解析, **agent 不用关心是哪个引擎**.

### 二、永远先调 freqtrade REST API, 不要"自己计算"

| 用户问 | 必须先调 |
|---|---|
| 现在赚多少 / 总盈亏 / 今天涨了多少 | `ft.mjs profit` (`/api/v1/profit`) |
| 持仓 / 现在开了哪些 | `ft.mjs trades_open` (`/api/v1/status`) |
| 余额 / 资金多少 | `ft.mjs balance` (`/api/v1/balance`) |
| 跑的什么策略 / 当前模式 | `ft.mjs daemon_info` 或 `config` |
| 历史交易 / 已平仓 | `ft.mjs trades_history` |
| 单交易对绩效 | `ft.mjs profit_per_pair` |

**dashboard 数字对齐规则(关键)**: 用户问"赚了多少"必须报告**两个数字**:
- **已平仓累计盈亏** = `profit_closed_coin` (USDT) — **dashboard 顶栏的累计盈亏 = 这个**
- **含浮动总盈亏** = `profit_all_coin` (USDT) — 已平仓 + 当前持仓的浮动盈亏

只调 `/status` 拿持仓浮动盈亏会漏掉已平仓部分, 导致跟 dashboard 数字不一致 — 用户立刻发现, 信任度归零.

### 三、切策略 / 切实盘 / 切交易对必须走脚本

config.json 是 daemon 启动时读一次, 手动改完不会自动生效. 必须用:

| 操作 | 命令 | 是否需要 daemon 重启 |
|---|---|---|
| 切策略 | `ft.mjs set_strategy {"strategy":"X"}` | 必须重启 (~30s) |
| 切交易对 | `ft.mjs set_pairs {"pairs":[...]}` | 不重启, `reload_config` 即可 |
| 切实盘/模拟 | `ft.mjs set_dry_run {"dry_run":false}` | 必须重启 |
| reload 配置 | `ft.mjs reload` | 不重启 |

或者一次完成所有变更: `ft-deploy.mjs deploy {"strategy":"X","pairs":["BTC/USDT:USDT"],"dry_run":false}`.

**任何直接修改 config.json 的操作(包括手动编辑 pair_whitelist / minimal_roi / stoploss 等), 改完后必须立即调 `ft.mjs reload`** — 否则 daemon 仍用内存里的旧配置运行, 白名单/止损等改动不会生效. 忘了 reload 是最常见的"改了但没用"的原因.

**chat 主动发起的高 stake 操作必须强 confirm**(违反即错):

适用: 用户在 chat 里说"平掉"、"切实盘"、"卖了"、"开仓"等 — 通过 agent 调用 `force_exit` / `force_enter` / `set_dry_run` 的操作.

流程:
1. **先列预览**: 动哪个 trade / pair / 当前盈亏 / 估算损益 / dry_run vs live / 余额状况
2. **明确等用户输"确认"或"yes"** 才真调 `force_exit` / `set_dry_run` / `force_enter`
3. 即使用户语气笃定("平了","直接切"), 也必须先预览等确认

**不需要 confirm 的**:
- 查询类(查持仓 / 盈亏 / 状态) — 直接读
- **freqtrade daemon 自己根据策略信号自动开/平仓** — 这是 daemon 本职工作, 用户切实盘那一刻就授权了, agent 不在这个链路里, 不要拦也不需要 confirm
- 非破坏性配置(`set_pairs` 加币对、`reload`) — 列改动表然后直接执行

**违反规则的反例**:
- ❌ 用户说"平掉", 你直接调 `force_exit` 平了真持仓 (K-Live-3 dogfood 抓到的真 bug)
- ❌ 用户说"切实盘", 你不列 .env key / 余额 / 风险就直接 `set_dry_run {"dry_run":false}`
- ✅ 用户说"平掉", 你列"持仓: BNB/USDT 0.05 +$1.07, 平这单吗? dry_run=true 模拟盘", 等用户确认

**写策略 + 切策略 倾向分两轮**(create_strategy 一轮, set_strategy 一轮). 不是技术限制,是 UX 选择:
1. 第一轮: 写完策略文件 → 告诉用户"已生成 X.py, 要切上去吗?"
2. 用户确认后第二轮: `set_strategy` 切策略 + 重启 daemon (~30s)

这样用户切策略前能 review 生成文件; daemon 重启 30s 期间用户对状态有预期, 不会误判 chat 卡死. 用户明确说"一气呵成做完"也可以单 turn 跑完两步, 但默认分轮.

### 四、Freqtrade 不支持网格策略 (grid)

用户问网格时直接说明限制 + 建议趋势跟踪 / 区间策略 / 网格回报模拟器替代. 不要硬写一个伪网格.

## 快速参考

| 任务 | 命令 |
|------|------|
| 看 daemon 状态 + 配置 | `node scripts/ft-deploy.mjs check` 或 `ft.mjs daemon_info` |
| 看策略列表 | `node scripts/ft-deploy.mjs strategy_list` |
| 创建策略(快速生成器) | `node scripts/ft-deploy.mjs create_strategy '{"name":"MyStrat","timeframe":"15m","indicators":["rsi","macd","ema"],"aicoin_data":["funding_rate"]}'` |
| 部署策略到 daemon | `node scripts/ft-deploy.mjs deploy '{"strategy":"MyStrat"}'` |
| 部署+切实盘 | `node scripts/ft-deploy.mjs deploy '{"strategy":"MyStrat","dry_run":false}'` |
| 回测 | `node scripts/ft-deploy.mjs backtest '{"strategy":"MyStrat","timeframe":"1h","timerange":"20250101-20260301"}'` |
| Hyperopt 调参 | `node scripts/ft-deploy.mjs hyperopt '{"strategy":"MyStrat","timeframe":"1h","epochs":100}'` |
| 看盈亏 | `node scripts/ft.mjs profit` |
| 看持仓 | `node scripts/ft.mjs trades_open` |
| 看余额 | `node scripts/ft.mjs balance` |
| 切交易对 | `node scripts/ft.mjs set_pairs '{"pairs":["BTC/USDT:USDT","ETH/USDT:USDT"]}'` |
| 重启 daemon | `node scripts/ft.mjs restart` |
| 看日志 | `node scripts/ft-deploy.mjs logs '{"lines":100}'` |

## 创建策略：先判断走哪条路

**判断规则**：
- 用户只给了笼统描述（"RSI 策略"、"均线交叉"、"布林带回归"）且没指定具体参数细节 → **A. 快速生成器**
- 用户给了具体逻辑（自定义入场/出场条件、跨周期共振、多币种轮动、复合指标、自定义仓位管理）→ **B. 直接写 Python**
- 用 A 生成后用户要改细节 → 直接编辑生成的 .py 文件，不要重新 create_strategy 覆盖

### A. 快速生成器(简单策略)

`create_strategy` 一条命令生成一个可跑的策略文件。适合"先跑起来再调"的场景：

```bash
node scripts/ft-deploy.mjs create_strategy '{"name":"MACDStrategy","timeframe":"15m","indicators":["macd","rsi","atr"]}'
node scripts/ft-deploy.mjs create_strategy '{"name":"RSILong","timeframe":"1h","indicators":["rsi"],"direction":"long"}'
node scripts/ft-deploy.mjs create_strategy '{"name":"WhaleStrat","timeframe":"15m","indicators":["rsi","macd"],"aicoin_data":["funding_rate","ls_ratio"]}'
```

可选 `indicators`: `rsi`, `bb`, `ema`, `sma`, `macd`, `stochastic`/`kdj`, `atr`, `adx`, `cci`, `williams_r`, `vwap`, `ichimoku`, `volume_sma`, `obv`.

可选 `direction`: `"long"` (默认,只做多) | `"short"` (只做空) | `"both"` (双向)。
**用户说"RSI<30 买入, RSI>70 卖出"→ direction="long"**(RSI>70 = 平多, 不是开空)。只有用户明确说"做空 / 双向 / 多空都做"时才用 `"both"` 或 `"short"`。

可选 `aicoin_data`: `funding_rate`、`ls_ratio`、`big_orders`、`liquidation_map`（都需付费套餐），`open_interest`（v3 聚合 OI 历史暂未接通，会自动降级到默认值）。

**生成器的局限**：只能组合预设指标，不支持跨周期、多币种轮动、自定义复合指标。遇到这些需求直接走 B。

### B. 自定义 Python 策略 (复杂逻辑)

直接写 `.py` 文件到 daemon 的 strategy 目录。用这条路可以实现任何 freqtrade 支持的策略逻辑（跨周期 informative pairs、自定义仓位管理、多指标复合条件等）。

三引擎该目录不同, **从 `daemon_info` 拿**或用 `Write` 工具写到下面任一路径(脚本会自动用 `/api/v1/show_config` 验证):

| 引擎 | strategy 目录 |
|---|---|
| OpenClaw | `~/.openclaw/workspace/strategies/` |
| Hermes | `/workspace/strategies/` |
| Claude Code | `/workspace/strategies/` |

用 AiCoin Python SDK (`aicoin_data.py`, image build 时已复制到上面目录, 也由 `create_strategy` 兜底拷贝):

它封装了 AiCoin Open API v3：

```python
from aicoin_data import AiCoinData

ac = AiCoinData(cache_ttl=300)   # 自动从 .env 读 key，内置 5 分钟缓存

# 高层信号 —— 直接返回能用的数字，丢进策略即可
ac.whale_signal("BTC/USDT:USDT", "binance")        # 大单买卖压力 -1..+1
ac.ls_ratio_norm()                                 # 多空比 0..1（>0.5 偏多）
ac.funding_rate_pct("BTC/USDT:USDT", "binance")    # 最新资金费率（百分比）
ac.liq_bias("BTC/USDT:USDT", "binance")            # 清算图方向偏向 -1..+1

# 原始数据
ac.coin_ticker("bitcoin,ethereum")                 # 实时行情
ac.klines("BTC/USDT", "binance", interval="1h", limit=100)

# 任意 v3 接口 —— path 是 /api/v3/ 后那段，清单见 https://open.aicoin.com/api/v3/_catalog
ac.get("markets/hot-coins", {"tab_key": "defi"})
ac.get("hyperliquid/whales/open-positions", {"coin": "BTC"})
```

回测期 AiCoin 实时数据不可用，高层信号会抛异常 —— 策略里要 `try/except` 兜底用默认值。资金费率、大单、清算等需要付费套餐，没权限同样抛异常（一样兜底）。

#### 完整模板

```python
from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import logging, time

logger = logging.getLogger(__name__)


class MyStrategy(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = '15m'
    can_short = True

    minimal_roi = {"0": 0.05, "60": 0.03, "120": 0.01}
    stoploss = -0.05
    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.03

    rsi_buy = IntParameter(20, 40, default=30, space='buy')
    rsi_sell = IntParameter(60, 80, default=70, space='sell')

    _ac_funding_rate = 0.0
    _ac_last_update = 0.0

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI
        delta = dataframe['close'].diff()
        gain = delta.clip(lower=0).rolling(window=14).mean()
        loss = (-delta.clip(upper=0)).rolling(window=14).mean()
        rs = gain / loss
        dataframe['rsi'] = 100 - (100 / (1 + rs))

        # AiCoin 数据 (live/dry_run only, backtest 用默认值 0.0)
        dataframe['funding_rate'] = 0.0
        if self.dp and self.dp.runmode.value in ('live', 'dry_run'):
            now = time.time()
            if now - self._ac_last_update > 300:
                self._update_aicoin_data(metadata)
                self._ac_last_update = now
            dataframe.iloc[-1, dataframe.columns.get_loc('funding_rate')] = self._ac_funding_rate

        return dataframe

    def _update_aicoin_data(self, metadata: dict):
        try:
            import sys, os
            _sd = os.path.dirname(os.path.abspath(__file__))
            if _sd not in sys.path:
                sys.path.insert(0, _sd)
            from aicoin_data import AiCoinData
            ac = AiCoinData(cache_ttl=300)
            pair = metadata.get('pair', 'BTC/USDT:USDT')
            exchange = self.config.get('exchange', {}).get('name', 'binance')
            self._ac_funding_rate = ac.funding_rate_pct(pair, exchange)
        except Exception as e:
            logger.warning(f"AiCoin data error: {e}")

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe['rsi'] < self.rsi_buy.value) &
            (dataframe['volume'] > 0),
            'enter_long'] = 1
        dataframe.loc[
            (dataframe['rsi'] > self.rsi_sell.value) &
            (dataframe['volume'] > 0),
            'enter_short'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[(dataframe['rsi'] > 70), 'exit_long'] = 1
        dataframe.loc[(dataframe['rsi'] < 30), 'exit_short'] = 1
        return dataframe
```

写完后用 `deploy {"strategy":"MyStrategy"}` 让 daemon 切到这个策略.

### AiCoin 数据集成模式

| AiCoin 数据 | 信号逻辑 | 套餐 |
|---|---|---|
| `funding_rate` | 大于 0.01% → 多头过度 → 空信号; 小于 -0.01% → 多信号 | 基础版 |
| `ls_ratio` | 小于 0.45 (空头多) → 反向做多; 大于 0.55 → 反向做空 | 基础版 |
| `big_orders` | `(buy_vol-sell_vol)/total > 0.3` → 鲸鱼买入做多 | 标准版 |
| `open_interest` | OI 涨 + 价涨 = 健康趋势; OI 涨 + 价跌 = 反转 | 专业版 |
| `liquidation_map` | 上方爆仓多 → 多头挤压 → 做多 | 高级版 |

### 回测注意事项

AiCoin 实时数据**不在历史区间内可用**. 回测时:

- AiCoin 列用默认值 (`funding_rate=0.0`, `ls_ratio=0.5`, `whale_signal=0.0`)
- 回测结果只反映**技术指标**部分
- live/dry_run 跑的时候才用真实 AiCoin 数据, 表现应该比回测好

向用户报告回测结果时必须主动说明这点, 不要让用户以为回测包含了 AiCoin 信号.

## 脚本 API

### `scripts/ft-deploy.mjs` — 策略 / 回测 / 部署

| Action | 参数示例 |
|---|---|
| `check` | (无) — 返回 daemon 状态 + 配置 + 余额 |
| `daemon_info`(在 ft.mjs) | (无) — 单调用拿全 |
| `deploy` | `{"strategy":"MyStrat"}` 或 `{"strategy":"MyStrat","dry_run":false,"pairs":["BTC/USDT:USDT"]}` |
| `create_strategy` | `{"name":"MyStrat","timeframe":"15m","indicators":["rsi","macd"],"direction":"long","aicoin_data":["funding_rate"]}` |
| `backtest` | `{"strategy":"MyStrat","timeframe":"1h","timerange":"20250101-20260301","pairs":["ETH/USDT:USDT"]}` |
| `hyperopt` | `{"strategy":"MyStrat","timeframe":"1h","epochs":100}` |
| `download_data` | `{"timeframe":"1h","timerange":"20250101-"}` |
| `strategy_list` | (无) |
| `backtest_results` | (无) — 列最近 10 个回测结果文件名 |
| `start` / `stop` | (无) — coinclaw 模式调 supervisorctl, host 模式管 PID |
| `status` / `logs` | `{"lines":100}` |
| `update` / `remove` | coinclaw 模式 no-op (提示用 helm upgrade / web UI 删 instance) |

### `scripts/ft.mjs` — 实时控制 (REST + 配置变更)

| Action | 用途 |
|---|---|
| `daemon_info` | 一次拿 strategy / mode / pairs / open trades 数量 |
| `profit` | 已平仓累计 + 含浮动总盈亏 (回答盈亏类问题必须先调) |
| `trades_open` | 当前持仓 (调 /status) |
| `trades_history` | 已平仓交易 |
| `balance` | 余额 |
| `profit_per_pair` | 每交易对绩效 |
| `daily` / `weekly` / `monthly` | 时间维度统计 |
| `force_enter` / `force_exit` | 手动开/平仓 |
| `set_strategy` | 切策略 (改 config + 重启 daemon) |
| `set_pairs` | 改交易对白名单 (reload, 不重启) |
| `set_dry_run` | 切实盘/模拟 (改 config + 重启 daemon) |
| `restart` | 重启 freqtrade daemon (supervisorctl + kill 兜底) |
| `reload` | reload_config 而不重启 |
| `start` / `stop` / `ping` / `version` / `health` | 标准 REST |
| `logs` | freqtrade 自带 /logs 接口 |

### `scripts/ft-dev.mjs` — 调试 (回测 / 蜡烛 / 策略详情)

`backtest_start` / `backtest_status` / `backtest_history` / `candles_live` / `candles_analyzed` / `strategy_list` / `strategy_get` / `whitelist` / `blacklist` 等.

## 环境变量与认证

`.env` 自动加载顺序:

- coinclaw 容器内: `/workspace/.env` (Hermes/CC) 或 `/home/node/.openclaw/workspace/.env` (OpenClaw)
- host 模式: **`~/.coinos/.env`**(coinos 文件夹, 推荐)→ 当前目录 `.env` → 旧 `~/.openclaw/.env`(向后兼容)

freqtrade REST 认证: `freqtrade-api.mjs` 自动从容器内 `.ft_api_pass` 文件读密码, **agent 不用配 FREQTRADE_USERNAME / FREQTRADE_PASSWORD**. 用户也可以通过 `.env` 覆盖.

交易所 key 在 web UI 的 EnvSection 里配置, 写到 .env 后 entrypoint 会自动 patch 进 freqtrade `config.json`. **agent 不要直接读 .env 给用户看交易所 key**.

AiCoin Open API key (用于策略集成 AiCoin 数据):
```
AICOIN_ACCESS_KEY_ID=your-key-id
AICOIN_ACCESS_SECRET=your-secret
```

## 付费功能引导

返回 304 / 403 时 **不要重试**, 直接告诉用户:

| 套餐 | 价格 | 用途 |
|---|---|---|
| 免费版 | $0 | 纯技术指标 |
| 基础版 | $29/mo | + `funding_rate`, `ls_ratio` |
| 标准版 | $79/mo | + `big_orders`, `agg_trades` |
| 高级版 | $299/mo | + `liquidation_map` |
| 专业版 | $699/mo | + `open_interest`, `ai_analysis` |

获取地址: https://www.aicoin.com/opendata

## 跨 skill 引用

| 用户问 | 用 |
|---|---|
| 单纯查行情 / K 线 / 新闻 / 资金费率 (不开仓) | **aicoin-market** |
| 直接下单 / 开仓 / 平仓 (不通过 freqtrade) | **aicoin-trading** |
| Hyperliquid 鲸鱼 / 持仓 / 清算 | **aicoin-hyperliquid** |
| 链上 DEX swap / 钱包余额 / gas | **aicoin-onchain** |
| 余额 / 持仓 / 注册 / API key 配置 (账户类) | **aicoin-account** |

## 常见 pitfall

- **不要 `cat /workspace/.ft_api_pass`** 把内部 daemon 密码贴到 chat — 直接用 `ft.mjs` 调 REST, 脚本内部读密码不会泄漏.
- **不要在 chat 里 echo 用户的交易所 key** — 这些是高敏数据, 引导用户去 EnvSection 配置.
- **不要自己心算 RSI / MACD / EMA** — freqtrade 算出的值跟你心算结果会差, 用 `ft-dev.mjs candles_analyzed` 拿 daemon 的真实指标.
- **不要"先 stop daemon 再 freqtrade trade ... &"** — 那是绕过 supervisord, 下次 dashboard 看到的还是老的 daemon 状态. 必须用 `set_strategy` / `deploy` / `restart`.
- **回测拿不到 AiCoin 数据是正常的** — 不要造假 CSV 喂回测, 直接告诉用户回测只反映技术指标. 见根 AGENTS.md 的"数据准确性铁则".
