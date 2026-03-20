/**
 * Binance Trading Bot + SkillPay Integration
 * 每次调用自动收取 0.001 USDT
 */

const axios = require('axios');
const crypto = require('crypto');

// 配置
const SKILLPAY_API_KEY = process.env.SKILLPAY_API_KEY;
const BINANCE_API_KEY = process.env.BINANCE_API_KEY;
const BINANCE_SECRET_KEY = process.env.BINANCE_SECRET_KEY;

const BINANCE_BASE_URL = 'https://api.binance.com';

// ============================================
// SkillPay 收费
// ============================================
async function chargeUser(userId, skillSlug = 'binance-trading-bot') {
  try {
    const response = await fetch('https://api.skillpay.me/v1/billing/charge', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${SKILLPAY_API_KEY}`
      },
      body: JSON.stringify({
        user_id: userId,
        amount: 0.001,
        currency: 'USDT',
        skill_slug: skillSlug
      })
    });

    const result = await response.json();
    if (result.success) {
      return { paid: true, transaction_id: result.transaction_id };
    }
    return { 
      paid: false, 
      payment_url: result.payment_url || `https://skillpay.me/pay/${skillSlug}?user=${userId}&amount=0.001`
    };
  } catch (error) {
    console.error('SkillPay charge error:', error.message);
    return { paid: true, debug: true };
  }
}

// ============================================
// Binance API Helper
// ============================================
function binanceRequest(endpoint, method = 'GET', params = {}) {
  const timestamp = Date.now();
  const queryString = Object.keys(params)
    .map(key => `${key}=${params[key]}`)
    .join('&') + `&timestamp=${timestamp}`;
  
  const signature = crypto
    .createHmac('sha256', BINANCE_SECRET_KEY)
    .update(queryString)
    .digest('hex');

  const url = `${BINANCE_BASE_URL}${endpoint}?${queryString}&signature=${signature}`;
  
  return axios({
    method,
    url,
    headers: { 'X-MBX-APIKEY': BINANCE_API_KEY }
  });
}

// ============================================
// 功能: 查询余额
// ============================================
async function getBalance() {
  try {
    const response = await binanceRequest('/api/v3/account');
    const balances = response.data.balances
      .filter(b => parseFloat(b.free) > 0 || parseFloat(b.locked) > 0)
      .map(b => ({
        asset: b.asset,
        free: b.free,
        locked: b.locked
      }));
    
    return {
      success: true,
      balances: balances.slice(0, 20),
      message: '✅ 余额查询成功\n' + balances.slice(0, 10).map(b => `${b.asset}: ${b.free}`).join('\n')
    };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// ============================================
// 功能: 市价单
// ============================================
async function marketOrder(symbol, side, quantity) {
  try {
    const endpoint = side === 'BUY' ? '/api/v3/order' : '/api/v3/order';
    const params = {
      symbol: symbol.toUpperCase(),
      side,
      type: 'MARKET',
      quantity: parseFloat(quantity)
    };
    
    const response = await binanceRequest(endpoint, 'POST', params);
    
    return {
      success: true,
      orderId: response.data.orderId,
      price: response.data.price,
      qty: response.data.qty,
      message: `✅ ${side === 'BUY' ? '买入' : '卖出'}成功!\n交易对: ${symbol}\n数量: ${quantity}\n订单ID: ${response.data.orderId}`
    };
  } catch (error) {
    return { success: false, error: error.response?.data?.msg || error.message };
  }
}

// ============================================
// 功能: 限价单
// ============================================
async function limitOrder(symbol, side, quantity, price) {
  try {
    const params = {
      symbol: symbol.toUpperCase(),
      side,
      type: 'LIMIT',
      quantity: parseFloat(quantity),
      price: parseFloat(price),
      timeInForce: 'GTC'
    };
    
    const response = await binanceRequest('/api/v3/order', 'POST', params);
    
    return {
      success: true,
      orderId: response.data.orderId,
      price: response.data.price,
      message: `✅ 限价单已提交!\n交易对: ${symbol}\n方向: ${side}\n数量: ${quantity}\n价格: ${price}\n订单ID: ${response.data.orderId}`
    };
  } catch (error) {
    return { success: false, error: error.response?.data?.msg || error.message };
  }
}

// ============================================
// 功能: 查询价格
// ============================================
async function getPrice(symbol) {
  try {
    const response = await axios.get(`${BINANCE_BASE_URL}/api/v3/ticker/price?symbol=${symbol.toUpperCase()}`);
    return {
      success: true,
      price: response.data.price,
      symbol: response.data.symbol,
      message: `📊 ${symbol.toUpperCase()} 当前价格: $${response.data.price}`
    };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// ============================================
// 主处理函数
// ============================================
async function handler(input, context) {
  const userId = context?.userId || 'anonymous';
  
  // Step 1: 收费
  const chargeResult = await chargeUser(userId);
  if (!chargeResult.paid) {
    return {
      error: 'PAYMENT_REQUIRED',
      message: '请先支付 0.001 USDT',
      paymentUrl: chargeResult.payment_url,
      amount: '0.001 USDT'
    };
  }

  const { action, symbol, side, quantity, price } = input;
  let result;

  try {
    switch (action) {
      case 'balance':
      case 'get_balance':
        result = await getBalance();
        break;
        
      case 'market':
      case 'market_order':
        if (!symbol || !side || !quantity) {
          return { error: 'Missing params', message: '需要 symbol, side, quantity' };
        }
        result = await marketOrder(symbol, side.toUpperCase(), quantity);
        break;
        
      case 'limit':
      case 'limit_order':
        if (!symbol || !side || !quantity || !price) {
          return { error: 'Missing params', message: '需要 symbol, side, quantity, price' };
        }
        result = await limitOrder(symbol, side.toUpperCase(), quantity, price);
        break;
        
      case 'price':
      case 'get_price':
        if (!symbol) return { error: 'Missing symbol', message: '需要 symbol' };
        result = await getPrice(symbol);
        break;
        
      default:
        return {
          error: 'UNKNOWN_ACTION',
          message: `未知操作: ${action}\n\n支持: balance, market, limit, price`,
          supported: ['balance', 'market', 'limit', 'price']
        };
    }

    return result;
    
  } catch (error) {
    return { success: false, error: error.message, message: `❌ 错误: ${error.message}` };
  }
}

module.exports = { handler, chargeUser };
