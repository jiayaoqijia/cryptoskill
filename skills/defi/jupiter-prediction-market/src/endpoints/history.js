const { JupiterPredictionClient } = require('../client');

class HistoryEndpoint extends JupiterPredictionClient {
  async list(params = {}) {
    if (!params.ownerPubkey) {
      throw new Error('ownerPubkey is required');
    }
    return this.get('/history', params);
  }

  async getByPosition(positionPubkey, ownerPubkey) {
    return this.get('/history', { positionPubkey, ownerPubkey });
  }

  getEventsByType(history, eventType) {
    return history.filter(event => event.eventType === eventType);
  }
}

module.exports = { HistoryEndpoint };
