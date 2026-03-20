import { EXPLORER_URL } from "./config.js";

// Health factor is scaled by 1e18 in Aave
const HF_DECIMALS = 18n;

export function formatHealthFactor(hfRaw) {
  if (hfRaw === 0n) return "N/A (no debt)";

  // MaxUint256 means no debt
  if (hfRaw >= 2n ** 128n) return "N/A (no debt)";

  const hf = Number(hfRaw) / 1e18;
  const hfStr = hf.toFixed(4);

  let label;
  if (hf >= 3) label = "SAFE";
  else if (hf >= 2) label = "GOOD";
  else if (hf >= 1.5) label = "MODERATE";
  else if (hf >= 1.1) label = "WARNING";
  else label = "DANGER";

  return `${hfStr} [${label}]`;
}

// Aave returns USD values scaled by 1e8
export function formatUsdValue(valueRaw) {
  const value = Number(valueRaw) / 1e8;
  return `$${value.toFixed(2)}`;
}

export function txLink(hash) {
  return `${EXPLORER_URL}/tx/${hash}`;
}

export function printAccountSummary(data) {
  console.log("\n--- Aave V3 Account Summary (Base Sepolia) ---");
  console.log(`Total Collateral:    ${formatUsdValue(data.totalCollateralBase)}`);
  console.log(`Total Debt:          ${formatUsdValue(data.totalDebtBase)}`);
  console.log(`Available to Borrow: ${formatUsdValue(data.availableBorrowsBase)}`);
  console.log(`Current LTV:         ${Number(data.ltv) / 100}%`);
  console.log(`Liquidation Threshold: ${Number(data.currentLiquidationThreshold) / 100}%`);
  console.log(`Health Factor:       ${formatHealthFactor(data.healthFactor)}`);
  console.log("-----------------------------------------------\n");
}
