/**
 * Output utilities for agent-friendly CLI.
 *
 * - TTY detection: auto-switch to JSON when stdout is piped
 * - Structured errors: JSON error objects when in JSON mode
 * - Field masking: filter output fields to reduce token consumption
 * - Human output goes to stderr, structured data to stdout
 */

/** Check if JSON mode is active (explicit --json flag OR piped stdout) */
export function isJsonMode(options: { json?: boolean }): boolean {
  if (options.json) return true;
  // Auto-detect: if stdout is not a TTY (piped), default to JSON
  if (!process.stdout.isTTY) return true;
  return false;
}

/** Write human-readable messages to stderr (never pollutes stdout for piped JSON) */
export function info(message: string): void {
  process.stderr.write(message + '\n');
}

/**
 * Write structured JSON result to stdout.
 * Supports field masking via --fields option.
 */
export function jsonOut(data: unknown, fields?: string): void {
  if (fields) {
    const allowed = fields.split(',').map(f => f.trim());
    if (Array.isArray(data)) {
      data = (data as Record<string, unknown>[]).map(obj => filterFields(obj, allowed));
    } else if (typeof data === 'object' && data !== null) {
      data = filterFields(data as Record<string, unknown>, allowed);
    }
  }
  process.stdout.write(JSON.stringify(data, null, 2) + '\n');
}

/** Write a structured JSON error to stdout and exit with specific code */
export function jsonError(code: ExitCode, message: string, details?: Record<string, unknown>): never {
  const error = {
    ok: false,
    error: { code, message, ...details }
  };
  process.stdout.write(JSON.stringify(error, null, 2) + '\n');
  process.exit(code);
}

function filterFields(obj: Record<string, unknown>, fields: string[]): Record<string, unknown> {
  const filtered: Record<string, unknown> = {};
  for (const field of fields) {
    if (field in obj) {
      filtered[field] = obj[field];
    }
  }
  return filtered;
}

/**
 * Meaningful exit codes beyond 0/1.
 * Agents can branch on these to decide next action.
 */
export enum ExitCode {
  SUCCESS = 0,
  GENERAL_ERROR = 1,
  NOT_AUTHENTICATED = 2,
  WALLET_NOT_FOUND = 3,
  PROVIDER_NOT_INSTALLED = 4,
  INVALID_INPUT = 5,
  ENCRYPTION_ERROR = 6,
  NETWORK_ERROR = 7,
  ALREADY_EXISTS = 8,
}
