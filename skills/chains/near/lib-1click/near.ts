// Import NEAR-JS Libraries
// See docs for more information: https://docs.near.org/tools/near-api
import { KeyPairSigner } from '@near-js/signers';
import { KeyPairString } from '@near-js/crypto';
import { JsonRpcProvider, Provider } from '@near-js/providers';
import { Account } from '@near-js/accounts';

export async function getAccount(accountId: string, privateKey: string) {
  // Create signer from private key in .env file
  const signer = KeyPairSigner.fromSecretKey(privateKey as KeyPairString);

  // Create provider for RPC connection to NEAR Blockchain
  const provider = new JsonRpcProvider({
    url: 'https://rpc.mainnet.fastnear.com',
  });

  // Instantiate NEAR account to perform actions on the blockchain
  const account = new Account(accountId, provider as Provider, signer);
  return account;
}
