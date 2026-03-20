---
name: bittensor-sdk
description: Comprehensive Bittensor blockchain interaction skill with wallet management, staking, subnet operations, neuron registration, and emissions tracking. Use for: bittensor operations, subtensor queries, stake/unstake TAO, register neurons, query subnet info, wallet operations, metagraph analysis, emissions tracking, and weight management.
license: MIT
compatibility: Requires Python 3.8+, bittensor>=8.0.0, network access to Bittensor network endpoints
metadata:
  author: bittensor_quest
  version: "1.0.0"
---

# Bittensor SDK Skill

Comprehensive Bittensor blockchain interaction skill for agents. Enables seamless interaction with the Bittensor decentralized AI network through the Python SDK.

## Overview

Bittensor is a decentralized machine learning network where independent subnets compete for TAO token emissions. This skill provides agents with full access to:

- **Wallet Management**: Coldkey/hotkey operations, proxy relationships
- **Staking Operations**: Stake/unstake TAO, auto-staking, safe staking
- **Subnet Management**: Query subnet info, hyperparameters, registration
- **Neuron Operations**: Register neurons, query metagraphs, weight management
- **Emissions & Rewards**: Track emissions, claim root dividends, reward distribution

## Key Concepts

### Core Terminology

- **Coldkey**: User's main wallet key for transfers and overall wallet management
- **Hotkey**: Key used for neuron operations (mining/validation)
- **Netuid**: Unique identifier for a subnet (0 = Root Subnet)
- **UID**: Unique identifier for a neuron on a specific subnet
- **Metagraph**: Complete state of a subnet at a given block
- **TAO**: Base network token (1 TAO = 1e9 Rao)
- **Alpha**: Subnet-specific token representing staked TAO
- **Rao**: Smallest unit of TAO

### Network Types

- **finney**: Bittensor mainnet
- **test**: Bittensor test network
- **local**: Locally deployed blockchain

## Installation

### Prerequisites

```bash
pip install bittensor>=8.0.0
```

### Opencode Installation

```bash
cp -r skills/bittensor-sdk ~/.opencode/skills/
```

## How It Works

### 1. Initialization

The skill initializes the Subtensor interface for blockchain interaction:

```python
import bittensor as bt

# Connect to mainnet
subtensor = bt.Subtensor(network="finney")

# Connect to testnet
subtensor = bt.Subtensor(network="test")

# Custom network with fallback endpoints
subtensor = bt.Subtensor(
    network="finney",
    fallback_endpoints=["wss://entrypoint-finney.opentensor.ai:443"],
    retry_forever=True
)
```

### 2. Wallet Setup

```python
from bittensor import wallet

# Load existing wallet
wallet = bt.Wallet()

# Create new wallet
wallet = bt.Wallet(name="my_wallet", hotkey="miner1")

# Check balances
coldkey_balance = wallet.coldkey_balance
print(f"Coldkey balance: {coldkey_balance}")
```

### 3. Core Operations

#### Query Subnet Information

```python
# Get all subnet netuids
netuids = subtensor.get_all_subnets_netuid()
print(f"Available subnets: {netuids}")

# Get detailed subnet info
subnet_info = subtensor.get_subnet_info(netuid=1)
print(f"Subnet 1 info: {subnet_info}")
```

#### Stake TAO

```python
from bittensor import Balance

# Stake TAO to a hotkey
amount = Balance.from_tao(10.0)  # 10 TAO
result = subtensor.add_stake(
    wallet=wallet,
    netuid=1,
    hotkey_ss58="5Hx...",  # Hotkey SS58 address
    amount=amount,
    safe_staking=True,     # Enable price protection
    allow_partial_stake=True
)
print(f"Stake result: {result}")
```

#### Register Neuron

```python
# Burned registration (recycle TAO)
result = subtensor.burned_register(
    wallet=wallet,
    netuid=1
)

# POW registration (computational proof)
result = subtensor.register(
    wallet=wallet,
    netuid=1
)
```

#### Query Metagraph

```python
# Get metagraph for a subnet
metagraph = subtensor.metagraph(netuid=1)

print(f"Number of neurons: {metagraph.n}")
print(f"Stake per neuron: {metagraph.S}")
print(f"Rewards: {metagraph.R}")
print(f"Hotkeys: {metagraph.hotkeys}")
```

#### Set Weights

```python
import numpy as np

# Validator sets weights for miners
uids = np.array([0, 1, 2, 3, 4])  # Miner UIDs
weights = np.array([0.2, 0.3, 0.2, 0.15, 0.15])  # Normalized weights

result = subtensor.set_weights(
    wallet=validator_wallet,
    netuid=1,
    uids=uids,
    weights=weights,
    wait_for_inclusion=True,
    wait_for_finalization=True
)
```

## Usage Examples

### Example 1: Complete Miner Setup

```python
import bittensor as bt
from bittensor import Balance
import numpy as np

# Initialize
subtensor = bt.Subtensor(network="finney")
wallet = bt.Wallet(name="miner_wallet", hotkey="miner1")

# Check balance
balance = subtensor.get_balance(wallet.coldkey.ss58_address)
print(f"Balance: {balance.tao} TAO")

# Register on subnet 1
print("Registering neuron...")
result = subtensor.register(
    wallet=wallet,
    netuid=1,
    wait_for_inclusion=True
)

# Get metagraph info
metagraph = subtensor.metagraph(netuid=1)
print(f"Neurons on subnet 1: {metagraph.n}")

# Check my neuron
my_uid = metagraph.hotkeys.index(wallet.hotkey.ss58_address)
my_neuron = metagraph.neurons[my_uid]
print(f"My UID: {my_uid}")
print(f"My stake: {my_neuron.stake}")
print(f"My emission: {my_neuron.emission}")
```

### Example 2: Validator Operations

```python
import bittensor as bt
from bittensor import Balance
import numpy as np

# Initialize
subtensor = bt.Subtensor(network="finney")
validator_wallet = bt.Wallet(name="validator", hotkey="val1")

# Get metagraph
metagraph = subtensor.metagraph(netuid=1)
print(f"Total miners: {metagraph.n}")

# Calculate weights based on performance
weights = np.zeros(metagraph.n)
for i in range(metagraph.n):
    weights[i] = metagraph.R[i] * 0.7 + metagraph.S[i] * 0.3

# Normalize weights
weights = weights / weights.sum()

# Set weights
result = subtensor.set_weights(
    wallet=validator_wallet,
    netuid=1,
    uids=np.arange(metagraph.n),
    weights=weights,
    wait_for_inclusion=True,
    wait_for_finalization=True
)

print(f"Weights set: {result.success}")
```

## Troubleshooting

### Connection Issues

**Problem**: Unable to connect to network
**Solution**:
```python
# Use fallback endpoints
subtensor = bt.Subtensor(
    network="finney",
    fallback_endpoints=[
        "wss://entrypoint-finney.opentensor.ai:443",
        "wss://finney.opentensor.io:443"
    ],
    retry_forever=True
)
```

### Rate Limiting

**Problem**: Too many requests error
**Solution**:
```python
import time
time.sleep(1)  # Rate limit delays
```

### Registration Failures

**Problem**: Registration fails repeatedly
**Solutions**:
1. Check balance (need > 1 TAO for burn registration)
2. Verify POW solution is correct
3. Check network connectivity
4. Try different registration method

### Wallet Issues

**Problem**: Wallet not found
**Solution**:
```python
# Create new wallet
wallet = bt.Wallet(name="new_wallet", hotkey="new_hotkey")
wallet.create_if_non_existing()
```

## Best Practices

1. **Always close connections**: Use `subtensor.close()` when done
2. **Handle errors gracefully**: Use try-except blocks
3. **Implement rate limiting**: Don't exceed network limits
4. **Use MEV protection**: Enable for large transactions
5. **Monitor emissions**: Track network health
6. **Use safe staking**: Enable price protection
7. **Keep keys secure**: Never expose private keys

## Security Considerations

1. **Private keys**: Never expose or log private keys
2. **Seed phrases**: Store securely, never share
3. **Transaction signing**: Always verify before signing
4. **MEV protection**: Enable for large transactions
5. **Proxy permissions**: Understand proxy types before delegating
6. **Rate limiting**: Prevent DoS by respecting limits

## Present Results to Users

When presenting Bittensor SDK results to users:

1. **Format TAO amounts clearly**: Show both TAO and Rao when relevant
2. **Explain network concepts**: Clarify coldkey/hotkey, netuid, UID for non-technical users
3. **Highlight key metrics**: Emphasize important values like stake, emission, registration costs
4. **Include relevant links**: Link to documentation for deeper exploration
5. **Note risks**: Highlight potential issues like deregistration risk, rate limits

Example output format:
```
=== Subnet 1 Status ===
Neurons: 256 registered
Total Stake: 125,450.5 TAO
Emission: 0.123 TAO/block
Registration Cost: 5.2 TAO
Validator Take: 18%
═══════════════════════════════════
```

## References

- [Bittensor Documentation](https://docs.bittensor.com/)
- [Bittensor SDK Reference](https://bittensor-sdk.readthedocs.io/)
- [Learn Bittensor](https://docs.learnbittensor.org/)
- [Taostats API](https://dash.taostats.io/)
- [Bittensor GitHub](https://github.com/opentensor)

## Detailed Documentation

For complete API reference, extended examples, and comprehensive troubleshooting, see:
- [API Reference](references/API_REFERENCE.md) - Complete method documentation
- [Extended Examples](references/API_REFERENCE.md#extended-examples) - Advanced usage patterns
- [Quick Reference](references/API_REFERENCE.md#quick-reference-card) - Common operations summary
