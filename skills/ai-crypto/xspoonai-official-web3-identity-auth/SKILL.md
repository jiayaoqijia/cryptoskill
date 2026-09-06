---
name: web3-identity-auth
description: Implement Web3 authentication and identity. Use when integrating Sign-In with Ethereum (SIWE), ENS resolution, session management, or verifiable credentials.
---

# Web3 Identity & Authentication

Implement decentralized identity and authentication.

## Authentication Methods

| Method | Use Case | Gas Cost |
|--------|----------|----------|
| SIWE | Web app login | None (signature only) |
| ENS | Human-readable addresses | None (read only) |
| ERC-8004 | Agent identity | On-chain registration |

## Sign-In with Ethereum (SIWE)

### SIWE Message Format

```
example.com wants you to sign in with your Ethereum account:
0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb7

Sign in to access your account.

URI: https://example.com
Version: 1
Chain ID: 1
Nonce: 32891756
Issued At: 2025-01-23T10:00:00.000Z
Expiration Time: 2025-01-23T11:00:00.000Z
```

### Backend Implementation

```python
# scripts/siwe_auth.py
from siwe import SiweMessage, generate_nonce
from datetime import datetime, timedelta
from typing import Optional
import os

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
```

### FastAPI Integration

```python
# scripts/siwe_api.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
import jwt
import os

app = FastAPI()
auth = SIWEAuthenticator(
    domain="example.com",
    uri="https://example.com"
)

class NonceRequest(BaseModel):
    address: str
    chain_id: int = 1

class VerifyRequest(BaseModel):
    message: str
    signature: str

@app.post("/auth/nonce")
async def get_nonce(request: NonceRequest):
    """Get SIWE message to sign."""
    result = auth.create_message(
        address=request.address,
        chain_id=request.chain_id
    )
    return result

@app.post("/auth/verify")
async def verify_signature(request: VerifyRequest):
    """Verify signature and issue JWT."""
    address = auth.verify(request.message, request.signature)

    if not address:
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Issue JWT
    token = jwt.encode(
        {
            "address": address,
            "exp": datetime.utcnow() + timedelta(hours=24)
        },
        os.getenv("JWT_SECRET"),
        algorithm="HS256"
    )

    return {"token": token, "address": address}

# Protected endpoint
security = HTTPBearer()

def get_current_user(credentials = Depends(security)):
    try:
        payload = jwt.decode(
            credentials.credentials,
            os.getenv("JWT_SECRET"),
            algorithms=["HS256"]
        )
        return payload["address"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/protected")
async def protected_route(address: str = Depends(get_current_user)):
    return {"message": f"Hello {address}"}
```

## ENS Resolution

### ENS Tool

```python
# scripts/ens_resolver.py
from spoon_ai.tools.base import BaseTool
from pydantic import Field
from web3 import Web3
from ens import ENS

ENS_REGISTRY = "0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e"

class ENSResolverTool(BaseTool):
    name: str = "ens_resolver"
    description: str = "Resolve ENS names to addresses and reverse lookup"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["resolve", "reverse", "records"]},
            "input": {"type": "string", "description": "ENS name or address"}
        },
        "required": ["action", "input"]
    })

    def __init__(self):
        super().__init__()
        self.w3 = Web3(Web3.HTTPProvider(os.getenv("ETHEREUM_RPC")))
        self.ns = ENS.from_web3(self.w3)

    async def execute(self, action: str, input: str) -> str:
        if action == "resolve":
            return self._resolve_name(input)
        elif action == "reverse":
            return self._reverse_lookup(input)
        elif action == "records":
            return self._get_records(input)

    def _resolve_name(self, name: str) -> str:
        """Resolve ENS name to address."""
        try:
            address = self.ns.address(name)
            if address:
                return f"{name} -> {address}"
            return f"No address found for {name}"
        except Exception as e:
            return f"Error: {str(e)}"

    def _reverse_lookup(self, address: str) -> str:
        """Reverse lookup address to ENS name."""
        try:
            name = self.ns.name(address)
            if name:
                return f"{address} -> {name}"
            return f"No ENS name for {address}"
        except Exception as e:
            return f"Error: {str(e)}"

    def _get_records(self, name: str) -> str:
        """Get ENS text records."""
        try:
            resolver = self.ns.resolver(name)
            if not resolver:
                return f"No resolver for {name}"

            records = {}
            text_keys = ["email", "url", "avatar", "description",
                        "com.twitter", "com.github", "com.discord"]

            for key in text_keys:
                try:
                    value = resolver.functions.text(
                        self.ns.namehash(name), key
                    ).call()
                    if value:
                        records[key] = value
                except:
                    pass

            if records:
                result = f"ENS Records for {name}:\n"
                for k, v in records.items():
                    result += f"  {k}: {v}\n"
                return result

            return f"No text records for {name}"

        except Exception as e:
            return f"Error: {str(e)}"
```

### Batch Resolution

```python
# scripts/ens_batch.py
import asyncio
import aiohttp

ENS_SUBGRAPH = "https://api.thegraph.com/subgraphs/name/ensdomains/ens"

async def batch_resolve_names(names: list) -> dict:
    """Resolve multiple ENS names efficiently via subgraph."""
    query = """
    query ResolveNames($names: [String!]) {
        domains(where: {name_in: $names}) {
            name
            resolvedAddress {
                id
            }
        }
    }
    """

    async with aiohttp.ClientSession() as session:
        async with session.post(
            ENS_SUBGRAPH,
            json={"query": query, "variables": {"names": names}}
        ) as resp:
            data = await resp.json()

    results = {}
    for domain in data.get("data", {}).get("domains", []):
        name = domain["name"]
        address = domain.get("resolvedAddress", {}).get("id")
        results[name] = address

    return results

async def batch_reverse_lookup(addresses: list) -> dict:
    """Reverse lookup multiple addresses."""
    query = """
    query ReverseResolve($addresses: [String!]) {
        accounts(where: {id_in: $addresses}) {
            id
            domains(where: {name_not: null}, first: 1) {
                name
            }
        }
    }
    """

    # Convert to lowercase for subgraph
    addresses = [a.lower() for a in addresses]

    async with aiohttp.ClientSession() as session:
        async with session.post(
            ENS_SUBGRAPH,
            json={"query": query, "variables": {"addresses": addresses}}
        ) as resp:
            data = await resp.json()

    results = {}
    for account in data.get("data", {}).get("accounts", []):
        address = Web3.to_checksum_address(account["id"])
        domains = account.get("domains", [])
        results[address] = domains[0]["name"] if domains else None

    return results
```

## Session Management

### Web3 Session Handler

```python
# scripts/session_manager.py
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
```

## SpoonOS Agent Integration

### Auth-Aware Agent

```python
# scripts/auth_agent.py
from spoon_ai.agents import SpoonReactMCP
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager

class AuthenticatedAgent(SpoonReactMCP):
    """Agent with Web3 authentication context."""

    name = "authenticated_agent"
    description = "Agent with user wallet context"

    def __init__(self, user_address: str = None, chain_id: int = 1):
        self.user_address = user_address
        self.chain_id = chain_id

        system_prompt = f"""You are an assistant for a Web3 user.

User Context:
- Wallet: {user_address or 'Not connected'}
- Chain: {chain_id}

When the user asks about their wallet, portfolio, or transactions,
use the provided address. Always confirm before executing transactions.
"""

        super().__init__(
            llm=ChatBot(model_name="gpt-4o"),
            tools=ToolManager([
                ENSResolverTool(),
                WalletTool(default_address=user_address)
            ]),
            system_prompt=system_prompt
        )

# API endpoint with auth
@app.post("/agent/query")
async def query_agent(
    query: str,
    session_id: str = Header(None)
):
    address = session_manager.validate_session(session_id)

    if not address:
        raise HTTPException(status_code=401, detail="Invalid session")

    agent = AuthenticatedAgent(user_address=address)
    response = await agent.run(query)

    return {"response": response}
```

## Environment Variables

```bash
# Authentication
JWT_SECRET=your-secret-key
SIWE_DOMAIN=example.com
SIWE_URI=https://example.com

# ENS
ETHEREUM_RPC=https://eth.llamarpc.com

# Session Storage
REDIS_URL=redis://localhost:6379
```

## Security Best Practices

1. **Nonce Management** - Single-use nonces with expiry
2. **Signature Verification** - Always verify on backend
3. **Session Rotation** - Rotate tokens periodically
4. **Chain Validation** - Verify chain ID matches expected
5. **Address Checksums** - Always use checksummed addresses
