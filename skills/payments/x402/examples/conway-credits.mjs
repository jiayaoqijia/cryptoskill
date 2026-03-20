#!/usr/bin/env node
/**
 * Conway Credits Top-up via x402
 * 
 * Usage:
 *   PRIVATE_KEY=0x... node conway-credits.mjs 5
 *   
 * Or with a wallet file:
 *   WALLET_PATH=/path/to/wallet.json node conway-credits.mjs 5
 */

import { privateKeyToAccount } from "viem/accounts";
import { x402Fetch } from "../x402.mjs";
import { readFileSync } from "fs";

// Load wallet from env or file
function loadWallet() {
  if (process.env.PRIVATE_KEY) {
    return privateKeyToAccount(process.env.PRIVATE_KEY);
  }
  
  if (process.env.WALLET_PATH) {
    const wallet = JSON.parse(readFileSync(process.env.WALLET_PATH, "utf-8"));
    return privateKeyToAccount(wallet.privateKey);
  }
  
  console.error("Error: Set PRIVATE_KEY or WALLET_PATH environment variable");
  process.exit(1);
}

const account = loadWallet();
const amountUsd = process.argv[2] || "5";

async function topUp() {
  console.log(`Wallet: ${account.address}`);
  console.log(`Topping up $${amountUsd} Conway credits...\n`);
  
  const url = `https://api.conway.tech/pay/${amountUsd}/${account.address}`;
  
  const response = await x402Fetch(account, url);
  const result = await response.json();
  
  console.log("Response:", JSON.stringify(result, null, 2));
  
  if (result.success) {
    console.log(`\n✅ Topped up ${result.credits_cents} cents`);
    if (result.tx_hash) {
      console.log(`TX: https://basescan.org/tx/${result.tx_hash}`);
    }
  }
}

topUp().catch(console.error);
