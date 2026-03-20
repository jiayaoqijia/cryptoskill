import { borrow } from "../lib/aave.js";

const amount = process.argv[2];
if (!amount) {
  console.error("Usage: node borrow.js <amount_usdc>");
  console.error("Example: node borrow.js 100");
  process.exit(1);
}

try {
  await borrow(amount);
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}
