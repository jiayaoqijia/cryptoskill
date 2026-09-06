import { strict as assert } from 'node:assert';
import {
  clearCaches,
  createWallet,
  getWalletByPrivateKey,
} from '../../../lib/aelf-client.js';

const first = createWallet();
const second = createWallet();

assert.ok(first.address, 'wallet address should be defined');
assert.equal(first.privateKey.length, 64, 'wallet private key should be 64 hex chars');
assert.notEqual(first.address, second.address, 'wallet addresses should be unique');
assert.notEqual(first.privateKey, second.privateKey, 'wallet private keys should be unique');
assert.ok(first.mnemonic, 'wallet mnemonic should be defined');

const restored = getWalletByPrivateKey(first.privateKey);
assert.equal(restored.address, first.address, 'restored address should match original');
assert.equal(restored.privateKey, first.privateKey, 'restored private key should match original');

const shortKeyWallet = getWalletByPrivateKey('abc123');
assert.ok(shortKeyWallet.address, 'short-key wallet should still resolve an address');

clearCaches();

console.log(
  JSON.stringify({
    walletAddress: first.address,
    walletPrivateKeyLength: first.privateKey.length,
    mnemonicWordCount: first.mnemonic?.split(' ').length ?? 0,
    uniqueAddresses: first.address !== second.address,
    uniquePrivateKeys: first.privateKey !== second.privateKey,
    restoredMatches:
      restored.address === first.address && restored.privateKey === first.privateKey,
    shortKeyAddressDefined: Boolean(shortKeyWallet.address),
    clearCachesOk: true,
  }),
);
