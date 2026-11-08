# MEXC Futures REST Recipes

Prepend every line below with `python "${CLAUDE_SKILL_DIR}/scripts/mexc_futures_request.py"`.
For targeted lookup from this skill folder, use `python "${CLAUDE_SKILL_DIR}/scripts/lookup.py" <topic>`.
Futures private writes are live-only and may be under maintenance or permission-gated; dry-run first, verify the current official docs, and add `--execute --confirm-live` only when explicitly requested.

## Market Data

```bash
GET /api/v1/contract/ping --execute
GET /api/v1/contract/detail --execute
GET /api/v1/contract/detail --params '{"symbol":"BTC_USDT"}' --execute
GET /api/v1/contract/depth/BTC_USDT --params '{"limit":20}' --execute
GET /api/v1/contract/ticker --execute
GET /api/v1/contract/ticker --params '{"symbol":"BTC_USDT"}' --execute
GET /api/v1/contract/index_price/BTC_USDT --execute
GET /api/v1/contract/fair_price/BTC_USDT --execute
GET /api/v1/contract/funding_rate/BTC_USDT --execute
GET /api/v1/contract/kline/BTC_USDT --params '{"interval":"Min1"}' --execute
```

## Assets And Account

```bash
GET /api/v1/private/account/assets --signed --execute
GET /api/v1/private/account/asset/USDT --signed --execute
GET /api/v1/private/account/transfer_record --signed --params '{"currency":"USDT"}' --execute
GET /api/v1/private/account/risk_limit --signed --params '{"symbol":"BTC_USDT"}' --execute
GET /api/v1/private/account/tiered_fee_rate --signed --params '{"symbol":"BTC_USDT"}' --execute
```

## Positions

Position-changing endpoints are private writes. Verify current official docs, account permissions, and maintenance status before live use.

```bash
GET /api/v1/private/position/open_positions --signed --execute
GET /api/v1/private/position/open_positions --signed --params '{"symbol":"BTC_USDT"}' --execute
GET /api/v1/private/position/list/history_positions --signed --params '{"symbol":"BTC_USDT","page_num":1,"page_size":20}' --execute
GET /api/v1/private/position/funding_records --signed --params '{"symbol":"BTC_USDT","page_num":1,"page_size":20}' --execute
GET /api/v1/private/position/leverage --signed --params '{"symbol":"BTC_USDT"}' --execute
GET /api/v1/private/position/position_mode --signed --execute
POST /api/v1/private/position/change_margin --signed --params '{"positionId":123,"amount":"1","type":"ADD"}'
POST /api/v1/private/position/change_leverage --signed --params '{"symbol":"BTC_USDT","positionType":1,"openType":1,"leverage":5}'
POST /api/v1/private/position/change_position_mode --signed --params '{"positionMode":1}'
```

## Orders

Order submit, batch submit, cancel, and related private order workflows may be under maintenance or permission-gated in the official docs. Verify the current official endpoint status before live use.

```bash
POST /api/v1/private/order/submit --signed --params '{"symbol":"BTC_USDT","price":"10000","vol":"1","leverage":1,"side":1,"type":1,"openType":1}'
POST /api/v1/private/order/submit_batch --signed --params '[{"symbol":"BTC_USDT","price":"10000","vol":"1","leverage":1,"side":1,"type":1,"openType":1}]'
GET /api/v1/private/order/list/open_orders/BTC_USDT --signed --execute
GET /api/v1/private/order/list/history_orders --signed --params '{"symbol":"BTC_USDT","page_num":1,"page_size":20}' --execute
GET /api/v1/private/order/external/BTC_USDT/exampleExternalOid --signed --execute
GET /api/v1/private/order/get/123456 --signed --execute
GET /api/v1/private/order/batch_query --signed --params '{"order_ids":"123456,789012"}' --execute
GET /api/v1/private/order/deal_details/123456 --signed --execute
GET /api/v1/private/order/list/order_deals --signed --params '{"symbol":"BTC_USDT","page_num":1,"page_size":20}' --execute
POST /api/v1/private/order/cancel --signed --params '[{"orderId":123456}]'
POST /api/v1/private/order/cancel_with_external --signed --params '[{"symbol":"BTC_USDT","externalOid":"exampleExternalOid"}]'
POST /api/v1/private/order/cancel_all --signed --params '{"symbol":"BTC_USDT"}'
```

## Plan, TP/SL, And Trailing Orders

Plan, TP/SL, trailing, and stop-order workflows may be under maintenance or permission-gated in the official docs. Verify the current official endpoint status before live use.

```bash
GET /api/v1/private/planorder/list/orders --signed --params '{"symbol":"BTC_USDT","states":"1"}' --execute
POST /api/v1/private/planorder/place --signed --params '{"symbol":"BTC_USDT","price":"10000","vol":"1","side":1,"openType":1,"triggerPrice":"11000","triggerType":1,"executeCycle":1,"orderType":1,"trend":1}'
POST /api/v1/private/planorder/cancel --signed --params '[{"symbol":"BTC_USDT","orderId":"123456"}]'
POST /api/v1/private/planorder/cancel_all --signed --params '{"symbol":"BTC_USDT"}'
GET /api/v1/private/stoporder/order_details/123456 --signed --execute
POST /api/v1/private/stoporder/cancel --signed --params '[{"stopPlanOrderId":123456}]'
POST /api/v1/private/stoporder/cancel_all --signed --params '{"symbol":"BTC_USDT"}'
```

## STP And Matching Controls

Current Futures docs include STP-related controls. Keep STP changes out of local recipes until exact endpoint paths and account permissions are verified against the live official docs for the task.
