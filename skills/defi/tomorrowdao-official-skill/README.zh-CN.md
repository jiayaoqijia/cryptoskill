# @tomorrowdao/agent-skills

[English](./README.md) | 中文

[![Unit Tests](https://github.com/TomorrowDAOProject/tomorrowDAO-skill/actions/workflows/test.yml/badge.svg)](https://github.com/TomorrowDAOProject/tomorrowDAO-skill/actions/workflows/test.yml)
[![Coverage](https://img.shields.io/endpoint?url=https://TomorrowDAOProject.github.io/tomorrowDAO-skill/coverage.json)](https://TomorrowDAOProject.github.io/tomorrowDAO-skill/coverage.json)

TomorrowDAO 的 AI Agent Skills 工具包，提供 **MCP + OpenClaw + CLI + SDK** 四种接入方式。

## 功能概览

- DAO：创建 DAO、更新 metadata、创建/投票/撤回/执行提案、讨论区接口
- Token 工具：balance view、allowance view、approve payload/send helper
- DAO 读工具：proposal my-info、DAO token allowance view alias、DAO token balance view alias
- Network Governance：提案创建/投票/Release、组织创建、合约名管理、合约流程工具
- BP Election：申请/退出、投票/撤回/切票、分红领取、团队信息维护
- Resource：资源代币买卖与记录查询
- 统一返回类型：`ToolResult<T>`、`TxReceipt`
- 执行模式：`simulate`（默认）和 `send`

## 接入方式

| 模式 | 入口 | 适用场景 |
|------|------|------|
| MCP | `src/mcp/server.ts` | Claude Desktop、Cursor、GPT 等 MCP 客户端 |
| CLI | `tomorrowdao_skill.ts` | 终端脚本、OpenClaw |
| SDK | `index.ts` | 自定义 Agent、LangChain/LlamaIndex |

## 架构

```text
tomorrowDAO-skill/
├── index.ts                # SDK 导出
├── tomorrowdao_skill.ts    # CLI 适配层
├── src/
│   ├── core/               # config/auth/http/chain/tx/error/types
│   ├── domains/            # dao/token/network/bp/resource
│   └── mcp/server.ts       # MCP 适配层
├── lib/                    # 兼容导出
├── bin/setup.ts            # claude/cursor/openclaw/ironclaw 一键配置
├── openclaw.json
├── mcp-config.example.json
└── tests/                  # unit/integration/e2e
```

## 快速开始

### 1. 安装

```bash
bun install
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 填写网络配置与可选 signer 回退配置
```

### 3. 一键配置（推荐）

```bash
# Claude Desktop
bun run setup claude

# Cursor（项目级）
bun run setup cursor

# Cursor（全局）
bun run setup cursor --global

# OpenClaw（打印配置）
bun run setup openclaw

# OpenClaw（合并到已有配置文件）
bun run setup openclaw --config-path /path/to/openclaw-config.json

# IronClaw（安装 trusted skill + stdio MCP server）
bun run setup ironclaw

# 查看配置状态
bun run setup list

# 移除 IronClaw 集成
bun run setup uninstall ironclaw
```

### IronClaw

```bash
# 安装 trusted skill + stdio MCP server
bun run setup ironclaw

# 移除 IronClaw 集成
bun run setup uninstall ironclaw
```

IronClaw 默认会做两件事：

- 向 `~/.ironclaw/mcp-servers.json` 写入一个 stdio MCP server
- 把当前仓库的 `SKILL.md` 复制到 `~/.ironclaw/skills/tomorrowdao-agent-skills/SKILL.md`

关于 trust model 的重要说明：

- 需要 DAO、BP、治理、资源类写操作时，务必使用上面的 trusted skill 路径。
- 如果你把这个包放进 `~/.ironclaw/installed_skills/`，不要期待它还能正常执行提案创建、投票、Release、BP 操作、资源交易等写操作。
- IronClaw 会把 installed skill 的工具权限衰减为只读，这会表现成“只能查，不能写”，即使 MCP server 本身是可用的。

当前 MCP server 已为写操作补齐 destructive annotations，IronClaw 可以据此在 DAO、治理、BP、资源状态变更前请求 approval。
为兼容当前 IronClaw 源码，这里的 MCP annotations 会同时输出标准 MCP 的 camelCase 字段和 IronClaw 兼容的 snake_case 字段，因为 IronClaw 目前按 snake_case 解析 MCP approval hints。

远程激活契约：

- GitHub repo/tree URL 只用于 discovery，不是最终的 IronClaw 安装载体。
- 推荐的 IronClaw npm 激活命令：`bunx -p @tomorrowdao/agent-skills tomorrowdao-setup ironclaw`
- OpenClaw 若有 ClawHub / managed install 则优先使用；否则回退到 `bunx -p @tomorrowdao/agent-skills tomorrowdao-setup openclaw`
- 本地 repo checkout 仅保留给开发阶段 smoke test。

## 环境变量

| 变量 | 必填 | 默认值 | 说明 |
|------|------|------|------|
| `TMRW_API_BASE` | 否 | `https://api.tmrwdao.com` | TomorrowDAO API 基地址 |
| `TMRW_AUTH_BASE` | 否 | `https://api.tmrwdao.com` | 鉴权服务基地址 |
| `TMRW_CHAIN_DEFAULT_DAO` | 否 | `tDVV` | DAO 默认链 |
| `TMRW_CHAIN_DEFAULT_NETWORK` | 否 | `AELF` | Network Governance 默认链 |
| `TMRW_AUTH_CHAIN_ID` | 否 | `AELF` | 鉴权签名使用链 ID |
| `TMRW_PRIVATE_KEY` | 否（`send`/鉴权 env 回退） | — | 签名私钥回退 |
| `AELF_PRIVATE_KEY` | 否 | — | 共享 skill 兼容的第二优先级私钥回退 |
| `PORTKEY_PRIVATE_KEY` | 否 | — | 共享 skill 兼容的第三优先级私钥回退 |
| `PORTKEY_WALLET_PASSWORD` | 否 | — | EOA wallet context 的密码缓存（可选） |
| `PORTKEY_CA_KEYSTORE_PASSWORD` | 否 | — | CA keystore context 的密码缓存（可选） |
| `PORTKEY_SKILL_WALLET_CONTEXT_PATH` | 否 | `~/.portkey/skill-wallet/context.v1.json` | 覆盖 active wallet context 文件路径 |
| `TMRW_SOURCE` | 否 | `nightElf` | 鉴权 `source` 字段 |
| `TMRW_CA_HASH` | 否 | — | 可选鉴权 `ca_hash` |
| `TMRW_RPC_AELF` | 否 | `https://aelf-public-node.aelf.io` | AELF RPC |
| `TMRW_RPC_TDVV` | 否 | `https://tdvv-public-node.aelf.io` | tDVV RPC |
| `TMRW_HTTP_TIMEOUT_MS` | 否 | `10000` | HTTP 超时时间（毫秒） |
| `TMRW_HTTP_RETRY_MAX` | 否 | `1` | 可重试请求的最大重试次数 |
| `TMRW_HTTP_RETRY_BASE_MS` | 否 | `200` | 重试指数退避基础间隔（毫秒） |
| `TMRW_HTTP_RETRY_POST` | 否 | `0` | 设为 `1/true` 时允许 POST 自动重试 |
| `TMRW_AELF_CACHE_MAX` | 否 | `8` | 长生命周期进程中 AElf 客户端缓存上限 |
| `TMRW_LOG_LEVEL` | 否 | `error` | 结构化日志级别（`error/warn/info/debug`） |

## 使用示例

### CLI

```bash
# DAO
bun run tomorrowdao_skill.ts dao create --input '{"args":{"metadata":{"name":"demo"}}}' --mode simulate

# DAO 投票（proposalId 和 votingItemId 都可作为 DAO 提案 hash 别名）
bun run tomorrowdao_skill.ts dao vote --input '{"args":{"proposalId":"<PROPOSAL_ID>","voteOption":0,"voteAmount":100000000}}' --mode send

# DAO Token 余额查询
bun run tomorrowdao_skill.ts dao token-balance-view --input '{"chainId":"tDVV","symbol":"AIBOUNTY","owner":"<OWNER_ADDRESS>"}'

# 通用 Token 余额查询
bun run tomorrowdao_skill.ts token balance-view --input '{"chainId":"tDVV","symbol":"AIBOUNTY","owner":"<OWNER_ADDRESS>"}'

# 通用 Token allowance 查询
bun run tomorrowdao_skill.ts token allowance-view --input '{"chainId":"tDVV","symbol":"AIBOUNTY","owner":"<OWNER_ADDRESS>","spender":"<SPENDER_ADDRESS>"}'

# 通用 Token approve（CA forward 编排优先用 simulate，EOA 写入可直接 send）
bun run tomorrowdao_skill.ts token approve --input '{"chainId":"tDVV","args":{"spender":"<SPENDER_ADDRESS>","symbol":"AIBOUNTY","amount":200000000}}' --mode simulate

# DAO 撤票
bun run tomorrowdao_skill.ts dao withdraw --input '{"args":{"daoId":"<DAO_ID>","withdrawAmount":100000000,"proposalId":"<PROPOSAL_ID>"}}' --mode send

# Network Governance
bun run tomorrowdao_skill.ts network proposal-create --input '{"proposalType":"Parliament","args":{...}}' --mode send

# BP
bun run tomorrowdao_skill.ts bp apply --input '{"args":{...}}' --mode send

# Resource
bun run tomorrowdao_skill.ts resource buy --input '{"symbol":"CPU","amount":100000000}' --mode send
```

### MCP

```bash
bun run src/mcp/server.ts
```

可参考 [mcp-config.example.json](./mcp-config.example.json)：

```json
{
  "mcpServers": {
    "tomorrowdao-agent-skills": {
      "command": "bun",
      "args": ["run", "/ABSOLUTE/PATH/TO/src/mcp/server.ts"],
      "env": {
        "TMRW_PRIVATE_KEY": "<YOUR_PRIVATE_KEY>",
        "TMRW_API_BASE": "https://api.tmrwdao.com",
        "TMRW_CHAIN_DEFAULT_DAO": "tDVV",
        "TMRW_CHAIN_DEFAULT_NETWORK": "AELF"
      }
    }
  }
}
```

写操作 signer 解析顺序：

1. 显式输入（`privateKey` 或 `signer` 对象）
2. active wallet context（`~/.portkey/skill-wallet/context.v1.json`）
3. 环境变量回退（`TMRW_PRIVATE_KEY` -> `AELF_PRIVATE_KEY` -> `PORTKEY_PRIVATE_KEY`）

如果 send 模式最终解析到的是 `CA` 身份，这个 skill 会直接返回 `SIGNER_CA_DIRECT_SEND_FORBIDDEN`，不会继续直发目标合约。`CA` keystore 虽然会解锁 manager key，但真正的 `CA` 写操作仍然必须走显式的 CA forward transport。

`signerMode=daemon` 仅预埋接口，本轮返回 `SIGNER_DAEMON_NOT_IMPLEMENTED`。

### OpenClaw

```bash
bun run build:openclaw
bun run build:openclaw:check
```

### SDK

```ts
import { daoCreate, daoVote, networkProposalCreate } from '@tomorrowdao/agent-skills';

const daoRes = await daoCreate({
  chainId: 'tDVV',
  mode: 'simulate',
  args: { metadata: { name: 'hello codex' } },
});

const voteRes = await daoVote({
  chainId: 'tDVV',
  mode: 'simulate',
  args: { proposalId: 'proposal-hash', voteOption: 0, voteAmount: 100000000 },
});

const proposalRes = await networkProposalCreate({
  chainId: 'AELF',
  proposalType: 'Parliament',
  mode: 'simulate',
  args: { title: 'demo', description: 'demo' },
});
```

## MCP 工具（共 45 个）

### DAO（13）
- `tomorrowdao_dao_create`
- `tomorrowdao_dao_update_metadata`
- `tomorrowdao_dao_upload_files`
- `tomorrowdao_dao_remove_files`
- `tomorrowdao_dao_proposal_create`
- `tomorrowdao_dao_vote`
- `tomorrowdao_dao_withdraw`
- `tomorrowdao_dao_execute`
- `tomorrowdao_discussion_list`
- `tomorrowdao_discussion_comment`
- `tomorrowdao_dao_proposal_my_info`
- `tomorrowdao_dao_token_allowance_view`
- `tomorrowdao_dao_token_balance_view`

### Token（3）
- `tomorrowdao_token_allowance_view`
- `tomorrowdao_token_approve`
- `tomorrowdao_token_balance_view`

### Network Governance（13）
- `tomorrowdao_network_proposals_list`
- `tomorrowdao_network_proposal_get`
- `tomorrowdao_network_proposal_create`
- `tomorrowdao_network_proposal_vote`
- `tomorrowdao_network_proposal_release`
- `tomorrowdao_network_org_create`
- `tomorrowdao_network_org_list`
- `tomorrowdao_network_contract_name_check`
- `tomorrowdao_network_contract_name_add`
- `tomorrowdao_network_contract_name_update`
- `tomorrowdao_network_contract_flow_start`
- `tomorrowdao_network_contract_flow_release`
- `tomorrowdao_network_contract_flow_status`

### BP（11）
- `tomorrowdao_bp_apply`
- `tomorrowdao_bp_quit`
- `tomorrowdao_bp_vote`
- `tomorrowdao_bp_withdraw`
- `tomorrowdao_bp_change_vote`
- `tomorrowdao_bp_claim_profits`
- `tomorrowdao_bp_votes_list`
- `tomorrowdao_bp_team_desc_get`
- `tomorrowdao_bp_team_desc_list`
- `tomorrowdao_bp_team_desc_add`
- `tomorrowdao_bp_vote_reclaim`

### Resource（5）
- `tomorrowdao_resource_buy`
- `tomorrowdao_resource_sell`
- `tomorrowdao_resource_realtime_records`
- `tomorrowdao_resource_turnover`
- `tomorrowdao_resource_records`

## 网络与能力范围

- 支持链：`AELF`、`tDVV`
- Network Governance / BP / Resource 的写操作仅支持 `AELF`
- DAO 默认 `tDVV`，可显式传 `chainId`

## 合约地址策略

- `src/core/config.ts` 中 DAO/Network 系统合约地址当前为有意硬编码默认值。
- 这是团队已确认的主网设计选择：这些地址按“长期稳定的系统合约”处理。
- 如未来要支持 testnet/devnet 覆盖，再通过独立 feature 分支引入 override，避免影响当前主网行为。

## 兼容层说明

- `lib/*` 文件用于兼容旧版 import 路径（re-export）。
- 新接入建议优先使用包根导出（`index.ts`）。
- `signature.ts` 中 `buildLegacyTimestampSignature`、`getAuthSigningMessage` 保留为公开兼容 API（legacy）。

## 测试

```bash
bun run test:unit
bun run test:integration
bun run test:e2e
bun run test:coverage

# 覆盖率门禁（仅统计 src/**，默认：lines>=80, funcs>=75）
bun run test:coverage:gate
COVERAGE_MIN_LINES=85 COVERAGE_MIN_FUNCS=80 bun run test:coverage:ci

# 真实只读 e2e（公网 API）
RUN_TMRW_E2E=1 bun run test:e2e
```

### IronClaw Smoke Test

1. 执行 `bun run setup ironclaw`
2. 先问一个只读问题，比如 `list the latest TomorrowDAO network proposals`
3. 再问一个写操作，比如 `create a TomorrowDAO proposal in simulate mode`
4. 再问一个治理写操作，比如 `vote on this TomorrowDAO proposal`
5. 确认 DAO/治理类 prompt 命中这个 skill，而 wallet 或 dex prompt 不会误路由过来

## 安全建议

- 不要在日志和对话里暴露私钥。
- 先用 `simulate` 预检，再切到 `send`。
- 主网验收时优先用最小额度/最小影响操作。

## License

MIT
