declare module "aelf-sdk" {
  const AElf: any;
  export default AElf;
}

declare module "aelf-sdk/src/util/keyStore.js" {
  export function getKeystore(
    account: { privateKey: string; mnemonic?: string; address?: string; nickName?: string },
    password: string,
    option?: Record<string, unknown>,
  ): unknown;
  export function unlockKeystore(keystore: unknown, password: string): {
    privateKey: string;
    mnemonic?: string;
    address?: string;
    nickName?: string;
  };
  export function checkPassword(keystore: unknown, password: string): boolean;
}
