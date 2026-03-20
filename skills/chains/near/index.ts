/**
 * NEAR Intents Skill - 1-Click SDK Integration
 * 
 * This is a wrapper around the official NEAR Intents 1-Click SDK
 * that maintains compatibility with the existing executeIntent() API
 * while using the more reliable 1-Click implementation.
 */

import {
  OpenAPI,
  OneClickService,
  QuoteRequest,
} from '@defuse-protocol/one-click-sdk-typescript';
import { Account } from '@near-js/accounts';
import { KeyPairSigner } from '@near-js/signers';
import { JsonRpcProvider, Provider } from '@near-js/providers';
import { KeyPairString } from '@near-js/crypto';
import { NEAR } from '@near-js/tokens';
import Decimal from 'decimal.js';
import dotenv from 'dotenv';

dotenv.config();

// Initialize 1-Click API
OpenAPI.BASE = 'https://1click.chaindefuser.com';
OpenAPI.TOKEN = process.env.ONE_CLICK_JWT; // Optional, but recommended to avoid 0.1% fee

interface ExecuteIntentParams {
  assetIn: string;
  assetOut: string;
  amount: string;
  recipient?: string;
  refundAddress?: string;  // Refund address on origin chain (required for non-NEAR origins)
  mode?: 'auto' | 'manual';  // auto = send automatically, manual = just get quote
  swapType?: 'EXACT_INPUT' | 'EXACT_OUTPUT';  // default: EXACT_INPUT
}

interface TokenInfo {
  symbol: string;
  decimals: number;
  assetId: string;
}

// Token mapping (simplified - full list in TOKENS.md)
const TOKEN_MAP: Record<string, TokenInfo> = {
  'NEAR': { symbol: 'NEAR', decimals: 24, assetId: 'nep141:wrap.near' },
  'wNEAR': { symbol: 'wNEAR', decimals: 24, assetId: 'nep141:wrap.near' },
  'USDC': { symbol: 'USDC', decimals: 6, assetId: 'nep141:17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1' },
  'USDT': { symbol: 'USDT', decimals: 6, assetId: 'nep141:usdt.tether-token.near' },
  'ETH': { symbol: 'ETH', decimals: 18, assetId: 'nep141:eth.bridge.near' },  // Rainbow Bridge ETH on NEAR
  
  // Base tokens
  'base:USDC': { symbol: 'USDC', decimals: 6, assetId: 'nep141:base-0x833589fcd6edb6e08f4c7c32d4f71b54bda02913.omft.near' },
  'base:ETH': { symbol: 'ETH', decimals: 18, assetId: 'nep141:base.omft.near' },
  
  // Arbitrum tokens
  'arb:ARB': { symbol: 'ARB', decimals: 18, assetId: 'nep141:arb-0x912ce59144191c1204e64559fe8253a0e49e6548.omft.near' },
  'arb:USDC': { symbol: 'USDC', decimals: 6, assetId: 'nep141:arb-0xaf88d065e77c8cc2239327c5edb3a432268e5831.omft.near' },
  'arb:ETH': { symbol: 'ETH', decimals: 18, assetId: 'nep141:arb.omft.near' },
  
  // Ethereum tokens
  'eth:ETH': { symbol: 'ETH', decimals: 18, assetId: 'nep141:eth.omft.near' },
  'eth:USDC': { symbol: 'USDC', decimals: 6, assetId: 'nep141:eth-0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48.omft.near' },
  
  // Solana tokens
  'sol:SOL': { symbol: 'SOL', decimals: 9, assetId: 'nep141:sol.omft.near' },
  'sol:USDC': { symbol: 'USDC', decimals: 6, assetId: 'nep141:sol-5ce3bf3a31af18be40ba30f721101b4341690186.omft.near' },
};

/**
 * Resolve token info from symbol
 */
function resolveToken(symbol: string): TokenInfo {
  const upperSymbol = symbol.toUpperCase();
  
  // Check direct mapping
  if (TOKEN_MAP[upperSymbol]) {
    return TOKEN_MAP[upperSymbol];
  }
  
  // Check with chain prefix
  for (const [key, value] of Object.entries(TOKEN_MAP)) {
    if (key.toUpperCase() === upperSymbol) {
      return value;
    }
  }
  
  throw new Error(`Token not found: ${symbol}. Check TOKENS.md for supported tokens.`);
}

/**
 * Convert human-readable amount to smallest unit
 */
function toSmallestUnit(amount: string, decimals: number): string {
  const dec = new Decimal(amount);
  const multiplier = new Decimal(10).pow(decimals);
  return dec.mul(multiplier).toFixed(0);
}

/**
 * Convert smallest unit to human-readable amount
 */
function fromSmallestUnit(amount: string, decimals: number): string {
  const dec = new Decimal(amount);
  const divisor = new Decimal(10).pow(decimals);
  return dec.div(divisor).toFixed();
}

/**
 * Initialize NEAR account
 */
async function initNearAccount(): Promise<Account> {
  const accountId = process.env.NEAR_ACCOUNT_ID;
  const privateKey = process.env.NEAR_PRIVATE_KEY;
  
  if (!accountId || !privateKey) {
    throw new Error('NEAR_ACCOUNT_ID and NEAR_PRIVATE_KEY must be set in .env');
  }
  
  // Create signer from private key
  const signer = KeyPairSigner.fromSecretKey(privateKey as KeyPairString);
  
  // Create provider for RPC connection
  const provider = new JsonRpcProvider({
    url: process.env.NEAR_RPC_URL || 'https://rpc.mainnet.fastnear.com',
  });
  
  // Instantiate NEAR account
  const account = new Account(accountId, provider as Provider, signer);
  
  return account;
}

/**
 * Send NEAR tokens to deposit address
 */
async function sendDeposit(
  account: Account,
  depositAddress: string,
  amount: string
): Promise<string> {
  console.log(`Sending ${amount} yoctoNEAR to ${depositAddress}...`);
  
  const result = await account.transfer({
    token: NEAR,
    amount,
    receiverId: depositAddress,
  });
  
  return result.transaction.hash;
}

/**
 * Poll swap status until completion
 */
async function pollStatus(depositAddress: string, maxAttempts = 30): Promise<any> {
  console.log('🔄 Starting status polling...');
  
  for (let i = 0; i < maxAttempts; i++) {
    try {
      const statusResponse = await OneClickService.getExecutionStatus(depositAddress);
      const status = statusResponse.status;
      
      console.log(`[${i + 1}/${maxAttempts}] Status: ${status}`);
      
      if (status === 'SUCCESS') {
        console.log('🎉 Intent Fulfilled!');
        return statusResponse;
      }
      
      if (status === 'REFUNDED' || status === 'FAILED') {
        throw new Error(`Swap failed with status: ${status}`);
      }
      
      // Wait 5 seconds before next poll
      await new Promise(resolve => setTimeout(resolve, 5000));
    } catch (error: any) {
      if (error?.message?.includes('failed')) {
        throw error;
      }
      // Continue polling on other errors
      console.log('⏳ Waiting 5 seconds before retry...');
      await new Promise(resolve => setTimeout(resolve, 5000));
    }
  }
  
  throw new Error('Status polling timed out');
}

/**
 * Main executeIntent function - compatible with existing API
 */
export async function executeIntent(params: ExecuteIntentParams): Promise<string> {
  const { assetIn, assetOut, amount, recipient, refundAddress, mode = 'auto', swapType = 'EXACT_INPUT' } = params;
  
  try {
    const isManual = mode === 'manual';
    const isExactOutput = swapType === 'EXACT_OUTPUT';
    
    console.log(`\n[1-Click SDK] ${isManual ? 'Manual Mode' : 'Auto Mode'}: ${amount} ${assetIn} → ${assetOut}`);
    
    // Resolve tokens
    const tokenIn = resolveToken(assetIn);
    const tokenOut = resolveToken(assetOut);
    
    console.log(`Token In: ${tokenIn.symbol} (${tokenIn.assetId})`);
    console.log(`Token Out: ${tokenOut.symbol} (${tokenOut.assetId})`);
    
    // Convert amount to smallest unit (for the appropriate token based on swap type)
    const amountToken = isExactOutput ? tokenOut : tokenIn;
    const amountInSmallest = toSmallestUnit(amount, amountToken.decimals);
    console.log(`Amount in smallest unit: ${amountInSmallest}`);
    
    // Get NEAR account
    const senderAddress = process.env.NEAR_ACCOUNT_ID!;
    
    // Determine if origin is NEAR or another chain
    const isNearOrigin = !assetIn.includes(':');
    
    // Determine refund address based on origin chain
    let refundToAddress: string;
    if (refundAddress) {
      refundToAddress = refundAddress;
    } else if (isNearOrigin) {
      refundToAddress = senderAddress;  // NEAR origin, use NEAR account
    } else {
      // Extract chain name for better error message
      const originChain = assetIn.split(':')[0].toUpperCase();
      throw new Error(
        `⚠️ CRITICAL: Cross-chain swap from ${assetIn} requires a refund address!\n\n` +
        `If the swap fails, your tokens will be refunded to this address on ${originChain}.\n` +
        `Please provide your ${originChain} wallet address using the 'refundAddress' parameter.\n\n` +
        `Example:\n` +
        `  refundAddress: '0x...'  // Your ${originChain} address\n\n` +
        `This is required for your fund safety - never skip this!`
      );
    }
    
    // Determine recipient address
    let recipientAddress = recipient || senderAddress;
    
    // If same chain (both NEAR), this is a withdrawal
    const isSameChain = !assetIn.includes(':') && !assetOut.includes(':');
    const isWithdrawal = isSameChain && recipient;
    
    if (isWithdrawal) {
      console.log(`Withdrawal mode: ${assetIn} → ${recipient}`);
      recipientAddress = recipient;
    }
    
    // Step 1: Get quote
    console.log('\n[Step 1] Getting quote...');
    const quoteRequest: QuoteRequest = {
      dry: false,
      swapType: isExactOutput ? QuoteRequest.swapType.EXACT_OUTPUT : QuoteRequest.swapType.EXACT_INPUT,
      slippageTolerance: 300, // 3%
      originAsset: tokenIn.assetId,
      depositType: QuoteRequest.depositType.ORIGIN_CHAIN,
      destinationAsset: tokenOut.assetId,
      amount: amountInSmallest,
      refundTo: refundToAddress,
      refundType: QuoteRequest.refundType.ORIGIN_CHAIN,
      recipient: recipientAddress,
      recipientType: QuoteRequest.recipientType.DESTINATION_CHAIN,
      deadline: new Date(Date.now() + 10 * 60 * 1000).toISOString(), // 10 minutes
      referral: 'openclaw',
      quoteWaitingTimeMs: 5000,
    };
    
    const quoteResponse = await OneClickService.getQuote(quoteRequest);
    
    if (!quoteResponse.quote?.depositAddress) {
      throw new Error('No deposit address in quote response');
    }
    
    const depositAddress = quoteResponse.quote.depositAddress;
    const amountIn = quoteResponse.quote.amountIn || '0';
    const amountOut = quoteResponse.quote.amountOut || '0';
    const amountInFormatted = fromSmallestUnit(amountIn, tokenIn.decimals);
    const amountOutFormatted = fromSmallestUnit(amountOut, tokenOut.decimals);
    
    console.log(`✅ Quote received`);
    console.log(`   Input: ${amountInFormatted} ${tokenIn.symbol}`);
    console.log(`   Output: ${amountOutFormatted} ${tokenOut.symbol}`);
    console.log(`   Deposit address: ${depositAddress}`);
    console.log(`   Deadline: ${quoteResponse.quote.deadline}`);
    
    // MANUAL MODE: Just return the quote
    if (isManual) {
      const manualInstructions = `
🎯 Manual Mode: Quote Generated

You need to send: ${amountInFormatted} ${tokenIn.symbol}
You will receive: ${amountOutFormatted} ${tokenOut.symbol}

📋 Instructions:
1. Send ${amountInFormatted} ${tokenIn.symbol} to:
   ${depositAddress}
   
2. Track your swap:
   https://explorer.near-intents.org/transactions/${depositAddress}
   
3. Your ${tokenOut.symbol} will arrive at:
   ${recipientAddress}
   
⏰ Deadline: ${quoteResponse.quote.deadline}
`;
      
      console.log(manualInstructions);
      return manualInstructions;
    }
    
    // AUTO MODE: Continue with automatic sending
    const account = await initNearAccount();
    
    // Step 2: Send deposit
    console.log('\n[Step 2] Sending deposit...');
    const txHash = await sendDeposit(account, depositAddress, amountIn);
    console.log(`✅ Deposit sent: https://nearblocks.io/txns/${txHash}`);
    
    // Step 3: Submit transaction hash (optional but helps 1-Click track faster)
    console.log('\n[Step 3] Submitting transaction hash...');
    try {
      await OneClickService.submitDepositTx({
        txHash,
        depositAddress,
      });
      console.log(`✅ Transaction hash submitted`);
    } catch (error) {
      console.log(`⚠️  Transaction hash submission failed (non-critical)`);
    }
    
    // Step 4: Poll status
    console.log('\n[Step 4] Monitoring swap status...');
    console.log('Waiting 5 seconds before polling...');
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    const finalStatus = await pollStatus(depositAddress);
    
    console.log('\n✅ Swap completed successfully!');
    console.log(`Explorer: https://explorer.near-intents.org/transactions/${depositAddress}`);
    
    return `Swap Successful! ${amountInFormatted} ${tokenIn.symbol} → ${amountOutFormatted} ${tokenOut.symbol}
Transaction: https://nearblocks.io/txns/${txHash}
Explorer: https://explorer.near-intents.org/transactions/${depositAddress}`;
    
  } catch (error: any) {
    console.error('❌ Swap failed:', error.message || error);
    throw new Error(`Swap failed: ${error.message || error}`);
  }
}

// Export for testing
export { resolveToken, toSmallestUnit, fromSmallestUnit };
