# openclaw-okx-api-skill

[English](README.md)

一个 [OpenClaw](https://openclaw.ai) Agent Skill，让 AI Agent 能够通过 OKX 官方 REST API v5 和 WebSocket 流与 [OKX](https://www.okx.com) 加密货币交易所进行交互。

---

## 功能概述

该 Skill 教会 OpenClaw Agent 如何：

- 查询实时市场数据（价格、订单簿、K 线、资金费率）
- 管理账户和持仓
- 下单、改单、撤单
- 通过 WebSocket 订阅实时数据

当用户说"查一下我的 OKX 账户余额"或"在 OKX 下一个 BTC 限价买单"时，Agent 会自动加载该 Skill 的上下文，生成正确的、带鉴权的 API 调用。

---

## 功能范围

### 已覆盖

| 类别 | 功能 |
|------|------|
| 行情数据 | Ticker、订单簿、成交记录、K 线、资金费率、标记价格、未平仓量 |
| 账户 | 余额查询、持仓查询 |
| 订单管理 | 单个或批量下单 / 改单 / 撤单 |
| 订单历史 | 当前挂单、7 天历史、3 个月归档 |
| WebSocket | 公共频道（Ticker、K 线、成交、盘口）；私有频道（订单、持仓、账户） |
| 合约类型 | SPOT（现货）、MARGIN（杠杆）、SWAP（永续合约）、FUTURES（交割合约）、OPTION（期权） |

### 不涉及

该 Skill **不**包含以下功能：

- 账户间资金划转
- 借贷（杠杆）
- 理财 / 质押产品
- 子账户管理
- 期权专属 API（Greeks、行权）
- 税务报告或盈亏分析
- 策略委托（网格、定投、冰山）

---

## 目录结构

```
openclaw-okx-api-skill/
├── SKILL.md                          # OpenClaw Skill 定义（frontmatter + 指引）
├── scripts/
│   └── okx_auth.py                   # 可复用的鉴权/请求工具 — 在脚本中直接导入
├── examples/
│   ├── get-balance.py                # 打印账户余额
│   ├── get-market-data.py            # Ticker + K 线数据
│   ├── place-order.py                # 下限价单（含模拟盘保护）
│   └── websocket-ticker.py          # 通过 WebSocket 获取实时价格流
└── references/
    ├── authentication.md             # HMAC SHA256 签名算法、边界情况、错误码
    ├── market-data-endpoints.md      # 所有公共 REST 端点
    ├── trading-endpoints.md          # 所有私有 REST 端点
    └── websocket.md                  # WebSocket 频道、订阅格式、私有鉴权
```

---

## 安装

### 方式一 — 复制到 OpenClaw 工作区 skills 目录

```bash
cp -r openclaw-okx-api-skill ~/.openclaw/workspace/skills/okx-api
```

### 方式二 — 复制到 agent-skills 插件目录

```bash
cp -r openclaw-okx-api-skill ~/.openclaw/skills/agent-skills/skills/okx-api
```

OpenClaw 会自动发现两个目录中的 Skill，无需额外注册步骤。

---

## 配置

在 `~/.openclaw/openclaw.json` 的顶级 `env` 字段中添加 OKX API 凭证：

```json
{
  "env": {
    "OKX_API_KEY": "your-api-key",
    "OKX_SECRET_KEY": "your-secret-key",
    "OKX_PASSPHRASE": "your-passphrase",
    "OKX_DEMO": "1"
  }
}
```

OpenClaw 会自动将这些变量注入每个 Agent 会话。

| 变量 | 说明 |
|------|------|
| `OKX_API_KEY` | 从 OKX 账户设置中获取的 API Key |
| `OKX_SECRET_KEY` | Secret Key |
| `OKX_PASSPHRASE` | 创建 API Key 时设置的 Passphrase |
| `OKX_DEMO` | 设为 `"1"` 使用沙盒（模拟交易）；省略或设为 `"0"` 则使用实盘 |

> **创建 API Key**：OKX → 账户 → API → 创建 API Key
>
> 模拟盘 Key：OKX 模拟交易 → 账户 → API

---

## 独立使用

`scripts/okx_auth.py` 工具可在任意 Python 项目中独立使用：

```python
import sys
sys.path.insert(0, "path/to/openclaw-okx-api-skill/scripts")
from okx_auth import make_request

# 公共端点 — 无需凭证
ticker = make_request("GET", "/api/v5/market/ticker", params={"instId": "BTC-USDT"})
print(ticker[0]["last"])

# 私有端点 — 需要环境变量 OKX_API_KEY、OKX_SECRET_KEY、OKX_PASSPHRASE
balance = make_request("GET", "/api/v5/account/balance")

# 下单
result = make_request("POST", "/api/v5/trade/order", body={
    "instId": "BTC-USDT",
    "tdMode": "cash",
    "side": "buy",
    "ordType": "limit",
    "px": "40000",
    "sz": "0.001",
})
```

直接运行示例脚本：

```bash
# 行情数据（无需凭证）
python examples/get-market-data.py BTC-USDT 1H

# 账户余额（需要凭证）
OKX_API_KEY=... OKX_SECRET_KEY=... OKX_PASSPHRASE=... python examples/get-balance.py

# 模拟交易
OKX_DEMO=1 python examples/place-order.py BTC-USDT buy limit 40000 0.001

# 实时价格流
python examples/websocket-ticker.py BTC-USDT ETH-USDT
```

---

## 依赖

```
requests
websocket-client   # 仅 websocket-ticker.py 需要
```

安装：

```bash
pip install requests websocket-client
```

需要 Python 3.10+（使用了 `dict | None` 类型联合语法）。

---

## 鉴权简介

OKX API v5 对私有端点使用 HMAC SHA256 签名：

```
signature = base64(hmac_sha256(timestamp + METHOD + path_with_query + body, secret_key))
```

`scripts/okx_auth.py` 中的 `make_request()` 函数会自动处理签名。完整算法、边界情况及错误码参考请见 `references/authentication.md`。

---

## 频率限制

| 端点类别 | 限制 |
|----------|------|
| 公共行情数据 | 每 IP 20 次 / 2s |
| 账户端点 | 每 UID 10 次 / 2s |
| 下单 | 每 UID 60 次 / 2s |
| 撤单 | 每 UID 60 次 / 2s |

遇到错误码 `50011`（超出频率限制）时，等待 2 秒后重试。

---

## License

MIT
