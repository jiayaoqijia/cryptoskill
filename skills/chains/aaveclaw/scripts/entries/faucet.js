import { mintTestTokens } from "../lib/aave.js";

const token = process.argv[2];
const amount = process.argv[3];

if (!token || !amount) {
  console.error("Usage: node faucet.js <weth|usdc> <amount>");
  console.error("Example: node faucet.js weth 1");
  console.error("Example: node faucet.js usdc 1000");
  process.exit(1);
}

try {
  await mintTestTokens(token, amount);
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}
