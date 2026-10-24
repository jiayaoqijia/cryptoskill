# Google Antigravity Proof-of-Escrow Integration

Zero-dependency standard-library tools for [Google Antigravity](https://antigravity.google) and autonomous AI coding agents to verify on-chain bounty escrows before spending compute.

## Quickstart

```bash
python -m unittest tests.test_antigravity_integration -v
```

```python
from integrations.antigravity.doomsday_antigravity_tools import antigravity_tools

# Attach tools to your Antigravity agent or subagent definition
tools = antigravity_tools()
```

## Features

- **Standard Library Only**: No external dependencies (`requests`, `pydantic`, etc. not required).
- **Proof-of-Escrow Verification**: Validates issue lock status, vault addresses, and `wDOOM` Base Mainnet contracts (`0x623c84A5E04bF715018203334b0eFE41696eBC3E`).
- **Defensive Input Handling**: Automatically filters malformed repository references and addresses before making network calls.
