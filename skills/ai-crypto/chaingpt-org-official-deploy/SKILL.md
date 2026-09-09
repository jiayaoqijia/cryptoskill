---
name: deploy
description: "Deploy Solidity contracts to MAINNET (or testnet) safely via the ChainGPT plugin. End-to-end: generate → audit → compile → estimate → build unsigned tx → user signs → verify on Etherscan. MAINNET is the default; the audit gate is mandatory for mainnet deploys. The plugin never holds private keys — the user signs externally via MetaMask / Rabby / hardware wallet / ERC-4337 smart account. Triggers: deploy contract, ship contract, deploy to mainnet, deploy to ethereum, deploy to base, deploy to bsc, verify contract, mainnet deploy, contract deployment."
---

# ChainGPT Deploy Skill

You orchestrate Solidity-contract deployment to **real mainnet chains** through the ChainGPT plugin. This skill is mainnet-first by design — testnet is an opt-in via the `network` parameter, never the default behavior.

The plugin is **custody-free**: it builds an unsigned transaction object and returns it. The user signs and broadcasts via their own wallet (MetaMask, Rabby, hardware wallet, ERC-4337 smart account, WalletConnect). Never ask the user for a private key. Never accept one in a tool argument.

## The mandatory pipeline

```
chaingpt_generate_contract       (optional — if generating from description)
       │
       ▼
chaingpt_audit_contract          ← MANDATORY for mainnet. Costs 1 credit. Never skip.
       │
       ▼
chaingpt_deploy_compile          ← solc 0.8.x, returns bytecode + ABI
       │
       ▼
chaingpt_deploy_estimate         ← gas + USD cost on the chosen mainnet
       │
       ▼
chaingpt_deploy_build_tx         ← MAINNET REFUSES unless acknowledgeMainnet: true
       │
       ▼
[user signs externally + broadcasts]
       │
       ▼
chaingpt_deploy_verify           ← submit source to Etherscan v2 multichain
       │
       ▼
chaingpt_deploy_verify_status    ← poll until ✓ Pass — Verified
```

## Hard rules for mainnet

1. **Never call `chaingpt_deploy_build_tx` with a mainnet network and `acknowledgeMainnet=true` until you have surfaced the audit report to the user.** If the audit raised any high-severity finding, refuse to proceed until the user explicitly waives it.
2. **Always surface the estimated cost in USD before the build-tx step.** Pull from `chaingpt_deploy_estimate` and convert via the current native-coin price.
3. **Echo the constructor args back to the user in plain English** before the build-tx step. ("You're about to deploy `MyToken` with name='X', symbol='Y', initialSupply=1,000,000 * 10**18 to mainnet Ethereum. Confirm?")
4. **Echo the deployer address back** and remind the user it must be the wallet they control.
5. **Default to testnet only when the user explicitly says "test", "testnet", "dry run", or names a testnet chain (sepolia, base-sepolia, etc.).** Anything else is mainnet.

## Supported networks

**Mainnets (default targets):** ethereum, base, arbitrum, optimism, polygon, bsc, avalanche, blast, linea, scroll.

**Testnets (opt-in):** sepolia, base-sepolia, arbitrum-sepolia, optimism-sepolia, polygon-amoy, bsc-testnet.

## Setup

- `CHAINGPT_API_KEY` — required for the audit step.
- `ETHERSCAN_API_KEY` — required for `chaingpt_deploy_verify`. Free at https://etherscan.io/myapikey. Works across all EVM chains via Etherscan v2.
- No `MORALIS_API_KEY` needed for deploy.

## Typical mainnet deploy session

```
User:  "Deploy an ERC-20 called CGPT2 with 100M supply to Base."

You:   1. chaingpt_generate_contract description="ERC-20 named CGPT2, symbol CGPT2, 100M supply, owner-mintable"
       2. chaingpt_audit_contract sourceCode=<generated>   →  surface findings
       3. (if no critical issues) chaingpt_deploy_compile source=<generated>
       4. chaingpt_deploy_estimate bytecode=<bytecode> constructorAbi=<...> constructorArgs=[…] network="base"
          → "Estimated cost: 0.0042 ETH (~$10 at current price)"
       5. Wait for user confirmation. ("Are you sure you want to deploy to mainnet Base?")
       6. chaingpt_deploy_build_tx … network="base" acknowledgeMainnet=true
          → returns unsigned tx JSON
       7. User signs externally + broadcasts. Tx hash returned.
       8. chaingpt_deploy_verify address=<deployed> source=<src> contractName="CGPT2" compilerVersion="v0.8.24+..." network="base"
       9. chaingpt_deploy_verify_status guid=<guid> network="base"  →  ✓ Verified
```

## When NOT to use this skill

- If the user already has a Foundry / Hardhat workflow set up locally and just wants the contract source generated — point them to `chaingpt_generate_contract` and stop.
- If the user is deploying a brand-new factory pattern or proxy upgrade — those require manual review beyond the audit tool. Recommend a human auditor.
- For Solana program deployment — this skill is EVM-only.

## Verification troubleshooting

The most common failure of `chaingpt_deploy_verify` is a constructor-args mismatch. The `constructorArgs` param must be the **ABI-encoded** hex (without leading 0x), not the raw values. The simplest way to get this string: take the `data` field from the `build_tx` output, then strip the bytecode prefix — what's left is your ABI-encoded constructor args.

If verification stays pending for more than 60 seconds, the most likely cause is a compiler-version mismatch — the `compilerVersion` param must be the FULL long string (e.g. `v0.8.24+commit.e11b9ed9`), which you can get from the `solcVersion` field of `chaingpt_deploy_compile`'s response.
