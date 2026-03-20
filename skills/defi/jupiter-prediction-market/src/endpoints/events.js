const { JupiterPredictionClient } = require('../client');

class EventsEndpoint extends JupiterPredictionClient {
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
}

module.exports = { EventsEndpoint };
