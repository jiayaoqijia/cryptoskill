import { OneClickService } from '@defuse-protocol/one-click-sdk-typescript';
import { displayTokensByBlockchain } from './utils';

/**
 *  Step 1: Get Available Tokens
 *
 *  This endpoint doesn't require JWT authentication.
 *  It returns a list of all supported tokens across different blockchains.
 *
 *  API Response is in an array of available tokens in the following format:
 *   {
 *     "blockchain": "arbitrum",
 *     "symbol": "USDC",
 *     "assetId": "arb-0xaf88d065e77c8cc2239327c5edb3a432268e5831.omft.near",
 *     "contractAddress": "0xaf88d065e77c8cc2239327c5edb3a432268e5831"
 *   }
 *
 */

async function getAvailableTokens() {
  try {
    console.log('Fetching available tokens...');

    // Fetch supported tokens from 1-Click API `/tokens` endpoint
    const tokens = await OneClickService.getTokens();

    console.log(`Found ${tokens.length} available tokens:\n`);

    // Display tokens grouped by blockchain
    displayTokensByBlockchain(tokens);

    // Show example token format
    console.log(
      `\n\n Response format example: \n\n ${JSON.stringify(tokens[0], null, 2)} \n`,
    );

    return tokens;
  } catch (error) {
    console.error('Error fetching tokens:', error);
    throw error;
  }
}

getAvailableTokens().catch(console.error);
