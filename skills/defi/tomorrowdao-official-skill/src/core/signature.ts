import AElf from 'aelf-sdk';
import { SkillError } from './errors.js';
import type { SignaturePayload } from './types.js';

const SIGN_TEXT_PREFIX = `Welcome to TMRWDAO! Click to sign in to the TMRWDAO platform! This request will not trigger any blockchain transaction or cost any gas fees.\n\nsignature: `;

function toSignatureHex(privateKey: string, data: string): string {
  const keypair = AElf.wallet.ellipticEc.keyFromPrivate(privateKey);
  const signedMsgObject = keypair.sign(data);
  return [
    signedMsgObject.r.toString(16, 64),
    signedMsgObject.s.toString(16, 64),
    `0${signedMsgObject.recoveryParam.toString()}`,
  ].join('');
}

export function getWalletByPrivateKey(privateKey: string) {
  if (!privateKey || privateKey.replace(/^0x/, '').length !== 64) {
    throw new SkillError('INVALID_PRIVATE_KEY', 'TMRW_PRIVATE_KEY is invalid or missing');
  }
  return AElf.wallet.getWalletByPrivateKey(privateKey.replace(/^0x/, ''));
}

export function buildSignaturePayload(privateKey: string, timestamp = Date.now()): SignaturePayload {
  const wallet = getWalletByPrivateKey(privateKey);
  const address = wallet.address;
  const plainTextOrigin = `${address}-${timestamp}`;

  // This format follows the same client-side flow as tomorrowDAO-interface.
  const signInfo = AElf.utils.sha256(plainTextOrigin);
  const signature = toSignatureHex(privateKey.replace(/^0x/, ''), signInfo);

  const publicKey = wallet.keyPair.getPublic('hex');
  if (!publicKey) {
    throw new SkillError('SIGN_ERROR', 'Failed to derive public key from private key');
  }

  return {
    timestamp,
    address,
    publicKey,
    signature,
  };
}

/**
 * @public
 * @legacy
 * Kept for legacy SDK consumers that still sign raw timestamp payloads.
 */
export function buildLegacyTimestampSignature(privateKey: string, timestamp: number): SignaturePayload {
  const wallet = getWalletByPrivateKey(privateKey);
  const signature = toSignatureHex(privateKey.replace(/^0x/, ''), String(timestamp));
  const publicKey = wallet.keyPair.getPublic('hex');
  return {
    timestamp,
    address: wallet.address,
    publicKey,
    signature,
  };
}

/**
 * @public
 * @legacy
 * Kept for SDK consumers that need the client-side auth prompt message.
 */
export function getAuthSigningMessage(address: string, timestamp: number): string {
  return `${SIGN_TEXT_PREFIX}${address}-${timestamp}`;
}
