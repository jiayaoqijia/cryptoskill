# Portkey CA Agent Skills

> [Portkey Wallet](https://portkey.finance) 的 AI Agent 工具包，基于 [aelf](https://aelf.com) 区块链 — 支持 Email 注册/登录、转账、Guardian 管理和通用合约调用。

[English](./README.md)
[![Unit Tests](https://github.com/Portkey-Wallet/ca-agent-skills/actions/workflows/test.yml/badge.svg)](https://github.com/Portkey-Wallet/ca-agent-skills/actions/workflows/test.yml)
[![Coverage](https://img.shields.io/endpoint?url=https://Portkey-Wallet.github.io/ca-agent-skills/coverage.json)](https://Portkey-Wallet.github.io/ca-agent-skills/coverage.json)

## 架构

```
ca-agent-skills/
├── index.ts                    # SDK 入口 — 供 LangChain / LlamaIndex 直接 import
├── src/
│   ├── core/                   # 纯业务逻辑（无副作用）
│   │   ├── account.ts          # 账户查询
│   │   ├── auth.ts             # 注册/登录/验证
│   │   ├── assets.ts           # 资产查询（Token、NFT、价格）
│   │   ├── transfer.ts         # 同链/跨链转账、卡单恢复
│   │   ├── guardian.ts         # Guardian 管理
│   │   ├── contract.ts         # 通用合约调用（view-call / ManagerForwardCall）
│   │   └── keystore.ts         # 钱包加密持久化（save、unlock、lock）
│   └── mcp/
│       └── server.ts           # MCP 适配器 — Claude Desktop / Cursor / GPT
├── portkey_query_skill.ts      # CLI — 查询命令
├── portkey_auth_skill.ts       # CLI — 注册/登录命令
├── portkey_tx_skill.ts         # CLI — 交易/Guardian 命令
├── bin/setup.ts                # 一键配置工具
└── lib/                        # 基础设施（config、types、aelf-sdk 封装、HTTP 客户端）
```

**核心模式：** 三个适配器（MCP / CLI / SDK）调用同一套 Core 函数，零重复逻辑。

## 功能清单

| # | 分类 | 功能 | MCP Tool | SDK 函数 |
|---|------|------|----------|----------|
| 1 | 账户 | 检查 Email 是否注册 | `portkey_check_account` | `checkAccount` |
| 2 | 账户 | 获取 Guardian 列表 | `portkey_get_guardian_list` | `getGuardianList` |
| 3 | 账户 | 获取 CA Holder 信息 | `portkey_get_holder_info` | `getHolderInfo` |
| 4 | 账户 | 获取链信息 | `portkey_get_chain_info` | `getChainInfo` |
| 5 | 验证 | 获取 Verifier | `portkey_get_verifier` | `getVerifierServer` |
| 6 | 验证 | 发送验证码 | `portkey_send_code` | `sendVerificationCode` |
| 7 | 验证 | 校验验证码 | `portkey_verify_code` | `verifyCode` |
| 8 | 注册 | 注册 CA 钱包 | `portkey_register` | `registerWallet` |
| 9 | 登录 | 恢复/登录 CA 钱包 | `portkey_recover` | `recoverWallet` |
| 10 | 状态 | 查询注册/恢复状态 | `portkey_check_status` | `checkRegisterOrRecoveryStatus` |
| 11 | 资产 | 查询 Token 余额 | `portkey_balance` | `getTokenBalance` |
| 12 | 资产 | Token 列表 | `portkey_token_list` | `getTokenList` |
| 13 | 资产 | NFT 集合 | `portkey_nft_collections` | `getNftCollections` |
| 14 | 资产 | NFT 项目 | `portkey_nft_items` | `getNftItems` |
| 15 | 资产 | Token 价格 | `portkey_token_price` | `getTokenPrice` |
| 16 | 转账 | 同链转账 | `portkey_transfer` | `sameChainTransfer` |
| 17 | 转账 | 跨链转账 | `portkey_cross_chain_transfer` | `crossChainTransfer` |
| 18 | 转账 | 查询交易结果 | `portkey_tx_result` | `getTransactionResult` |
| 19 | 转账 | 跨链卡单恢复 | `portkey_recover_stuck_transfer` | `recoverStuckTransfer` |
| 20 | Guardian | 添加 Guardian | `portkey_add_guardian` | `addGuardian` |
| 21 | Guardian | 移除 Guardian | `portkey_remove_guardian` | `removeGuardian` |
| 22 | 合约 | 通用 ManagerForwardCall | `portkey_forward_call` | `managerForwardCall` |
| 23 | 合约 | 只读合约调用 | `portkey_view_call` | `callContractViewMethod` |
| 24 | 钱包 | 创建钱包 | `portkey_create_wallet` | `createWallet` |
| 25 | 钱包 | 保存 Keystore | `portkey_save_keystore` | `saveKeystore` |
| 26 | 钱包 | 解锁钱包 | `portkey_unlock` | `unlockWallet` |
| 27 | 钱包 | 锁定钱包 | `portkey_lock` | `lockWallet` |
| 28 | 钱包 | 钱包状态 | `portkey_wallet_status` | `getWalletStatus` |
| 29 | 钱包 | 读取 active wallet context | `portkey_get_active_wallet` | `getActiveWallet` |
| 30 | 钱包 | 设置 active wallet context | `portkey_set_active_wallet` | `setActiveWallet` |
| 31 | 钱包 | Manager 同步状态 | `portkey_manager_sync_status` | `checkManagerSyncState` |

## 合约调用路由规则

合约工具要按方法类型选，不要只看是不是 CA 钱包。

- `forward-call` / `managerForwardCall` 只用于 state-changing 方法。
- `view-call` / `callContractViewMethod` 才用于 `Get*` 和其它 read-only 方法。
- 对 `GetConfig` 这类 `Empty` 入参的 view 方法，要直接省略 `--params`，让工具走不带参数的 `.call()`。
- 如果把 read-only 方法拿去走 `forward-call`，拿到的是 `CA.ManagerForwardCall` 的交易回执语义，不是 inner method 的 view 返回值。
- `VirtualTransactionCreated` 出现在 forwarded write 回执里是正常的。它只说明 CA 合约创建了 inner call，不是解码后的返回值，也不能单独证明最终业务成功。

Resonance 示例：

```bash
# 只读查询排队状态
bun run portkey_query_skill.ts view-call \
  --rpc-url https://tdvv-public-node.aelf.io \
  --contract-address 28Lot71VrWm1WxrEjuDqaepywi7gYyZwHysUcztjkHGFsPPrZy \
  --method-name GetPairQueueStatus \
  --params '"<address>"'

# 发起写操作加入队列
bun run portkey_tx_skill.ts forward-call \
  --login-email "user@example.com" \
  --password "你的密码" \
  --ca-hash "<caHash>" \
  --contract-address 28Lot71VrWm1WxrEjuDqaepywi7gYyZwHysUcztjkHGFsPPrZy \
  --method-name JoinPairQueue \
  --args '{}' \
  --chain-id tDVV
```

## 钱包持久化（Keystore）

Manager 私钥使用 aelf-sdk 内置的 keystore 方案（scrypt + AES-128-CTR）加密存储到本地。

**存储路径：** `~/.portkey/ca/{network}.keystore.json`

### 首次设置（注册/恢复成功后）

```bash
# AI 流程：create_wallet → register → check_status → save_keystore(密码)
# 保存后自动解锁，当前对话可直接使用。
```

### 新对话

```bash
# AI 调用 portkey_wallet_status 检查 active 或指定 profile 的 keystore
# 对 profile keystore，传 --login-email（或依赖之前 save/recover 写入的 active profile）
# 如果已锁定，向用户索要密码 → portkey_unlock(密码)
# 如果忘记密码，切换到 recover-and-save，重新完成 guardian 验证码校验并保存新的 keystore
# 之后写操作自动生效
```

### CLI 手动操作

```bash
# 保存 keystore
bun run portkey_auth_skill.ts save-keystore \
  --password "你的密码" \
  --private-key "hex私钥" \
  --mnemonic "助记词" \
  --ca-hash "xxx" --ca-address "ELF_xxx_tDVV" \
  --origin-chain-id "tDVV"

# 解锁
bun run portkey_auth_skill.ts unlock --password "你的密码"

# 如果忘记密码，重新登录 / 恢复并保存新的可复用 keystore
bun run portkey_auth_skill.ts recover-and-save \
  --email "user@example.com" \
  --guardians-approved '[...]' \
  --chain-id AELF \
  --password "新的密码"

# 查看状态
bun run portkey_auth_skill.ts wallet-status

# 锁定
bun run portkey_auth_skill.ts lock
```

### 工作原理

1. **Save** — 用用户密码加密 Manager 私钥 + 助记词，写入 `~/.portkey/ca/`
2. **Unlock** — 解密 keystore，将钱包加载到进程内存
3. **Lock** — 清除内存中的私钥
4. **写操作** — 优先使用已解锁的钱包；如果没有解锁的 keystore，fallback 到 `PORTKEY_PRIVATE_KEY` 环境变量

### 推荐的 CA 写操作路径

```bash
# 1. recover -> 保存可复用 keystore
bun run portkey_auth_skill.ts recover-and-save \
  --email "user@example.com" \
  --guardians-approved '[...]' \
  --chain-id AELF \
  --password "你的密码"

# 2. 在目标链轮询 manager 是否已同步
bun run portkey_query_skill.ts manager-sync-status \
  --ca-hash "<caHash>" \
  --chain-id tDVV \
  --manager-address "<recover-and-save 返回的 managerAddress，或当前选中的 signer 地址>"

# 3. 收集 fresh transferApprove proofs
# 4. 直接用 loginEmail + password 发起写操作
bun run portkey_tx_skill.ts transfer \
  --login-email "user@example.com" \
  --password "你的密码" \
  --ca-hash "<caHash>" \
  --token-contract "<tokenContract>" \
  --symbol ELF \
  --to "<receiver>" \
  --amount 101000000 \
  --chain-id tDVV \
  --guardians-approved '[...]'
```

- `forward-call` 现在也会像 `transfer` / `cross-chain-transfer` 一样先检查 manager sync，未同步时不会继续做 fee preview 或发交易。
- `wallet-status` 在本地已有 keystore 但未解锁时，会返回 `recommendedAction` 和 `userHint`。`recommendedAction` 是机器可路由的下一步（`unlock`），`userHint` 会补充“先确认 loginEmail / keystoreFile 是否选对；如果忘记密码再走 recover-and-save”的说明。

## 跨 Skill 签名共享

- `portkey_save_keystore` 与 `portkey_unlock` 会自动更新共享 active wallet context。
- 其它写能力 skill 可按 `explicit -> active context -> env` 顺序解析 signer（auto 模式）。
- 共享 context 文件仅保存指针信息，不保存明文私钥。

## 前置条件

- [Bun](https://bun.sh) >= 1.0
- aelf 钱包私钥或已解锁的 keystore（仅写操作需要）

## 快速开始

```bash
# 安装
bun add @portkey/ca-agent-skills

# 配置
cp .env.example .env
# 编辑 .env，添加 PORTKEY_PRIVATE_KEY（仅写操作需要）

# 一键配置到 AI 平台
bun run bin/setup.ts claude          # Claude Desktop
bun run bin/setup.ts cursor          # Cursor（项目级）
bun run bin/setup.ts cursor --global # Cursor（全局）
bun run bin/setup.ts openclaw        # OpenClaw — 输出配置到 stdout
bun run bin/setup.ts openclaw --config-path ./my-openclaw.json  # 合并到已有配置
bun run bin/setup.ts ironclaw        # IronClaw — 安装 trusted skill + stdio MCP server

# 查看配置状态（Claude / Cursor / OpenClaw / IronClaw）
bun run bin/setup.ts list

# 卸载
bun run bin/setup.ts uninstall claude
bun run bin/setup.ts uninstall cursor
bun run bin/setup.ts uninstall openclaw --config-path ./my-openclaw.json
bun run bin/setup.ts uninstall ironclaw
```

### IronClaw

```bash
# 安装 trusted skill + stdio MCP server
bun run bin/setup.ts ironclaw

# 移除 IronClaw 集成
bun run bin/setup.ts uninstall ironclaw
```

IronClaw 默认会做两件事：

- 向 `~/.ironclaw/mcp-servers.json` 写入一个 stdio MCP server
- 把当前仓库的 `SKILL.md` 复制到 `~/.ironclaw/skills/portkey-ca-agent-skills/SKILL.md`

关于 trust model 的重要说明：

- 需要 CA 钱包写操作时，务必使用上面的 trusted skill 路径。
- 如果你把这个包放进 `~/.ironclaw/installed_skills/`，不要期待它还能正常执行注册、恢复、转账、Guardian 管理等写操作。
- IronClaw 会把 installed skill 的工具权限衰减为只读，这会表现成“只能查，不能写”，即使 MCP server 本身是可用的。

当前 MCP server 已为 CA 写操作补齐 destructive annotations，IronClaw 可以据此在注册、恢复、转账、Guardian、合约调用前请求 approval。
为兼容当前 IronClaw 源码，这里的 MCP annotations 会同时输出标准 MCP 的 camelCase 字段和 IronClaw 兼容的 snake_case 字段，因为 IronClaw 目前按 snake_case 解析 MCP approval hints。

远程激活契约：

- GitHub repo/tree URL 只用于 discovery，不是最终的 IronClaw 安装载体。
- 推荐的 IronClaw npm 激活命令：`bunx -p @portkey/ca-agent-skills portkey-ca-setup ironclaw`
- OpenClaw 若有 ClawHub / managed install 则优先使用；否则回退到 `bunx -p @portkey/ca-agent-skills portkey-ca-setup openclaw`
- 本地 repo checkout 仅保留给开发阶段 smoke test。
- 迁移说明：`2.0.0` 起移除了 `portkey-setup`，请改用 `portkey-ca-setup` 执行 npm 激活命令。

## CLI 示例

```bash
# 检查邮箱是否注册
bun run portkey_query_skill.ts check-account --email user@example.com

# 获取链信息
bun run portkey_query_skill.ts chain-info

# 创建钱包
bun run portkey_auth_skill.ts create-wallet

# 先解析推荐流程和链
bun run portkey_query_skill.ts prepare-auth-flow --email user@example.com

# low-level auth 工具必须显式传 prepare-auth-flow 返回的 resolvedChainId
bun run portkey_auth_skill.ts get-verifier --chain-id <resolvedChainId>
bun run portkey_auth_skill.ts send-code --email user@example.com --verifier-id <id> --operation recovery --chain-id <resolvedChainId>
bun run portkey_auth_skill.ts verify-code --email user@example.com --code 123456 --verifier-id <id> --session-id <sid> --operation recovery --chain-id <resolvedChainId>

# Token 列表策略：aa | auto | eoa（默认 auto）
bun run portkey_query_skill.ts token-list --ca-address-infos '[{"chainId":"tDVV","caAddress":"xxx"}]' --strategy auto
```

恢复证明校验：
- `recover` 在提交前会先做本地校验。
- 每个 guardian 的 `verificationDoc` 必须来自 `verify-code --operation recovery`；使用 register 证明会被拒绝。

资产查询策略（`token-list`）：
- `aa`：仅查 AA 接口（`/api/app/user/assets/token`）。
- `auto`（默认）：先查 AA；若返回 `401 Unauthorized` 自动回退到 EOA 接口。
- `eoa`：仅查 EOA 接口。
- 可通过 `PORTKEY_EOA_FALLBACK_ENABLED=false` 关闭自动回退。
- 回退重试可通过 `PORTKEY_EOA_FALLBACK_RETRY_COUNT` 与 `PORTKEY_EOA_FALLBACK_RETRY_DELAY_MS` 配置。
- 回退时会动态读取 EOA `chainsinfoindex` 链列表（当前 mainnet 返回 `AELF`、`tDVV`）。

## SDK 使用示例

```typescript
import { getConfig, checkAccount, createWallet, getTokenBalance } from '@portkey/ca-agent-skills';

const config = getConfig({ network: 'mainnet' });

// 检查账户
const account = await checkAccount(config, { email: 'user@example.com' });
console.log(account.isRegistered, account.originChainId);

// 创建钱包
const wallet = createWallet();
console.log(wallet.address, wallet.privateKey);

// 查询余额
const balance = await getTokenBalance(config, {
  caAddress: 'xxx',
  chainId: 'tDVV',
  symbol: 'ELF',
});
```

## 注册流程示例（Email）

```typescript
import {
  getConfig, createWallet, prepareAuthFlow, getVerifierServer,
  sendVerificationCode, verifyCode, registerWallet,
  checkRegisterOrRecoveryStatus, OperationType,
} from '@portkey/ca-agent-skills';

const config = getConfig({ network: 'mainnet' });

// 1. 先解析推荐流程和链
const authFlow = await prepareAuthFlow(config, {
  email: 'user@example.com',
  network: 'mainnet',
});

// 2. 获取 Verifier
const verifier = await getVerifierServer(config, {
  chainId: authFlow.resolvedChainId,
});

// 3. 发送验证码（注意：mainnet 已废弃 Register(0)，统一使用 CommunityRecovery(1)）
const { verifierSessionId } = await sendVerificationCode(config, {
  email: 'user@example.com',
  verifierId: verifier.id,
  chainId: authFlow.resolvedChainId,
  operationType: OperationType.CreateCAHolder, // 注册用 1，登录用 SocialRecovery(2)
});

// 4. 用户输入验证码后校验
const { signature, verificationDoc } = await verifyCode(config, {
  email: 'user@example.com',
  verificationCode: '123456',
  verifierId: verifier.id,
  verifierSessionId,
  chainId: authFlow.resolvedChainId,
  operationType: OperationType.CreateCAHolder,
});

// 5. 创建 Manager 钱包
const wallet = createWallet();

// 6. 提交注册
const { sessionId } = await registerWallet(config, {
  email: 'user@example.com',
  manager: wallet.address,
  verifierId: verifier.id,
  verificationDoc,
  signature,
  chainId: authFlow.resolvedChainId,
});

// 7. 轮询状态
let status;
do {
  await new Promise(r => setTimeout(r, 3000));
  status = await checkRegisterOrRecoveryStatus(config, { sessionId, type: 'register' });
} while (status.status === 'pending');

console.log('CA Address:', status.caAddress);
console.log('CA Hash:', status.caHash);

// 8. 保存 keystore（加密持久化 Manager 私钥）
import { saveKeystore } from '@portkey/ca-agent-skills';
saveKeystore({
  password: 'user-chosen-password',
  privateKey: wallet.privateKey,
  mnemonic: wallet.mnemonic,
  caHash: status.caHash!,
  caAddress: status.caAddress!,
  originChainId: authFlow.resolvedChainId,
  network: 'mainnet',
});
// 钱包已自动解锁，后续写操作无需再设置 PORTKEY_PRIVATE_KEY
```

## 环境变量

| 变量 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| `PORTKEY_PRIVATE_KEY` | Fallback | — | Manager 钱包私钥（keystore 未解锁时的 fallback） |
| `PORTKEY_CA_KEYSTORE_PASSWORD` | 否 | — | 跨 skill signer 解析时可选的 keystore 密码缓存 |
| `PORTKEY_SKILL_WALLET_CONTEXT_PATH` | 否 | `~/.portkey/skill-wallet/context.v1.json` | 覆盖共享 wallet context 路径 |
| `PORTKEY_NETWORK` | 否 | `mainnet` | 仅支持 `mainnet`，传 `testnet` 会直接报错 |
| `PORTKEY_API_URL` | 否 | 按网络 | 覆盖 API 地址 |
| `PORTKEY_EOA_API_URL` | 否 | 按网络 | 覆盖 token-list 回退使用的 EOA API 地址 |
| `PORTKEY_GRAPHQL_URL` | 否 | 按网络 | 覆盖 GraphQL 地址 |
| `PORTKEY_EOA_FALLBACK_ENABLED` | 否 | `true` | 是否启用 token-list 的 AA -> EOA 自动回退 |
| `PORTKEY_EOA_FALLBACK_RETRY_COUNT` | 否 | `2` | 回退重试次数（包含首次请求） |
| `PORTKEY_EOA_FALLBACK_RETRY_DELAY_MS` | 否 | `200` | 回退重试间隔（毫秒） |

## 测试

```bash
bun test                    # 全部测试
bun run test:unit           # 单元测试
bun run test:integration    # 集成测试（需要网络）
bun run test:e2e            # E2E 测试（需要私钥）
```

### IronClaw Smoke Test

1. 执行 `bun run bin/setup.ts ironclaw`
2. 先问一个只读问题，比如 `show my guardian list for this Portkey CA wallet`
3. 再问一个本地写操作，比如 `create a new Portkey CA wallet`
4. 再问一个链上写操作，比如 `transfer 1 ELF from my CA wallet`
5. 确认 CA 场景会命中这个 skill，而 EOA wallet lifecycle 场景不会误路由过来

## 安全

- `.env` 文件已默认 git-ignore，不要提交
- 私钥仅写操作需要（转账、Guardian 管理、合约调用）
- **Keystore 加密**：Manager 私钥使用 scrypt（N=8192）+ AES-128-CTR 加密，文件权限 `0600`
- **内存生命周期**：私钥仅在 unlock 期间存在于内存，`portkey_lock` 立即清除
- MCP 模式下，keystore 密码仅存在于 AI 对话上下文，不会写入磁盘
- `PORTKEY_PRIVATE_KEY` 环境变量仍然支持作为 fallback，但推荐使用 keystore

## License

MIT
