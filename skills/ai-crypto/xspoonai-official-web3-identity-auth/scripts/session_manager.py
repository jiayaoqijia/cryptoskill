#!/usr/bin/env python3
"""Web3 Session Management."""

from datetime import datetime, timedelta
from typing import Optional, Dict
import secrets
import json


class Web3SessionManager:
    """Manage authenticated Web3 sessions."""

    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.local_sessions = {}  # Fallback if no Redis

    def create_session(self, address: str, chain_id: int,
                       metadata: dict = None) -> str:
        """Create new session after SIWE auth."""
        session_id = secrets.token_urlsafe(32)

        session_data = {
            "address": address,
            "chain_id": chain_id,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(hours=24)).isoformat(),
            "metadata": metadata or {}
        }

        if self.redis:
            self.redis.setex(
                f"session:{session_id}",
                timedelta(hours=24),
                json.dumps(session_data)
            )
        else:
            self.local_sessions[session_id] = session_data

        return session_id

    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session data."""
        if self.redis:
            data = self.redis.get(f"session:{session_id}")
            if data:
                return json.loads(data)
        else:
            return self.local_sessions.get(session_id)

        return None

    def validate_session(self, session_id: str) -> Optional[str]:
        """Validate session and return address."""
        session = self.get_session(session_id)

        if not session:
            return None

        expires = datetime.fromisoformat(session["expires_at"])
        if datetime.utcnow() > expires:
            self.destroy_session(session_id)
            return None

        return session["address"]

    def destroy_session(self, session_id: str):
        """Destroy session."""
        if self.redis:
            self.redis.delete(f"session:{session_id}")
        else:
            self.local_sessions.pop(session_id, None)

    def refresh_session(self, session_id: str) -> bool:
        """Extend session expiry."""
        session = self.get_session(session_id)

        if not session:
            return False

        session["expires_at"] = (
            datetime.utcnow() + timedelta(hours=24)
        ).isoformat()

        if self.redis:
            self.redis.setex(
                f"session:{session_id}",
                timedelta(hours=24),
                json.dumps(session)
            )
        else:
            self.local_sessions[session_id] = session

        return True


def main():
    # Example usage
    manager = Web3SessionManager()

    # Create session
    session_id = manager.create_session(
        address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb7",
        chain_id=1,
        metadata={"role": "user"}
    )

    print(f"Created session: {session_id}")

    # Validate session
    address = manager.validate_session(session_id)
    print(f"Session valid for: {address}")

    # Refresh session
    manager.refresh_session(session_id)
    print("Session refreshed")


if __name__ == "__main__":
    main()
