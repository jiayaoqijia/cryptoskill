import { getAccount } from './near';
import { NEAR } from '@near-js/tokens';
import 'dotenv/config';

/**
 *  Step 3: Send Deposit to Quote Address
 *
 *  This process sends $NEAR tokens to the `depositAddress`
 *
 *  It's important to note that although this example uses $NEAR, you can send any token on any
 *  supported network by the 1-Click API. No NEAR account is required to use 1Click API.
 *
 *  For example, if you use $ARB `assetId` as the `originAsset` in the quote, you will get an $ARB `depositAddress`
 *  in the quote response. You can then send $ARB to this `depositAddress` on Arbitrum to execute the swap.
 *
 */

// Configure token deposit
const senderAccount = process.env.SENDER_NEAR_ACCOUNT as string;
const senderPrivateKey = process.env.SENDER_PRIVATE_KEY as string;
const depositAmount = NEAR.toUnits('0.001').toString();
export const depositAddress =
  '84e2dc2b3a7d866c6e8fead3dfd296bc9e6abcf8eeec295e8c29b099bf21fbc7'; // deposit address from getQuote

export async function sendTokens(
  senderAccount: string,
  senderPrivateKey: string,
  depositAddress: string,
  depositAmount: string,
) {
  try {
    const account = await getAccount(senderAccount, senderPrivateKey);
    const result = await account.transfer({
      token: NEAR,
      amount: depositAmount,
      receiverId: depositAddress as string,
    });

    return result;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

// Only run if this file is executed directly
if (require.main === module) {
  sendTokens(senderAccount, senderPrivateKey, depositAddress, depositAmount)
    .then((result) =>
      console.log(
        `\nDeposit sent! \n See transaction: https://nearblocks.io/txns/${result.transaction.hash}`,
      ),
    )
    .catch(console.error);
}
