import { withPortkeyRecoveryHint } from './lib/error-hints.js';

/**
 * CLI output helpers.
 * Standardized JSON output for success, structured error for failure.
 */

export function outputSuccess(data: unknown): void {
  console.log(JSON.stringify({ status: 'success', data }, null, 2));
}

export function outputError(message: string): void {
  console.error(`[ERROR] ${withPortkeyRecoveryHint(message)}`);
  process.exit(1);
}

/**
 * Safe JSON.parse with a user-friendly error message.
 * Use this for all CLI options that accept JSON strings.
 */
export function safeJsonParse(raw: string, paramName: string): unknown {
  try {
    return JSON.parse(raw);
  } catch {
    outputError(`Invalid JSON for --${paramName}: ${raw.slice(0, 200)}`);
    return undefined; // unreachable — outputError exits
  }
}
