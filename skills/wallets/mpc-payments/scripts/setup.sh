#!/usr/bin/env bash
# setup.sh — Initialize Helio (MoonPay Commerce) credentials
# Fetches wallet ID automatically from API — no need to copy from dashboard.
#
# Usage:
#   bash setup.sh              Interactive setup
#   bash setup.sh status       Show current config
#   bash setup.sh clear        Remove saved credentials

set -euo pipefail

CONFIG_DIR="$HOME/.mpc/helio"
CONFIG_FILE="$CONFIG_DIR/config"
BASE="https://api.hel.io/v1"

die() { echo "❌ $1" >&2; exit 1; }
ok()  { echo "✅ $1"; }

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

cmd_status() {
    echo "=== Helio Configuration ==="
    if [[ -f "$CONFIG_FILE" ]]; then
        load_config "$CONFIG_FILE"
        echo "Config: $CONFIG_FILE"
        echo "API Key: ${HELIO_API_KEY:0:8}...${HELIO_API_KEY: -4}"
        echo "API Secret: ${HELIO_API_SECRET:0:8}...${HELIO_API_SECRET: -4}"
        echo "Wallet ID: $HELIO_WALLET_ID"
        if [[ -n "${HELIO_WALLET_PUBKEY:-}" ]]; then
            echo "Wallet Address: $HELIO_WALLET_PUBKEY"
        fi
    else
        echo "Not configured. Run: bash setup.sh"
    fi
}

cmd_clear() {
    if [[ -f "$CONFIG_FILE" ]]; then
        rm -f "$CONFIG_FILE"
        ok "Credentials cleared."
    else
        echo "No config to clear."
    fi
}

cmd_setup() {
    echo "=== Helio Setup ==="
    echo ""
    echo "Get your API credentials from: https://app.hel.io → Settings → API Keys"
    echo ""

    # Check if already configured
    if [[ -f "$CONFIG_FILE" ]]; then
        echo "⚠️  Existing config found. This will replace it."
        read -p "Continue? [y/N] " confirm
        [[ "$confirm" =~ ^[Yy] ]] || exit 0
        echo ""
    fi

    # Get API Key
    read -p "API Key: " api_key
    [[ -n "$api_key" ]] || die "API Key is required."

    # Get API Secret
    read -p "API Secret: " api_secret
    [[ -n "$api_secret" ]] || die "API Secret is required."

    echo ""
    echo "Fetching wallets from API..."

    # Fetch wallets
    response=$(curl -s -w "\n%{http_code}" "$BASE/wallet/all?apiKey=$api_key" \
        -H "Authorization: Bearer $api_secret")
    
    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$d')

    if [[ "$http_code" != "200" ]]; then
        echo "Response: $body"
        die "API returned HTTP $http_code. Check your credentials."
    fi

    # Parse wallets — look for SOL PAYOUT wallet
    wallets=$(echo "$body" | jq -r '.[] | select(.blockchainEngineType == "SOL")')
    
    if [[ -z "$wallets" ]]; then
        die "No Solana wallets found. Add a wallet at https://app.hel.io → Settings → Wallets"
    fi

    # Prefer PAYOUT wallet, fallback to CONNECTED
    payout_wallet=$(echo "$body" | jq -r '[.[] | select(.blockchainEngineType == "SOL" and .walletCategory == "PAYOUT")][0]')
    connected_wallet=$(echo "$body" | jq -r '[.[] | select(.blockchainEngineType == "SOL" and .walletCategory == "CONNECTED")][0]')

    if [[ "$payout_wallet" != "null" && -n "$payout_wallet" ]]; then
        wallet="$payout_wallet"
        echo "Found SOL PAYOUT wallet"
    elif [[ "$connected_wallet" != "null" && -n "$connected_wallet" ]]; then
        wallet="$connected_wallet"
        echo "Found SOL CONNECTED wallet (no PAYOUT wallet found)"
    else
        die "No suitable Solana wallet found."
    fi

    wallet_id=$(echo "$wallet" | jq -r '.id')
    wallet_pubkey=$(echo "$wallet" | jq -r '.publicKey')
    wallet_name=$(echo "$wallet" | jq -r '.name // "unnamed"')
    wallet_category=$(echo "$wallet" | jq -r '.walletCategory')

    echo ""
    echo "Selected wallet:"
    echo "  ID: $wallet_id"
    echo "  Address: $wallet_pubkey"
    echo "  Name: $wallet_name"
    echo "  Type: $wallet_category"
    echo ""

    # If multiple SOL wallets, let user confirm
    wallet_count=$(echo "$body" | jq '[.[] | select(.blockchainEngineType == "SOL")] | length')
    if [[ "$wallet_count" -gt 1 ]]; then
        echo "ℹ️  Found $wallet_count Solana wallets. Using the one above."
        echo "   To use a different wallet, configure manually in $CONFIG_FILE"
    fi

    # Save config
    mkdir -p "$CONFIG_DIR"
    cat > "$CONFIG_FILE" <<EOF
# Helio (MoonPay Commerce) credentials
# Generated by setup.sh — $(date -u +"%Y-%m-%dT%H:%M:%SZ")

HELIO_API_KEY="$api_key"
HELIO_API_SECRET="$api_secret"
HELIO_WALLET_ID="$wallet_id"
HELIO_WALLET_PUBKEY="$wallet_pubkey"
EOF
    chmod 600 "$CONFIG_FILE"

    ok "Configuration saved to $CONFIG_FILE"
    echo ""
    echo "You can now use helio.sh commands:"
    echo "  bash scripts/helio.sh create-paylink \"Coffee\" 5.00 USDC"
    echo "  bash scripts/helio.sh charge <paylink-id>"
}

case "${1:-setup}" in
    setup)  cmd_setup ;;
    status) cmd_status ;;
    clear)  cmd_clear ;;
    *)
        echo "Usage: setup.sh [setup|status|clear]"
        echo ""
        echo "  setup   Configure API credentials (default)"
        echo "  status  Show current configuration"
        echo "  clear   Remove saved credentials"
        ;;
esac
