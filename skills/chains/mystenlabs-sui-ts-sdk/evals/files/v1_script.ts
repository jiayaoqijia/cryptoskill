import { SuiClient, getFullnodeUrl } from '@mysten/sui/client';
import { TransactionBlock } from '@mysten/sui/transactions';
import { Ed25519Keypair } from '@mysten/sui/keypairs/ed25519';

const client = new SuiClient({ url: getFullnodeUrl('testnet') });
const keypair = Ed25519Keypair.deriveKeypair('test test test test test test test test test test test junk');

async function main() {
  // Query owned objects
  const objects = await client.getOwnedObjects({
    owner: keypair.toSuiAddress(),
    options: { showContent: true },
  });
  console.log(`Found ${objects.data.length} objects`);

  // Query coins
  const coins = await client.getCoins({
    owner: keypair.toSuiAddress(),
    coinType: '0x2::sui::SUI',
  });
  console.log(`Found ${coins.data.length} SUI coins`);

  // Build and execute a transaction
  const txb = new TransactionBlock();
  const [coin] = txb.splitCoins(txb.gas, [txb.pure(1_000_000_000)]);
  txb.transferObjects([coin], txb.pure(keypair.toSuiAddress()));

  const result = await client.signAndExecuteTransactionBlock({
    transactionBlock: txb,
    signer: keypair,
    options: {
      showEffects: true,
      showEvents: true,
    },
  });

  // Check result
  const status = result.effects?.status?.status;
  if (status !== 'success') {
    throw new Error(`Transaction failed: ${status}`);
  }

  console.log(`Transaction succeeded: ${result.digest}`);

  // Wait for indexing
  await client.waitForTransactionBlock({
    digest: result.digest,
  });

  // Query dynamic fields
  const fields = await client.getDynamicFields({
    parentId: '0xOBJECT',
  });
  console.log(`Found ${fields.data.length} dynamic fields`);
}

main().catch(console.error);