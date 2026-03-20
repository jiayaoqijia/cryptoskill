import { getHealthFactor } from "../lib/aave.js";

const address = process.argv[2] || undefined;

try {
  await getHealthFactor(address);
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}
