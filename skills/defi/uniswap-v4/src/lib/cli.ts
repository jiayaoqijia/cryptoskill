/**
 * Minimal CLI argument parser.
 * Zero dependencies — implements --flag value, --flag=value, and --boolean-flag.
 */

import path from "node:path";
import { fileURLToPath } from "node:url";

/**
 * Returns true if a module is being executed directly (vs imported).
 * Useful for CLI scripts that also export functions for tests.
 */
export function isMain(
  importMetaUrl: string,
  argv1: string | undefined = process.argv[1]
): boolean {
  if (!argv1) return false;
  try {
    const thisFile = fileURLToPath(importMetaUrl);
    const entryFile = path.resolve(argv1);
    return thisFile === entryFile;
  } catch {
    return false;
  }
}

export interface ParsedArgs {
  /** Named flags: --key value or --key=value */
  flags: Record<string, string>;
  /** Positional arguments */
  positional: string[];
  /** Boolean flags present */
  booleans: Set<string>;
}

/**
 * Parse process.argv (skipping node + script path).
 *
 * Boolean flag names must be declared so we don't consume the next arg as a value.
 */
export function parseArgs(
  argv: string[] = process.argv.slice(2),
  booleanFlags: string[] = ["json", "help", "h", "auto-approve"]
): ParsedArgs {
  const flags: Record<string, string> = {};
  const positional: string[] = [];
  const booleans = new Set<string>();
  const boolSet = new Set(booleanFlags);

  let i = 0;
  while (i < argv.length) {
    const arg = argv[i];
    if (arg === "--private-key" || arg.startsWith("--private-key=")) {
      throw new Error(
        "--private-key CLI flag is disabled for security (visible in ps output). " +
        "Set PRIVATE_KEY environment variable instead."
      );
    }
    if (arg.startsWith("--")) {
      const eqIdx = arg.indexOf("=");
      if (eqIdx !== -1) {
        // --key=value
        const key = arg.slice(2, eqIdx);
        flags[key] = arg.slice(eqIdx + 1);
        i++;
      } else {
        const key = arg.slice(2);
        if (boolSet.has(key)) {
          booleans.add(key);
          i++;
        } else if (i + 1 < argv.length && !argv[i + 1].startsWith("--")) {
          flags[key] = argv[i + 1];
          i += 2;
        } else {
          booleans.add(key);
          i++;
        }
      }
    } else if (arg.startsWith("-") && arg.length === 2) {
      const key = arg.slice(1);
      if (boolSet.has(key)) {
        booleans.add(key);
        i++;
      } else if (i + 1 < argv.length) {
        flags[key] = argv[i + 1];
        i += 2;
      } else {
        booleans.add(key);
        i++;
      }
    } else {
      positional.push(arg);
      i++;
    }
  }
  return { flags, positional, booleans };
}

/** Log to stderr (keeps stdout clean for JSON). */
export function log(...args: unknown[]): void {
  process.stderr.write(args.map(String).join(" ") + "\n");
}

/** Print error and exit. */
export function fatal(msg: string): never {
  process.stderr.write(`ERROR: ${msg}\n`);
  process.exit(1);
}
