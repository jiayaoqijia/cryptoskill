---
name: web3-security-analysis
description: Analyze Web3 security risks with SpoonOS agents. Use when checking token safety (honeypots, rugs), simulating transactions, detecting MEV, or auditing contracts.
---

# Security Analysis

Protect users with comprehensive Web3 security tools.

## Security Stack

| Tool | Purpose | API |
|------|---------|-----|
| GoPlus | Token/address risk | `api.gopluslabs.io` |
| Honeypot.is | Honeypot detection | `api.honeypot.is` |
| Tenderly | Transaction simulation | `api.tenderly.co` |
| Flashbots | MEV protection | `rpc.flashbots.net` |

## Token Security Analysis

### GoPlus Integration

```python
# scripts/goplus_security.py
import aiohttp
from spoon_ai.tools.base import BaseTool
from pydantic import Field

GOPLUS_API = "https://api.gopluslabs.io/api/v1"

CHAIN_IDS = {
    "ethereum": "1",
    "bsc": "56",
    "polygon": "137",
    "arbitrum": "42161",
    "base": "8453"
}

class TokenSecurityTool(BaseTool):
    name: str = "token_security"
    description: str = "Analyze token security risks via GoPlus"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "token_address": {"type": "string", "description": "Token contract address"},
            "chain": {"type": "string", "default": "ethereum"}
        },
        "required": ["token_address"]
    })

    async def execute(self, token_address: str, chain: str = "ethereum") -> str:
        chain_id = CHAIN_IDS.get(chain, "1")
        url = f"{GOPLUS_API}/token_security/{chain_id}"

        params = {"contract_addresses": token_address.lower()}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                if resp.status != 200:
                    return f"Error: API returned {resp.status}"

                data = await resp.json()

        if data.get("code") != 1:
            return f"Error: {data.get('message', 'Unknown error')}"

        result = data.get("result", {}).get(token_address.lower(), {})

        return self._format_security_report(result, token_address)

    def _format_security_report(self, data: dict, address: str) -> str:
        """Format security analysis report."""

        # Risk indicators
        risks = []
        warnings = []

        # Critical risks
        if data.get("is_honeypot") == "1":
            risks.append("HONEYPOT DETECTED")
        if data.get("is_blacklisted") == "1":
            risks.append("BLACKLISTED TOKEN")
        if data.get("is_proxy") == "1":
            warnings.append("Proxy contract (upgradeable)")
        if data.get("is_mintable") == "1":
            warnings.append("Mintable token")
        if data.get("can_take_back_ownership") == "1":
            risks.append("Owner can reclaim ownership")
        if data.get("hidden_owner") == "1":
            risks.append("Hidden owner detected")
        if data.get("selfdestruct") == "1":
            risks.append("Self-destruct function")
        if data.get("external_call") == "1":
            warnings.append("External calls in contract")

        # Tax analysis
        buy_tax = float(data.get("buy_tax", "0") or "0") * 100
        sell_tax = float(data.get("sell_tax", "0") or "0") * 100

        if buy_tax > 10:
            warnings.append(f"High buy tax: {buy_tax:.1f}%")
        if sell_tax > 10:
            risks.append(f"High sell tax: {sell_tax:.1f}%")
        if sell_tax > 50:
            risks.append("EXTREME SELL TAX - LIKELY SCAM")

        # Holder analysis
        holder_count = data.get("holder_count", "Unknown")
        top_holders = data.get("holders", [])

        # Format report
        risk_level = "HIGH" if risks else ("MEDIUM" if warnings else "LOW")

        report = f"""
TOKEN SECURITY REPORT
{'='*50}
Address: {address}
Risk Level: {risk_level}

Token Info:
- Name: {data.get('token_name', 'Unknown')}
- Symbol: {data.get('token_symbol', 'Unknown')}
- Holders: {holder_count}

Taxes:
- Buy Tax: {buy_tax:.1f}%
- Sell Tax: {sell_tax:.1f}%
"""

        if risks:
            report += f"\nCRITICAL RISKS:\n"
            for risk in risks:
                report += f"  - {risk}\n"

        if warnings:
            report += f"\nWARNINGS:\n"
            for warning in warnings:
                report += f"  - {warning}\n"

        if top_holders:
            report += f"\nTop Holders:\n"
            for i, holder in enumerate(top_holders[:5], 1):
                pct = float(holder.get("percent", 0)) * 100
                report += f"  {i}. {holder.get('address', 'Unknown')[:10]}... ({pct:.1f}%)\n"

        return report
```

### Honeypot Detection

```python
# scripts/honeypot_check.py
import aiohttp
from spoon_ai.tools.base import BaseTool
from pydantic import Field

HONEYPOT_API = "https://api.honeypot.is/v2"

class HoneypotCheckTool(BaseTool):
    name: str = "honeypot_check"
    description: str = "Check if token is a honeypot"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "token_address": {"type": "string"},
            "chain": {"type": "string", "default": "ethereum"}
        },
        "required": ["token_address"]
    })

    async def execute(self, token_address: str, chain: str = "ethereum") -> str:
        url = f"{HONEYPOT_API}/IsHoneypot"

        payload = {
            "address": token_address,
            "chainId": CHAIN_IDS.get(chain, 1)
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                if resp.status != 200:
                    return f"Error: {resp.status}"

                data = await resp.json()

        honeypot = data.get("honeypotResult", {})
        simulation = data.get("simulationResult", {})

        is_honeypot = honeypot.get("isHoneypot", False)

        report = f"""
HONEYPOT ANALYSIS
{'='*40}
Token: {token_address}
Chain: {chain}

Result: {"HONEYPOT DETECTED" if is_honeypot else "NOT A HONEYPOT"}

Simulation:
- Buy Tax: {simulation.get('buyTax', 0):.1f}%
- Sell Tax: {simulation.get('sellTax', 0):.1f}%
- Buy Gas: {simulation.get('buyGas', 'N/A')}
- Sell Gas: {simulation.get('sellGas', 'N/A')}
"""

        if is_honeypot:
            report += f"\nReason: {honeypot.get('honeypotReason', 'Unknown')}"

        return report
```

## Transaction Simulation

### Tenderly Simulation

```python
# scripts/tenderly_simulate.py
import aiohttp
import os
from spoon_ai.tools.base import BaseTool
from pydantic import Field

TENDERLY_API = "https://api.tenderly.co/api/v1"

class TransactionSimulatorTool(BaseTool):
    name: str = "simulate_transaction"
    description: str = "Simulate transaction before execution"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "to": {"type": "string", "description": "Target contract"},
            "data": {"type": "string", "description": "Calldata (hex)"},
            "value": {"type": "string", "default": "0", "description": "ETH value in wei"},
            "chain": {"type": "string", "default": "ethereum"}
        },
        "required": ["to", "data"]
    })

    async def execute(self, to: str, data: str, value: str = "0",
                      chain: str = "ethereum") -> str:
        account = os.getenv("TENDERLY_ACCOUNT")
        project = os.getenv("TENDERLY_PROJECT")
        api_key = os.getenv("TENDERLY_API_KEY")

        url = f"{TENDERLY_API}/account/{account}/project/{project}/simulate"

        headers = {
            "X-Access-Key": api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "network_id": CHAIN_IDS.get(chain, "1"),
            "from": os.getenv("WALLET_ADDRESS"),
            "to": to,
            "input": data,
            "value": value,
            "gas": 8000000,
            "gas_price": "0",
            "save_if_fails": True
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as resp:
                if resp.status != 200:
                    error = await resp.text()
                    return f"Simulation failed: {error}"

                result = await resp.json()

        return self._format_simulation(result)

    def _format_simulation(self, result: dict) -> str:
        """Format simulation results."""
        tx = result.get("transaction", {})

        status = "SUCCESS" if tx.get("status") else "FAILED"
        gas_used = tx.get("gas_used", 0)

        report = f"""
TRANSACTION SIMULATION
{'='*40}
Status: {status}
Gas Used: {gas_used:,}

"""

        # Asset changes
        asset_changes = result.get("transaction", {}).get("transaction_info", {}).get("asset_changes", [])

        if asset_changes:
            report += "Asset Changes:\n"
            for change in asset_changes:
                direction = "+" if change.get("type") == "Transfer" else "-"
                amount = change.get("amount", 0)
                symbol = change.get("token_info", {}).get("symbol", "ETH")
                report += f"  {direction}{amount} {symbol}\n"

        # Logs/Events
        logs = tx.get("logs", [])
        if logs:
            report += f"\nEvents Emitted: {len(logs)}\n"
            for log in logs[:5]:
                report += f"  - {log.get('name', 'Unknown')}\n"

        # Error info
        if not tx.get("status"):
            error_info = tx.get("error_info", {})
            report += f"\nError: {error_info.get('error_message', 'Unknown error')}"

        return report
```

## MEV Protection

### Flashbots Integration

```python
# scripts/flashbots_protect.py
from web3 import Web3
from eth_account import Account
import os

FLASHBOTS_RPC = "https://rpc.flashbots.net/fast"

class FlashbotsProtector:
    """Send transactions via Flashbots for MEV protection."""

    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(FLASHBOTS_RPC))
        self.account = Account.from_key(os.getenv("PRIVATE_KEY"))

    async def send_protected_transaction(
        self,
        to: str,
        data: str,
        value: int = 0,
        gas_limit: int = None
    ) -> str:
        """Send transaction via Flashbots Protect."""

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

    def get_private_rpc(self) -> str:
        """Get Flashbots private RPC URL."""
        return FLASHBOTS_RPC
```

### MEV Blocker Alternative

```python
# scripts/mev_blocker.py
MEV_BLOCKER_RPC = "https://rpc.mevblocker.io"

class MEVBlockerProtector:
    """Alternative MEV protection via MEV Blocker."""

    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(MEV_BLOCKER_RPC))
        self.account = Account.from_key(os.getenv("PRIVATE_KEY"))

    async def send_protected_transaction(self, to: str, data: str, value: int = 0) -> str:
        """Send via MEV Blocker (90% backrun MEV returned to user)."""

        tx = {
            "from": self.account.address,
            "to": to,
            "data": data,
            "value": value,
            "gas": 500000,
            "maxFeePerGas": self.w3.eth.gas_price * 2,
            "maxPriorityFeePerGas": self.w3.to_wei(1, "gwei"),
            "nonce": self.w3.eth.get_transaction_count(self.account.address),
            "chainId": 1
        }

        signed = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)

        return tx_hash.hex()
```

## Address Risk Analysis

### Malicious Address Check

```python
# scripts/address_risk.py
import aiohttp
from spoon_ai.tools.base import BaseTool
from pydantic import Field

class AddressRiskTool(BaseTool):
    name: str = "address_risk"
    description: str = "Check if address is associated with scams/hacks"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "address": {"type": "string"}
        },
        "required": ["address"]
    })

    async def execute(self, address: str) -> str:
        url = f"{GOPLUS_API}/address_security/{address}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return f"Error checking address"

                data = await resp.json()

        result = data.get("result", {})

        risks = []

        if result.get("cybercrime") == "1":
            risks.append("CYBERCRIME: Associated with crypto crimes")
        if result.get("money_laundering") == "1":
            risks.append("MONEY LAUNDERING: Flagged for laundering")
        if result.get("financial_crime") == "1":
            risks.append("FINANCIAL CRIME: Involved in fraud")
        if result.get("darkweb_transactions") == "1":
            risks.append("DARKWEB: Transactions with darkweb")
        if result.get("phishing_activities") == "1":
            risks.append("PHISHING: Known phishing address")
        if result.get("contract_address") == "1":
            risks.append("INFO: This is a contract address")

        if not risks:
            return f"Address {address}: No known risks detected"

        report = f"ADDRESS RISK REPORT\n{'='*40}\n{address}\n\n"
        for risk in risks:
            report += f"  - {risk}\n"

        return report
```

## Comprehensive Security Tool

```python
# scripts/security_analyzer.py
from spoon_ai.tools.base import BaseTool
from pydantic import Field

class SecurityAnalyzerTool(BaseTool):
    name: str = "security_analyzer"
    description: str = "Comprehensive security analysis for tokens and addresses"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "target": {"type": "string", "description": "Token or wallet address"},
            "type": {"type": "string", "enum": ["token", "address", "transaction"]},
            "chain": {"type": "string", "default": "ethereum"}
        },
        "required": ["target", "type"]
    })

    async def execute(self, target: str, type: str, chain: str = "ethereum") -> str:
        if type == "token":
            # Run token security + honeypot check
            token_tool = TokenSecurityTool()
            honeypot_tool = HoneypotCheckTool()

            token_result = await token_tool.execute(target, chain)
            honeypot_result = await honeypot_tool.execute(target, chain)

            return f"{token_result}\n\n{honeypot_result}"

        elif type == "address":
            risk_tool = AddressRiskTool()
            return await risk_tool.execute(target)

        elif type == "transaction":
            # Would need tx data for simulation
            return "Transaction simulation requires calldata. Use simulate_transaction tool."
```

## Environment Variables

```bash
# GoPlus (optional - has free tier)
GOPLUS_API_KEY=...

# Tenderly (required for simulation)
TENDERLY_ACCOUNT=...
TENDERLY_PROJECT=...
TENDERLY_API_KEY=...

# Wallet
PRIVATE_KEY=0x...
WALLET_ADDRESS=0x...
```

## Best Practices

1. **Always Check Before Swap** - Run token security before any trade
2. **Simulate First** - Use Tenderly before large transactions
3. **Use MEV Protection** - Route swaps through Flashbots/MEV Blocker
4. **Verify Addresses** - Check counterparty addresses for risks
5. **Monitor Approvals** - Regularly audit token approvals
