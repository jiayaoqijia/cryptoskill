const { JupiterPredictionClient } = require('../client');

class OrdersEndpoint extends JupiterPredictionClient {
  async create(orderData) {
    const required = ['ownerPubkey', 'marketId', 'isYes', 'isBuy', 'depositAmount', 'depositMint'];
    const missing = required.filter(field => !orderData[field]);

    if (missing.length > 0) {
      throw new Error(`Missing required fields: ${missing.join(', ')}`);
    }

    return this.post('/orders', orderData);
  }

  async list(params = {}) {
    return this.get('/orders', params);
  }

  async status(orderPubkey) {
    return this.get(`/orders/status/${orderPubkey}`);
  }

  async cancel(orderPubkey, ownerPubkey) {
    return this.delete(`/orders/${orderPubkey}`, { ownerPubkey });
  }
}

module.exports = { OrdersEndpoint };
