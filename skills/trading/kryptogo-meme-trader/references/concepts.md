# Core Concepts

## 1. Wallet Clustering

A **cluster** is a group of wallets controlled by the same entity -- a market maker, trading team, or token operator. These wallets appear independent on-chain but are algorithmically linked through:

1. **Fund flow correlation** -- money flowing between addresses
2. **Same fund source** -- addresses receiving initial funding from the same origin
3. **Close withdrawal timing** -- addresses making withdrawals within similar timeframes
4. **Same-transaction binding** -- addresses tied to the same transaction (bundle buys)
5. **Multi-sig patterns** -- shared governance structures

**Why clustering matters:** Market manipulators spread holdings across dozens or hundreds of addresses. Tracking a single whale address misses the complete picture. Cluster analysis reveals the **total capital layout** of an entity.

**Key metric -- Cluster Holding Ratio:** The percentage of total token supply held by all identified clusters combined.
- **>=30-35%** = Token is "controlled" -- a major entity holds significant supply
- **>=50%** = Highly concentrated -- high manipulation risk but also high upside if accumulating
- **<10%** = Dispersed -- no clear major holder, likely retail-driven

**Scam detection rule:** If a **single cluster** controls more than **50% of total token supply**, this is a strong indicator of a scam or rug pull token. Avoid trading these unless you have extremely compelling reasons. The operator can dump the token at any time and drain liquidity.

## 2. Address Labels (3-Layer Model)

Every wallet is classified by on-chain behavior using a **3-layer model** ordered by cost basis (lowest to highest). Labels appear across all analysis responses and are critical for interpreting holder intent.

### Layer 1 -- Lowest-Cost Tokens (Sell Pressure Risk)

These addresses hold the cheapest tokens and pose the highest sell pressure risk. **Check these first -- if they haven't cleared, upside is capped.**

| Label | Threshold | What It Means |
|-------|-----------|---------------|
| **Developer** | Deployed the token + associated wallets | Core team addresses with lowest cost basis. If still holding large amounts = high dump risk. KryptoGO tracks multi-layer addresses linked to the deployer. |
| **Sniper** | Bought within 1 second of creation | Holds the absolute lowest-cost tokens. If NOT cleared = strong sell pressure overhead. |

### Layer 2 -- Manipulation Indicators (Operation Signals)

These labels indicate organized manipulation or short-term speculation. **High proportion = artificial activity, not genuine market interest.**

| Label | Threshold | What It Means |
|-------|-----------|---------------|
| **New Wallet** | Created within 24h before token deployment | Likely pre-prepared operation addresses. Batch-created for distributed manipulation. |
| **Bundle Transaction** | Multiple addresses buying in the same tx | Team operation pattern -- multiple small wallets eating internal orders at extremely low cost. |
| **High-Frequency** | Median hold < 12 hours | Short-term speculators. High proportion = unstable trend, likely just a hot spot. |

### Layer 3 -- Trend Direction (Smart Capital)

These are the most informative labels for trend prediction. **Their behavior indicates where experienced capital is flowing.**

| Label | Threshold | What It Means |
|-------|-----------|---------------|
| **Smart Money** | Realized profit > $100K | Consistently profitable traders. Their accumulation often precedes major price moves. |
| **Blue-Chip Profit** | Profit > $100K on tokens that peaked > $10M mcap | Long-term trend traders who catch main waves. KryptoGO re-parses Jupiter limit orders, DCA buys, and split orders to restore accurate cost basis. |
| **Whale** | Single-token position > $100K | Large capital holders. A whale cluster does not equal just "big holder" -- it could be an operating team or cross-market operator. |

## 3. Accumulation vs Distribution

The core analytical question: **Is the major holder buying or selling?**

**Accumulation:**
- Cluster holding % is **rising** while price is consolidating or pulling back
- Smart money / whale clusters are increasing positions
- Developer and sniper positions have been **cleared** (reduced sell pressure)
- New fund inflow approximately equals market cap times cluster holding % increase

**Distribution:**
- Price is **rising** but cluster holding % is **declining** -- major holder selling into strength
- Smart money holdings decreasing -- entering harvest phase
- Blue-chip profit wallets distributing en masse -- often signals end of main price wave
- Signal triggered but cluster % quickly drops back -- possible bull trap

**Key insight: Price and cluster holdings DIVERGING is the most important signal.** Rising price + falling cluster % = distribution. Falling price + rising cluster % = accumulation.

## 4. The "Other Holders" Survivorship Bias

The `/analyze-token` response includes `other_top_holders` -- top 200 non-cluster addresses. **Be careful**: this list only shows CURRENT holders. Addresses that sold and left are not shown, creating a survivorship bias where "other holders" appear bullish even when many have actually exited.

Cluster data is more reliable because it tracks the complete entity across all its addresses.
