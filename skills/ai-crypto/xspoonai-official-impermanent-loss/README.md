# Impermanent Loss Calculator Skill

Liquidity Providing (LPing) is risky. The **Impermanent Loss Calculator** gives SpoonOS agents the ability to mathematically assess that risk, ensuring they don't lose value relative to just holding ("HODLing") the tokens.

## Features

- **divergence_loss**: Calculates loss percentage based on price ratio change.
- **break_even**: Calculates required APY/Fees to offset the loss.
- **multi_scenario**: Can output a table of potential outcomes (e.g., if price goes up 10%, 20%, 50%).

## Usage

### Parameters

- `price_ratio` (float): The new price ratio vs old price ratio (e.g., 1.5 = 50% increase).
- `initial_value` (float, optional): Initial investment value in USD (default 1000).

### formulas

$$ IL = 2 \cdot \frac{\sqrt{P\_ratio}}{1 + P\_ratio} - 1 $$

### Example Agent Prompts

> "Calculate impermanent loss if ETH goes from $2000 to $3000."
> "Is it safe to LP if I expect 20% volatility?"

### Output

```json
{
  "price_change": "50.0%",
  "impermanent_loss_percent": -2.02,
  "value_if_held": 1250.00,
  "value_in_pool": 1224.74
}
```
