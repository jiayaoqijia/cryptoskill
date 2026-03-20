#!/usr/bin/env node
// wallet-gen.mjs — Generate a new EVM wallet for x402 payments
// Usage: node wallet-gen.mjs [--out <file>]
// Outputs private key and address. Optionally saves key to file.

import { generatePrivateKey, privateKeyToAccount } from "viem/accounts";

const args = process.argv.slice(2);
let outFile = null;
for (let i = 0; i < args.length; i++) {
  if (args[i] === "--out") outFile = args[++i];
}

const key = generatePrivateKey();
const account = privateKeyToAccount(key);

console.log(`Address:     ${account.address}`);
console.log(`Private Key: ${key}`);
console.log(`Network:     Base Sepolia (eip155:84532)`);
console.log();
console.log("Next steps:");
console.log("1. Get Base Sepolia ETH: https://www.alchemy.com/faucets/base-sepolia");
console.log("2. Get Base Sepolia USDC: https://faucet.circle.com/ (select Base Sepolia + USDC)");
console.log(`3. Send ETH and USDC to: ${account.address}`);

if (outFile) {
  const { writeFileSync } = await import("fs");
  writeFileSync(outFile, key + "\n", { mode: 0o600 });
  console.log(`\nPrivate key saved to: ${outFile}`);
}
