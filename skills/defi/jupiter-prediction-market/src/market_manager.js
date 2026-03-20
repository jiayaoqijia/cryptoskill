// Phase 2 - Market Discovery (Read-Only)
// Purpose: Provide lightweight wrappers around the Jupiter Prediction Market API for events, markets and orderbook.
// Dependencies:
// - api_client.js singleton (export: { get, post, delete })
// - utils.js: presentation helpers (microUsdToUsd, calculateImpliedProbability, formatTimestamp)

const api = require('../api_client');
const { microUsdToUsd, calculateImpliedProbability, formatTimestamp } = require('../utils');

/**
 * Market Manager - Phase 2 (Read-Only)
 * Exposes small, stable wrappers around the Prediction API for discovery of events/markets
 * and for retrieving current market data including order books and trading status.
 */
async function listEvents(filters = {}) {
  const query = new URLSearchParams(filters).toString();
  const endpoint = '/events' + (query ? `?${query}` : '');
  return api.get(endpoint);
}

async function searchEvents(query, limit = 10) {
  const endpoint = '/events/search?' + new URLSearchParams({ query, limit }).toString();
  return api.get(endpoint);
}

async function getEventDetails(eventId) {
  const endpoint = `/events/${eventId}`;
  return api.get(endpoint);
}

async function getMarketDetails(marketId) {
  const endpoint = `/markets/${marketId}`;
  const market = await api.get(endpoint);
  // Enriquecer con probabilidad implícita si existe buyYesPriceUsd
  if (market && market.buyYesPriceUsd) {
    market.impliedYesPct = calculateImpliedProbability(market.buyYesPriceUsd);
  }
  return market;
}

async function getOrderBook(marketId) {
  const endpoint = `/orderbook/${marketId}`;
  return api.get(endpoint);
}

async function getTradingStatus() {
  const endpoint = '/trading-status';
  return api.get(endpoint);
}

module.exports = {
  listEvents,
  searchEvents,
  getEventDetails,
  getMarketDetails,
  getOrderBook,
  getTradingStatus,
};
