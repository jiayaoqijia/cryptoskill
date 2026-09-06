---
name: bittensor-sdk
description: "Complete Bittensor SDK reference — Subtensor, AsyncSubtensor, Metagraph, Axon, Dendrite, Synapse, chain_data models, extrinsics (sync + async), extras (subtensor_api, dev_framework, timelock), and utils (balance, btlogging, weight_utils, registration, liquidity, networking, version). Use for any bittensor operation: wallet management, staking, subnet ops, neuron registration, metagraph queries, emissions tracking, liquidity management, MEV protection, proxy delegation, coldkey swaps, crowdloans, weight setting, and more."
license: MIT
compatibility: Requires Python 3.8+, bittensor>=8.0.0, network access to Bittensor network endpoints
metadata:
  author: taoli
  twitter: taoleeh
  github: taoleeh
  website: bittensor.quest
  version: "2.0.0"
---

# Bittensor SDK — Complete API Reference

Comprehensive reference for the Bittensor Python SDK. Based on the full autoapi documentation.

## Package Structure

```
bittensor/
├── core/
│   ├── subtensor          — Synchronous blockchain interface (main class)
│   ├── async_subtensor     — Asynchronous blockchain interface
│   ├── metagraph           — Subnet state representation (sync/async/torch/nontorch)
│   ├── axon                — Server-side neuron endpoint (FastAPI)
│   ├── dendrite            — Client-side network request sender
│   ├── synapse             — Communication schema between neurons (Pydantic)
│   ├── stream              — Streaming response model
│   ├── tensor              — Tensor serialization utilities
│   ├── threadpool          — Priority thread pool for Axon
│   ├── config              — Configuration management
│   ├── settings            — Default settings
│   ├── types               — Shared type aliases and mixins
│   ├── errors              — Exception hierarchy
│   ├── chain_data/         — 26 data models for chain state
│   └── extrinsics/         — Sync + async extrinsic operations + pallet definitions
├── extras/
│   ├── subtensor_api/      — High-level SubtensorApi wrapper with 14 sub-APIs
│   ├── dev_framework/      — Test framework with ~184 namedtuple call blueprints
│   └── timelock/           — Drand-based time-lock encryption
└── utils/
    ├── balance             — Balance type (TAO/Rao conversion)
    ├── btlogging/          — Custom logging subsystem (6 modules)
    ├── weight_utils        — Weight normalization/conversion (12 functions)
    ├── registration/       — Registration utilities + torch compat
    ├── liquidity           — Uniswap V3-style liquidity math
    ├── networking          — IP/port utilities
    ├── formatting          — Human-readable number formatting
    ├── subnets             — Community SubnetsAPI base class
    ├── version             — PyPI version checker
    ├── axon_utils          — Nonce window calculations
    └── easy_imports        — Centralized import hub
```

## Quick Start

```python
import bittensor as bt

# Connect to network
subtensor = bt.Subtensor(network="finney")
# or async:
# subtensor = bt.AsyncSubtensor(network="finney")

# Wallet
wallet = bt.Wallet(name="my_wallet", hotkey="my_hotkey")

# Metagraph
metagraph = subtensor.metagraph(netuid=1)

# Stake
from bittensor import Balance
subtensor.add_stake(wallet, netuid=1, hotkey_ss58=wallet.hotkey.ss58_address,
                    amount=Balance.from_tao(10.0))

# Set weights
import numpy as np
subtensor.set_weights(wallet, netuid=1, uids=np.array([0,1,2]),
                      weights=np.array([0.3, 0.4, 0.3]))
```

## Core Modules

### bittensor.core.subtensor — Subtensor (Synchronous)

```python
Subtensor(network=None, config=None, log_verbose=False, fallback_endpoints=None,
          retry_forever=False, archive_endpoints=None, mock=False)
```

**Staking & Liquidity:**
- `add_stake(wallet, netuid, hotkey_ss58, amount, safe_staking=False, allow_partial_stake=False, rate_tolerance=0.005, ...)` — Stake TAO
- `add_stake_burn(wallet, netuid, hotkey_ss58, amount, limit_price=None, ...)` — Subnet buyback
- `add_stake_multiple(wallet, netuids, hotkey_ss58s, amounts, ...)` — Bulk stake
- `add_liquidity(wallet, netuid, liquidity, price_low, price_high, hotkey_ss58=None, ...)` — Add liquidity
- `remove_liquidity(wallet, netuid, position_id, hotkey_ss58=None, ...)` — Remove liquidity
- `modify_liquidity(wallet, netuid, position_id, liquidity_delta, hotkey_ss58=None, ...)` — Modify position
- `move_stake(wallet, origin_netuid, origin_hotkey, dest_netuid, dest_hotkey, amount, ...)` — Move stake between subnets
- `swap_stake(wallet, origin_netuid, dest_netuid, hotkey_ss58, amount, limit_price=None, ...)` — Swap Alpha between subnets
- `transfer_stake(wallet, origin_netuid, dest_netuid, dest_coldkey, hotkey_ss58, amount, ...)` — Transfer stake to new owner
- `unstake(wallet, netuid, hotkey_ss58, amount, ...)` — Unstake partial
- `unstake_all(wallet, hotkey_ss58, ...)` — Unstake all
- `unstake_multiple(wallet, netuids, hotkey_ss58s, amounts, ...)` — Bulk unstake

**Registration:**
- `register(wallet, netuid, ...)` — POW registration
- `burned_register(wallet, netuid, ...)` — Burn registration (recycle TAO)
- `register_limit(wallet, netuid, limit_price, ...)` — Registration with price cap
- `root_register(wallet, ...)` — Root network registration

**Weights:**
- `set_weights(wallet, netuid, uids, weights, version_key=..., ...)` — Direct weight setting
- `commit_weights(wallet, netuid, salt, uids, weights, mechid=0, ...)` — Commit-reveal step 1
- `reveal_weights(wallet, netuid, uids, weights, salt, ...)` — Commit-reveal step 2
- `commit_reveal_enabled(netuid, block=None)` — Check if commit-reveal is active

**Serving:**
- `serve_axon(wallet, netuid, ip, port, protocol, version, ...)` — Register axon endpoint
- `serve_axon_tls(wallet, netuid, ip, port, protocol, version, certificate, ...)` — Register TLS axon
- `serve_prometheus(wallet, netuid, ip, port, version, ...)` — Register Prometheus endpoint

**Proxy & Delegation:**
- `add_proxy(wallet, delegate_ss58, proxy_type, delay, ...)` — Add proxy relationship
- `remove_proxy(wallet, delegate_ss58, proxy_type, delay, ...)` — Remove proxy
- `remove_proxies(wallet, ...)` — Remove all proxies
- `announce_proxy(wallet, real_account_ss58, call_hash, ...)` — Announce proxy call
- `proxy(wallet, real_account_ss58, call, ...)` — Execute via proxy

**Coldkey Swaps:**
- `announce_coldkey_swap(wallet, new_coldkey_ss58, ...)` — Announce swap intent
- `swap_coldkey_announced(wallet, new_coldkey_ss58, ...)` — Execute announced swap
- `clear_coldkey_swap_announcement(wallet, ...)` — Withdraw announcement
- `dispute_coldkey_swap(wallet, ...)` — Dispute active swap

**Root Operations:**
- `claim_root(wallet, netuids, ...)` — Claim root dividends
- `set_root_claim_type(wallet, new_root_claim_type, ...)` — Set root claim mechanism

**Children (Child-Hotkeys):**
- `set_children(wallet, netuid, hotkey, children, ...)` — Set child hotkeys
- `get_children(netuid, hotkey_ss58, block=None)` — Get children of hotkey

**Queries (read-only, no wallet needed):**
- `metagraph(netuid, block=None)` — Get metagraph
- `get_subnet_info(netuid, block=None)` — Get subnet details
- `all_subnets(block=None)` — All subnets with parameters
- `get_balance(address, block=None)` — Get coldkey balance
- `get_stake(coldkey_ss58, hotkey_ss58, netuid, block=None)` — Get stake amount
- `get_total_subnets(block=None)` — Total subnet count
- `subnet_exists(netuid, block=None)` — Check subnet exists
- `is_hotkey_registered(netuid, hotkey_ss58, block=None)` — Check registration
- `get_uid_for_hotkey(netuid, hotkey_ss58, block=None)` — Get neuron UID
- `bonds(netuid, mechid=0, block=None)` — Bond distribution
- `weights(netuid, mechid=0, block=None)` — Weight matrix
- `tempo(netuid, block=None)` — Subnet tempo
- `difficulty(netuid, block=None)` — POW difficulty
- `immunity_period(netuid, block=None)` — Immunity period
- `blocks_since_last_step(netuid, block=None)` — Blocks since last epoch
- `blocks_until_next_epoch(netuid, block=None)` — Blocks until next epoch
- `get_subnet_burn_cost(netuid, block=None)` — Burn registration cost
- `get_subnet_price(netuid, block=None)` — Current Alpha/TAO price
- `get_subnet_prices(block=None)` — All subnet prices
- `get_subnet_hyperparameters(netuid, block=None)` — Hyperparameters
- `get_subnet_reveal_period_epochs(netuid, block=None)` — Reveal period
- `get_delegate_by_hotkey(hotkey_ss58, block=None)` — Delegate info
- `get_delegates(block=None)` — All delegates
- `get_delegated(coldkey_ss58, block=None)` — Delegation status
- `get_coldkey_swap_announcement(coldkey_ss58)` — Swap announcement
- `get_mev_shield_current_key()` — MEV shield key
- `close()` — Close connection

**~130+ total methods** on Subtensor class. Many methods accept these common keyword args:
`mev_protection=DEFAULT_MEV_PROTECTION`, `period=DEFAULT_PERIOD`, `raise_error=False`,
`wait_for_inclusion=True`, `wait_for_finalization=True`, `wait_for_revealed_execution=True`

### bittensor.core.async_subtensor — AsyncSubtensor

Identical API to Subtensor but all methods are `async`. Takes same constructor args:

```python
AsyncSubtensor(network=None, config=None, log_verbose=False, fallback_endpoints=None,
               retry_forever=False, archive_endpoints=None, websocket_shutdown_timer=5.0, mock=False)
```

All ~130+ methods match Subtensor but are `await`-able. Use when building async applications (FastAPI miners/validators).

### bittensor.core.metagraph — Metagraph

```python
Metagraph(netuid, mechid=0, network=DEFAULT_NETWORK, lite=True, sync=True, subtensor=None)
AsyncMetagraph(netuid, mechid=0, network=DEFAULT_NETWORK, lite=True, sync=True, subtensor=None)
TorchMetagraph(netuid, ...)   # PyTorch tensor attributes
NonTorchMetagraph(netuid, ...)  # NumPy array attributes
MetagraphMixin(netuid, ...)    # Abstract base
```

Key attributes: `n`, `S` (stake), `R` (rewards), `I` (incentive), `T` (trust), `C` (consensus), `hotkeys`, `coldkeys`, `uids`, `axon_infos`, `neurons`, `W` (weights), `bonds`, `emission`, `dividends`, `active`, `last_update`, `block`

Methods: `sync(block=None, lite=None, subtensor=None)`, `save(root_dir=None)`, `load(root_dir=None)`, `state_dict()`, `metadata()`

Factory: `async_metagraph(netuid, ...)` — Creates pre-synced AsyncMetagraph

### bittensor.core.axon — Axon (Server)

```python
Axon(wallet=None, config=None, port=None, ip=None, external_ip=None,
     external_port=None, max_workers=None)
```

Key methods:
- `attach(forward_fn, blacklist_fn=None, priority_fn=None, verify_fn=None)` — Register handlers
- `serve(netuid, subtensor=None, certificate=None)` — Register on-chain
- `start()` / `stop()` — Server lifecycle
- `info()` — Get AxonInfo
- `default_verify(synapse)` — Signature verification middleware
- `verify_body_integrity(request)` — Request body integrity check

Also: `AxonMiddleware` (Starlette middleware for request processing), `FastAPIThreadedServer` (uvicorn in a thread)

### bittensor.core.dendrite — Dendrite (Client)

```python
Dendrite(wallet=None)
DendriteMixin(wallet=None)  # Shared base
```

Key methods:
- `query(target_axon, synapse, timeout=12.0)` — Sync query to axon(s)
- `aquery(target_axon, synapse, timeout=12.0)` — Async query
- `preprocess_synapse_for_request(target_axon_info, synapse, timeout=12.0)` — Build headers + sign
- `process_server_response(server_response, json_response, local_synapse)` — Merge server state
- `close_session()` / `aclose_session()` — Cleanup

### bittensor.core.synapse — Synapse

```python
Synapse()           # Base (Pydantic BaseModel)
TerminalInfo()      # Neuron metadata carrier
```

Synapse methods: `deserialize()`, `get_total_size()`, `to_headers()`, `from_headers(headers)`, `body_hash()`, `parse_headers_to_inputs(headers)`, `get_required_fields()`

TerminalInfo: `cast_float(raw)`, `cast_int(raw)`, `get_size(obj)`

### bittensor.core.stream — BTStreamingResponseModel

Streaming response support for large data transfers between neurons.

### bittensor.core.threadpool — PriorityThreadPoolExecutor

Priority-based thread pool used internally by Axon for request handling.

### bittensor.core.tensor

Tensor serialization utilities for network communication.

### bittensor.core.config — Config

Configuration object parsed from CLI args. Used throughout the framework.

### bittensor.core.settings — DEFAULTS

Default settings: axon (ip, port, max_workers), logging (debug, trace, info, logging_dir), priority (max_workers, maxsize), subtensor (chain_endpoint, network), wallet (name, hotkey, path).

### bittensor.core.types

Shared types: `AxonInfo`, `PrometheusInfo`, `SubnetInfo`, `NeuronInfo`, `NeuronInfoLite`, `DelegateInfo`, `StakeInfo`, `ProposalVoteData`, etc. Also `SubtensorMixin` base class.

### bittensor.core.errors

Exception hierarchy: `ChainConnectionError`, `ChainTransactionError`, `IdentityError`, `StakeError`, `MetadataError`, `PriorityException`, `AxonException`, `DendriteException`, `SynapseException`, `StreamException`, `ConfigException`, etc.

## Chain Data Models (26 modules)

All under `bittensor.core.chain_data`:

| Model | Description |
|-------|-------------|
| `AxonInfo` | Neuron axon endpoint: ip, port, ip_type, protocol, version, placeholder1/2 |
| `ChainIdentity` | On-chain identity: name, url, description, discord, github_repo, additional |
| `ColdkeySwap` | Coldkey swap execution data |
| `CrowdloanInfo` | Crowdloan details: id, cap, raised, end, min_contribution, target |
| `DelegateInfo` | Delegate: hotkey_ss58, total_stake, take, nominators, owner_ss58 |
| `DelegateInfoLite` | Lightweight delegate info |
| `DynamicInfo` | Subnet dynamic parameters |
| `InfoBase` | Base dataclass for all info types |
| `IPInfo` | IP: ip, ip_type, port, protocol |
| `MetagraphInfo` | Metagraph metadata |
| `NeuronInfo` | Full neuron: hotkey, coldkey, uid, netuid, stake, rank, trust, incentive, emission, axon_info, prometheus_info, etc. |
| `NeuronInfoLite` | Lightweight neuron info |
| `PrometheusInfo` | Prometheus endpoint: ip, port, version |
| `ProposalVoteData` | Governance proposal vote data |
| `Proxy` | Proxy relationship: delegate, proxy_type, delay |
| `RootClaim` | Root claim data |
| `ScheduledColdkeySwapInfo` | Scheduled swap details |
| `SimSwap` | Simulated swap result |
| `StakeInfo` | Stake: hotkey_ss58, coldkey_ss58, stake |
| `SubnetHyperparameters` | Full hyperparameter set for a subnet |
| `SubnetIdentity` | Subnet identity: subnet_name, subnet_url, subnet_contact, logo_url, description, discord, github_repo, additional |
| `SubnetInfo` | Subnet: netuid, owner, tempo, emission, dynamic_info |
| `SubnetState` | Subnet state data |
| `WeightCommitInfo` | Weight commit-reveal info |
| `utils` | Chain data utility functions |

## Extrinsics — Pallet Operations

### Sync Extrinsics (`bittensor.core.extrinsics`)

Each module provides functions that compose and submit extrinsics:

- `staking` — add_stake, add_stake_burn, add_stake_multiple, move_stake, swap_stake, transfer_stake, unstake, unstake_all, unstake_multiple
- `unstaking` — remove_stake, remove_stake_limit, remove_stake_full_limit, unstake_all_alpha
- `registration` — burned_register, register, register_limit, root_register
- `weights` — set_weights, commit_weights, reveal_weights, batch_set_weights, batch_commit_weights, batch_reveal_weights
- `serving` — serve_axon, serve_axon_tls, serve_prometheus
- `root` — claim_root, root_register, root_dissolve_network, set_root_claim_type
- `proxy` — add_proxy, remove_proxy, remove_proxies, announce_proxy, proxy, proxy_announced
- `transfer` — transfer, transfer_stake
- `coldkey_swap` — announce_coldkey_swap, swap_coldkey, swap_coldkey_announced, clear_coldkey_swap_announcement, dispute_coldkey_swap
- `crowdloan` — create, contribute, dissolve, finalize, refund, update_cap, update_end, update_min_contribution, withdraw
- `liquidity` — add_liquidity, remove_liquidity, modify_liquidity, toggle_user_liquidity, swap_stake
- `mev_shield` — mev_submit_encrypted
- `take` — increase_take, decrease_take
- `children` — set_children, swap_hotkey
- `sudo` — Admin/root operations
- `start_call` — Start call
- `move_stake` — move_stake, swap_stake, transfer_stake
- `utils` — Helper utilities

### Async Extrinsics (`bittensor.core.extrinsics.asyncex`)

Identical module structure but async versions. All functions are `async def`.

### Pallet Definitions (`bittensor.core.extrinsics.pallets`)

Constants for pallet names used in extrinsics:

- `admin_utils` — Admin utility pallet constants
- `balances` — Balance transfer constants (Transfer, TransferKeepAlive, TransferAllowDeath, etc.)
- `base` — Base pallet shared types
- `commitments` — Commitment pallet
- `crowdloan` — Crowdloan pallet
- `mev_shield` — MEV shield pallet
- `proxy` — Proxy pallet types
- `subtensor_module` — Main SubtensorModule pallet
- `sudo` — Sudo pallet
- `swap` — Swap pallet

## Extras

### bittensor.extras.subtensor_api — SubtensorApi

High-level wrapper providing a unified interface over both Subtensor and AsyncSubtensor:

```python
SubtensorApi(network=None, config=None, async_subtensor=False, legacy_methods=False,
             fallback_endpoints=None, retry_forever=False, log_verbose=False,
             mock=False, archive_endpoints=None, websocket_shutdown_timer=5.0)
```

Properties (each returns a sub-API instance):
- `.chain` — `Chain`: get_current_block, get_block_hash, get_timestamp, state_call, tx_rate_limit, is_fast_blocks, last_drand_round, get_existential_deposit, get_minimum_required_stake, etc. (15 methods)
- `.commitments` — `Commitments`: get_commitment, get_all_commitments, set_commitment, commit_reveal_enabled, etc. (12 methods)
- `.crowdloans` — `Crowdloans`: create_crowdloan, contribute_crowdloan, dissolve_crowdloan, finalize_crowdloan, get_crowdloans, etc. (14 methods)
- `.delegates` — `Delegates`: get_delegates, get_delegate_by_hotkey, get_delegate_take, set_delegate_take, get_delegated, etc. (7 methods)
- `.extrinsics` — `Extrinsics`: add_stake, set_weights, burned_register, serve_axon, etc. (45 methods)
- `.metagraphs` — `Metagraphs`: metagraph, get_metagraph_info, get_all_metagraphs_info
- `.mev_shield` — `MevShield`: get_mev_shield_current_key, get_mev_shield_next_key, mev_submit_encrypted
- `.neurons` — `Neurons`: neurons, neurons_lite, neuron_for_uid, query_identity, get_neuron_certificate
- `.proxies` — `Proxy`: add_proxy, remove_proxy, get_proxies, etc. (16 methods)
- `.queries` — `Queries`: query_subtensor, query_map, query_constant, query_module, query_runtime_api
- `.staking` — `Staking`: add_stake, unstake, move_stake, swap_stake, claim_root, get_stake, etc. (30 methods)
- `.subnets` — `Subnets`: all_subnets, get_subnet_info, get_subnet_hyperparameters, register, etc. (45 methods)
- `.utils` — Utility functions
- `.wallets` — `Wallets`: get_balance, get_balances, transfer, get_stake, is_hotkey_registered, etc. (35 methods)

Each sub-API class takes `subtensor: Union[Subtensor, AsyncSubtensor]` and supports both sync and async.

### bittensor.extras.dev_framework — Test Framework

**calls module:** ~184 namedtuple call blueprints for constructing extrinsics. Divided into:
- `non_sudo_calls` (~100 namedtuples): ADD_STAKE, SET_WEIGHTS, REGISTER, BURNED_REGISTER, COMMIT_WEIGHTS, REVEAL_WEIGHTS, TRANSFER, etc.
- `sudo_calls` (~84 namedtuples): SUDO_SET_TEMPO, SUDO_SET_DIFFICULTY, SUDO_SET_MAX_ALLOWED_UIDS, etc.
- `pallets` (string constants): AdminUtils, Balances, Commitments, Crowdloan, MevShield, Proxy, SubtensorModule, Sudo, Swap, etc.

**subnet module:** `TestSubnet` class for test subnet lifecycle management.

**utils module:** `ActivateSubnet`, `RegisterNeuron`, `RegisterSubnet` helpers.

### bittensor.extras.timelock — Time-Lock Encryption

Drand QuickNet-based TLE:

```python
encrypt(data, n_blocks, block_time=12.0) -> tuple  # (encrypted_data, reveal_round)
decrypt(encrypted_data, no_errors=True, return_str=False)
wait_reveal_and_decrypt(encrypted_data, reveal_round=None, no_errors=True, return_str=False) -> bytes
```

Use `block_time=0.25` for fast-blocks nodes.

## Utils

### bittensor.utils.balance — Balance

```python
Balance(balance: int | float)  # int=rao, float=tao
```

Static methods: `from_tao(amount)`, `from_rao(amount)`, `from_float(amount)`, `get_unit(netuid)`
Properties: `tao` (float), `rao` (int), `unit` (str), `rao_unit` (str)
Helpers: `tao(amount, netuid=0) -> Balance`, `rao(amount, netuid=0) -> Balance`

### bittensor.utils.btlogging — Logging

Custom logging subsystem with state machine:

```python
LoggingMachine(config, name="bittensor")  # StateMachine + logging.Logger
```

States: Default, Debug, Trace, Info, Warning, Disabled
Methods: `debug()`, `info()`, `warning()`, `error()`, `success()`, `trace()`, `critical()`, `exception()`
Toggle: `set_debug(on)`, `set_trace(on)`, `set_info(on)`, `on()`, `off()`
Console: `BittensorConsole` with `info()`, `success()`, `warning()`, `error()`, `critical()`, `debug()`
Formatters: `BtFileFormatter`, `BtStreamFormatter` (colors, emojis, millisecond timestamps)
Config: `LoggingConfig` namedtuple — debug, info, trace, record_log, logging_dir, enable_third_party_loggers

Global toggles: `btlogging.debug(on)`, `btlogging.trace(on)`, `btlogging.info(on)`, `btlogging.warning(on)`

### bittensor.utils.weight_utils — Weight Processing (12 functions)

- `normalize_max_weight(x, limit=0.1)` — Normalize with max cap
- `process_weights(uids, weights, num_neurons, min_allowed_weights, max_weight_limit, exclude_quantile=0)` — Full weight processing
- `process_weights_for_netuid(uids, weights, netuid, subtensor, metagraph=None, exclude_quantile=0)` — Subnet-aware processing
- `convert_weights_and_uids_for_emit(uids, weights)` — To chain format
- `convert_weight_uids_and_vals_to_tensor(n, uids, weights)` — From chain format
- `convert_root_weight_uids_and_vals_to_tensor(n, uids, weights, subnets)` — Root weights
- `generate_weight_hash(address, netuid, uids, values, version_key, salt)` — Commit hash

### bittensor.utils.liquidity — Liquidity Math

Uniswap V3-style: `price_to_tick(price)`, `tick_to_price(tick)`, `calculate_fees(...)`, `get_fees(...)`

`LiquidityPosition` dataclass: id, netuid, liquidity, price_low, price_high, fees_tao, fees_alpha
Method: `to_token_amounts(current_subnet_price) -> (alpha_amount, tao_amount)`

### bittensor.utils.networking

`get_external_ip()`, `get_formatted_ws_endpoint_url(url)`, `int_to_ip(int)`, `ip_to_int(str)`, `ip_version(str)`

### bittensor.utils.registration.torch_utils

`LazyLoadedTorch` — lazy torch import proxy
`legacy_torch_api_compat(func)` — Decorator for torch↔numpy compatibility
`use_torch()` — Check/enable torch mode

### bittensor.utils.axon_utils

`allowed_nonce_window_ns(current_time_ns, synapse_timeout)` — Nonce window
`calculate_diff_seconds(current_time, synapse_timeout, synapse_nonce)` — Time diff

### Other Utils

- `bittensor.utils.version`: `check_version(timeout)`, `get_and_save_latest_version(timeout)`
- `bittensor.utils.formatting`: `get_human_readable(num)`, `millify(n)`
- `bittensor.utils.subnets`: `SubnetsAPI(wallet)` — Community ABC for subnet querying
- `bittensor.utils`: `unlock_key(wallet)`, `is_valid_ss58_address(addr)`, `decode_hex_identity_dict(d)`, `format_error_message(err)`, `strtobool(val)`, `float_to_u64(val)`, `u16_normalized_float(x)`, `determine_chain_endpoint_and_network(network)`

## Common Patterns

### MEV Protection

Most extrinsic methods accept these keyword args:
```python
mev_protection=DEFAULT_MEV_PROTECTION  # Enable MEV shielding
period=DEFAULT_PERIOD                   # Blocks to wait for inclusion
raise_error=False                       # Raise on failure instead of returning error
wait_for_inclusion=True                 # Wait for block inclusion
wait_for_finalization=True              # Wait for block finalization
wait_for_revealed_execution=True        # Wait for MEV reveal period
```

### Safe Staking

```python
subtensor.add_stake(wallet, netuid=1, hotkey_ss58=addr, amount=amount,
                    safe_staking=True,       # Price protection
                    allow_partial_stake=True, # Accept partial fill
                    rate_tolerance=0.005)     # 0.5% slippage
```

### Async Pattern

```python
async with bt.AsyncSubtensor(network="finney") as subtensor:
    metagraph = await subtensor.metagraph(netuid=1)
    result = await subtensor.add_stake(wallet, netuid=1, ...)
```

### Using SubtensorApi (Recommended for new code)

```python
api = bt.SubtensorApi(network="finney")
block = api.block
info = api.subnets.get_subnet_info(netuid=1)
stake = api.staking.add_stake(wallet, netuid=1, ...)
```

## Network Types

- `finney` — Mainnet
- `test` — Testnet
- `local` — Local dev chain

## Key Constants

- `RAOPERTAO = 1_000_000_000.0` (1 TAO = 1e9 Rao)
- `U16_MAX = 65535`, `U32_MAX = 4294967295`, `U64_MAX = 18446744073709551615`
- `GLOBAL_MAX_SUBNET_COUNT = 4096`

## Examples

### Complete Miner

```python
import bittensor as bt

subtensor = bt.Subtensor(network="finney")
wallet = bt.Wallet(name="miner", hotkey="hk1")

# Register
subtensor.burned_register(wallet, netuid=1, wait_for_inclusion=True)

# Check position
mg = subtensor.metagraph(netuid=1)
uid = mg.hotkeys.index(wallet.hotkey.ss58_address)
print(f"UID: {uid}, Stake: {mg.S[uid]}, Emission: {mg.emission[uid]}")
```

### Complete Validator

```python
import bittensor as bt
import numpy as np

subtensor = bt.Subtensor(network="finney")
wallet = bt.Wallet(name="validator", hotkey="vk1")

mg = subtensor.metagraph(netuid=1)
weights = np.random.rand(mg.n)
weights = weights / weights.sum()

subtensor.set_weights(wallet, netuid=1, uids=np.arange(mg.n),
                      weights=weights,
                      wait_for_inclusion=True, wait_for_finalization=True)
```

### Axon Server

```python
import bittensor as bt

def forward(synapse): ...
def blacklist(synapse): ...
def priority(synapse): ...

wallet = bt.Wallet(name="miner", hotkey="hk1")
axon = bt.Axon(wallet=wallet, port=8091)
axon.attach(forward_fn=forward, blacklist_fn=blacklist, priority_fn=priority)
axon.serve(netuid=1)
axon.start()
```

### Dendrite Client

```python
import bittensor as bt

dendrite = bt.Dendrite(wallet=bt.Wallet(name="validator", hotkey="vk1"))
metagraph = bt.Subtensor(network="finney").metagraph(netuid=1)
responses = dendrite.query(metagraph.axons, bt.Synapse(), timeout=12)
```

### Liquidity Management

```python
subtensor.add_liquidity(wallet, netuid=1,
                        liquidity=bt.Balance.from_tao(100),
                        price_low=bt.Balance.from_tao(50),
                        price_high=bt.Balance.from_tao(200),
                        wait_for_inclusion=True)
```

### Time-Lock Encryption

```python
from bittensor.extras.timelock import encrypt, decrypt, wait_reveal_and_decrypt

encrypted, reveal_round = encrypt(b"secret data", n_blocks=100)
# Later, after enough blocks...
data = wait_reveal_and_decrypt(encrypted)
```

## Troubleshooting

**Connection issues**: Use fallback endpoints and `retry_forever=True`
```python
subtensor = bt.Subtensor(network="finney",
    fallback_endpoints=["wss://entrypoint-finney.opentensor.ai:443"],
    retry_forever=True)
```

**Registration fails**: Check balance, try alternative method. Use `register_limit()` for price protection.

**Weight setting fails**: Verify commit-reveal cycle. Check `commit_reveal_enabled(netuid)` first.

**Rate limiting**: Space out extrinsics. Use `period=` parameter to control inclusion window.

**Wallet not found**: Use `bt.Wallet(name="...").create_if_non_existing()` or `bt.Wallet(name="...", hotkey="...").regenerate_coldkey(...)`.

## References

- [Bittensor Docs](https://docs.bittensor.com/)
- [Bittensor SDK Reference](https://bittensor-sdk.readthedocs.io/)
- [Learn Bittensor](https://docs.learnbittensor.org/)
- [Taostats API](https://dash.taostats.io/)
- [Bittensor GitHub](https://github.com/opentensor)
- Full autoapi: `references/autoapi/index.md` (133 files, complete SDK API docs)
