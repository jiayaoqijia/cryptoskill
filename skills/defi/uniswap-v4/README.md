# Uniswap V4 Skill (OpenClaw)

Swap tokens and read pool state on **Uniswap V4** on **Base** and **Ethereum mainnet**.

Production-grade TypeScript rewrite with strict types, full test suite, and CI/CD.

## Install (recommended)

Install into an OpenClaw skills directory:

```bash
clawhub install uniswap-v4
```

## Quick Start (from this repo)

```bash
npm install

# Read pool state (no key needed)
npx tsx src/pool-info.ts --token0 ETH --token1 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 --chain base --rpc https://mainnet.base.org

# Quote a swap
npx tsx src/quote.ts --token-in ETH --token-out 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 --amount 10000000000000000 --rpc https://mainnet.base.org

# Execute a swap
PRIVATE_KEY=0x... npx tsx src/swap.ts --token-in ETH --token-out 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 --amount 10000000000000000 --rpc https://mainnet.base.org --json
```

## Documentation

See **[`SKILL.md`](./SKILL.md)** for full documentation: decision tree, all scripts with usage, env vars, architecture notes, and error handling.

## Testing

```bash
# Unit tests (no network required)
npm run test:unit

# Fork tests (requires Foundry/Anvil)
# If you installed Foundry via foundryup, you may need:
export PATH="$HOME/.foundry/bin:$PATH"

anvil --fork-url https://mainnet.base.org --port 8545 &
npm run test:fork

# Testnet reads (Base Sepolia)
npm run test:testnet

# Mainnet smoke tests (read-only)
npm run test:mainnet

# Full suite
npm test
```

## Development

```bash
npm run typecheck    # tsc --noEmit --strict
npm run lint         # eslint
npm run security     # security scan for eval/exec/hardcoded keys
```

## Architecture

```
src/
  swap.ts          — Execute swaps via Universal Router
  quote.ts         — Quote amounts via V4Quoter
  pool-info.ts     — Read pool state via StateView
  approve.ts       — Permit2 approval flow
  lib/
    v4-encoding.ts — V4 ABI encoding (actions, params, settle/take)
    addresses.ts   — Contract addresses per chain
    validation.ts  — Input validation, BigInt parsing, slippage
    cli.ts         — CLI argument parser

tests/
  unit/            — Encoding, validation, address tests
  fork/            — Anvil fork integration tests (real swaps)
  testnet/         — Base Sepolia contract verification
  mainnet/         — Live read-only smoke tests
```

## SECURITY

**Secrets / private keys**
- `PRIVATE_KEY` must be provided via an environment variable or secret manager only.
- **Never** paste or send `PRIVATE_KEY` in chat.
- **Never** commit `PRIVATE_KEY` (or `.env` files) to git.
- Treat **stdout/stderr as public logs** (CI, terminals, chat). This skill is tested to ensure `PRIVATE_KEY` is never printed.

Key security hardening included (validated by tests + `npm run security`):

- **PT-001**: Bash arithmetic injection → eliminated (TypeScript, no shell)
- **PT-002**: Integer overflow → BigInt (arbitrary precision)
- **PT-003**: Private key in ps → env var only, `--private-key` flag rejected
- **C-01**: Wrong pool discovery → StateView contract
- **C-02**: Wrong action bytes → verified against Actions.sol (SETTLE_ALL=0x0c)
- **C-03**: Broken slippage → V4Quoter for proper quoting
- **C-04**: Bad ABI encoding → ethers AbiCoder
- **H-01**: Non-canonical addresses → official Uniswap deployment addresses

## License

MIT
