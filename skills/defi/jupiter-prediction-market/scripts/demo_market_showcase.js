// Demo script to showcase Phase 2 usage for market_manager.js
const marketManager = require('../src/market_manager');

async function demo() {
  try {
    const events = await marketManager.listEvents({ category: 'crypto', filter: 'trending', includeMarkets: 'true' });
    console.log('Trending Crypto Events:', events);
    if (events && events.data && events.data.length) {
      const event = events.data[0];
      const marketId = event.marketId || event.eventId;
      if (marketId) {
        const market = await marketManager.getMarketDetails(marketId);
        console.log('Market Details:', market);
        const ob = await marketManager.getOrderBook(marketId);
        console.log('Order Book:', ob);
      }
    }
  } catch (e) {
    console.error('Demo error:', e);
  }
}

demo();
