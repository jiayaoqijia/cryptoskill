# Examples

## Discovery

```bash
bin/openclaw-kraken endpoints
bin/openclaw-kraken endpoints funding.
bin/openclaw-kraken describe earn.allocate
bin/openclaw-kraken futures endpoints account.
bin/openclaw-kraken futures describe trading.send-order
```

## Public

```bash
bin/openclaw-kraken market assets
bin/openclaw-kraken market asset-pairs --pair XBTUSD
bin/openclaw-kraken market orderbook --pair XBTUSD --count 25 --compact
bin/openclaw-kraken market ohlc --pair XBTUSD --interval 60
```

## Read-only private

```bash
bin/openclaw-kraken account balance
bin/openclaw-kraken account open-orders --trades true --jq '.result.open'
bin/openclaw-kraken account ledgers --type trade
bin/openclaw-kraken call account.query-orders --txid OABCDEF-123456-XYZ789
```

## Trading

```bash
bin/openclaw-kraken orders add --pair XBTUSD --side buy --type market --volume 0.01 --oflags post --time-in-force IOC --userref 42 --confirm
bin/openclaw-kraken call trading.add-order-batch --pair XBTUSD --param-file orders /tmp/orders.json --confirm
bin/openclaw-kraken orders cancel --txid OABCDEF-123456-XYZ789 --confirm
bin/openclaw-kraken orders cancel-all --confirm
```

## Funding, Earn, and Subaccounts

```bash
bin/openclaw-kraken funding deposit-methods --asset ETH
bin/openclaw-kraken funding withdraw-info --asset ETH --key MyWallet --amount 0.5
bin/openclaw-kraken earn strategies --ascending true
bin/openclaw-kraken subaccounts transfer --asset XBT --amount 0.01 --from master --to trading-desk --confirm
```

## Futures

```bash
bin/openclaw-kraken futures call market.tickers
bin/openclaw-kraken futures call market.orderbook --symbol PI_XBTUSD
bin/openclaw-kraken futures call account.open-orders
bin/openclaw-kraken futures call trading.send-order --symbol PI_XBTUSD --side buy --size 5 --orderType lmt --limitPrice 30000 --confirm
bin/openclaw-kraken futures raw private /derivatives/api/v3/cancelorder --set order_id abc123 --confirm --method POST
```

## WebSockets

```bash
bin/openclaw-kraken ws spot-public --message-json '{"method":"ping"}'
bin/openclaw-kraken ws spot-private --message-json '{"method":"subscribe","params":{"channel":"balances"}}'
bin/openclaw-kraken ws futures-public --message-json '{"event":"subscribe","feed":"ticker","product_ids":["PI_XBTUSD"]}'
bin/openclaw-kraken ws futures-sign-challenge '<challenge-string>'
bin/openclaw-kraken ws open --url wss://ws.kraken.com/v2 --message-file /tmp/request.json --timeout-ms 15000 --max-messages 5
```
