import { resolveManagerWallet } from '../core/keystore.js';

export function requireWallet(input: {
  network?: string;
  loginEmail?: string;
  password?: string;
  keystoreFile?: string;
} = {}) {
  return resolveManagerWallet({
    network: input.network || 'mainnet',
    loginEmail: input.loginEmail,
    password: input.password,
    keystoreFile: input.keystoreFile,
  }).wallet;
}
