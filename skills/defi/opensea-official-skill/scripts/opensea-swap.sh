#!/usr/bin/env bash
set -euo pipefail

# Swap tokens via OpenSea MCP
# Usage: PRIVATE_KEY=0xYourKey ./opensea-swap.sh <to_token_address> <amount> <wallet_address> [chain] [from_token]
#
# Example:
#   PRIVATE_KEY=0xYourKey ./opensea-swap.sh 0xb695559b26bb2c9703ef1935c37aeae9526bab07 0.02 0xYourWallet base
#   PRIVATE_KEY=0xYourKey ./opensea-swap.sh 0xToToken 100 0xYourWallet base 0xFromToken
#
# Requires: OPENSEA_API_KEY env var, PRIVATE_KEY env var, mcporter, node with viem, jq

TO_TOKEN="${1:?Usage: PRIVATE_KEY=0x... $0 <to_token_address> <amount> <wallet_address> [chain] [from_token]}"
AMOUNT="${2:?Amount required}"
WALLET="${3:?Wallet address required}"
CHAIN="${4:-base}"
FROM_TOKEN="${5:-0x0000000000000000000000000000000000000000}"

ALLOWED_CHAINS="base ethereum mainnet polygon matic arbitrum optimism"
if ! echo " $ALLOWED_CHAINS " | grep -qF " $CHAIN "; then
  echo "Invalid chain '${CHAIN}'. Allowed: ${ALLOWED_CHAINS}" >&2
  exit 1
fi

if [ -z "${PRIVATE_KEY:-}" ]; then
  echo "PRIVATE_KEY environment variable is required" >&2
  exit 1
fi

tmp_quote=$(mktemp)
chmod 600 "$tmp_quote"
trap 'rm -f "$tmp_quote"' EXIT

echo "Getting swap quote: ${AMOUNT} tokens on ${CHAIN}..." >&2

if ! QUOTE=$(mcporter call opensea.get_token_swap_quote --args "{
  \"fromContractAddress\": \"${FROM_TOKEN}\",
  \"fromChain\": \"${CHAIN}\",
  \"toContractAddress\": \"${TO_TOKEN}\",
  \"toChain\": \"${CHAIN}\",
  \"fromQuantity\": \"${AMOUNT}\",
  \"address\": \"${WALLET}\"
}" --output raw 2>&1); then
  echo "mcporter failed: $QUOTE" >&2
  exit 1
fi

if ! echo "$QUOTE" | jq empty 2>/dev/null; then
  echo "Invalid response (not JSON): $QUOTE" >&2
  exit 1
fi

if echo "$QUOTE" | jq -e '.error // .isError // empty' >/dev/null 2>&1; then
  echo "Failed to get quote: $QUOTE" >&2
  exit 1
fi

echo "$QUOTE" > "$tmp_quote"

node --input-type=module -e "
import { createPublicClient, createWalletClient, http } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { base, mainnet, polygon, arbitrum, optimism } from 'viem/chains';
import { readFileSync } from 'fs';

const chains = { base, ethereum: mainnet, mainnet, matic: polygon, polygon, arbitrum, optimism };
const chain = chains['${CHAIN}'] || base;

const account = privateKeyToAccount(process.env.PRIVATE_KEY);
const wallet = createWalletClient({ account, chain, transport: http() });
const pub = createPublicClient({ chain, transport: http() });

const raw = readFileSync('$tmp_quote', 'utf8');
let quote;
try {
  const wrapper = JSON.parse(raw);
  quote = JSON.parse(wrapper.content[0].text);
} catch (e) {
  quote = JSON.parse(raw);
}

if (!quote.swap?.actions?.[0]?.transactionSubmissionData) {
  console.error('ERROR: Quote response missing swap.actions[0].transactionSubmissionData');
  process.exit(1);
}
const txData = quote.swap.actions[0].transactionSubmissionData;
if (!txData.to || !txData.data || txData.value === undefined) {
  console.error('ERROR: transactionSubmissionData missing required fields (to, data, value)');
  process.exit(1);
}

const ethAddrRegex = /^0x[0-9a-fA-F]{40}$/;
if (!ethAddrRegex.test(txData.to)) {
  console.error('ERROR: Invalid destination address:', txData.to);
  process.exit(1);
}

const valueBigInt = (() => { try { return BigInt(txData.value); } catch { return null; } })();
if (valueBigInt === null || valueBigInt < 0n) {
  console.error('ERROR: Invalid transaction value (not a non-negative integer):', txData.value);
  process.exit(1);
}

const toSymbol = quote.swapQuote.swapRoutes[0].toAsset.symbol;

console.error('Quote received — To:', txData.to, 'Value:', txData.value, 'wei', 'Token:', toSymbol);
console.error('Sending transaction...');

const hash = await wallet.sendTransaction({
  to: txData.to,
  data: txData.data,
  value: BigInt(txData.value)
});

const explorerUrl = chain.blockExplorers?.default?.url || 'https://basescan.org';
console.error('TX: ' + explorerUrl + '/tx/' + hash);
console.error('Waiting for confirmation...');

const receipt = await pub.waitForTransactionReceipt({ hash });
console.error(receipt.status === 'success' ? 'Swap complete!' : 'Swap failed');
console.error('Gas used:', receipt.gasUsed.toString());

if (receipt.status !== 'success') process.exit(1);
"
