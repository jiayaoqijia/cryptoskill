# @tomorrowdao/agent-skills

[中文版](./README.zh-CN.md) | English

[![Unit Tests](https://github.com/TomorrowDAOProject/tomorrowDAO-skill/actions/workflows/test.yml/badge.svg)](https://github.com/TomorrowDAOProject/tomorrowDAO-skill/actions/workflows/test.yml)
[![Coverage](https://img.shields.io/endpoint?url=https://TomorrowDAOProject.github.io/tomorrowDAO-skill/coverage.json)](https://TomorrowDAOProject.github.io/tomorrowDAO-skill/coverage.json)

TomorrowDAO AI agent skill toolkit on aelf, with **MCP + OpenClaw + CLI + SDK** interfaces.

## Features

- DAO: create DAO, update metadata, create/vote/withdraw/execute proposal, discussion APIs
- Token helpers: balance view, allowance view, approve payload/send helper
- DAO read helpers: proposal my-info, DAO token allowance view alias, DAO token balance view alias
- Network governance: proposal create/vote/release, organization create, contract-name management, contract-flow actions
- BP election: apply, quit, vote, withdraw, change vote, claim profits, team description updates
- Resource: buy/sell resource token and query market records
- Unified result model: `ToolResult<T>` and `TxReceipt`
- Execution mode: `simulate` (default) and `send`

## Consumption Modes

| Mode | Entry | Use Case |
|------|------|------|
| MCP | `src/mcp/server.ts` | Claude Desktop, Cursor, GPT and other MCP clients |
| CLI | `tomorrowdao_skill.ts` | terminal scripts, OpenClaw |
| SDK | `index.ts` | custom agents, LangChain/LlamaIndex integrations |

## Architecture

```text
tomorrowDAO-skill/
├── index.ts                # SDK exports
├── tomorrowdao_skill.ts    # CLI adapter
├── src/
│   ├── core/               # config/auth/http/chain/tx/error/types
│   ├── domains/            # dao/token/network/bp/resource
│   └── mcp/server.ts       # MCP adapter
├── lib/                    # compatibility re-exports
├── bin/setup.ts            # setup for claude/cursor/openclaw/ironclaw
├── openclaw.json
├── mcp-config.example.json
└── tests/                  # unit/integration/e2e
```

## Quick Start

### Install

```bash
bun install
```

### Configure Env

```bash
cp .env.example .env
# fill network config and optional signer fallback values
```

### One-Click Setup

```bash
# Claude Desktop
bun run setup claude

# Cursor (project-level)
bun run setup cursor

# Cursor (global)
bun run setup cursor --global

# OpenClaw (print config)
bun run setup openclaw

# OpenClaw (merge into existing config)
bun run setup openclaw --config-path /path/to/openclaw-config.json

# IronClaw (install trusted skill + stdio MCP server)
bun run setup ironclaw

# Check setup status
bun run setup list

# Remove IronClaw integration
bun run setup uninstall ironclaw
```

### IronClaw

```bash
# Install trusted skill + stdio MCP server
bun run setup ironclaw

# Remove IronClaw integration
bun run setup uninstall ironclaw
```

The IronClaw setup does two things by default:

- Writes a stdio MCP server entry to `~/.ironclaw/mcp-servers.json`
- Copies this repo's `SKILL.md` to `~/.ironclaw/skills/tomorrowdao-agent-skills/SKILL.md`

Important trust model note:

- Use the trusted skill path above for DAO, BP, governance, and resource write operations.
- Do **not** rely on `~/.ironclaw/installed_skills/` for this package if you need proposal creation, voting, release, BP actions, or resource trading.
- IronClaw attenuates installed skills to read-only tools, which can make the agent appear to "query only" even though the MCP server is available.

The MCP server exposes destructive annotations for write operations so IronClaw can request approval before DAO, governance, BP, and resource state changes.
For compatibility, the MCP server currently emits both standard MCP camelCase annotations and IronClaw-compatible snake_case annotations because the current IronClaw source parses snake_case fields for MCP approval hints.

Remote activation contract:

- GitHub repo/tree URLs are discovery sources only, not the final IronClaw install payload.
- Preferred IronClaw activation from npm: `bunx -p @tomorrowdao/agent-skills tomorrowdao-setup ironclaw`
- Prefer ClawHub / managed install for OpenClaw when available; otherwise use `bunx -p @tomorrowdao/agent-skills tomorrowdao-setup openclaw`
- Local repo checkout remains a development smoke-test path only.

## Environment Variables

| Variable | Required | Default | Description |
|------|------|------|------|
| `TMRW_API_BASE` | No | `https://api.tmrwdao.com` | TomorrowDAO API base URL |
| `TMRW_AUTH_BASE` | No | `https://api.tmrwdao.com` | Auth server base URL |
| `TMRW_CHAIN_DEFAULT_DAO` | No | `tDVV` | Default DAO chain |
| `TMRW_CHAIN_DEFAULT_NETWORK` | No | `AELF` | Default network governance chain |
| `TMRW_AUTH_CHAIN_ID` | No | `AELF` | Chain id used in auth signature grant |
| `TMRW_PRIVATE_KEY` | No (env fallback for `send`/auth) | — | Signer private key fallback |
| `AELF_PRIVATE_KEY` | No | — | Secondary signer fallback for shared-skill compatibility |
| `PORTKEY_PRIVATE_KEY` | No | — | Third signer fallback for shared-skill compatibility |
| `PORTKEY_WALLET_PASSWORD` | No | — | Optional password cache for EOA wallet context |
| `PORTKEY_CA_KEYSTORE_PASSWORD` | No | — | Optional password cache for CA keystore context |
| `PORTKEY_SKILL_WALLET_CONTEXT_PATH` | No | `~/.portkey/skill-wallet/context.v1.json` | Override active wallet context path |
| `TMRW_SOURCE` | No | `nightElf` | Auth `source` field |
| `TMRW_CA_HASH` | No | — | Optional auth `ca_hash` |
| `TMRW_RPC_AELF` | No | `https://aelf-public-node.aelf.io` | AELF RPC endpoint |
| `TMRW_RPC_TDVV` | No | `https://tdvv-public-node.aelf.io` | tDVV RPC endpoint |
| `TMRW_HTTP_TIMEOUT_MS` | No | `10000` | HTTP timeout in milliseconds |
| `TMRW_HTTP_RETRY_MAX` | No | `1` | Max retry count for retryable HTTP requests |
| `TMRW_HTTP_RETRY_BASE_MS` | No | `200` | Retry base backoff milliseconds |
| `TMRW_HTTP_RETRY_POST` | No | `0` | Retry POST when set to `1/true` |
| `TMRW_AELF_CACHE_MAX` | No | `8` | Max cached AElf client instances in long-lived process |
| `TMRW_LOG_LEVEL` | No | `error` | Structured logger level (`error/warn/info/debug`) |

## Usage

### CLI

```bash
# DAO
bun run tomorrowdao_skill.ts dao create --input '{"args":{"metadata":{"name":"demo"}}}' --mode simulate

# DAO vote (proposalId and votingItemId are interchangeable DAO hash aliases)
bun run tomorrowdao_skill.ts dao vote --input '{"args":{"proposalId":"<PROPOSAL_ID>","voteOption":0,"voteAmount":100000000}}' --mode send

# DAO token balance view
bun run tomorrowdao_skill.ts dao token-balance-view --input '{"chainId":"tDVV","symbol":"AIBOUNTY","owner":"<OWNER_ADDRESS>"}'

# Generic token balance view
bun run tomorrowdao_skill.ts token balance-view --input '{"chainId":"tDVV","symbol":"AIBOUNTY","owner":"<OWNER_ADDRESS>"}'

# Generic token allowance view
bun run tomorrowdao_skill.ts token allowance-view --input '{"chainId":"tDVV","symbol":"AIBOUNTY","owner":"<OWNER_ADDRESS>","spender":"<SPENDER_ADDRESS>"}'

# Generic token approve (simulate for CA-forward orchestration, send for EOA flows)
bun run tomorrowdao_skill.ts token approve --input '{"chainId":"tDVV","args":{"spender":"<SPENDER_ADDRESS>","symbol":"AIBOUNTY","amount":200000000}}' --mode simulate

# DAO withdraw
bun run tomorrowdao_skill.ts dao withdraw --input '{"args":{"daoId":"<DAO_ID>","withdrawAmount":100000000,"proposalId":"<PROPOSAL_ID>"}}' --mode send

# Network governance
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

Use [mcp-config.example.json](./mcp-config.example.json) as template:

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

Write operations resolve signer in this order:

1. explicit input (`privateKey` or `signer` object)
2. active wallet context (`~/.portkey/skill-wallet/context.v1.json`)
3. env fallback (`TMRW_PRIVATE_KEY` -> `AELF_PRIVATE_KEY` -> `PORTKEY_PRIVATE_KEY`)

If send mode resolves a `CA` identity, this skill stops with `SIGNER_CA_DIRECT_SEND_FORBIDDEN` instead of sending directly to the target contract. A `CA` keystore may unlock the manager key, but real `CA` writes must still go through an explicit CA forward transport.

`signerMode=daemon` is pre-wired and currently returns `SIGNER_DAEMON_NOT_IMPLEMENTED`.

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

## MCP Tools (45)

### DAO (13)
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

### Token (3)
- `tomorrowdao_token_allowance_view`
- `tomorrowdao_token_approve`
- `tomorrowdao_token_balance_view`

### Network Governance (13)
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

### BP (11)
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

### Resource (5)
- `tomorrowdao_resource_buy`
- `tomorrowdao_resource_sell`
- `tomorrowdao_resource_realtime_records`
- `tomorrowdao_resource_turnover`
- `tomorrowdao_resource_records`

## Network Scope

- Supported chains: `AELF`, `tDVV`
- Network governance/BP/resource write operations are `AELF` only
- DAO defaults to `tDVV` unless `chainId` is explicitly set

## Contract Address Policy

- DAO/Network system contract addresses in `src/core/config.ts` are intentionally hardcoded defaults.
- This is a deliberate mainnet design choice confirmed by the team: these addresses are treated as long-term stable system contracts.
- If testnet/devnet override is required in future, introduce it in a dedicated feature branch to avoid changing current mainnet behavior.

## Compatibility Layer

- `lib/*` files are compatibility re-exports for older import paths.
- New integrations should prefer `index.ts` exports from package root.
- Legacy helpers in `signature.ts` (`buildLegacyTimestampSignature`, `getAuthSigningMessage`) are kept as public backward-compatible APIs.

## Testing

```bash
bun run test:unit
bun run test:integration
bun run test:e2e
bun run test:coverage

# coverage gate (src-only, default: lines>=80, funcs>=75)
bun run test:coverage:gate
COVERAGE_MIN_LINES=85 COVERAGE_MIN_FUNCS=80 bun run test:coverage:ci

# run real read-only e2e against public APIs
RUN_TMRW_E2E=1 bun run test:e2e
```

### IronClaw Smoke Test

1. Run `bun run setup ironclaw`
2. Ask a read prompt like `list the latest TomorrowDAO network proposals`
3. Ask a network write prompt like `create a TomorrowDAO proposal in simulate mode`
4. Ask a governance write prompt like `vote on this TomorrowDAO proposal`
5. Confirm DAO/governance prompts stay on this skill and wallet or dex prompts do not

## Security

- Never expose private keys in logs/messages.
- Use `simulate` first for pre-check, then switch to `send`.
- For acceptance on mainnet, use minimal value operations first.

## License

MIT
