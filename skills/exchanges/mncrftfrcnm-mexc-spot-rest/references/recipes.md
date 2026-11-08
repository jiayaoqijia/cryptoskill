# MEXC Spot REST Recipes

Prepend every line below with `python "${CLAUDE_SKILL_DIR}/scripts/mexc_spot_request.py"`.
For targeted lookup from this skill folder, use `python "${CLAUDE_SKILL_DIR}/scripts/lookup.py" <topic>`.
Keep live mutating requests dry-run first; add `--execute --confirm-live` only when explicitly requested.

## Market Data

```bash
GET /api/v3/ping --execute
GET /api/v3/time --execute
GET /api/v3/defaultSymbols --execute
GET /api/v3/exchangeInfo --execute
GET /api/v3/depth --params '{"symbol":"BTCUSDT","limit":100}' --execute
GET /api/v3/trades --params '{"symbol":"BTCUSDT","limit":100}' --execute
GET /api/v3/aggTrades --params '{"symbol":"BTCUSDT"}' --execute
GET /api/v3/klines --params '{"symbol":"BTCUSDT","interval":"1m","limit":100}' --execute
GET /api/v3/ticker/24hr --params '{"symbol":"BTCUSDT"}' --execute
GET /api/v3/ticker/price --params '{"symbol":"BTCUSDT"}' --execute
GET /api/v3/ticker/bookTicker --params '{"symbol":"BTCUSDT"}' --execute
```

## Account And Balances

```bash
GET /api/v3/account --signed --execute
GET /api/v3/kyc/status --signed --execute
GET /api/v3/selfSymbols --signed --execute
GET /api/v3/myTrades --signed --params '{"symbol":"BTCUSDT"}' --execute
```

## Spot Orders

```bash
POST /api/v3/order/test --signed --params '{"symbol":"BTCUSDT","side":"BUY","type":"LIMIT","quantity":"0.001","price":"10000"}' --execute
POST /api/v3/order --signed --params '{"symbol":"BTCUSDT","side":"BUY","type":"LIMIT","quantity":"0.001","price":"10000"}'
GET /api/v3/order --signed --params '{"symbol":"BTCUSDT","orderId":"123456"}' --execute
GET /api/v3/openOrders --signed --params '{"symbol":"BTCUSDT"}' --execute
GET /api/v3/allOrders --signed --params '{"symbol":"BTCUSDT"}' --execute
DELETE /api/v3/order --signed --params '{"symbol":"BTCUSDT","orderId":"123456"}'
DELETE /api/v3/openOrders --signed --params '{"symbol":"BTCUSDT"}'
```

## Listen Keys And Private Streams

MEXC currently requires signed listen-key requests on the live Spot V3 API.

```bash
POST /api/v3/userDataStream --signed --execute --confirm-live
GET /api/v3/userDataStream --signed --execute
PUT /api/v3/userDataStream --signed --params '{"listenKey":"<listenKey>"}' --execute --confirm-live
DELETE /api/v3/userDataStream --signed --params '{"listenKey":"<listenKey>"}' --execute --confirm-live
```

Connect private Spot WebSocket clients to `wss://wbs-api.mexc.com/ws?listenKey=<listenKey>`.

## Wallet

Use wallet write endpoints only when explicitly requested. Withdrawal and deposit-address generation endpoints are live writes; verify the coin, network, address, memo/tag requirements, withdrawal fee, and official endpoint status before live use.

```bash
GET /api/v3/capital/config/getall --signed --execute
GET /api/v3/capital/deposit/hisrec --signed --params '{"coin":"USDT"}' --execute
GET /api/v3/capital/withdraw/history --signed --params '{"coin":"USDT"}' --execute
GET /api/v3/capital/deposit/address --signed --params '{"coin":"USDT","network":"TRX"}' --execute
POST /api/v3/capital/deposit/address --signed --params '{"coin":"USDT","network":"TRX"}'
POST /api/v3/capital/withdraw --signed --params '{"coin":"USDT","network":"TRX","address":"<address>","amount":"10"}'
```

## Sub-Accounts

Master-account permissions are required.

```bash
POST /api/v3/sub-account/virtualSubAccount --signed --params '{"subAccount":"name","note":"note"}'
GET /api/v3/sub-account/list --signed --params '{"page":1,"limit":20}' --execute
POST /api/v3/sub-account/apiKey --signed --params '{"subAccount":"name","note":"read-only","permissions":"SPOT_ACCOUNT_READ","ip":"1.2.3.4"}'
GET /api/v3/sub-account/apiKey --signed --params '{"subAccount":"name"}' --execute
DELETE /api/v3/sub-account/apiKey --signed --params '{"subAccount":"name","apiKey":"<apiKey>"}'
GET /api/v3/sub-account/asset --signed --params '{"subAccount":"name","accountType":"SPOT"}' --execute
POST /api/v3/capital/sub-account/universalTransfer --signed --params '{"fromAccountType":"SPOT","toAccountType":"FUTURES","asset":"USDT","amount":"1"}'
GET /api/v3/capital/sub-account/universalTransfer --signed --params '{"limit":100}' --execute
```

## Rebates And Affiliate

```bash
GET /api/v3/rebate/taxQuery --signed --params '{"page":1}' --execute
GET /api/v3/rebate/detail --signed --params '{"page":1}' --execute
GET /api/v3/rebate/detail/kickback --signed --params '{"page":1}' --execute
GET /api/v3/rebate/referCode --signed --execute
GET /api/v3/rebate/affiliate/commission/detail --signed --params '{"page":1,"pageSize":10}' --execute
GET /api/v3/rebate/affiliate/referral --signed --params '{"page":1,"pageSize":10}' --execute
GET /api/v3/rebate/affiliate/subaffiliates --signed --params '{"page":1,"pageSize":10}' --execute
```
