# Changelog

## [2.0.4] — 2026-02-10

### Security / Safety
- Added a CI-safe regression test to ensure `PRIVATE_KEY` is never printed to stdout/stderr.
- Docs: Treat stdout/stderr as public logs (CI, terminals, chat).

## [2.0.3] — 2026-02-09

### Security / Safety
- **Bytecode preflight:** All scripts now verify critical contract bytecode (router/quoter/Permit2/StateView + ERC20s) before proceeding. This reduces wrong-RPC / wrong-chain foot-guns.

### Docs
- Corrected shipped address reference table.

### Tests
- Added unit tests for `assertHasBytecode`.

## [2.0.2] — 2026-02-09

### Fixes
- **RPC provider:** Pin providers to a static network (ethers v6 `staticNetwork: true`) to avoid noisy network auto-detection retries on flaky RPCs.

### Dev / Security
- **vitest:** Bumped to `^3.2.4`.

### Tests
- Added unit tests for RPC provider helpers (chainId parsing, mismatch + error wrapping).

## [2.0.1] — 2026-02-09

### Fixes
- **swap.ts:** `--recipient` is now honored — swap output can be routed to a custom address via **TAKE (0x0e)** with OPEN_DELTA (amount=0)
- **swap.ts:** `--json` mode now exits **non-zero** on failures (no pool / quote failure / tx revert)
- **Security:** CLI now rejects both `--private-key <value>` and **`--private-key=<value>`** forms (prevents accidental key exposure in process table)

### Tests
- Added unit tests covering TAKE vs TAKE_ALL encoding and the `--private-key=value` bypass vector

## [2.0.0] — 2026-02-08

### 🔄 Complete TypeScript Rewrite

**Breaking Changes:**
- All scripts rewritten from bash/Python to TypeScript (run with `npx tsx`)
- Removed dependency on `cast` (Foundry CLI) and Python — now pure Node.js
- CLI syntax changed: use `npx tsx src/<script>.ts` instead of `./scripts/<script>.sh`
- Private key MUST be set via `PRIVATE_KEY` env var — `--private-key` flag rejected

**New Features:**
- **V4Quoter integration** — proper on-chain quoting for accurate swap output estimation
- **Auto-approve** — `--auto-approve` flag on swap.ts handles Permit2 flow automatically
- **Best pool selection** — pool discovery sorted by liquidity (not first match)
- **Base Sepolia support** — testnet chain for development
- **Full test suite** — unit, fork (Anvil), testnet, and mainnet smoke tests
- **CI/CD pipeline** — lint, typecheck, unit tests, fork tests, security scan
- **Security scan** — automated check for eval(), exec(), hardcoded secrets

**Security Fixes (from PhD Review + Pentest):**
- PT-001: Bash arithmetic injection → ELIMINATED (TypeScript rewrite)
- PT-002: Integer overflow → BigInt everywhere (no 64-bit limits)
- PT-003: Private key in process table → env var only
- C-01: Pool discovery via StateView (not nonexistent PoolManager.getSlot0)
- C-02: Correct V4 action bytes (SETTLE_ALL = 0x0c, not 0x0b)
- C-03: Proper quoting via V4Quoter (not input-amount-as-output)
- C-04: Clean ABI encoding via ethers AbiCoder (not bash/cast nesting)
- H-01: Canonical Uniswap V4 addresses from official deployment docs
- H-02: Fixed v4-encoding.md action byte table
- M-01: Best pool by liquidity (not first match)
- M-04: Dynamic fee pools searched with multiple tick spacings (60, 200, 10)
- M-05: Consistent Permit2 expiry (max uint48)

**Technical:**
- TypeScript strict mode (`"strict": true`)
- ES2022 target, NodeNext modules
- ethers v6 for all on-chain interaction
- BigInt for ALL token amounts
- vitest for testing
- eslint + @typescript-eslint for linting

## [1.0.0] — 2026-02-07

### Initial Release (bash)
- Pool info reading via extsload
- Pool discovery across fee tiers
- Swap execution via Universal Router (bash + cast)
- Permit2 approval flow
- Multiple critical bugs (see PhD review)
