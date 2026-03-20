import { deposit } from "../lib/aave.js";

const amount = process.argv[2];
if (!amount) {
  console.error("Usage: node deposit.js <amount_eth>");
  console.error("Example: node deposit.js 0.5");
  process.exit(1);
}

try {
  await deposit(amount);
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}
