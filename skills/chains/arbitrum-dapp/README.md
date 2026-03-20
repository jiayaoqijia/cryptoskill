<p align="center">
  <img src=".github/banner.svg" alt="arbitrum-dapp-skill" width="100%">
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="License: MIT"></a>
  <a href="https://www.rust-lang.org"><img src="https://img.shields.io/badge/Rust-1.81+-orange.svg?style=flat-square&logo=rust" alt="Rust"></a>
  <a href="https://soliditylang.org/"><img src="https://img.shields.io/badge/Solidity-0.8+-363636.svg?style=flat-square&logo=solidity" alt="Solidity"></a>
  <a href="https://arbitrum.io"><img src="https://img.shields.io/badge/Arbitrum-Stylus-28A0F0.svg?style=flat-square" alt="Arbitrum Stylus"></a>
  <a href="https://book.getfoundry.sh/"><img src="https://img.shields.io/badge/Built%20with-Foundry-FFDB1C.svg?style=flat-square" alt="Foundry"></a>
  <a href="http://makeapullrequest.com"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square" alt="PRs Welcome"></a>
  <a href="https://clawhub.ai/hummusonrails/arbitrum-dapp-skill"><img src="https://img.shields.io/badge/ClawHub-arbitrum--dapp--skill-FF6B4A.svg?style=flat-square" alt="ClawHub"></a>
</p>

<p align="center">
  <strong>A <a href="https://github.com/anthropics/skills">Claude Code skill</a> for building high-performance dApps on Arbitrum with Stylus Rust and Solidity.</strong>
  <br>
  <a href="https://www.youtube.com/watch?v=vsejiaOTmJA">Demo</a> · <a href="https://hummusonrails.github.io/arbitrum-dapp-skill?ref=github-readme">Documentation</a> · <a href="#quick-start">Quick Start</a> · <a href="https://github.com/hummusonrails/arbitrum-dapp-skill/issues">Report a Bug</a>
</p>

<p align="center">
  <a href="https://www.youtube.com/watch?v=vsejiaOTmJA">
    <img src=".github/video-thumbnail.png" alt="Watch the demo on YouTube" width="600">
  </a>
</p>

## What it does

This skill gives Claude Code deep knowledge of the Arbitrum development stack so it can help you:

- **Scaffold** a monorepo with Stylus Rust contracts, Solidity contracts, and a React frontend
- **Write and test** smart contracts using the Stylus Rust SDK or Foundry
- **Run** a local Arbitrum devnode for development
- **Build** frontend interfaces with viem and wagmi
- **Deploy** contracts to Arbitrum Sepolia and Arbitrum One
- **Interop** across contract languages (Stylus and Solidity)

## Quick Start

```bash
bash <(curl -s https://raw.githubusercontent.com/hummusonrails/arbitrum-dapp-skill/main/install.sh)
```

Then start Claude Code and ask it to build something:

```
> Create a Stylus contract for an ERC-20 token with a React frontend
```

That's it. The skill loads automatically.

<details>
<summary><strong>Install from ClawHub</strong></summary>

<br>

```bash
npx clawhub@latest install arbitrum-dapp-skill
```

Or browse the skill on [ClawHub](https://clawhub.ai/hummusonrails/arbitrum-dapp-skill).

</details>

<details>
<summary><strong>Manual installation</strong></summary>

<br>

```bash
git clone https://github.com/hummusonrails/arbitrum-dapp-skill.git ~/.claude/skills/arbitrum-dapp-skill
```

</details>

## Stack

| Layer | Tool | Notes |
|:------|:-----|:------|
| Smart contracts (Rust) | `stylus-sdk` v0.10+ | Compiled to WASM, runs on Stylus VM |
| Smart contracts (Solidity) | Solidity 0.8.x + Foundry | Standard EVM path on Arbitrum |
| Local chain | `nitro-devnode` | Docker-based with pre-funded accounts |
| Contract CLI | `cargo-stylus` | Check, deploy, export-abi |
| Contract toolchain | `forge` / `cast` | Build, test, deploy, interact |
| Frontend | viem + wagmi | Type-safe chain interaction |
| Package manager | pnpm | Workspace-friendly, fast |

<details>
<summary><strong>Prerequisites</strong></summary>

<br>

The skill will guide you through installing these, but for reference:

- [Rust](https://rustup.rs/) 1.81+
- [cargo-stylus](https://github.com/OffchainLabs/stylus-sdk-rs): `cargo install --force cargo-stylus`
- [Foundry](https://book.getfoundry.sh/getting-started/installation): `curl -L https://foundry.paradigm.xyz | bash && foundryup`
- [Docker](https://www.docker.com/products/docker-desktop/) for the local devnode
- [Node.js](https://nodejs.org/) 20+ and [pnpm](https://pnpm.io/)

</details>

## Usage examples

Once installed, start a Claude Code session and try:

```
> Help me create a new Arbitrum dApp
> Write a Stylus contract that implements an ERC-20 token
> Set up my local devnode and deploy my contract
> Add a frontend that reads from my deployed contract
> Help me write tests for my Stylus contract
```

## Skill structure

```
arbitrum-dapp-skill/
├── SKILL.md                            # Main skill definition
├── references/
│   ├── stylus-rust-contracts.md        # Stylus SDK patterns and examples
│   ├── solidity-contracts.md           # Solidity on Arbitrum + Foundry
│   ├── frontend-integration.md         # viem + wagmi patterns
│   ├── local-devnode.md                # Nitro devnode setup
│   ├── deployment.md                   # Testnet and mainnet deployment
│   └── testing.md                      # Testing strategies
├── install.sh
└── README.md
```

## Resources

| Resource | Description |
|:---------|:------------|
| [Demo Video](https://www.youtube.com/watch?v=vsejiaOTmJA) | Watch the skill in action |
| [Arbitrum Stylus Quickstart](https://docs.arbitrum.io/stylus/quickstart) | Official getting-started guide |
| [Stylus SDK](https://github.com/OffchainLabs/stylus-sdk-rs) | Rust SDK for writing Stylus contracts |
| [Stylus Workshop](https://github.com/ArbitrumFoundation/stylus-workshop-gol) | Game of Life example project |
| [Nitro Devnode](https://github.com/OffchainLabs/nitro-devnode) | Local Arbitrum chain for development |
| [viem](https://viem.sh) | TypeScript interface for Ethereum |
| [wagmi](https://wagmi.sh) | React hooks for Ethereum |

## Contributing

Contributions welcome. Open an [issue](https://github.com/hummusonrails/arbitrum-dapp-skill/issues) or submit a [pull request](https://github.com/hummusonrails/arbitrum-dapp-skill/pulls).

## License

[MIT](LICENSE)
