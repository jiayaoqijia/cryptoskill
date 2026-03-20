const { KuCoinClient, getConfig } = require('../lib/kucoin-client');

const ACCOUNT_TYPE_LABELS = {
    'trade': '🎯 **现货账户 (Spot Trading)**',
    'main': '💰 **资金账户 (Funding / Main)**',
    'margin': '📈 **全仓杠杆账户 (Cross Margin)**',
    'isolated': '📊 **逐仓杠杆账户 (Isolated Margin)**',
    'futures': '⚡ **合约账户 (Futures)**'
};

async function runAccountCheck() {
    try {
        const client = new KuCoinClient(getConfig());

        console.log('\n📊 **KuCoin (KC) 账户资产概览**\n');

        const spotData = await fetchSpotAccounts(client);
        await displaySpotAccounts(client, spotData);

        const marginData = await fetchMarginAccounts(client);
        await displayMarginAccounts(client, marginData);

        const isolatedData = await fetchIsolatedMarginAccounts(client);
        await displayIsolatedMarginAccounts(client, isolatedData);

        const futuresData = await fetchFuturesAccounts(client);
        await displayFuturesAccounts(client, futuresData);

        printTimestamp();
    } catch (error) {
        console.error('Error:', error.message);
    }
}

async function fetchSpotAccounts(client) {
    const data = await client.getAccounts();
    if (data.error) {
        console.error('Error fetching accounts:', data.error);
        return {};
    }

    const accountsByType = {};
    data.forEach(acc => {
        if (!accountsByType[acc.type]) {
            accountsByType[acc.type] = [];
        }
        accountsByType[acc.type].push(acc);
    });
    return accountsByType;
}

async function fetchMarginAccounts(client) {
    try {
        const data = await client.getMarginAccount();
        return data;
    } catch (e) {
        return null;
    }
}

async function fetchIsolatedMarginAccounts(client) {
    try {
        const data = await client.getIsolatedMarginAccount();
        return data;
    } catch (e) {
        return null;
    }
}

async function displayMarginAccounts(client, marginData) {
    if (!marginData || marginData.error) return;
    if (!marginData.accounts || marginData.accounts.length === 0) return;

    console.log('📈 **全仓杠杆账户 (Cross Margin)**\n');
    
    const totalAsset = parseFloat(marginData.totalAssetOfQuoteCurrency || 0);
    const totalLiability = parseFloat(marginData.totalLiabilityOfQuoteCurrency || 0);
    const debtRatio = parseFloat(marginData.debtRatio || 0) * 100;
    
    console.log(`  总资产(折合): ${totalAsset.toFixed(2)} USDT`);
    console.log(`  总负债: ${totalLiability.toFixed(2)} USDT`);
    console.log(`  负债率: ${debtRatio.toFixed(2)}%`);

    const activeAccounts = marginData.accounts.filter(acc => 
        parseFloat(acc.total) > 0 || parseFloat(acc.liability) > 0
    );
    
    if (activeAccounts.length === 0) {
        console.log('  暂无资产\n');
        return;
    }

    console.log(`\n  有资产的币种 (${activeAccounts.length} 个):`);
    activeAccounts.forEach(acc => {
        console.log(`    ${acc.currency}: 总额=${parseFloat(acc.total).toFixed(8)}, 可用=${parseFloat(acc.available).toFixed(8)}, 负债=${parseFloat(acc.liability).toFixed(8)}`);
    });
    console.log('');
}

async function displayIsolatedMarginAccounts(client, isolatedData) {
    if (!isolatedData || isolatedData.error) return;
    if (!isolatedData.assets || isolatedData.assets.length === 0) return;

    console.log('📊 **逐仓杠杆账户 (Isolated Margin)**\n');
    
    const totalAsset = parseFloat(isolatedData.totalAssetOfQuoteCurrency || 0);
    const totalLiability = parseFloat(isolatedData.totalLiabilityOfQuoteCurrency || 0);
    
    console.log(`  总资产(折合): ${totalAsset.toFixed(2)} USDT`);
    console.log(`  总负债: ${totalLiability.toFixed(6)} USDT`);

    const activeAssets = isolatedData.assets.filter(a => 
        parseFloat(a.baseAsset.total) > 0 || 
        parseFloat(a.quoteAsset.total) > 0 || 
        parseFloat(a.baseAsset.liability) > 0 || 
        parseFloat(a.quoteAsset.liability) > 0
    );
    
    if (activeAssets.length === 0) {
        console.log('  暂无资产\n');
        return;
    }

    console.log(`\n  有资产的仓位 (${activeAssets.length} 个):`);
    activeAssets.forEach(asset => {
        console.log(`    ${asset.symbol} [${asset.status}]:`);
        console.log(`      ${asset.baseAsset.currency}: 总额=${parseFloat(asset.baseAsset.total).toFixed(8)}, 可用=${parseFloat(asset.baseAsset.available).toFixed(8)}, 负债=${parseFloat(asset.baseAsset.liability).toFixed(8)}`);
        console.log(`      ${asset.quoteAsset.currency}: 总额=${parseFloat(asset.quoteAsset.total).toFixed(8)}, 可用=${parseFloat(asset.quoteAsset.available).toFixed(8)}, 负债=${parseFloat(asset.quoteAsset.liability).toFixed(8)}`);
    });
    console.log('');
}

async function displaySpotAccounts(client, accountsByType) {
    const allCurrencies = new Set();
    for (const accounts of Object.values(accountsByType)) {
        accounts.forEach(acc => {
            if (parseFloat(acc.balance) > 0) {
                allCurrencies.add(acc.currency);
            }
        });
    }
    const prices = await client.getPrices([...allCurrencies]);

    // 始终显示所有账户类型，包括空账户
    const accountTypes = ['main', 'trade', 'margin', 'isolated', 'futures'];
    
    for (const type of accountTypes) {
        if (type === 'margin') continue; // margin 单独处理
        
        const accounts = accountsByType[type] || [];
        const label = ACCOUNT_TYPE_LABELS[type] || `**${type}**`;
        console.log(`${label}`);

        let totalUsdt = 0;
        let hasAssets = false;
        
        accounts.forEach(acc => {
            const balance = parseFloat(acc.balance);
            if (balance > 0) {
                hasAssets = true;
                const currency = acc.currency;
                const price = prices[currency] || 0;
                const usdtValue = balance * price;
                totalUsdt += usdtValue;
                const hold = acc.hold ? parseFloat(acc.hold).toFixed(8) : '0';
                console.log(`  • ${currency}: ${balance.toFixed(8)} (≈${usdtValue.toFixed(2)} USDT), 可用=${parseFloat(acc.available).toFixed(8)}, 冻结=${hold}`);
            }
        });
        
        if (!hasAssets) {
            console.log('  (无资产)');
        }
        
        if (totalUsdt > 0) {
            console.log(`  **合计: ${totalUsdt.toFixed(2)} USDT**`);
        }
        console.log('');
    }
}

async function fetchFuturesAccounts(client) {
    return await client.getAllFuturesAccounts();
}

async function displayFuturesAccounts(client, data) {
    if (data.error) return;

    const allCurrencies = [];
    if (data.usdtM) data.usdtM.forEach(acc => allCurrencies.push(acc.currency));
    if (data.coinM) data.coinM.forEach(acc => allCurrencies.push(acc.currency));
    const prices = await client.getPrices(allCurrencies);

    console.log('⚡ **合约账户 (USD本位)**');
    if (data.usdtM && data.usdtM.length > 0) {
        let totalUsdt = 0;
        data.usdtM.forEach(acc => {
            const total = parseFloat(acc.totalBalance || acc.accountEquity || acc.marginBalance || 0);
            const available = parseFloat(acc.availableBalance || 0);
            const unrealised = parseFloat(acc.unrealisedPL || acc.unrealisedPNL || 0);
            const currency = acc.currency;
            const price = prices[currency] || 1;
            const usdtValue = total * price;
            totalUsdt += usdtValue;
            console.log(`  • ${currency}: ${available.toFixed(8)} (≈${usdtValue.toFixed(2)} USDT), 未实现盈亏: ${unrealised.toFixed(8)}`);
        });
        console.log(`  **合计: ${totalUsdt.toFixed(2)} USDT**`);
    } else {
        console.log('  (无USD本位资产)');
    }

    console.log('\n🪙 **合约账户 (币本位)**');
    if (data.coinM && data.coinM.length > 0) {
        let totalUsdt = 0;
        data.coinM.forEach(acc => {
            const total = parseFloat(acc.totalBalance || acc.accountEquity || acc.marginBalance || 0);
            const available = parseFloat(acc.availableBalance || 0);
            const unrealised = parseFloat(acc.unrealisedPL || acc.unrealisedPNL || 0);
            const currency = acc.currency;
            const price = prices[currency] || 0;
            const usdtValue = total * price;
            totalUsdt += usdtValue;
            console.log(`  • ${currency}: ${available.toFixed(8)} (≈${usdtValue.toFixed(2)} USDT), 未实现盈亏: ${unrealised.toFixed(8)}`);
        });
        console.log(`  **合计: ${totalUsdt.toFixed(2)} USDT**`);
    } else {
        console.log('  (无币本位资产)');
    }
}

function printTimestamp() {
    const now = new Date();
    console.log(`*(${now.toISOString().replace('T', ' ').slice(0, 19)}) - KuCoin (KC) Trader 自动生成*`);
}

runAccountCheck();
