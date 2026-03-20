const { JupiterPredictionClient, JupiterPredictionError, RateLimitError, ApiKeyError } = require('./client');
const { EventsEndpoint } = require('./endpoints/events');
const { MarketsEndpoint } = require('./endpoints/markets');
const { OrdersEndpoint } = require('./endpoints/orders');
const { PositionsEndpoint } = require('./endpoints/positions');
const { PayoutsEndpoint } = require('./endpoints/payouts');
const { HistoryEndpoint } = require('./endpoints/history');
const { SocialEndpoint } = require('./endpoints/social');

const { 
  microUsdToUsd, 
  usdToMicroUsd, 
  formatUsd, 
  formatPrice,
  parsePrice,
  calculateProbability,
  MICRO_USD_DIVISOR 
} = require('./utils/prices');

const { 
  parsePositionsResponse, 
  parseOrdersResponse, 
  parseMarketResponse,
  parseEventResponse,
  parseEventsResponse,
  filterClaimable,
  filterOpen,
  filterByMarket,
  aggregatePnL 
} = require('./utils/parser');

const { 
  JupiterPredictionError: Err,
  ValidationError,
  AuthenticationError,
  NotFoundError,
  handleError,
  withRetry 
} = require('./utils/errors');

const { ApiKeyManager } = require('./utils/api-key');

class JupiterPrediction extends JupiterPredictionClient {
  async list(params = {}) {
    return this.get('/events', params);
  }

  async search(query, limit = 10) {
    return this.get('/events/search', { query, limit });
  }

  async getEvent(eventId) {
    return this.get(`/events/${eventId}`);
  }

  async suggested(pubkey) {
    return this.get(`/events/suggested/${pubkey}`);
  }

  async getMarket(marketId) {
    return this.get(`/markets/${marketId}`);
  }

  async orderbook(marketId) {
    return this.get(`/orderbook/${marketId}`);
  }

  async create(orderData) {
    return this.post('/orders', orderData);
  }

  async listOrders(params = {}) {
    return this.get('/orders', params);
  }

  async status(orderPubkey) {
    return this.get(`/orders/status/${orderPubkey}`);
  }

  async cancelOrder(orderPubkey, ownerPubkey) {
    return this.delete(`/orders/${orderPubkey}`, { ownerPubkey });
  }

  async listPositions(params = {}) {
    if (!params.ownerPubkey) {
      throw new Error('ownerPubkey is required');
    }
    return this.get('/positions', params);
  }

  async getPosition(positionPubkey) {
    return this.get(`/positions/${positionPubkey}`);
  }

  async closePosition(positionPubkey, ownerPubkey) {
    return this.delete(`/positions/${positionPubkey}`, { ownerPubkey });
  }

  async closeAllPositions(ownerPubkey) {
    return this.delete('/positions', { ownerPubkey });
  }

  async claim(positionPubkey, ownerPubkey) {
    return this.post(`/positions/${positionPubkey}/claim`, { ownerPubkey });
  }

  getClaimablePositions(positions) {
    return positions.filter(p => p.claimable === true && p.claimed === false);
  }

  getOpenPositions(positions) {
    return positions.filter(p => p.contracts > 0 && !p.claimed);
  }

  async listHistory(params = {}) {
    if (!params.ownerPubkey) {
      throw new Error('ownerPubkey is required');
    }
    return this.get('/history', params);
  }

  async getHistoryByPosition(positionPubkey, ownerPubkey) {
    return this.get('/history', { positionPubkey, ownerPubkey });
  }

  getEventsByType(history, eventType) {
    return history.filter(event => event.eventType === eventType);
  }

  async profile(pubkey) {
    return this.get(`/profiles/${pubkey}`);
  }

  async pnlHistory(pubkey, interval = '24h', count = 10) {
    return this.get(`/profiles/${pubkey}/pnl-history`, { interval, count });
  }

  async trades(params = {}) {
    return this.get('/trades', params);
  }

  async leaderboards(params = {}) {
    const { period = 'weekly', metric = 'pnl', limit = 10 } = params;
    return this.get('/leaderboards', { period, metric, limit });
  }

  async follow(pubkey) {
    return this.post(`/follow/${pubkey}`);
  }

  async unfollow(pubkey) {
    return this.delete(`/unfollow/${pubkey}`);
  }

  async followers(pubkey) {
    return this.get(`/followers/${pubkey}`);
  }

  async following(pubkey) {
    return this.get(`/following/${pubkey}`);
  }
}

function createClient(options = {}) {
  return new JupiterPrediction(options);
}

module.exports = {
  JupiterPredictionClient,
  JupiterPrediction,
  createClient,
  ApiKeyError,
  ApiKeyManager,
  microUsdToUsd,
  usdToMicroUsd,
  formatUsd,
  formatPrice,
  parsePrice,
  calculateProbability,
  MICRO_USD_DIVISOR,
  parsePositionsResponse,
  parseOrdersResponse,
  parseMarketResponse,
  parseEventResponse,
  parseEventsResponse,
  filterClaimable,
  filterOpen,
  filterByMarket,
  aggregatePnL,
  JupiterPredictionError: Err,
  ValidationError,
  AuthenticationError,
  RateLimitError,
  NotFoundError,
  handleError,
  withRetry
};
