#!/usr/bin/env python3
"""
Agent Negotiation Engine — StateGraph-based multi-round negotiation state machine.

Implements automated negotiation between buyer and seller agents using
SpoonOS StateGraph for workflow orchestration and Qwen LLM for decision-making.

Author: bonujel
Version: 1.0.0
"""

from __future__ import annotations

import json
import os
import time
import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, TypedDict

import httpx
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_NEGOTIATION_ROUNDS = 5
CONCESSION_RATE_BUYER = 0.15   # Buyer concedes up to 15% per round
CONCESSION_RATE_SELLER = 0.12  # Seller concedes up to 12% per round


# ---------------------------------------------------------------------------
# Qwen LLM Client
# ---------------------------------------------------------------------------

class QwenClient:
    """Lightweight async client for DashScope (Qwen) chat completions."""

    BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

    def __init__(self) -> None:
        self.api_key = os.getenv("DASHSCOPE_API_KEY", "")
        self.model = os.getenv("QWEN_MODEL", "qwen-plus")
        if not self.api_key:
            raise EnvironmentError(
                "DASHSCOPE_API_KEY is not set. "
                "Get one at https://dashscope.console.aliyun.com/apiKey"
            )

    async def chat(self, system_prompt: str, user_prompt: str) -> str:
        """Send a chat completion request and return the assistant message."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.7,
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(self.BASE_URL, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]


# Module-level lazy singleton — avoids re-creating QwenClient per node call.
_qwen_client: QwenClient | None = None


def _get_qwen_client() -> QwenClient:
    """Return a cached QwenClient instance (created once on first call)."""
    global _qwen_client
    if _qwen_client is None:
        _qwen_client = QwenClient()
    return _qwen_client


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

class NegotiationStatus(str, Enum):
    """Possible outcomes of a negotiation session."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    AGREED = "agreed"
    REJECTED = "rejected"
    TIMEOUT = "timeout"


@dataclass(frozen=True)
class Proposal:
    """An immutable negotiation proposal from one party."""
    price: float
    sla_tier: str          # "basic" | "standard" | "premium"
    delivery_hours: int
    reasoning: str
    round_number: int


@dataclass(frozen=True)
class NegotiationResult:
    """Final outcome of a negotiation session."""
    status: NegotiationStatus
    agreed_price: float | None
    agreed_sla: str | None
    rounds_taken: int
    buyer_initial: float
    seller_initial: float
    history: list[dict[str, Any]]
    tx_hash: str | None = None


class NegotiationState(TypedDict, total=False):
    """StateGraph workflow state for the negotiation process."""
    # Participant info
    buyer_intent: str
    seller_capability: str
    buyer_budget: float
    seller_base_price: float
    # Negotiation tracking
    current_round: int
    max_rounds: int
    status: str
    # Proposals
    buyer_proposal: dict[str, Any] | None
    seller_proposal: dict[str, Any] | None
    # History & result
    history: list[dict[str, Any]]
    final_result: dict[str, Any] | None


# ---------------------------------------------------------------------------
# LLM Prompt Templates
# ---------------------------------------------------------------------------

BUYER_SYSTEM_PROMPT = """\
You are a buyer agent negotiating to purchase a service.
Your goal: get the best price while ensuring quality.
You must respond with ONLY a valid JSON object (no markdown, no explanation).

JSON format:
{
  "action": "propose" | "accept" | "reject",
  "price": <float>,
  "sla_tier": "basic" | "standard" | "premium",
  "delivery_hours": <int>,
  "reasoning": "<brief explanation>"
}
"""

SELLER_SYSTEM_PROMPT = """\
You are a seller agent negotiating to provide a service.
Your goal: maximize revenue while maintaining a fair reputation.
You must respond with ONLY a valid JSON object (no markdown, no explanation).

JSON format:
{
  "action": "counter" | "accept" | "reject",
  "price": <float>,
  "sla_tier": "basic" | "standard" | "premium",
  "delivery_hours": <int>,
  "reasoning": "<brief explanation>"
}
"""


def _parse_llm_json(raw: str) -> dict[str, Any]:
    """Extract JSON from LLM response, tolerating markdown fences.

    Raises ``ValueError`` with a diagnostic snippet when parsing fails.
    """
    text = raw.strip()
    # Strip markdown code fences (```json ... ```)
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        # Provide a diagnostic snippet (first 200 chars) for debugging
        snippet = text[:200] + ("..." if len(text) > 200 else "")
        raise ValueError(
            f"LLM returned invalid JSON (pos {exc.pos}): {exc.msg}\n"
            f"Response snippet: {snippet!r}"
        ) from exc


# ---------------------------------------------------------------------------
# StateGraph Node Functions
# ---------------------------------------------------------------------------

async def buyer_propose(state: NegotiationState) -> dict[str, Any]:
    """Buyer agent generates an initial or counter-proposal."""
    llm = _get_qwen_client()
    round_num = state.get("current_round", 1)
    budget = state["buyer_budget"]

    # Progressive concession: buyer raises offer each round
    offer_price = budget * (1 + CONCESSION_RATE_BUYER * (round_num - 1))
    seller_last = state.get("seller_proposal")

    context = (
        f"Round {round_num}/{state.get('max_rounds', MAX_NEGOTIATION_ROUNDS)}.\n"
        f"Your budget: ${budget:.2f}. Your current offer ceiling: ${offer_price:.2f}.\n"
        f"Service needed: {state['buyer_intent']}.\n"
    )
    if seller_last:
        context += (
            f"Seller's last proposal: price=${seller_last['price']:.2f}, "
            f"SLA={seller_last['sla_tier']}, delivery={seller_last['delivery_hours']}h.\n"
            f"Seller's reasoning: {seller_last.get('reasoning', 'N/A')}\n"
        )
    context += f"Propose a price ≤ ${offer_price:.2f}."

    raw = await llm.chat(BUYER_SYSTEM_PROMPT, context)
    proposal = _parse_llm_json(raw)
    # Enforce budget constraint
    proposal["price"] = min(float(proposal["price"]), offer_price)
    proposal["round_number"] = round_num

    history = list(state.get("history", []))
    history.append({"role": "buyer", "round": round_num, **proposal})

    return {
        "buyer_proposal": proposal,
        "history": history,
        "status": NegotiationStatus.IN_PROGRESS.value,
    }


async def seller_evaluate(state: NegotiationState) -> dict[str, Any]:
    """Seller agent evaluates buyer's proposal and responds."""
    llm = _get_qwen_client()
    round_num = state.get("current_round", 1)
    base_price = state["seller_base_price"]
    buyer_prop = state["buyer_proposal"]

    # Progressive concession: seller lowers floor each round
    floor_price = base_price * (1 - CONCESSION_RATE_SELLER * (round_num - 1))

    context = (
        f"Round {round_num}/{state.get('max_rounds', MAX_NEGOTIATION_ROUNDS)}.\n"
        f"Your base price: ${base_price:.2f}. Your current floor: ${floor_price:.2f}.\n"
        f"Your capability: {state['seller_capability']}.\n"
        f"Buyer's proposal: price=${buyer_prop['price']:.2f}, "
        f"SLA={buyer_prop['sla_tier']}, delivery={buyer_prop['delivery_hours']}h.\n"
        f"Buyer's reasoning: {buyer_prop.get('reasoning', 'N/A')}\n"
    )
    if buyer_prop["price"] >= floor_price:
        context += "The offer meets your floor price. Consider accepting."
    else:
        gap = floor_price - buyer_prop["price"]
        context += f"Gap to your floor: ${gap:.2f}. Counter with price ≥ ${floor_price:.2f}."

    raw = await llm.chat(SELLER_SYSTEM_PROMPT, context)
    response = _parse_llm_json(raw)
    response["round_number"] = round_num

    history = list(state.get("history", []))
    history.append({"role": "seller", "round": round_num, **response})

    return {
        "seller_proposal": response,
        "history": history,
    }


def route_after_seller(state: NegotiationState) -> str:
    """Conditional routing after seller evaluation."""
    seller_resp = state.get("seller_proposal", {})
    action = seller_resp.get("action", "counter")
    round_num = state.get("current_round", 1)
    max_rounds = state.get("max_rounds", MAX_NEGOTIATION_ROUNDS)

    if action == "accept":
        return "settle"
    if action == "reject" or round_num >= max_rounds:
        return "abort"
    return "buyer_decide"


async def buyer_decide(state: NegotiationState) -> dict[str, Any]:
    """Buyer decides whether to accept seller's counter or continue."""
    llm = _get_qwen_client()
    round_num = state.get("current_round", 1)
    budget = state["buyer_budget"]
    seller_prop = state["seller_proposal"]
    # Acceptance ceiling: same concession base as buyer_propose (round_num - 1)
    # plus a half-step tolerance so the buyer accepts slightly above their own offer
    # without jumping a full concession round ahead.
    offer_ceiling = budget * (1 + CONCESSION_RATE_BUYER * (round_num - 0.5))

    context = (
        f"Round {round_num}/{state.get('max_rounds', MAX_NEGOTIATION_ROUNDS)}.\n"
        f"Your budget: ${budget:.2f}. Max you can pay: ${offer_ceiling:.2f}.\n"
        f"Seller countered: price=${seller_prop['price']:.2f}, "
        f"SLA={seller_prop['sla_tier']}, delivery={seller_prop['delivery_hours']}h.\n"
        f"Seller's reasoning: {seller_prop.get('reasoning', 'N/A')}\n"
    )
    if seller_prop["price"] <= offer_ceiling:
        context += "This is within your acceptable range. Consider accepting."
    else:
        context += "This exceeds your range. Propose a counter-offer or reject."

    raw = await llm.chat(BUYER_SYSTEM_PROMPT, context)
    decision = _parse_llm_json(raw)
    decision["round_number"] = round_num

    history = list(state.get("history", []))
    history.append({"role": "buyer_decision", "round": round_num, **decision})

    return {
        "buyer_proposal": decision,
        "current_round": round_num + 1,
        "history": history,
    }


def route_after_buyer(state: NegotiationState) -> str:
    """Conditional routing after buyer decision."""
    buyer_resp = state.get("buyer_proposal", {})
    action = buyer_resp.get("action", "propose")
    round_num = state.get("current_round", 1)
    max_rounds = state.get("max_rounds", MAX_NEGOTIATION_ROUNDS)

    if action == "accept":
        return "settle"
    if action == "reject" or round_num > max_rounds:
        return "abort"
    return "seller_evaluate"


async def settle(state: NegotiationState) -> dict[str, Any]:
    """Finalize agreement and prepare for x402 settlement."""
    history = state.get("history", [])
    # Find the accepted proposal
    last_entry = history[-1] if history else {}
    agreed_price = float(last_entry.get("price", 0))
    agreed_sla = last_entry.get("sla_tier", "standard")

    # Use the round recorded in the last history entry to avoid off-by-one
    # from current_round being incremented before routing to settle.
    actual_round = last_entry.get("round", state.get("current_round", 1))

    result = {
        "status": NegotiationStatus.AGREED.value,
        "agreed_price": agreed_price,
        "agreed_sla": agreed_sla,
        "rounds_taken": actual_round,
        "buyer_initial": state["buyer_budget"],
        "seller_initial": state["seller_base_price"],
    }
    return {"final_result": result, "status": NegotiationStatus.AGREED.value}


async def abort(state: NegotiationState) -> dict[str, Any]:
    """Negotiation failed — no agreement reached."""
    result = {
        "status": NegotiationStatus.REJECTED.value,
        "agreed_price": None,
        "agreed_sla": None,
        "rounds_taken": state.get("current_round", 1),
        "buyer_initial": state["buyer_budget"],
        "seller_initial": state["seller_base_price"],
    }
    return {"final_result": result, "status": NegotiationStatus.REJECTED.value}


# ---------------------------------------------------------------------------
# StateGraph Builder (SpoonOS-compatible pattern)
# ---------------------------------------------------------------------------

class SimpleStateGraph:
    """
    Minimal StateGraph implementation compatible with SpoonOS patterns.

    Models the negotiation as a directed graph:
      buyer_propose → seller_evaluate → [settle | buyer_decide | abort]
      buyer_decide → [settle | seller_evaluate | abort]

    In production SpoonOS, replace with:
      from spoon_ai.graph import StateGraph, END
    """

    def __init__(self) -> None:
        self._nodes: dict[str, Any] = {}
        self._edges: dict[str, Any] = {}
        self._conditional_edges: dict[str, Any] = {}
        self._entry: str = ""

    def add_node(self, name: str, func: Any) -> None:
        self._nodes[name] = func

    def add_edge(self, src: str, dst: str) -> None:
        self._edges[src] = dst

    def add_conditional_edges(
        self, src: str, router: Any, mapping: dict[str, str]
    ) -> None:
        self._conditional_edges[src] = (router, mapping)

    def set_entry_point(self, name: str) -> None:
        self._entry = name

    async def invoke(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute the graph until reaching a terminal node."""
        current = self._entry
        while current and current != "__end__":
            node_fn = self._nodes.get(current)
            if node_fn is None:
                break
            updates = await node_fn(state)
            state = {**state, **updates}

            # Check conditional edges first
            if current in self._conditional_edges:
                router, mapping = self._conditional_edges[current]
                next_key = router(state)
                current = mapping.get(next_key, "__end__")
            elif current in self._edges:
                current = self._edges[current]
            else:
                current = "__end__"
        return state


# ---------------------------------------------------------------------------
# Negotiation Engine
# ---------------------------------------------------------------------------

class NegotiationEngine:
    """
    Orchestrates multi-round agent negotiation via StateGraph.

    Usage:
        engine = NegotiationEngine()
        result = await engine.run_negotiation(
            buyer_intent="Data analysis for 100 wallets",
            seller_capability="On-chain analytics service",
            buyer_budget=50.0,
            seller_base_price=80.0,
        )
    """

    def __init__(self, max_rounds: int = MAX_NEGOTIATION_ROUNDS) -> None:
        self.max_rounds = max_rounds
        self.graph = self._build_graph()

    def _build_graph(self) -> SimpleStateGraph:
        """Construct the negotiation StateGraph."""
        graph = SimpleStateGraph()

        # Register nodes
        graph.add_node("buyer_propose", buyer_propose)
        graph.add_node("seller_evaluate", seller_evaluate)
        graph.add_node("buyer_decide", buyer_decide)
        graph.add_node("settle", settle)
        graph.add_node("abort", abort)

        # Entry point
        graph.set_entry_point("buyer_propose")

        # Edges: buyer_propose → seller_evaluate (always)
        graph.add_edge("buyer_propose", "seller_evaluate")

        # Conditional: after seller evaluates
        graph.add_conditional_edges("seller_evaluate", route_after_seller, {
            "settle": "settle",
            "abort": "abort",
            "buyer_decide": "buyer_decide",
        })

        # Conditional: after buyer decides
        graph.add_conditional_edges("buyer_decide", route_after_buyer, {
            "settle": "settle",
            "abort": "abort",
            "seller_evaluate": "seller_evaluate",
        })

        # Terminal nodes
        graph.add_edge("settle", "__end__")
        graph.add_edge("abort", "__end__")

        return graph

    async def run_negotiation(
        self,
        buyer_intent: str,
        seller_capability: str,
        buyer_budget: float,
        seller_base_price: float,
    ) -> NegotiationResult:
        """Execute a full negotiation session."""
        initial_state: NegotiationState = {
            "buyer_intent": buyer_intent,
            "seller_capability": seller_capability,
            "buyer_budget": buyer_budget,
            "seller_base_price": seller_base_price,
            "current_round": 1,
            "max_rounds": self.max_rounds,
            "status": NegotiationStatus.PENDING.value,
            "buyer_proposal": None,
            "seller_proposal": None,
            "history": [],
            "final_result": None,
        }

        final_state = await self.graph.invoke(initial_state)
        result_data = final_state.get("final_result", {})

        return NegotiationResult(
            status=NegotiationStatus(result_data.get("status", "rejected")),
            agreed_price=result_data.get("agreed_price"),
            agreed_sla=result_data.get("agreed_sla"),
            rounds_taken=result_data.get("rounds_taken", 0),
            buyer_initial=buyer_budget,
            seller_initial=seller_base_price,
            history=final_state.get("history", []),
        )


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

async def main() -> None:
    """Demo: run a negotiation between two agents."""
    print("=" * 65)
    print("  Agent Negotiation Protocol — SpoonOS Demo")
    print("=" * 65)

    engine = NegotiationEngine(max_rounds=5)
    result = await engine.run_negotiation(
        buyer_intent="On-chain data analysis for 100 wallets, "
                     "including transaction patterns and risk scoring",
        seller_capability="Full-stack on-chain analytics service, "
                         "supports batch wallet profiling, risk assessment, "
                         "and custom report generation",
        buyer_budget=50.0,
        seller_base_price=80.0,
    )

    print(f"\n{'─' * 65}")
    print("  Negotiation History")
    print(f"{'─' * 65}")
    for entry in result.history:
        role = entry.get("role", "?")
        rnd = entry.get("round", "?")
        action = entry.get("action", "?")
        price = entry.get("price", "?")
        reasoning = entry.get("reasoning", "")
        print(f"  [Round {rnd}] {role:>15} | {action:<8} | ${price:<8} | {reasoning}")

    print(f"\n{'─' * 65}")
    print("  Result")
    print(f"{'─' * 65}")
    print(f"  Status:         {result.status.value}")
    print(f"  Agreed Price:   ${result.agreed_price}" if result.agreed_price else "  Agreed Price:   N/A")
    print(f"  Agreed SLA:     {result.agreed_sla or 'N/A'}")
    print(f"  Rounds Taken:   {result.rounds_taken}")
    print(f"  Buyer Initial:  ${result.buyer_initial}")
    print(f"  Seller Initial: ${result.seller_initial}")

    if result.status == NegotiationStatus.AGREED and result.agreed_price:
        print(f"\n  → Proceeding to x402 settlement...")
        from x402_settlement import X402Settlement
        settlement = X402Settlement()
        tx = await settlement.execute_settlement(
            agreed_price=result.agreed_price,
            buyer_id="agent-buyer-001",
            seller_id="agent-seller-001",
            sla_tier=result.agreed_sla or "standard",
        )
        print(f"  → Settlement TX: {tx.tx_hash}")
        print(f"  → Buyer reputation:  {tx.buyer_reputation_after:.2f}")
        print(f"  → Seller reputation: {tx.seller_reputation_after:.2f}")

    print(f"\n{'=' * 65}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
