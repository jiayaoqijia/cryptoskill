---
name: bnbagent-studio-wiring-llm-tools
description: When the user wants their agent's LLM to call read-only chain queries (wallet balance, ERC-8004 agent info, ERC-8183 job status, etc.) - exposes the 15 functions in `@bnbagent/studio-runtime/tools` as LLM tools via AI SDK `tool()` wrappers, or any other TS agent framework.
---

> **Reference file** of the `bnbagent-studio` router skill - installed at `bnbagent-studio/references/` and loaded on demand (not a standalone skill). Route here via the router's decision tree.

# bnbagent-studio-wiring-llm-tools

Wire `bnbagent-studio`'s 15 chain readonly functions into the user's agent so the LLM can autonomously query wallet, balance, ERC-8004 identity, ERC-8183 jobs, etc. Studio ships the pure functions plus two emitted wrapper files: the runtime recipe's curated default (`app/agent/src/tools.ts`, `LLM_READ_TOOLS`) and the full-inventory `tools-chain` recipe (`tools-chain/code/{{PKG}}/chainTools.ts.tmpl`, emitted as `app/agent/src/chainTools.ts`); for a non-AI-SDK framework you (Claude Code) write a thin wrapping file in the Agent sub-project.

In v1 the workspace contains one sub-project, `app/agent/` - the single selected-faces seller runtime. LLM tools always live in **`app/agent/src/tools.ts`**. The `{{PKG}}` recipe variable resolves to the agent's `src/` dir, so the emit target is `app/agent/src/tools.ts` - its meaning is "source dir of the agent sub-project", not "package inside a single-root project".

## Audience

Claude Code (or another agent) editing the user's workspace. The user has run `bag init` and wants their Agent sub-project to expose read-only chain queries to its LLM (`app/agent/src/tools.ts`). These are READ-ONLY - the Agent's signing always stays in `app/agent/src/signing.ts` (fixed code), never an LLM tool.

## When to use this skill

- The user says "let my agent query its balance" / "agent should know about its on-chain jobs" / "give the LLM access to chain state"
- The user wants to wire chain tools into a **non-AI-SDK** stack (LangChain.js, a bare OpenAI/Anthropic SDK tool loop, custom)
- The user wants to **customize** which chain queries their LLM sees
- The user uses `bag init` but wants to extend / re-emit the tool list

## When NOT to use this skill

- The user wants the Agent to **sign transactions / pay** - in the single seller model all signing (quote-sign, submit, settle) is FIXED code in `app/agent/src/signing.ts` (called by A2A's `SellerAgentExecutor` or MCP's `src/mcpMain.ts` tools), **never** an LLM-callable tool. The LLM only produces work text after a job is verified funded; fixed code resolves the canonical price/asset, signs, and submits. There is no "wire a signing tool into the LLM" path in v1.
- The user is doing dev-time debugging via Claude Code - that's the `bag` CLI read commands (`bag wallet`, `bag erc8183 status/list`, …), not LLM tools.

---

## The 15 functions

All in `@bnbagent/studio-runtime/tools`. Each returns a plain object (or string); the wire-format keys stay snake_case (the tool contract shared with LLMs and MCP clients).

### Wallet & chain basics - always safe

| Function | Reads | Dependency |
| --- | --- | --- |
| `walletInfo()` | active wallet address + source + keystore dir | none |
| `walletAddress()` | active wallet address (alias of walletInfo) | none |
| `walletList()` | all configured keystore addresses | dev concern |
| `balanceNative(address?, network?)` | BNB / tBNB balance | none |
| `balanceU(address?, network?)` | U token balance | `[u_token]` |
| `networkInfo(network?)` | chain id, RPC host, contract addresses | none |
| `txStatus(txHash, network?)` | tx receipt + revert reason | none |

### LLM provider - Pieverse-specific

| Function | Reads | Dependency |
| --- | --- | --- |
| `pieverseUsage(days=7)` | LLM spend on Pieverse | `[llm.provider=pieverse-llm]` |

Note: `pieverseUsage` does a SIWE EIP-191 personal_sign (no on-chain effect, domain-locked). Other functions are pure RPC reads.

### ERC-8004 identity

| Function | Reads | Dependency |
| --- | --- | --- |
| `agentInfo(agentId, network?)` | on-chain ERC-8004 record by ID | `[erc8004]` |
| `agentByAddress(address, network?)` | look up agent by owner address | `[erc8004]` |

### ERC-8183 jobs

| Function | Reads | Dependency |
| --- | --- | --- |
| `jobStatus(jobId, network?)` | job state, client, provider, budget | `[erc8183]` |
| `jobList(limit=10, mine=false, provider?, network?)` | recent jobs | `[erc8183]` |
| `jobCount(network?)` | network-wide inflight job count | `[erc8183]` |

### Advanced / footguns

| Function | Reads | Why footgun |
| --- | --- | --- |
| `blockInfo(block?, network?)` | block summary | usually noise for LLM |
| `contractCallView(address, functionSignature, args?, outputTypes?, network?)` | arbitrary `eth_call` | accepts **any** ABI - LLM can be prompt-injected into calling attacker contracts |

---

## Step 1 - Confirm the user has run `bag init`

```bash
# from workspace root:
ls app/agent/studio.toml && (ls app/agent/src/unifiedMain.ts 2>/dev/null || ls app/agent/src/mcpMain.ts)
```

If `app/agent/src/tools.ts` already exists, the user has the AI SDK form already. Skip to Step 4 if they want to customize.

---

## Step 2 - Identify the stack

Look at `app/agent/src/unifiedMain.ts` or `app/agent/src/mcpMain.ts` imports / `app/agent/package.json`:

| Sign in code | Stack |
| --- | --- |
| `import { tool, generateText } from "ai"` | **AI SDK** (use stock recipe) |
| `from "langchain"` / `from "@langchain/core"` | **LangChain.js** |
| `openai.chat.completions.create({ tools: ... })` | **bare OpenAI SDK loop** |
| `anthropic.messages.create({ tools: ... })` | **bare Anthropic SDK loop** |

If AI SDK: emit the stock recipe and stop.

```bash
bag recipe code tools-chain > app/agent/src/chainTools.ts    # full inventory + CHAIN_READ_TOOLS
```

Then in the protocol entrypoint (`app/agent/src/unifiedMain.ts` for A2A, `app/agent/src/mcpMain.ts` for MCP), pass the tool set into the generate call:

```ts
import { LLM_READ_TOOLS } from "./tools.js";
// inside runWork:
const { text } = await generateText({ model, tools: LLM_READ_TOOLS, prompt });
```

For non-AI-SDK stacks, continue.

---

## Step 3 - Write a framework-specific wrapper

Studio doesn't ship adapters for non-AI-SDK stacks (commitment: "agent code the user owns"). You write a wrapper file in the user's project. Pattern: import the pure functions, wrap each with the framework's tool primitive.

### LangChain.js

```ts
// app/agent/src/tools.ts
import { tool } from "@langchain/core/tools";
import { z } from "zod";
import * as cr from "@bnbagent/studio-runtime/tools";

export const LLM_READ_TOOLS = [
  tool(async () => cr.walletInfo(), {
    name: "wallet_info",
    description: "Describe the agent's active wallet.",
    schema: z.object({}),
  }),
  tool(
    async ({ address, network }) => cr.balanceNative(address ?? null, network),
    {
      name: "balance_native",
      description:
        "Native BNB balance of an address (defaults to the agent's wallet).",
      schema: z.object({
        address: z.string().optional(),
        network: z.string().optional(),
      }),
    },
  ),
  // balanceU (requires [u_token]), networkInfo, txStatus,
  // pieverseUsage (requires [llm.provider=pieverse-llm]),
  // agentInfo / agentByAddress (require [erc8004]),
  // jobStatus / jobList (require [erc8183]) - same pattern.
  // ⚠️ contractCallView accepts any ABI - keep it out unless deliberate.
];
```

Wire into the agent (e.g. `createReactAgent({ llm, tools: LLM_READ_TOOLS })`).

### Bare OpenAI / Anthropic tool loop

For a hand-rolled tool loop, declare each function in the provider's tool JSON format and dispatch on the tool name:

```ts
// app/agent/src/tools.ts
import * as cr from "@bnbagent/studio-runtime/tools";

export const CHAIN_READ_FUNCTIONS: Record<
  string,
  (args: any) => Promise<unknown>
> = {
  wallet_info: async () => cr.walletInfo(),
  balance_native: async (a) => cr.balanceNative(a.address ?? null, a.network),
  balance_u: async (a) => cr.balanceU(a.address ?? null, a.network), // requires [u_token]
  network_info: async (a) => cr.networkInfo(a.network),
  tx_status: async (a) => cr.txStatus(a.tx_hash, a.network),
  // pieverse_usage,                       // requires [llm.provider=pieverse-llm]
  // agent_info, agent_by_address,         // require [erc8004]
  // job_status, job_list,                 // require [erc8183]
  // contract_call_view, block_info, wallet_list, wallet_address,
};
```

### Generic

For any framework that accepts a typed function + description, the pattern is identical - wrap each `cr.*` function in the framework's tool primitive and assemble a list. The emitted AI SDK files (`tools.ts` / `chainTools.ts`) already carry per-tool descriptions and zod input schemas you can copy from.

---

## Step 4 - Customize what the LLM sees

The recipe gives a sensible default; the user owns the file. Common edits:

**Remove tools** the agent doesn't need (smaller LLM context = better focus):

```ts
export const LLM_READ_TOOLS: ToolSet = {
  balance_u: CHAIN_READ_TOOLS.balance_u, // only thing this agent really needs
  tx_status: CHAIN_READ_TOOLS.tx_status,
};
```

**Uncomment Pieverse usage** if the user's `[llm].provider = "pieverse-llm"`:

```ts
pieverse_usage: ...,   // requires [llm.provider=pieverse-llm]
```

**Uncomment 8004 / 8183 reads** if the user added those sections to `studio.toml` after `bag init` (e.g., ran `bag erc8004 register` later).

**Never uncomment** `contract_call_view` without thinking - it accepts any ABI signature and an LLM jailbreak / prompt injection can drain via reads from malicious contracts (or hammer expensive RPC). Keep commented unless the agent has a specific debug / introspection job and the user has read the tool description.

---

## Step 5 - Write operations live in fixed code, NOT LLM tools

Read tools (this skill) are safe-ish - worst case the LLM gives wrong info. **Write operations** (quote-sign, submit, settle) are the whole point of the single seller model's signing boundary: they live as FIXED code in `app/agent/src/signing.ts`, are dispatched by A2A's `SellerCore` (in `app/agent/src/sellerCore.ts`, which `SellerAgentExecutor` inherits) or MCP's server tools (`negotiate`/`notify_funded`; `settle` is the manual `bag erc8183 settle`), and are **never** put in the LLM's `tools` set. The quote price is rule-based: fixed code reads canonical `[payments.seller].price_usd`, converts it exactly for the selected asset, and signs; the LLM never touches the price. Only a legacy U-only config without `[payments.seller]` retains `price`/`min_price`/`max_price` clamp semantics. The LLM only PRODUCES the work text in `notify_funded` delivery - money never flows through a tool call.

The one automatic signing path outside `signing.ts` is the budget-gated model-wrapper LLM-credit auto-renew hook (in the emitted `app/agent/src/model.ts`'s `buildModel()` factory, backed by `@bnbagent/studio-runtime/pieverse` `PieverseCreditEnsurer`) - also automatic, also **not** an LLM tool.

The x402 buyer kernel (`@bnbagent/studio-runtime/x402`, the payment signer) is **not** an LLM tool either - in v1 it is reachable only as the Agent's automatic model-wrapper LLM-credit auto-renew (above), driven by fixed code, never the LLM. Do not wire it into the Agent's `tools` set. The SDK's `SigningPolicy` is the second-layer gate on every signature regardless.

---

## Common questions

**Q: Why isn't `app/agent/src/tools.ts` auto-synced with `app/agent/studio.toml` changes?**

A: The recipe is emitted once at `bag init` time; the file is the user's. To refresh after configuring new features (e.g., enabling `[erc8183]` later):

```bash
bag recipe code tools-chain > app/agent/src/chainTools.ts.new
diff app/agent/src/chainTools.ts app/agent/src/chainTools.ts.new
# manually merge - preserves any user customizations
```

**Q: Does this work in AgentCore deployment?**

A: Yes. The functions only need `@bnbagent/studio-runtime` (already a dependency of the Agent sub-project via `app/agent/package.json`). No subprocess, no MCP transport - pure in-process calls. The deploy artifact ships the built `tools.ts` as part of the Agent that serves its selected A2A/MCP faces on AgentCore.

**Q: Is this the same as `bag init --protocols MCP`?**

A: No. `bag init --protocols MCP` selects an **external seller face** (streamable-HTTP `/mcp` for buyers). This skill wires read-only chain queries into the Agent's own LLM as in-process tools. The current release does not ship MCP-for-agent (the agent runtime consuming a subprocess MCP server as its LLM tools). MCP here is instead an _external seller face_ (`bag init --protocols MCP` or `--protocols A2A,MCP`) - see `docs/design/decisions.md`. For now: in-process is simpler, faster, and matches commitment "agent code the user owns".

**Q: How do I know if my `app/agent/src/tools.ts` is up to date?**

A: Re-emit with `bag recipe code tools-chain > app/agent/src/chainTools.ts.new` and diff against your current file. If studio added new tools in a newer version, they'll appear in the emit; you decide whether to adopt.

**Q: Can I reuse a Pieverse API key I created with a DIFFERENT wallet (BYOK)?**

A: Yes, for inference - with one caveat. The LLM-credit auto-renew hook (`PieverseCreditEnsurer`) authenticates to Pieverse with the **agent's signing wallet** and can only inspect/allocate keys **that wallet owns**. If you set `[llm.pieverse].key_hash` to a key created by another wallet (the owner is your day-to-day wallet, not the agent's throwaway signer), the hook can't see it: it detects the owner mismatch, prints one warning, **disables itself for that session, and lets inference run on the key's existing Bearer credit**. It does not crash the agent and does not repeat the check.

Recommended BYOK setup - do NOT hand the owner wallet's private key to the agent (that would violate the "keys stay in the user's environment" boundary):

1. Put the key in the agent env: `PIEVERSE_LLM_API_KEY=sk-pv-…` in `.studio/.env.local`, plus `[llm.pieverse].key_hash = "0x…"` and `network` in `studio.toml`.
2. Turn off auto-renew so the hook doesn't try to allocate a key it can't own: `bag llm auto-renew llm off`.
3. Top the key up yourself in the Pieverse portal (or from the owner wallet) when it runs low - the agent will 402 upstream if the Bearer credit is exhausted.

If you instead want the agent to auto-allocate/topup, activate a key the **agent's own** signing wallet owns with `bag llm activate` (zero-deposit is fine) and keep auto-renew on.
