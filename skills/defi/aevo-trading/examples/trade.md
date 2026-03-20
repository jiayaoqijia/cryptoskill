# Example: Bracket Trade

Placing a long ETH-PERP position with stop-loss and take-profit using a bracket order. Demonstrates the mandatory confirmation flow before order execution.

---

**User**: I want to long 0.5 ETH-PERP at $2,450 with a stop at $2,380 and TP at $2,600.

**Assistant**: Got it. Before placing this order, let me run a risk check on the proposed trade.

*[calls aevo_risk_check(instrument_name="ETH-PERP", side="buy", amount=0.5, price=2450)]*

Here's the risk assessment for your proposed trade:

| Detail | Value |
|---|---|
| **Instrument** | ETH-PERP |
| **Side** | Long |
| **Size** | 0.5 ETH |
| **Entry price** | $2,450.00 (limit) |
| **Notional** | $1,225.00 |
| **Stop-loss** | $2,380.00 (-2.86%) |
| **Take-profit** | $2,600.00 (+6.12%) |
| **Max loss** | $35.00 (at stop) |
| **Max profit** | $75.00 (at TP) |
| **Risk/reward** | 1 : 2.14 |
| **Post-trade margin utilization** | 18.4% (from 12.1%) |
| **Liquidation distance** | >40% (healthy) |

Risk check passed. No guardrail violations.

**Shall I place this bracket order?** (entry + stop-loss + take-profit)

---

**User**: Yes, go ahead.

**Assistant**: Placing the bracket order now.

*[calls aevo_bracket_order(instrument_name="ETH-PERP", side="buy", amount=0.5, limit_price=2450, stop_loss=2380, take_profit=2600)]*

Bracket order submitted. Let me verify all three legs.

*[calls aevo_list_orders(instrument_name="ETH-PERP")]*

All 3 legs confirmed:

| Leg | Type | Price | Status |
|---|---|---|---|
| **Entry** | Limit Buy | $2,450.00 | Open (resting) |
| **Stop-loss** | Stop Market Sell | $2,380.00 | Pending (triggers on entry fill) |
| **Take-profit** | Limit Sell | $2,600.00 | Pending (triggers on entry fill) |

**Summary**: Your long 0.5 ETH-PERP bracket order is live. The entry is resting at $2,450. Once filled, the stop-loss at $2,380 and take-profit at $2,600 will activate automatically.

- If ETH drops to $2,380 first: you lose ~$35
- If ETH reaches $2,600 first: you gain ~$75
- Risk/reward: 1 : 2.14

I'll keep an eye on this. Want me to check the orderbook depth at $2,450, or is there anything else?

---

**User**: Actually, can you tighten the stop to $2,420?

**Assistant**: Let me cancel the existing stop-loss and replace it. First, let me check the current orders.

*[calls aevo_list_orders(instrument_name="ETH-PERP")]*

Found the stop-loss order. I'll cancel and replace it.

*[calls aevo_cancel_order(order_id="0xabc123...stop_order_id")]*

Stop-loss cancelled. Now placing the updated stop.

Before I do, here's how this changes your risk profile:

| Detail | Old | New |
|---|---|---|
| **Stop-loss** | $2,380 (-2.86%) | $2,420 (-1.22%) |
| **Max loss** | $35.00 | $15.00 |
| **Risk/reward** | 1 : 2.14 | 1 : 5.0 |

The tighter stop reduces your max loss to $15 but increases the chance of getting stopped out on normal volatility. ETH's recent intraday range has been ~$40-60, so a $30 stop is fairly tight.

**Want me to proceed with the $2,420 stop?**

---

**User**: Yes.

**Assistant**: *[calls aevo_create_order(instrument_name="ETH-PERP", side="sell", amount=0.5, trigger_price=2420, order_type="stop_market", reduce_only=true)]*

*[calls aevo_list_orders(instrument_name="ETH-PERP")]*

Updated stop-loss confirmed:

| Leg | Type | Price | Status |
|---|---|---|---|
| **Entry** | Limit Buy | $2,450.00 | Open (resting) |
| **Stop-loss** | Stop Market Sell | $2,420.00 | Pending |
| **Take-profit** | Limit Sell | $2,600.00 | Pending |

New risk/reward is 1 : 5.0. Your bracket is live with the tighter stop. Just be aware of the higher stop-out probability given current volatility.
