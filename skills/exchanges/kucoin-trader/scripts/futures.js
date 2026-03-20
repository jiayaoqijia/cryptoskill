const { KuCoinClient, getConfig } = require('../lib/kucoin-client');

const args = process.argv.slice(2);
const command = args[0];
const params = {};

for (let i = 1; i < args.length; i += 2) {
    const key = args[i]?.replace('--', '');
    const value = args[i + 1];
    if (key && value) params[key] = value;
}

const COMMANDS = {
    'balance': '查询合约账户余额',
    'positions': '查询持仓',
    'ticker': '查询合约行情',
    'contracts': '查询合约列表',
    'trade': '合约下单',
    'orders': '查询合约订单',
    'cancel': '取消合约订单'
};

async function runFuturesCommand() {
    const client = new KuCoinClient(getConfig());

    if (!command || command === 'help' || command === '--help') {
        console.log('\n⚡ **KuCoin 合约交易命令帮助**\n');
        console.log('用法: node futures.js <命令> [参数]\n');
        console.log('可用命令:');
        for (const [cmd, desc] of Object.entries(COMMANDS)) {
            console.log(`  ${cmd.padEnd(12)} - ${desc}`);
        }
        console.log('\n示例:');
        console.log('  node futures.js balance');
        console.log('  node futures.js balance --currency USDT');
        console.log('  node futures.js positions');
        console.log('  node futures.js positions --symbol XBTUSDTM');
        console.log('  node futures.js ticker --symbol XBTUSDTM');
        console.log('  node futures.js contracts');
        console.log('  node futures.js trade --symbol XBTUSDTM --side buy --size 1');
        console.log('  node futures.js trade --symbol XBTUSDTM --side sell --size 1 --price 50000');
        console.log('  node futures.js orders --symbol XBTUSDTM');
        console.log('  node futures.js cancel --orderId xxx');
        console.log('\n资金划转请使用: node transfer.js');
        return;
    }

    try {
        switch (command) {
            case 'balance':
                await getBalance(client, params.currency);
                break;
            case 'positions':
                await getPositions(client, params.symbol);
                break;
            case 'ticker':
                await getTicker(client, params.symbol);
                break;
            case 'contracts':
                await getContracts(client);
                break;
            case 'trade':
                await placeOrder(client);
                break;
            case 'orders':
                await getOrders(client, params.symbol, params.status);
                break;
            case 'cancel':
                await cancelOrder(client, params.orderId);
                break;
            default:
                console.error(`未知命令: ${command}`);
                console.log('运行 "node futures.js help" 查看帮助');
        }
    } catch (error) {
        console.error('❌ 错误:', error.message);
        process.exit(1);
    }
}

async function getBalance(client, currency) {
    const curr = currency || 'USDT';
    console.log(`\n⚡ **查询合约账户余额 (${curr})**\n`);

    const result = await client.futuresAccountOverview(curr);
    if (result.error) {
        console.error('❌ 查询失败:', result.error);
        process.exit(1);
    }

    console.log(`  账户余额: ${parseFloat(result.balance || 0).toFixed(8)} ${curr}`);
    console.log(`  可用余额: ${parseFloat(result.availableBalance || 0).toFixed(8)} ${curr}`);
    console.log(`  冻结金额: ${parseFloat(result.hold || 0).toFixed(8)} ${curr}`);
    console.log(`  账户权益: ${parseFloat(result.accountEquity || 0).toFixed(8)} ${curr}`);
    console.log(`  已实现盈亏: ${parseFloat(result.realizedPnl || 0).toFixed(8)} ${curr}`);
    console.log(`  未实现盈亏: ${parseFloat(result.unrealizedPnl || 0).toFixed(8)} ${curr}`);
    console.log(`  保证金余额: ${parseFloat(result.marginBalance || 0).toFixed(8)} ${curr}`);
}

async function getPositions(client, symbol) {
    console.log('\n⚡ **查询合约持仓**\n');

    const result = await client.getFuturesPositions(symbol);
    if (result.error) {
        console.error('❌ 查询失败:', result.error);
        process.exit(1);
    }

    const positions = Array.isArray(result) ? result : [result];
    if (positions.length === 0 || !positions[0]) {
        console.log('  暂无持仓');
        return;
    }

    const activePositions = positions.filter(p => p && (parseFloat(p.openOrderSize) > 0 || parseFloat(p.size) !== 0));
    if (activePositions.length === 0) {
        console.log('  暂无持仓');
        return;
    }

    console.log(`共 ${activePositions.length} 个持仓:\n`);
    activePositions.forEach(pos => {
        const side = parseFloat(pos.size) > 0 ? '多仓' : '空仓';
        const size = Math.abs(parseFloat(pos.size));
        const entryPrice = parseFloat(pos.avgEntryPrice || pos.entryPrice || 0);
        const markPrice = parseFloat(pos.markPrice || 0);
        const unrealizedPnl = parseFloat(pos.unrealizedPnl || 0);
        const roe = parseFloat(pos.roe || 0) * 100;

        console.log(`  ${pos.symbol}:`);
        console.log(`    方向: ${side}`);
        console.log(`    数量: ${size}`);
        console.log(`    开仓价格: ${entryPrice.toFixed(4)}`);
        console.log(`    标记价格: ${markPrice.toFixed(4)}`);
        console.log(`    未实现盈亏: ${unrealizedPnl.toFixed(4)}`);
        console.log(`    收益率: ${roe.toFixed(2)}%`);
        console.log(`    杠杆: ${pos.leverage || '1'}x`);
        console.log('');
    });
}

async function getTicker(client, symbol) {
    if (!symbol) {
        console.error('❌ 请指定合约: --symbol XBTUSDTM');
        process.exit(1);
    }
    console.log(`\n⚡ **查询合约行情 ${symbol}**\n`);

    const result = await client.getFuturesTicker(symbol);
    if (result.error) {
        console.error('❌ 查询失败:', result.error);
        process.exit(1);
    }

    console.log(`  最新价格: ${result.price || result.last}`);
    console.log(`  买一价: ${result.bestBid || result.bid}`);
    console.log(`  卖一价: ${result.bestAsk || result.ask}`);
    console.log(`  24h成交量: ${result.size || result.volume}`);
    console.log(`  24h涨跌: ${result.change || result.priceChange || '0'}%`);
    console.log(`  24h最高: ${result.high || result.priceHigh}`);
    console.log(`  24h最低: ${result.low || result.priceLow}`);
}

async function getContracts(client) {
    console.log('\n⚡ **查询可用合约**\n');

    const result = await client.getFuturesContracts();
    if (result.error) {
        console.error('❌ 查询失败:', result.error);
        process.exit(1);
    }

    const contracts = result.data || result;
    if (!contracts || contracts.length === 0) {
        console.log('  暂无可用合约');
        return;
    }

    console.log(`共 ${contracts.length} 个合约:\n`);
    contracts.slice(0, 20).forEach(c => {
        console.log(`  ${c.symbol}:`);
        console.log(`    名称: ${c.name}`);
        console.log(`    合约类型: ${c.type}`);
        console.log(`    基础币种: ${c.baseCurrency}`);
        console.log(`    计价币种: ${c.quoteCurrency}`);
        console.log(`    合约大小: ${c.size}`);
        console.log('');
    });
    if (contracts.length > 20) {
        console.log(`  ... 还有 ${contracts.length - 20} 个合约`);
    }
}

async function placeOrder(client) {
    const symbol = params.symbol || params.s;
    const side = params.side || params.sd;
    const size = params.size || params.q || params.amount;
    const price = params.price || params.p;
    const type = params.type || (price ? 'limit' : 'market');
    const leverage = params.leverage || params.l;

    if (!symbol || !side || !size) {
        console.error('❌ 请指定必要参数: --symbol XBTUSDTM --side buy --size 1');
        console.error('  方向: buy (做多) / sell (做空)');
        console.error('  示例: node futures.js trade --symbol XBTUSDTM --side sell --size 10 --leverage 5');
        process.exit(1);
    }

    const sideLabel = side === 'buy' ? '做多' : '做空';
    const typeLabel = type === 'market' ? '市价' : '限价';
    const marginMode = params.marginMode || params.m || 'CROSS';

    console.log('\n⚡ **合约下单**');
    console.log(`  合约: ${symbol}`);
    console.log(`  方向: ${sideLabel}`);
    console.log(`  类型: ${typeLabel}`);
    console.log(`  数量: ${size}`);
    if (price) {
        console.log(`  价格: ${price}\n`);
    } else {
        console.log('');
    }

    if (leverage) {
        console.log(`  杠杆: ${leverage}x`);
        const leverageResult = await client.setLeverage(symbol, leverage, marginMode);
        if (leverageResult.error) {
            console.error('❌ 设置杠杆失败:', leverageResult.error);
            process.exit(1);
        }
        console.log(`  ✅ 杠杆设置成功\n`);
    }

    const orderParams = {
        clientOid: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        side: side,
        symbol: symbol,
        size: size,
        type: type,
        leverage: leverage || '125',
        marginMode: marginMode
    };

    if (price) {
        orderParams.price = price;
    }

    const result = await client.futuresOrder(orderParams);

    if (result.error) {
        console.error('❌ 下单失败:', result.error);
        process.exit(1);
    }
    console.log('✅ 下单成功');
    console.log(`  订单ID: ${result.orderId}`);
    console.log(`  Client OID: ${orderParams.clientOid}`);
}

async function getOrders(client, symbol, status) {
    console.log('\n⚡ **查询合约订单**\n');

    const queryParams = {};
    if (symbol) queryParams.symbol = symbol;
    if (status) queryParams.status = status;

    const result = await client.getFuturesOrders(queryParams);

    if (result.error) {
        console.error('❌ 查询失败:', result.error);
        process.exit(1);
    }

    const orders = result.data || result;
    if (!orders || orders.length === 0) {
        console.log('  暂无订单记录');
        return;
    }

    console.log(`共 ${orders.length} 个订单:\n`);
    orders.forEach(order => {
        const sideLabel = order.side === 'buy' ? '做多' : '做空';
        console.log(`  订单ID: ${order.id || order.orderId}`);
        console.log(`    合约: ${order.symbol}`);
        console.log(`    方向: ${sideLabel}`);
        console.log(`    类型: ${order.type}`);
        console.log(`    数量: ${order.size}`);
        console.log(`    价格: ${order.price || '市价'}`);
        console.log(`    状态: ${order.status}`);
        console.log(`    创建时间: ${new Date(order.createdAt || order.createdTime).toLocaleString()}`);
        console.log('');
    });
}

async function cancelOrder(client, orderId) {
    if (!orderId) {
        console.error('❌ 请指定订单ID: --orderId xxx');
        process.exit(1);
    }
    console.log(`\n⚡ **取消合约订单 ${orderId}**\n`);

    const result = await client.cancelFuturesOrder(orderId);

    if (result.error) {
        console.error('❌ 取消失败:', result.error);
        process.exit(1);
    }
    console.log('✅ 订单已取消');
}

runFuturesCommand();
