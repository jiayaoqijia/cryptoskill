#!/usr/bin/env python3
"""
Custom Strategy Example — Demonstrates how to customize negotiation parameters.

Shows how to:
  1. Pre-check ZOPA feasibility before negotiation
  2. Use custom concession rates
  3. Integrate x402 settlement after agreement
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from negotiation_engine import (
    NegotiationEngine,
    NegotiationStatus,
    CONCESSION_RATE_BUYER,
    CONCESSION_RATE_SELLER,
)
from x402_settlement import X402Settlement


def check_zopa_feasibility(
    buyer_budget: float,
    seller_base_price: float,
    max_rounds: int,
    buyer_rate: float = CONCESSION_RATE_BUYER,
    seller_rate: float = CONCESSION_RATE_SELLER,
) -> bool:
    """
    Pre-check whether a Zone of Possible Agreement (ZOPA) can exist.

    Returns True if buyer's ceiling can reach seller's floor within max_rounds.
    """
    for n in range(1, max_rounds + 1):
        buyer_ceiling = buyer_budget * (1 + buyer_rate * (n - 1))
        seller_floor = seller_base_price * (1 - seller_rate * (n - 1))
        if buyer_ceiling >= seller_floor:
            print(f"  ZOPA possible at round {n}: "
                  f"buyer ceiling=${buyer_ceiling:.2f} >= seller floor=${seller_floor:.2f}")
            return True
    print(f"  No ZOPA within {max_rounds} rounds")
    return False


async def negotiate_with_settlement() -> None:
    """Run negotiation with ZOPA pre-check and x402 settlement."""
    buyer_budget = 60.0
    seller_base_price = 90.0
    max_rounds = 5

    print("=" * 50)
    print("  Custom Strategy Negotiation")
    print("=" * 50)

    # Layer 1: Pre-check ZOPA feasibility
    print("\n[Layer 1] ZOPA Feasibility Check:")
    if not check_zopa_feasibility(buyer_budget, seller_base_price, max_rounds):
        print("Aborting: no agreement possible with current parameters.")
        return

    # Layer 2: Run negotiation
    print("\n[Layer 2] Running Negotiation:")
    engine = NegotiationEngine(max_rounds=max_rounds)
    result = await engine.run_negotiation(
        buyer_intent="Smart contract security audit for DeFi protocol",
        seller_capability="Automated + manual security analysis, supports Solidity/Vyper",
        buyer_budget=buyer_budget,
        seller_base_price=seller_base_price,
    )

    print(f"  Status: {result.status.value}")
    print(f"  Price:  ${result.agreed_price}" if result.agreed_price else "  Price:  N/A")
    print(f"  Rounds: {result.rounds_taken}")

    # Layer 3: Settlement (only if agreed)
    if result.status == NegotiationStatus.AGREED and result.agreed_price:
        print("\n[Layer 3] x402 Settlement:")
        settlement = X402Settlement()
        tx = await settlement.execute_settlement(
            agreed_price=result.agreed_price,
            buyer_id="agent-buyer-defi",
            seller_id="agent-seller-audit",
            sla_tier=result.agreed_sla or "standard",
        )
        print(f"  TX Hash:           {tx.tx_hash}")
        print(f"  Status:            {tx.status}")
        print(f"  Buyer Reputation:  {tx.buyer_reputation_after:.2f}")
        print(f"  Seller Reputation: {tx.seller_reputation_after:.2f}")
    else:
        print("\n[Layer 3] No settlement — negotiation did not reach agreement.")

    print(f"\n{'=' * 50}")


if __name__ == "__main__":
    asyncio.run(negotiate_with_settlement())
