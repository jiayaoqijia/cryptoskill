# Adapter Plugin Contract

Adapters are the extension point for exchanges, data feeds, and research tools.

## Adapter types

- `execution`: place/cancel/query orders on broker/exchange venues.
- `market_data`: retrieve normalized quotes/candles/orderbook snapshots.
- `news`: retrieve normalized headlines/sentiment snippets for research.

## Requirements

- Register adapters via `AdapterRegistry`.
- Return normalized payloads to keep orchestration independent from specific vendors.
- Avoid hardcoding venue assumptions in orchestration and strategy code.

## Skill-aware routing

- Use `SkillDiscoveryService` to scan local skill roots for available `SKILL.md` capabilities.
- Use `AdapterRouter` to resolve provider routes:
  - skill-backed route when matching skill aliases exist
  - direct adapter route otherwise
- Router preferences are mutable per provider, allowing gradual migration from skill-backed to direct adapters (or the reverse) as implementations improve.
- Discovery supports periodic refresh via TTL and optional force-refresh on demand.
