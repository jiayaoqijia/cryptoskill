import { ApiError } from '@defuse-protocol/one-click-sdk-typescript';
import { getQuote } from './2-get-quote';
import { sendTokens } from './3-send-deposit';
import { submitTxHash } from './4-submit-tx-hash-OPTIONAL';
import { pollStatusUntilSuccess } from './5-check-status-OPTIONAL';
import { displaySwapCostTable } from './utils';
import { NEAR } from '@near-js/tokens';
import 'dotenv/config';

/**
 *  Step 5: Full Swap Implementation
 *
 *  This combines steps 2 - 5:
 *   1. Get a quote with deposit address
 *   2. Send deposit to the quote's deposit address
 *   3. Submit transaction hash to 1-Click API
 *   4. Check the status of the swap
 *
 *  NOTE: Configure this file independently of the other files in this directory
 */

// Example Swap Configuration
const isTest = false; // keep set to false for actual execution
const senderAddress = process.env.SENDER_NEAR_ACCOUNT as string;
const senderPrivateKey = process.env.SENDER_PRIVATE_KEY as string;
const recipientAddress = '0x553e771500f2d7529079918F93d86C0a845B540b'; // Token swap recipient address on Arbitrum
const originAsset = 'nep141:wrap.near'; // Native $NEAR
const destinationAsset =
  'nep141:arb-0x912ce59144191c1204e64559fe8253a0e49e6548.omft.near'; // Native $ARB
const amount = NEAR.toUnits('0.01').toString(); // amount in smallest unit of the input or output token depending on `swapType`

async function fullSwap() {
  try {
    console.log('Starting NEAR Intents full swap process w/ 1-Click API...\n');

    // Step 1: Get quote and extract deposit address
    console.log('Step 1: Getting quote...');
    console.log('--------------------------------');
    const quote = await getQuote(
      isTest,
      senderAddress,
      recipientAddress,
      originAsset,
      destinationAsset,
      amount,
    );

    // Extract deposit address from quote response
    const depositAddress = quote.quote?.depositAddress;
    if (!depositAddress) {
      throw new Error('No deposit address found in quote response');
    }

    console.log(
      `💬 - Quote: ${quote.quote?.amountInFormatted} NEAR → ${quote.quote?.amountOutFormatted} ARB`,
    );
    console.log(`🎯 - Deposit address: ${depositAddress}`);

    // Display swap cost breakdown table
    displaySwapCostTable(quote);

    // Step 2: Send deposit
    console.log('Step 2: Sending deposit...');
    console.log('--------------------------------');
    const depositResult = await sendTokens(
      senderAddress,
      senderPrivateKey,
      depositAddress,
      amount,
    );
    console.log('✅ - Deposit sent successfully!');
    console.log(
      `🔍 - See transaction: https://nearblocks.io/txns/${depositResult.transaction.hash}\n`,
    );

    // Step 3: Submit transaction hash
    console.log('Step 3: Submitting transaction hash...');
    console.log('--------------------------------');
    const submitResult = await submitTxHash(
      depositResult.transaction.hash,
      depositAddress,
    );
    console.log('✅ - Transaction hash submitted successfully!\n');

    // Step 4: Poll status until success
    console.log('Step 4: Monitoring swap status...');
    console.log('--------------------------------');
    console.log('⏳ Waiting 5 seconds before starting status checks...');
    await new Promise((resolve) => setTimeout(resolve, 5000));

    const finalStatus = await pollStatusUntilSuccess(depositAddress);
    console.log('--------------------------------');
    console.log('✅ Full swap process completed! \n\n');
    console.log(
      `🔍 View full transaction on NEAR Intents Explorer: \n https://explorer.near-intents.org/transactions/${depositAddress} \n`,
    );

    return { quote, depositAddress, depositResult, submitResult, finalStatus };
  } catch (error) {
    console.error('❌ Full swap failed:', error as ApiError);
    throw error;
  }
}

fullSwap().catch(console.error);
