#!/usr/bin/env bash
# Buy token with configurable slippage and optional dynamic retry.
# Run from universal-account-example directory.
#
# Example:
#   bash {baseDir}/scripts/buy-with-slippage.sh \
#     --chain bsc \
#     --token-address 0x0000000000000000000000000000000000000000 \
#     --amount-usd 5 \
#     --slippage-bps 300 \
#     --dynamic-slippage \
#     --retry-slippages 300,500,800,1200 \
#     --solana-mev-tip-amount 0.003 \
#     --retry-mev-tips 0.001,0.003,0.005

set -euo pipefail

CHAIN_INPUT=""
TOKEN_ADDRESS=""
AMOUNT_USD=""
SLIPPAGE_BPS=100
DYNAMIC_SLIPPAGE=0
RETRY_SLIPPAGES=""
UNIVERSAL_GAS="true"
POLL_ATTEMPTS=30
POLL_INTERVAL_SEC=2
SOLANA_MEV_TIP_AMOUNT=0.001
RETRY_MEV_TIPS="0.001,0.003,0.005"

print_usage() {
    echo "Usage:"
    echo "  ./buy-with-slippage.sh --chain <bsc|arbitrum|polygon|optimism|ethereum|solana|chainId>"
    echo "    --token-address <0x...> --amount-usd <amount>"
    echo "    [--slippage-bps 100]"
    echo "    [--dynamic-slippage]"
    echo "    [--retry-slippages 100,300,500,800,1200]"
    echo "    [--solana-mev-tip-amount 0.001]"
    echo "    [--retry-mev-tips 0.001,0.003,0.005]"
    echo "    [--universal-gas true|false]"
    echo "    [--poll-attempts 30]"
    echo "    [--poll-interval-sec 2]"
}

while [ "$#" -gt 0 ]; do
    case "$1" in
        --chain)
            shift
            CHAIN_INPUT="${1:-}"
            shift || true
            ;;
        --token-address)
            shift
            TOKEN_ADDRESS="${1:-}"
            shift || true
            ;;
        --amount-usd)
            shift
            AMOUNT_USD="${1:-}"
            shift || true
            ;;
        --slippage-bps)
            shift
            SLIPPAGE_BPS="${1:-}"
            shift || true
            ;;
        --dynamic-slippage)
            DYNAMIC_SLIPPAGE=1
            shift
            ;;
        --retry-slippages)
            shift
            RETRY_SLIPPAGES="${1:-}"
            shift || true
            ;;
        --solana-mev-tip-amount)
            shift
            SOLANA_MEV_TIP_AMOUNT="${1:-}"
            shift || true
            ;;
        --retry-mev-tips)
            shift
            RETRY_MEV_TIPS="${1:-}"
            shift || true
            ;;
        --universal-gas)
            shift
            UNIVERSAL_GAS="${1:-}"
            shift || true
            ;;
        --poll-attempts)
            shift
            POLL_ATTEMPTS="${1:-}"
            shift || true
            ;;
        --poll-interval-sec)
            shift
            POLL_INTERVAL_SEC="${1:-}"
            shift || true
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        *)
            echo "Unknown argument: $1"
            print_usage
            exit 1
            ;;
    esac
done

if [ -z "$CHAIN_INPUT" ] || [ -z "$TOKEN_ADDRESS" ] || [ -z "$AMOUNT_USD" ]; then
    print_usage
    exit 1
fi

if [ ! -f package.json ]; then
    echo "package.json not found. Run this script from universal-account-example."
    exit 1
fi

if [ ! -f .env ]; then
    echo ".env not found. Initialize wallet first."
    exit 1
fi

if ! [[ "$SLIPPAGE_BPS" =~ ^[0-9]+$ ]] || [ "$SLIPPAGE_BPS" -le 0 ] || [ "$SLIPPAGE_BPS" -gt 10000 ]; then
    echo "--slippage-bps must be an integer between 1 and 10000."
    exit 1
fi

if ! [[ "$POLL_ATTEMPTS" =~ ^[0-9]+$ ]] || [ "$POLL_ATTEMPTS" -le 0 ]; then
    echo "--poll-attempts must be a positive integer."
    exit 1
fi

if ! [[ "$POLL_INTERVAL_SEC" =~ ^[0-9]+$ ]] || [ "$POLL_INTERVAL_SEC" -le 0 ]; then
    echo "--poll-interval-sec must be a positive integer."
    exit 1
fi

CHAIN_INPUT="$CHAIN_INPUT" \
TOKEN_ADDRESS="$TOKEN_ADDRESS" \
AMOUNT_USD="$AMOUNT_USD" \
SLIPPAGE_BPS="$SLIPPAGE_BPS" \
DYNAMIC_SLIPPAGE="$DYNAMIC_SLIPPAGE" \
RETRY_SLIPPAGES="$RETRY_SLIPPAGES" \
SOLANA_MEV_TIP_AMOUNT="$SOLANA_MEV_TIP_AMOUNT" \
RETRY_MEV_TIPS="$RETRY_MEV_TIPS" \
UNIVERSAL_GAS="$UNIVERSAL_GAS" \
POLL_ATTEMPTS="$POLL_ATTEMPTS" \
POLL_INTERVAL_SEC="$POLL_INTERVAL_SEC" \
node - <<'__NODE__'
const { config } = require('dotenv');
const { Wallet, getBytes, formatUnits } = require('ethers');
const {
  CHAIN_ID,
  UA_TRANSACTION_STATUS,
  UniversalAccount,
} = require('@particle-network/universal-account-sdk');

config();

function parsePositiveInt(value, name, max = Number.MAX_SAFE_INTEGER) {
  const n = Number(value);
  if (!Number.isInteger(n) || n <= 0 || n > max) {
    throw new Error(`${name} must be an integer in range 1..${max}`);
  }
  return n;
}

function parseBoolean(value, name) {
  const v = String(value).toLowerCase();
  if (v === 'true') return true;
  if (v === 'false') return false;
  throw new Error(`${name} must be true or false`);
}

function parseNonNegativeNumber(value, name) {
  const n = Number(value);
  if (!Number.isFinite(n) || n < 0) {
    throw new Error(`${name} must be a non-negative number`);
  }
  return n;
}

function resolveChainId(input) {
  const raw = String(input || '').trim();
  if (/^[0-9]+$/.test(raw)) return Number(raw);

  const map = {
    solana: CHAIN_ID.SOLANA_MAINNET,
    ethereum: CHAIN_ID.ETHEREUM_MAINNET,
    eth: CHAIN_ID.ETHEREUM_MAINNET,
    bsc: CHAIN_ID.BSC_MAINNET,
    binance: CHAIN_ID.BSC_MAINNET,
    arbitrum: CHAIN_ID.ARBITRUM_MAINNET_ONE,
    arb: CHAIN_ID.ARBITRUM_MAINNET_ONE,
    optimism: CHAIN_ID.OPTIMISM_MAINNET,
    op: CHAIN_ID.OPTIMISM_MAINNET,
    polygon: CHAIN_ID.POLYGON_MAINNET,
    matic: CHAIN_ID.POLYGON_MAINNET,
  };

  const chainId = map[raw.toLowerCase()];
  if (!chainId) {
    throw new Error(`Unsupported chain: ${raw}`);
  }
  return chainId;
}

function buildSlippagePlan(base, dynamicEnabled, retrySlippages) {
  if (!dynamicEnabled) return [base];

  const parsed = (retrySlippages || '')
    .split(',')
    .map((x) => x.trim())
    .filter(Boolean)
    .map((x) => parsePositiveInt(x, 'retry slippage', 10000));

  const fallback = [base, 300, 500, 800, 1200, 1500];
  const source = parsed.length > 0 ? parsed : fallback;

  const dedup = [];
  const set = new Set();
  for (const bps of [base, ...source]) {
    if (!set.has(bps)) {
      set.add(bps);
      dedup.push(bps);
    }
  }
  return dedup;
}

function buildMevTipPlan(baseTip, retryMevTips) {
  const parsed = (retryMevTips || '')
    .split(',')
    .map((x) => x.trim())
    .filter(Boolean)
    .map((x) => parseNonNegativeNumber(x, 'retry mev tip'));

  const dedup = [];
  const set = new Set();
  for (const tip of [baseTip, ...parsed]) {
    const key = Number(tip).toString();
    if (!set.has(key)) {
      set.add(key);
      dedup.push(tip);
    }
  }
  return dedup;
}

function isSolanaChain(chainId) {
  return chainId === CHAIN_ID.SOLANA_MAINNET;
}

function isSuccessStatus(status) {
  return status === UA_TRANSACTION_STATUS?.FINISHED || status === 7;
}

function isFailureStatus(status) {
  return status === UA_TRANSACTION_STATUS?.FAILED || status === 11;
}

function formatFee(weiLikeHex) {
  try {
    return `$${formatUnits(weiLikeHex, 18)}`;
  } catch {
    return String(weiLikeHex);
  }
}

async function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function pollFinalStatus(ua, transactionId, maxAttempts, intervalSec) {
  for (let i = 1; i <= maxAttempts; i++) {
    const tx = await ua.getTransaction(transactionId);
    const status = tx?.status;
    console.log(`poll ${i}/${maxAttempts}: status=${status}`);

    if (isSuccessStatus(status)) return { final: 'SUCCESS', tx };
    if (isFailureStatus(status)) return { final: 'FAILED', tx };

    if (i < maxAttempts) await sleep(intervalSec * 1000);
  }
  return { final: 'PENDING', tx: null };
}

async function main() {
  const chainId = resolveChainId(process.env.CHAIN_INPUT);
  const tokenAddress = String(process.env.TOKEN_ADDRESS || '').trim();
  const amountInUSD = String(process.env.AMOUNT_USD || '').trim();
  const baseSlippage = parsePositiveInt(process.env.SLIPPAGE_BPS, 'slippage bps', 10000);
  const dynamicSlippage = String(process.env.DYNAMIC_SLIPPAGE || '0') === '1';
  const retrySlippages = process.env.RETRY_SLIPPAGES || '';
  const solanaMevTipAmount = parseNonNegativeNumber(
    process.env.SOLANA_MEV_TIP_AMOUNT || '0',
    'solana mev tip amount',
  );
  const retryMevTips = process.env.RETRY_MEV_TIPS || '';
  const universalGas = parseBoolean(process.env.UNIVERSAL_GAS, 'universal gas');
  const pollAttempts = parsePositiveInt(process.env.POLL_ATTEMPTS, 'poll attempts');
  const pollIntervalSec = parsePositiveInt(process.env.POLL_INTERVAL_SEC, 'poll interval');

  const privateKey = process.env.PRIVATE_KEY || '';
  const projectId = process.env.PROJECT_ID || '';
  const projectClientKey = process.env.PROJECT_CLIENT_KEY || '';
  const projectAppUuid = process.env.PROJECT_APP_UUID || '';

  if (!/^0x[a-fA-F0-9]{64}$/.test(privateKey)) {
    throw new Error('PRIVATE_KEY is missing or invalid in .env');
  }
  if (!projectId || !projectClientKey || !projectAppUuid) {
    throw new Error('PROJECT_ID / PROJECT_CLIENT_KEY / PROJECT_APP_UUID missing in .env');
  }
  if (!tokenAddress) {
    throw new Error('token address is required');
  }
  if (!amountInUSD || Number(amountInUSD) <= 0) {
    throw new Error('amount-usd must be a positive number');
  }

  const wallet = new Wallet(privateKey);
  const slippagePlan = buildSlippagePlan(baseSlippage, dynamicSlippage, retrySlippages);
  const isSolana = isSolanaChain(chainId);
  const mevTipPlan = isSolana ? buildMevTipPlan(solanaMevTipAmount, retryMevTips) : [0];

  console.log('BUY_WITH_SLIPPAGE_START');
  console.log(`CHAIN_ID=${chainId}`);
  console.log(`TOKEN_ADDRESS=${tokenAddress}`);
  console.log(`AMOUNT_USD=${amountInUSD}`);
  console.log(`UNIVERSAL_GAS=${universalGas}`);
  console.log(`SLIPPAGE_PLAN=${slippagePlan.join(',')}`);
  if (isSolana) {
    console.log(`MEV_TIP_PLAN_SOL=${mevTipPlan.join(',')}`);
  } else if (retryMevTips || solanaMevTipAmount > 0) {
    console.log('MEV tip args provided but chain is not Solana, ignoring tip settings.');
  }

  let lastError = '';
  const totalAttempts = slippagePlan.length * mevTipPlan.length;
  let attemptIndex = 0;

  for (let i = 0; i < slippagePlan.length; i++) {
    const slippageBps = slippagePlan[i];
    for (let j = 0; j < mevTipPlan.length; j++) {
      const mevTip = mevTipPlan[j];
      attemptIndex += 1;
      console.log(
        `ATTEMPT=${attemptIndex}/${totalAttempts} SLIPPAGE_BPS=${slippageBps} SOLANA_MEV_TIP_AMOUNT=${mevTip}`,
      );

      try {
        const tradeConfig = {
          slippageBps,
          universalGas,
        };
        if (isSolana) {
          tradeConfig.solanaMEVTipAmount = mevTip;
        }

        const ua = new UniversalAccount({
          projectId,
          projectClientKey,
          projectAppUuid,
          ownerAddress: wallet.address,
          tradeConfig,
        });

        const transaction = await ua.createBuyTransaction({
          token: { chainId, address: tokenAddress },
          amountInUSD,
        });

        const feeQuote = transaction?.feeQuotes?.[0];
        const feeTotals = feeQuote?.fees?.totals;
        if (feeTotals) {
          console.log(`FEE_TOTAL_USD=${formatFee(feeTotals.feeTokenAmountInUSD)}`);
          console.log(`FEE_GAS_USD=${formatFee(feeTotals.gasFeeTokenAmountInUSD)}`);
          if (feeTotals.solanaMevTipFeeInUSD) {
            console.log(`FEE_SOLANA_MEV_TIP_USD=${formatFee(feeTotals.solanaMevTipFeeInUSD)}`);
          }
        }

        const sendResult = await ua.sendTransaction(
          transaction,
          wallet.signMessageSync(getBytes(transaction.rootHash)),
        );

        const txId = sendResult?.transactionId;
        if (!txId) {
          throw new Error('transactionId missing from sendTransaction result');
        }

        console.log(`TRANSACTION_ID=${txId}`);
        console.log(`EXPLORER_URL=https://universalx.app/activity/details?id=${txId}`);

        const polled = await pollFinalStatus(ua, txId, pollAttempts, pollIntervalSec);
        if (polled.final === 'SUCCESS') {
          console.log('FINAL_STATUS=SUCCESS');
          return;
        }

        if (polled.final === 'FAILED') {
          console.log('FINAL_STATUS=FAILED');
          lastError = `transaction failed at slippage ${slippageBps}, mevTip ${mevTip}`;
          if (attemptIndex < totalAttempts) {
            console.log('RETRY_NEXT_ATTEMPT=1');
            continue;
          }
          throw new Error(lastError);
        }

        console.log('FINAL_STATUS=PENDING');
        return;
      } catch (err) {
        lastError = err?.message || String(err);
        console.log(`ATTEMPT_ERROR=${lastError}`);
        if (attemptIndex < totalAttempts) {
          console.log('RETRY_NEXT_ATTEMPT=1');
          continue;
        }
      }
    }
  }

  throw new Error(lastError || 'buy failed after retries');
}

main().catch((err) => {
  console.error('BUY_WITH_SLIPPAGE_ERROR:', err.message || err);
  process.exit(1);
});
__NODE__
