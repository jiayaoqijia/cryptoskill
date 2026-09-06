---
name: hedera-official-agent-kit-js
description: "Build Hedera-powered AI agents **in under a minute**."
---

# Hedera Agent Kit

![npm version](https://badgen.net/npm/v/@hashgraph/hedera-agent-kit)
![license](https://badgen.net/github/license/hashgraph/hedera-agent-kit-js)
![build](https://badgen.net/github/checks/hashgraph/hedera-agent-kit-js)

Build Hedera-powered AI agents **in under a minute**.

> **Upgrading from v3?** See the [v3 → v4 Migration Guide](docs/MIGRATION-v4.md) for all breaking changes.
>
> **Building a custom plugin?** See the [Custom Plugin Authoring Guide](docs/PLUGINS.md#creating-a-plugin) — the v4 `BaseTool` pattern, a runnable starter in [`examples/plugin`](examples/plugin), and a no-LLM smoke test.

## Packages

The Hedera Agent Kit is organized as a monorepo containing the core SDK and multiple framework adapter packages:

| Package                                     | NPM Link                                                                   | Description                                            |
|---------------------------------------------|----------------------------------------------------------------------------|--------------------------------------------------------|
| **`@hashgraph/hedera-agent-kit`**           | [npm](https://www.npmjs.com/package/@hashgraph/hedera-agent-kit)           | Core SDK & plugins for Hedera network integration      |
| **`@hashgraph/hedera-agent-kit-langchain`** | [npm](https://www.npmjs.com/package/@hashgraph/hedera-agent-kit-langchain) | LangChain adapter (StructuredTools, agent utils)       |
| **`@hashgraph/hedera-agent-kit-ai-sdk`**    | [npm](https://www.npmjs.com/package/@hashgraph/hedera-agent-kit-ai-sdk)    | Vercel AI SDK adapter (compatible with standard tools) |
| **`@hashgraph/hedera-agent-kit-elizaos`**   | [npm](https://www.npmjs.com/package/@hashgraph/hedera-agent-kit-elizaos)   | ElizaOS adapter (custom Eliza Actions)                 |
| **`@hashgraph/hedera-agent-kit-mcp`**       | [npm](https://www.npmjs.com/package/@hashgraph/hedera-agent-kit-mcp)       | Model Context Protocol (MCP) Server toolkit            |
| **`@hashgraph/hedera-agent-kit-adk`**       | [npm](https://www.npmjs.com/package/@hashgraph/hedera-agent-kit-adk)       | Google Agent Development Kit (ADK) adapter             |
| **`create-hedera-agent`**                   | [npm](https://www.npmjs.com/package/create-hedera-agent)                   | CLI scaffold tool to bootstrap Next.js agent apps      |

---

## Contents

- [Packages](#-packages)
- [Key Features](#key-features)
- [About the Agent Kit Functionality](#agent-kit-functionality)
- [Third Party Plugins](#third-party-plugins)
- [Hooks and Policies](#hooks-and-policies)
- [Developer Examples](#developer-examples)
- [🚀 60-Second Quick-Start](#-60-second-quick-start)
- [Agent Execution Modes](#agent-execution-modes)
- [Hedera Plugins & Tools](#hedera-plugins--tools)
- [Creating Plugins & Contributing](#creating-plugins--contributing)
- [License](#license)
- [Credits](#credits)

---

## Key Features

The Hedera Agent Kit is an open-source toolkit that brings intelligent agent workflows to the Hedera network. It’s designed for developers who want to integrate Hedera account management and Hedera native functionality into agent applications. With the Hedera Agent Kit, developers can build agents that interact on-chain through a conversational interface. This means Hedera agents can do more than process information; they can also send tokens, manage accounts, store data on Hedera Consensus Service, and coordinate workflows directly on a public ledger.

As of v4, the Hedera Agent Kit is organized as a monorepo of `@hashgraph`-scoped packages. You install the core package plus only the toolkit for your framework (LangChain, Vercel AI SDK, ElizaOS, or MCP). See the [v3 → v4 Migration Guide](docs/MIGRATION-v4.md) for details.

The Hedera Agent Kit is extensible with third party plugins by other projects.

---

## Agent Kit Functionality

The list of currently available Hedera plugins and functionality can be found in the [Plugins & Tools section](#hedera-plugins--tools) of this page

👉 See [docs/HEDERAPLUGINS.md](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/HEDERAPLUGINS.md) for the full catalogue & usage examples for Hedera Tools.

Want to add more functionality from Hedera Services? [Open an issue](https://github.com/hashgraph/hedera-agent-kit-js/issues/new?template=toolkit_feature_request.yml&labels=feature-request)!

---

### Third Party Plugins
The Hedera Agent Kit is extensible with third-party plugins developed by other projects. See how you can build and submit your own plugin to be listed as a Hedera Agent Kit plugin in [Hedera Docs](https://docs.hedera.com/hedera/open-source-solutions/ai-studio-on-hedera/hedera-ai-agent-kit/plugins#plugins) and in [docs/PLUGINS.md](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/PLUGINS.md).

👉 **Build your own plugin:** follow the [Custom Plugin Authoring Guide](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/PLUGINS.md#creating-a-plugin) (v4 `BaseTool` pattern, a runnable starter in [`examples/plugin`](https://github.com/hashgraph/hedera-agent-kit-js/tree/main/examples/plugin), and a no-LLM smoke test), then [publish and register it](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/PLUGINS.md#publish-and-register-your-plugin) to get it listed here.

_[Contribute your own plugin](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/PLUGINS.md#creating-a-plugin)_

### Hooks and Policies

The Hedera Agent Kit provides a flexible and powerful system for putting limits on tool usage and enforcing business logic, effectively enabling you to limit the functionality of AI agents through **Hooks** and **Policies**. These hooks and policies can be used to enforce security, compliance, and other business rules.

**Features**
* Hooks and policies can be called when parameters are passed, after parameter normalization, before tool execution when a transaction has been formed, and after tool execution when a transaction has been signed and submitted.
* Users can create their own hooks and policies on any available Hedera Agent Kit tool, simply fork this repo and create your own hooks and policies in the `typescript/src/hooks` and `typescript/src/policies` directories.
* We have provided examples:
  * A hook to [log actions to an HCS topic](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/HOOKS_AND_POLICIES.md#1-hcsaudittrailhook-hook), creating an easy to track audit trail. 
  * A policy that [sets the maximum number of recipients](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/HOOKS_AND_POLICIES.md#2-maxrecipientspolicy-policy) in a transfer or airdrop.
  * A policy the [blocks tool usage](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/HOOKS_AND_POLICIES.md#3-rejecttoolpolicy-policy) by an agent.

For more information on hooks and policies, see the [Hooks and Policies documentation](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/HOOKS_AND_POLICIES.md).

Try out an example [Audit Trail Agent](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md#option-i-run-the-audit-trail-agent) to see how hooks and policies work in practice.

---

## Developer Examples


You can try out examples of the different types of agents you can build by followin the instructions in the [Developer Examples](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md) doc in this repo.

First follow instructions in the [Developer Examples to clone and configure the example](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md), then choose from one of the examples to run:

- **Option A -** [Example Tool Calling Agent](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md#option-a-run-the-example-tool-calling-agent)
- **Option B -** [Example Structured Chat Agent](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md#option-b-run-the-structured-chat-agent-langchain-v03-only)
- **Option C -** [Example Return Bytes Agent](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md#option-c-try-the-human-in-the-loop-chat-agent)
- **Option D -** [Example MCP Server](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md#option-d-try-out-the-mcp-server)
- **Option E -** [Example External MCP Agent](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md#option-e-try-out-the-external-mcp-agent)
- **Option F -** [Example ElizaOS Agent](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md#option-f-try-out-the-hedera-agent-kit-with-elizaos)
- **Option G -** [Example Preconfigured MCP Client Agent](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md#option-g-try-out-the-preconfigured-mcp-client-agent)
- **Option H -** [Example Policy Enforcement Agent](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md#option-h-run-the-policy-enforcement-agent)
- **Option I -** [Example Audit Trail Agent](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md#option-i-run-the-audit-trail-agent)
- **Option J -** [Example Custom Signing Agent](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md#option-j-run-the-custom-signing-agent)
- **Option K -** [Example Google ADK Agent](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md#option-k-try-out-the-google-adk-agent)

---

## 🚀 60-Second Quick-Start

See more info at [https://www.npmjs.com/package/@hashgraph/hedera-agent-kit](https://www.npmjs.com/package/@hashgraph/hedera-agent-kit)

### 🆓 Free AI Options Available!

- **Ollama**: 100% free, runs on your computer, no API key needed
- **[Groq](https://console.groq.com/keys)**: Offers generous free tier with API key
- **[Claude](https://console.anthropic.com/settings/keys) & [OpenAI](https://platform.openai.com/api-keys)**: Paid options for production use

### 1 – Project Setup
Create a directory for your project and install dependencies:
```bash
mkdir hello-hedera-agent-kit
cd hello-hedera-agent-kit
```

Init and install with npm
```bash
npm init -y
```

Open `package.json` and add `"type": "module"` to enable ES modules.

Install the core package, LangChain toolkit, your LLM provider, and the Hedera SDK:

```bash
npm install @hiero-ledger/sdk @hashgraph/hedera-agent-kit @hashgraph/hedera-agent-kit-langchain langchain @langchain/openai dotenv
```

> Using a different LLM? Replace `@langchain/openai` with `@langchain/anthropic`, `@langchain/groq`, or `@langchain/ollama`.

### 2 – Configure: Add Environment Variables

Create an `.env` file in the root directory of your project:

```bash
touch .env
```

If you already have a **testnet** account, you can use it. Otherwise, you can create a new one at [https://portal.hedera.com/dashboard](https://portal.hedera.com/dashboard)

Add the following to the .env file:

```env
# Required: Hedera credentials (get free testnet account at https://portal.hedera.com/dashboard)
ACCOUNT_ID="0.0.xxxxx"
PRIVATE_KEY="0x..." # ECDSA or ED25519 private key (see note below)

# Optional: Add the API key for your chosen AI provider
OPENAI_API_KEY="sk-proj-..."      # For OpenAI (https://platform.openai.com/api-keys)
ANTHROPIC_API_KEY="sk-ant-..."    # For Claude (https://console.anthropic.com)
GROQ_API_KEY="gsk_..."            # For Groq free tier (https://console.groq.com/keys)
# Ollama doesn't need an API key (runs locally)
```

##### About Private Keys

Hedera supports two key types: **ECDSA (secp256k1)** and **ED25519**. These examples default to **ECDSA**. To switch to ED25519, uncomment the appropriate line in the agent's `.ts` file:

```ts
PrivateKey.fromStringECDSA(process.env.PRIVATE_KEY!)   // default
// PrivateKey.fromStringED25519(process.env.PRIVATE_KEY!)
```

Both constructors accept hex (`0x...`) and DER-encoded keys. DER-encoded ED25519 keys start with `302e...`; DER-encoded ECDSA keys start with `3030...`. The untyped `PrivateKey.fromString()` is deprecated — use the typed constructors instead. There is no reliable way to infer the key type from the string alone, so pick the constructor matching how the key was generated (the Hedera Portal shows the type). A mismatch is rejected by the network with `INVALID_SIGNATURE`. Note: the agent kit's built-in EVM/ERC tools currently require an ECDSA operator key; the Hedera EVM itself supports both key types.

See the Hedera docs on [Keys and Signatures](https://docs.hedera.com/hedera/core-concepts/keys-and-signatures#key-types:-ecdsa-vs-ed25519) and [Accounts and Keys (EVM)](https://docs.hedera.com/evm/differences/accounts-and-keys).

### 3 – Simple "Hello Hedera Agent Kit" Example

Create a new file called `index.ts` in the `hello-hedera-agent-kit` folder.

```bash
touch index.ts
```

Once you have created the file and added the environment variables, you can run the following code:

```typescript
// index.ts
import { Client, PrivateKey } from '@hiero-ledger/sdk';
import { AgentMode } from '@hashgraph/hedera-agent-kit';
import { allCorePlugins } from '@hashgraph/hedera-agent-kit/plugins';
import { HederaLangchainToolkit } from '@hashgraph/hedera-agent-kit-langchain';
import { ChatOpenAI } from '@langchain/openai';
import { createAgent } from 'langchain';
import * as dotenv from 'dotenv';

dotenv.config();

async function main() {
  // Hedera client setup (Testnet by default)
  const client = Client.forTestnet().setOperator(
    process.env.ACCOUNT_ID!,
    PrivateKey.fromStringECDSA(process.env.PRIVATE_KEY!)
  );

  // Prepare Hedera toolkit with explicit plugin selection
  const toolkit = new HederaLangchainToolkit({
    client,
    configuration: {
      plugins: allCorePlugins,
      context: { mode: AgentMode.AUTONOMOUS },
    },
  });

  const agent = createAgent({
    model: new ChatOpenAI({ model: 'gpt-4o-mini' }),
    tools: toolkit.getTools(),
    systemPrompt: 'You are a helpful assistant with access to Hedera blockchain tools',
  });

  const response = await agent.invoke({
    messages: [{ role: 'user', content: "What's my HBAR balance?" }],
  });

  const lastMessage = response.messages[response.messages.length - 1];
  console.log(lastMessage.content);
}

main().catch(console.error);
```

### 4 – Run Your "Hello Hedera Agent Kit" Example

From the root directory, run your example agent:

```bash
npx tsx index.ts
```

> To see more examples, check out the [examples/](https://github.com/hashgraph/hedera-agent-kit-js/tree/main/examples) directory in this repo.

---

## About the Agent Kit

### Agent Execution Modes

HAK supports three transaction execution modes:

- `mode: AgentMode.AUTONOMOUS` — signs and broadcasts transactions directly using the operator key set on the client. Ideal for local testing, scripts, and fully autonomous agents.
- `mode: AgentMode.RETURN_BYTES` — returns serialized unsigned transaction bytes to the caller for external signing (e.g. MetaMask, HashPack, or any wallet). Ideal for stateless servers, browser extensions, and dApps.
- `mode: AgentMode.CUSTOM_EXECUTE_TX` — delegates signing **and execution** to a pluggable `TransactionStrategy` (e.g. remote TEE, MPC, KMS, HITL console). Returns a full receipt; compatible with audit-trail hooks.
- `mode: AgentMode.CUSTOM_RETURN_BYTES` — delegates transaction assembly to a pluggable `TransactionStrategy` that returns unsigned bytes for out-of-band signing. Enables delegated-payer flows.

For full configuration examples, built-in strategies, and a reference implementation, see [docs/TRANSACTION_MODES.md](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/TRANSACTION_MODES.md). For building non-custodial MCP servers on top of `RETURN_BYTES` mode, see [docs/MCP.md](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/MCP.md).

### Hedera Plugins & Tools

The Hedera Agent Kit provides a set of tools, bundled into plugins, to interact with the Hedera network. See how to build your own plugins in [docs/HEDERAPLUGINS.md](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/HEDERAPLUGINS.md)

Currently, the following plugins are available:

#### Available Plugins & Tools

#### Core Account Plugin: Tools for Hedera Account Service operations

- Transfer HBAR

#### Core Consensus Plugin: Tools for Hedera Consensus Service (HCS) operations

- Create a Topic
- Submit a message to a Topic

#### Core Token Plugin: Tools for Hedera Token Service operations

- Create a Fungible Token
- Create a Non-Fungible Token
- Airdrop Fungible Tokens

#### Query Plugins: Tools for querying Hedera network data

- Account queries (balances, info)
- Token queries (info, airdrops)
- Consensus queries (topic info, messages)
- EVM queries (contract info)
- Misc queries (exchange rates)
- Transaction queries (transaction records)

_See more in [docs/PLUGINS.md](docs/PLUGINS.md)_

---

## Creating Plugins & Contributing

- You can find a guide for creating plugins in [docs/PLUGINS.md](docs/PLUGINS.md)

- For a complete, annotated custom-plugin starter (v4 `BaseTool` pattern, non-transaction tools, and a no-LLM smoke test), see [examples/plugin](examples/plugin)

- This guide also has instructions for [publishing and registering your plugin](docs/PLUGINS.md#publish-and-register-your-plugin) to help our community find and use it.

- If you would like to contribute and suggest improvements for the cord SDK and MCP server, see [CONTRIBUTING.md](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/CONTRIBUTING.md) for details on how to contribute to the Hedera Agent Kit.

## License

Apache 2.0

## Credits

Special thanks to the developers of the [Stripe Agent Toolkit](https://github.com/stripe/agent-toolkit) who provided the inspiration for the architecture and patterns used in this project.
