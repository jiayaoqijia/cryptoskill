import {
  OpenAPI,
  OneClickService,
} from '@defuse-protocol/one-click-sdk-typescript';
import 'dotenv/config';

/**
 *  Step 6: Submit Transaction Hash (Optional)
 *
 *  This endpoint submits a transaction hash and deposit address to the 1-Click API
 *  as an early notification to speed up the process.
 *
 */

// Initialize the API client
OpenAPI.BASE = 'https://1click.chaindefuser.com';

// Configure your JSON Web Token (JWT) required for most endpoints
// Request one here -> https://docs.google.com/forms/d/e/1FAIpQLSdrSrqSkKOMb_a8XhwF0f7N5xZ0Y5CYgyzxiAuoC2g4a2N68g/viewform
// If you don't have a JWT, you can comment out line 18 but you will pay a 0.1% fee on all swaps
OpenAPI.TOKEN = process.env.ONE_CLICK_JWT;

const txHash = '0x123abc456def789';
const depositAddress = '0x2527D02599Ba641c19FEa793cD0F167589a0f10D';

export async function submitTxHash(txHash: string, depositAddress: string) {
  try {
    console.log(`Transaction Hash: ${txHash}`);
    console.log(`Deposit Address: ${depositAddress}`);

    // Make the API call to submit the transaction hash
    await OneClickService.submitDepositTx({
      txHash,
      depositAddress,
    });
  } catch (error) {
    console.error('Error submitting transaction hash:', error);
    throw error;
  }
}

// Only run if this file is executed directly
if (require.main === module) {
  submitTxHash(txHash, depositAddress)
    .then((result) => console.log('\n\nSubmit tx hash RESPONSE:', result))
    .catch(console.error);
}
