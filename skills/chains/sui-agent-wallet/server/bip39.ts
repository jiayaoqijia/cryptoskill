/**
 * BIP39 Mnemonic utilities
 * Using @scure/bip39 for secure mnemonic generation
 */

import { generateMnemonic as _generateMnemonic, mnemonicToSeedSync as _mnemonicToSeedSync, validateMnemonic as _validateMnemonic } from '@scure/bip39';
import { wordlist } from '@scure/bip39/wordlists/english';

export function generateMnemonic(strength: number = 128): string {
  // 128 bits = 12 words, 256 bits = 24 words
  return _generateMnemonic(wordlist, strength);
}

export function mnemonicToSeedSync(mnemonic: string, passphrase?: string): Uint8Array {
  return _mnemonicToSeedSync(mnemonic, passphrase);
}

export function validateMnemonic(mnemonic: string): boolean {
  return _validateMnemonic(mnemonic, wordlist);
}
