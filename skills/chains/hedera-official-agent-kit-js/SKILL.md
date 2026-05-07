---
name: hedera-official-agent-kit-js
description: "Build Hedera-powered AI agents **in under a minute**."
---

# hedera-official-agent-kit-js

_Source: [github.com/hashgraph/hedera-agent-kit-js](https://github.com/hashgraph/hedera-agent-kit-js). The body below is the upstream README.md captured at the time of registration._

---

# Hedera Agent Kit

![npm version](https://badgen.net/npm/v/@hashgraph/hedera-agent-kit)
![license](https://badgen.net/github/license/hashgraph/hedera-agent-kit-js)
![build](https://badgen.net/github/checks/hashgraph/hedera-agent-kit-js)

Build Hedera-powered AI agents **in under a minute**.

> **Upgrading from v3?** See the [v3 → v4 Migration Guide](docs/MIGRATION-v4.md) for all breaking changes.

## 📋 Contents

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

The list of currently available Hedera plugins and functionality can be found in the [Plugins & Tools section](#hedera-plugins-tools) of this page

👉 See [docs/HEDERAPLUGINS.md](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/HEDERAPLUGINS.md) for the full catalogue & usage examples for Hedera Tools.

Want to add more functionality from Hedera Services? [Open an issue](https://github.com/hashgraph/hedera-agent-kit-js/issues/new?template=toolkit_feature_request.yml&labels=feature-request)!

---

### Third Party Plugins
The Hedera Agent Kit is extensible with third party plugins by other projects. See how you can build and submit your own plugin to listed as a Hedera Agent Kit plugin in [Hedera Docs](https://docs.hedera.com/hedera/open-source-solutions/ai-studio-on-hedera/hedera-ai-agent-kit/hedera-agent-kit-js/plugins) and README in [docs/PLUGINS.md](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/PLUGINS.md) 

- [Memejob Plugin](https://www.npmjs.com/package/@buidlerlabs/hak-memejob-plugin) provides a streamlined interface to the [**memejob**](https://memejob.fun/) protocol, exposing the core actions (`create`, `buy`, `sell`) for interacting with meme tokens on Hedera:

  Github repository: https://github.com/buidler-labs/hak-memejob-plugin

- [Bonzo Plugin](https://www.npmjs.com/package/@bonzofinancelabs/hak-bonzo-plugin) is a unified SDK to the [**Bonzo**](https://bonzo.finance) protocol, exposing the core actions (`deposit`, `withdraw`, `repay`, `borrow`) for decentralised lending and borrowing on Hedera:

  Github repository: [https://github.com/Bonzo-Labs/bonzoPlugin](https://github.com/Bonzo-Labs/bonzoPlugin)

- [SaucerSwap Plugin](https://www.npmjs.com/package/hak-saucerswap-plugin) provides a streamlined interface to the [**SaucerSwap**](https://saucerswap.finance) DEX, exposing the core actions (`saucerswap_get_swap_quote`, `saucerswap_swap_tokens`, `saucerswap_get_pools`, `saucerswap_add_liquidity`, `saucerswap_remove_liquidity`, `saucerswap_get_farms`) for swaps, liquidity, and farming insights:

  NPM: https://www.npmjs.com/package/hak-saucerswap-plugin
  Source: https://github.com/jmgomezl/hak-saucerswap-plugin
  Tested/endorsed version: hak-saucerswap-plugin@1.0.1

- [Pyth Plugin](https://www.npmjs.com/package/hak-pyth-plugin) provides access to the [**Pyth Network**](https://www.pyth.network/) price feeds via the Hermes API, exposing tools to list feeds and fetch latest prices:

  Github repository: [https://github.com/jmgomezl/hak-pyth-plugin](https://github.com/jmgomezl/hak-pyth-plugin).
  Tested/endorsed version of plugin: hak-pyth-plugin@0.1.1

- [CoinCap Plugin](https://www.npmjs.com/package/coincap-hedera-plugin) provides access to the [**CoinCap API service**](https://www.coincap.io) to access cryptocurrency market data. It exposes the action (`get HBAR price in USD`) to get the current price of HBAR in USD currency, by using it you can ask your agent to get your current HBAR balance expressed in USD.

  Github repository: [https://github.com/henrytongv/coincap-hedera-plugin](https://github.com/henrytongv/coincap-hedera-plugin). Tested/endorsed version of plugin: coincap-hedera-plugin@1.0.4

- [Chainlink price feed Plugin](https://www.npmjs.com/package/chainlink-pricefeed-plugin) provides access to the [**Chainlink price feeds**](https://docs.chain.link/data-feeds/price-feeds) to get data aggregated from many data sources. It exposes the action (`get price feed`) that allows you to get the current price for ETH, BTC, HBAR, LINK, USDC, UST or DAI.

  Github repository: [https://github.com/henrytongv/chainlink-price-plugin-js](https://github.com/henrytongv/chainlink-price-plugin-js). Tested/endorsed version of plugin: chainlink-pricefeed-plugin@1.0.4

- [Hedera T3N Plugin](https://www.npmjs.com/package/@terminal3/hedera-t3n-plugin) provides access to [Terminal 3 Network (T3N)](https://docs.terminal3.io/t3n/) to enable identity verification, authentication, and last mile-delivery or selective disclosure of private and sensitive information for AI-driven applications, ensuring compliant and auditable interactions.

  Github repository: [https://github.com/Terminal-3/hedera-t3n-plugin](https://github.com/Terminal-3/hedera-t3n-plugin)

_[Contribute your own plugin](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/PLUGINS.md)_

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

Try out an example [Audit Hook Agent](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md#option-i-try-out-the-audit-hook-agent) to see how hooks and policies work in practice.

---

## Developer Examples


You can try out examples of the different types of agents you can build by followin the instructions in the [Developer Examples](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md) doc in this repo.

First follow instructions in the [Developer Examples to clone and configure the example](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md), then choose from one of the examples to run:

- **Option A -** [Example Tool Calling Agent](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md#option-a-run-the-example-tool-calling-agent)
- **Option B -** [Example Structured Chat Agent](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md#option-b-run-the-structured-chat-agent)
- **Option C -** [Example Return Bytes Agent](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md#option-c-try-the-human-in-the-loop-chat-agent)
- **Option D -** [Example MCP Server](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md#option-d-try-out-the-mcp-server)
- **Option E -** [Example ElizaOS Agent](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md#option-e-try-out-the-hedera-agent-kit-with-elizaos)
- **Option F -** [Example Preconfigured MCP Client Agent](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md#option-g-try-out-the-preconfigured-mcp-client-agent)
- **Option G -** [Example Google ADK Agent](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/docs/DEVEXAMPLES.md#option-h-try-out-the-google-adk-agent)

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
npm install @hiero-ledger/sdk @hashgraph/hedera-agent-kit @hashgraph/hedera-agent-kit-langchain @langchain/openai dotenv
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
PRIVATE_KEY="0x..." # ECDSA encoded private key

# Optional: Add the API key for your chosen AI provider
OPENAI_API_KEY="sk-proj-..."      # For OpenAI (https://platform.openai.com/api-keys)
ANTHROPIC_API_KEY="sk-ant-..."    # For Claude (https://console.anthropic.com)
GROQ_API_KEY="gsk_..."            # For Groq free tier (https://console.groq.com/keys)
# Ollama doesn't need an API key (runs locally)
```

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

This tool has two execution modes with AI agents; autonomous execution and return bytes. If you set:

- `mode: AgentMode.RETURN_BYTE` the transaction will be executed, and the bytes to execute the Hedera transaction will be returned.
- `mode: AgentMode.AUTONOMOUS` the transaction will be executed autonomously, using the accountID set (the operator account can be set in the client with `.setOperator(process.env.ACCOUNT_ID!`)

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

- This guide also has instructions for [publishing and registering your plugin](docs/PLUGINS.md#publish-and-register-your-plugin) to help our community find and use it.

- If you would like to contribute and suggest improvements for the cord SDK and MCP server, see [CONTRIBUTING.md](https://github.com/hashgraph/hedera-agent-kit-js/blob/main/CONTRIBUTING.md) for details on how to contribute to the Hedera Agent Kit.

## License

Apache 2.0

## Credits

Special thanks to the developers of the [Stripe Agent Toolkit](https://github.com/stripe/agent-toolkit) who provided the inspiration for the architecture and patterns used in this project.
