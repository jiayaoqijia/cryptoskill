#!/usr/bin/env python3
"""
Impermanent Loss Calculator - Calculate IL for liquidity pool positions.

Pure math calculator (no API calls) that computes impermanent loss for
constant-product AMM liquidity pool positions at various price scenarios.
Shows dollar impact, hold vs LP comparison, break-even APY, and multi-scenario
analysis including net P&L with pool APY rewards.

Input (JSON via stdin):
Option 1 - Full calculation:
{
    "token_a_symbol": "ETH",
    "token_b_symbol": "USDC",
    "initial_price_a": 3000,
    "initial_price_b": 1,
    "current_price_a": 3500,
    "current_price_b": 1,
    "investment_usd": 10000,
    "pool_apy": 25.0,
    "holding_days": 180
}

Option 2 - Quick calculation:
{
    "price_change_pct": 20
}

Output (JSON via stdout):
{
    "success": true,
    "impermanent_loss": {...},
    "scenarios": [...],
    "with_apy": {...}
}
"""

import json
import sys
import math
from typing import Any, Dict, List, Optional, Tuple


# Default scenarios for multi-scenario analysis
DEFAULT_SCENARIOS = [-50, -30, -20, -10, -5, 5, 10, 20, 30, 50, 100, 200]

# Default investment amount for calculations
DEFAULT_INVESTMENT = 10000.0

# Default holding period in days
DEFAULT_HOLDING_DAYS = 365


def _safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert a value to float.

    Args:
        value: Value to convert.
        default: Default if conversion fails.

    Returns:
        Float value.
    """
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def calculate_il_from_ratio(price_ratio: float) -> float:
    """Calculate impermanent loss from a price ratio.

    Uses the constant-product AMM IL formula:
    IL = 2 * sqrt(price_ratio) / (1 + price_ratio) - 1

    Args:
        price_ratio: The ratio of new_price / old_price for the volatile asset.

    Returns:
        IL as a negative decimal (e.g., -0.0572 for 5.72% loss).
    """
    if price_ratio <= 0:
        return -1.0  # Total loss if price goes to zero

    sqrt_ratio = math.sqrt(price_ratio)
    il = 2 * sqrt_ratio / (1 + price_ratio) - 1
    return il


def calculate_il_from_prices(
    initial_price_a: float,
    initial_price_b: float,
    current_price_a: float,
    current_price_b: float,
) -> float:
    """Calculate IL from initial and current prices of both tokens.

    For a standard AMM LP with two tokens, IL depends on the relative price change
    of the two assets.

    Args:
        initial_price_a: Initial price of token A in USD.
        initial_price_b: Initial price of token B in USD.
        current_price_a: Current price of token A in USD.
        current_price_b: Current price of token B in USD.

    Returns:
        IL as a negative decimal.
    """
    if initial_price_a <= 0 or initial_price_b <= 0:
        return 0.0
    if current_price_a <= 0 or current_price_b <= 0:
        return -1.0

    # Calculate relative price change
    # Price ratio = (current_a / current_b) / (initial_a / initial_b)
    initial_relative = initial_price_a / initial_price_b
    current_relative = current_price_a / current_price_b
    price_ratio = current_relative / initial_relative

    return calculate_il_from_ratio(price_ratio)


def calculate_hold_value(
    investment_usd: float,
    initial_price_a: float,
    initial_price_b: float,
    current_price_a: float,
    current_price_b: float,
) -> float:
    """Calculate the value of simply holding both tokens (no LP).

    In a 50/50 LP, you start with equal value of each token.

    Args:
        investment_usd: Total investment in USD.
        initial_price_a: Initial price of token A.
        initial_price_b: Initial price of token B.
        current_price_a: Current price of token A.
        current_price_b: Current price of token B.

    Returns:
        Value of holding the tokens in USD.
    """
    if initial_price_a <= 0 or initial_price_b <= 0:
        return investment_usd

    half = investment_usd / 2.0
    amount_a = half / initial_price_a
    amount_b = half / initial_price_b

    value_a = amount_a * current_price_a
    value_b = amount_b * current_price_b

    return value_a + value_b


def calculate_lp_value(
    investment_usd: float,
    initial_price_a: float,
    initial_price_b: float,
    current_price_a: float,
    current_price_b: float,
) -> float:
    """Calculate the value of the LP position (affected by IL).

    For a constant-product AMM, the LP value is:
    LP_value = hold_value * (1 + IL)

    But more precisely:
    LP_value = investment * 2 * sqrt(price_ratio) / (1 + price_ratio)
    where price_ratio considers both token price changes.

    Args:
        investment_usd: Total initial investment.
        initial_price_a: Initial price of token A.
        initial_price_b: Initial price of token B.
        current_price_a: Current price of token A.
        current_price_b: Current price of token B.

    Returns:
        LP position value in USD.
    """
    hold_value = calculate_hold_value(
        investment_usd, initial_price_a, initial_price_b,
        current_price_a, current_price_b
    )
    il = calculate_il_from_prices(
        initial_price_a, initial_price_b,
        current_price_a, current_price_b
    )
    return hold_value * (1 + il)


def calculate_breakeven_apy(il_pct: float, holding_days: int = 365) -> float:
    """Calculate the minimum APY needed to offset impermanent loss.

    Args:
        il_pct: IL as a positive percentage (e.g., 5.72 for 5.72% loss).
        holding_days: Number of days holding the LP position.

    Returns:
        Minimum APY percentage needed to break even.
    """
    if il_pct <= 0:
        return 0.0
    if holding_days <= 0:
        return float("inf")

    # Annualize the IL
    annual_il = il_pct * (365.0 / holding_days)
    return round(annual_il, 2)


def calculate_apy_earnings(
    investment_usd: float,
    pool_apy: float,
    holding_days: int,
) -> float:
    """Calculate earnings from pool APY over holding period.

    Args:
        investment_usd: LP position value (simplified as constant).
        pool_apy: Annual percentage yield.
        holding_days: Days held.

    Returns:
        APY earnings in USD.
    """
    if pool_apy <= 0 or holding_days <= 0:
        return 0.0

    daily_rate = pool_apy / 100.0 / 365.0
    earnings = investment_usd * daily_rate * holding_days
    return round(earnings, 2)


def generate_scenario(
    price_change_pct: float,
    investment_usd: float,
    pool_apy: float = 0.0,
    holding_days: int = 365,
) -> Dict:
    """Generate IL analysis for a single price change scenario.

    Assumes token B is stable (price = 1) and token A changes by the given percentage.

    Args:
        price_change_pct: Price change of token A in percent (e.g., 50 for +50%).
        investment_usd: Total LP investment.
        pool_apy: Pool APY for net P&L calculation.
        holding_days: Days held.

    Returns:
        Scenario analysis dict.
    """
    price_ratio = 1.0 + (price_change_pct / 100.0)
    if price_ratio <= 0:
        price_ratio = 0.001  # Avoid division by zero

    il = calculate_il_from_ratio(price_ratio)
    il_pct = il * 100

    # Hold value: half in token A (which changed), half in token B (stable)
    hold_value = investment_usd * (0.5 * price_ratio + 0.5)
    lp_value = hold_value * (1 + il)
    il_dollar = lp_value - hold_value

    # APY earnings
    apy_earnings = calculate_apy_earnings(investment_usd, pool_apy, holding_days)
    net_pnl = (lp_value - investment_usd) + apy_earnings

    return {
        "price_change": f"{price_change_pct:+.0f}%",
        "price_ratio": round(price_ratio, 4),
        "il_pct": round(il_pct, 2),
        "il_dollar": round(il_dollar, 2),
        "hold_value": round(hold_value, 2),
        "lp_value": round(lp_value, 2),
        "lp_vs_hold": round(il_dollar, 2),
        "apy_earnings": round(apy_earnings, 2) if pool_apy > 0 else None,
        "net_pnl": round(net_pnl, 2) if pool_apy > 0 else round(lp_value - investment_usd, 2),
    }


def _validate_input(params: Dict) -> Tuple[Dict, Optional[str]]:
    """Validate and normalize input parameters.

    Args:
        params: Raw input parameters.

    Returns:
        Tuple of (normalized_params, error_string).
    """
    normalized = {}

    # Check if this is a quick calculation
    if "price_change_pct" in params and "initial_price_a" not in params:
        pct = _safe_float(params.get("price_change_pct"))
        if pct < -99:
            return {}, "price_change_pct must be greater than -99"
        if pct > 10000:
            return {}, "price_change_pct must be less than 10000"
        normalized["mode"] = "quick"
        normalized["price_change_pct"] = pct
        normalized["investment_usd"] = _safe_float(
            params.get("investment_usd", DEFAULT_INVESTMENT)
        )
        normalized["pool_apy"] = _safe_float(params.get("pool_apy", 0))
        normalized["holding_days"] = int(
            _safe_float(params.get("holding_days", DEFAULT_HOLDING_DAYS))
        )
        normalized["token_a_symbol"] = params.get("token_a_symbol", "TOKEN_A")
        normalized["token_b_symbol"] = params.get("token_b_symbol", "TOKEN_B")
        return normalized, None

    # Full calculation mode
    normalized["mode"] = "full"
    normalized["token_a_symbol"] = params.get("token_a_symbol", "TOKEN_A")
    normalized["token_b_symbol"] = params.get("token_b_symbol", "TOKEN_B")

    # Prices
    initial_a = _safe_float(params.get("initial_price_a"))
    initial_b = _safe_float(params.get("initial_price_b", 1.0))
    current_a = _safe_float(params.get("current_price_a"))
    current_b = _safe_float(params.get("current_price_b", 1.0))

    if initial_a <= 0:
        return {}, "initial_price_a must be a positive number"
    if initial_b <= 0:
        return {}, "initial_price_b must be a positive number"
    if current_a <= 0:
        return {}, "current_price_a must be a positive number"
    if current_b <= 0:
        return {}, "current_price_b must be a positive number"

    normalized["initial_price_a"] = initial_a
    normalized["initial_price_b"] = initial_b
    normalized["current_price_a"] = current_a
    normalized["current_price_b"] = current_b

    # Investment
    normalized["investment_usd"] = _safe_float(
        params.get("investment_usd", DEFAULT_INVESTMENT)
    )
    if normalized["investment_usd"] <= 0:
        return {}, "investment_usd must be positive"

    # APY and holding period
    normalized["pool_apy"] = _safe_float(params.get("pool_apy", 0))
    if normalized["pool_apy"] < 0:
        return {}, "pool_apy must be non-negative"

    normalized["holding_days"] = int(
        _safe_float(params.get("holding_days", DEFAULT_HOLDING_DAYS))
    )
    if normalized["holding_days"] <= 0:
        return {}, "holding_days must be positive"

    # Custom scenarios
    custom_scenarios = params.get("scenarios")
    if custom_scenarios and isinstance(custom_scenarios, list):
        normalized["scenarios"] = [_safe_float(s) for s in custom_scenarios]
    else:
        normalized["scenarios"] = DEFAULT_SCENARIOS

    return normalized, None


def calculate_full(params: Dict) -> Dict:
    """Perform full IL calculation with two token prices.

    Args:
        params: Validated input parameters.

    Returns:
        Result dict.
    """
    token_a = params["token_a_symbol"]
    token_b = params["token_b_symbol"]
    init_a = params["initial_price_a"]
    init_b = params["initial_price_b"]
    curr_a = params["current_price_a"]
    curr_b = params["current_price_b"]
    investment = params["investment_usd"]
    pool_apy = params["pool_apy"]
    holding_days = params["holding_days"]

    # Calculate IL
    il = calculate_il_from_prices(init_a, init_b, curr_a, curr_b)
    il_pct = il * 100

    # Calculate values
    hold_value = calculate_hold_value(investment, init_a, init_b, curr_a, curr_b)
    lp_value = calculate_lp_value(investment, init_a, init_b, curr_a, curr_b)
    il_dollar = lp_value - hold_value

    # Price change percentage
    price_change_a = ((curr_a - init_a) / init_a) * 100
    price_change_b = ((curr_b - init_b) / init_b) * 100

    # Break-even APY
    breakeven_apy = calculate_breakeven_apy(abs(il_pct), holding_days)

    # Build main result
    result = {
        "success": True,
        "input": {
            "token_a": token_a,
            "token_b": token_b,
            "initial_price_a": init_a,
            "initial_price_b": init_b,
            "current_price_a": curr_a,
            "current_price_b": curr_b,
            "price_change_a_pct": round(price_change_a, 2),
            "price_change_b_pct": round(price_change_b, 2),
            "investment_usd": investment,
        },
        "impermanent_loss": {
            "il_percentage": round(il_pct, 4),
            "il_dollar_amount": round(il_dollar, 2),
            "hold_value": round(hold_value, 2),
            "lp_value": round(lp_value, 2),
            "lp_vs_hold_difference": round(il_dollar, 2),
            "breakeven_apy": breakeven_apy,
        },
        "explanation": _generate_explanation(
            token_a, token_b, il_pct, il_dollar, hold_value, lp_value, breakeven_apy
        ),
    }

    # Generate scenarios based on token A price changes (keeping token B stable)
    scenarios = []
    for pct in params.get("scenarios", DEFAULT_SCENARIOS):
        # Calculate the relative price ratio change
        relative_ratio = 1.0 + (pct / 100.0)
        if relative_ratio <= 0:
            continue
        scenario_il = calculate_il_from_ratio(relative_ratio)
        scenario_il_pct = scenario_il * 100

        # For the scenario: token A changes by pct%, token B stays same
        scenario_hold = investment * (0.5 * relative_ratio + 0.5)
        scenario_lp = scenario_hold * (1 + scenario_il)
        scenario_il_dollar = scenario_lp - scenario_hold

        apy_earnings = calculate_apy_earnings(investment, pool_apy, holding_days)
        scenario_net = (scenario_lp - investment) + apy_earnings

        scenarios.append({
            "price_change": f"{pct:+.0f}%",
            f"{token_a}_price": round(init_a * relative_ratio, 2),
            "il_pct": f"{scenario_il_pct:.2f}%",
            "il_dollar": round(scenario_il_dollar, 2),
            "hold_value": round(scenario_hold, 2),
            "lp_value": round(scenario_lp, 2),
            "net_pnl": round(scenario_net, 2) if pool_apy > 0 else round(scenario_lp - investment, 2),
        })

    result["scenarios"] = scenarios

    # APY analysis
    if pool_apy > 0:
        apy_earnings = calculate_apy_earnings(investment, pool_apy, holding_days)
        net_pnl = (lp_value - investment) + apy_earnings
        result["with_apy"] = {
            "pool_apy": pool_apy,
            "holding_days": holding_days,
            "apy_earnings": apy_earnings,
            "il_cost": round(abs(il_dollar), 2),
            "net_pnl": round(net_pnl, 2),
            "profitable": net_pnl > 0,
            "effective_apy": round(
                ((net_pnl / investment) * (365.0 / holding_days)) * 100, 2
            ),
        }
        if net_pnl > 0:
            result["with_apy"]["summary"] = (
                f"Despite {abs(il_pct):.2f}% IL (${abs(il_dollar):.2f}), the {pool_apy}% "
                f"APY earns ${apy_earnings:.2f} over {holding_days} days, "
                f"resulting in net profit of ${net_pnl:.2f}"
            )
        else:
            result["with_apy"]["summary"] = (
                f"The {abs(il_pct):.2f}% IL (${abs(il_dollar):.2f}) exceeds the "
                f"${apy_earnings:.2f} earned from {pool_apy}% APY over {holding_days} days, "
                f"resulting in net loss of ${abs(net_pnl):.2f}"
            )

    return result


def calculate_quick(params: Dict) -> Dict:
    """Perform quick IL calculation from a price change percentage.

    Args:
        params: Validated input parameters with price_change_pct.

    Returns:
        Result dict.
    """
    pct = params["price_change_pct"]
    investment = params["investment_usd"]
    pool_apy = params["pool_apy"]
    holding_days = params["holding_days"]
    token_a = params["token_a_symbol"]
    token_b = params["token_b_symbol"]

    price_ratio = 1.0 + (pct / 100.0)
    if price_ratio <= 0:
        price_ratio = 0.001

    il = calculate_il_from_ratio(price_ratio)
    il_pct = il * 100

    # Hold value: half in volatile (changed), half in stable
    hold_value = investment * (0.5 * price_ratio + 0.5)
    lp_value = hold_value * (1 + il)
    il_dollar = lp_value - hold_value

    breakeven_apy = calculate_breakeven_apy(abs(il_pct), holding_days)

    result = {
        "success": True,
        "input": {
            "price_change_pct": pct,
            "investment_usd": investment,
            "token_a": token_a,
            "token_b": token_b,
        },
        "impermanent_loss": {
            "il_percentage": round(il_pct, 4),
            "il_dollar_amount": round(il_dollar, 2),
            "hold_value": round(hold_value, 2),
            "lp_value": round(lp_value, 2),
            "lp_vs_hold_difference": round(il_dollar, 2),
            "breakeven_apy": breakeven_apy,
        },
    }

    # Generate scenarios
    scenarios = []
    for s_pct in DEFAULT_SCENARIOS:
        scenario = generate_scenario(s_pct, investment, pool_apy, holding_days)
        scenarios.append(scenario)

    result["scenarios"] = scenarios

    # APY analysis
    if pool_apy > 0:
        apy_earnings = calculate_apy_earnings(investment, pool_apy, holding_days)
        net_pnl = (lp_value - investment) + apy_earnings
        result["with_apy"] = {
            "pool_apy": pool_apy,
            "holding_days": holding_days,
            "apy_earnings": apy_earnings,
            "il_cost": round(abs(il_dollar), 2),
            "net_pnl": round(net_pnl, 2),
            "profitable": net_pnl > 0,
        }

    return result


def _generate_explanation(
    token_a: str,
    token_b: str,
    il_pct: float,
    il_dollar: float,
    hold_value: float,
    lp_value: float,
    breakeven_apy: float,
) -> str:
    """Generate a human-readable explanation of the IL result.

    Args:
        token_a: Token A symbol.
        token_b: Token B symbol.
        il_pct: IL percentage.
        il_dollar: IL dollar amount.
        hold_value: Hold strategy value.
        lp_value: LP strategy value.
        breakeven_apy: Minimum APY to break even.

    Returns:
        Explanation string.
    """
    if abs(il_pct) < 0.01:
        return (
            f"No meaningful impermanent loss. The {token_a}/{token_b} price ratio "
            f"has not changed significantly."
        )

    direction = "loss" if il_dollar < 0 else "gain"
    parts = [
        f"Providing liquidity for {token_a}/{token_b} results in an impermanent "
        f"{direction} of {abs(il_pct):.2f}% (${abs(il_dollar):.2f}).",
        f"Holding the tokens would be worth ${hold_value:.2f}, while the LP position "
        f"is worth ${lp_value:.2f}.",
    ]

    if breakeven_apy > 0 and il_dollar < 0:
        parts.append(
            f"You would need at least {breakeven_apy:.2f}% APY to offset this "
            f"impermanent loss."
        )

    if abs(il_pct) < 1:
        parts.append("This is a relatively small IL, common for minor price movements.")
    elif abs(il_pct) < 5:
        parts.append("This is a moderate IL. Many active LP pools can offset this with fees.")
    elif abs(il_pct) < 10:
        parts.append("This is significant IL. Ensure pool APY exceeds the break-even threshold.")
    else:
        parts.append(
            "This is severe IL. Consider whether the pool's APY truly compensates "
            "for this level of loss."
        )

    return " ".join(parts)


def main() -> None:
    """Entry point: read JSON from stdin, process, write JSON to stdout."""
    try:
        raw_input = sys.stdin.read().strip()
        if not raw_input:
            params = {}
        else:
            params = json.loads(raw_input)
    except json.JSONDecodeError as e:
        result = {
            "success": False,
            "error": f"Invalid JSON input: {str(e)}",
            "usage": {
                "full_calc": {
                    "token_a_symbol": "ETH",
                    "token_b_symbol": "USDC",
                    "initial_price_a": 3000,
                    "current_price_a": 3500,
                    "investment_usd": 10000,
                    "pool_apy": 25.0,
                },
                "quick_calc": {
                    "price_change_pct": 20,
                },
            },
        }
        print(json.dumps(result, indent=2))
        return

    if not isinstance(params, dict):
        result = {"success": False, "error": "Input must be a JSON object"}
        print(json.dumps(result, indent=2))
        return

    # Handle empty input with helpful message
    if not params:
        result = {
            "success": False,
            "error": "No parameters provided",
            "usage": {
                "description": "Calculate impermanent loss for LP positions",
                "full_calc": {
                    "token_a_symbol": "ETH",
                    "token_b_symbol": "USDC",
                    "initial_price_a": 3000,
                    "initial_price_b": 1,
                    "current_price_a": 3500,
                    "current_price_b": 1,
                    "investment_usd": 10000,
                    "pool_apy": 25.0,
                    "holding_days": 180,
                },
                "quick_calc": {
                    "price_change_pct": 50,
                },
            },
        }
        print(json.dumps(result, indent=2))
        return

    # Validate input
    validated, error = _validate_input(params)
    if error:
        result = {"success": False, "error": f"Input validation failed: {error}"}
        print(json.dumps(result, indent=2))
        return

    # Run appropriate calculation mode
    if validated["mode"] == "quick":
        result = calculate_quick(validated)
    else:
        result = calculate_full(validated)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
