#!/usr/bin/env python3
"""Flashbots MEV Protection."""

import os
from web3 import Web3
from eth_account import Account

FLASHBOTS_RPC = "https://rpc.flashbots.net/fast"
MEV_BLOCKER_RPC = "https://rpc.mevblocker.io"


class FlashbotsProtector:
    """Send transactions via Flashbots for MEV protection."""

    def __init__(self, use_mev_blocker: bool = False):
        rpc = MEV_BLOCKER_RPC if use_mev_blocker else FLASHBOTS_RPC
        self.w3 = Web3(Web3.HTTPProvider(rpc))
        self.account = Account.from_key(os.getenv("PRIVATE_KEY"))
        self.use_mev_blocker = use_mev_blocker

    async def send_protected_transaction(
        self,
        to: str,
        data: str,
        value: int = 0,
        gas_limit: int = None
    ) -> str:
        """Send transaction via Flashbots/MEV Blocker for MEV protection."""

        # Estimate gas if not provided
        if gas_limit is None:
            gas_limit = self.w3.eth.estimate_gas({
                "from": self.account.address,
                "to": to,
                "data": data,
                "value": value
            })

        # Build transaction
        tx = {
            "from": self.account.address,
            "to": to,
            "data": data,
            "value": value,
            "gas": gas_limit,
            "maxFeePerGas": self.w3.eth.gas_price * 2,
            "maxPriorityFeePerGas": self.w3.to_wei(2, "gwei"),
            "nonce": self.w3.eth.get_transaction_count(self.account.address),
            "chainId": 1
        }

        # Sign and send
        signed = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)

        return tx_hash.hex()

    def get_protection_info(self) -> str:
        """Get info about current MEV protection."""
        if self.use_mev_blocker:
            return """
MEV Blocker Protection:
- RPC: https://rpc.mevblocker.io
- Returns 90% of backrun MEV to users
- No frontrunning or sandwich attacks
"""
        else:
            return """
Flashbots Protect:
- RPC: https://rpc.flashbots.net/fast
- Transactions not visible in public mempool
- No frontrunning or sandwich attacks
- Fast mode for quicker inclusion
"""


def main():
    # Example usage
    protector = FlashbotsProtector(use_mev_blocker=False)
    print(protector.get_protection_info())

    # MEV Blocker alternative
    mev_blocker = FlashbotsProtector(use_mev_blocker=True)
    print(mev_blocker.get_protection_info())


if __name__ == "__main__":
    main()
