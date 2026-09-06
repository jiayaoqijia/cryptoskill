export const SIGNER_ERROR_CODES = {
  CONTEXT_NOT_FOUND: 'SIGNER_CONTEXT_NOT_FOUND',
  PASSWORD_REQUIRED: 'SIGNER_PASSWORD_REQUIRED',
  CONTEXT_INVALID: 'SIGNER_CONTEXT_INVALID',
  DAEMON_NOT_IMPLEMENTED: 'SIGNER_DAEMON_NOT_IMPLEMENTED',
  CONTEXT_LOCK_TIMEOUT: 'SIGNER_CONTEXT_LOCK_TIMEOUT',
} as const;

export type SignerErrorCode =
  (typeof SIGNER_ERROR_CODES)[keyof typeof SIGNER_ERROR_CODES];

export function formatSignerError(code: SignerErrorCode, message: string): string {
  return `${code}: ${message}`;
}
