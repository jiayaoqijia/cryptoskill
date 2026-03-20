const { KuCoinClient, getConfig } = require('../lib/kucoin-client');

function getLocalTimeStr() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

const args = process.argv.slice(2);
let params = {
    from: 'trade',
    to: 'main',
    currency: 'USDT',
    amount: '100'
};

for (let i = 0; i < args.length; i += 2) {
    const key = args[i]?.replace('--', '');
    const value = args[i + 1];
    if (key && value) {
        params[key] = value;
    }
}

// 将 symbol 转换为 toAccountTag/fromAccountTag，用于逐仓杠杆
if (params.symbol) {
    params.accountTag = params.symbol;
    delete params.symbol;
}

const typeLabels = {
    'trade': '现货账户 (TRADE)',
    'main': '资金账户 (MAIN)',
    'margin': '杠杆账户 (MARGIN)',
    'isolated': '逐仓杠杆 (ISOLATED)',
    'futures': '合约账户 (CONTRACT)'
};

const accountTypeMap = {
    'trade': 'TRADE',
    'main': 'MAIN',
    'margin': 'MARGIN',
    'isolated': 'ISOLATED',
    'futures': 'CONTRACT'
};

console.log(`\n🔄 **开始资产划转**`);
console.log(`  • 从: ${typeLabels[params.from] || params.from}`);
console.log(`  • 到: ${typeLabels[params.to] || params.to}`);
console.log(`  • 币种: ${params.currency.toUpperCase()}`);
console.log(`  • 金额: ${params.amount}\n`);

async function runTransfer() {
    try {
        const config = getConfig();
        if (!config) {
            console.error('❌ 错误: 找不到 KuCoin 授权信息');
            console.error('请创建配置文件: ~/.openclaw/credentials/kucoin.json 或设置环境变量');
            process.exit(1);
        }
        const client = new KuCoinClient(config);
        const clientOid = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

        const fromType = accountTypeMap[params.from] || params.from.toUpperCase();
        const toType = accountTypeMap[params.to] || params.to.toUpperCase();

        const transferParams = {
            clientOid: clientOid,
            type: 'INTERNAL',
            currency: params.currency.toUpperCase(),
            amount: params.amount,
            fromAccountType: fromType,
            toAccountType: toType
        };

        // 逐仓杠杆需要指定交易对，使用 toAccountTag 参数
        if (params.to === 'isolated' && params.accountTag) {
            transferParams.toAccountTag = params.accountTag.toUpperCase();
            console.log(`  • 交易对: ${transferParams.toAccountTag}`);
        } else if (params.to === 'isolated') {
            console.error('❌ 错误: 逐仓划转需要指定 --symbol 参数');
            process.exit(1);
        }

        // 从逐仓杠杆转出需要指定交易对，使用 fromAccountTag 参数
        if (params.from === 'isolated' && params.accountTag) {
            transferParams.fromAccountTag = params.accountTag.toUpperCase();
            console.log(`  • 交易对: ${transferParams.fromAccountTag}`);
        } else if (params.from === 'isolated') {
            console.error('❌ 错误: 从逐仓杠杆转出需要指定 --symbol 参数');
            process.exit(1);
        }

        console.log('⏳ 处理中...\n');
        const result = await client.universalTransfer(transferParams);

        if (result.error) {
            if (result.error.includes('permission')) {
                console.error('❌ 划转失败: API 权限不足');
                console.error('请在 KuCoin 后台修改 API 权限:');
                console.error('  1. 登录 KuCoin → API 管理');
                console.error('  2. 编辑你的 API');
                console.error('  3. 勾选"Flex Transfer"或"Universal Transfer"权限');
                console.error('  4. 保存并重新尝试');
            } else {
                console.error('❌ 划转失败:', result.error);
            }
            process.exit(1);
        }

        console.log('✅ **划转成功**');
        console.log(`  • 转账ID: ${result.orderId || result.applyId || 'N/A'}`);
        console.log(`  • Client OID: ${clientOid}`);
    } catch (error) {
        console.error('❌ 错误:', error.message);
        process.exit(1);
    }
}

runTransfer();
