/** Runs `fn` over `items` with at most `concurrency` in flight at once, preserving input order in the result. */
export async function mapWithConcurrency<T, R>(
  items: T[],
  concurrency: number,
  fn: (item: T, index: number) => Promise<R>,
): Promise<R[]> {
  const results: R[] = new Array(items.length);
  let next = 0;

  async function worker() {
    for (;;) {
      const i = next++;
      if (i >= items.length) return;
      results[i] = await fn(items[i], i);
    }
  }

  await Promise.all(Array.from({ length: Math.min(concurrency, items.length) }, worker));
  return results;
}

/** Validates that a string looks like an EVM address: `0x` followed by exactly 40 hex characters. */
export function isValidAddress(address: string): boolean {
  return /^0x[a-fA-F0-9]{40}$/.test(address);
}

/**
 * Reduces a thrown value to a single-line message, for both CLI error output
 * and MCP tool error results. viem errors (the common case here — a failed
 * RPC call) carry a concise `.shortMessage` but their `.message` is a
 * multi-paragraph dump of docs links, metaMessages, and version info;
 * surfacing that (or the raw Error, stack trace and all) buries the actual
 * problem in noise.
 */
export function formatError(err: unknown): string {
  if (err instanceof Error) {
    const shortMessage = (err as { shortMessage?: unknown }).shortMessage;
    return typeof shortMessage === "string" ? shortMessage : err.message;
  }
  return String(err);
}

/**
 * Pads `value` to `width` for a fixed-width table column, truncating with an
 * ellipsis first if it's already at or past `width`.
 *
 * Pool symbols come straight from on-chain token metadata with no length
 * limit, and `String.prototype.padEnd` is a no-op once the input reaches the
 * target width — so an 18-character-or-longer symbol (several already exist
 * in live data, e.g. `vAMM-VIRTUAL/cbBTC`) printed with a bare `.padEnd(18)`
 * runs straight into the next column with no separator, merging the two in
 * the CLI's human-readable table output. Truncating first guarantees at least
 * one space of separation regardless of how long the value is.
 */
export function padCol(value: string, width: number): string {
  if (value.length < width) return value.padEnd(width);
  if (width <= 2) return value.slice(0, width);
  return `${value.slice(0, width - 2)}…`.padEnd(width);
}

