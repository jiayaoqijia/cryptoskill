# Autonomy Modes

## Modes

- `cautious`: ask for confirmation on every trade decision.
- `balanced`: auto-approve within configured risk thresholds, request confirmation when exceeded.
- `autonomous`: auto-decide within constraints; block trades that violate configured thresholds.
- `free-agent`: full execution autonomy unless global safety halt is active. In this mode, the agent may define risk tolerance dynamically from mandate goals rather than user-specified per-trade thresholds.

## Strategy collaboration model

- Strategy defaults come from per-strategy config.
- User or agents can override risk and behavior per hypothesis.
- Promotion from paper to live should be mode-aware and KPI-gated.
