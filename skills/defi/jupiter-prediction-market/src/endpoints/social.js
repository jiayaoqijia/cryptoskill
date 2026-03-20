const { JupiterPredictionClient } = require('../client');

class SocialEndpoint extends JupiterPredictionClient {
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

module.exports = { SocialEndpoint };
