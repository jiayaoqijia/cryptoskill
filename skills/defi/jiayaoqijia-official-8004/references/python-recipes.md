# Python SDK Recipes

Recipes for interacting with ERC-8004 contracts using the [Agent0 Python SDK](https://github.com/agent0labs/agent0-py) and raw web3.py.

## Setup

```bash
pip install agent0-py web3
```

```python
from agent0 import Agent0Client
from web3 import Web3

# Initialize client
client = Agent0Client(
    chain_id=11155111,  # Ethereum Sepolia
    rpc_url="https://rpc.sepolia.org",
    private_key="0x..."  # Or use environment variable
)
```

## Identity Registry

### Register an Agent

```python
# Prepare registration file (host on IPFS or HTTPS)
agent_uri = "https://example.com/agent.json"

# Mint agent NFT
tx = client.identity.register(agent_uri=agent_uri)
print(f"Agent registered: token ID {tx.token_id}")
print(f"Agent ID: {client.chain_id}:{tx.token_id}")
```

### Read Agent URI

```python
# Get the agentURI for an existing agent
uri = client.identity.agent_uri(token_id=42)
print(f"Agent URI: {uri}")
```

### Transfer Agent Ownership

```python
tx = client.identity.transfer(
    token_id=42,
    to_address="0xNewOwner..."
)
```

### Update Agent URI

```python
tx = client.identity.set_agent_uri(
    token_id=42,
    agent_uri="https://example.com/agent-v2.json"
)
```

## Reputation Registry

### Submit Feedback

```python
# Star rating: 1★=20, 2★=40, 3★=60, 4★=80, 5★=100
tx = client.reputation.submit_feedback(
    token_id=42,
    value=80,        # 4 stars
    decimals=0,
    tag="starred",
    payload=""       # Optional IPFS hash for detailed review
)
```

### Submit Negative Feedback

```python
tx = client.reputation.submit_feedback(
    token_id=42,
    value=-50,       # Negative signal
    decimals=0,
    tag="dispute",
    payload="bafybei..."  # IPFS hash with dispute details
)
```

### Read Feedback

```python
# Get all feedback for an agent
feedbacks = client.reputation.get_feedbacks(token_id=42)
for fb in feedbacks:
    print(f"  From: {fb.submitter}, Value: {fb.value}, Tag: {fb.tag}")

# Compute trust label
count = len(feedbacks)
avg = sum(f.value for f in feedbacks) / count if count else 0
label = compute_trust_label(count, avg)
```

### Revoke Feedback

```python
# Only the original submitter can revoke
tx = client.reputation.revoke_feedback(
    token_id=42,
    feedback_id=7
)
```

## Validation Registry

### Request Validation

```python
tx = client.validation.request_validation(
    token_id=42,
    validator_address="0xValidator..."
)
```

### Submit Validation Response (Validator)

```python
tx = client.validation.submit_response(
    token_id=42,
    score=85,          # 0-100
    proof="0x..."      # Attestation proof bytes
)
```

## Raw web3.py (Without SDK)

### Contract ABIs

```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://rpc.sepolia.org"))

# Identity Registry (testnet)
IDENTITY_ADDRESS = "0x8004A818BFB912233c491871b3d84c89A494BD9e"

# Minimal ABI for reading
IDENTITY_ABI = [
    {
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "name": "agentURI",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    }
]

identity = w3.eth.contract(address=IDENTITY_ADDRESS, abi=IDENTITY_ABI)

# Read agent URI
uri = identity.functions.agentURI(42).call()
owner = identity.functions.ownerOf(42).call()
```

### Reputation Registry

```python
REPUTATION_ADDRESS = "0x8004B663056A597Dffe9eCcC1965A193B7388713"

REPUTATION_ABI = [
    {
        "inputs": [
            {"name": "tokenId", "type": "uint256"},
            {"name": "value", "type": "int128"},
            {"name": "decimals", "type": "uint8"},
            {"name": "tag", "type": "string"},
            {"name": "payload", "type": "string"}
        ],
        "name": "submitFeedback",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

reputation = w3.eth.contract(address=REPUTATION_ADDRESS, abi=REPUTATION_ABI)

# Submit feedback (requires signing)
tx = reputation.functions.submitFeedback(
    42,     # tokenId
    80,     # value (4 stars)
    0,      # decimals
    "starred",
    ""
).build_transaction({
    "from": account.address,
    "nonce": w3.eth.get_transaction_count(account.address),
    "gas": 200000,
})
signed = account.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
```

## Trust Label Computation

```python
def compute_trust_label(count: int, avg: float) -> str:
    """Apply ERC-8004 trust label rules. First match wins."""
    if count >= 5 and avg < -50:
        return f"🔴 Untrusted -- {avg}/100 ({count} reviews)"
    if avg < 0:
        return f"🟠 Caution -- {avg}/100 ({count} reviews)"
    if count >= 20 and avg >= 80:
        return f"⭐ Highly Trusted -- {avg}/100 ({count} reviews)"
    if count >= 10 and avg >= 70:
        return f"🟢 Trusted -- {avg}/100 ({count} reviews)"
    if count >= 5 and avg >= 50:
        return f"🟢 Established -- {avg}/100 ({count} reviews)"
    if count > 0:
        return f"🔵 Emerging -- {avg}/100 ({count} reviews)"
    return f"⚪ No Data -- 0/100 (0 reviews)"
```

## Batch Operations

### Fetch All Agents for an Owner

```python
import requests

def get_owner_agents(address: str) -> list:
    """Use 8004scan API for efficient owner lookup."""
    resp = requests.get(
        f"https://www.8004scan.io/api/v1/public/accounts/{address}/agents"
    )
    data = resp.json()
    return data["data"]["agents"] if data["success"] else []
```

### Monitor New Registrations

```python
import time

def poll_new_agents(chain_id: int, interval: int = 60):
    """Poll 8004scan for new agent registrations."""
    seen = set()
    while True:
        resp = requests.get(
            "https://www.8004scan.io/api/v1/public/agents",
            params={"chainId": chain_id, "limit": 20, "sortBy": "createdAt", "sortOrder": "desc"}
        )
        if resp.ok:
            for agent in resp.json()["data"]["agents"]:
                aid = f"{agent['chainId']}:{agent['tokenId']}"
                if aid not in seen:
                    seen.add(aid)
                    yield agent
        time.sleep(interval)
```

## Environment Configuration

```python
import os

# Recommended: use environment variables
config = {
    "chain_id": int(os.getenv("ERC8004_CHAIN_ID", "11155111")),
    "rpc_url": os.getenv("ERC8004_RPC_URL", "https://rpc.sepolia.org"),
    "private_key": os.getenv("ERC8004_PRIVATE_KEY"),
    "api_key": os.getenv("EIGHTSCAN_API_KEY"),
}
```
