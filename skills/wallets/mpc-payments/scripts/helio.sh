#!/usr/bin/env bash
# helio.sh — MoonPay Commerce (Helio) CLI helper
# Usage: bash helio.sh <command> [args...]
#
# Commands:
#   currencies                         List Solana currencies
#   currency-id <SYMBOL>               Get currency ID by symbol (e.g. USDC, SOL)
#   create-paylink <name> <amount> <symbol>  Create a Pay Link
#   charge <paylink-id>                Create checkout URL
#   transactions <paylink-id>          List transactions
#   disable <paylink-id>               Disable a Pay Link
#   enable <paylink-id>                Re-enable a Pay Link

set -euo pipefail

command -v jq &>/dev/null || { echo "❌ jq required. Install: brew install jq (macOS) or apt install jq (Linux)"; exit 1; }

BASE="https://api.hel.io/v1"
CONFIG_FILE="$HOME/.mpc/helio/config"

# Safe config loader — only parses whitelisted KEY="value" lines
load_config() {
  local cfg="$1"
  [[ -f "$cfg" ]] || return 1

  # Validate file ownership (must be current user)
  local file_owner
  if stat --version &>/dev/null 2>&1; then
    file_owner=$(stat -c '%u' "$cfg")  # GNU
  else
    file_owner=$(stat -f '%u' "$cfg")  # BSD/macOS
  fi
  if [[ "$file_owner" != "$(id -u)" ]]; then
    echo "WARNING: Config $cfg is not owned by you — skipping" >&2
    return 1
  fi

  # Reject world-readable or world-writable
  local perms
  if stat --version &>/dev/null 2>&1; then
    perms=$(stat -c '%a' "$cfg")  # GNU
  else
    perms=$(stat -f '%A' "$cfg")  # BSD/macOS
  fi
  local other="${perms: -1}"
  if [[ "$other" != "0" ]]; then
    echo "WARNING: Config $cfg has unsafe permissions ($perms) — skipping" >&2
    echo "  Fix with: chmod 600 $cfg" >&2
    return 1
  fi

  # Parse only whitelisted KEY="value" lines
  while IFS='=' read -r key value; do
    # Strip leading/trailing whitespace from key
    key="${key// /}"
    # Skip comments and blank lines
    [[ -z "$key" || "$key" == \#* ]] && continue
    # Strip surrounding quotes from value
    value="${value%\"}"
    value="${value#\"}"
    case "$key" in
      HELIO_API_KEY)       HELIO_API_KEY="$value" ;;
      HELIO_API_SECRET)    HELIO_API_SECRET="$value" ;;
      HELIO_WALLET_ID)     HELIO_WALLET_ID="$value" ;;
      HELIO_WALLET_PUBKEY) HELIO_WALLET_PUBKEY="$value" ;;
    esac
  done < "$cfg"
}

# Reject input containing shell metacharacters or URL traversal
validate_input() {
  local label="$1" value="$2"
  if [[ "$value" =~ [^a-zA-Z0-9._@:/-] ]]; then
    echo "ERROR: Invalid $label: contains unsafe characters" >&2
    exit 1
  fi
  if [[ "$value" == *..* ]]; then
    echo "ERROR: Invalid $label: path traversal not allowed" >&2
    exit 1
  fi
}

# Auto-load config if exists
load_config "$CONFIG_FILE" || true

# Check credentials
check_auth() {
  if [[ -z "${HELIO_API_KEY:-}" || -z "${HELIO_API_SECRET:-}" ]]; then
    echo "ERROR: Helio not configured. Run setup first:" >&2
    echo "  bash scripts/setup.sh" >&2
    exit 1
  fi
}

check_wallet() {
  if [[ -z "${HELIO_WALLET_ID:-}" ]]; then
    echo "ERROR: Wallet ID not configured. Run setup first:" >&2
    echo "  bash scripts/setup.sh" >&2
    exit 1
  fi
}

# Auth headers
auth_headers() {
  echo -H "Authorization: Bearer $HELIO_API_SECRET"
}

cmd="${1:-help}"
shift || true

case "$cmd" in
  currencies)
    echo "Fetching Solana currencies..."
    curl -s "$BASE/currency" | jq -r '.[] | select(.blockchain.symbol == "SOL") | "\(.symbol)\t\(.id)\tdecimals=\(.decimals)"' | sort
    ;;

  currency-id)
    symbol="${1:?Usage: helio.sh currency-id <SYMBOL>}"
    validate_input "symbol" "$symbol"
    curl -s "$BASE/currency" | jq -r --arg s "$symbol" '.[] | select(.symbol == $s and .blockchain.symbol == "SOL") | .id'
    ;;

  create-paylink)
    name="${1:?Usage: helio.sh create-paylink <name> <amount> <symbol>}"
    amount="${2:?Missing amount}"
    symbol="${3:-USDC}"
    validate_input "amount" "$amount"
    validate_input "symbol" "$symbol"
    check_auth
    check_wallet

    # Look up currency
    echo "Looking up currency $symbol..."
    currency_info=$(curl -s "$BASE/currency" | jq -r --arg s "$symbol" '[.[] | select(.symbol == $s and .blockchain.symbol == "SOL")][0]')

    if [[ "$currency_info" == "null" || -z "$currency_info" ]]; then
      echo "ERROR: Currency $symbol not found on Solana" >&2
      exit 1
    fi

    currency_id=$(echo "$currency_info" | jq -r '.id')
    decimals=$(echo "$currency_info" | jq -r '.decimals')

    # Convert human-readable amount to base units
    price=$(awk -v amt="$amount" -v dec="$decimals" 'BEGIN {
      p = 1; for (i = 0; i < dec; i++) p *= 10
      printf "%.0f", amt * p
    }')

    echo "Creating Pay Link: $name — $amount $symbol ($price base units, currency=$currency_id, swap=on)"

    result=$(curl -s -X POST "$BASE/paylink/create/api-key?apiKey=$HELIO_API_KEY" \
      -H "Authorization: Bearer $HELIO_API_SECRET" \
      -H "Content-Type: application/json" \
      -d "$(jq -n \
        --arg name "$name" \
        --arg price "$price" \
        --arg currId "$currency_id" \
        --arg walletId "$HELIO_WALLET_ID" \
        '{
          name: $name,
          template: "OTHER",
          pricingCurrency: $currId,
          price: $price,
          features: {
            canChangePrice: false,
            canChangeQuantity: false,
            canSwapTokens: true
          },
          recipients: [{
            currencyId: $currId,
            walletId: $walletId
          }]
        }'
      )")

    echo "$result" | jq .

    # Extract paylink ID if present
    plid=$(echo "$result" | jq -r '.id // empty')
    if [[ -n "$plid" ]]; then
      echo ""
      echo "Pay Link ID: $plid"
      echo "Checkout:    https://app.hel.io/pay/$plid"
    fi
    ;;

  charge)
    paylink_id="${1:?Usage: helio.sh charge <paylink-id>}"
    validate_input "paylink-id" "$paylink_id"
    check_auth

    echo "Creating charge for paylink $paylink_id..."
    result=$(curl -s -X POST "$BASE/charge/api-key?apiKey=$HELIO_API_KEY" \
      -H "Authorization: Bearer $HELIO_API_SECRET" \
      -H "Content-Type: application/json" \
      -d "$(jq -n --arg id "$paylink_id" '{paymentRequestId: $id}')")

    echo "$result" | jq .

    url=$(echo "$result" | jq -r '.pageUrl // empty')
    if [[ -n "$url" ]]; then
      echo ""
      echo "Checkout URL: $url"
    fi
    ;;

  transactions)
    paylink_id="${1:?Usage: helio.sh transactions <paylink-id>}"
    validate_input "paylink-id" "$paylink_id"
    check_auth

    echo "Fetching transactions for paylink $paylink_id..."
    curl -s "$BASE/paylink/$paylink_id/transactions?apiKey=$HELIO_API_KEY" \
      -H "Authorization: Bearer $HELIO_API_SECRET" | jq .
    ;;

  disable)
    paylink_id="${1:?Usage: helio.sh disable <paylink-id>}"
    validate_input "paylink-id" "$paylink_id"
    check_auth

    echo "Disabling paylink $paylink_id..."
    curl -s -X PATCH "$BASE/paylink/$paylink_id/disable?apiKey=$HELIO_API_KEY&disabled=true" \
      -H "Authorization: Bearer $HELIO_API_SECRET"
    echo "Done."
    ;;

  enable)
    paylink_id="${1:?Usage: helio.sh enable <paylink-id>}"
    validate_input "paylink-id" "$paylink_id"
    check_auth

    echo "Enabling paylink $paylink_id..."
    curl -s -X PATCH "$BASE/paylink/$paylink_id/disable?apiKey=$HELIO_API_KEY&disabled=false" \
      -H "Authorization: Bearer $HELIO_API_SECRET"
    echo "Done."
    ;;

  help|*)
    cat <<'EOF'
helio.sh — MoonPay Commerce (Helio) CLI helper

Commands:
  currencies                             List Solana currencies (no auth needed)
  currency-id <SYMBOL>                   Get currency ID for a symbol
  create-paylink <name> <amount> <symbol>  Create a Pay Link
  charge <paylink-id>                    Create a checkout URL for payers
  transactions <paylink-id>              List transactions for a Pay Link
  disable <paylink-id>                   Disable a Pay Link
  enable <paylink-id>                    Re-enable a Pay Link

Setup:
  bash scripts/setup.sh                  Configure API key + secret (auto-fetches wallet ID)
  bash scripts/setup.sh status           Show current config
  bash scripts/setup.sh clear            Remove saved credentials

Config is loaded from: ~/.mpc/helio/config
Get API credentials at: https://app.hel.io → Settings → API Keys
EOF
    ;;
esac
