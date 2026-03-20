const { KuCoinClient, getConfig } = require('../lib/kucoin-client');

const args = process.argv.slice(2);
let params = { symbol: 'BTC-USDT' };

for (let i = 0; i < args.length; i += 2) {
    const key = args[i]?.replace('--', '');
    const value = args[i + 1];
    if (key && value) params[key] = value;
}

async function runMarket() {
    try {
        const client = new KuCoinClient(getConfig());
        console.log(`\n📈 **KuCoin (KC) 市场数据 - ${params.symbol}**\n`);

        const ticker = await client.getTicker(params.symbol);
        if (ticker.error) {
            console.error('Error fetching ticker:', ticker.error);
            return;
        }

        const price = parseFloat(ticker.price);
        const bestBid = parseFloat(ticker.bestBid);
        const bestAsk = parseFloat(ticker.bestAsk);
        const bestBidSize = parseFloat(ticker.bestBidSize);
        const bestAskSize = parseFloat(ticker.bestAskSize);

        console.log(`💰 **当前价格:** ${price.toFixed(2)} USDT`);
        console.log(`📊 **盘口数据:**`);
        console.log(`  • 买一: ${bestBid.toFixed(2)} USDT (${bestBidSize.toFixed(6)})`);
        console.log(`  • 卖一: ${bestAsk.toFixed(2)} USDT (${bestAskSize.toFixed(6)})`);
    } catch (error) {
        console.error('Error:', error.message);
    }
}

runMarket();
