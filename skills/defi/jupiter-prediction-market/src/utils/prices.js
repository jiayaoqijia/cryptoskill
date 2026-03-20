const MICRO_USD_DIVISOR = 1000000;

function microUsdToUsd(microUsd) {
  if (microUsd === null || microUsd === undefined) {
    return null;
  }

  const num = typeof microUsd === 'string' ? parseInt(microUsd, 10) : microUsd;
  
  if (isNaN(num)) {
    throw new Error(`Invalid micro USD value: ${microUsd}`);
  }

  return num / MICRO_USD_DIVISOR;
}

function usdToMicroUsd(usd) {
  if (usd === null || usd === undefined) {
    return null;
  }

  const num = typeof usd === 'string' ? parseFloat(usd) : usd;

  if (isNaN(num)) {
    throw new Error(`Invalid USD value: ${usd}`);
  }

  return Math.round(num * MICRO_USD_DIVISOR);
}

function formatUsd(microUsd, decimals = 2) {
  const usd = microUsdToUsd(microUsd);
  if (usd === null) return null;
  return `$${usd.toFixed(decimals)}`;
}

function formatPrice(microUsd) {
  const usd = microUsdToUsd(microUsd);
  if (usd === null) return null;
  return `${(usd * 100).toFixed(0)}¢`;
}

function parsePrice(priceString) {
  if (!priceString) return null;
  const cleaned = priceString.replace(/[$,¢]/g, '');
  return parseFloat(cleaned);
}

function calculateProbability(yesPrice) {
  if (yesPrice === null || yesPrice === undefined) return null;
  if (yesPrice > 1) {
    yesPrice = microUsdToUsd(yesPrice);
  }
  return yesPrice * 100;
}

module.exports = {
  MICRO_USD_DIVISOR,
  microUsdToUsd,
  usdToMicroUsd,
  formatUsd,
  formatPrice,
  parsePrice,
  calculateProbability
};
