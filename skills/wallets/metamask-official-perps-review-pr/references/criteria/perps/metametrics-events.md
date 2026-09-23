# MetaMetrics Events

Every perps event uses one of the eight consolidated events and their typed property constants (mobile `docs/perps/perps-metametrics-reference.md`); no new event names or untyped properties.

- **Magic string event properties** — using `'status'`, `'asset'`, `'direction'` instead of `PERPS_EVENT_PROPERTY.STATUS`, `PERPS_EVENT_PROPERTY.ASSET`, etc. from `@metamask/perps-controller`.
- **Magic string event values** — using `'executed'`, `'long'`, `'market'` instead of `PERPS_EVENT_VALUE.STATUS.EXECUTED`, `PERPS_EVENT_VALUE.DIRECTION.LONG`, `PERPS_EVENT_VALUE.ORDER_TYPE.MARKET`.
- **New event instead of property** — creating a 9th event when the change should be a new `screen_type`, `interaction_type`, or `action_type` value on an existing event. The 8-event model is intentional (Segment cost optimization).
- **Missing `source` on screen view** — `PERPS_SCREEN_VIEWED` without `source` property loses navigation flow tracking. Source = current screen, not earlier in the chain.
- **Hardcoded source in reusable component** — reusable components (`PerpsMarketTypeSection`, `PerpsWatchlistMarkets`, `PerpsCard`) must receive `source` as a prop from the parent screen, not set it implicitly.
- **New screen/view without tracking** — adding a new view without `PERPS_SCREEN_VIEWED` event + `usePerpsMeasurement` Sentry trace.
- **Missing `completion_duration` on transaction events** — all transaction events (`PERPS_TRADE_TRANSACTION`, `PERPS_POSITION_CLOSE_TRANSACTION`, etc.) require duration tracking.
