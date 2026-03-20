const crypto = require('crypto');
const https = require('https');
const fs = require('fs');
const path = require('path');

function getConfig() {
    if (process.env.KUCOIN_API_KEY && process.env.KUCOIN_SECRET_KEY && process.env.KUCOIN_PASSPHRASE) {
        return {
            apiKey: process.env.KUCOIN_API_KEY,
            secretKey: process.env.KUCOIN_SECRET_KEY,
            passphrase: process.env.KUCOIN_PASSPHRASE
        };
    }

    const homeDir = process.env.HOME || process.env.USERPROFILE;
    if (!homeDir) {
        return null;
    }

    const configPath = path.join(homeDir, '.openclaw/credentials/kucoin.json');
    if (fs.existsSync(configPath)) {
        try {
            return JSON.parse(fs.readFileSync(configPath, 'utf8'));
        } catch (e) {
            return null;
        }
    }

    return null;
}

class KuCoinClient {
    constructor(config = {}) {
        this.apiKey = config.apiKey || process.env.KUCOIN_API_KEY;
        this.secretKey = config.secretKey || process.env.KUCOIN_SECRET_KEY;
        this.passphrase = config.passphrase || process.env.KUCOIN_PASSPHRASE;

        this.baseUrl = 'api.kucoin.com';
        this.futuresUrl = 'api-futures.kucoin.com';
    }

    sign(timestamp, method, endpoint, body = '') {
        const message = timestamp + method + endpoint + body;
        const hmac = crypto.createHmac('sha256', this.secretKey);
        hmac.update(message);
        return hmac.digest('base64');
    }

    request(endpoint, method = 'GET', params = {}) {
        return new Promise((resolve, reject) => {
            const timestamp = Date.now().toString();
            let pathStr = endpoint;
            let body = '';

            if (method === 'GET' && Object.keys(params).length > 0) {
                pathStr += '?' + new URLSearchParams(params).toString();
            } else if ((method === 'POST' || method === 'DELETE') && Object.keys(params).length > 0) {
                body = JSON.stringify(params);
            }

            const signature = this.sign(timestamp, method, pathStr, body);

            const options = {
                hostname: this.baseUrl,
                port: 443,
                path: pathStr,
                method: method,
                headers: {
                    'KC-API-KEY': this.apiKey,
                    'KC-API-SIGN': signature,
                    'KC-API-TIMESTAMP': timestamp,
                    'KC-API-PASSPHRASE': this.passphrase,
                    'Content-Type': 'application/json'
                }
            };

            const req = https.request(options, res => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try {
                        const json = JSON.parse(data);
                        if (json.code && json.code !== '200000') {
                            resolve({ error: json.msg || json.message, code: json.code });
                        } else {
                            resolve(json.data || json);
                        }
                    } catch (e) {
                        resolve({ error: e.message });
                    }
                });
            });

            req.on('error', reject);
            if (body) req.write(body);
            req.end();
        });
    }

    futuresRequest(endpoint, method = 'GET', params = {}) {
        return new Promise((resolve, reject) => {
            const timestamp = Date.now().toString();
            let pathStr = endpoint;
            let body = '';

            if (method === 'GET' && Object.keys(params).length > 0) {
                pathStr += '?' + new URLSearchParams(params).toString();
            } else if ((method === 'POST' || method === 'DELETE') && Object.keys(params).length > 0) {
                body = JSON.stringify(params);
            }

            const signature = this.sign(timestamp, method, pathStr, body);

            const options = {
                hostname: this.futuresUrl,
                port: 443,
                path: pathStr,
                method: method,
                headers: {
                    'KC-API-KEY': this.apiKey,
                    'KC-API-SIGN': signature,
                    'KC-API-TIMESTAMP': timestamp,
                    'KC-API-PASSPHRASE': this.passphrase,
                    'KC-API-SIGN-VERSION': '2',
                    'Content-Type': 'application/json'
                }
            };

            const req = https.request(options, res => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try {
                        const json = JSON.parse(data);
                        if (json.code && json.code !== '200000') {
                            resolve({ error: json.msg || json.message, code: json.code });
                        } else {
                            resolve(json.data || json);
                        }
                    } catch (e) {
                        resolve({ error: e.message });
                    }
                });
            });

            req.on('error', reject);
            if (body) req.write(body);
            req.end();
        });
    }

    getAccounts() {
        return this.request('/api/v3/accounts', 'GET');
    }

    getAccountBalance(currency) {
        return this.request(`/api/v3/accounts?currency=${currency}`, 'GET');
    }

    universalTransfer(params) {
        // 统一使用 v3 universal-transfer 接口
        return this.request('/api/v3/accounts/universal-transfer', 'POST', params);
    }

    futuresAccountOverview(currency = 'USDT') {
        return this.futuresRequest(`/api/v1/account-overview?currency=${currency}`, 'GET');
    }

    async getAllFuturesAccounts() {
        const usdtCoins = ['USDT', 'USDC'];
        const coinMCoins = ['BTC', 'ETH', 'XBT', 'DOT', 'ADA', 'XRP', 'SOL', 'DOGE', 'AVAX', 'MATIC', 'LINK', 'ATOM', 'LTC', 'UNI', 'ETC'];

        const results = { usdtM: [], coinM: [] };

        for (const currency of usdtCoins) {
            try {
                const data = await this.futuresAccountOverview(currency);
                if (!data.error) {
                    const total = parseFloat(data.totalBalance || data.accountEquity || data.marginBalance || 0);
                    if (total > 0) {
                        results.usdtM.push({ currency, ...data });
                    }
                }
            } catch (e) {}
        }

        for (const currency of coinMCoins) {
            try {
                const data = await this.futuresAccountOverview(currency);
                if (!data.error) {
                    const total = parseFloat(data.totalBalance || data.accountEquity || data.marginBalance || 0);
                    if (total > 0) {
                        results.coinM.push({ currency, ...data });
                    }
                }
            } catch (e) {}
        }

        return results;
    }

    createOrder(params) {
        return this.request('/api/v3/orders', 'POST', params);
    }

    cancelOrder(orderId) {
        return this.request(`/api/v3/orders/${orderId}`, 'DELETE');
    }

    getOrders(params) {
        return this.request('/api/v3/orders', 'GET', params);
    }

    getTicker(symbol) {
        return this.request(`/api/v1/market/orderbook/level1?symbol=${symbol}`, 'GET');
    }

    async getPrices(currencies) {
        const prices = {};
        for (const currency of currencies) {
            if (currency === 'USDT' || currency === 'USDC') {
                prices[currency] = 1;
                continue;
            }
            try {
                const ticker = await this.getTicker(`${currency}-USDT`);
                if (!ticker.error) {
                    prices[currency] = parseFloat(ticker.price);
                }
            } catch (e) {
                prices[currency] = 0;
            }
        }
        return prices;
    }

    getKlines(symbol, type, startAt, endAt) {
        return this.request(`/api/v2/market/candles?symbol=${symbol}&type=${type}&startAt=${startAt}&endAt=${endAt}`, 'GET');
    }

    // ========== 杠杆交易相关 API (v3) ==========

    getMarginAccount() {
        return this.request('/api/v3/margin/accounts', 'GET');
    }

    getIsolatedMarginAccount(symbol, quoteCurrency = 'USDT') {
        const params = { queryType: 'ISOLATED' };
        if (symbol) params.symbol = symbol;
        if (quoteCurrency) params.quoteCurrency = quoteCurrency;
        return this.request(`/api/v3/isolated/accounts?${new URLSearchParams(params).toString()}`, 'GET');
    }

    getBorrowable(currency) {
        return this.request(`/api/v1/margin/borrowable?currency=${currency}`, 'GET');
    }

    getBorrowHistory(params = {}) {
        return this.request('/api/v3/margin/borrow/history', 'GET', params);
    }

    getRepayHistory(params = {}) {
        return this.request('/api/v3/margin/repay/history', 'GET', params);
    }

    borrow(params) {
        // Add required timeInForce for borrow requests
        const borrowParams = { ...params, timeInForce: params.timeInForce || 'IOC' };
        return this.request('/api/v3/margin/borrow', 'POST', borrowParams);
    }

    isolatedBorrow(params) {
        return this.request('/api/v3/margin/borrow', 'POST', params);
    }

    repay(params) {
        return this.request('/api/v3/margin/repay', 'POST', params);
    }

    isolatedRepay(params) {
        return this.request('/api/v3/margin/repay', 'POST', params);
    }

    marginOrder(params) {
        return this.request('/api/v3/hf/margin/order', 'POST', params);
    }

    cancelMarginOrder(orderId) {
        return this.request(`/api/v3/margin/orders/${orderId}`, 'DELETE');
    }

    getMarginOrders(params = {}) {
        return this.request('/api/v1/margin/orders', 'GET', params);
    }

    getMarginOrder(orderId) {
        return this.request(`/api/v3/margin/orders/${orderId}`, 'GET');
    }

    getIsolatedOrders(params = {}) {
        return this.request('/api/v1/isolated/orders', 'GET', params);
    }

    getMarginConfig() {
        return this.request('/api/v1/margin/config', 'GET');
    }

    setMarginLeverage(leverage) {
        return this.request('/api/v3/position/update-user-leverage', 'POST', {
            leverage: String(leverage)
        });
    }

    setLeverage(symbol, leverage, marginMode = 'CROSSED') {
        return this.futuresRequest('/api/v1/position/leverage', 'POST', {
            symbol: symbol,
            leverage: parseInt(leverage),
            marginMode: marginMode
        });
    }

    // ========== 合约交易相关 API ==========

    futuresOrder(params) {
        return this.futuresRequest('/api/v1/orders', 'POST', params);
    }

    cancelFuturesOrder(orderId) {
        return this.futuresRequest(`/api/v1/orders/${orderId}`, 'DELETE');
    }

    getFuturesOrders(params = {}) {
        return this.futuresRequest('/api/v1/orders', 'GET', params);
    }

    getFuturesOrder(orderId) {
        return this.futuresRequest(`/api/v1/orders/${orderId}`, 'GET');
    }

    getFuturesPositions(symbol) {
        const endpoint = symbol ? `/api/v1/positions?symbol=${symbol}` : '/api/v1/positions';
        return this.futuresRequest(endpoint, 'GET');
    }

    getFuturesContracts() {
        return this.futuresRequest('/api/v1/contracts/active', 'GET');
    }

    getFuturesTicker(symbol) {
        return this.futuresRequest(`/api/v1/ticker?symbol=${symbol}`, 'GET');
    }
}

module.exports = { KuCoinClient, getConfig };
