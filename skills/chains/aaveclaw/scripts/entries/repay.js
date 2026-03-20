import { repay } from "../lib/aave.js";

const amount = process.argv[2];
if (!amount) {
  console.error("Usage: node repay.js <amount_usdc|max>");
  console.error("Example: node repay.js 50");
  console.error("Example: node repay.js max");
  process.exit(1);
}

try {
  await repay(amount);
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}
