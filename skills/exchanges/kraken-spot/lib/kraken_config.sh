#!/usr/bin/env bash

kraken_load_config() {
  local root_dir="$1"
  local version_file="$root_dir/VERSION"

  if [ -n "${OPENCLAW_KRAKEN_CONFIG:-}" ]; then
    [ -f "$OPENCLAW_KRAKEN_CONFIG" ] || kraken_fail "config file not found: $OPENCLAW_KRAKEN_CONFIG"
    # shellcheck disable=SC1090
    source "$OPENCLAW_KRAKEN_CONFIG"
  fi

  if [ -f "$version_file" ]; then
    KRAKEN_VERSION="$(tr -d '\n' <"$version_file")"
  else
    KRAKEN_VERSION="dev"
  fi

  : "${KRAKEN_API_BASE_URL:=https://api.kraken.com}"
  : "${KRAKEN_API_VERSION:=0}"
  : "${KRAKEN_TIMEOUT_SECS:=30}"
  : "${KRAKEN_USER_AGENT:=openclaw-kraken/${KRAKEN_VERSION}}"
  : "${KRAKEN_LOG_LEVEL:=info}"
  : "${KRAKEN_REQUIRE_CONFIRM:=true}"
  : "${KRAKEN_OUTPUT_MODE:=raw}"
  : "${KRAKEN_DEFAULT_PAIR:=}"
  : "${KRAKEN_OTP:=}"
  : "${KRAKEN_HTTP_BIN:=curl}"
  : "${KRAKEN_NONCE_CMD:=}"
  : "${KRAKEN_ALLOW_INSECURE_BASE_URL:=false}"
  : "${KRAKEN_SIMULATE:=false}"
  : "${KRAKEN_ENDPOINTS_FILE:=$root_dir/config/endpoints.tsv}"
  : "${KRAKEN_FUTURES_API_BASE_URL:=https://futures.kraken.com}"
  : "${KRAKEN_FUTURES_ENDPOINTS_FILE:=$root_dir/config/futures_endpoints.tsv}"
  : "${KRAKEN_WS_SPOT_PUBLIC_URL:=wss://ws.kraken.com/v2}"
  : "${KRAKEN_WS_SPOT_PRIVATE_URL:=wss://ws-auth.kraken.com/v2}"
  : "${KRAKEN_WS_FUTURES_URL:=wss://futures.kraken.com/ws/v1}"
  : "${KRAKEN_WS_TIMEOUT_MS:=10000}"
  : "${KRAKEN_WS_MAX_MESSAGES:=1}"
  : "${KRAKEN_WS_NODE_BIN:=node}"

  export KRAKEN_ROOT_DIR="$root_dir"
}
