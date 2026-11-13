---
name: american-exercise
domain: investing/american-exercise
trigger: "Handling early exercise and assignment on a commodity option."
anti_trigger: "Not for European option theory, and not for delivery mechanics."
scope: "Early exercise, assignment into a futures position, and the resulting margin."
status: seedling
---

# American exercise

## Standard

Most commodity options are American: the holder may exercise at any time before expiry. Exercise delivers a futures position at the strike, and the position is marked to market immediately, which means an exercise can create a margin requirement the holder had not planned for.

The early-exercise decision is not usually about the intrinsic value alone. Exercising early forfeits the remaining time value and, in a future that is trading at a premium or discount to spot, changes which price the holder actually pays. For deep in-the-money options the early exercise becomes economically rational when the value of the futures position exceeds the option's market price, and that calculation depends on the cost of carry and on the future's basis.

Primary sources: <https://www.cmegroup.com/> and <https://www.cftc.gov/>.

## Decision rules

- Record the exercise style and any notice cut-off time.
- Record the option's market price against its intrinsic value before deciding.
- Record the resulting futures position, its margin, and its notice dates.
- Record the basis between the future delivered and the spot price.
- Record the assignment risk for short positions, and the plan if assigned.
- Record the funding available to meet margin on an exercise.

## Procedure

1. Record exercise style and cut-off.
2. Compare the option price with intrinsic value.
3. Compute the futures position and its margin.
4. Check the notice dates of the delivered future.
5. Decide exercise, sell, or let expire, and record the reason.
6. Record the funding plan for a margin call.

## Anti-patterns

- Exercising because the option is in the money, without comparing prices.
- Ignoring the margin the delivered future requires.
- Forgetting that assignment can arrive on a short before expiry.
- Treating the exercise price as the price paid for the physical good.
- Assuming the position can be closed before the notice day.

## Done checklist

- [ ] Exercise style and cut-off recorded.
- [ ] Price versus intrinsic compared.
- [ ] Delivered future and margin computed.
- [ ] Notice dates checked.
- [ ] Decision and reason recorded.
- [ ] Funding plan written.

The early-exercise decision also depends on the future's liquidity: exercising into a contract that trades thinly creates a position that is harder to close than the option was to hold, and the option's price may already reflect that discount, so the comparison must be made against the executable price rather than the screen price.


## Sources

- Exchange exercise rules and specifications: <https://www.cmegroup.com/>
- Regulatory guidance: <https://www.cftc.gov/>
- Investor education on options: <https://www.investor.gov/introduction-investing>
