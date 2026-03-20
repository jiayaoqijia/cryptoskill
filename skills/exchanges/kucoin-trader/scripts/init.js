const fs = require('fs');
const path = require('path');

const homeDir = process.env.HOME || process.env.USERPROFILE;
const configDir = path.join(homeDir, '.openclaw/credentials');

if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
}

const configPath = path.join(configDir, 'kucoin.json');

console.log('\n🚀 **KuCoin Trader 初始化**\n');
console.log(`配置文件位置: ${configPath}\n');

console.log('请手动创建配置文件，内容如下:');
console.log('');
console.log('{');
console.log('  "apiKey": "your_api_key",');
console.log('  "secretKey": "your_secret_key",');
console.log('  "passphrase": "your_passphrase",');
console.log('  "isSandbox": false');
console.log('}');
console.log('');

if (fs.existsSync(configPath)) {
    console.log('✅ 配置文件已存在');
} else {
    console.log('⚠️ 配置文件不存在，请创建');
}
