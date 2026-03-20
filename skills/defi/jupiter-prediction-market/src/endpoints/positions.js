const { JupiterPredictionClient } = require('../client');

class PositionsEndpoint extends JupiterPredictionClient {
  async list(params = {}) {
    if (!params.ownerPubkey) {
      throw new Error('ownerPubkey is required');
    }
    return this.get('/positions', params);
  }

  async get(positionPubkey) {
    return this.get(`/positions/${positionPubkey}`);
  }

  async close(positionPubkey, ownerPubkey) {
    return this.delete(`/positions/${positionPubkey}`, { ownerPubkey });
  }

  async closeAll(ownerPubkey) {
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
}

module.exports = { PositionsEndpoint };
