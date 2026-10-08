---
name: cost-a-product-from-its-inputs
description: Use when you must price a physical product or a billable service and have no defensible unit cost yet. Builds the per-unit cost from every input line, keeps variable and allocated cost apart, and holds every amount in exact minor units.
---

# Cost a product from its inputs

A price is a guess until you can name the cost of one more unit. Build the unit cost from the bill of materials and the labour and freight lines that actually scale with output, keep the money in integer cents, and only then choose where the price sits.

## Procedure

1. Freeze the unit of account: one finished unit — one candle, one seat-month, one delivered report. Every cost below attaches to exactly that unit.
2. List the variable inputs that rise with volume: materials, direct labour, packaging, fulfilment, payment fees. Leave rent and salaried staff for the allocation step.
3. Cost materials at the price you will actually pay this quarter, not last year's invoice. Wax at $8.40/kg, 300 g per unit:

       ```
       python3 -c "from decimal import Decimal as D; print(D('8.40')*D('0.300'))"
       # 2.520  -> $2.52 of wax per unit
       ```

4. Convert labour time to a loaded rate: 6 minutes at $24.00/hour is `D('24')*6/60 = D('2.40')`.
5. Add packaging and freight per unit, and divide any per-order fee by units per order: a $0.30 payment fee is $0.30 on a 1-unit order and $0.075 on a 4-unit order.
6. Sum the variable block: 2.52 wax + 0.09 wick + 1.30 jar + 0.12 label + 2.40 labour + 0.55 pack + 0.18 freight-in = **$7.16 per unit**.
7. Allocate fixed cost separately and label it as allocated, not variable: $3,000/month over 4,000 units is $0.75 per unit.
8. For materials with duties or freight-in, add them here; they are per-unit variable and are the line most often left out.
9. Report the two numbers apart — variable unit cost $7.16 and fully-loaded unit cost $7.91 — because only the first is a floor for the decision in `set-a-minimum-viable-price-floor`.
10. Keep every amount an integer minor unit in the build sheet: `amount_minor=716`. Never `float`; a run of float products drifts by cents that surface at invoicing.
11. Re-cost when any input moves more than a set threshold, say 10%. A stale BOM is the usual cause of a price that quietly lost its margin.

## Pitfalls

- Costing the prototype rather than the production unit; the first build is always dearer and anchors the price too high.
- Omitting freight-in and duties on materials, which are variable and belong in step 8.
- Treating allocated rent as a variable cost, so the "floor" includes cost that one more unit does not cause.
- Using last year's material price, so a 15% input move silently erases the margin.
- Averaging labour across the whole team instead of the loaded rate of the role that does the work.
- Leaving an amount as a float, so a 3-decimal unit cost drifts when multiplied across a large order.

## Verification

    ```
    python3 -c "from decimal import Decimal as D; print(D('7.16')*D('1000'))"
    # 7160.00 exact; a float 7.16*1000 drifts off the cent
    ```

Pass when the build sheet shows integer minor units and both unit costs. Report the variable unit cost and the fully-loaded unit cost separately, with the price and rate inputs behind them.
