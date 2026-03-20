const { JupiterPredictionClient } = require('../client');

class PayoutsEndpoint extends JupiterPredictionClient {
  async claim(positionPubkey, ownerPubkey) {
    return this.post(`/positions/${positionPubkey}/claim`, { ownerPubkey });
  }
}

module.exports = { PayoutsEndpoint };
