#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLI="$ROOT_DIR/bin/openclaw-kraken"
TMP_DIR="$ROOT_DIR/test/.tmp"

mkdir -p "$TMP_DIR"

export OPENCLAW_KRAKEN_CONFIG="$ROOT_DIR/config/kraken.env.example"
export KRAKEN_SIMULATE=true
export KRAKEN_NONCE_CMD="$ROOT_DIR/test/support/fixed_nonce.sh"
export KRAKEN_API_KEY="example-public-key"
export KRAKEN_API_SECRET="kQH5HW/8p1uGOVjbgWA7FunAmGO8lsSUXNsu3eow76sz84Q18fWxnyRzBHCd3pd5nE9qa99HAZtuZuj6F1huXg=="

run() {
  local name="$1"
  shift
  local out="$TMP_DIR/${name}.out"
  local err="$TMP_DIR/${name}.err"
  "$CLI" "$@" >"$out" 2>"$err"
  printf '%s\n' "$out"
}

assert_contains() {
  local file="$1"
  local pattern="$2"
  grep -F "$pattern" "$file" >/dev/null 2>&1 || {
    echo "expected pattern not found in $file: $pattern" >&2
    exit 1
  }
}

assert_not_contains() {
  local file="$1"
  local pattern="$2"
  if grep -F "$pattern" "$file" >/dev/null 2>&1; then
    echo "unexpected pattern found in $file: $pattern" >&2
    exit 1
  fi
}

market_out="$(run market_ticker market ticker --pair XBTUSD)"
assert_contains "$market_out" '"signed":false'
assert_contains "$market_out" '/0/public/Ticker?pair=XBTUSD'

list_out="$(run endpoints_list endpoints funding.)"
assert_contains "$list_out" 'funding.deposit-methods'
assert_contains "$list_out" 'funding.withdraw'

describe_out="$(run describe_withdraw describe funding.withdraw)"
assert_contains "$describe_out" 'confirm_required: true'
assert_contains "$describe_out" '/private/Withdraw'

generic_out="$(run call_balance call account.balance)"
assert_contains "$generic_out" '/0/private/Balance'

raw_out="$(run raw_query_orders raw private QueryOrders --txid OABCDEF-123456-XYZ789)"
assert_contains "$raw_out" '/0/private/QueryOrders'
assert_contains "$raw_out" 'txid=OABCDEF-123456-XYZ789'

futures_list_out="$(run futures_endpoints futures endpoints trading.)"
assert_contains "$futures_list_out" 'trading.send-order'
assert_contains "$futures_list_out" 'trading.cancel-order'

futures_desc_out="$(run futures_describe futures describe trading.send-order)"
assert_contains "$futures_desc_out" 'confirm_required: true'
assert_contains "$futures_desc_out" '/derivatives/api/v3/sendorder'

futures_market_out="$(run futures_market futures call market.tickers --symbol PI_XBTUSD)"
assert_contains "$futures_market_out" '/derivatives/api/v3/tickers?symbol=PI_XBTUSD'

export KRAKEN_FUTURES_API_KEY="example-futures-key"
export KRAKEN_FUTURES_API_SECRET="$KRAKEN_API_SECRET"

futures_order_out="$(run futures_order futures call trading.send-order --symbol PI_XBTUSD --side buy --size 5 --orderType lmt --limitPrice 30000 --confirm)"
assert_contains "$futures_order_out" '/derivatives/api/v3/sendorder'
assert_contains "$futures_order_out" 'symbol=PI_XBTUSD'
assert_contains "$futures_order_out" 'orderType=lmt'

balance_out="$(run account_balance account balance)"
assert_contains "$balance_out" '"signed":true'
assert_contains "$balance_out" 'nonce=1616492376594'
assert_not_contains "$TMP_DIR/account_balance.err" "$KRAKEN_API_SECRET"
assert_not_contains "$TMP_DIR/account_balance.err" "$KRAKEN_API_KEY"
assert_not_contains "$balance_out" "$KRAKEN_API_SECRET"

order_out="$(run orders_add orders add --pair XBTUSD --side buy --type limit --volume 1.25 --price 37500 --confirm)"
assert_contains "$order_out" '/0/private/AddOrder'
assert_contains "$order_out" 'pair=XBTUSD'
assert_contains "$order_out" 'type=buy'
assert_contains "$order_out" 'ordertype=limit'

rich_order_out="$(run rich_orders_add orders add --pair XBTUSD --side sell --type stop-loss-limit --volume 0.75 --price 36500 --price2 36450 --leverage 2:1 --oflags fcib --time-in-force IOC --userref 42 --post-only true --reduce-only true --confirm)"
assert_contains "$rich_order_out" 'price2=36450'
assert_contains "$rich_order_out" 'leverage=2%3A1'
assert_contains "$rich_order_out" 'timeinforce=IOC'
assert_contains "$rich_order_out" 'userref=42'
assert_contains "$rich_order_out" 'oflags=fcib%2Cpost%2Creduce_only'

funding_out="$(run funding_methods funding deposit-methods --asset ETH)"
assert_contains "$funding_out" '/0/private/DepositMethods'
assert_contains "$funding_out" 'asset=ETH'

earn_out="$(run earn_strategies earn strategies --ascending true)"
assert_contains "$earn_out" '/0/private/Earn/Strategies'
assert_contains "$earn_out" 'ascending=true'

if "$CLI" orders cancel --txid OABC >"$TMP_DIR/should_fail.out" 2>"$TMP_DIR/should_fail.err"; then
  echo "cancel without --confirm unexpectedly succeeded" >&2
  exit 1
fi
assert_contains "$TMP_DIR/should_fail.err" 'without --confirm'

if "$CLI" funding withdraw --asset ETH --key MyWallet --amount 0.1 >"$TMP_DIR/withdraw_fail.out" 2>"$TMP_DIR/withdraw_fail.err"; then
  echo "withdraw without --confirm unexpectedly succeeded" >&2
  exit 1
fi
assert_contains "$TMP_DIR/withdraw_fail.err" 'without --confirm'

challenge_out="$(run futures_challenge ws futures-sign-challenge challenge-string)"
assert_contains "$challenge_out" '"api_key":"example-futures-key"'
assert_contains "$challenge_out" '"original_challenge":"challenge-string"'

echo "smoke tests passed"
