const { microUsdToUsd, formatUsd } = require('./prices');

function parsePositionsResponse(response) {
  if (!response) return [];
  
  const data = response.data || response;
  if (!Array.isArray(data)) {
    return [];
  }

  return data.map(position => ({
    ...position,
    contracts: parseInt(position.contracts, 10) || 0,
    totalCostUsd: microUsdToUsd(position.totalCostUsd),
    avgPriceUsd: microUsdToUsd(position.avgPriceUsd),
    valueUsd: microUsdToUsd(position.valueUsd),
    markPriceUsd: microUsdToUsd(position.markPriceUsd),
    pnlUsd: microUsdToUsd(position.pnlUsd),
    pnlUsdPercent: parseFloat(position.pnlUsdPercent) || 0,
    pnlUsdAfterFees: microUsdToUsd(position.pnlUsdAfterFees),
    pnlUsdAfterFeesPercent: parseFloat(position.pnlUsdAfterFeesPercent) || 0,
    realizedPnlUsd: microUsdToUsd(position.realizedPnlUsd),
    feesPaidUsd: microUsdToUsd(position.feesPaidUsd),
    payoutUsd: microUsdToUsd(position.payoutUsd),
    claimedUsd: microUsdToUsd(position.claimedUsd),
    claimable: position.claimable === true,
    claimed: position.claimed === true
  }));
}

function parseOrdersResponse(response) {
  if (!response) return [];
  
  const data = response.data || response;
  if (!Array.isArray(data)) {
    return [];
  }

  return data.map(order => ({
    ...order,
    contracts: parseInt(order.contracts, 10) || 0,
    filledContracts: parseInt(order.filledContracts, 10) || 0,
    avgFillPriceUsd: microUsdToUsd(order.avgFillPriceUsd),
    totalCostUsd: microUsdToUsd(order.totalCostUsd),
    feesPaidUsd: microUsdToUsd(order.feesPaidUsd),
    createdAt: order.createdAt ? new Date(order.createdAt * 1000) : null,
    filledAt: order.filledAt ? new Date(order.filledAt * 1000) : null
  }));
}

function parseMarketResponse(market) {
  if (!market) return null;

  const pricing = market.pricing || {};

  const buyYesPriceUsd = pricing.buyYesPriceUsd ?? market.buyYesPriceUsd;
  const sellYesPriceUsd = pricing.sellYesPriceUsd ?? market.sellYesPriceUsd;
  const buyNoPriceUsd = pricing.buyNoPriceUsd ?? market.buyNoPriceUsd;
  const sellNoPriceUsd = pricing.sellNoPriceUsd ?? market.sellNoPriceUsd;
  const volumeUsd = pricing.volume ?? market.volumeUsd;

  return {
    ...market,
    marketId: market.marketId,
    title: market.metadata?.title || market.title,
    status: market.status,
    result: market.result,
    buyYesPriceUsd: microUsdToUsd(buyYesPriceUsd),
    sellYesPriceUsd: microUsdToUsd(sellYesPriceUsd),
    buyNoPriceUsd: microUsdToUsd(buyNoPriceUsd),
    sellNoPriceUsd: microUsdToUsd(sellNoPriceUsd),
    volumeUsd: microUsdToUsd(volumeUsd),
    liquidityUsd: microUsdToUsd(market.liquidityUsd),
    openInterest: parseInt(market.openInterest, 10) || 0,
    closeTime: market.closeTime,
    openTime: market.openTime
  };
}

function parseEventResponse(event) {
  if (!event) return null;

  return {
    ...event,
    eventId: event.eventId,
    title: event.metadata?.title || event.title,
    category: event.category,
    subcategory: event.subcategory,
    isTrending: event.isTrending,
    isLive: event.isLive,
    volumeUsd: microUsdToUsd(event.volumeUsd),
    closeTime: event.metadata?.closeTime,
    markets: event.markets ? event.markets.map(m => parseMarketResponse(m)) : []
  };
}

function parseEventsResponse(response) {
  if (!response) return { data: [] };
  
  const data = response.data || response;
  if (!Array.isArray(data)) {
    return { data: [] };
  }

  return {
    ...response,
    data: data.map(parseEventResponse)
  };
}

function filterClaimable(positions) {
  return positions.filter(p => p.claimable && !p.claimed);
}

function filterOpen(positions) {
  return positions.filter(p => p.contracts > 0 && !p.claimed);
}

function filterByMarket(positions, marketId) {
  return positions.filter(p => p.marketId === marketId);
}

function aggregatePnL(positions) {
  if (!positions || positions.length === 0) {
    return { totalValue: 0, totalCost: 0, totalPnL: 0, totalRealizedPnL: 0, totalFees: 0 };
  }
  
  return positions.reduce((acc, pos) => ({
    totalValue: (acc.totalValue || 0) + (pos.valueUsd || 0),
    totalCost: (acc.totalCost || 0) + (pos.totalCostUsd || 0),
    totalPnL: (acc.totalPnL || 0) + (pos.pnlUsd || 0),
    totalRealizedPnL: (acc.totalRealizedPnL || 0) + (pos.realizedPnlUsd || 0),
    totalFees: (acc.totalFees || 0) + (pos.feesPaidUsd || 0)
  }), { totalValue: 0, totalCost: 0, totalPnL: 0, totalRealizedPnL: 0, totalFees: 0 });
}

module.exports = {
  parsePositionsResponse,
  parseOrdersResponse,
  parseMarketResponse,
  parseEventResponse,
  parseEventsResponse,
  filterClaimable,
  filterOpen,
  filterByMarket,
  aggregatePnL
};
