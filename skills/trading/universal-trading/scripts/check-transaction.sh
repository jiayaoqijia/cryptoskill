#!/usr/bin/env bash
# Poll UniversalX transaction status until success/failure or timeout.
# Run from universal-account-example directory.
#
# Usage:
#   ./check-transaction.sh <TRANSACTION_ID> [--max-attempts 20] [--interval-sec 2]

set -euo pipefail

TX_ID="${1:-}"
MAX_ATTEMPTS=20
INTERVAL_SEC=2

print_usage() {
    echo "Usage:"
    echo "  ./check-transaction.sh <TRANSACTION_ID> [--max-attempts 20] [--interval-sec 2]"
}

if [ -z "$TX_ID" ]; then
    print_usage
    exit 1
fi

shift || true
while [ "$#" -gt 0 ]; do
    case "$1" in
        --max-attempts)
            shift
            MAX_ATTEMPTS="${1:-}"
            shift || true
            ;;
        --interval-sec)
            shift
            INTERVAL_SEC="${1:-}"
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

if ! [[ "$MAX_ATTEMPTS" =~ ^[0-9]+$ ]] || [ "$MAX_ATTEMPTS" -le 0 ]; then
    echo "--max-attempts must be a positive integer."
    exit 1
fi

if ! [[ "$INTERVAL_SEC" =~ ^[0-9]+$ ]] || [ "$INTERVAL_SEC" -le 0 ]; then
    echo "--interval-sec must be a positive integer."
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

TX_ID="$TX_ID" MAX_ATTEMPTS="$MAX_ATTEMPTS" INTERVAL_SEC="$INTERVAL_SEC" node - <<'__NODE__'
const { config } = require('dotenv');
const { Wallet } = require('ethers');
const { UniversalAccount, UA_TRANSACTION_STATUS } = require('@particle-network/universal-account-sdk');

config();

function parseNum(name, fallback) {
  const n = Number(process.env[name] || fallback);
  if (!Number.isFinite(n) || n <= 0) {
    throw new Error(`${name} must be a positive number`);
  }
  return Math.floor(n);
}

async function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function isSuccessStatus(status) {
  const known = UA_TRANSACTION_STATUS?.FINISHED;
  return status === known || status === 7;
}

function isFailureStatus(status) {
  const known = UA_TRANSACTION_STATUS?.FAILED;
  return status === known || status === 11;
}

async function main() {
  const txId = process.env.TX_ID || '';
  const maxAttempts = parseNum('MAX_ATTEMPTS', 20);
  const intervalSec = parseNum('INTERVAL_SEC', 2);

  const privateKey = process.env.PRIVATE_KEY || '';
  const projectId = process.env.PROJECT_ID || '';
  const projectClientKey = process.env.PROJECT_CLIENT_KEY || '';
  const projectAppUuid = process.env.PROJECT_APP_UUID || '';

  if (!/^0x[a-fA-F0-9]{64}$/.test(privateKey)) {
    throw new Error('PRIVATE_KEY is missing or invalid in .env');
  }

  const wallet = new Wallet(privateKey);
  const ua = new UniversalAccount({
    projectId,
    projectClientKey,
    projectAppUuid,
    ownerAddress: wallet.address,
  });

  for (let i = 1; i <= maxAttempts; i++) {
    const tx = await ua.getTransaction(txId);
    const status = tx?.status;
    console.log(`poll ${i}/${maxAttempts}: status=${status}`);

    if (isSuccessStatus(status)) {
      console.log('FINAL_STATUS=SUCCESS');
      console.log(`EXPLORER_URL=https://universalx.app/activity/details?id=${txId}`);
      return;
    }
    if (isFailureStatus(status)) {
      console.log('FINAL_STATUS=FAILED');
      console.log(`EXPLORER_URL=https://universalx.app/activity/details?id=${txId}`);
      return;
    }

    if (i < maxAttempts) {
      await sleep(intervalSec * 1000);
    }
  }

  console.log('FINAL_STATUS=PENDING');
  console.log(`EXPLORER_URL=https://universalx.app/activity/details?id=${txId}`);
}

main().catch((err) => {
  console.error('CHECK_TX_ERROR:', err.message || err);
  process.exit(1);
});
__NODE__
