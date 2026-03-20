
import axios from 'axios';
import { Environment } from './near-intents-lib/environment';
import {
  intentSwap,
  depositToIntents,
  withdrawFromIntents,
  getIntentsDepositAddress,
  getIntentsBalance,
  _walletBalance
} from './near-intents-lib';
import { checkMinimumUSDValue } from './price-service';

// Define types for our asset mapping
interface Asset {
  symbol: string;
  name: string;
  decimals: number;
  blockchain: string;
  intents_token_id: string; // The Defuse Asset ID
  contract_address?: string;
}

interface IntentParams {
  assetIn: string;
  assetOut: string;
  amount: string;
  recipient?: string;
  chainOut?: string; // Optional: Explicit chain destination
}

export class IntentsOptimizer {
  private env: Environment;
  private tokens: Asset[] = [];

  constructor(env: Environment) {
    this.env = env;
  }

  /**
   * Initialize the optimizer by fetching supported tokens
   */
  async init() {
    try {
      const response = await axios.get("https://api-mng-console.chaindefuser.com/api/tokens");
      const rawTokens = response.data?.items || [];
      this.tokens = rawTokens.map((t: any) => ({
        ...t,
        intents_token_id: t.defuse_asset_id || t.intents_token_id,
        // Ensure name is present
        name: t.name || t.symbol
      }));
      
      console.log(`[IntentsOptimizer] Loaded ${this.tokens.length} supported tokens.`);
    } catch (error) {
      console.error("[IntentsOptimizer] Failed to fetch tokens:", error);
      // Fallback or retry logic could go here
    }
  }

  /**
   * Find a token by symbol or loose name matching
   */
  private findToken(query: string): Asset | undefined {
    let q = query.toLowerCase();
    
    let targetBlockchain = '';
    if (q.includes(':')) {
        const parts = q.split(':');
        if (['near', 'base', 'eth', 'arb', 'sol', 'gnosis', 'bsc', 'starknet'].includes(parts[0])) {
            targetBlockchain = parts[0];
            q = parts[1]; // search for symbol part
        }
    }
    
    // 0. Manual Aliases
    if (q === 'near') return this.tokens.find(t => t.intents_token_id === 'nep141:wrap.near');
    // Adjust usdc alias to prefer NEAR version unless blockchain specified
    if (q === 'usdc' && !targetBlockchain) return this.tokens.find(t => t.intents_token_id === 'nep141:17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1');

    // 1. Try exact match on symbol
    const duplicates = this.tokens.filter(t => t.symbol.toLowerCase() === q);
    if (duplicates.length > 0) {
        // If blockchain specified, look for it
        if (targetBlockchain) {
          const match = duplicates.find(t => t.blockchain === targetBlockchain);
          if (match) return match;
        }
        
        // Prioritize NEAR chain, then others
        const onNear = duplicates.find(t => t.blockchain === 'near');
        if (onNear) return onNear;
        return duplicates[0];
    }

    // 2. Try match with blockchain prefix (exact ID matches)
    // If we already peeled off blockchain, search using original query or just name
    const fuzzy = this.tokens.find(t => 
      t.intents_token_id.toLowerCase().includes(query.toLowerCase()) || 
      t.name.toLowerCase().includes(q)
    );
    return fuzzy;
  }

  /**
   * Main entry point to execute an intent
   */
  async executeIntent(params: IntentParams): Promise<string> {
    if (this.tokens.length === 0) await this.init();

    const { assetIn, assetOut, amount, recipient, chainOut } = params;

    // 1. Asset Mapping
    const tokenIn = this.findToken(assetIn);
    const tokenOut = this.findToken(assetOut);

    if (!tokenIn) return `Error: Could not find supported asset for '${assetIn}'`;
    if (!tokenOut) return `Error: Could not find supported asset for '${assetOut}'`;

    console.log(`[IntentsOptimizer] Planning transaction: ${amount} ${tokenIn.symbol} -> ${tokenOut.symbol}`);

    // 2. Minimum USD Value Check
    console.log(`[IntentsOptimizer] Checking minimum USD value ($0.2)...`);
    console.log(`[IntentsOptimizer] Token: ${tokenIn.symbol}, Amount: ${amount}`);
    const priceCheck = await checkMinimumUSDValue(tokenIn.symbol, amount, 0.2);
    console.log(`[IntentsOptimizer] USD value: $${priceCheck.usdValue.toFixed(2)}`);

    if (!priceCheck.valid) {
      return `Error: Amount too small. ${amount} ${tokenIn.symbol} = $${priceCheck.usdValue.toFixed(2)}, but minimum is $${priceCheck.minimumUSD.toFixed(2)}. Please increase the amount.`;
    }

    // 3. Smart Routing
    // Check if it's a simple NEAR transfer (NEAR -> NEAR on NEAR chain)
    if (tokenIn.symbol === 'NEAR' && tokenOut.symbol === 'NEAR' && (!chainOut || chainOut === 'near')) {
      if (recipient) {
         // Fallback to standard CLI
         // NOTE: In a real agent execution, I would return a specific structure instructing the agent to use 'near-tools'.
         // For now, I will return a string suggestion.
         return `SUGGESTION: Use standard near-cli for simple NEAR transfers. Command: 'near tokens send-near ${this.env.wallet.ACCOUNT_ID} ${recipient} ${amount} NOW'`;
      }
    }

    // 3. Execution (Swap/Bridge via Intents)
    
    // Check if we need to deposit first (from NEAR wallet to Intents Contract)
    // We can check balances on the Intents contract
    const intentsBalances = await getIntentsBalance(this.env, this.env.wallet.ACCOUNT_ID || "", this.tokens);
    // Logic to check if we have enough balance in intents.near
    // This is complex because 'intentsBalances' returns an array of {symbol, balance, ...}
    // We need to check if we have enough 'tokenIn' in intents.near
    
    // For now, let's try to just run the swap/withdraw flow which usually includes checks?
    // Looking at 'swap.ts' -> 'intentSwap', it calls '_intentSwap' which checks balances.
    // But 'deposit.ts' is for depositing.
    
    // Let's rely on 'intentSwap' to fail if balance is low? No, we should be smarter.
    // 'depositToIntents' handles checking wrap.near balance and depositing?
    // Let's checking 'swap.ts' behavior again...
    // It calls `mt_batch_balance_of`.

    this.env.add_reply(`Initiating Intent: ${amount} ${tokenIn.symbol} -> ${tokenOut.symbol}`);

    // LOGIC:
    // If AssetIn == AssetOut, it's a bridge/withdraw (or deposit?)
    // If AssetIn != AssetOut, it's a swap (potentially cross-chain if AssetOut is on another chain)

    if (tokenIn.intents_token_id === tokenOut.intents_token_id) {
        // Same asset execution
        // If the user wants to "Bridge", they usually mean "Withdraw to another chain"
        // But if tokenIn and tokenOut are the EXACT same ID, it implies they are on the same chain in the Defuse world.
        // Wait, Defuse has different IDs for different chains?
        // e.g. 'nep141:usdc.near' vs 'sol:...'
        
        // If they are different IDs but same symbol -> Swap
        // If they are same ID ? -> Transfer/Withdraw?
        
        // Let's assume user wants to Withdraw/Bridge if they specified 'recipient' or 'chainOut'.
        if (recipient) {
             const success = await withdrawFromIntents(
                this.env, 
                tokenIn.symbol, 
                amount, 
                recipient, 
                this.tokens, 
                tokenIn // Using tokenIn data for withdrawal
            );
            return success ? "Withdrawal/Bridge initiated successfully." : "Failed to initiate withdrawal.";
        } else {
             return "Error: Recipient required for bridging/withdrawal of same asset.";
        }
    } else {
        // Swap Logic
        // We might need to deposit first if balance on intents contract is 0.
        // Let's try to deposit automatically if needed?
        // For now, let's call intentSwap.
        
        // Note: intentSwap in the library takes `contractIn` and `contractOut` (which correspond to intents_token_id).
        // Check if we have enough balance on intents.near
        // Note: intentSwap checks balance too, but doesn't auto-deposit.
        // We need to ensure we have enough.
        
        // We can try to deposit the full amount if we assume the user intends to use their wallet balance.
        // A more sophisticated approach would be: check intents balance -> if < amout -> deposit difference.
        
        // For this first version, let's just attempt to deposit the amount if it's NEAR or a supported token.
        // But doing it blindly might be wasteful if they already have balance.
        
        // Let's use getIntentsBalance
        const balances = await getIntentsBalance(this.env, this.env.wallet.ACCOUNT_ID || "", this.tokens);
        const tokenBalanceObj = balances.find((b: any) => b.symbol === tokenIn.symbol);
        const currentBalance = tokenBalanceObj ? (tokenBalanceObj as any).balance : "0";
        
        console.log(`[IntentsOptimizer] Current Balance on Intents: ${currentBalance} ${tokenIn.symbol}`);
        
        // Simple comparison (using string/float parsing for now, ideally Decimal)
        if (parseFloat(currentBalance) < parseFloat(amount)) {
            console.log(`[IntentsOptimizer] Insufficient balance on Intents. Attempting deposit of ${amount} ${tokenIn.symbol}...`);
            const depositSuccess = await depositToIntents(
                this.env,
                this.tokens,
                amount, // Valid assumption: deposit takes user-facing amount
                this.env.wallet.ACCOUNT_ID || "",
                tokenIn.symbol
            );
            
            if (!depositSuccess) {
                return `Error: Failed to deposit ${amount} ${tokenIn.symbol} to Intents contract. Check wallet balance.`;
            }
            console.log(`[IntentsOptimizer] Deposit successful.`);
        }

        let result;
        try {
            result = await intentSwap(
                this.env,
                tokenIn.symbol,
                tokenOut.symbol,
                amount,
                this.tokens,
                tokenIn.intents_token_id,
                tokenOut.intents_token_id
            );
        } catch (error: any) {
            console.error("[IntentsOptimizer] Swap execution failed:", error);
            
            // Analyze error for better agent feedback
            const errString = error.toString();
            if (errString.includes("Empty result") || errString.includes("result is not provided")) {
                return `Error: Swap failed because no solver provided a quote (Liquidity/Timeout). 
SUGGESTION: Try a larger amount or a different token pair. If this persists, the Defuse solver might be down.`;
            }
            if (errString.includes("NotEnoughBalance")) {
                return `Error: Insufficient balance on Intents Contract. 
SUGGESTION: Check your wallet balance and ensure you have enough ${tokenIn.symbol} including gas fees. You can use 'near-tools' to check balances.`;
            }
            
            return `Error: Swap failed with message: ${errString}`;
        }

        if (result) {
            // Check for bridge/withdrawal (Recipient provided for cross-chain)
            const { amountOut } = result as any;
            if (recipient && tokenOut.blockchain !== 'near') {
                 console.log(`[IntentsOptimizer] Swapped to ${tokenOut.symbol}, now withdrawing to ${recipient} on ${tokenOut.blockchain}...`);
                 const withdrawSuccess = await withdrawFromIntents(
                    this.env,
                    tokenOut.symbol,
                    amountOut, // Use the amount we received from swap
                    recipient,
                    this.tokens,
                    tokenOut
                 );
                 if (withdrawSuccess) {
                    return `🌉 Bridge/Withdraw Successful!\n✅ Sent ${amountOut} ${tokenOut.symbol} to ${recipient}\n📦 Destination: ${tokenOut.blockchain}\n\n💡 You can track the withdrawal on the ${tokenOut.blockchain} block explorer.`;
                 } else {
                    return `✅ Swap successful, but Withdraw failed.\n📦 You hold ${amountOut} ${tokenOut.symbol} on the Intents Contract.\n💡 Please try the withdrawal again.`;
                 }
            }

             const { txHash } = result as any;
             const nearblocksUrl = `https://nearblocks.io/txns/${txHash}`;
             return `✅ Swap Successful!\n💰 Received: ${amountOut} ${tokenOut.symbol}\n🔗 NEAR Blocks: ${nearblocksUrl}\n\n✨ Transaction completed!`;
        } else {
            return `Error: Swap failed. No result returned from solver. 
SUGGESTION: The network might be congested or no solver is available for ${tokenIn.symbol}->${tokenOut.symbol}. Try again later or use 'near-tools' for standard swaps if applicable.`;
        }
    }
  }
}
