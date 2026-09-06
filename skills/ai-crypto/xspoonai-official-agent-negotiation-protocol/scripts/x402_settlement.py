#!/usr/bin/env python3
"""
x402 Settlement Module — Payment settlement and reputation tracking.

Simulates the x402 payment protocol flow for agent-to-agent transactions:
  1. Buyer requests paid service → 402 Payment Required
  2. Agent wallet signs payment transaction
  3. Service verifies signature → 200 OK
  4. Reputation scores updated for both parties

Author: bonujel
Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SettlementResult:
    """Immutable result of an x402 settlement transaction."""
    tx_hash: str
    buyer_id: str
    seller_id: str
    amount: float
    asset: str
    sla_tier: str
    timestamp: float
    buyer_reputation_after: float
    seller_reputation_after: float
    status: str  # "confirmed" | "pending" | "failed"


@dataclass(frozen=True)
class AgentReputation:
    """Immutable reputation record for an agent (ERC-8004 compatible)."""
    agent_id: str
    score: float = 0.5          # 0.0 ~ 1.0
    total_deals: int = 0
    successful_deals: int = 0
    total_volume: float = 0.0
    avg_settlement_time: float = 0.0


# ---------------------------------------------------------------------------
# Reputation Store (in-memory, ERC-8004 compatible interface)
# ---------------------------------------------------------------------------

class ReputationStore:
    """
    In-memory reputation registry mirroring ERC-8004 IdentityRegistry.

    In production SpoonOS, this would interact with:
      - NeoX Testnet IdentityRegistry contract
      - NeoFS for Agent Card / DID Document storage
    """

    def __init__(self) -> None:
        self._store: dict[str, AgentReputation] = {}

    def get_or_create(self, agent_id: str) -> AgentReputation:
        """Retrieve agent reputation, creating a default if absent."""
        if agent_id not in self._store:
            self._store[agent_id] = AgentReputation(agent_id=agent_id)
        return self._store[agent_id]

    def update_after_deal(
        self,
        agent_id: str,
        success: bool,
        deal_volume: float,
        settlement_time: float,
    ) -> AgentReputation:
        """Update reputation after a completed deal. Returns a new immutable record."""
        old = self.get_or_create(agent_id)
        new_total_deals = old.total_deals + 1
        new_total_volume = old.total_volume + deal_volume
        new_successful = old.successful_deals + (1 if success else 0)

        # Exponential moving average for score
        success_rate = new_successful / new_total_deals
        new_score = 0.7 * success_rate + 0.3 * old.score

        # Update average settlement time
        new_avg_time = (
            old.avg_settlement_time * (new_total_deals - 1) + settlement_time
        ) / new_total_deals

        updated = AgentReputation(
            agent_id=agent_id,
            score=new_score,
            total_deals=new_total_deals,
            successful_deals=new_successful,
            total_volume=new_total_volume,
            avg_settlement_time=new_avg_time,
        )
        self._store[agent_id] = updated
        return updated


# ---------------------------------------------------------------------------
# x402 Payment Challenge (protocol simulation)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PaymentChallenge:
    """
    Represents the 402 Payment Required challenge from a service provider.

    In the real x402 protocol:
      - Server returns HTTP 402 with this challenge in headers/body
      - Agent wallet signs the payment matching these parameters
      - Server verifies signature before granting access
    """
    receiver_address: str
    amount: float
    asset: str           # e.g. "USDC"
    network: str         # e.g. "base", "polygon"
    nonce: str
    expires_at: float


def _generate_tx_hash(
    buyer_id: str,
    seller_id: str,
    amount: float,
    nonce: str,
    timestamp: float,
) -> str:
    """Generate a deterministic mock transaction hash."""
    payload = f"{buyer_id}:{seller_id}:{amount}:{nonce}:{timestamp}"
    return "0x" + hashlib.sha256(payload.encode()).hexdigest()


# ---------------------------------------------------------------------------
# X402 Settlement Engine
# ---------------------------------------------------------------------------

class X402Settlement:
    """
    Executes x402 payment settlement between negotiating agents.

    Flow:
      1. Create payment challenge (simulates 402 response)
      2. Buyer agent "signs" the transaction
      3. Verify signature and confirm payment
      4. Update reputation for both parties

    In production SpoonOS, integrate with:
      - spoon_ai.payments for real x402 flow
      - spoon_ai.turnkey for wallet signing
      - ERC-8004 IdentityRegistry for on-chain reputation
    """

    def __init__(self) -> None:
        self.reputation_store = ReputationStore()

    def create_challenge(
        self,
        seller_id: str,
        amount: float,
        asset: str = "USDC",
        network: str = "base",
    ) -> PaymentChallenge:
        """Simulate a 402 Payment Required challenge from the seller."""
        nonce = hashlib.sha256(
            f"{seller_id}:{time.time()}".encode()
        ).hexdigest()[:16]

        return PaymentChallenge(
            receiver_address=f"0x{hashlib.sha256(seller_id.encode()).hexdigest()[:40]}",
            amount=amount,
            asset=asset,
            network=network,
            nonce=nonce,
            expires_at=time.time() + 300,  # 5 min expiry
        )

    def verify_payment(
        self,
        challenge: PaymentChallenge,
        buyer_id: str,
        signed_amount: float,
    ) -> bool:
        """
        Verify the buyer's payment matches the challenge.

        In production, this verifies the cryptographic signature
        against the challenge parameters (EIP-3009 for USDC).
        """
        if time.time() > challenge.expires_at:
            return False
        if abs(signed_amount - challenge.amount) > 0.01:
            return False
        return True

    async def execute_settlement(
        self,
        agreed_price: float,
        buyer_id: str,
        seller_id: str,
        sla_tier: str = "standard",
        asset: str = "USDC",
        network: str = "base",
    ) -> SettlementResult:
        """
        Execute the full x402 settlement flow.

        Steps:
          1. Seller issues 402 challenge
          2. Buyer signs payment
          3. Verify and confirm
          4. Update reputations
        """
        timestamp = time.time()

        # Step 1: Create payment challenge
        challenge = self.create_challenge(
            seller_id=seller_id,
            amount=agreed_price,
            asset=asset,
            network=network,
        )

        # Step 2: Buyer "signs" the payment (simulated)
        signed_amount = agreed_price

        # Step 3: Verify payment
        is_valid = self.verify_payment(challenge, buyer_id, signed_amount)

        if not is_valid:
            return SettlementResult(
                tx_hash="0x" + "0" * 64,
                buyer_id=buyer_id,
                seller_id=seller_id,
                amount=agreed_price,
                asset=asset,
                sla_tier=sla_tier,
                timestamp=timestamp,
                buyer_reputation_after=self.reputation_store.get_or_create(buyer_id).score,
                seller_reputation_after=self.reputation_store.get_or_create(seller_id).score,
                status="failed",
            )

        # Step 4: Generate transaction hash
        tx_hash = _generate_tx_hash(
            buyer_id, seller_id, agreed_price, challenge.nonce, timestamp
        )

        # Step 5: Update reputations
        settlement_time = time.time() - timestamp
        buyer_rep = self.reputation_store.update_after_deal(
            agent_id=buyer_id,
            success=True,
            deal_volume=agreed_price,
            settlement_time=settlement_time,
        )
        seller_rep = self.reputation_store.update_after_deal(
            agent_id=seller_id,
            success=True,
            deal_volume=agreed_price,
            settlement_time=settlement_time,
        )

        return SettlementResult(
            tx_hash=tx_hash,
            buyer_id=buyer_id,
            seller_id=seller_id,
            amount=agreed_price,
            asset=asset,
            sla_tier=sla_tier,
            timestamp=timestamp,
            buyer_reputation_after=buyer_rep.score,
            seller_reputation_after=seller_rep.score,
            status="confirmed",
        )
