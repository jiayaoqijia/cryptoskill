#!/usr/bin/env python3
"""Sign-In with Ethereum (SIWE) Authentication."""

from siwe import SiweMessage, generate_nonce
from datetime import datetime, timedelta
from typing import Optional


class SIWEAuthenticator:
    """SIWE authentication handler."""

    def __init__(self, domain: str, uri: str):
        self.domain = domain
        self.uri = uri
        self.nonces = {}  # In production, use Redis/DB

    def create_message(self, address: str, chain_id: int = 1,
                       statement: str = "Sign in to access your account.") -> dict:
        """Create SIWE message for signing."""
        nonce = generate_nonce()

        # Store nonce with expiry
        self.nonces[nonce] = {
            "address": address,
            "expires": datetime.utcnow() + timedelta(minutes=10)
        }

        message = SiweMessage(
            domain=self.domain,
            address=address,
            statement=statement,
            uri=self.uri,
            version="1",
            chain_id=chain_id,
            nonce=nonce,
            issued_at=datetime.utcnow().isoformat() + "Z",
            expiration_time=(datetime.utcnow() + timedelta(hours=1)).isoformat() + "Z"
        )

        return {
            "message": message.prepare_message(),
            "nonce": nonce
        }

    def verify(self, message: str, signature: str) -> Optional[str]:
        """Verify SIWE signature and return address."""
        try:
            siwe_message = SiweMessage.from_message(message)

            # Check nonce
            nonce = siwe_message.nonce
            if nonce not in self.nonces:
                return None

            nonce_data = self.nonces[nonce]
            if datetime.utcnow() > nonce_data["expires"]:
                del self.nonces[nonce]
                return None

            # Verify signature
            siwe_message.verify(signature)

            # Clean up nonce (single use)
            del self.nonces[nonce]

            return siwe_message.address

        except Exception as e:
            print(f"SIWE verification failed: {e}")
            return None


def main():
    # Example usage
    auth = SIWEAuthenticator(
        domain="example.com",
        uri="https://example.com"
    )

    # Create message for user to sign
    result = auth.create_message(
        address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb7",
        chain_id=1
    )

    print("SIWE Message to sign:")
    print(result["message"])
    print(f"\nNonce: {result['nonce']}")


if __name__ == "__main__":
    main()
