
import { executeIntent } from '../index';
import * as dotenv from 'dotenv';
dotenv.config();

// Mock env vars for testing if not present
// Mock env vars for testing if not present
if (!process.env.NEAR_ACCOUNT_ID) {
    process.env.NEAR_ACCOUNT_ID = "justatestwallet1.near";
}
if (!process.env.NEAR_PRIVATE_KEY) {
    process.env.NEAR_PRIVATE_KEY = "ed25519:5ojctFUi161WBkBFinDit2ZTYC4ksekTeWT2oZVyCofHAzb6iTniuP13xq9voxhZCsRXfwpTwSHSiNJBBFAgW5zi";
}


async function runTest() {
    console.log("Testing Intent Execution on MAINNET...");
    
    // Test 1: Real Swap (Small amount)
    try {
        const result = await executeIntent({
            assetIn: "NEAR",
            assetOut: "base:USDC",
            amount: "0.3", // Fits in 0.36 balance, > 0.15 USDC value
            recipient: "0x30FE694284a082a5D1adfF6D25C0B9B6bF61F77D"
        });
        
        console.log("Result:", result);
    } catch (error) {
        console.error("Test Failed with Error:", error);
    }
}

runTest();
