# Analytics Wiring Patterns

Screen views are emitted once, from the screen or modal that renders them, and attribution for controller-owned events is merged in `createPerpsInfrastructure`, not in UI code.

- **Screen-view double-emission on normal+error page pairs** — any page that renders both a normal screen view and an error screen view must gate the normal view on the subject existing (`Boolean(market)`) and give the error view a `resetKey`. Without this, one rendered error screen emits two events, and consecutive bad symbols each emit one instead of resetting cleanly.
- **Modal screen view at trigger site instead of in the modal** — screen views for a modal belong in the modal itself, not at its trigger sites. A modal with many triggers (e.g. a geo-block notice with 17 triggers across 11 hosts) needs one declarative `usePerpsEventTracking({conditions: isOpen})` in the modal, not 17 scattered call sites.
- **Removing client `track()` calls without checking background API** — when migrating analytics from client to controller, verify the matching background API actually accepts `trackingData`. Some APIs (e.g. `UpdateMarginParams`) do not — no `trackingData` field is needed for those.
- **Attribution split** — UI `trackingData` carries entry/discovery/hlFeeRate; stored UTM context must be merged in `createPerpsInfrastructure` via `mergeAttributionContext` for controller-emitted lifecycle events. Do not merge attribution in UI code for controller-owned events.
