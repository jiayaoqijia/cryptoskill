/**
 * Input validation — every user-facing parameter is validated before use.
 * Eliminates PT-001 (injection), PT-002 (overflow), PT-012 (address format).
 * Uses BigInt exclusively for token amounts — never floating point.
 */

const ADDRESS_RE = /^0x[0-9a-fA-F]{40}$/;
const INTEGER_RE = /^[0-9]+$/;

/** Validate an Ethereum address (0x + 40 hex chars). */
export function validateAddress(value: string, name: string): string {
  if (!ADDRESS_RE.test(value)) {
    throw new Error(
      `--${name} must be a valid Ethereum address (0x + 40 hex chars). Got: '${value}'`
    );
  }
  return value;
}

/**
 * Resolve a token input: "ETH"/"eth" → address(0), otherwise validate as address.
 */
export function resolveTokenInput(value: string, name: string): string {
  const lower = value.toLowerCase();
  if (lower === "eth" || lower === "0x0") {
    return "0x0000000000000000000000000000000000000000";
  }
  return validateAddress(value, name);
}

/**
 * Parse an amount string to BigInt.
 * Accepts integer strings only (no decimals, no scientific notation).
 * Bounds check: must be > 0 and ≤ 2^128 - 1 (uint128 max for V4).
 */
export function parseAmount(value: string, name: string): bigint {
  if (!INTEGER_RE.test(value)) {
    throw new Error(
      `--${name} must be a non-negative integer (wei). Got: '${value}'`
    );
  }
  const n = BigInt(value);
  if (n <= 0n) {
    throw new Error(`--${name} must be > 0. Got: ${value}`);
  }
  const UINT128_MAX = (1n << 128n) - 1n;
  if (n > UINT128_MAX) {
    throw new Error(
      `--${name} exceeds uint128 max (${UINT128_MAX}). Got: ${value}`
    );
  }
  return n;
}

/**
 * Parse slippage in basis points (0-10000).
 * 50 = 0.5%, 100 = 1%, 10000 = 100%.
 */
export function parseSlippage(value: string): number {
  if (!INTEGER_RE.test(value)) {
    throw new Error(`--slippage must be a non-negative integer (bps). Got: '${value}'`);
  }
  const n = Number(value);
  if (n < 0 || n > 10000) {
    throw new Error(`--slippage must be 0-10000 bps. Got: ${n}`);
  }
  if (n === 10000) {
    // Warn but allow — zero protection
    process.stderr.write("WARNING: slippage=10000 bps means ZERO price protection.\n");
  }
  return n;
}

/** Validate chain parameter. */
export function validateChain(value: string): string {
  const SUPPORTED = ["base", "ethereum", "base-sepolia"];
  if (!SUPPORTED.includes(value)) {
    throw new Error(
      `Unsupported chain: '${value}'. Supported: ${SUPPORTED.join(", ")}`
    );
  }
  return value;
}

/**
 * Compute minimum output with slippage (BigInt-safe).
 * minOut = expectedOut * (10000 - slippageBps) / 10000
 * Always returns ≥ 1 for nonzero expectedOut (prevents 0-protection swaps).
 */
export function applySlippage(expectedOut: bigint, slippageBps: number): bigint {
  if (expectedOut <= 0n) return 0n;
  const minOut = (expectedOut * BigInt(10000 - slippageBps)) / 10000n;
  return minOut > 0n ? minOut : 1n;
}

/**
 * Sort two currency addresses for V4 PoolKey (currency0 < currency1 by numeric value).
 * Returns [currency0, currency1, zeroForOne].
 * zeroForOne = true when tokenIn is currency0.
 */
export function sortCurrencies(
  tokenIn: string,
  tokenOut: string
): { currency0: string; currency1: string; zeroForOne: boolean } {
  const inBig = BigInt(tokenIn);
  const outBig = BigInt(tokenOut);
  if (inBig === outBig) {
    throw new Error("tokenIn and tokenOut must be different.");
  }
  if (inBig < outBig) {
    return { currency0: tokenIn, currency1: tokenOut, zeroForOne: true };
  }
  return { currency0: tokenOut, currency1: tokenIn, zeroForOne: false };
}

/**
 * Get the private key from environment (never CLI).
 * Fixes PT-003: private key exposure in process listing.
 */
export function getPrivateKey(): string {
  const key = process.env.PRIVATE_KEY;
  if (!key) {
    throw new Error(
      "PRIVATE_KEY environment variable required. Never pass private keys as CLI arguments."
    );
  }
  if (!key.startsWith("0x") || key.length !== 66) {
    throw new Error("PRIVATE_KEY must be 0x-prefixed and 64 hex chars (32 bytes).");
  }
  return key;
}
