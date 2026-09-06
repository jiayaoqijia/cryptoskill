// scripts/monitor.js
// Core logic to check for balance changes on a given wallet list using Public RPC.
// Author: with-philia

const axios = require('axios');

// Public RPC Endpoint (Free, no key required)
// Can be overridden by environment variable RPC_URL
const RPC_URL = process.env.RPC_URL || 'https://eth.public-rpc.com';

// Target Wallets (Example: Binance Hot Wallet, Foundation, etc.)
// Can be overridden by environment variable WALLET_ADDRESSES (comma-separated)
const DEFAULT_WALLETS = [
    '0xBE0eB53F46cd790Cd13851d5EfF43D12404d33E8', // Binance 7 (Known huge wallet)
    '0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B', // Vitalik Buterin (Vb 3)
];

const WALLET_ADDRESSES = process.env.WALLET_ADDRESSES 
    ? process.env.WALLET_ADDRESSES.split(',') 
    : DEFAULT_WALLETS;

const BALANCE_THRESHOLD_ETH = process.env.BALANCE_THRESHOLD_ETH 
    ? parseFloat(process.env.BALANCE_THRESHOLD_ETH) 
    : 100; // Reporting threshold

async function checkWallets() {
    console.log(`🐳 Starting Wallet Monitor (RPC: ${RPC_URL})...`);
    console.log(`Monitoring ${WALLET_ADDRESSES.length} wallets with threshold > ${BALANCE_THRESHOLD_ETH} ETH`);

    for (const address of WALLET_ADDRESSES) {
        try {
            // RPC Payload: eth_getBalance
            const payload = {
                jsonrpc: "2.0",
                method: "eth_getBalance",
                params: [address.trim(), "latest"],
                id: 1
            };

            const response = await axios.post(RPC_URL, payload);
            
            if (response.data && response.data.result) {
                const hexBalance = response.data.result;
                // Convert Hex to BigInt then to Number (ETH)
                const balanceWei = BigInt(hexBalance);
                const balanceEth = Number(balanceWei) / 10**18;

                console.log(`Checking ${address.trim()}...`);
                console.log(`Balance: ${balanceEth.toFixed(4)} ETH`);

                if (balanceEth > BALANCE_THRESHOLD_ETH) {
                    console.log(`🚨 ALERT: Wallet holds > ${BALANCE_THRESHOLD_ETH} ETH`);
                }
            } else {
                console.log(`No data for ${address.trim()} (Response: ${JSON.stringify(response.data)})`);
            }

        } catch (error) {
            console.error(`Error checking wallet ${address.trim()}:`, error.message);
        }
    }
    console.log("✅ Monitor run complete.");
}

// Execute
checkWallets();
