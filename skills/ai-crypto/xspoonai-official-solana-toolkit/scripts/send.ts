/**
 * Send SOL or SPL tokens
 * 
 * Usage:
 *   npx tsx scripts/send.ts sol <from-wallet> <to-address> <amount>
 *   npx tsx scripts/send.ts token <from-wallet> <to-address> <mint> <amount>
 */

import {
  Connection,
  PublicKey,
  Transaction,
  SystemProgram,
  sendAndConfirmTransaction,
  LAMPORTS_PER_SOL,
  ComputeBudgetProgram
} from '@solana/web3.js';
import {
  getAssociatedTokenAddress,
  createAssociatedTokenAccountInstruction,
  createTransferInstruction,
  TOKEN_PROGRAM_ID,
  getAccount
} from '@solana/spl-token';
import { loadConfig, getRpcUrl } from './config.js';
import { loadWallet, getBalance } from './wallet.js';

function isValidAddress(address: string): boolean {
  try {
    new PublicKey(address);
    return true;
  } catch {
    return false;
  }
}

async function getPriorityFee(connection: Connection, accounts: string[]): Promise<number> {
  try {
    const config = loadConfig();
    const response = await fetch(getRpcUrl(config), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 'fee-1',
        method: 'getPriorityFeeEstimate',
        params: [{
          accountKeys: accounts,
          options: { priorityLevel: 'Medium' }
        }]
      })
    });
    
    const data = await response.json();
    return data.result?.priorityFeeEstimate || 50000; // Default 50k microlamports
  } catch {
    return 50000;
  }
}

export async function sendSol(
  fromWalletName: string,
  toAddress: string,
  amount: number
): Promise<string> {
  if (!isValidAddress(toAddress)) {
    throw new Error(`Invalid recipient address: ${toAddress}`);
  }
  
  if (amount <= 0) {
    throw new Error('Amount must be positive');
  }
  
  const config = loadConfig();
  const connection = new Connection(getRpcUrl(config), 'confirmed');
  const fromWallet = loadWallet(fromWalletName);
  const toPubkey = new PublicKey(toAddress);
  
  // Check balance
  const balance = await getBalance(fromWallet.publicKey);
  const lamportsToSend = amount * LAMPORTS_PER_SOL;
  const estimatedFee = 0.000005 * LAMPORTS_PER_SOL; // ~5000 lamports
  
  if (balance.lamports < lamportsToSend + estimatedFee) {
    throw new Error(
      `Insufficient balance. Have: ${balance.sol} SOL, ` +
      `Need: ${amount} SOL + ~0.000005 SOL fee`
    );
  }
  
  // Get priority fee
  const priorityFee = await getPriorityFee(connection, [
    fromWallet.publicKey.toBase58(),
    toAddress
  ]);
  
  // Build transaction
  const tx = new Transaction().add(
    ComputeBudgetProgram.setComputeUnitPrice({ microLamports: priorityFee }),
    ComputeBudgetProgram.setComputeUnitLimit({ units: 200_000 }),
    SystemProgram.transfer({
      fromPubkey: fromWallet.publicKey,
      toPubkey,
      lamports: lamportsToSend
    })
  );
  
  // Send and confirm
  const signature = await sendAndConfirmTransaction(connection, tx, [fromWallet], {
    commitment: 'confirmed'
  });
  
  return signature;
}

export async function sendToken(
  fromWalletName: string,
  toAddress: string,
  mintAddress: string,
  amount: number
): Promise<string> {
  if (!isValidAddress(toAddress)) {
    throw new Error(`Invalid recipient address: ${toAddress}`);
  }
  if (!isValidAddress(mintAddress)) {
    throw new Error(`Invalid mint address: ${mintAddress}`);
  }
  
  const config = loadConfig();
  const connection = new Connection(getRpcUrl(config), 'confirmed');
  const fromWallet = loadWallet(fromWalletName);
  const toPubkey = new PublicKey(toAddress);
  const mint = new PublicKey(mintAddress);
  
  // Get token accounts
  const fromAta = await getAssociatedTokenAddress(mint, fromWallet.publicKey);
  const toAta = await getAssociatedTokenAddress(mint, toPubkey);
  
  // Check source balance
  let sourceAccount;
  try {
    sourceAccount = await getAccount(connection, fromAta);
  } catch {
    throw new Error(`No token account found for ${mintAddress} in source wallet`);
  }
  
  // Get decimals from mint
  const mintInfo = await connection.getParsedAccountInfo(mint);
  const decimals = (mintInfo.value?.data as any)?.parsed?.info?.decimals || 9;
  const amountRaw = BigInt(Math.floor(amount * Math.pow(10, decimals)));
  
  if (sourceAccount.amount < amountRaw) {
    throw new Error(
      `Insufficient token balance. Have: ${Number(sourceAccount.amount) / Math.pow(10, decimals)}, ` +
      `Need: ${amount}`
    );
  }
  
  // Build transaction
  const tx = new Transaction();
  
  // Check if destination ATA exists
  const destAccountInfo = await connection.getAccountInfo(toAta);
  if (!destAccountInfo) {
    tx.add(
      createAssociatedTokenAccountInstruction(
        fromWallet.publicKey, // payer
        toAta,
        toPubkey,
        mint
      )
    );
  }
  
  tx.add(
    createTransferInstruction(
      fromAta,
      toAta,
      fromWallet.publicKey,
      amountRaw
    )
  );
  
  // Add priority fee
  const priorityFee = await getPriorityFee(connection, [
    fromWallet.publicKey.toBase58(),
    mint.toBase58()
  ]);
  
  tx.instructions.unshift(
    ComputeBudgetProgram.setComputeUnitPrice({ microLamports: priorityFee }),
    ComputeBudgetProgram.setComputeUnitLimit({ units: 300_000 })
  );
  
  // Send and confirm
  const signature = await sendAndConfirmTransaction(connection, tx, [fromWallet], {
    commitment: 'confirmed'
  });
  
  return signature;
}

// CLI handler
async function main() {
  const [,, type, fromWallet, toAddress, ...rest] = process.argv;
  
  if (!type || !fromWallet || !toAddress) {
    console.log(`
Send SOL or Tokens

Usage:
  npx tsx scripts/send.ts sol <from-wallet> <to-address> <amount>
  npx tsx scripts/send.ts token <from-wallet> <to-address> <mint> <amount>

Examples:
  npx tsx scripts/send.ts sol main 8xK...abc 0.1
  npx tsx scripts/send.ts token main 8xK...abc EPjF...1v 100
`);
    process.exit(1);
  }
  
  try {
    let signature: string;
    
    if (type === 'sol') {
      const amount = parseFloat(rest[0]);
      if (isNaN(amount)) {
        throw new Error('Invalid amount');
      }
      
      console.log(`Sending ${amount} SOL to ${toAddress}...`);
      signature = await sendSol(fromWallet, toAddress, amount);
    } else if (type === 'token') {
      const mint = rest[0];
      const amount = parseFloat(rest[1]);
      
      if (!mint || isNaN(amount)) {
        throw new Error('Invalid mint or amount');
      }
      
      console.log(`Sending ${amount} tokens (${mint}) to ${toAddress}...`);
      signature = await sendToken(fromWallet, toAddress, mint, amount);
    } else {
      throw new Error(`Unknown type: ${type}. Use 'sol' or 'token'`);
    }
    
    console.log(`\n✅ Transaction confirmed!`);
    console.log(`   Signature: ${signature}`);
    console.log(`   Explorer: https://solscan.io/tx/${signature}`);
  } catch (error) {
    console.error(`\n❌ Error: ${(error as Error).message}`);
    process.exit(1);
  }
}

main().catch(console.error);
