/**
 * macOS Keychain integration for secure seed phrase storage
 */

import { execSync } from 'child_process';

const SERVICE_NAME = 'sui-agent-wallet';
const ACCOUNT_NAME = 'mnemonic';

/**
 * Store seed phrase in macOS Keychain
 */
export function storeMnemonic(mnemonic: string): boolean {
  try {
    // First try to delete existing entry (ignore errors)
    try {
      execSync(`security delete-generic-password -s "${SERVICE_NAME}" -a "${ACCOUNT_NAME}" 2>/dev/null`);
    } catch {}
    
    // Add new entry
    execSync(
      `security add-generic-password -s "${SERVICE_NAME}" -a "${ACCOUNT_NAME}" -w "${mnemonic}"`,
      { stdio: 'pipe' }
    );
    console.log('✅ Seed phrase stored in macOS Keychain');
    return true;
  } catch (e: any) {
    console.error('Failed to store in Keychain:', e.message);
    return false;
  }
}

/**
 * Retrieve seed phrase from macOS Keychain
 */
export function retrieveMnemonic(): string | null {
  try {
    const result = execSync(
      `security find-generic-password -s "${SERVICE_NAME}" -a "${ACCOUNT_NAME}" -w`,
      { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] }
    );
    return result.trim();
  } catch {
    return null;
  }
}

/**
 * Delete seed phrase from Keychain
 */
export function deleteMnemonic(): boolean {
  try {
    execSync(`security delete-generic-password -s "${SERVICE_NAME}" -a "${ACCOUNT_NAME}"`);
    return true;
  } catch {
    return false;
  }
}

/**
 * Check if seed phrase exists in Keychain
 */
export function hasMnemonic(): boolean {
  return retrieveMnemonic() !== null;
}
