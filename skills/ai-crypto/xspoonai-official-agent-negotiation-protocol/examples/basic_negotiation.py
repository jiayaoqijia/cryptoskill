#!/usr/bin/env python3
"""
Basic Negotiation Example — Minimal usage of the Agent Negotiation Protocol.

Demonstrates a simple buyer-seller negotiation with default settings.
"""

import asyncio
import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from negotiation_engine import NegotiationEngine, NegotiationStatus


async def main() -> None:
    """Run a basic negotiation between two agents."""
    engine = NegotiationEngine(max_rounds=5)

    result = await engine.run_negotiation(
        buyer_intent="On-chain data analysis for 100 wallets",
        seller_capability="Batch wallet profiling service",
        buyer_budget=50.0,
        seller_base_price=80.0,
    )

    print(f"Status:       {result.status.value}")
    print(f"Agreed Price: ${result.agreed_price}" if result.agreed_price else "Agreed Price: N/A")
    print(f"Agreed SLA:   {result.agreed_sla or 'N/A'}")
    print(f"Rounds:       {result.rounds_taken}")

    for entry in result.history:
        role = entry.get("role", "?")
        rnd = entry.get("round", "?")
        action = entry.get("action", "?")
        price = entry.get("price", "?")
        print(f"  [Round {rnd}] {role:>15} | {action:<8} | ${price}")


if __name__ == "__main__":
    asyncio.run(main())
