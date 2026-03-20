#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

export OPENCLAW_KRAKEN_CONFIG="$ROOT_DIR/config/kraken.env.example"
export KRAKEN_API_KEY="unused"
export KRAKEN_API_SECRET="kQH5HW/8p1uGOVjbgWA7FunAmGO8lsSUXNsu3eow76sz84Q18fWxnyRzBHCd3pd5nE9qa99HAZtuZuj6F1huXg=="

# shellcheck source=/dev/null
source "$ROOT_DIR/lib/kraken_redact.sh"
# shellcheck source=/dev/null
source "$ROOT_DIR/lib/kraken_config.sh"
# shellcheck source=/dev/null
source "$ROOT_DIR/lib/kraken_validate.sh"
# shellcheck source=/dev/null
source "$ROOT_DIR/lib/kraken_auth.sh"

kraken_load_config "$ROOT_DIR"
kraken_validate_runtime

payload='nonce=1616492376594&ordertype=limit&pair=XBTUSD&price=37500&type=buy&volume=1.25'
actual="$(kraken_sign_payload "/private/AddOrder" "$payload" "1616492376594")"
expected='4/dpxb3iT4tp/ZCVEwSnEsLxx0bqyhLpdfOpc6fn7OR8+UClSV5n9E6aSS8MPtnRfp32bAb0nmbRn6H8ndwLUQ=='

if [ "$actual" != "$expected" ]; then
  echo "signature mismatch" >&2
  echo "expected: $expected" >&2
  echo "actual:   $actual" >&2
  exit 1
fi

echo "signature example passed"
