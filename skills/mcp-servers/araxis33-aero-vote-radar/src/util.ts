import { getAddress } from "viem";

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
 * Normalizes a syntactically valid address (any letter case) to its canonical
 * EIP-55 checksum casing. viem's own contract calls validate that a mixed-case
 * address matches its checksum and throw a raw "Address ... is invalid" error
 * otherwise — so an address that merely *looks* valid per `isValidAddress`
 * (e.g. typed or pasted in all-uppercase, or any case that isn't the exact
 * checksum) would pass this project's own validation and then crash deep
 * inside viem instead of returning a clean result. Callers should validate with
 * `isValidAddress` first (this assumes that already holds) and normalize with
 * this before the address reaches any on-chain call.
 */
export function normalizeAddress(address: string): `0x${string}` {
  return getAddress(address);
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

/**
 * Breaks a paragraph onto lines no longer than `width`, on spaces only.
 *
 * The CLI's own output is hand-formatted to fit a terminal, but explanatory
 * prose written once and printed in two places (here and, in a different shape,
 * on the web page) cannot carry its own line breaks without one of the two
 * surfaces wearing the other's. So the text is stored as one paragraph and
 * wrapped where it is printed.
 *
 * A word longer than `width` is left on its own line rather than cut: a broken
 * URL or contract address is worse than a long line.
 */
export function wrapText(text: string, width: number): string {
  const lines: string[] = [];
  let line = "";

  for (const word of text.split(/\s+/).filter(Boolean)) {
    if (line === "") {
      line = word;
    } else if (line.length + 1 + word.length <= width) {
      line += ` ${word}`;
    } else {
      lines.push(line);
      line = word;
    }
  }
  if (line !== "") lines.push(line);

  return lines.join("\n");
}

