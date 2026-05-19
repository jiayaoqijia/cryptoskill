---
name: aptos-official-agent-skills
description: "[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Compatible-green.svg)](https://agentskills.io)"
---

# aptos-official-agent-skills

_Source: [github.com/aptos-labs/aptos-agent-skills](https://github.com/aptos-labs/aptos-agent-skills). The body below is the upstream README.md captured at the time of registration._

---

# Aptos Agent Skills

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Compatible-green.svg)](https://agentskills.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills: 17](https://img.shields.io/badge/Skills-17-green.svg)](#aptos-development-skills)
[![Patterns: 9](https://img.shields.io/badge/Patterns-9-orange.svg)](patterns/)
[![SkillsMP](https://img.shields.io/badge/SkillsMP-Browse-purple.svg)](https://skillsmp.com/search?q=aptos)
[![Skills.sh](https://img.shields.io/badge/Skills.sh-Install-blue.svg)](https://skills.sh/search?q=aptos)

AI-assisted Aptos blockchain development with **Claude Code**, **Cursor**, and **GitHub Copilot**. These skills give
your AI coding assistant deep knowledge of Move smart contract development, the Aptos TypeScript SDK, and the full dApp
lifecycle — from project scaffolding to deployment.

- **Move V2 Object Model** — Write secure smart contracts using modern Aptos patterns
- **Gas Optimization** — Analyze and reduce transaction costs in Move contracts
- **Security Auditing** — Catch vulnerabilities before deploying to devnet, testnet, or mainnet
- **TypeScript SDK** — Integrate Aptos wallets, transactions, and view functions into your frontend
- **AI-Powered Workflow** — Skills activate automatically based on developer intent

## Install

#### Recommended

```bash
npx skills add aptos-labs/aptos-agent-skills
```

#### Claude Code plugin

```
/plugin marketplace add aptos-labs/aptos-agent-skills
```

#### Manual

```bash
git clone https://github.com/aptos-labs/aptos-agent-skills.git
```

See [INSTALL.md](INSTALL.md) for selective installation and other options.

## Aptos Development Skills

### Move Smart Contracts

| Skill                                                                     | Purpose                                                      |
| ------------------------------------------------------------------------- | ------------------------------------------------------------ |
| [write-contracts](skills/move/write-contracts/SKILL.md)                   | Generate secure Aptos Move V2 smart contracts                |
| [generate-tests](skills/move/generate-tests/SKILL.md)                     | Generate Move unit tests targeting 100% code coverage        |
| [security-audit](skills/move/security-audit/SKILL.md)                     | Security audit for Move smart contracts before deployment    |
| [deploy-contracts](skills/move/deploy-contracts/SKILL.md)                 | Deploy Move contracts to devnet, testnet, or mainnet         |
| [search-aptos-examples](skills/move/search-aptos-examples/SKILL.md)       | Search aptos-core for reference implementations and patterns |
| [analyze-gas-optimization](skills/move/analyze-gas-optimization/SKILL.md) | Analyze and reduce gas costs in Move smart contracts         |
| [modernize-move](skills/move/modernize-move/SKILL.md)                     | Migrate Move V1 resource accounts to V2 object model         |

### TypeScript SDK

| Skill                                                                         | Purpose                                                                        |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [use-ts-sdk](skills/sdk/typescript/use-ts-sdk/SKILL.md)                       | Aptos TypeScript SDK orchestrator for frontend integration                     |
| [ts-sdk-client](skills/sdk/typescript/ts-sdk-client/SKILL.md)                 | Set up Aptos client with AptosConfig and network selection                     |
| [ts-sdk-account](skills/sdk/typescript/ts-sdk-account/SKILL.md)               | Create Aptos accounts and signers from private keys or derivation paths        |
| [ts-sdk-address](skills/sdk/typescript/ts-sdk-address/SKILL.md)               | Parse and derive Aptos account addresses (AIP-40)                              |
| [ts-sdk-transactions](skills/sdk/typescript/ts-sdk-transactions/SKILL.md)     | Build, sign, and submit Aptos transactions including sponsored and multi-agent |
| [ts-sdk-view-and-query](skills/sdk/typescript/ts-sdk-view-and-query/SKILL.md) | Call Move view functions and query on-chain Aptos data                         |
| [ts-sdk-types](skills/sdk/typescript/ts-sdk-types/SKILL.md)                   | Map Move types to TypeScript (u64, u128, address, vector)                      |
| [ts-sdk-wallet-adapter](skills/sdk/typescript/ts-sdk-wallet-adapter/SKILL.md) | Integrate Aptos wallets into React apps with useWallet                         |

### Project Setup

| Skill                                                                | Purpose                                                 |
| -------------------------------------------------------------------- | ------------------------------------------------------- |
| [create-aptos-project](skills/project/create-aptos-project/SKILL.md) | Scaffold new Aptos dApp projects with create-aptos-dapp |

### Community Skills

Community-contributed skills built by developers across the Aptos ecosystem. These are independently maintained and have
not been reviewed by Aptos Labs. See [community-skills/](community-skills/) for contribution guidelines.

| Skill                                                              | Author    | Purpose                                                 |
| ------------------------------------------------------------------ | --------- | ------------------------------------------------------- |
| [smoothsend-gasless](community-skills/smoothsend-gasless/SKILL.md) | ivedmohan | Sponsor gas fees for Aptos transactions with SmoothSend |

## Quick Start

### Claude Code

Skills activate automatically based on what you say:

```
"Create a new dApp"           → project scaffolding
"Write an NFT contract"       → /write-contracts
"Write tests for this"        → /generate-tests
"Check security"              → /security-audit
"Deploy to testnet"           → /deploy-contracts
"Add a frontend"              → /use-ts-sdk
```

### Cursor / Copilot

Reference skill files directly in prompts:

```
@skills/move/write-contracts/SKILL.md Help me build an NFT marketplace
```

Include `CLAUDE.md` in your workspace context for full skill routing and auto-recommendations.

## Aptos dApp Development Workflow

1. **Create** — `/create-aptos-project` scaffolds with `npx create-aptos-dapp`
2. **Write** — `/write-contracts` generates Move modules
3. **Test** — `/generate-tests` creates test suites with 100% coverage
4. **Audit** — `/security-audit` checks for vulnerabilities
5. **Deploy** — `/deploy-contracts` publishes to your target network
6. **Frontend** — `/use-ts-sdk` wires up TypeScript integration

See [CLAUDE.md](CLAUDE.md) for all workflows, global rules, and pattern references.

## Learn More

| Resource                                        | Description                                                                     |
| ----------------------------------------------- | ------------------------------------------------------------------------------- |
| [CLAUDE.md](CLAUDE.md)                          | Full guide for AI assistants — workflows, rules, skill routing                  |
| [INSTALL.md](INSTALL.md)                        | Installation options and selective skill setup                                  |
| [patterns/](patterns/)                          | Reference docs for objects, digital assets, fungible assets, security, and more |
| [community-skills/](community-skills/)          | Community-contributed skills and contribution guidelines                        |
| [aptos.dev](https://aptos.dev)                  | Official Aptos documentation                                                    |
| [SkillsMP](https://skillsmp.com/search?q=aptos) | Browse Aptos skills on SkillsMP                                                 |
| [Skills.sh](https://skills.sh/search?q=aptos)   | Browse and install via Skills.sh                                                |

## Contributing

We welcome contributions — new skills, pattern improvements, examples, and bug fixes. See
[CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT — see [LICENSE](LICENSE) for details.
