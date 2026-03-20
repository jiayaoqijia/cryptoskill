const { KuCoinClient, getConfig } = require('../lib/kucoin-client');

const args = process.argv.slice(2);
const command = args[0] || 'trade';
let params = {
    symbol: 'BTC-USDT',
    side: 'buy',
    type: 'limit',
    price: '0',
    size: '0'
};

for (let i = 1; i < args.length; i += 2) {
    const key = args[i]?.replace('--', '');
    const value = args[i + 1];
    if (key && value) params[key] = value;
}

async function runSpot() {
    try {
        const client = new KuCoinClient(getConfig());
        
        if (command === 'help') {
            console.log('\n📖 **现货交易帮助**\n');
            console.log('  node spot.js trade --symbol BTC-USDT --side buy --size 0.01');
            console.log('  node spot.js trade --symbol BTC-USDT --side sell --size 0.01 --price 50000');
            console.log('  node spot.js orders --symbol BTC-USDT');
            console.log('  node spot.js cancel --orderId xxx');
            console.log('\n资金划转请使用: node transfer.js');
            return;
        }

        switch (command) {
            case 'trade':
                await placeOrder(client);
                break;
            case 'orders':
                await getOrders(client, params.symbol);
                break;
            case 'cancel':
                await cancelOrder(client, params.orderId);
                break;
            default:
                console.error(`未知命令: ${command}`);
                console.log('运行 "node spot.js help" 查看帮助');
        }
    } catch (error) {
        console.error('❌ 错误:', error.message);
        process.exit(1);
    }
}

async function placeOrder(client) {
    const orderType = params.type === 'market' ? '市价' : '限价';
    const sideLabel = params.side === 'buy' ? '买入' : '卖出';
    
    console.log(`\n📝 **提交订单**`);
    console.log(`  • 交易对: ${params.symbol}`);
    console.log(`  • 方向: ${sideLabel}`);
    console.log(`  • 类型: ${orderType}`);
    if (params.type === 'limit') {
        console.log(`  • 价格: ${params.price} USDT`);
    }
    console.log(`  • 数量: ${params.size}\n`);

    const orderParams = {
        clientOid: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        side: params.side,
        symbol: params.symbol,
        type: params.type,
        size: params.size
    };

    if (params.type === 'limit' && params.price) {
        orderParams.price = params.price;
    }

    const result = await client.createOrder(orderParams);

    if (result.error) {
        console.error('❌ 下单失败:', result.error);
        process.exit(1);
    }

    console.log('✅ **下单成功**');
    console.log(`  • 订单ID: ${result.orderId || 'N/A'}`);
    console.log(`  • Client OID: ${orderParams.clientOid}`);
}

async function getOrders(client, symbol) {
    console.log(`\n📋 **查询现货订单 (${symbol})**\n`);

    const result = await client.getOrders({ symbol, status: 'active' });

    if (result.error) {
        console.error('❌ 查询失败:', result.error);
        process.exit(1);
    }

    const orders = result.items || [];
    if (orders.length === 0) {
        console.log('  暂无活跃订单');
        return;
    }

    console.log(`  活跃订单数: ${orders.length}\n`);
    orders.forEach(order => {
        console.log(`  订单ID: ${order.id}`);
        console.log(`    • 交易对: ${order.symbol}`);
        console.log(`    • 方向: ${order.side === 'buy' ? '买入' : '卖出'}`);
        console.log(`    • 类型: ${order.type}`);
        console.log(`    • 价格: ${order.price}`);
        console.log(`    • 数量: ${order.size}`);
        console.log(`    • 状态: ${order.isActive ? '活跃' : '已完成'}\n`);
    });
}

async function cancelOrder(client, orderId) {
    if (!orderId) {
        console.error('❌ 请指定订单ID: --orderId xxx');
        process.exit(1);
    }
    console.log(`\n⚡ **取消现货订单 ${orderId}**\n`);

    const result = await client.cancelOrder(orderId);

    if (result.error) {
        console.error('❌ 取消失败:', result.error);
        process.exit(1);
    }
    console.log('✅ 订单已取消');
}

runSpot();
