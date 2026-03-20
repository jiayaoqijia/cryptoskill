const { KuCoinClient, getConfig } = require('../lib/kucoin-client');

async function queryAllOrders() {
    const client = new KuCoinClient(getConfig());

    console.log('\n📊 **查询KC账户委托订单**\n');
    console.log('='.repeat(50));

    let totalActive = 0;
    let totalHistory = 0;

    totalActive += await querySpotOrders(client);
    console.log('');
    console.log('='.repeat(50));

    totalActive += await queryMarginOrders(client);
    console.log('');
    console.log('='.repeat(50));

    totalActive += await queryFuturesOrders(client);

    console.log('\n' + '='.repeat(50));
    console.log(`📈 汇总: 共 ${totalActive} 单活跃委托`);
}

async function querySpotOrders(client) {
    console.log('\n📝 **现货 (Spot)**\n');

    try {
        const result = await client.getOrders({ status: 'active' });
        const orders = result.items || result.data || result;

        if (!orders || orders.length === 0) {
            console.log('  📭 无活跃委托');
            return 0;
        }

        console.log(`  ⏳ 活跃委托: ${orders.length} 单`);
        console.log('\n  委托明细:');
        orders.forEach(o => {
            console.log(`    ${o.symbol} - ${o.side === 'buy' ? '买入' : '卖出'} ${o.type} ${o.size} @ ${o.price || '市价'}`);
        });
        return orders.length;
    } catch (e) {
        console.log(`  查询失败: ${e.message}`);
        return 0;
    }
}

async function queryMarginOrders(client) {
    console.log('\n📈 **杠杆 (Margin)**\n');

    try {
        const result = await client.getOrders({ tradeType: 'MARGIN_TRADE', status: 'active' });
        const orders = result.items || result.data || result;

        if (!orders || orders.length === 0) {
            console.log('  📭 无活跃委托');
            console.log('  ⚠️  注意: UTA模式下杠杆活跃委托API存在限制，若有实际挂单请通过App或Web确认');
            return 0;
        }

        console.log(`  ⏳ 活跃委托: ${orders.length} 单`);
        console.log('\n  委托明细:');
        orders.forEach(order => {
            console.log(`    ${order.symbol} - ${order.side === 'buy' ? '买入' : '卖出'} ${order.type} ${order.size} @ ${order.price || '市价'}`);
        });
        return orders.length;
    } catch (e) {
        console.log(`  查询失败: ${e.message}`);
        return 0;
    }
}

async function queryFuturesOrders(client) {
    console.log('\n⚡ **合约 (Futures)**\n');

    try {
        const result = await client.getFuturesOrders({ status: 'active' });
        const orders = result.items || result.data || result;

        if (!orders || orders.length === 0) {
            console.log('  📭 无活跃委托');
            return 0;
        }

        console.log(`  ⏳ 活跃委托: ${orders.length} 单`);
        console.log('\n  委托明细:');
        orders.forEach(o => {
            console.log(`    ${o.symbol} - ${o.side === 'buy' ? '做多' : '做空'} ${o.type} ${o.size} @ ${o.price || '市价'}`);
        });
        return orders.length;
    } catch (e) {
        console.log(`  查询失败: ${e.message}`);
        return 0;
    }
}

queryAllOrders();
