[中文](SKILL_ROUTING_MATRIX.zh-CN.md) | English

# Skill Routing Matrix (Intent -> Skill)

Use this matrix to route user intents across multiple skills.

## 1. General routing table

| User Intent | Recommended Skill | Alternative Skill | Selection Rule |
|---|---|---|---|
| Wallet lifecycle, asset query, transfer | `portkey-eoa-agent-skills` | `portkey-ca-agent-skills` | Default to EOA; switch to CA when CA identity/guardian flow is required |
| CA registration/recovery/guardian/CA identity tx | `portkey-ca-agent-skills` | `portkey-eoa-agent-skills` | If CA status or guardian flow is involved, choose CA |
| Chain status/block/tx details, contract view/send | `aelf-node-skill` | `aelfscan-skill` | Prefer aelf-node for direct node capabilities or send workflows |
| Explorer analytics on address/token/NFT/statistics | `aelfscan-skill` | `aelf-node-skill` | Prefer aelfscan for aggregated explorer analytics |
| DEX quote/swap/liquidity | `awaken-agent-skills` | `portkey-eoa-agent-skills` or `portkey-ca-agent-skills` | Trade execution depends on wallet skill as signer source |
| eForest token/NFT marketplace actions | `eforest-agent-skills` | `portkey-eoa-agent-skills` or `portkey-ca-agent-skills` | eForest handles domain actions, wallet skills provide signing identity |
| TomorrowDAO governance/BP/resource operations | `tomorrowdao-agent-skills` | `portkey-ca-agent-skills` | Use tomorrowdao for governance domain; wallet skills supplement identity management |

## 2. Key ambiguity decisions

### 2.1 `portkey-eoa` vs `portkey-ca`

1. Default to `portkey-eoa-agent-skills`.
2. Switch to `portkey-ca-agent-skills` when these signals appear:
- `CA wallet`
- `guardian`
- `register/recover`
- `CA hash / CA address`

### 2.2 `aelf-node` vs `aelfscan`

1. Choose `aelf-node-skill` for raw chain interaction (node read/send/fee/view).
2. Choose `aelfscan-skill` for explorer-level analytics and search.
3. For “analyze then verify” tasks, use `aelfscan` first, then `aelf-node`.

### 2.3 wallet skill composition with `awaken/eforest`

1. `awaken-agent-skills` and `eforest-agent-skills` handle domain operations.
2. Signing identity should come from wallet skills:
- standard private key flows: `portkey-eoa-agent-skills`
- CA identity flows: `portkey-ca-agent-skills`

### 2.4 shared active wallet context (cross-skill signing)

1. After wallet creation/unlock, wallet skills should update active context at `~/.portkey/skill-wallet/context.v1.json`.
2. Consumer write skills (`awaken`, `eforest`, `tomorrowdao`, `aelf-node`) should resolve signer in fixed order:
- explicit input
- active context
- env fallback
3. If context points to encrypted wallet/keystore, require password from tool input or password env.
4. `signerMode=daemon` is reserved for future rollout and should return a structured not-implemented error in current wave.

### 2.5 signer env priority matrix

| Skill | Env priority (high -> low) | Notes |
|---|---|---|
| `portkey-eoa-agent-skills` | `PORTKEY_PRIVATE_KEY` | Context/password path preferred when active wallet is available |
| `portkey-ca-agent-skills` | `PORTKEY_PRIVATE_KEY` + `PORTKEY_CA_HASH` + `PORTKEY_CA_ADDRESS` | CA tuple required for CA signer from env |
| `tomorrowdao-agent-skills` | `TMRW_PRIVATE_KEY` -> `AELF_PRIVATE_KEY` -> `PORTKEY_PRIVATE_KEY` | Context path checked before env in auto mode |
| `aelf-node-skill` | `AELF_PRIVATE_KEY` -> `PORTKEY_PRIVATE_KEY` | Context path checked before env in auto mode |
| `awaken-agent-skills` | `PORTKEY_PRIVATE_KEY` (CA) / `AELF_PRIVATE_KEY` (EOA legacy) | Context/password path preferred in signerMode=auto |
| `eforest-agent-skills` | `PORTKEY_PRIVATE_KEY` (CA) / `AELF_PRIVATE_KEY` (EOA legacy) | Context/password path preferred in signerMode=auto |

### 2.6 wallet-context schema

Canonical schema: `docs/schemas/wallet-context.v1.schema.json`.  
Each skill repo mirrors this schema under `schemas/wallet-context.v1.schema.json` and validates it in `deps:check`.

## 3. Fallback strategy

1. If intent is ambiguous, start with read-only operations to gather context.
2. Before any write action, confirm identity mode (EOA/CA) and network settings.
3. If still ambiguous, return “recommended + alternative + reason” instead of forcing a single choice.

Recommended output format:
```text
Recommended: <skill-id>
Alternative: <skill-id>
Reason: <why recommended path is preferred under current signals>
```

Example (EOA/CA ambiguity):
```text
Recommended: portkey-eoa-agent-skills
Alternative: portkey-ca-agent-skills
Reason: No CA/guardian signals detected; default to EOA path.
```
