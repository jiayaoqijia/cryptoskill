import { withdraw } from "../lib/aave.js";

const amount = process.argv[2];
if (!amount) {
  console.error("Usage: node withdraw.js <amount_eth|max>");
  console.error("Example: node withdraw.js 0.5");
  console.error("Example: node withdraw.js max");
  process.exit(1);
}

try {
  await withdraw(amount);
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}
