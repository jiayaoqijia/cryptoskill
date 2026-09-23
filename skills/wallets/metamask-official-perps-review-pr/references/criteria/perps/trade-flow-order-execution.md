# Trade Flow & Order Execution

Order submission runs the shared pre-trade checks, carries the user's slippage, and refreshes state after confirmation.

- **Pre-trade checks missing** — submitting trade without verifying: sufficient balance, market open, position limit, leverage within bounds, slippage tolerance set.
- **Post-trade state not refreshed** — after trade confirmation, not triggering refresh of balances, positions, orders. User sees stale data until next WS tick.
- **Missing slippage in order params** — creating order without slippage tolerance, or hardcoding slippage instead of user preference.
