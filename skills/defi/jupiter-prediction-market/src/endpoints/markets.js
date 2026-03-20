const { JupiterPredictionClient } = require('../client');

class MarketsEndpoint extends JupiterPredictionClient {
  async getMarket(marketId) {
    return this.get(`/markets/${marketId}`);
  }

  async orderbook(marketId) {
    return this.get(`/orderbook/${marketId}`);
  }
}

module.exports = { MarketsEndpoint };
