import { SIGNER_ERROR_CODES } from '../../lib/signer-error-codes';

const MESSAGE_CODE_ALLOWLIST = new Set<string>([
  ...Object.values(SIGNER_ERROR_CODES),
  'INVALID_PARAMS',
  'UNKNOWN_ERROR',
]);

export type McpErrorPayload = {
  code: string;
  message: string;
  details?: unknown;
  traceId?: string;
};

export function toMcpError(err: unknown): McpErrorPayload {
  const fallback: McpErrorPayload = {
    code: 'UNKNOWN_ERROR',
    message: String(err),
    details: undefined,
    traceId: undefined,
  };
  if (!err || typeof err !== 'object') return fallback;

  const record = err as Record<string, unknown>;
  const rawMessage =
    typeof record.message === 'string' ? record.message : fallback.message;
  const explicitCode = typeof record.code === 'string' ? record.code : '';

  let code = explicitCode;
  let message = rawMessage;

  if (!code) {
    const prefixed = rawMessage.match(/^([A-Z0-9_]+):\s*(.*)$/);
    const prefixedCode = prefixed?.[1];
    if (prefixedCode && MESSAGE_CODE_ALLOWLIST.has(prefixedCode)) {
      code = prefixedCode;
      message = prefixed?.[2] || prefixedCode;
    }
  }

  return {
    code: code || 'UNKNOWN_ERROR',
    message,
    details: record.details,
    traceId: typeof record.traceId === 'string' ? record.traceId : undefined,
  };
}

export function fail(err: unknown) {
  const parsed = toMcpError(err);
  return {
    content: [
      { type: 'text' as const, text: `[ERROR] ${parsed.code}: ${parsed.message}` },
      { type: 'text' as const, text: JSON.stringify({ error: parsed }, null, 2) },
    ],
    isError: true as const,
  };
}
