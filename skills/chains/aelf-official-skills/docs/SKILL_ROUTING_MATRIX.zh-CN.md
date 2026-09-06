中文 | [English](SKILL_ROUTING_MATRIX.md)

# Skill 路由矩阵（Intent -> Skill）

用于指导 AI 在多 skill 之间做路由决策。

## 1. 通用路由表

| 用户意图 | 推荐 Skill | 备选 Skill | 选择规则 |
|---|---|---|---|
| 创建/管理钱包、查询资产、转账 | `portkey-eoa-agent-skills` | `portkey-ca-agent-skills` | 默认 EOA；需要 CA 身份/guardian 流程时改用 CA |
| CA 注册/恢复/guardian/CA 身份交易 | `portkey-ca-agent-skills` | `portkey-eoa-agent-skills` | 只要涉及 CA 身份状态或 guardian，优先 CA |
| 查询链状态/区块/交易详情、合约 view/send | `aelf-node-skill` | `aelfscan-skill` | 需要链节点直接能力或 send 流程，优先 aelf-node |
| 浏览器统计/地址/Token/NFT 分析 | `aelfscan-skill` | `aelf-node-skill` | 需要 explorer 聚合统计时优先 aelfscan |
| DEX 报价、swap、流动性 | `awaken-agent-skills` | `portkey-eoa-agent-skills` 或 `portkey-ca-agent-skills` | 交易执行依赖钱包能力，钱包 skill 作为 signer 来源 |
| eForest token/NFT 市场操作 | `eforest-agent-skills` | `portkey-eoa-agent-skills` 或 `portkey-ca-agent-skills` | eForest 负责业务动作，钱包 skill 负责签名身份 |
| TomorrowDAO 治理/BP/资源操作 | `tomorrowdao-agent-skills` | `portkey-ca-agent-skills` | 治理业务优先 tomorrowdao，身份管理由钱包 skill 补充 |

## 2. 重点歧义决策

### 2.1 `portkey-eoa` vs `portkey-ca`

1. 默认选择 `portkey-eoa-agent-skills`。
2. 出现以下关键词时切换到 `portkey-ca-agent-skills`：
- `CA wallet`
- `guardian`
- `register/recover`
- `CA hash / CA address`

### 2.2 `aelf-node` vs `aelfscan`

1. 需要原始链交互（node read/send/fee/view）选 `aelf-node-skill`。
2. 需要浏览器聚合统计与多维检索选 `aelfscan-skill`。
3. 若用户问题是“先统计后验证”，可先 `aelfscan` 再 `aelf-node`。

### 2.3 `awaken/eforest` 与钱包 skill 组合

1. `awaken-agent-skills` 与 `eforest-agent-skills` 处理业务域动作。
2. 交易签名身份由钱包 skill 提供：
- 普通私钥场景：`portkey-eoa-agent-skills`
- CA 身份场景：`portkey-ca-agent-skills`

### 2.4 共享 active wallet context（跨 skill 签名）

1. 钱包创建/解锁后，由钱包 skill 写入 active context：`~/.portkey/skill-wallet/context.v1.json`。
2. 消费写操作 skill（`awaken`、`eforest`、`tomorrowdao`、`aelf-node`）统一按顺序解析 signer：
- 显式输入
- active context
- 环境变量回退
3. 若 context 指向加密钱包/keystore，要求工具入参密码或密码 env。
4. `signerMode=daemon` 为下一轮预埋，本轮返回结构化 not-implemented 错误。

### 2.5 signer env 优先级矩阵

| Skill | Env 优先级（高 -> 低） | 说明 |
|---|---|---|
| `portkey-eoa-agent-skills` | `PORTKEY_PRIVATE_KEY` | 有 active wallet 时优先 context/password |
| `portkey-ca-agent-skills` | `PORTKEY_PRIVATE_KEY` + `PORTKEY_CA_HASH` + `PORTKEY_CA_ADDRESS` | CA env 需三元组 |
| `tomorrowdao-agent-skills` | `TMRW_PRIVATE_KEY` -> `AELF_PRIVATE_KEY` -> `PORTKEY_PRIVATE_KEY` | `auto` 模式先 context 再 env |
| `aelf-node-skill` | `AELF_PRIVATE_KEY` -> `PORTKEY_PRIVATE_KEY` | `auto` 模式先 context 再 env |
| `awaken-agent-skills` | `PORTKEY_PRIVATE_KEY`（CA）/ `AELF_PRIVATE_KEY`（EOA 兼容） | `signerMode=auto` 优先 context/password |
| `eforest-agent-skills` | `PORTKEY_PRIVATE_KEY`（CA）/ `AELF_PRIVATE_KEY`（EOA 兼容） | `signerMode=auto` 优先 context/password |

### 2.6 wallet-context schema

Canonical schema：`docs/schemas/wallet-context.v1.schema.json`。  
各 skill 仓镜像到 `schemas/wallet-context.v1.schema.json`，并在 `deps:check` 中做校验。

## 3. 路由兜底策略

1. 当意图不明确时，先用只读能力收集上下文（quote/query/status）。
2. 写操作前必须确认身份模式（EOA/CA）与网络配置。
3. 无法判定时给出“推荐 + 备选 + 原因”三段式回答，而不是强行单选。

推荐输出格式：
```text
Recommended: <skill-id>
Alternative: <skill-id>
Reason: <why recommended path is preferred under current signals>
```

示例（EOA/CA 分歧）：
```text
Recommended: portkey-eoa-agent-skills
Alternative: portkey-ca-agent-skills
Reason: No CA/guardian signals detected; default to EOA path.
```
