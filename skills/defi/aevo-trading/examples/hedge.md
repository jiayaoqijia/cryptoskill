# Example: Portfolio Hedge

Analyzing portfolio risk and executing a hedge to reduce directional exposure. Shows the full workflow from risk identification through hedge execution.

---

**User**: I'm feeling overexposed. Can you check my portfolio and suggest a hedge?

**Assistant**: Let me pull up your positions and run a full risk analysis.

*[calls in parallel: aevo_get_positions(), aevo_portfolio_risk()]*

Here's your current portfolio:

**Positions**:
| Instrument | Side | Size | Entry Price | Mark Price | Unrealized PnL |
|---|---|---|---|---|---|
| ETH-PERP | Long | 2.0 ETH | $2,380.00 | $2,455.00 | +$150.00 |
| ETH-28MAR25-3000-C | Long | 5 contracts | $82.00 | $95.50 | +$67.50 |
| BTC-PERP | Long | 0.05 BTC | $66,800 | $67,240 | +$22.00 |

**Aggregate Risk**:
| Metric | Value |
|---|---|
| **Total notional** | $8,272 |
| **Net delta (ETH-equivalent)** | +3.8 ETH (~$9,329 delta exposure) |
| **Net gamma** | +0.0012 |
| **Net vega** | +$42.00 |
| **Margin utilization** | 34% |
| **Session PnL** | +$239.50 |

**Risk Assessment**: You're significantly long delta on ETH — between the perp and the calls, you have about 3.8 ETH of directional exposure. The BTC perp adds a small correlated long on top. Your portfolio will lose roughly $380 for every 1% drop in ETH.

Let me check the volatility environment to determine the best hedging approach.

*[calls aevo_volatility_snapshot(asset="ETH")]*

**Vol Context**: ATM IV is 58%, RV is 52%. IV is slightly elevated. This matters because:
- Buying puts is somewhat expensive right now (you'd be buying rich vol)
- Selling the perp is delta-neutral and vol-agnostic

**Hedge Options**:

| Strategy | Instrument | Cost | Effect |
|---|---|---|---|
| **A. Short perp** | Sell 1.5 ETH-PERP | No premium (margin only) | Reduces net delta to ~2.3 ETH. Clean, simple, no time decay. |
| **B. Buy puts** | Buy 5x ETH-28MAR25-2300-P | ~$155 premium | Adds downside protection below $2,300. Keeps upside intact. But IV is rich, so you overpay slightly. |
| **C. Collar** | Sell 5x ETH-28MAR25-2800-C + Buy 5x ETH-28MAR25-2200-P | ~$20 net credit | Caps upside at $2,800 but gives free downside protection below $2,200. |

My recommendation: **Option A (short perp)** is the cleanest hedge if you just want to reduce delta. If you want to keep the upside but add crash protection, **Option C (collar)** is cost-effective since IV is elevated — you collect more from selling calls.

Which approach interests you, or would you like me to model a different hedge?

---

**User**: Let's go with the collar. Can you build it out?

**Assistant**: Let me build the collar legs and show you the full picture.

*[calls aevo_get_expiries(asset="ETH")]*

Using the 28MAR25 expiry to match your existing calls. Let me construct the legs.

*[calls aevo_options_leg_builder(strategy_type="collar", asset="ETH", expiry="28MAR25", long_put_strike=2200, short_call_strike=2800, quantity=5)]*

Here's the collar breakdown:

**Collar: ETH 28MAR25**

| Leg | Instrument | Side | Size | Price | Cost |
|---|---|---|---|---|---|
| Short call | ETH-28MAR25-2800-C | Sell | 5 | $48.20 | +$241.00 (credit) |
| Long put | ETH-28MAR25-2200-P | Buy | 5 | $44.30 | -$221.50 (debit) |
| | | | | **Net** | **+$19.50 credit** |

**Post-Hedge Risk Profile**:

| Metric | Before | After |
|---|---|---|
| **Net delta** | +3.8 ETH | +3.2 ETH |
| **Net gamma** | +0.0012 | +0.0008 |
| **Net vega** | +$42.00 | +$18.00 |
| **Downside protection** | None | Floor at $2,200 (5 contracts) |
| **Upside cap** | Unlimited | Capped at $2,800 (5 contracts) |
| **Max portfolio loss (to expiry)** | Theoretically unlimited | Limited below $2,200 |

**Scenario Analysis**:
- ETH at $2,200 (-10%): Portfolio loses ~$485, but puts kick in below $2,200 limiting further loss
- ETH at $2,450 (flat): Net +$19.50 from collar premium, positions unchanged
- ETH at $2,800 (+14%): Portfolio gains ~$1,330, but gains above $2,800 are capped by the short calls

The collar costs you essentially nothing ($19.50 net credit) and gives you a floor at $2,200. The tradeoff is your upside is capped at $2,800 on the hedged portion.

**Shall I execute this collar?**

---

**User**: Looks good. Execute it.

**Assistant**: Executing the collar now.

*[calls aevo_risk_check(instrument_name="ETH-28MAR25-2800-C", side="sell", amount=5, price=48.20)]*

Risk check passed on the short call leg.

*[calls aevo_risk_check(instrument_name="ETH-28MAR25-2200-P", side="buy", amount=5, price=44.30)]*

Risk check passed on the long put leg. Placing both orders.

*[calls aevo_create_order(instrument_name="ETH-28MAR25-2800-C", side="sell", amount=5, limit_price=48.20)]*

*[calls aevo_create_order(instrument_name="ETH-28MAR25-2200-P", side="buy", amount=5, limit_price=44.30)]*

Both legs submitted. Let me verify.

*[calls aevo_list_orders()]*

**Execution confirmed**:

| Leg | Status | Fill Price |
|---|---|---|
| Sell 5x ETH-28MAR25-2800-C | Filled | $48.20 |
| Buy 5x ETH-28MAR25-2200-P | Filled | $44.30 |

Net credit received: **$19.50**

Your collar is live. Here's your updated portfolio:

| Instrument | Side | Size |
|---|---|---|
| ETH-PERP | Long | 2.0 ETH |
| ETH-28MAR25-3000-C | Long | 5 contracts |
| ETH-28MAR25-2800-C | Short | 5 contracts |
| ETH-28MAR25-2200-P | Long | 5 contracts |
| BTC-PERP | Long | 0.05 BTC |

Your downside is now protected below $2,200 on the options portion. You still have uncapped upside on the ETH perp, and the BTC perp is a small position. Overall margin utilization is at 38%.

Want me to also hedge the BTC exposure, or are you comfortable with that position?
