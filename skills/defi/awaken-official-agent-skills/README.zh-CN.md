# Awaken Agent Kit

[![English](https://img.shields.io/badge/docs-English-blue)](./README.md)
[![Unit Tests](https://github.com/Awaken-Finance/awaken-agent-skills/actions/workflows/test.yml/badge.svg)](https://github.com/Awaken-Finance/awaken-agent-skills/actions/workflows/test.yml)
[![Coverage](https://img.shields.io/endpoint?url=https://Awaken-Finance.github.io/awaken-agent-skills/coverage.json)](https://Awaken-Finance.github.io/awaken-agent-skills/coverage.json)

> 面向 [Awaken DEX](https://awaken.finance)（[aelf](https://aelf.com) 区块链）的 AI Agent 工具包 —— 代币兑换、流动性管理、K 线数据获取。

---

## 架构

```
awaken-agent-kit/
├── index.ts                  # SDK 入口 — 可直接导入用于 LangChain / LlamaIndex
├── src/
│   ├── core/                 # 纯业务逻辑（无 I/O 副作用）
│   │   ├── query.ts          # getQuote, getPair, getTokenBalance, getTokenAllowance, getLiquidityPositions
│   │   ├── trade.ts          # executeSwap, addLiquidity, removeLiquidity, approveTokenSpending
│   │   └── kline.ts          # fetchKline, getKlineIntervals
│   └── mcp/
│       └── server.ts         # MCP 适配器 — 用于 Claude Desktop、Cursor、GPT 等
├── awaken_query_skill.ts     # CLI 适配器 — OpenClaw / 终端查询命令
├── awaken_trade_skill.ts     # CLI 适配器 — OpenClaw / 终端交易命令
├── awaken_kline_skill.ts     # CLI 适配器 — OpenClaw / 终端 K 线命令
├── cli-helpers.ts            # CLI 输出工具（outputSuccess / outputError）
├── lib/
│   ├── config.ts             # 网络配置、环境变量覆盖、默认值
│   ├── aelf-client.ts        # aelf-sdk 封装（钱包、合约调用、精度转换）
│   └── types.ts              # TypeScript 接口与常量
├── openclaw.json             # OpenClaw 工具定义
├── mcp-config.example.json   # MCP 客户端配置示例
├── .env.example              # 环境变量模板
└── __tests__/                # 单元 / 集成 / E2E 测试
```

**Core + Adapters 分层模式：**

| 层 | 位置 | 职责 |
|---|------|------|
| **Core** | `src/core/` | 纯函数。无 `process.exit`，无 `console.log`。出错则 throw。 |
| **CLI 适配器** | `awaken_*_skill.ts` | 基于 `commander` 的薄包装层。解析参数 → 调用 core → 输出 JSON。 |
| **MCP 适配器** | `src/mcp/server.ts` | 将 core 函数注册为 MCP 工具，供 Claude Desktop、Cursor、GPT 等使用。 |
| **SDK** | `index.ts` | 重新导出 core 函数和类型。`import { executeSwap } from '@awaken-finance/agent-kit'`。 |

---

## 功能列表

| # | 分类 | 能力 | CLI 工具 | MCP 工具 | SDK 函数 |
|---|------|------|----------|----------|----------|
| 1 | 查询 | Swap 报价与路由 | `awaken-query-quote` | `awaken_quote` | `getQuote` |
| 2 | 查询 | 交易对信息 | `awaken-query-pair` | `awaken_pair` | `getPair` |
| 3 | 查询 | 代币余额 | `awaken-query-balance` | `awaken_balance` | `getTokenBalance` |
| 4 | 查询 | 代币授权额度 | `awaken-query-allowance` | `awaken_allowance` | `getTokenAllowance` |
| 5 | 查询 | 流动性持仓（含 USD 价值） | `awaken-query-liquidity` | `awaken_liquidity` | `getLiquidityPositions` |
| 6 | 交易 | 代币兑换 | `awaken-trade-swap` | `awaken_swap` | `executeSwap` |
| 7 | 交易 | 添加流动性 | `awaken-trade-add-liquidity` | `awaken_add_liquidity` | `addLiquidity` |
| 8 | 交易 | 移除流动性 | `awaken-trade-remove-liquidity` | `awaken_remove_liquidity` | `removeLiquidity` |
| 9 | 交易 | 授权代币消费 | `awaken-trade-approve` | `awaken_approve` | `approveTokenSpending` |
| 10 | K线 | 获取 K 线数据 | `awaken-kline-fetch` | `awaken_kline_fetch` | `fetchKline` |
| 11 | K线 | 列出时间间隔 | `awaken-kline-intervals` | `awaken_kline_intervals` | `getKlineIntervals` |

---

## 前置要求

- [Bun](https://bun.sh) ≥ 1.0
- 一个 aelf 钱包私钥（仅交易操作需要）

---

## 快速开始

### 1. 安装

```bash
# 作为依赖安装
bun add @awaken-finance/agent-kit

# 或克隆后本地安装
git clone https://github.com/AwakenFinance/awaken-agent-skills.git
cd awaken-agent-skills
bun install
```

### 2. 配置

```bash
cp .env.example .env
# 编辑 .env — 填入你的 AELF_PRIVATE_KEY
```

### 3. 一键配置（推荐）

```bash
# 配置 Claude Desktop
bun run bin/setup.ts claude

# 配置 Cursor（项目级）
bun run bin/setup.ts cursor

# 配置 Cursor（全局）
bun run bin/setup.ts cursor --global

# 配置 IronClaw
bun run bin/setup.ts ironclaw

# 生成 OpenClaw 配置
bun run bin/setup.ts openclaw

# 查看配置状态
bun run bin/setup.ts list

# 从平台移除配置
bun run bin/setup.ts uninstall claude
bun run bin/setup.ts uninstall ironclaw
```

setup 工具自动检测操作系统、推导路径、安全合并配置（不会覆盖其他 MCP server）。配置完成后，编辑生成的配置文件，将 `<YOUR_PRIVATE_KEY>` 替换为你的实际私钥。

### IronClaw

```bash
bun run bin/setup.ts ironclaw
bun run bin/setup.ts uninstall ironclaw
```

IronClaw 安装会向 `~/.ironclaw/mcp-servers.json` 写入 stdio MCP entry，并把当前仓库的 `SKILL.md` 安装到 `~/.ironclaw/skills/awaken-agent-skills/SKILL.md`。

关于 trust model 的说明：

- 如果要执行 swap、liquidity、approve 这类写能力，必须使用上面的 trusted skill 路径。
- 不要把 `~/.ironclaw/installed_skills/` 当成主安装路径，否则写操作的 approval 行为会不稳定。
- 当前 MCP server 会同时输出标准 MCP camelCase annotations 和 IronClaw 兼容 snake_case annotations，确保 IronClaw 能识别读写 hints。

远程激活契约：

- GitHub repo/tree URL 只用于 discovery，不是最终的 IronClaw 安装载体。
- 推荐的 IronClaw npm 激活命令：`bunx -p @awaken-finance/agent-kit awaken-setup ironclaw`
- OpenClaw 若有 ClawHub / managed install 则优先使用；否则回退到 `bunx -p @awaken-finance/agent-kit awaken-setup openclaw`
- 本地 repo checkout 仅保留给开发阶段 smoke test。

最短 smoke test：

1. `bun run bin/setup.ts ironclaw`
2. 让 IronClaw 查询 `quote ELF to USDT on Awaken`
3. 再让它执行 `approve ELF for Awaken`，确认执行前会出现 approval

**高级选项：**

```bash
# 自定义配置文件路径
bun run bin/setup.ts claude --config-path /custom/path/config.json

# 自定义 MCP server 路径
bun run bin/setup.ts cursor --server-path /my/custom/server.ts

# 强制覆盖已有配置
bun run bin/setup.ts claude --force
```

**配置优先级（高 → 低）：**

1. 函数参数（SDK 调用者）
2. CLI 参数（`--network`, `--slippage`）
3. MCP env 块（`mcp.json` → `env: {}`）
4. 环境变量（`AWAKEN_*`）
5. `.env` 文件
6. 代码默认值

查看 [`.env.example`](./.env.example) 了解所有可覆盖配置（RPC 地址、API 地址、合约地址、滑点等）。

---

## 使用方式

### CLI（OpenClaw / 终端）

```bash
# 查询兑换报价
bun run awaken_query_skill.ts quote --symbol-in ELF --symbol-out USDT --amount-in 10

# 查询交易对
bun run awaken_query_skill.ts pair --token0 ELF --token1 USDT --fee-rate 0.3

# 查询余额
bun run awaken_query_skill.ts balance --address YOUR_ADDRESS --symbol ELF

# 查询流动性持仓
bun run awaken_query_skill.ts liquidity --address YOUR_ADDRESS

# 代币兑换（需要 signer：输入/上下文/env 任一可用）
bun run awaken_trade_skill.ts swap --symbol-in ELF --symbol-out USDT --amount-in 1

# 添加流动性（需要 signer：输入/上下文/env 任一可用）
bun run awaken_trade_skill.ts add-liquidity --token-a ELF --token-b USDT --amount-a 10 --amount-b 5

# 移除流动性（需要 signer：输入/上下文/env 任一可用）
bun run awaken_trade_skill.ts remove-liquidity --token-a ELF --token-b USDT --lp-amount 0.5

# 获取 K 线数据
bun run awaken_kline_skill.ts fetch --pair-id PAIR_UUID --interval 1D

# 列出 K 线时间间隔
bun run awaken_kline_skill.ts intervals
```

所有命令成功时输出标准化 JSON，错误输出到 stderr 并带 `[ERROR]` 前缀。

### MCP（Claude Desktop / Cursor / GPT）

1. 将 [`mcp-config.example.json`](./mcp-config.example.json) 中的配置复制到你的 AI 工具的 MCP 设置中：

   - **Claude Desktop**：`~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Cursor（项目级）**：`.cursor/mcp.json`
   - **Cursor（全局）**：`~/.cursor/mcp.json`

2. 更新路径和环境变量：

```json
{
  "mcpServers": {
    "awaken-agent-kit": {
      "command": "bun",
      "args": ["run", "/绝对路径/scripts/skills/src/mcp/server.ts"],
      "env": {
        "AELF_PRIVATE_KEY": "你的私钥",
        "AWAKEN_NETWORK": "mainnet"
      }
    }
  }
}
```

3. 手动启动 MCP 服务器（用于调试）：

```bash
bun run mcp
```

### 跨 Skill 签名上下文（推荐）

写操作工具（`swap`、`addLiquidity`、`removeLiquidity`、`approve`）统一按以下顺序解析 signer：

1. 显式输入（`signer.privateKey` 或 CA 三元组）
2. Active wallet context（`~/.portkey/skill-wallet/context.v1.json`）
3. 环境变量回退（`AELF_PRIVATE_KEY` 或 `PORTKEY_*`）

可选 `signer` 入参示例：

```json
{
  "signerMode": "auto",
  "walletType": "EOA",
  "address": "ELF_...",
  "password": "可选密码",
  "privateKey": "可选显式私钥"
}
```

`signerMode=daemon` 已预埋接口，但本轮仍返回 `SIGNER_DAEMON_NOT_IMPLEMENTED`。

### SDK（TypeScript / JavaScript）

```typescript
import {
  getQuote,
  executeSwap,
  getNetworkConfig,
  getLiquidityPositions,
} from '@awaken-finance/agent-kit';

// 查询兑换报价
const config = getNetworkConfig('mainnet');
const quote = await getQuote(config, {
  symbolIn: 'ELF',
  symbolOut: 'USDT',
  amountIn: '10',
});
console.log(quote);

// 执行兑换（需要 privateKey）
const result = await executeSwap(config, wallet, {
  symbolIn: 'ELF',
  symbolOut: 'USDT',
  amountIn: '10',
  slippage: '0.005',
});
console.log(result.transactionId);
```

### OpenClaw

将 [`openclaw.json`](./openclaw.json) 导入你的 OpenClaw 配置。所有 11 个工具已预配置，描述针对 AI 理解进行了优化。

---

## 网络

| 网络 | Chain ID | RPC | 区块浏览器 |
|------|----------|-----|-----------|
| **mainnet**（默认） | tDVV | `https://tdvv-public-node.aelf.io` | `https://aelfscan.io/tDVV` |
| testnet | tDVW | `https://tdvw-test-node.aelf.io` | `https://testnet.aelfscan.io/tDVW` |

通过 `--network testnet`（CLI）、`AWAKEN_NETWORK=testnet`（环境变量）或直接传入 config（SDK）切换网络。

---

## 测试

```bash
# 全部测试
bun test

# 仅单元测试
bun run test:unit

# 集成测试（需要网络）
bun run test:integration

# E2E 测试（需要 AELF_PRIVATE_KEY，在 mainnet 发送真实交易）
bun run test:e2e
```

| 测试级别 | 覆盖范围 |
|---------|---------|
| **Unit** | 配置、类型、精度运算、Core 导出、错误路径、MCP server、CLI helpers |
| **Integration** | Awaken API、链上 view 调用、SignalR K 线、Core query 函数 |
| **E2E** | mainnet 真实 Swap 与流动性增减 |

---

## 环境变量

| 变量 | 是否必填 | 默认值 | 说明 |
|------|---------|--------|------|
| `AELF_PRIVATE_KEY` | 交易时必填 | — | aelf 钱包私钥 |
| `PORTKEY_PRIVATE_KEY` | CA 交易时可选 | — | Portkey Manager 私钥 |
| `PORTKEY_CA_HASH` | CA 交易时可选 | — | Portkey CA Hash |
| `PORTKEY_CA_ADDRESS` | CA 交易时可选 | — | Portkey CA Address |
| `PORTKEY_WALLET_PASSWORD` | 否 | — | EOA wallet context 解密密码缓存（可选） |
| `PORTKEY_CA_KEYSTORE_PASSWORD` | 否 | — | CA keystore context 解密密码缓存（可选） |
| `PORTKEY_SKILL_WALLET_CONTEXT_PATH` | 否 | `~/.portkey/skill-wallet/context.v1.json` | 覆盖 active context 文件路径 |
| `AWAKEN_NETWORK` | 否 | `mainnet` | `mainnet` 或 `testnet` |
| `AWAKEN_RPC_URL` | 否 | 按网络 | 覆盖 RPC 地址 |
| `AWAKEN_API_BASE_URL` | 否 | 按网络 | 覆盖 API 地址 |
| `AWAKEN_SOCKET_URL` | 否 | 按网络 | 覆盖 SignalR 地址 |
| `AWAKEN_EXPLORER_URL` | 否 | 按网络 | 覆盖区块浏览器地址 |
| `AWAKEN_TOKEN_CONTRACT` | 否 | 按网络 | 覆盖 Token 合约地址 |
| `AWAKEN_SWAP_HOOK_CONTRACT` | 否 | 按网络 | 覆盖 Swap Hook 合约地址 |
| `AWAKEN_DEFAULT_SLIPPAGE` | 否 | `0.005` | 默认滑点容忍度 |

---

## 安全

- **永远不要提交你的 `.env` 文件。** 它已默认被 git 忽略。
- 私钥仅用于交易操作（兑换、添加/移除流动性、授权）。查询和 K 线操作为只读。
- 使用 MCP 时，通过 MCP 配置的 `env` 块传入私钥 —— 不会通过网络传输。

---

## 许可证

MIT
