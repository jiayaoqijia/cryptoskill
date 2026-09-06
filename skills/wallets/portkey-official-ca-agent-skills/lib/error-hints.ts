/**
 * Add stable operator hints for common Portkey recovery failures.
 */
export function withPortkeyRecoveryHint(message: string): string {
  if (!message) return 'Unknown error';

  if (message.includes('Please complete the approval of all guardians')) {
    return `${message} Hint: ensure guardian approvals meet threshold and each proof was generated with verify-code --operation recovery.`;
  }

  if (message.includes('Error mapping types') && message.includes('GuardianApproved')) {
    return `${message} Hint: guardiansApproved must include identifier, type, verifierId, verificationDoc, and signature for each guardian.`;
  }

  return message;
}
