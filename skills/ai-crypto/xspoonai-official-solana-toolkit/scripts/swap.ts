/**
 * Token swaps via Jupiter
 * 
 * Usage:
 *   npx tsx scripts/swap.ts quote <input-mint> <output-mint> <amount>
 *   npx tsx scripts/swap.ts execute <wallet> <input-mint> <output-mint> <amount> [slippage-bps]
 */

import { Connection, VersionedTransaction } from '@solana/web3.js';
import { loadConfig, getRpcUrl } from './config.js';
import { loadWallet, getFullBalance } from './wallet.js';

const JUPITER_API = 'https://api.jup.ag/swap/v1';

// Common token mints
const KNOWN_TOKENS: Record<string, { mint: string; decimals: number }> = {
  'SOL': { mint: 'So11111111111111111111111111111111111111112', decimals: 9 },
  'USDC': { mint: 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v', decimals: 6 },
  'USDT': { mint: 'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB', decimals: 6 },
  'BONK': { mint: 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263', decimals: 5 },
  'JUP': { mint: 'JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN', decimals: 6 },
  'RAY': { mint: '4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R', decimals: 6 },
  'ORCA': { mint: 'orcaEKTdK7LKz57vaAYr9QeNsVEPfiu6QeMU1kektZE', decimals: 6 },
  'PYTH': { mint: 'HZ1JovNiVvGrGNiiYvEozEVgZ58xaU3RKwX8eACQBCt3', decimals: 6 },
};

function resolveToken(input: string): { mint: string; decimals: number } {
  const upper = input.toUpperCase();
  if (KNOWN_TOKENS[upper]) {
    return KNOWN_TOKENS[upper];
  }
  // Assume it's a mint address with default 9 decimals
  return { mint: input, decimals: 9 };
}

interface QuoteResponse {
  inputMint: string;
  outputMint: string;
  inAmount: string;
  outAmount: string;
  priceImpactPct: string;
  routePlan: Array<{
    swapInfo: {
      label: string;
    };
    percent: number;
  }>;
  contextSlot: number;
}

export async function getQuote(
  inputMint: string,
  outputMint: string,
  amount: number,
  inputDecimals: number,
  slippageBps: number = 100
): Promise<QuoteResponse> {
  const amountRaw = Math.floor(amount * Math.pow(10, inputDecimals)).toString();
  
  const params = new URLSearchParams({
    inputMint,
    outputMint,
    amount: amountRaw,
    slippageBps: slippageBps.toString()
  });
  
  const response = await fetch(`${JUPITER_API}/quote?${params}`);
  
  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Quote failed: ${error}`);
  }
  
  return response.json();
}

export async function executeSwap(
  walletName: string,
  inputToken: string,
  outputToken: string,
  amount: number,
  slippageBps: number = 100
): Promise<{ signature: string; inputAmount: string; outputAmount: string }> {
  const config = loadConfig();
  const connection = new Connection(getRpcUrl(config), 'confirmed');
  const wallet = loadWallet(walletName);
  
  const input = resolveToken(inputToken);
  const output = resolveToken(outputToken);
  
  // Get quote
  console.log(`Getting quote for ${amount} ${inputToken} → ${outputToken}...`);
  const quote = await getQuote(input.mint, output.mint, amount, input.decimals, slippageBps);
  
  // Check price impact
  const priceImpact = parseFloat(quote.priceImpactPct);
  if (priceImpact > 5) {
    throw new Error(`Price impact too high: ${priceImpact.toFixed(2)}%. Aborting.`);
  }
  
  if (priceImpact > 1) {
    console.warn(`⚠️  Warning: Price impact is ${priceImpact.toFixed(2)}%`);
  }
  
  // Build swap transaction
  console.log('Building swap transaction...');
  const swapResponse = await fetch(`${JUPITER_API}/swap`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      quoteResponse: quote,
      userPublicKey: wallet.publicKey.toString(),
      wrapAndUnwrapSol: true,
      dynamicComputeUnitLimit: true,
      prioritizationFeeLamports: 'auto'
    })
  });
  
  if (!swapResponse.ok) {
    const error = await swapResponse.text();
    throw new Error(`Swap build failed: ${error}`);
  }
  
  const { swapTransaction, lastValidBlockHeight } = await swapResponse.json();
  
  // Deserialize and sign
  const txBuffer = Buffer.from(swapTransaction, 'base64');
  const tx = VersionedTransaction.deserialize(txBuffer);
  tx.sign([wallet]);
  
  // Send with confirmation
  console.log('Sending transaction...');
  const signature = await connection.sendRawTransaction(tx.serialize(), {
    skipPreflight: true,
    maxRetries: 3
  });
  
  // Wait for confirmation
  console.log('Waiting for confirmation...');
  const confirmation = await connection.confirmTransaction({
    signature,
    blockhash: tx.message.recentBlockhash,
    lastValidBlockHeight
  }, 'confirmed');
  
  if (confirmation.value.err) {
    throw new Error(`Transaction failed: ${JSON.stringify(confirmation.value.err)}`);
  }
  
  const outputDecimals = output.decimals;
  const inputAmount = (parseInt(quote.inAmount) / Math.pow(10, input.decimals)).toFixed(6);
  const outputAmount = (parseInt(quote.outAmount) / Math.pow(10, outputDecimals)).toFixed(6);
  
  return {
    signature,
    inputAmount,
    outputAmount
  };
}

export async function getPrice(mints: string[]): Promise<Record<string, number>> {
  const ids = mints.join(',');
  const response = await fetch(`https://api.jup.ag/price/v2?ids=${ids}`);
  const data = await response.json();
  
  const prices: Record<string, number> = {};
  for (const [mint, info] of Object.entries(data.data || {})) {
    prices[mint] = parseFloat((info as any).price || '0');
  }
  return prices;
}

// CLI handler
async function main() {
  const [,, command, ...args] = process.argv;
  
  if (!command) {
    console.log(`
Jupiter Swap

Commands:
  quote <input> <output> <amount>
    Get swap quote. Use token symbols (SOL, USDC) or mint addresses.

  execute <wallet> <input> <output> <amount> [slippage-bps]
    Execute swap. Default slippage: 100 (1%)

  price <tokens...>
    Get current prices

Examples:
  npx tsx scripts/swap.ts quote SOL USDC 1
  npx tsx scripts/swap.ts execute main SOL USDC 0.5
  npx tsx scripts/swap.ts execute main SOL USDC 0.5 50  # 0.5% slippage
  npx tsx scripts/swap.ts price SOL USDC BONK
`);
    process.exit(1);
  }
  
  try {
    switch (command) {
      case 'quote': {
        const [inputToken, outputToken, amountStr] = args;
        if (!inputToken || !outputToken || !amountStr) {
          throw new Error('Usage: quote <input> <output> <amount>');
        }
        
        const amount = parseFloat(amountStr);
        const input = resolveToken(inputToken);
        const output = resolveToken(outputToken);
        
        const quote = await getQuote(input.mint, output.mint, amount, input.decimals);
        
        const inAmount = parseInt(quote.inAmount) / Math.pow(10, input.decimals);
        const outAmount = parseInt(quote.outAmount) / Math.pow(10, output.decimals);
        const rate = outAmount / inAmount;
        
        console.log(`\n📊 Swap Quote`);
        console.log(`   ${inAmount} ${inputToken} → ${outAmount.toFixed(6)} ${outputToken}`);
        console.log(`   Rate: 1 ${inputToken} = ${rate.toFixed(6)} ${outputToken}`);
        console.log(`   Price Impact: ${quote.priceImpactPct}%`);
        console.log(`   Route: ${quote.routePlan.map(r => r.swapInfo.label).join(' → ')}`);
        break;
      }
      
      case 'execute': {
        const [wallet, inputToken, outputToken, amountStr, slippageStr] = args;
        if (!wallet || !inputToken || !outputToken || !amountStr) {
          throw new Error('Usage: execute <wallet> <input> <output> <amount> [slippage-bps]');
        }
        
        const amount = parseFloat(amountStr);
        const slippageBps = slippageStr ? parseInt(slippageStr) : 100;
        
        const result = await executeSwap(wallet, inputToken, outputToken, amount, slippageBps);
        
        console.log(`\n✅ Swap executed!`);
        console.log(`   Swapped: ${result.inputAmount} ${inputToken} → ${result.outputAmount} ${outputToken}`);
        console.log(`   Signature: ${result.signature}`);
        console.log(`   Explorer: https://solscan.io/tx/${result.signature}`);
        break;
      }
      
      case 'price': {
        const tokens = args;
        if (tokens.length === 0) {
          throw new Error('Usage: price <token1> [token2] ...');
        }
        
        const mints = tokens.map(t => resolveToken(t).mint);
        const prices = await getPrice(mints);
        
        console.log('\n💰 Current Prices (USD):');
        for (let i = 0; i < tokens.length; i++) {
          const price = prices[mints[i]] || 0;
          console.log(`   ${tokens[i]}: $${price.toFixed(6)}`);
        }
        break;
      }
      
      default:
        throw new Error(`Unknown command: ${command}`);
    }
  } catch (error) {
    console.error(`\n❌ Error: ${(error as Error).message}`);
    process.exit(1);
  }
}

main().catch(console.error);
