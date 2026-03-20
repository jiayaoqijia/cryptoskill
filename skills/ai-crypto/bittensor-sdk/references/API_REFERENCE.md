## bittensor.core.subtensor Print to PDF

## Contents

- Classes
- Module Contents

## Classes

Subtensor

Synchronous interface for interacting with the Bittensor blockchain.

## Module Contents

[source] class bittensor.core.subtensor.Subtensor(network=None, config=None, log\_verbose=False, fallback\_endpoints=None, retry\_forever=False, archive\_endpoints=None, mock=False)

Bases: bittensor.core.types.SubtensorMixin

Synchronous interface for interacting with the Bittensor blockchain.

This class provides a thin layer over the Substrate Interface offering synchronous functionality for Bittensor. This includes frequently-used calls for querying blockchain data, managing stakes and liquidity positions, registering neurons, submitting weights, and many other functions for participating in Bittensor.

<!-- image -->

## Notes

Key Bittensor concepts used throughout this class:

- Coldkey : The key pair corresponding to a user's overall wallet. Used to transfer, stake, manage subnets.
- Hotkey : A key pair (each wallet may have zero, one, or more) used for neuron operations (mining and validation).
- Netuid : Unique identifier for a subnet (0 is the Root Subnet)
- UID : Unique identifier for a neuron registered to a hotkey on a specific subnet.
- Metagraph : Data structure containing the complete state of a subnet at a block.
- TAO : The base network token; subnet 0 stake is in TAO
- Alpha : Subnet-specific token representing some quantity of TAO staked into a subnet.
- Rao : Smallest unit of TAO (1 TAO = 1e9 Rao)
- Bittensor Glossary &lt;https:/ /docs.learnbittensor.org/glossary&gt;
- Wallets, Coldkeys and Hotkeys in Bittensor &lt;https:/ /docs.learnbittensor.org/keys/wallets&gt;

Initializes a Subtensor instance for blockchain interaction.

## Parameters:

- network (Optional[str]) - The network name to connect to (e.g., finney for Bittensor mainnet, test, for Bittensor test network, local for a locally deployed blockchain). If None, uses the default network from config.
- config (Optional[bittensor.core.config.Config]) - Configuration object for the Subtensor instance. If None, uses the default configuration.
- log\_verbose (bool) - Enables or disables verbose logging.
- fallback\_endpoints (Optional[list[str]]) - List of fallback WebSocket endpoints to use if the primary network endpoint is unavailable. These are tried in order when the default endpoint fails.
- retry\_forever (bool) - Whether to retry connection attempts indefinitely on connection errors.
- mock (bool) - Whether this is a mock instance. FOR TESTING ONLY.

- archive\_endpoints (Optional[list[str]]) - List of archive node endpoints for queries requiring historical block data beyond the retention period of lite nodes. These are only used when requesting blocks that the current node is unable to serve.

## Returns:

None add\_liquidity(wallet, netuid, liquidity, price\_low, price\_high, hotkey\_ss 58 =None, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True) Adds liquidity to the specified price range.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet used to sign the extrinsic (must be unlocked).
- netuid (int) - The UID of the target subnet for which the call is being initiated.
- liquidity (bittensor.utils.balance.Balance) - The amount of liquidity to be added.
- price\_low (bittensor.utils.balance.Balance) - The lower bound of the price tick range. In TAO.
- price\_high (bittensor.utils.balance.Balance) - The upper bound of the price tick range. In TAO.
- hotkey\_ss58 (Optional[str]) - The hotkey with staked TAO in Alpha. If not passed then the wallet hotkey is used.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the extrinsic to be included in a block.

[source]

- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

Note: Adding is allowed even when user liquidity is enabled in specified subnet. Call toggle\_user\_liquidity method to enable/disable user liquidity.

add\_proxy(wallet, delegate\_ss 58 , proxy\_type, delay, *, raise\_error=False, wait\_for\_inclusion=True, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Adds a proxy relationship.

This method creates a proxy relationship where the delegate can execute calls on behalf of the real account (the wallet owner) with restrictions defined by the proxy type and a delay period. A deposit is required and held as long as the proxy relationship exists.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor wallet object.
- delegate\_ss58 (str) - The SS58 address of the delegate proxy account.
- proxy\_type (Union[str, bittensor.core.chain\_data.ProxyType]) - The type of proxy permissions (e.g., 'Any', 'NonTransfer', 'Governance', 'Staking'). Can be a string or ProxyType enum value.
- delay (int) - The number of blocks before the proxy can be used.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block

within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the inclusion of the transaction.
- wait\_for\_finalization (bool) - Whether to wait for the finalization of the transaction.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

<!-- image -->

## Notes

- A deposit is required when adding a proxy. The deposit amount is determined by runtime constants and is returned when the proxy is removed. Use get\_proxy\_constants() to check current deposit requirements.
- See: &lt;https:/ /docs.learnbittensor.org/keys/proxies/create-proxy&gt;

add\_stake(wallet, netuid, hotkey\_ss 58 , amount, safe\_staking=False, allow\_partial\_stake=False, rate\_tolerance=0.005, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

[source] Adds stake from the specified wallet to a neuron on a specified subnet.

Staking is a fundamental process in the Bittensor network that enables neurons to participate actively and earn incentives. This method transfers TAO from the coldkey to stake on a hotkey in a specific subnet, converting it to Alpha (subnet-specific token) in the process.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet to be used for staking.
- netuid (int) - The unique identifier of the subnet to which the neuron belongs.
- hotkey\_ss58 (str) - The SS58 address of the hotkey account to stake to.
- amount (bittensor.utils.balance.Balance) - The amount of TAO to stake.
- safe\_staking (bool) - If True, enables price safety checks to protect against fluctuating prices. The stake will only execute if the price change doesn't exceed the rate tolerance.
- allow\_partial\_stake (bool) - If True and safe\_staking is enabled, allows partial staking when the full amount would exceed the price tolerance. If false, the entire stake fails if it would exceed the tolerance.
- rate\_tolerance (float) - The maximum allowed price change ratio when staking. For example, 0.005 = 0.5% maximum price increase. Only used when safe\_staking is True.
- mev\_protection (bool) - If True, encrypts and submits the staking transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Waits for the transaction to be included in a block.
- wait\_for\_finalization (bool) - Waits for the transaction to be finalized on the blockchain.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

## Notes 

<!-- image -->

When safe\_staking is enabled, it provides protection against price fluctuations during the time between when stake is submitted and when it is actually processed by the chain.

- &lt;https:/ /docs.learnbittensor.org/staking-and-delegation/staking&gt;
- Price Protection: &lt;https:/ /docs.learnbittensor.org/learn/priceprotection&gt;
- Rate Limits: &lt;https:/ /docs.learnbittensor.org/learn/chain-ratelimits#staking-operations-rate-limits&gt;

add\_stake\_multiple(wallet, netuids, hotkey\_ss 58 s, amounts, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

[source] Adds stakes to multiple neurons identified by their hotkey SS58 addresses. This bulk operation allows for efficient staking across different neurons from a single wallet.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet used for staking.
- netuids (bittensor.core.types.UIDs) - List of subnet UIDs.
- hotkey\_ss58s (list[str]) - List of SS58 addresses of hotkeys to stake to.
- amounts (list[bittensor.utils.balance.Balance]) - List of corresponding TAO amounts to bet for each netuid and hotkey.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Waits for the transaction to be included in a block.
- wait\_for\_finalization (bool) - Waits for the transaction to be finalized on the blockchain.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

<!-- image -->

## Notes

- Price Protection: &lt;https:/ /docs.learnbittensor.org/learn/priceprotection&gt;
- Rate Limits: &lt;https:/ /docs.learnbittensor.org/learn/chain-ratelimits#staking-operations-rate-limits&gt;

## all\_subnets(block=None)

## [source]

Queries the blockchain for comprehensive information about all subnets, including their dynamic parameters and operational status.

## Parameters:

block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

A list of DynamicInfo objects, each containing detailed information about a subnet, or None if the query fails.

## Return type:

Optional[list[DynamicInfo]]

announce\_proxy(wallet, real\_account\_ss 58 , call\_hash, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD,

## raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Announces a future call that will be executed through a proxy.

This method allows a proxy account to declare its intention to execute a specific call on behalf of a real account after a delay period. The real account can review and either approve (via proxy\_announced() ) or reject (via reject\_proxy\_announcement() ) the announcement.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor wallet object (should be the proxy account wallet).
- real\_account\_ss58 (str) - The SS58 address of the real account on whose behalf the call will be made.
- call\_hash (str) - The hash of the call that will be executed in the future.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the inclusion of the transaction.
- wait\_for\_finalization (bool) - Whether to wait for the finalization of the transaction.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

<!-- image -->

## Notes

- A deposit is required when making an announcement. The deposit is returned when the announcement is

executed, rejected, or removed. The announcement can be executed after the delay period has passed. - See:

&lt;https:/ /docs.learnbittensor.org/keys/proxies&gt;

## property block: int

Provides an asynchronous getter to retrieve the current block number.

## Returns:

The current blockchain block number.

## Return type:

int

## blocks\_since\_last\_step(netuid, block=None)

[source]

Queries the blockchain to determine how many blocks have passed since the last epoch step for a specific subnet.

## Parameters:

- netuid (int) - The unique identifier of the subnetwork.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

The number of blocks since the last step in the subnet, or None if the query fails.

## Return type:

Optional[int]

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/glossary#epoch&gt;

## blocks\_since\_last\_update(netuid, uid, block=None)

<!-- image -->

Returns the number of blocks since the last update, or None if the subnetwork or UID does not exist.

## Parameters:

- netuid (int) - The unique identifier of the subnetwork.
- uid (int) - The unique identifier of the neuron.
- block (Optional[int]) - The block number for this query. If None, queries the current chain head.

## Returns:

The number of blocks since the last update, or None if the subnetwork or UID does not exist.

## Return type:

Optional[int]

## blocks\_until\_next\_epoch(netuid, tempo=None, block=None)

Returns the number of blocks until the next epoch of subnet with provided netuid.

## Parameters:

- netuid (int) - The unique identifier of the subnetwork.
- tempo (Optional[int]) - The tempo of the subnet.
- block (Optional[int]) - the block number for this query.

## Returns:

The number of blocks until the next epoch of the subnet with provided netuid.

## Return type:

Optional[int]

## bonds(netuid, mechid=0, block=None)

[source]

Retrieves the bond distribution set by subnet validators within a specific subnet.

Bonds represent a validator's accumulated assessment of each miner's performance over time, which serves as the starting point of Yuma Consensus.

## Parameters:

- netuid (int) - Subnet identifier.
- mechid (int) - Subnet mechanism identifier (default 0 for primary mechanism).
- block (Optional[int]) - The block number for this query. If None, queries the current chain head.

## Returns:

- validator\_uid: The UID of the validator
- bonds: List of (miner\_uid, bond\_value) pairs

Bond values are u16-normalized (0-65535, where 65535 = 1.0 or 100%).

## Return type:

List of tuples, where each tuple contains

## Example:

```
# Get bonds for subnet 1 bonds = subtensor.bonds(netuid=1) print(bonds[0]) # example output: (5, [(0, 32767), (1, 16383), (3, 8191)]) # This means validator UID 5 has bonds: 50% to miner 0, 25% to miner 1,
```

<!-- image -->

## Notes 

- See: &lt;https:/ /docs.learnbittensor.org/glossary#validator-miner-bonds&gt;
- See: &lt;https:/ /docs.learnbittensor.org/glossary#yuma-consensus&gt;

## burned\_register(wallet, netuid, *,

```
mev_protection=DEFAULT_MEV_PROTECTION, period=DEFAULT_PERIOD, raise_error=False, wait_for_inclusion=True, wait_for_finalization=True, wait_for_revealed_execution=True)
```

[source] Registers a neuron on the Bittensor network by recycling TAO. This method of registration involves recycling TAO tokens, allowing them to be re-mined by performing work on the network.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet associated with the neuron to be registered.
- netuid (int) - The unique identifier of the subnet.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Waits for the transaction to be included in a block.
- wait\_for\_finalization (bool) - Waits for the transaction to be finalized on the blockchain.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

<!-- image -->

## Notes

- Rate Limits: &lt;https:/ /docs.learnbittensor.org/learn/chain-ratelimits#registration-rate-limits&gt;

## claim\_root(wallet, netuids, *,

mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Submit an extrinsic to manually claim accumulated root dividends from one or more subnets.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor Wallet instance.
- netuids (bittensor.core.types.UIDs) - Iterable of subnet IDs to claim from in this call (the chain enforces a maximum number per transaction).
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - Number of blocks during which the transaction remains valid after submission. If the extrinsic is not included in a block within this window, it will expire and be rejected.
- raise\_error (bool) - Whether to raise a Python exception instead of returning a failed ExtrinsicResponse.
- wait\_for\_inclusion (bool) - Whether to wait until the extrinsic is included in a block before returning.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic in a block before returning.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

ExtrinsicResponse describing the result of the extrinsic execution.

<!-- image -->

## Notes

- Only Alpha dividends are claimed; the underlying TAO stake on the Root Subnet remains unchanged.
- The current root claim type (Swap or Keep) determines whether claimed Alpha is converted to TAO and restaked on root or left as Alpha on the originating subnets.
- See: &lt;https:/ /docs.learnbittensor.org/staking-and-delegation/rootclaims&gt;
- See also: &lt;https:/ /docs.learnbittensor.org/staking-and-delegation/rootclaims/managing-root-claims&gt;
- Transaction fees: &lt;https:/ /docs.learnbittensor.org/learn/fees&gt;

## [source]

## close()

Closes the connection to the blockchain.

Use this to explicitly clean up resources and close the network connection instead of waiting for garbage collection.

## Returns:

None

## Example:

```
sub = bt.Subtensor(network="finney") # calls to subtensor sub.close()
```

## commit\_reveal\_enabled(netuid, block=None)

[source]

Check if commit-reveal mechanism is enabled for a given subnet at a specific block.

## Parameters:

- netuid (int) - The unique identifier of the subnet for which to check the commit-reveal mechanism.

- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

True if commit-reveal mechanism is enabled, False otherwise.

## Return type:

bool

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/glossary#commit-reveal&gt;
- &lt;https:/ /docs.learnbittensor.org/subnets/subnet-hyperparameters&gt;

commit\_weights(wallet, netuid, salt, uids, weights, mechid=0, version\_key=version\_as\_int, max\_attempts=5, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=16, raise\_error=True, wait\_for\_inclusion=False, wait\_for\_finalization=False, wait\_for\_revealed\_execution=True)

[source]

Commits a hash of the neuron's weights to the Bittensor blockchain using the provided wallet. This action serves as a commitment or snapshot of the neuron's current weight distribution.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet associated with the neuron committing the weights.
- netuid (int) - The unique identifier of the subnet.
- salt (bittensor.core.types.Salt) - list of randomly generated integers as salt to generated weighted hash.
- uids (bittensor.core.types.UIDs) - NumPy array of neuron UIDs for which weights are being committed.
- weights (bittensor.core.types.Weights) - NumPy array of weight values corresponding to each UID.
- mechid (int) - Subnet mechanism unique identifier.
- version\_key (int) - Version key for compatibility with the network.
- max\_attempts (int) - The number of maximum attempts to commit weights.

- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the extrinsic to be included in a block.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

## ExtrinsicResponse

This function allows neurons to create a tamper-proof record of their weight distribution at a specific point in time, enhancing transparency and accountability within the Bittensor network.

<!-- image -->

## Notes

- Rate Limits: &lt;https:/ /docs.learnbittensor.org/learn/chain-ratelimits#weights-setting-rate-limit&gt;

## compose\_call(call\_module, call\_function, call\_params, block=None)

Dynamically compose a GenericCall using on-chain Substrate metadata after validating the provided parameters.

## Parameters:

- call\_module (str) - Pallet name (e.g. 'SubtensorModule', 'AdminUtils').

- call\_function (str) - Function name (e.g. 'set\_weights', 'sudo\_set\_tempo').
- call\_params (dict[str, Any]) - Dictionary of parameters for the call.
- block (Optional[int]) - Block number for querying metadata.

## Returns:

Composed call object ready for extrinsic submission.

## Return type:

GenericCall

<!-- image -->

## Notes

For detailed documentation and examples of composing calls, including the CallBuilder utility, see: &lt;https:/ /docs.learnbittensor.org/sdk/call&gt;

## contribute\_crowdloan(wallet, crowdloan\_id, amount, *,

mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True,

wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Contributes TAO to an active crowdloan campaign.

Contributions must occur before the crowdloan's end block and are subject to minimum contribution requirements. If a contribution would push the total raised above the cap, it is automatically clipped to fit the remaining amount. Once the cap is reached, further contributions are rejected.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor wallet instance used to sign the transaction (coldkey pays, coldkey receives emissions).
- crowdloan\_id (int) - The unique identifier of the crowdloan to contribute to.
- amount (bittensor.utils.balance.Balance) - Amount to contribute (TAO). Must meet or exceed the campaign's min\_contribution.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted.
- raise\_error (bool) - If True, raises an exception rather than returning failure in the response.
- wait\_for\_inclusion (bool) - Whether to wait for the extrinsic to be included in a block.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

ExtrinsicResponse indicating success or failure, with error details if applicable.

## Return type:

bittensor.core.types.ExtrinsicResponse

<!-- image -->

## Notes

- Contributions can be withdrawn before finalization via withdraw\_crowdloan.
- If the campaign does not reach its cap by the end block, contributors can be refunded via refund\_crowdloan.
- Contributions are counted toward MaxContributors limit per crowdloan.
- Crowdloans Overview: &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans&gt;
- Crowdloan Tutorial: &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans/crowdloanstutorial#step-4-contribute-to-the-crowdloan&gt;

create\_crowdloan(wallet, deposit, min\_contribution, cap, end, call=None, target\_address=None, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True,

wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Creates a new crowdloan campaign on-chain.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor Wallet instance used to sign the transaction.
- deposit (bittensor.utils.balance.Balance) - Initial deposit in RAO from the creator.
- min\_contribution (bittensor.utils.balance.Balance) - Minimum contribution amount.
- cap (bittensor.utils.balance.Balance) - Maximum cap to be raised.
- end (int) - Block number when the campaign ends.
- call (Optional[scalecodec.types.GenericCall]) - Runtime call data (e.g., subtensor::register\_leased\_network).
- target\_address (Optional[str]) - SS58 address to transfer funds to on success.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the extrinsic to be included in a block.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

ExtrinsicResponse indicating success or failure. On success, the crowdloan ID can be extracted from the Crowdloan.Created event in the response.

## Return type:

bittensor.core.types.ExtrinsicResponse

<!-- image -->

## Notes

- Creator cannot update call or target\_address after creation.
- Creator can update cap, end, and min\_contribution before finalization via update\_* methods.
- Use get\_crowdloan\_next\_id to determine the ID that will be assigned to the new crowdloan.
- Crowdloans Overview: &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans&gt;
- Crowdloan Tutorial:
- &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans/crowdloanstutorial#step-3-create-a-crowdloan&gt;
- Leasing:
- &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans#crowdloanlifecycle&gt;

create\_pure\_proxy(wallet, proxy\_type, delay, index, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Creates a pure proxy account.

A pure proxy is a keyless account that can only be controlled through proxy relationships. Unlike regular proxies, pure proxies do not have their own private keys, making them more secure for certain use cases. The pure proxy address is deterministically generated based on the spawner account, proxy type, delay, and index.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor wallet object.
- proxy\_type (Union[str, bittensor.core.chain\_data.ProxyType]) - The type of proxy permissions for the pure proxy. Can be a string or ProxyType enum value. For available proxy types and their permissions, see the documentation link in the Notes section below.
- delay (int) - Optionally, include a delay in blocks. The number of blocks that must elapse between announcing and executing a proxied transaction. A delay

- of 0 means the pure proxy can be used immediately without any announcement period. A non-zero delay creates a time-lock, requiring announcements before execution to give the spawner time to review/reject.
- index (int) - A salt value (u16, range 0-65535) used to generate unique pure proxy addresses. This should generally be left as 0 unless you are creating batches of proxies. When creating multiple pure proxies with identical parameters (same proxy\_type and delay), different index values will produce different SS58 addresses. This is not a sequential counter-you can use any unique values (e.g., 0, 100, 7, 42) in any order. The index must be preserved as it's required for kill\_pure\_proxy() . If creating multiple pure proxies in a single batch transaction, each must have a unique index value.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the inclusion of the transaction.
- wait\_for\_finalization (bool) - Whether to wait for the finalization of the transaction.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

<!-- image -->

## Notes

- The pure proxy account address can be extracted from the 'PureCreated' event in the response. Store the spawner address, proxy\_type, index, height, and ext\_index as they are required to kill the pure proxy later via kill\_pure\_proxy() .
- Bittensor proxies: &lt;https:/ /docs.learnbittensor.org/keys/proxies/pureproxies&gt;
- Polkadot proxy documentation: &lt;https:/ /wiki.polkadot.network/docs/learn-proxies&gt;

## determine\_block\_hash(block)

[source]

Determine the block hash for the block specified with the provided parameters.

Ensures that only one of the block specification parameters is used and returns the appropriate block hash for blockchain queries.

## Parameters:

block (Optional[int]) - The block number to get the hash for. If None, returns None.

## Returns:

The block hash (hex string with 0x prefix) if one can be determined, None otherwise.

## Return type:

Optional[str]

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/glossary#block&gt;

## difficulty(netuid, block=None)

[source]

Retrieves the 'Difficulty' hyperparameter for a specified subnet in the Bittensor network.

## This parameter determines the computational challenge required for neurons to participate in consensus and

validation processes, using proof of work (POW) registration.

## Parameters:

- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

The value of the 'Difficulty' hyperparameter if the subnet exists, None otherwise.

## Return type:

Optional[int]

<!-- image -->

## Notes

Burn registration is much more common on Bittensor subnets currently, compared to POW registration.

- &lt;https:/ /docs.learnbittensor.org/subnets/subnet-hyperparameters&gt;
- &lt;https:/ /docs.learnbittensor.org/validators#validator-registration&gt;
- &lt;https:/ /docs.learnbittensor.org/miners#miner-registration&gt;

## dissolve\_crowdloan(wallet, crowdloan\_id, *,

mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Dissolves a failed or refunded crowdloan, cleaning up storage and returning the creator's deposit.

This permanently removes the crowdloan from on-chain storage and returns the creator's deposit. Can only be called by the creator after all non-creator contributors have been refunded via refund\_crowdloan. This is the final step in the lifecycle of a failed crowdloan (one that did not reach its cap by the end block).

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor wallet instance used to sign the transaction (must be the creator's coldkey).
- crowdloan\_id (int) - The unique identifier of the crowdloan to dissolve.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after submission.
- raise\_error (bool) - If True, raises an exception rather than returning failure in the response.
- wait\_for\_inclusion (bool) - Whether to wait for the extrinsic to be included in a block.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

ExtrinsicResponse indicating success or failure, with error details if applicable.

## Return type:

bittensor.core.types.ExtrinsicResponse

<!-- image -->

## Notes

- Only the creator can dissolve their own crowdloan.
- All non-creator contributors must be refunded first via refund\_crowdloan.
- The creator's deposit (and any remaining contribution above deposit) is returned.
- After dissolution, the crowdloan is permanently removed from chain storage.
- &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans&gt;

does\_hotkey\_exist(hotkey\_ss 58 , block=None)

[source]

Returns true if the hotkey has been associated with a coldkey through account creation.

This method queries the Subtensor's Owner storage map to check if the hotkey has been paired with a coldkey, as it must be before it (the hotkey) can be used for neuron registration.

The Owner storage map defaults to the zero address

(5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM) for unused hotkeys. This method returns True if the Owner value is anything other than this default.

## Parameters:

- hotkey\_ss58 (str) - The SS58 address of the hotkey.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

True if the hotkey has been associated with a coldkey, False otherwise.

## Return type:

bool

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/glossary#hotkey&gt;

## filter\_netuids\_by\_registered\_hotkeys(all\_netuids,

filter\_for\_netuids, all\_hotkeys, block)

[source]

Filters netuids by combining netuids from all\_netuids and netuids with registered hotkeys.

## If filter\_for\_netuids is empty/None:

Returns all netuids where hotkeys from all\_hotkeys are registered.

## If filter\_for\_netuids is provided:

Returns the union of: - Netuids from all\_netuids that are in filter\_for\_netuids, AND Netuids with registered hotkeys that are in filter\_for\_netuids

This allows you to get netuids that are either in your specified list (all\_netuids) or have registered hotkeys, as long as they match filter\_for\_netuids.

## Parameters:

- all\_netuids (Iterable[int]) - A list of netuids to consider for filtering.
- filter\_for\_netuids (Iterable[int]) - A subset of netuids to restrict the result to. If None/empty, returns all netuids with registered hotkeys.
- all\_hotkeys (Iterable[Wallet]) - Hotkeys to check for registration.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

The filtered list of netuids (union of filtered all\_netuids and registered hotkeys).

## Return type:

list[int]

## finalize\_crowdloan(wallet, crowdloan\_id, *,

mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Finalizes a successful crowdloan after the cap is fully raised and the end block has passed.

Finalization executes the stored call (e.g., register\_leased\_network) or transfers raised funds to the target address. For subnet lease crowdloans, this registers the subnet, creates a SubnetLeaseBeneficiary proxy for the creator, and records contributor shares for pro-rata emissions distribution. Leftover funds (after registration and proxy costs) are refunded to contributors.

Only the creator can finalize, and finalization can only occur after both the end block is reached and the total raised equals the cap.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor wallet instance used to sign the transaction (must be the creator's coldkey).
- crowdloan\_id (int) - The unique identifier of the crowdloan to finalize.

- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after submission.
- raise\_error (bool) - If True, raises an exception rather than returning failure in the response.
- wait\_for\_inclusion (bool) - Whether to wait for the extrinsic to be included in a block.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

ExtrinsicResponse indicating success or failure. On success, a subnet lease is created (if applicable) and contributor shares are recorded for emissions.

## Return type:

bittensor.core.types.ExtrinsicResponse

<!-- image -->

## Notes

- Only the creator can finalize.
- Finalization requires raised == cap and current\_block &gt;= end.
- For subnet leases, emissions are swapped to TAO and distributed to contributors' coldkeys during the lease.
- Leftover cap (after subnet lock + proxy deposit) is refunded to contributors pro-rata.
- Crowdloans Overview: &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans&gt;
- Crowdloan Tutorial: &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans/crowdloanstutorial#step-5-finalize-the-crowdloan&gt;
- Emissions Distribution:
- &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans#emissionsdistribution-during-a-lease&gt;

## get\_admin\_freeze\_window(block=None)

Returns the duration, in blocks, of the administrative freeze window at the end of each epoch.

The admin freeze window is a period at the end of each epoch during which subnet owner operations are prohibited. This prevents subnet owners from modifying hyperparameters or performing certain administrative actions right before validators submit weights at the epoch boundary.

## Parameters:

block (Optional[int]) - The block number to query.

## Returns:

10 blocks, ~2 minutes).

## Return type:

The number of blocks in the administrative freeze window (default

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/learn/chain-rate-limits#administrativefreeze-window&gt;

## get\_all\_commitments(netuid, block=None)

Retrieves raw commitment metadata from a given subnet.

This method retrieves all commitment data for all neurons in a specific subnet. This is useful for analyzing the commit-reveal patterns across an entire subnet.

## Parameters:

- netuid (int) - The unique identifier of the subnetwork.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

commitment with the commitment as a string.

## Return type:

A mapping of the ss58

[source]

## Example:

## get\_all\_ema\_tao\_inflow(block=None)

Retrieves the EMA (exponential moving average) of net TAO flows for all subnets.

The EMA tracks net TAO flows (staking minus unstaking) with a 30-day half-life (~86.8 day window), smoothing out short-term fluctuations while capturing sustained staking trends. This metric determines the subnet's share of TAO emissions under the current, flow-based model. Positive values indicate net inflow (more staking than unstaking), negative values indicate net outflow. Subnets with negative EMA flows receive zero emissions.

## Parameters:

block (Optional[int]) - The block number to retrieve the commitment from.

## Returns:

Dict mapping netuid to (last\_updated\_block, ema\_flow). The Balance represents the EMA of net TAO flow in TAO units. Positive values indicate sustained net inflow, negative values indicate sustained net outflow.

## Return type:

dict[int, tuple[int, bittensor.utils.balance.Balance]]

The EMA uses a smoothing factor α ≈ 0.000003209, creating a 30-day half-life and ~86.8 day window. Only direct stake/unstake operations count toward flows; neuron registrations and root claims are excluded. Subnet 0 (root network) does not have an EMA TAO flow value.

<!-- image -->

## Notes

- Flow-based emissions:

&lt;https:/ /docs.learnbittensor.org/learn/emissions#tao-reserve-injection&gt;

- EMA smoothing: &lt;https:/ /docs.learnbittensor.org/learn/ema&gt;

[source] get\_all\_metagraphs\_info(all\_mechanisms=False, block=None) Retrieves a list of MetagraphInfo objects for all subnets

## Parameters:

- all\_mechanisms (bool) - If True then returns all mechanisms, otherwise only those with index 0 for all subnets.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

List of MetagraphInfo objects for all existing subnets.

## Return type:

Optional[list[bittensor.core.chain\_data.MetagraphInfo]]

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/glossary#metagraph&gt;

## [source] get\_all\_neuron\_certificates(netuid, block=None)

Retrieves the TLS certificates for neurons within a specified subnet (netuid) of the Bittensor network.

## Parameters:

- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

Dictionary mapping neuron hotkey SS58 addresses to their Certificate objects.

Only includes neurons that have registered certificates.

## Return type:

dict[str, bittensor.utils.Certificate]

<!-- image -->

## Notes

This method is used for certificate discovery to establish mutual TLS communication between neurons.

- &lt;https:/ /docs.learnbittensor.org/subnets/neuron-tls-certificates&gt;

get\_all\_revealed\_commitments(netuid, block=None)

<!-- image -->

Retrieves all revealed commitments for a given subnet.

## Parameters:

- netuid (int) - The unique identifier of the subnetwork.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

A dictionary mapping hotkey addresses to tuples of (reveal\_block, commitment\_message) pairs. Each validator can have multiple revealed commitments (up to 10 most recent).

## Return type:

dict[str, tuple[tuple[int, str], Ellipsis]]

## Example:

```
# sample return value { "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY": ( (12, "Alice me "5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty": ( (12, "Bob mess }
```

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/glossary#commit-reveal&gt;

## get\_all\_subnets\_info(block=None)

## [source]

Retrieves detailed information about all subnets within the Bittensor network.

## Parameters:

block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

A list of SubnetInfo objects, each containing detailed information about a subnet.

## Return type:

list[bittensor.core.chain\_data.SubnetInfo]

## get\_all\_subnets\_netuid(block=None)

Retrieves the list of all subnet unique identifiers (netuids) currently present in the Bittensor network.

## Parameters:

block (Optional[int]) - The blockchain block number for the query.

## Returns:

A list of subnet netuids.

## Return type:

bittensor.core.types.UIDs

This function provides a comprehensive view of the subnets within the Bittensor network, offering insights into its diversity and scale.

## get\_auto\_stakes(coldkey\_ss 58 , block=None)

Fetches auto stake destinations for a given wallet across all subnets.

## Parameters:

- coldkey\_ss58 (str) - Coldkey ss58 address.
- block (Optional[int]) - The block number for the query. If None, queries the current chain head.

## Returns:

- netuid: The unique identifier of the subnet.
- hotkey: The hotkey of the wallet.

## Return type:

Dictionary mapping netuid to hotkey, where

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/miners/autostaking&gt;

## get\_balance(address, block=None)

Retrieves the balance for given coldkey.

This method queries the System module's Account storage to get the current balance of a coldkey address. The balance represents the amount of TAO tokens held by the specified address.

## Parameters:

- address (str) - The coldkey address in SS58 format.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

The balance object containing the account's TAO balance.

## Return type:

Balance

## get\_balances(*addresses, block=None)

Retrieves the balance for given coldkey(s).

This method efficiently queries multiple coldkey addresses in a single batch operation, returning a dictionary mapping each address to its corresponding balance. This is more efficient than calling get\_balance multiple times.

## Parameters:

- *addresses (str) - Variable number of coldkey addresses in SS58 format.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

A dictionary mapping each address to its Balance object.

## Return type:

dict[str, bittensor.utils.balance.Balance]

## get\_block\_hash(block=None)

Retrieves the hash of a specific block on the Bittensor blockchain.

[source]

[source]

[source]

The block hash is a unique identifier representing the cryptographic hash of the block's content, ensuring its integrity and immutability. It is a fundamental aspect of blockchain technology, providing a secure reference to each block's data. It is crucial for verifying transactions, ensuring data consistency, and maintaining the trustworthiness of the blockchain.

## Parameters:

block (Optional[int]) - The block number for which the hash is to be retrieved. If None, returns the latest block hash.

## Returns:

The cryptographic hash of the specified block.

## Return type:

str

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/glossary#block&gt;

## get\_block\_info(block=None, block\_hash=None)

Retrieve complete information about a specific block from the Subtensor chain.

This method aggregates multiple low-level RPC calls into a single structured response, returning both the raw on-chain data and high-level decoded metadata for the given block.

## Parameters:

- block (Optional[int]) - The block number for which the hash is to be retrieved.
- block\_hash (Optional[str]) - The hash of the block to retrieve the block from.

## Returns:

A dataclass containing all available information about the specified block, including:

- number: The block number.
- hash: The corresponding block hash.
- timestamp: The timestamp of the block (based on the Timestamp.Now extrinsic).

- header: The raw block header returned by the node RPC.
- extrinsics: The list of decoded extrinsics included in the block.
- explorer: The link to block explorer service. Always related with finney block data.

## Return type:

BlockInfo instance

## get\_children(hotkey\_ss 58 , netuid, block=None)

Retrieves the children of a given hotkey and netuid.

This method queries the SubtensorModule's ChildKeys storage function to get the children and formats them before returning as a tuple. It provides information about the child neurons that a validator has set for weight distribution.

## Parameters:

- hotkey\_ss58 (str) - The hotkey value.
- netuid (int) - The netuid value.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

A tuple containing a boolean indicating success or failure, a list of formatted children with their proportions, and an error message (if applicable).

## Return type:

tuple[bool, list[tuple[float, str]], str]

## Example:

[source]

```
# Get children for a hotkey in subnet 1 success, children, error = subtensor.get_children(hotkey="5F…", netuid=1 if success: for proportion, child_hotkey in children: print(f"Child {child_hotkey}: {proportion}")
```

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/validators/child-hotkeys&gt;

## [source] get\_children\_pending(hotkey\_ss 58 , netuid, block=None)

Retrieves the pending children of a given hotkey and netuid.

This method queries the SubtensorModule's PendingChildKeys storage function to get children that are pending approval or in a cooldown period. These are children that have been proposed but not yet finalized.

## Parameters:

- hotkey\_ss58 (str) - The hotkey value.
- netuid (int) - The netuid value.
- block (Optional[int]) - The block number for which the children are to be retrieved. If None, queries the current chain head.

## Returns:

## A tuple containing:

- list[tuple[float, str]]: A list of children with their proportions.
- int: The cool-down block number.

## Return type:

tuple

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/validators/child-hotkeys&gt;

## get\_commitment(netuid, uid, block=None)

[source]

Retrieves the on-chain commitment for a specific neuron in the Bittensor network.

This method retrieves the commitment data that a neuron has published to the blockchain. Commitments are used in the commit-reveal mechanism for secure weight setting and other network operations.

## Parameters:

- netuid (int) - The unique identifier of the subnetwork.
- uid (int) - The unique identifier of the neuron.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

The commitment data as a string.

## Return type:

str

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/glossary#commit-reveal&gt;

## get\_commitment\_metadata(netuid, hotkey\_ss 58 , block=None)

Fetches raw commitment metadata from specific subnet for given hotkey.

## Parameters:

- netuid (int) - The unique subnet identifier.
- hotkey\_ss58 (str) - The hotkey ss58 address.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

The raw commitment metadata. Returns a dict when commitment data exists, or an empty string when no commitment is found for the given hotkey on the subnet.

## Return type:

Union[str, dict]

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/glossary#commit-reveal&gt;

## get\_crowdloan\_by\_id(crowdloan\_id, block=None)

Retrieves detailed information about a specific crowdloan campaign.

## Parameters:

- crowdloan\_id (int) - Unique identifier of the crowdloan (auto-incremented starting from 0).
- block (Optional[int]) - The blockchain block number for the query. If None, queries the current chain head.

## Returns:

campaign ID, creator address, creator's deposit, minimum contribution amount, end block, funding cap, funds account address, amount raised, optional target address, optional embedded call, finalization status, and contributor count. Returns None if the crowdloan does not exist.

## Return type:

CrowdloanInfo object containing

<!-- image -->

## Notes

- Crowdloans Overview: &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans&gt;

## get\_crowdloan\_constants(constants=None, block=None)

Retrieves runtime configuration constants governing crowdloan behavior and limits on the Bittensor blockchain.

If a list of constant names is provided, only those constants will be queried. Otherwise, all known constants defined in CrowdloanConstants.field\_names() are fetched.

These constants define requirements and operational limits for crowdloan campaigns:

- AbsoluteMinimumContribution: Minimum amount per contribution (TAO).
- MaxContributors: Maximum number of unique contributors per crowdloan.
- MaximumBlockDuration: Maximum duration (in blocks) for a crowdloan campaign (60 days = 432,000 blocks on production).
- MinimumDeposit: Minimum deposit required from the creator (TAO).
- MinimumBlockDuration: Minimum duration (in blocks) for a crowdloan campaign (7 days = 50,400 blocks on production).
- RefundContributorsLimit: Maximum number of contributors refunded per refund\_crowdloan call (typically 50).

## Parameters:

- constants (Optional[list[str]]) - Specific constant names to query. If None, retrieves all constants from CrowdloanConstants.
- block (Optional[int]) - The blockchain block number for the query. If None, queries the current chain head.

## Returns:

A CrowdloanConstants data object containing the queried constants. Missing constants return None.

## Return type:

bittensor.core.chain\_data.CrowdloanConstants

<!-- image -->

## Notes 

These constants enforce contribution floors, duration bounds, and refund batching limits.

- Crowdloans Overview: &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans&gt;

## get\_crowdloan\_contributions(crowdloan\_id, block=None)

Retrieves all contributions made to a specific crowdloan campaign.

Returns a mapping of contributor coldkey addresses to their contribution amounts in Rao.

## Parameters:

- crowdloan\_id (int) - The unique identifier of the crowdloan.
- block (Optional[int]) - The blockchain block number for the query. If None, queries the current chain head.

## Returns:

Dictionary mapping contributor SS58 addresses to their Balance contribution amounts (in Rao). Returns empty dictionary if the crowdloan has no contributions or does not exist.

## Return type:

dict[str, bittensor.utils.balance.Balance]

<!-- image -->

## Notes

Contributions are clipped to the remaining cap. Once the cap is reached, no further contributions are accepted.

- Crowdloans Overview: &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans&gt;
- Crowdloan Tutorial: &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans/crowdloanstutorial#step-4-contribute-to-the-crowdloan&gt;

## get\_crowdloan\_next\_id(block=None)

Retrieves the next available crowdloan identifier.

Crowdloan IDs are allocated sequentially starting from 0. This method returns the ID that will be assigned to the next crowdloan created via create\_crowdloan() .

## Parameters:

block (Optional[int]) - The blockchain block number for the query. If None, queries the current chain head.

## Returns:

The next crowdloan ID (integer) to be assigned.

## Return type:

int

<!-- image -->

## Notes

- Crowdloans Overview: &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans&gt;
- Crowdloan Tutorial: &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans/crowdloanstutorial#get-the-crowdloan-id&gt;

## get\_crowdloans(block=None)

Retrieves all existing crowdloan campaigns with their metadata.

Returns comprehensive information for all crowdloans registered on the blockchain, including both active and finalized campaigns.

## Parameters:

block (Optional[int]) - The blockchain block number for the query. If None, queries the current chain head.

## Returns:

campaign ID, creator address, creator's deposit, minimum contribution amount, end block, funding cap, funds account address, amount raised, optional target address, optional embedded call, finalization status, and contributor count. Returns empty list if no crowdloans exist.

## Return type:

List of CrowdloanInfo objects, each containing

<!-- image -->

## Notes

- Crowdloans Overview: &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans&gt;
- Crowdloan Lifecycle: &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans#crowdloanlifecycle&gt;

## get\_current\_block()

Returns the current block number on the Bittensor blockchain.

This function provides the latest block number, indicating the most recent state of the blockchain.

## Returns:

The current chain block number.

## Return type:

int

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/glossary#block&gt;

## [source] get\_delegate\_by\_hotkey(hotkey\_ss 58 , block=None)

Retrieves detailed information about a delegate neuron (validator) based on its hotkey. This function provides a comprehensive view of the delegate's status, including its stakes, nominators, and reward distribution.

## Parameters:

- hotkey\_ss58 (str) - The SS58 address of the delegate's hotkey.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

Detailed information about the delegate neuron, None if not found.

## Return type:

Optional[bittensor.core.chain\_data.DelegateInfo]

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/glossary#delegate&gt;
- &lt;https:/ /docs.learnbittensor.org/glossary#nominator&gt;

## [source]

## get\_delegate\_identities(block=None)

Fetches delegate identities.

Delegates are validators that accept stake from other TAO holders

(nominators/delegators). This method retrieves the on-chain identity information for all delegates, including display name, legal name, web URLs, and other metadata they have set.

## Parameters:

block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

Dictionary mapping delegate SS58 addresses to their ChainIdentity objects.

## Return type:

dict[str, bittensor.core.chain\_data.chain\_identity.ChainIdentity]

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/staking-and-delegation/delegation&gt;

## get\_delegate\_take(hotkey\_ss 58 , block=None)

[source]

Retrieves the delegate 'take' percentage for a neuron identified by its hotkey. The 'take' represents the percentage of rewards that the delegate claims from its nominators' stakes.

## Parameters:

- hotkey\_ss58 (str) - The SS58 address of the neuron's hotkey.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

The delegate take percentage.

## Return type:

float

## [source]

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/staking-and-delegation/delegation&gt;

## get\_delegated(coldkey\_ss 58 , block=None)

[source]

Retrieves delegates and their associated stakes for a given nominator coldkey.

This method identifies all delegates (validators) that a specific coldkey has staked tokens to, along with stake amounts and other delegation information. This is useful for account holders to understand their stake allocations and involvement in the network's delegation and consensus mechanisms.

## Parameters:

- coldkey\_ss58 (str) - The SS58 address of the account's coldkey.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

List of DelegatedInfo objects containing stake amounts and delegate information. Returns empty list if no delegations exist for the coldkey.

## Return type:

list[bittensor.core.chain\_data.DelegatedInfo]

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/staking-and-delegation/delegation&gt;

## get\_delegates(block=None)

Fetches all delegates registered on the chain.

Delegates are validators that accept stake from other TAO holders (nominators/delegators). This method retrieves comprehensive information about all delegates including their hotkeys, total stake, nominator count, take percentage, and other metadata.

## Parameters:

[source]

block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

List of DelegateInfo objects containing comprehensive delegate information. Returns empty list if no delegates are registered.

## Return type:

list[bittensor.core.chain\_data.DelegateInfo]

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/staking-and-delegation/delegation&gt;

## get\_ema\_tao\_inflow(netuid, block=None)

Retrieves the EMA (exponential moving average) of net TAO flow for a specific subnet.

The EMA tracks net TAO flows (staking minus unstaking) with a 30-day half-life (~86.8 day window), smoothing out short-term fluctuations while capturing sustained staking trends. This metric determines the subnet's share of TAO emissions under the current, flow-based model. Positive values indicate net inflow (more staking than unstaking), negative values indicate net outflow. Subnets with negative EMA flows receive zero emissions.

## Parameters:

- netuid (int) - The unique identifier of the subnet to query.
- block (Optional[int]) - The block number to query. If None, uses latest finalized block.

## Returns:

Tuple of (last\_updated\_block, ema\_flow) where ema\_flow is the EMA of net TAO flow in TAO units. Returns None if the subnet does not exist or if querying subnet 0 (root network).

## Return type:

Optional[tuple[int, bittensor.utils.balance.Balance]]

The EMA uses a smoothing factor α ≈ 0.000003209, creating a 30-day half-life and ~86.8 day window. Only direct stake/unstake operations count toward flows; neuron

registrations and root claims are excluded. Subnet 0 (root network) does not have an EMA TAO flow value and will return None.

<!-- image -->

## Notes

- Flow-based emissions:

&lt;https:/ /docs.learnbittensor.org/learn/emissions#tao-reserve-injection&gt;

- EMA smoothing: &lt;https:/ /docs.learnbittensor.org/learn/ema&gt;

## get\_existential\_deposit(block=None)

## [source]

Retrieves the existential deposit amount for the Bittensor blockchain.

The existential deposit is the minimum amount of TAO required for an account to exist on the blockchain. Accounts with balances below this threshold can be reaped (removed) to conserve network resources and prevent blockchain bloat from dust accounts.

## Parameters:

block (Optional[int]) - The blockchain block number for the query.

## Returns:

The existential deposit amount in RAO.

## Return type:

Optional[bittensor.utils.balance.Balance]

<!-- image -->

## Notes 

- &lt;https:/ /docs.learnbittensor.org/glossary#existential-deposit&gt;

## get\_extrinsic\_fee(call, keypair)

Gets the extrinsic fee for a given extrinsic call and keypair.

This method estimates the transaction fee that will be charged for submitting the extrinsic to the blockchain. The fee is returned in Rao (the smallest unit of TAO, where 1 TAO = 1e9 Rao).

## Parameters:

- call (scalecodec.types.GenericCall) - The extrinsic GenericCall object representing the transaction to estimate.
- keypair (bittensor\_wallet.Keypair) - The keypair associated with the extrinsic (used to determine the account paying the fee).

## Returns:

Balance object representing the extrinsic fee in Rao.

## Return type:

bittensor.utils.balance.Balance

## Example:

```
# Estimate fee before sending a transfer call = subtensor.compose_call( call_module="Balances", call_function="transfer", call_params={"dest": destination_ss58, "value": amount.rao} ) fee = subtensor.get_extrinsic_fee(call=call, keypair=wallet.coldkey) print(f"Estimated fee: {fee.tao} TAO")
```

<!-- image -->

## Notes

To create the GenericCall object, use the compose\_call method with proper parameters. - &lt;https:/ /docs.learnbittensor.org/learn/fees&gt;

## get\_hotkey\_owner(hotkey\_ss 58 , block=None)

## [source]

Retrieves the owner of the given hotkey at a specific block hash. This function queries the blockchain for the owner of the provided hotkey. If the hotkey does not exist at the specified block hash, it returns None.

## Parameters:

- hotkey\_ss58 (str) - The SS58 address of the hotkey.

- block (Optional[int]) - The blockchain block number for the query. If None, queries the current chain head.

## Returns:

The SS58 address of the owner if the hotkey exists, or None if it doesn't.

## Return type:

Optional[str]

## get\_hotkey\_stake

## [source] get\_hyperparameter(param\_name, netuid, block=None)

Retrieves a specified hyperparameter for a specific subnet.

This method queries the blockchain for subnet-specific hyperparameters such as difficulty, tempo, immunity period, and other network configuration values. Return types and units vary by parameter.

## Parameters:

- param\_name (str) - The name of the hyperparameter storage function to retrieve.
- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

The value of the specified hyperparameter if the subnet exists, None otherwise. Return type varies by parameter (int, float, bool, or Balance).

## Return type:

Optional[Any]

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/subnets/subnet-hyperparameters&gt;

get\_last\_bonds\_reset(netuid, hotkey\_ss 58 , block=None)

Retrieves the block number when bonds were last reset for a specific hotkey on a subnet.

## Parameters:

- netuid (int) - The network uid to fetch from.
- hotkey\_ss58 (str) - The hotkey of the neuron for which to fetch the last bonds reset.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

The block number when bonds were last reset, or None if no bonds reset has occurred.

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/resources/glossary#validator-minerbonds&gt;
- &lt;https:/ /docs.learnbittensor.org/resources/glossary#commit-reveal&gt;

## get\_last\_commitment\_bonds\_reset\_block(netuid, uid, block=None)

[source] Retrieves the last block number when the bonds reset were triggered by publish\_metadata for a specific neuron.

## Parameters:

- netuid (int) - The unique identifier of the subnetwork.
- uid (int) - The unique identifier of the neuron.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

The block number when the bonds were last reset, or None if not found.

## Return type:

Optional[int]

get\_liquidity\_list(wallet, netuid, block=None)

[source]

Retrieves all liquidity positions for the given wallet on a specified subnet (netuid). Calculates associated fee rewards based on current global and tick-level fee data.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Wallet instance to fetch positions for.
- netuid (int) - Subnet unique id.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

List of liquidity positions, or None if subnet does not exist.

## Return type:

Optional[list[bittensor.utils.liquidity.LiquidityPosition]]

## get\_mechanism\_count(netuid, block=None)

Retrieves the number of mechanisms for the given subnet.

## Parameters:

- netuid (int) - Subnet identifier.
- block (Optional[int]) - The blockchain block number for the query. If None, queries the current chain head.

## Returns:

The number of mechanisms for the given subnet.

## Return type:

int

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/subnets/understanding-multiplemech-subnets&gt;

## get\_mechanism\_emission\_split(netuid, block=None)

Returns the emission percentages allocated to each subnet mechanism.

## Parameters:

- netuid (int) - The unique identifier of the subnet.

- block (Optional[int]) - The blockchain block number for the query.

## Returns:

A list of integers representing the percentage of emission allocated to each subnet mechanism (rounded to whole numbers). Returns None if emission is evenly split or if the data is unavailable.

## Return type:

Optional[list[int]]

get\_metagraph\_info(netuid, mechid=0, selected\_indices=None, block=None)

[source]

Retrieves full or partial metagraph information for the specified subnet (netuid).

A metagraph is a data structure that contains comprehensive information about the current state of a subnet, including detailed information on all the nodes (neurons) such as subnet validator stakes and subnet weights and bonds.

## Parameters:

- netuid (int) - Subnet unique identifier.
- mechid (int) - Subnet mechanism unique identifier.
- selected\_indices
- (Optional[Union[list[bittensor.core.chain\_data.SelectiveMetagraphIndex], list[int]]]) - Optional list of SelectiveMetagraphIndex or int values specifying which fields to retrieve. If not provided, all available fields will be returned.
- block (Optional[int]) - The block number at which to query the data. If None, queries the current chain head.

## Returns:

MetagraphInfo object with the requested subnet mechanism data, None if the subnet mechanism does not exist.

## Return type:

Optional[bittensor.core.chain\_data.MetagraphInfo]

## Example:

```
# Retrieve all fields from the metagraph from subnet 2 mechanism 0 meta_info = subtensor.get_metagraph_info(netuid=2) # Retrieve all fields from the metagraph from subnet 2 mechanism 1 meta_info = subtensor.get_metagraph_info(netuid=2, mechid=1) # Retrieve selective data from the metagraph from subnet 2 mechanism 0 partial_meta_info = subtensor.get_metagraph_info( netuid=2, selected_indices=[SelectiveMetagraphIndex.Name, SelectiveMetagraphIn ) # Retrieve selective data from the metagraph from subnet 2 mechanism 1 partial_meta_info = subtensor.get_metagraph_info( netuid=2, mechid=1, selected_indices=[SelectiveMetagraphIndex.Name, SelectiveMetagraphIn )
```

<!-- image -->

## Notes 

- &lt;https:/ /docs.learnbittensor.org/subnets/metagraph&gt;

## get\_mev\_shield\_current\_key(block=None)

Retrieves the CurrentKey from the MevShield pallet storage.

The CurrentKey contains the ML-KEM-768 public key that is currently being used for encryption in this block. This key is rotated from NextKey at the beginning of each block.

## Parameters:

block (Optional[int]) - The blockchain block number at which to perform the query. If None, uses the current block.

## Returns:

The ML-KEM-768 public key as bytes (1184 bytes for ML-KEM-768)

## Return type:

<!-- image -->

## Optional[bytes]

Note

If CurrentKey is not set (None in storage), this function returns None. This can happen if no validator has announced a key yet.

## get\_mev\_shield\_next\_key(block=None)

Retrieves the NextKey from the MevShield pallet storage.

The NextKey contains the ML-KEM-768 public key that will be used for encryption in the next block. This key is rotated from NextKey to CurrentKey at the beginning of each block.

## Parameters:

block (Optional[int]) - The blockchain block number at which to perform the query. If None, uses the current block.

## Returns:

The ML-KEM-768 public key as bytes (1184 bytes for ML-KEM-768)

## Return type:

Optional[bytes]

<!-- image -->

Note

If NextKey is not set (None in storage), this function returns None. This can happen if no validator has announced the next key yet.

## get\_mev\_shield\_submission(submission\_id, block=None)

Retrieves Submission from the MevShield pallet storage.

If submission\_id is provided, returns a single submission. If submission\_id is None, returns all submissions from the storage map.

## Parameters:

- submission\_id (str) - The hash ID of the submission. Can be a hex string with '0x' prefix or bytes. If None, returns all submissions.
- block (Optional[int]) - The blockchain block number at which to perform the query. If None, uses the current block.

## Returns:

## A dictionary containing the submission data if found, None otherwise. The

dictionary contains: - author: The SS58 address of the account that submitted the encrypted extrinsic - commitment: The blake2\_256 hash of the payload\_core (as hex string with '0x' prefix) - ciphertext: The encrypted blob as bytes (format: [u16 kem\_len][kem\_ct][nonce24][aead\_ct]) -submitted\_in: The block number when the submission was created

If submission\_id is None: A dictionary mapping submission IDs (as hex strings) to submission dictionaries.

## Return type:

If submission\_id is provided

<!-- image -->

Note

If a specific submission does not exist in storage, this function returns None. If querying all submissions and none exist, returns an empty dictionary.

## get\_mev\_shield\_submissions(block=None)

Retrieves all encrypted submissions from the MevShield pallet storage.

This function queries the MevShield.Submissions storage map and returns all pending encrypted submissions that have been submitted via submit\_encrypted but not yet executed via execute\_revealed.

## Parameters:

block (Optional[int]) - The blockchain block number for the query. If None, uses the current block.

## Returns:

A dictionary mapping wrapper\_id (as hex string with '0x' prefix) to submission data dictionaries. Each submission dictionary contains: - author: The SS58 address of the account that submitted the encrypted extrinsic - commitment:

The blake2\_256 hash of the payload\_core as bytes (32 bytes) - ciphertext: The encrypted blob as bytes (format: [u16 kem\_len][kem\_ct][nonce24][aead\_ct]) -submitted\_in: The block number when the submission was created Returns None if no submissions exist in storage at the specified block.

## Return type:

Optional[dict[str, dict[str, str | int]]]

<!-- image -->

## Note

Submissions are automatically pruned after KEY\_EPOCH\_HISTORY blocks (100 blocks) by the pallet's on\_initialize hook. Only submissions that have been submitted but not yet executed will be present in storage.

## get\_minimum\_required\_stake()

[source]

Returns the minimum required stake threshold for nominator cleanup operations.

This threshold is used ONLY for cleanup after unstaking operations. If a nominator's remaining stake falls below this minimum after an unstake, the remaining stake is forcefully cleared and returned to the coldkey to prevent dust accounts.

This is NOT the minimum checked during staking operations. The actual minimum for staking is determined by DefaultMinStake (typically 0.001 TAO plus fees).

## Returns:

The minimum stake threshold as a Balance object. Nominator stakes below this amount are automatically cleared after unstake operations.

## Return type:

bittensor.utils.balance.Balance

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/staking-and-delegation/delegation&gt;

get\_netuids\_for\_hotkey(hotkey\_ss 58 , block=None)

[source]

## Retrieves a list of subnet UIDs (netuids) where a given hotkey is a member. This function identifies the

specific subnets within the Bittensor network where the neuron associated with the hotkey is active.

## Parameters:

- hotkey\_ss58 (str) - The SS58 address of the neuron's hotkey.
- block (Optional[int]) - The blockchain block number for the query. If None, queries the current chain head.

## Returns:

A list of netuids where the neuron is a member.

## Return type:

list[int]

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/glossary#hotkey&gt;

## [source] get\_neuron\_certificate(hotkey\_ss 58 , netuid, block=None)

Retrieves the TLS certificate for a specific neuron identified by its unique identifier (UID) within a specified subnet (netuid) of the Bittensor network.

## Parameters:

- hotkey\_ss58 (str) - The SS58 address of the neuron's hotkey.
- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The blockchain block number for the query. If None, queries the current chain head.

## Returns:

Certificate object containing the neuron's TLS public key and algorithm, or None if the neuron has not registered a certificate.

## Return type:

Optional[bittensor.utils.Certificate]

This function is used for certificate discovery for setting up mutual tls communication between neurons.

## get\_neuron\_for\_pubkey\_and\_subnet(hotkey\_ss 58 , netuid,

block=None)

[source]

Retrieves information about a neuron based on its public key (hotkey SS58 address) and the specific subnet UID (netuid). This function provides detailed neuron information for a particular subnet within the Bittensor network.

## Parameters:

- hotkey\_ss58 (str) - The SS58 address of the neuron's hotkey.
- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

Detailed information about the neuron if found, None otherwise.

## Return type:

Optional

This function is crucial for accessing specific neuron data and understanding its status, stake, and other attributes within a particular subnet of the Bittensor ecosystem.

## get\_next\_epoch\_start\_block(netuid, block=None)

[source]

Calculates the first block number of the next epoch for the given subnet.

If block is not provided, the current chain block will be used. Epochs are determined based on the subnet's tempo (i.e., blocks per epoch). The result is the block number at which the next epoch will begin.

## Parameters:

- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The reference block to calculate from. If None, uses the current chain block height.

## Returns:

The block number at which the next epoch will start, or None if tempo is 0 or invalid.

## Return type:

int

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/glossary#tempo&gt;

## get\_owned\_hotkeys(coldkey\_ss 58 , block=None)

Retrieves all hotkeys owned by a specific coldkey address.

## Parameters:

- coldkey\_ss58 (str) - The SS58 address of the coldkey to query.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

A list of hotkey SS58 addresses owned by the coldkey.

## Return type:

list[str]

## get\_parents(hotkey\_ss 58 , netuid, block=None)

[source]

[source]

This method retrieves the parent of a given hotkey and netuid. It queries the SubtensorModule's ParentKeys storage function to get the children and formats them before returning as a tuple.

## Parameters:

- hotkey\_ss58 (str) - The child hotkey SS58.
- netuid (int) - The netuid value.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

A list of formatted parents [(proportion, parent)]

## Return type:

list[tuple[float, str]]

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/validators/child-hotkeys&gt;
- get\_children() for retrieving child keys

## get\_proxies(block=None)

Retrieves all proxy relationships from the chain.

This method queries the Proxy.Proxies storage map across all accounts and returns a dictionary mapping each real account (delegator) to its list of proxy relationships.

## Parameters:

block (Optional[int]) - The blockchain block number for the query. If None, queries the latest block.

## Returns:

Dictionary mapping real account SS58 addresses to lists of ProxyInfo objects. Each ProxyInfo contains the delegate address, proxy type, and delay for that proxy relationship.

## Return type:

dict[str, list[bittensor.core.chain\_data.ProxyInfo]]

<!-- image -->

## Notes

- This method queries all proxy relationships on the chain, which may be resource-intensive for large networks. Consider using get\_proxies\_for\_real\_account() for querying specific accounts.
- See: &lt;https:/ /docs.learnbittensor.org/keys/proxies&gt;

## get\_proxies\_for\_real\_account(real\_account\_ss 58 , block=None)

Returns proxy/ies associated with the provided real account.

This method queries the Proxy.Proxies storage for a specific real account and returns all proxy relationships where this real account is the delegator. It also returns the deposit amount reserved for these proxies.

## Parameters:

- real\_account\_ss58 (str) - SS58 address of the real account (delegator) whose proxies to retrieve.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

- List of ProxyInfo objects representing all proxy relationships for the real account. Each ProxyInfo

contains delegate address, proxy type, and delay.

- Balance object representing the reserved deposit amount for these proxies. This deposit is held as

long as the proxy relationships exist and is returned when proxies are removed.

## Return type:

Tuple containing

<!-- image -->

## Notes

- If the account has no proxies, returns an empty list and a zero balance.
- See: &lt;https:/ /docs.learnbittensor.org/keys/proxies/create-proxy&gt;

## get\_proxy\_announcement(delegate\_account\_ss 58 , block=None)

Retrieves proxy announcements for a specific delegate account.

This method queries the Proxy.Announcements storage for announcements made by the given delegate proxy account. Announcements allow a proxy to declare its intention to execute a call on behalf of a real account after a delay period.

## Parameters:

- delegate\_account\_ss58 (str) - SS58 address of the delegate proxy account whose announcements to retrieve.
- block (Optional[int]) - The blockchain block number for the query. If None, queries the latest block.

## Returns:

## List of ProxyAnnouncementInfo objects. Each object contains the real account address, call hash, and block

height at which the announcement was made.

## Return type:

list[bittensor.core.chain\_data.ProxyAnnouncementInfo]

<!-- image -->

## Notes

- If the delegate has no announcements, returns an empty list.
- See: &lt;https:/ /docs.learnbittensor.org/keys/proxies&gt;

## get\_proxy\_announcements(block=None)

Retrieves all proxy announcements from the chain.

This method queries the Proxy.Announcements storage map across all delegate accounts and returns a dictionary mapping each delegate to its list of pending announcements.

## Parameters:

block (Optional[int]) - The blockchain block number for the query. If None, queries the latest block.

## Returns:

Dictionary mapping delegate account SS58 addresses to lists of ProxyAnnouncementInfo objects. Each ProxyAnnouncementInfo contains the real account address, call hash, and block height.

## Return type:

dict[str, list[bittensor.core.chain\_data.ProxyAnnouncementInfo]]

<!-- image -->

## Notes

- This method queries all announcements on the chain, which may be resource-intensive for large networks. Consider using get\_proxy\_announcement() for querying specific delegates.
- See: &lt;https:/ /docs.learnbittensor.org/keys/proxies&gt;

## get\_proxy\_constants(constants=None, as\_dict=False, block=None)

Fetches runtime configuration constants from the Proxy pallet.

This method retrieves on-chain configuration constants that define deposit requirements, proxy limits, and announcement constraints for the Proxy pallet. These constants govern how proxy accounts operate within the Subtensor network.

## Parameters:

- constants (Optional[list[str]]) - Optional list of specific constant names to fetch. If omitted, all constants defined in ProxyConstants.constants\_names() are queried. Valid constant names include: 'AnnouncementDepositBase', 'AnnouncementDepositFactor', 'MaxProxies', 'MaxPending',
- 'ProxyDepositBase', 'ProxyDepositFactor'.
- as\_dict (bool) - If True, returns the constants as a dictionary instead of a ProxyConstants object.
- block (Optional[int]) - The blockchain block number for the query. If None, queries the latest block.

## Returns:

ProxyConstants object containing all requested constants. If as\_dict is True:

Dictionary mapping constant names to their values (Balance objects for deposit constants, integers for limit constants).

## Return type:

If as\_dict is False

<!-- image -->

## Notes

- All Balance amounts are returned in RAO. Constants reflect the current chain configuration at the specified

block. - See: &lt;https:/ /docs.learnbittensor.org/keys/proxies&gt;

get\_revealed\_commitment(netuid, uid, block=None)

Returns uid related revealed commitment for a given netuid.

<!-- image -->

## Parameters:

- netuid (int) - The unique identifier of the subnetwork.
- uid (int) - The neuron uid to retrieve the commitment from.
- block (Optional[int]) - The block number to retrieve the commitment from. If None, queries the current chain head.

## Returns:

A tuple of reveal block and commitment message.

## Return type:

Optional[tuple[tuple[int, str], Ellipsis]]

## Example:

```
# sample return value ( (12, "Alice message 1"), (152, "Alice message 2") ) ( (12, "Bob message 1"), (147, "Bob message 2") )
```

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/glossary#commit-reveal&gt;

## get\_revealed\_commitment\_by\_hotkey(netuid, hotkey\_ss 58 ,

block=None)

Retrieves hotkey related revealed commitment for a given subnet.

## Parameters:

- netuid (int) - The unique identifier of the subnetwork.
- hotkey\_ss58 (str) - The ss58 address of the committee member.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

A tuple of reveal block and commitment message.

## Return type:

Optional[tuple[tuple[int, str], Ellipsis]]

[source]

<!-- image -->

- &lt;https:/ /docs.learnbittensor.org/glossary#commit-reveal&gt;

## get\_root\_alpha\_dividends\_per\_subnet(hotkey\_ss 58 , netuid,

block=None)

Retrieves the root alpha dividends per subnet for a given hotkey.

This storage tracks the root alpha dividends that a hotkey has received on a specific subnet. It is updated during block emission distribution when root alpha is distributed to validators.

## Parameters:

- hotkey\_ss58 (str) - The ss58 address of the root validator hotkey.
- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

The root alpha dividends for this hotkey on this subnet in Rao, with unit set to netuid.

## Return type:

Balance

## get\_root\_claim\_type(coldkey\_ss 58 , block=None)

Return the configured root claim type for a given coldkey.

The root claim type controls how dividends from staking to the Root Subnet (subnet 0) are processed when they are claimed:

- Swap (default): Alpha dividends are swapped to TAO at claim time and restaked on the root subnet.
- Keep: Alpha dividends remain as Alpha on the originating subnets.

## Parameters:

- coldkey\_ss58 (str) - The SS58 address of the coldkey whose root claim preference to query.

- block (Optional[int]) - The block number to query. Do not specify if using block\_hash or reuse\_block.

## Returns:

The root claim type as a string, either Swap or Keep, or dict for 'KeepSubnets' in format {'KeepSubnets': {'subnets': [1, 2, 3]}}.

## Return type:

Union[str, dict]

<!-- image -->

## Notes

- The claim type applies to both automatic and manual root claims; it does not affect the original TAO stake on subnet 0, only how Alpha dividends are treated.
- See: &lt;https:/ /docs.learnbittensor.org/staking-and-delegation/rootclaims&gt;
- See also: &lt;https:/ /docs.learnbittensor.org/staking-and-delegation/rootclaims/managing-root-claims&gt;

## get\_root\_claimable\_all\_rates(hotkey\_ss 58 , block=None)

Retrieves all root claimable rates from a given hotkey address for all subnets with this validator.

## Parameters:

- hotkey\_ss58 (str) - The SS58 address of the root validator hotkey.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

Dictionary mapping netuid to a float claimable rate (approximately in the range [0.0, 1.0]) for that subnet. Missing entries imply no claimable Alpha dividends for that subnet.

## Return type:

dict[int, float]

<!-- image -->

## Notes

- See: &lt;https:/ /docs.learnbittensor.org/staking-and-delegation/rootclaims/managing-root-claims&gt;

## get\_root\_claimable\_rate(hotkey\_ss 58 , netuid, block=None)

Return the fraction of root stake currently claimable on a subnet.

This method returns a normalized rate representing how much Alpha dividends are currently claimable on the given subnet relative to the validator's root stake. It is primarily a low-level helper; most users should call get\_root\_claimable\_stake() instead to obtain a Balance.

## Parameters:

- hotkey\_ss58 (str) - The SS58 address of the root validator hotkey.
- netuid (int) - The unique identifier of the subnet whose claimable rate to compute.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

A float representing the claimable rate for this subnet (approximately in the range [0.0, 1.0]). A value of 0.0 means there are currently no claimable Alpha dividends on the subnet.

## Return type:

float

<!-- image -->

## Notes

- Use get\_root\_claimable\_stake() to retrieve the actual claimable amount as a Balance object.
- See: &lt;https:/ /docs.learnbittensor.org/staking-and-delegation/rootclaims/managing-root-claims&gt;

## get\_root\_claimable\_stake(coldkey\_ss 58 , hotkey\_ss 58 , netuid, block=None)

Return the currently claimable Alpha staking dividends for a coldkey from a root validator on a subnet.

## Parameters:

- coldkey\_ss58 (str) - The SS58 address of the delegator's coldkey.
- hotkey\_ss58 (str) - The SS58 address of the root validator hotkey.
- netuid (int) - The subnet ID where Alpha dividends will be claimed.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

Balance representing the Alpha stake currently available to claim on the specified subnet (unit is the subnet's Alpha token).

## Return type:

bittensor.utils.balance.Balance

<!-- image -->

## Notes

- After a successful manual or automatic claim, this value typically drops to zero for that subnet until new dividends accumulate.
- The underlying TAO stake on the Root Subnet remains unaffected; only Alpha dividends are moved or swapped according to the configured root claim type.
- See: &lt;https:/ /docs.learnbittensor.org/staking-and-delegation/rootclaims&gt;
- See also: &lt;https:/ /docs.learnbittensor.org/staking-and-delegation/rootclaims/managing-root-claims&gt;

## get\_root\_claimed(coldkey\_ss 58 , hotkey\_ss 58 , netuid, block=None)

Return the total Alpha dividends already claimed for a coldkey from a root validator on a subnet.

## Parameters:

- coldkey\_ss58 (str) - The SS58 address of the delegator's coldkey.

- hotkey\_ss58 (str) - The SS58 address of the root validator hotkey.
- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

Balance representing the cumulative Alpha stake that has already been claimed from the root validator on the specified subnet.

## Return type:

bittensor.utils.balance.Balance

<!-- image -->

## Notes

- See: &lt;https:/ /docs.learnbittensor.org/staking-and-delegation/rootclaims/managing-root-claims&gt;

## [source] get\_stake(coldkey\_ss 58 , hotkey\_ss 58 , netuid, block=None)

Returns the amount of Alpha staked by a specific coldkey to a specific hotkey within a given subnet. This function retrieves the delegated stake balance, referred to as the ' Alpha' value.

## Parameters:

- coldkey\_ss58 (str) - The SS58 address of the coldkey that delegated the stake. This address owns the stake.
- hotkey\_ss58 (str) - The ss58 address of the hotkey which the stake is on.
- netuid (int) - The unique identifier of the subnet to query.
- block (Optional[int]) - The specific block number at which to retrieve the stake information.

## Returns:

An object representing the amount of Alpha (TAO ONLY if the subnet's netuid is 0) currently staked from the specified coldkey to the specified hotkey within the given subnet.

## Return type:

bittensor.utils.balance.Balance

## get\_stake\_add\_fee(amount, netuid, block=None)

Calculates the fee for adding new stake to a hotkey.

## Parameters:

- amount (bittensor.utils.balance.Balance) - Amount of stake to add in TAO
- netuid (int) - Netuid of subnet
- block (Optional[int]) - Block number at which to perform the calculation

## Returns:

The calculated stake fee as a Balance object in TAO.

## Return type:

bittensor.utils.balance.Balance

## get\_stake\_for\_coldkey\_and\_hotkey(coldkey\_ss 58 , hotkey\_ss 58 ,

netuids=None, block=None)

Retrieves all coldkey-hotkey pairing stake across specified (or all) subnets

## Parameters:

- coldkey\_ss58 (str) - The SS58 address of the coldkey.
- hotkey\_ss58 (str) - The SS58 address of the hotkey.
- netuids (Optional[bittensor.core.types.UIDs]) - The subnet IDs to query for. Set to None for all subnets.
- block (Optional[int]) - The block number at which to query the stake information.

## Returns:

A netuid to StakeInfo mapping of all stakes across all subnets.

## Return type:

dict[int, bittensor.core.chain\_data.StakeInfo]

## [source] get\_stake\_for\_hotkey(hotkey\_ss 58 , netuid, block=None)

Retrieves the stake information for a given hotkey.

## Parameters:

- hotkey\_ss58 (str) - The SS58 address of the hotkey.

[source]

<!-- image -->

- netuid (int) - The subnet ID to query for.
- block (Optional[int]) - The block number at which to query the stake information.

## Return type:

bittensor.utils.balance.Balance

## get\_stake\_info\_for\_coldkey(coldkey\_ss 58 , block=None)

Retrieves the stake information for a given coldkey.

## Parameters:

- coldkey\_ss58 (str) - The SS58 address of the coldkey.
- block (Optional[int]) - The block number at which to query the stake information.

## Returns:

List of StakeInfo objects.

## Return type:

list[bittensor.core.chain\_data.StakeInfo]

## get\_stake\_info\_for\_coldkeys(coldkey\_ss 58 s, block=None)

Retrieves the stake information for multiple coldkeys.

## Parameters:

- coldkey\_ss58s (list[str]) - A list of SS58 addresses of the coldkeys to query.
- block (Optional[int]) - The block number at which to query the stake information.

## Returns:

The dictionary mapping coldkey addresses to a list of StakeInfo objects.

## Return type:

dict[str, list[bittensor.core.chain\_data.StakeInfo]]

[source] get\_stake\_movement\_fee(origin\_netuid, destination\_netuid, amount, block=None)

Calculates the fee for moving stake between hotkeys/subnets/coldkeys.

## Parameters:

- origin\_netuid (int) - Netuid of source subnet.
- destination\_netuid (int) - Netuid of the destination subnet.
- amount (bittensor.utils.balance.Balance) - Amount of stake to move.
- block (Optional[int]) - The block number for which the children are to be retrieved.

## Returns:

The calculated stake fee as a Balance object

## Return type:

bittensor.utils.balance.Balance

## get\_stake\_weight(netuid, block=None)

Retrieves the stake weight for all hotkeys in a given subnet.

## Parameters:

- netuid (int) - Netuid of subnet.
- block (Optional[int]) - Block number at which to perform the calculation.

## Returns:

A list of stake weights for all hotkeys in the specified subnet.

## Return type:

list[float]

## get\_subnet\_burn\_cost(block=None)

[source]

Retrieves the burn cost for registering a new subnet within the Bittensor network. This cost represents the amount of Tao that needs to be locked or burned to establish a new subnet.

## Parameters:

block (Optional[int]) - The blockchain block number for the query.

## Returns:

The burn cost for subnet registration.

## Return type:

int

The subnet burn cost is an important economic parameter, reflecting the network's mechanisms for controlling the proliferation of subnets and ensuring their commitment to the network's long-term viability.

## [source] get\_subnet\_hyperparameters(netuid, block=None)

Retrieves the hyperparameters for a specific subnet within the Bittensor network. These hyperparameters define the operational settings and rules governing the subnet's behavior.

## Parameters:

- netuid (int) - The network UID of the subnet to query.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

The subnet's hyperparameters, or None if not available.

## Return type:

Optional[Union[list, bittensor.core.chain\_data.SubnetHyperparameters]]

Understanding the hyperparameters is crucial for comprehending how subnets are configured and managed, and how they interact with the network's consensus and incentive mechanisms.

## get\_subnet\_info(netuid, block=None)

[source]

Retrieves detailed information about subnet within the Bittensor network. This function provides comprehensive data on subnet, including its characteristics and operational parameters.

## Parameters:

- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

A SubnetInfo objects, each containing detailed information about a subnet.

## Return type:

## SubnetInfo

Gaining insights into the subnet's details assists in understanding the network's composition, the roles of different subnets, and their unique features.

## get\_subnet\_owner\_hotkey(netuid, block=None)

Retrieves the hotkey of the subnet owner for a given network UID.

This function queries the subtensor network to fetch the hotkey of the owner of a subnet specified by its netuid. If no data is found or the query fails, the function returns None.

## Parameters:

- netuid (int) - The network UID of the subnet to fetch the owner's hotkey for.
- block (Optional[int]) - The blockchain block number for the query. If None, queries the current chain head.

## Returns:

The hotkey of the subnet owner if available; None otherwise.

## Return type:

Optional[str]

## get\_subnet\_price(netuid, block=None)

Gets the current Alpha price in TAO for the specified subnet.

## Parameters:

- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The blockchain block number for the query. If None, queries the current chain head.

## Returns:

The current Alpha price in TAO units for the specified subnet.

## Return type:

bittensor.utils.balance.Balance

[source]

[source]

<!-- image -->

## Notes

Subnet 0 (root network) always returns 1 TAO since it uses TAO directly rather than Alpha.

## get\_subnet\_prices(block=None)

Gets the current Alpha price in TAO for all subnets.

## Parameters:

block (Optional[int]) - The blockchain block number for the query. If None, queries the current chain head.

## Returns:

A dictionary mapping subnet unique ID (netuid) to the current Alpha price in TAO units.

## Return type:

dict[int, bittensor.utils.balance.Balance]

<!-- image -->

## Notes

Subnet 0 (root network) always has a price of 1 TAO since it uses TAO directly rather than Alpha.

## [source] get\_subnet\_reveal\_period\_epochs(netuid, block=None)

Retrieves the SubnetRevealPeriodEpochs hyperparameter for a specified subnet.

This hyperparameter determines the number of epochs that must pass before a committed weight can be revealed in the commit-reveal mechanism.

## Parameters:

- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The blockchain block number for the query. If None, queries the current chain head.

## Returns:

The number of epochs in the reveal period for the subnet.

[source]

## Return type:

int

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/glossary#commit-reveal&gt;

## [source] get\_subnet\_validator\_permits(netuid, block=None)

<!-- image -->

Retrieves the list of validator permits for a given subnet as boolean values.

## Parameters:

- netuid (int) - The unique identifier of the subnetwork.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

A list of boolean values representing validator permits, or None if not available.

## Return type:

Optional[list[bool]]

## get\_timelocked\_weight\_commits(netuid, mechid=0, block=None)

Retrieves CRv4 (Commit-Reveal version 4) weight commit information for a specific subnet.

This method retrieves timelocked weight commitments made by validators using the commit-reveal mechanism. The raw byte/vector encoding from the chain is automatically parsed and converted into a structured format via WeightCommitInfo.

## Parameters:

- netuid (int) - The unique identifier of the subnet.
- mechid (int) - Subnet mechanism identifier (default 0 for primary mechanism).
- block (Optional[int]) - The blockchain block number for the query. If None, queries the current chain head.

## Returns:

- ss58\_address: The SS58 address of the committer.
- commit\_block: The block number when the commitment was made.

- commit\_message: The commit message (encoded commitment data).
- reveal\_round: The drand round when the commitment can be revealed.

## Return type:

A list of commit details, where each item is a tuple containing

<!-- image -->

## Notes

The list may be empty if there are no commits found. -

&lt;https:/ /docs.learnbittensor.org/resources/glossary#commit-reveal&gt;

## get\_timestamp(block=None)

Retrieves the datetime timestamp for a given block

## Parameters:

block (Optional[int]) - The blockchain block number for the query.

## Returns:

datetime object for the timestamp of the block

## Return type:

datetime.datetime

## get\_total\_subnets(block=None)

[source]

[source]

Retrieves the total number of subnets within the Bittensor network as of a specific blockchain block.

## Parameters:

block (Optional[int]) - The blockchain block number for the query. If None, queries the current chain head.

## Returns:

The total number of subnets in the network.

## Return type:

Optional[int]

## get\_transfer\_fee(wallet, destination\_ss 58 , amount,

keep\_alive=True)

[source]

Calculates the transaction fee for transferring tokens from a wallet to a specified destination address. This function simulates the transfer to estimate the associated cost, taking into account the current network conditions and transaction complexity.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet from which the transfer is initiated.
- destination\_ss58 (str) - The SS58 address of the destination account.
- amount (Optional[bittensor.utils.balance.Balance]) - The amount of tokens to be transferred, specified as a Balance object, or in Tao or Rao units.
- keep\_alive (bool) - Whether the transfer fee should be calculated based on keeping the wallet alive (existential deposit) or not.

## Returns:

The estimated transaction fee for the transfer, represented as a Balance object.

## Return type:

bittensor.utils.balance.Balance

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/learn/fees&gt;

## get\_uid\_for\_hotkey\_on\_subnet(hotkey\_ss 58 , netuid, block=None)

[source] Retrieves the unique identifier (UID) for a neuron's hotkey on a specific subnet.

## Parameters:

- hotkey\_ss58 (str) - The SS58 address of the neuron's hotkey.
- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

The UID of the neuron if it is registered on the subnet, None otherwise.

## Return type:

Optional[int]

The UID is a critical identifier within the network, linking the neuron's hotkey to its operational and governance activities on a particular subnet.

get\_unstake\_fee(netuid, amount, block=None)

Calculates the fee for unstaking from a hotkey.

## Parameters:

- netuid (int) - The unique identifier of the subnet.
- amount (bittensor.utils.balance.Balance) - Amount of stake to unstake in TAO.
- block (Optional[int]) - The blockchain block number for the query. If None, queries the current chain head.

## Returns:

The calculated stake fee as a Balance object in Alpha.

## Return type:

bittensor.utils.balance.Balance

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/learn/fees&gt;

## get\_vote\_data(proposal\_hash, block=None)

[source]

Retrieves the voting data for a specific proposal on the Bittensor blockchain. This data includes information about how senate members have voted on the proposal.

## Parameters:

- proposal\_hash (str) - The hash of the proposal for which voting data is requested.
- block (Optional[int]) - The blockchain block number for the query. If None, queries the current chain head.

## Returns:

An object containing the proposal's voting data, or None if not found.

[source]

## Return type:

Optional[bittensor.core.chain\_data.ProposalVoteData]

This function is important for tracking and understanding the decision-making processes within the Bittensor network, particularly how proposals are received and acted upon by the governing body.

## immunity\_period(netuid, block=None)

[source]

Retrieves the 'ImmunityPeriod' hyperparameter for a specific subnet. This parameter defines the duration during which new neurons are protected from certain network penalties or restrictions.

## Parameters:

- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

The value of the 'ImmunityPeriod' hyperparameter if the subnet exists, None otherwise.

## Return type:

Optional[int]

The 'ImmunityPeriod' is a critical aspect of the network's governance system, ensuring that new participants have a grace period to establish themselves and contribute to the network without facing immediate punitive actions.

## is\_fast\_blocks()

Checks if the node is running with fast blocks enabled.

Fast blocks have a block time of 10 seconds, compared to the standard 12-second block time. This affects transaction timing and network synchronization.

## Returns:

True if fast blocks are enabled (10-second block time), False otherwise (12-second block time).

## Return type:

[source]

<!-- image -->

## bool

## Notes

- &lt;https:/ /docs.learnbittensor.org/resources/glossary#fast-blocks&gt;

## [source] is\_hotkey\_delegate(hotkey\_ss 58 , block=None)

Determines whether a given hotkey (public key) is a delegate on the Bittensor network. This function checks if the neuron associated with the hotkey is part of the network's delegation system.

## Parameters:

- hotkey\_ss58 (str) - The SS58 address of the neuron's hotkey.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

True if the hotkey is a delegate, False otherwise.

## Return type:

bool

Being a delegate is a significant status within the Bittensor network, indicating a neuron's involvement in consensus and governance processes.

## is\_hotkey\_registered(hotkey\_ss 58 , netuid=None, block=None)

[source] Determines whether a given hotkey (public key) is registered in the Bittensor network, either globally across any subnet or specifically on a specified subnet. This function checks the registration status of a neuron identified by its hotkey, which is crucial for validating its participation and activities within the network.

## Parameters:

- hotkey\_ss58 (str) - The SS58 address of the neuron's hotkey.
- netuid (Optional[int]) - The unique identifier of the subnet to check the registration. If None, the registration is checked across all subnets.
- block (Optional[int]) - The blockchain block number at which to perform the query.

## Returns:

Trueif the hotkey is registered in the specified context (either any subnet or a specific subnet),

False otherwise.

## Return type:

bool

This function is important for verifying the active status of neurons in the Bittensor network. It aids in understanding whether a neuron is eligible to participate in network processes such as consensus, validation, and incentive distribution based on its registration status.

## [source] is\_hotkey\_registered\_any(hotkey\_ss 58 , block=None)

Checks if a neuron's hotkey is registered on any subnet within the Bittensor network.

## Parameters:

- hotkey\_ss58 (str) - The SS58 address of the neuron's hotkey.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

True if the hotkey is registered on any subnet, False otherwise.

## Return type:

bool

## is\_hotkey\_registered\_on\_subnet(hotkey\_ss 58 , netuid, block=None)

Checks if the hotkey is registered on a given subnet.

## Parameters:

- hotkey\_ss58 (str) - The SS58 address of the hotkey to check.
- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The blockchain block number for the query. If None, queries the current chain head.

## Returns:

True if the hotkey is registered on the specified subnet, False otherwise.

[source]

## Return type:

bool

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/glossary#hotkey&gt;

## is\_in\_admin\_freeze\_window(netuid, block=None)

Returns True if the current block is within the terminal freeze window of the tempo for the given subnet. During this window, admin ops are prohibited to avoid interference with validator weight submissions.

## Parameters:

- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

True if in freeze window, else False.

## Return type:

bool

## is\_subnet\_active(netuid, block=None)

Verifies if a subnet with the provided netuid is active.

A subnet is considered active if the start\_call extrinsic has been executed. A newly registered subnet may exist but not be active until the subnet owner calls start\_call to begin emissions.

## Parameters:

- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The blockchain block number for the query. If None, queries the current chain head.

## Returns:

True if the subnet is active (emissions have started), False otherwise.

## Return type:

[source]

## bool

## Notes 

<!-- image -->

- &lt;https:/ /docs.learnbittensor.org/subnets/working-with-subnets&gt;

kill\_pure\_proxy(wallet, pure\_proxy\_ss 58 , spawner, proxy\_type, index, height, ext\_index, force\_proxy\_type=ProxyType.Any, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True) Kills (removes) a pure proxy account.

This method removes a pure proxy account that was previously created via create\_pure\_proxy() . The kill\_pure call must be executed through the pure proxy account itself, with the spawner acting as an 'Any' proxy. This method automatically handles this by executing the call via proxy() .

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor wallet object. The wallet.coldkey.ss58\_address must be the spawner of the pure proxy (the account that created it via create\_pure\_proxy() ). The spawner must have an 'Any' proxy relationship with the pure proxy.
- pure\_proxy\_ss58 (str) - The SS58 address of the pure proxy account to be killed. This is the address that was returned in the create\_pure\_proxy() response.
- spawner (str) - The SS58 address of the spawner account (the account that originally created the pure proxy via create\_pure\_proxy() ). This should match wallet.coldkey.ss58\_address.
- proxy\_type (Union[str, bittensor.core.chain\_data.ProxyType]) - The type of proxy permissions. Can be a string or ProxyType enum value. Must match the proxy\_type used when creating the pure proxy.
- index (int) - The salt value (u16, range 0-65535) originally used in create\_pure\_proxy() to generate this pure proxy's address. This value,

- combined with proxy\_type, delay, and spawner, uniquely identifies the pure proxy to be killed. Must match exactly the index used during creation.
- height (int) - The block height at which the pure proxy was created.
- ext\_index (int) - The extrinsic index at which the pure proxy was created.
- force\_proxy\_type (Optional[Union[str, bittensor.core.chain\_data.ProxyType]]) The proxy type relationship to use when executing kill\_pure through the proxy mechanism. Since pure proxies are keyless and cannot sign transactions, the spawner must act as a proxy for the pure proxy to execute kill\_pure. This parameter specifies which proxy type relationship between the spawner and the pure proxy account should be used. The spawner must have a proxy relationship of this type (or Any) with the pure proxy account. Defaults to ProxyType.Any for maximum compatibility. If None, Substrate will automatically select an available proxy type from the spawner's proxy relationships.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the inclusion of the transaction.
- wait\_for\_finalization (bool) - Whether to wait for the finalization of the transaction.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

<!-- image -->

## Notes

- The kill\_pure call must be executed through the pure proxy account itself, with the spawner acting as an Any proxy. This method automatically handles this by executing the call via proxy() . The spawner must have an Any proxy relationship with the pure proxy for this to work.
- See: &lt;https:/ /docs.learnbittensor.org/keys/proxies/pure-proxies&gt;

<!-- image -->

## Warning ⚠

All access to this account will be lost. Any funds remaining in the pure proxy account will become permanently inaccessible after this operation.

## last\_drand\_round()

Retrieves the last drand round emitted in Bittensor.

Drand (distributed randomness) rounds are used to determine when committed weights can be revealed in the commit-reveal mechanism. This method returns the most recent drand round number, which corresponds to the timing for weight reveals.

## Returns:

The latest drand round number emitted in Bittensor, or None if no round has been stored.

## Return type:

Optional[int]

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/resources/glossary#drandtime-lockencryption&gt;

## log\_verbose  =  False

## [source]

## max\_weight\_limit(netuid, block=None)

Returns the MaxWeightsLimit hyperparameter for a subnet.

## Parameters:

- netuid (int) - The unique identifier of the subnetwork.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

The stored maximum weight limit as a normalized float in Noneif the

[0, 1], or subnetwork does not exist. Note: this value is not actually enforced - the weight validation code uses a hardcoded u16::MAX instead.

## Return type:

Optional[float]

<!-- image -->

## Notes

- This hyperparameter is now a constant rather than a settable variable.
- &lt;https:/ /docs.learnbittensor.org/subnets/subnet-hyperparameters&gt;

metagraph(netuid, mechid=0, lite=True, block=None)

## [source]

Returns a synced metagraph for a specified subnet within the Bittensor network. The metagraph represents the network's structure, including neuron connections and interactions.

## Parameters:

- netuid (int) - The network UID of the subnet to query.
- mechid (int) - Subnet mechanism identifier.
- lite (bool) - If True, returns a metagraph using a lightweight sync (no weights, no bonds).
- block (Optional[int]) - Block number for synchronization, or None for the latest block.

## Returns:

The metagraph representing the subnet's structure and neuron relationships.

## Return type:

<!-- image -->

## bittensor.core.metagraph.Metagraph

The metagraph is an essential tool for understanding the topology and dynamics of the Bittensor network's decentralized architecture, particularly in relation to neuron interconnectivity and consensus processes.

mev\_submit\_encrypted(wallet, call, sign\_with='coldkey', *, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True, blocks\_for\_revealed\_execution=3)

Submits an encrypted extrinsic to the MEV Shield pallet.

This function encrypts a call using ML-KEM-768 + XChaCha20Poly1305 and submits it to the MevShield pallet. The extrinsic remains encrypted in the transaction pool until it is included in a block and decrypted by validators.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet used to sign the extrinsic (must be unlocked, coldkey will be used for signing).
- call (scalecodec.types.GenericCall) - The GenericCall object to encrypt and submit.
- sign\_with (str) - The keypair to use for signing the inner call/extrinsic. Can be either 'coldkey' or 'hotkey'.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the inclusion of the transaction.
- wait\_for\_finalization (bool) - Whether to wait for the finalization of the transaction.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the executed event, indicating that validators have successfully decrypted and executed the inner

<!-- image -->

<!-- image -->

call. If True, the function will poll subsequent blocks for the event matching this submission's commitment.

- blocks\_for\_revealed\_execution (int) - Maximum number of blocks to poll for the executed event after inclusion. The function checks blocks from start\_block+1 to start\_block + blocks\_for\_revealed\_execution. Returns immediately if the event is found before the block limit is reached.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

## Raises:

- ValueError - If NextKey is not available in storage or encryption fails.
- SubstrateRequestException - If the extrinsic fails to be submitted or included.

## Note

The encryption uses the public key from NextKey storage, which rotates every block. The payload structure is: payload\_core = signer\_bytes (32B) + nonce (u32 LE, 4B) + SCALE(call) plaintext = payload\_core + b'x01' + signature (64B for sr25519) commitment = blake2\_256(payload\_core)

## Notes

For detailed documentation and examples of MEV Shield protection, see:

&lt;https:/ /docs.learnbittensor.org/sdk/mev-protection&gt;

For creating GenericCall objects to use with this method, see:

&lt;https:/ /docs.learnbittensor.org/sdk/call&gt;

## min\_allowed\_weights(netuid, block=None)

Returns the MinAllowedWeights hyperparameter for a subnet.

This hyperparameter sets the minimum length of the weights vector that a validator must submit. It checks weights.len() &gt;= MinAllowedWeights. For example, a validator could submit [1000, 0, 0, 0] to satisfy MinAllowedWeights=4, but this would fail if

[source]

MinAllowedWeights were set to 5. This ensures validators distribute attention across the subnet.

## Parameters:

- netuid (int) - The unique identifier of the subnetwork.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

The minimum number of required weight connections, or

Noneif the subnetwork does not

exist or the parameter is not found.

## Return type:

Optional[int]

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/subnets/subnet-hyperparameters&gt;

modify\_liquidity(wallet, netuid, position\_id, liquidity\_delta, hotkey\_ss 58 =None, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

[source] Modifies liquidity in liquidity position by adding or removing liquidity from it.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet used to sign the extrinsic (must be unlocked).
- netuid (int) - The UID of the target subnet for which the call is being initiated.
- position\_id (int) - The id of the position record in the pool.
- liquidity\_delta (bittensor.utils.balance.Balance) - The amount of liquidity to be added or removed (add if positive or remove if negative).
- hotkey\_ss58 (Optional[str]) - The hotkey with staked TAO in Alpha. If not passed then the wallet hotkey is used.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The

- transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the extrinsic to be included in a block.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

## Example:

```
import bittensor as bt subtensor = bt.subtensor(network="local") my_wallet = bt.Wallet() # if liquidity_delta is negative my_liquidity_delta = Balance.from_tao(100) * -1 subtensor.modify_liquidity( wallet=my_wallet, netuid=123, position_id=2, liquidity_delta=my_liquidity_delta ) # if liquidity_delta is positive my_liquidity_delta = Balance.from_tao(120) subtensor.modify_liquidity( wallet=my_wallet, netuid=123, position_id=2, liquidity_delta=my_liquidity_delta )
```

Note: Modifying is allowed even when user liquidity is enabled in specified subnet. Call toggle\_user\_liquidity to enable/disable user liquidity.

```
[source] move_stake(wallet, origin_netuid, origin_hotkey_ss 58 , destination_netuid, destination_hotkey_ss 58 , amount=None, move_all_stake=False, *, mev_protection=DEFAULT_MEV_PROTECTION, period=DEFAULT_PERIOD, raise_error=False, wait_for_inclusion=True, wait_for_finalization=True, wait_for_revealed_execution=True) Moves stake to a different hotkey and/or subnet.
```

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet to move stake from.
- origin\_netuid (int) - The netuid of the source subnet.
- origin\_hotkey\_ss58 (str) - The SS58 address of the source hotkey.
- destination\_netuid (int) - The netuid of the destination subnet.
- destination\_hotkey\_ss58 (str) - The SS58 address of the destination hotkey.
- amount (Optional[bittensor.utils.balance.Balance]) - Amount of stake to move.
- move\_all\_stake (bool) - If True, moves all stake from the source hotkey to the destination hotkey.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Waits for the transaction to be included in a block.
- wait\_for\_finalization (bool) - Waits for the transaction to be finalized on the blockchain.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

## Notes 

<!-- image -->

- Price Protection: &lt;https:/ /docs.learnbittensor.org/learn/priceprotection&gt;
- Rate Limits: &lt;https:/ /docs.learnbittensor.org/learn/chain-ratelimits#staking-operations-rate-limits&gt;

## neuron\_for\_uid(uid, netuid, block=None)

## [source]

Retrieves detailed information about a specific neuron identified by its unique identifier (UID) within a specified subnet (netuid) of the Bittensor network. This function provides a comprehensive view of a neuron's attributes, including its stake, rank, and operational status.

## Parameters:

- uid (int) - The unique identifier of the neuron.
- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

Detailed information about the neuron if found, a null neuron otherwise

## Return type:

bittensor.core.chain\_data.NeuronInfo

This function is crucial for analyzing individual neurons' contributions and status within a specific subnet, offering insights into their roles in the network's consensus and validation mechanisms.

## neurons(netuid, block=None)

[source]

Retrieves a list of all neurons within a specified subnet of the Bittensor network. This function provides a snapshot of the subnet's neuron population, including each neuron's attributes and network interactions.

## Parameters:

- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

A list of NeuronInfo objects detailing each neuron's characteristics in the subnet.

## Return type:

list[bittensor.core.chain\_data.NeuronInfo]

Understanding the distribution and status of neurons within a subnet is key to comprehending the network's decentralized structure and the dynamics of its consensus and governance processes.

## neurons\_lite(netuid, block=None)

## [source]

Retrieves a list of neurons in a 'lite' format from a specific subnet of the Bittensor network. This function provides a streamlined view of the neurons, focusing on key attributes such as stake and network participation.

## Parameters:

- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

A list of simplified neuron information for the subnet.

## Return type:

list[bittensor.core.chain\_data.NeuronInfoLite]

This function offers a quick overview of the neuron population within a subnet, facilitating efficient analysis of the network's decentralized structure and neuron dynamics.

poke\_deposit(wallet, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Adjusts deposits made for proxies and announcements based on current values.

This method recalculates and updates the locked deposit amounts for both proxy relationships and announcements for the signing account. It can be used to potentially lower the locked amount if the deposit requirements have changed (e.g., due to runtime upgrades or changes in the number of proxies/announcements).

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor wallet object (the account whose deposits will be adjusted).
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the inclusion of the transaction.
- wait\_for\_finalization (bool) - Whether to wait for the finalization of the transaction.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

<!-- image -->

## Note

This method automatically adjusts deposits for both proxy relationships and announcements. No parameters are needed as it operates on the account's current state.

## When to use:

- After runtime upgrade, if deposit constants have changed.
- After removing proxies/announcements, to free up excess locked funds.
- Periodically to optimize locked deposit amounts.

proxy(wallet, real\_account\_ss 58 , force\_proxy\_type, call, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD,

raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Executes a call on behalf of the real account through a proxy.

This method allows a proxy account (delegate) to execute a call on behalf of the real account (delegator). The call is subject to the permissions defined by the proxy type and must respect the delay period if one was set when the proxy was added.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor wallet object (should be the proxy account wallet).
- real\_account\_ss58 (str) - The SS58 address of the real account on whose behalf the call is being made.
- force\_proxy\_type (Optional[Union[str, bittensor.core.chain\_data.ProxyType]]) The type of proxy to use for the call. If None, any proxy type can be used. Otherwise, must match one of the allowed proxy types. Can be a string or ProxyType enum value.
- call (scalecodec.types.GenericCall) - The inner call to be executed on behalf of the real account.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the inclusion of the transaction.
- wait\_for\_finalization (bool) - Whether to wait for the finalization of the transaction.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

## ExtrinsicResponse

<!-- image -->

## Note

The call must be permitted by the proxy type. For example, a 'NonTransfer' proxy cannot execute transfer calls. The delay period must also have passed since the proxy was added.

proxy\_announced(wallet, delegate\_ss 58 , real\_account\_ss 58 , force\_proxy\_type, call, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Executes an announced call on behalf of the real account through a proxy.

This method executes a call that was previously announced via announce\_proxy() . The call must match the call\_hash that was announced, and the delay period must have passed since the announcement was made. The real account has the opportunity to review and reject the announcement before execution.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor wallet object (should be the proxy account wallet that made the announcement).
- delegate\_ss58 (str) - The SS58 address of the delegate proxy account that made the announcement.
- real\_account\_ss58 (str) - The SS58 address of the real account on whose behalf the call will be made.
- force\_proxy\_type (Optional[Union[str, bittensor.core.chain\_data.ProxyType]]) The type of proxy to use for the call. If None, any proxy type can be used. Otherwise, must match one of the allowed proxy types. Can be a string or ProxyType enum value.
- call (scalecodec.types.GenericCall) - The inner call to be executed on behalf of the real account (must match the announced call\_hash).
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The

- transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the inclusion of the transaction.
- wait\_for\_finalization (bool) - Whether to wait for the finalization of the transaction.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

## Note 

<!-- image -->

The call\_hash of the provided call must match the call\_hash that was announced. The announcement must not have been rejected by the real account, and the delay period must have passed.

## [source] query\_constant(module\_name, constant\_name, block=None)

Retrieves a constant from the specified module on the Bittensor blockchain.

Use this function for nonstandard queries to constants defined within the Bittensor blockchain, if these cannot be accessed through other, standard getter methods.

## Parameters:

- module\_name (str) - The name of the module containing the constant (e.g., Balances, SubtensorModule).
- constant\_name (str) - The name of the constant to retrieve (e.g., ExistentialDeposit).

- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

A SCALE-decoded object if found, None otherwise. Access the actual value using .value attribute. Common types include int (for counts/blocks), Balance objects (for amounts in Rao), and booleans.

## Return type:

Optional[async\_substrate\_interface.types.ScaleObj]

## query\_identity(coldkey\_ss 58 , block=None)

[source]

Queries the identity of a neuron on the Bittensor blockchain using the given key. This function retrieves detailed identity information about a specific neuron, which is a crucial aspect of the network's decentralized identity and governance system.

## Parameters:

- coldkey\_ss58 (str) - Coldkey used to query the neuron's identity (technically the neuron's coldkey SS58 address).
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

An object containing the identity information of the neuron if found, None otherwise.

## Return type:

Optional[bittensor.core.chain\_data.chain\_identity.ChainIdentity]

The identity information can include various attributes such as the neuron's stake, rank, and other network-specific details, providing insights into the neuron's role and status within the Bittensor network.

<!-- image -->

Note

See the Bittensor CLI documentation for supported identity parameters.

query\_map(module, name, params=None, block=None)

Queries map storage from any module on the Bittensor blockchain.

[source]

Use this function for nonstandard queries to map storage defined within the Bittensor blockchain, if these cannot be accessed through other, standard getter methods.

## Parameters:

- module (str) - The name of the module from which to query the map storage (e.g., 'SubtensorModule', 'System').
- name (str) - The specific storage function within the module to query (e.g., 'Bonds', 'Weights').
- params (Optional[list]) - Parameters to be passed to the query.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

A data structure representing the map storage if found, None otherwise.

## Return type:

QueryMapResult

## query\_map\_subtensor(name, params=None, block=None)

[source]

Queries map storage from the Subtensor module on the Bittensor blockchain.

Use this function for nonstandard queries to map storage defined within the Bittensor blockchain, if these cannot be accessed through other, standard getter methods.

## Parameters:

- name (str) - The name of the map storage function to query.
- params (Optional[list]) - A list of parameters to pass to the query function.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

An object containing the map-like data structure, or None if not found.

## Return type:

async\_substrate\_interface.sync\_substrate.QueryMapResult query\_module(module, name, params=None, block=None)

[source]

Queries any module storage on the Bittensor blockchain with the specified parameters and block number. This function is a generic query interface that allows for flexible and diverse data retrieval from various blockchain modules. Use this function for nonstandard queries to storage defined within the Bittensor blockchain, if these cannot be accessed through other, standard getter methods.

## Parameters:

- module (str) - The name of the module from which to query data.
- name (str) - The name of the storage function within the module.
- params (Optional[list]) - A list of parameters to pass to the query function.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

An object containing the requested data if found, None otherwise.

## Return type:

Optional[Union[async\_substrate\_interface.types.ScaleObj, Any, bittensor.utils.balance.FixedPoint]]

query\_runtime\_api(runtime\_api, method, params=None, block=None)

[source] Queries the runtime API of the Bittensor blockchain, providing a way to interact with the underlying runtime and retrieve data encoded in Scale Bytes format. Use this function for nonstandard queries to the runtime environment, if these cannot be accessed through other, standard getter methods.

## Parameters:

- runtime\_api (str) - The name of the runtime API to query.
- method (str) - The specific method within the runtime API to call.
- params (Optional[Union[list[Any], dict[str, Any]]]) - The parameters to pass to the method call.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

The decoded result from the runtime API call, or None if the call fails.

## Return type:

Any

## [source] query\_subtensor(name, params=None, block=None)

Queries named storage from the Subtensor module on the Bittensor blockchain.

Use this function for nonstandard queries to constants defined within the Bittensor blockchain, if these cannot be accessed through other, standard getter methods.

## Parameters:

- name (str) - The name of the storage function to query.
- params (Optional[list]) - A list of parameters to pass to the query function.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

An object containing the requested data.

## Return type:

query\_response

## recycle(netuid, block=None)

Retrieves the 'Burn' hyperparameter for a specified subnet.

The 'Burn' parameter represents the amount of TAO that is recycled when registering a neuron on this subnet. Recycled tokens are removed from circulation but can be reemitted, unlike burned tokens which are permanently removed.

## Parameters:

- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

The amount of TAO recycled per neuron registration, or None if the subnet does not exist.

## Return type:

[source]

<!-- image -->

## Optional[bittensor.utils.balance.Balance]

## Notes

- &lt;https:/ /docs.learnbittensor.org/resources/glossary#recycling-andburning&gt;

## refund\_crowdloan(wallet, crowdloan\_id, *,

mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True,

wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Refunds contributors from a failed crowdloan campaign that did not reach its cap.

Refunds are batched, processing up to RefundContributorsLimit (default 50) contributors per call. For campaigns with more contributors, multiple calls are required. Only non-creator contributors are refunded; the creator's deposit remains until dissolution via dissolve\_crowdloan.

Only the crowdloan creator can call this method for a non-finalized crowdloan.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor wallet instance used to sign the transaction (must be the crowdloan creator).
- crowdloan\_id (int) - The unique identifier of the crowdloan to refund.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after submission.
- raise\_error (bool) - If True, raises an exception rather than returning failure in the response.
- wait\_for\_inclusion (bool) - Whether to wait for the extrinsic to be included in a block.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic.

- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

ExtrinsicResponse indicating success or failure, with error details if applicable.

## Return type:

bittensor.core.types.ExtrinsicResponse

<!-- image -->

## Notes

- Crowdloans Overview: &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans&gt;
- Crowdloan Lifecycle: &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans#crowdloanlifecycle&gt;
- Refund and Dissolve:
- &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans/crowdloanstutorial#alternative-path-refund-and-dissolve&gt;

register(wallet, netuid, max\_allowed\_attempts=3, num\_processes=None, update\_interval=None, log\_verbose=False, *, output\_in\_place=True, cuda=False, dev\_id=0, tpb=256, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True,

wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

[source] Registers a neuron on the Bittensor subnet with provided netuid using the provided wallet.

Registration is a critical step for a neuron to become an active participant in the network, enabling it to stake, set weights, and receive incentives.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet associated with the neuron to be registered.
- netuid (int) - The unique identifier of the subnet.

- max\_allowed\_attempts (int) - Maximum number of attempts to register the wallet.
- output\_in\_place (bool) - If True, prints the progress of the proof of work to the console in-place. Meaning the progress is printed on the same lines.
- cuda (bool) - If true, the wallet should be registered using CUDA device(s).
- dev\_id (Union[list[int], int]) - The CUDA device id to use, or a list of device ids.
- tpb (int) - The number of threads per block (CUDA).
- num\_processes (Optional[int]) - The number of processes to use to register.
- update\_interval (Optional[int]) - The number of nonces to solve between updates.
- log\_verbose (bool) - If true, the registration process will log more information.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the inclusion of the transaction.
- wait\_for\_finalization (bool) - Whether to wait for the finalization of the transaction.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

This function facilitates the entry of new neurons into the network, supporting the decentralized growth and scalability of the Bittensor ecosystem.

<!-- image -->

## Notes

- Rate Limits: &lt;https:/ /docs.learnbittensor.org/learn/chain-ratelimits#registration-rate-limits&gt;

register\_subnet(wallet, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Registers a new subnetwork on the Bittensor network.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet to be used for subnet registration.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the extrinsic to be included in a block.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

[source]

<!-- image -->

## Notes

- Rate Limits: &lt;https:/ /docs.learnbittensor.org/learn/chain-ratelimits#network-registration-rate-limit&gt;

reject\_proxy\_announcement(wallet, delegate\_ss 58 , call\_hash, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Rejects an announcement made by a proxy delegate.

This method allows the real account to reject an announcement made by a proxy delegate, preventing the announced call from being executed. Once rejected, the announcement cannot be executed and the announcement deposit is returned to the delegate.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor wallet object (should be the real account wallet).
- delegate\_ss58 (str) - The SS58 address of the delegate proxy account whose announcement is being rejected.
- call\_hash (str) - The hash of the call that was announced and is now being rejected.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the inclusion of the transaction.

- wait\_for\_finalization (bool) - Whether to wait for the finalization of the transaction.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

<!-- image -->

## Note

Once rejected, the announcement cannot be executed. The delegate's announcement deposit is returned.

remove\_liquidity(wallet, netuid, position\_id, hotkey\_ss 58 =None, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

[source] Remove liquidity and credit balances back to wallet's hotkey stake.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet used to sign the extrinsic (must be unlocked).
- netuid (int) - The UID of the target subnet for which the call is being initiated.
- position\_id (int) - The id of the position record in the pool.
- hotkey\_ss58 (Optional[str]) - The hotkey with staked TAO in Alpha. If not passed then the wallet hotkey is used.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block

within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the extrinsic to be included in a block.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

<!-- image -->

## Note

- Adding is allowed even when user liquidity is enabled in specified subnet. Call toggle\_user\_liquidity

## extrinsic to enable/disable user liquidity.

- To get the position\_id use get\_liquidity\_list method.

remove\_proxies(wallet, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Removes all proxy relationships for the account in a single transaction.

This method removes all proxy relationships for the signing account in a single call, which is more efficient than removing them one by one using remove\_proxy() . The deposit for all proxies will be returned to the account.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor wallet object. The account whose proxies will be removed (the delegator). All proxy relationships where wallet.coldkey.ss58\_address is the real account will be removed.

- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the inclusion of the transaction.
- wait\_for\_finalization (bool) - Whether to wait for the finalization of the transaction.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

<!-- image -->

## Note

This removes all proxy relationships for the account, regardless of proxy type or delegate. Use remove\_proxy() if you need to remove specific proxy relationships selectively.

remove\_proxy(wallet, delegate\_ss 58 , proxy\_type, delay, *, raise\_error=False, wait\_for\_inclusion=True, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Removes a specific proxy relationship.

This method removes a single proxy relationship between the real account and a delegate. The parameters must exactly match those used when the proxy was added via add\_proxy() . The deposit for this proxy will be returned to the account.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor wallet object.
- delegate\_ss58 (str) - The SS58 address of the delegate proxy account to remove.
- proxy\_type (Union[str, bittensor.core.chain\_data.ProxyType]) - The type of proxy permissions to remove. Can be a string or ProxyType enum value.
- delay (int) - The number of blocks before the proxy removal takes effect.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the inclusion of the transaction.
- wait\_for\_finalization (bool) - Whether to wait for the finalization of the transaction.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

<!-- image -->

## Note

The delegate\_ss58, proxy\_type, and delay parameters must exactly match those used when the proxy was added. Use get\_proxies\_for\_real\_account() to retrieve the exact parameters for existing proxies.

remove\_proxy\_announcement(wallet, real\_account\_ss 58 , call\_hash, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Removes an announcement made by a proxy account.

This method allows the proxy account to remove its own announcement before it is executed or rejected. This frees up the announcement deposit and prevents the call from being executed. Only the proxy account that made the announcement can remove it.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor wallet object (should be the proxy account wallet that made the announcement).
- real\_account\_ss58 (str) - The SS58 address of the real account on whose behalf the call was announced.
- call\_hash (str) - The hash of the call that was announced and is now being removed.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the inclusion of the transaction.
- wait\_for\_finalization (bool) - Whether to wait for the finalization of the transaction.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

## ExtrinsicResponse

<!-- image -->

## Note

Only the proxy account that made the announcement can remove it. The real account can reject it via reject\_proxy\_announcement() , but cannot remove it directly.

## reveal\_weights(wallet, netuid, uids, weights, salt, mechid=0,

max\_attempts=5, version\_key=version\_as\_int, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=16,

raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

[source] Reveals the weights for a specific subnet on the Bittensor blockchain using the provided wallet. This action serves as a revelation of the neuron's previously committed weight distribution.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor Wallet instance.
- netuid (int) - The unique identifier of the subnet.
- uids (bittensor.core.types.UIDs) - NumPy array of neuron UIDs for which weights are being revealed.
- weights (bittensor.core.types.Weights) - NumPy array of weight values corresponding to each UID.
- salt (bittensor.core.types.Salt) - NumPy array of salt values corresponding to the hash function.
- mechid (int) - The subnet mechanism unique identifier.
- max\_attempts (int) - The number of maximum attempts to reveal weights.
- version\_key (int) - Version key for compatibility with the network.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Waits for the transaction to be included in a block.
- wait\_for\_finalization (bool) - Waits for the transaction to be finalized on the blockchain.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

This function allows neurons to reveal their previously committed weight distribution, ensuring transparency and accountability within the Bittensor network.

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/glossary#commit-reveal&gt;
- Rate Limits: &lt;https:/ /docs.learnbittensor.org/learn/chain-ratelimits#weights-setting-rate-limit&gt;

root\_register(wallet, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

[source] Register neuron by recycling some TAO.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor wallet instance.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The

- transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Waits for the transaction to be included in a block.
- wait\_for\_finalization (bool) - Waits for the transaction to be finalized on the blockchain.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

<!-- image -->

## Notes

- Rate Limits: &lt;https:/ /docs.learnbittensor.org/learn/chain-ratelimits#registration-rate-limits&gt;

## root\_set\_pending\_childkey\_cooldown(wallet, cooldown, *,

mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Sets the pending childkey cooldown.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - bittensor wallet instance.
- cooldown (int) - the number of blocks to setting pending childkey cooldown.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The

[source]

- transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Waits for the transaction to be included in a block.
- wait\_for\_finalization (bool) - Waits for the transaction to be finalized on the blockchain.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

Note: This operation can only be successfully performed if your wallet has root privileges.

```
serve_axon(netuid, axon, certificate=None, *, mev_protection=DEFAULT_MEV_PROTECTION, period=DEFAULT_PERIOD,
```

raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

[source] Registers an Axon serving endpoint on the Bittensor network for a specific neuron.

This function is used to set up the Axon, a key component of a neuron that handles incoming queries and data processing tasks.

## Parameters:

- netuid (int) - The unique identifier of the subnetwork.
- axon (bittensor.core.axon.Axon) - The Axon instance to be registered for serving.

- certificate (Optional[bittensor.utils.Certificate]) - Certificate to use for TLS. If None, no TLS will be used.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Waits for the transaction to be included in a block.
- wait\_for\_finalization (bool) - Waits for the transaction to be finalized on the blockchain.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

## ExtrinsicResponse

By registering an Axon, the neuron becomes an active part of the network's distributed computing infrastructure, contributing to the collective intelligence of Bittensor.

<!-- image -->

## Notes

- Rate Limits: &lt;https:/ /docs.learnbittensor.org/learn/chain-ratelimits#serving-rate-limits&gt;

set\_auto\_stake(wallet, netuid, hotkey\_ss 58 , *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD,

raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Sets the coldkey to automatically stake to the hotkey within specific subnet mechanism.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor Wallet instance.
- netuid (int) - The subnet unique identifier.
- hotkey\_ss58 (str) - The SS58 address of the validator's hotkey to which the miner automatically stakes all rewards received from the specified subnet immediately upon receipt.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the inclusion of the transaction.
- wait\_for\_finalization (bool) - Whether to wait for the finalization of the transaction.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

<!-- image -->

Note

Use the get\_auto\_stakes method to get the hotkey address of the validator where auto stake is set.

set\_children(wallet, netuid, hotkey\_ss 58 , children, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True,

wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Allows a coldkey to set children-keys.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - bittensor wallet instance.
- hotkey\_ss58 (str) - The SS58 address of the neuron's hotkey.
- netuid (int) - The netuid value.
- children (list[tuple[float, str]]) - A list of children with their proportions.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Waits for the transaction to be included in a block.
- wait\_for\_finalization (bool) - Waits for the transaction to be finalized on the blockchain.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

<!-- image -->

## Notes

- Rate Limits: &lt;https:/ /docs.learnbittensor.org/learn/chain-ratelimits#child-hotkey-operations-rate-limit&gt;

[source]

set\_commitment(wallet, netuid, data, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Commits arbitrary data to the Bittensor network by publishing metadata.

This method allows neurons to publish arbitrary data to the blockchain, which can be used for various purposes such as sharing model updates, configuration data, or other network-relevant information.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet associated with the neuron committing the data.
- netuid (int) - The unique identifier of the subnetwork.
- data (str) - The data to be committed to the network.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the inclusion of the transaction.
- wait\_for\_finalization (bool) - Whether to wait for the finalization of the transaction.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

## Example:

```
# Commit some data to subnet 1 response = await subtensor.commit(wallet=my_wallet, netuid=1, data="Hell # Commit with custom period response = await subtensor.commit(wallet=my_wallet, netuid=1, data="Mode
```

Note: See &lt;https:/ /docs.learnbittensor.org/glossary#commit-reveal&gt;

```
set_delegate_take(wallet, hotkey_ss 58 , take, wait_for_inclusion=True, wait_for_finalization=True, raise_error=False, period=DEFAULT_PERIOD, wait_for_revealed_execution=True)
```

[source]

Sets the delegate 'take' percentage for a neuron identified by its hotkey. The 'take' represents the percentage of rewards that the delegate claims from its nominators' stakes.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - bittensor wallet instance.
- hotkey\_ss58 (str) - The SS58 address of the neuron's hotkey.
- take (float) - Percentage reward for the delegate.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Waits for the transaction to be included in a block.
- wait\_for\_finalization (bool) - Waits for the transaction to be finalized on the blockchain.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

## ExtrinsicResponse

## Raises:

- DelegateTakeTooHigh - Delegate take is too high.
- DelegateTakeTooLow - Delegate take is too low.
- DelegateTxRateLimitExceeded - A transactor exceeded the rate limit for delegate transaction.
- HotKeyAccountNotExists - The hotkey does not exist.
- NonAssociatedColdKey - Request to stake, unstake, or subscribe is made by a coldkey that is not associated with the hotkey account.
- bittensor\_wallet.errors.PasswordError - Decryption failed or wrong password for decryption provided.
- bittensor\_wallet.errors.KeyFileError - Failed to decode keyfile data.

The delegate take is a critical parameter in the network's incentive structure, influencing the distribution of rewards among neurons and their nominators.

## Notes

<!-- image -->

- Rate Limits: &lt;https:/ /docs.learnbittensor.org/learn/chain-ratelimits#delegate-take-rate-limit&gt;

set\_reveal\_commitment(wallet, netuid, data, blocks\_until\_reveal=360, block\_time=12, *,

mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True,

wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

[source] Commits arbitrary data to the Bittensor network by publishing metadata.

## Parameters:

- wallet - The wallet associated with the neuron committing the data.
- netuid (int) - The unique identifier of the subnetwork.
- data (str) - The data to be committed to the network.

- blocks\_until\_reveal (int) - The number of blocks from now after which the data will be revealed. Then number of blocks in one epoch.
- block\_time (Union[int, float]) - The number of seconds between each block.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the inclusion of the transaction.
- wait\_for\_finalization (bool) - Whether to wait for the finalization of the transaction.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

<!-- image -->

## Note

A commitment can be set once per subnet epoch and is reset at the next epoch in the chain automatically. Successful extrinsic's the 'data' field contains {'encrypted': encrypted, 'reveal\_round': reveal\_round}.

## set\_root\_claim\_type(wallet, new\_root\_claim\_type, *,

mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Submit an extrinsic to set the root claim type for the wallet's coldkey.

The root claim type determines how future Alpha dividends from subnets are handled when they are claimed for the wallet's coldkey:

- Swap: Alpha dividends are swapped to TAO at claim time and restaked on the Root Subnet (default).
- Keep: Alpha dividends remain as Alpha on the originating subnets.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor Wallet instance.
- new\_root\_claim\_type (Literal['Swap', 'Keep'] | RootClaimType | dict) - The new root claim type to set. Can be: - String: 'Swap' or 'Keep' - RootClaimType: RootClaimType.Swap, RootClaimType.Keep - Dict: {'KeepSubnets': {'subnets': [1, 2, 3]}} - Callable: RootClaimType.KeepSubnets([1, 2, 3])
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - Number of blocks for which the transaction remains valid after submission. If the extrinsic is not included in a block within this window, it will expire and be rejected.
- raise\_error (bool) - Whether to raise a Python exception instead of returning a failed ExtrinsicResponse.
- wait\_for\_inclusion (bool) - Whether to wait until the extrinsic is included in a block before returning.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic in a block before returning.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

ExtrinsicResponse describing the result of the extrinsic execution.

<!-- image -->

## Notes

- This setting applies to both automatic and manual root claims going forward; it does not retroactively change how already-claimed dividends were processed.
- Only the treatment of Alpha dividends is affected; the underlying TAO stake on the Root Subnet is unchanged.
- See: &lt;https:/ /docs.learnbittensor.org/staking-and-delegation/rootclaims&gt;
- See also: &lt;https:/ /docs.learnbittensor.org/staking-and-delegation/rootclaims/managing-root-claims&gt;

set\_subnet\_identity(wallet, netuid, subnet\_identity, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True,

wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Sets the identity of a subnet for a specific wallet and network.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet instance that will authorize the transaction.
- netuid (int) - The unique ID of the network on which the operation takes place.
- subnet\_identity (bittensor.core.chain\_data.SubnetIdentity) - The identity data of the subnet including attributes like name, GitHub repository, contact, URL, discord, description, and any additional metadata.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.

[source]

- wait\_for\_inclusion (bool) - Waits for the transaction to be included in a block.
- wait\_for\_finalization (bool) - Waits for the transaction to be finalized on the blockchain.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse set\_weights(wallet, netuid, uids, weights, mechid=0,

```
block_time=12.0, commit_reveal_version=4, max_attempts=5, version_key=version_as_int, *, mev_protection=DEFAULT_MEV_PROTECTION, period=DEFAULT_PERIOD, raise_error=False, wait_for_inclusion=True,
```

wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

[source] Sets the interneuronal weights for the specified neuron. This process involves specifying the influence or trust a neuron places on other neurons in the network, which is a fundamental aspect of Bittensor's decentralized learning architecture.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet associated with the subnet validator setting the weights.
- netuid (int) - The unique identifier of the subnet.
- uids (bittensor.core.types.UIDs) - The list of subnet miner neuron UIDs that the weights are being set for.
- weights (bittensor.core.types.Weights) - The corresponding weights to be set for each UID, representing the validator's evaluation of each miner's performance.
- mechid (int) - The subnet mechanism unique identifier.
- block\_time (float) - The number of seconds for block duration.
- commit\_reveal\_version (int) - The version of the chain commit-reveal protocol to use.

- max\_attempts (int) - The number of maximum attempts to set weights.
- version\_key (int) - Version key for compatibility with the network.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Waits for the transaction to be included in a block.
- wait\_for\_finalization (bool) - Waits for the transaction to be finalized on the blockchain.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

This function is crucial in shaping the network's collective intelligence, where each neuron's learning and contribution are influenced by the weights it sets towards others.

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/glossary#yuma-consensus&gt;
- Rate Limits: &lt;https:/ /docs.learnbittensor.org/learn/chain-ratelimits#weights-setting-rate-limit&gt;

## sign\_and\_send\_extrinsic(call, wallet, sign\_with='coldkey',

use\_nonce=False, nonce\_key='hotkey', nonce=None, *, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=False, calling\_function=None)

<!-- image -->

Helper method to sign and submit an extrinsic call to chain.

## Parameters:

- call (scalecodec.types.GenericCall) - A prepared Call object
- wallet (bittensor\_wallet.Wallet) - The wallet whose coldkey will be used to sign the extrinsic
- sign\_with (str) - The wallet's keypair to use for the signing. Options are 'coldkey', 'hotkey', 'coldkeypub'
- use\_nonce (bool) - Unique identifier for the transaction related with hot/coldkey.
- nonce\_key (str) - The type on nonce to use. Options are 'hotkey' or 'coldkey'.
- nonce (Optional[int]) - The nonce to use for the transaction. If not provided, it will be fetched from the chain.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises the relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait until the extrinsic call is included on the chain
- wait\_for\_finalization (bool) - Whether to wait until the extrinsic call is finalized on the chain
- calling\_function (Optional[str]) - The name of the calling function.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

## Raises:

SubstrateRequestException - Substrate request exception.

sim\_swap(origin\_netuid, destination\_netuid, amount, block=None)

Simulates a swap/stake operation and calculates the fees and resulting amounts.

This method queries the SimSwap Runtime API to calculate the swap fees (in Alpha or TAO) and the quantities of Alpha or TAO tokens expected as output from the transaction. This simulation does NOT include the blockchain extrinsic transaction fee (the fee to submit the transaction itself).

When moving stake between subnets, the operation may involve swapping Alpha (subnet-specific stake token) to TAO (the base network token), then TAO to Alpha on the destination subnet. For subnet 0 (root network), all stake is in TAO.

## Parameters:

- origin\_netuid (int) - Netuid of the source subnet (0 if adding stake).
- destination\_netuid (int) - Netuid of the destination subnet.
- amount (bittensor.utils.balance.Balance) - Amount to swap/stake as a Balance object. Use Balance.from\_tao(…) or Balance.from\_rao(…) to create the amount.
- block (Optional[int]) - The block number to query. If None, uses the current chain head.

## Returns:

Object containing alpha\_fee, tao\_fee, alpha\_amount, and tao\_amount fields representing the swap fees and output amounts.

## Return type:

SimSwapResult

## Example:

```
# Simulate staking 100 TAO stake to subnet 1 result = subtensor.sim_swap( origin_netuid=0, destination_netuid=1, amount=Balance.from_tao(100) ) print(f"Fee: {result.tao_fee.tao} TAO, Output: {result.alpha_amount} Alp
```

## Notes 

<!-- image -->

- Alpha : Subnet-specific stake token (dynamic TAO)
- TAO : Base network token; subnet 0 uses TAO directly
- The returned fees do NOT include the extrinsic transaction fee
- Transaction Fees: &lt;https:/ /docs.learnbittensor.org/learn/fees&gt;
- Glossary: &lt;https:/ /docs.learnbittensor.org/glossary&gt;

## start\_call(wallet, netuid, *,

mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=False, wait\_for\_revealed\_execution=True)

[source] Submits a start\_call extrinsic to the blockchain, to trigger the start call process for a subnet (used to start a new subnet's emission mechanism).

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet used to sign the extrinsic (must be unlocked).
- netuid (int) - The UID of the target subnet for which the call is being initiated.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the inclusion of the transaction.
- wait\_for\_finalization (bool) - Whether to wait for the finalization of the transaction.

- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

## state\_call(method, data, block=None)

[source]

Makes a state call to the Bittensor blockchain, allowing for direct queries of the blockchain's state. This function is typically used for advanced, nonstandard queries not provided by other getter methods.

Use this method when you need to query runtime APIs or storage functions that don't have dedicated wrapper methods in the SDK. For standard queries, prefer the specific getter methods (e.g., get\_balance, get\_stake) which provide better type safety and error handling.

## Parameters:

- method (str) - The runtime API method name (e.g., 'SubnetInfoRuntimeApi', 'get\_metagraph').
- data (str) - Hex-encoded string of the SCALE-encoded parameters to pass to the method.
- block (Optional[int]) - The block number to query. If None, queries the current chain head.

## Returns:

The result of the rpc call.

## Return type:

dict[Any, Any]

## subnet(netuid, block=None)

Retrieves the subnet information for a single subnet in the network.

## Parameters:

- netuid (int) - The unique identifier of the subnet.

[source]

- block (Optional[int]) - The block number to query the subnet information from.

## Returns:

A DynamicInfo object, containing detailed information about a subnet.

## Return type:

Optional[bittensor.core.chain\_data.DynamicInfo]

## subnet\_exists(netuid, block=None)

[source]

Checks if a subnet with the specified unique identifier (netuid) exists within the Bittensor network.

## Parameters:

- netuid (int) - The unique identifier of the subnet.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

True if the subnet exists, False otherwise.

## Return type:

bool

This function is critical for verifying the presence of specific subnets in the network, enabling a deeper understanding of the network's structure and composition.

## subnetwork\_n(netuid, block=None)

Returns the current number of registered neurons (UIDs) in a subnet.

## Parameters:

- netuid (int) - The unique identifier of the subnetwork.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

The current number of registered neurons in the subnet, or None if the subnetwork does not exist.

## Return type:

Optional[int]

[source]

## substrate

swap\_stake(wallet, hotkey\_ss 58 , origin\_netuid, destination\_netuid, amount, safe\_swapping=False, allow\_partial\_stake=False, rate\_tolerance=0.005, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

[source] Moves stake between subnets while keeping the same coldkey-hotkey pair ownership. Like subnet hopping - same owner, same hotkey, just changing which subnet the stake is in.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet to swap stake from.
- hotkey\_ss58 (str) - The SS58 address of the hotkey whose stake is being swapped.
- origin\_netuid (int) - The netuid from which stake is removed.
- destination\_netuid (int) - The netuid to which stake is added.
- amount (bittensor.utils.balance.Balance) - The amount to swap.
- safe\_swapping (bool) - If True, enables price safety checks to protect against fluctuating prices. The swap will only execute if the price ratio between subnets doesn't exceed the rate tolerance.
- allow\_partial\_stake (bool) - If True and safe\_staking is enabled, allows partial stake swaps when the full amount would exceed the price tolerance. If false, the entire swap fails if it would exceed the tolerance.
- rate\_tolerance (float) - The maximum allowed increase in the price ratio between subnets (origin\_price/destination\_price). For example, 0.005 = 0.5% maximum increase. Only used when safe\_staking is True.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block

within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the inclusion of the transaction.
- wait\_for\_finalization (bool) - Whether to wait for the finalization of the transaction.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

<!-- image -->

## Notes

The price ratio for swap\_stake in safe mode is calculated as: origin\_subnet\_price / destination\_subnet\_price. When safe\_swapping is enabled, the swap will only execute if: - With allow\_partial\_stake=False: The entire swap amount can be executed without the price ratio increasing more than rate\_tolerance.

- With allow\_partial\_stake=True: A partial amount will be swapped up to the point where the price ratio would increase by rate\_tolerance.
- Price Protection: &lt;https:/ /docs.learnbittensor.org/learn/priceprotection&gt;
- Rate Limits: &lt;https:/ /docs.learnbittensor.org/learn/chain-ratelimits#staking-operations-rate-limits&gt;

## tempo(netuid, block=None)

Returns the Tempo hyperparameter for a subnet.

Tempo determines the length of an epoch in blocks. It defines how frequently the subnet's consensus mechanism runs, calculating emissions and updating rankings. A

[source]

tempo of 360 blocks equals approximately 72 minutes (360 blocks × 12 seconds per block).

## Parameters:

- netuid (int) - The unique identifier of the subnetwork.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

The tempo value in blocks, or None if the subnetwork does not exist.

## Return type:

Optional[int]

<!-- image -->

## Notes

- &lt;https:/ /docs.learnbittensor.org/resources/glossary#tempo&gt;
- &lt;https:/ /docs.learnbittensor.org/resources/glossary#epoch&gt;

## toggle\_user\_liquidity(wallet, netuid, enable, *,

mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Allow to toggle user liquidity for specified subnet.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet used to sign the extrinsic (must be unlocked).
- netuid (int) - The UID of the target subnet for which the call is being initiated.
- enable (bool) - Boolean indicating whether to enable user liquidity.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

[source]

- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the extrinsic to be included in a block.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

Note: The call can be executed successfully by the subnet owner only.

transfer(wallet, destination\_ss 58 , amount, transfer\_all=False, keep\_alive=True, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=False, wait\_for\_revealed\_execution=True)

Transfer token of amount to destination.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Source wallet for the transfer.
- destination\_ss58 (str) - Destination address for the transfer.
- amount (Optional[bittensor.utils.balance.Balance]) - Number of tokens to transfer. None is transferring all.
- transfer\_all (bool) - Flag to transfer all tokens.
- keep\_alive (bool) - Flag to keep the connection alive.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block

[source]

- within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the extrinsic to be included in a block.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse transfer\_stake(wallet, destination\_coldkey\_ss 58 , hotkey\_ss 58 , origin\_netuid, destination\_netuid, amount, *,

mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

[source] Transfers stake from one subnet to another while changing the coldkey owner.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet to transfer stake from.
- destination\_coldkey\_ss58 (str) - The destination coldkey SS58 address.
- hotkey\_ss58 (str) - The hotkey SS58 address associated with the stake.
- origin\_netuid (int) - The source subnet UID.
- destination\_netuid (int) - The destination subnet UID.
- amount (bittensor.utils.balance.Balance) - Amount to transfer.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the extrinsic to be included in a block.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

<!-- image -->

## Notes

- Price Protection: &lt;https:/ /docs.learnbittensor.org/learn/priceprotection&gt;
- Rate Limits: &lt;https:/ /docs.learnbittensor.org/learn/chain-ratelimits#staking-operations-rate-limits&gt;

## tx\_rate\_limit(block=None)

## [source]

Retrieves the transaction rate limit for the Bittensor network as of a specific blockchain block. This rate limit sets the maximum number of transactions that can be processed within a given time frame.

## Parameters:

block (Optional[int]) - The blockchain block number for the query.

## Returns:

The transaction rate limit of the network, None if not available.

## Return type:

Optional[int]

## The transaction rate limit is an essential parameter for ensuring the stability and scalability of the Bittensor

network. It helps in managing network load and preventing congestion, thereby maintaining efficient and timely transaction processing.

unstake(wallet, netuid, hotkey\_ss 58 , amount, allow\_partial\_stake=False, rate\_tolerance=0.005, safe\_unstaking=False, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

[source] Removes a specified amount of stake from a single hotkey account. This function is critical for adjusting individual neuron stakes within the Bittensor network.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet associated with the neuron from which the stake is being removed.
- netuid (int) - The unique identifier of the subnet.
- hotkey\_ss58 (str) - The SS58 address of the hotkey account to unstake from.
- amount (bittensor.utils.balance.Balance) - The amount of alpha to unstake. If not specified, unstakes all. Alpha amount.
- allow\_partial\_stake (bool) - If True and safe\_staking is enabled, allows partial unstaking when the full amount would exceed the price tolerance. If false, the entire unstake fails if it would exceed the tolerance.
- rate\_tolerance (float) - The maximum allowed price change ratio when unstaking. For example, 0.005 = 0.5% maximum price decrease. Only used when safe\_staking is True.
- safe\_unstaking (bool) - If True, enables price safety checks to protect against fluctuating prices. The unstake will only execute if the price change doesn't exceed the rate tolerance.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the extrinsic to be included in a block.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

This function supports flexible stake management, allowing neurons to adjust their network participation and potential reward accruals. When safe\_staking is enabled, it provides protection against price fluctuations during the time unstake is executed and the time it is actually processed by the chain.

<!-- image -->

## Notes

- Price Protection: &lt;https:/ /docs.learnbittensor.org/learn/priceprotection&gt;
- Rate Limits: &lt;https:/ /docs.learnbittensor.org/learn/chain-ratelimits#staking-operations-rate-limits&gt;

unstake\_all(wallet, netuid, hotkey\_ss 58 , rate\_tolerance=0.005, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

[source] Unstakes all TAO/Alpha associated with a hotkey from the specified subnets on the Bittensor network.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet of the stake owner.
- netuid (int) - The unique identifier of the subnet.
- hotkey\_ss58 (str) - The SS58 address of the hotkey to unstake from.
- rate\_tolerance (Optional[float]) - The maximum allowed price change ratio when unstaking. For example, 0.005 = 0.5% maximum price decrease. If not passed (None), then unstaking goes without price limit.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.
- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the extrinsic to be included in a block.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

## Example:

```
# If you would like to unstake all stakes in all subnets safely: import bittensor as bt subtensor = bt.Subtensor() wallet = bt.Wallet("my_wallet") netuid = 14 hotkey = "5%SOME_HOTKEY%" wallet_stakes = subtensor.get_stake_info_for_coldkey(coldkey_ss58=wallet for stake in wallet_stakes: result = subtensor.unstake_all( wallet=wallet, hotkey_ss58=stake.hotkey_ss58, netuid=stake.netuid, ) print(result) # If you would like to unstake all stakes in all subnets unsafely, use r import bittensor as bt subtensor = bt.Subtensor() wallet = bt.Wallet("my_wallet") netuid = 14 hotkey = "5%SOME_HOTKEY_WHERE_IS_YOUR_STAKE_NOW%" wallet_stakes = subtensor.get_stake_info_for_coldkey(coldkey_ss58=wallet for stake in wallet_stakes: result = subtensor.unstake_all( wallet=wallet, hotkey_ss58=stake.hotkey_ss58, netuid=stake.netuid, rate_tolerance=None, )
```

print(result)

<!-- image -->

## Notes

- Price Protection: &lt;https:/ /docs.learnbittensor.org/learn/priceprotection&gt;
- Rate Limits: &lt;https:/ /docs.learnbittensor.org/learn/chain-ratelimits#staking-operations-rate-limits&gt;

unstake\_multiple(wallet, netuids, hotkey\_ss 58 s, amounts=None, unstake\_all=False, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

[source] Performs batch unstaking from multiple hotkey accounts, allowing a neuron to reduce its staked amounts efficiently. This function is useful for managing the distribution of stakes across multiple neurons.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - The wallet linked to the coldkey from which the stakes are being withdrawn.
- netuids (bittensor.core.types.UIDs) - Subnets unique IDs.
- hotkey\_ss58s (list[str]) - A list of hotkey SS58 addresses to unstake from.
- amounts (Optional[list[bittensor.utils.balance.Balance]]) - The amounts of TAO to unstake from each hotkey. If not provided, unstakes all.
- unstake\_all (bool) - If True, unstakes all tokens. Amounts are ignored.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after it's submitted. If the transaction is not included in a block

within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

- raise\_error (bool) - Raises a relevant exception rather than returning False if unsuccessful.
- wait\_for\_inclusion (bool) - Whether to wait for the extrinsic to be included in a block.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

The result object of the extrinsic execution.

## Return type:

ExtrinsicResponse

This function allows for strategic reallocation or withdrawal of stakes, aligning with the dynamic stake management aspect of the Bittensor network.

<!-- image -->

## Notes

- Price Protection: &lt;https:/ /docs.learnbittensor.org/learn/priceprotection&gt;
- Rate Limits: &lt;https:/ /docs.learnbittensor.org/learn/chain-ratelimits#staking-operations-rate-limits&gt;

## update\_cap\_crowdloan(wallet, crowdloan\_id, new\_cap, *,

mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Updates the fundraising cap of an active (non-finalized) crowdloan.

Allows the creator to adjust the maximum total contribution amount before finalization. The new cap must be at least equal to the amount already raised. This is useful for adjusting campaign goals based on contributor feedback or changing subnet costs.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor wallet instance used to sign the transaction (must be the creator's coldkey).
- crowdloan\_id (int) - The unique identifier of the crowdloan to update.
- new\_cap (bittensor.utils.balance.Balance) - The new fundraising cap (TAO). Must be &gt;= raised.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after submission.
- raise\_error (bool) - If True, raises an exception rather than returning failure in the response.
- wait\_for\_inclusion (bool) - Whether to wait for the extrinsic to be included in a block.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

ExtrinsicResponse indicating success or failure, with error details if applicable.

## Return type:

bittensor.core.types.ExtrinsicResponse

<!-- image -->

## Notes

- Only the creator can update the cap.
- The crowdloan must not be finalized.
- The new cap must be &gt;= the total funds already raised.
- Crowdloans Overview: &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans&gt;
- Update Parameters:

&lt;https:/ /docs.learnbittensor.org/subnets/crowdloans#crowdloanlifecycle&gt;

update\_end\_crowdloan(wallet, crowdloan\_id, new\_end, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Updates the end block of an active (non-finalized) crowdloan.

Allows the creator to extend (or shorten) the contribution period before finalization. The new end block must be in the future and respect the minimum and maximum duration bounds defined in the runtime constants. This is useful for extending campaigns that need more time to reach their cap or shortening campaigns with sufficient contributions.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor wallet instance used to sign the transaction (must be the creator's coldkey).
- crowdloan\_id (int) - The unique identifier of the crowdloan to update.
- new\_end (int) - The new block number at which the crowdloan will end. Must be between MinimumBlockDuration (7 days = 50,400 blocks) and MaximumBlockDuration (60 days = 432,000 blocks) from the current block.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after submission.
- raise\_error (bool) - If True, raises an exception rather than returning failure in the response.
- wait\_for\_inclusion (bool) - Whether to wait for the extrinsic to be included in a block.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

ExtrinsicResponse indicating success or failure, with error details if applicable.

## Return type:

<!-- image -->

## bittensor.core.types.ExtrinsicResponse

## Notes

- Only the creator can update the end block.
- The crowdloan must not be finalized.
- The new end block must respect duration bounds (MinimumBlockDuration to MaximumBlockDuration).
- Crowdloans Overview: &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans&gt;
- Update Parameters:
- &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans#crowdloanlifecycle&gt;

## update\_min\_contribution\_crowdloan(wallet, crowdloan\_id,

new\_min\_contribution, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True, wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Updates the minimum contribution amount of an active (non-finalized) crowdloan.

Allows the creator to adjust the minimum per-contribution amount before finalization. The new value must meet or exceed the AbsoluteMinimumContribution constant. This is useful for adjusting contribution requirements based on the number of expected contributors or campaign strategy.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor wallet instance used to sign the transaction (must be the creator's coldkey).
- crowdloan\_id (int) - The unique identifier of the crowdloan to update.
- new\_min\_contribution (bittensor.utils.balance.Balance) - The new minimum contribution amount (TAO). Must be &gt;= AbsoluteMinimumContribution.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

- period (Optional[int]) - The number of blocks during which the transaction will remain valid after submission.
- raise\_error (bool) - If True, raises an exception rather than returning failure in the response.
- wait\_for\_inclusion (bool) - Whether to wait for the extrinsic to be included in a block.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

ExtrinsicResponse indicating success or failure, with error details if applicable.

## Return type:

bittensor.core.types.ExtrinsicResponse

<!-- image -->

## Notes

- Only the creator can update the minimum contribution.
- The crowdloan must not be finalized.
- The new minimum must be &gt;= AbsoluteMinimumContribution (check via get\_crowdloan\_constants).
- Crowdloans Overview: &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans&gt;
- Update Parameters:
- &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans#crowdloanlifecycle&gt;

## validate\_extrinsic\_params(call\_module, call\_function,

call\_params, block=None)

Validate and filter extrinsic parameters against on-chain metadata.

This method checks that the provided parameters match the expected signature of the given extrinsic (module and function) as defined in the Substrate metadata. It raises explicit errors for missing or invalid parameters and silently ignores any extra keys not present in the function definition.

## Parameters:

- call\_module (str) - The pallet name, e.g. 'SubtensorModule' or 'AdminUtils'.
- call\_function (str) - The extrinsic function name, e.g. 'set\_weights' or 'sudo\_set\_tempo'.
- call\_params (dict[str, Any]) - A dictionary of parameters to validate.
- block (Optional[int]) - Optional block number to query metadata from. If not provided, the latest metadata is used.

## Returns:

A filtered dictionary containing only the parameters that are valid for the specified extrinsic.

## Raises:

- ValueError - If the given module or function is not found in the chain metadata.
- KeyError - If one or more required parameters are missing.

## Notes 

<!-- image -->

This method does not compose or submit the extrinsic. It only ensures that call\_params conforms to the expected schema derived from on-chain metadata.

## wait\_for\_block(block=None)

[source]

Waits until a specific block is reached on the chain. If no block is specified, waits for the next block.

## Parameters:

block (Optional[int]) - The block number to wait for. If None, waits for the next block.

## Returns:

True if the target block was reached, False if timeout occurred.

## Example:

```
# Waits for a specific block subtensor.wait_for_block(block=1234)
```

## weights(netuid, mechid=0, block=None)

## [source]

Retrieves the weight distribution set by neurons within a specific subnet of the Bittensor network. This function maps each neuron's UID to the weights it assigns to other neurons, reflecting the network's trust and value assignment mechanisms.

## Parameters:

- netuid (int) - The network UID of the subnet to query.
- mechid (int) - Subnet mechanism identifier.
- block (Optional[int]) - Block number for synchronization, or None for the latest block.

## Returns:

A list of tuples mapping each neuron's UID to its assigned weights.

## Return type:

list[tuple[int, list[tuple[int, int]]]]

The weight distribution is a key factor in the network's consensus algorithm and the ranking of neurons, influencing their influence and reward allocation within the subnet.

## weights\_rate\_limit(netuid, block=None)

Returns the WeightsSetRateLimit hyperparameter for a subnet.

This hyperparameter limits how many times a validator can set weights per epoch. It prevents validators from spamming weight updates and ensures stable consensus calculations. Once the limit is reached, validators must wait until the next epoch to set weights again.

## Parameters:

- netuid (int) - The unique identifier of the subnetwork.
- block (Optional[int]) - The blockchain block number for the query.

## Returns:

The maximum number of weight set operations allowed per epoch, or

Noneif the subnetwork does not

exist or the parameter is not found.

## Return type:

Optional[int]

[source]

withdraw\_crowdloan(wallet, crowdloan\_id, *, mev\_protection=DEFAULT\_MEV\_PROTECTION, period=DEFAULT\_PERIOD, raise\_error=False, wait\_for\_inclusion=True,

wait\_for\_finalization=True, wait\_for\_revealed\_execution=True)

Withdraws a contribution from an active (not yet finalized or dissolved) crowdloan.

Contributors can withdraw their contributions at any time before finalization. For regular contributors, the full contribution amount is returned. For the creator, only amounts exceeding the initial deposit can be withdrawn; the deposit itself remains locked until dissolution.

## Parameters:

- wallet (bittensor\_wallet.Wallet) - Bittensor wallet instance used to sign the transaction (coldkey must match a contributor).
- crowdloan\_id (int) - The unique identifier of the crowdloan to withdraw from.
- mev\_protection (bool) - If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.
- period (Optional[int]) - The number of blocks during which the transaction will remain valid after submission, after which it will be rejected.
- raise\_error (bool) - If True, raises an exception rather than returning False in the response, in case the transaction fails.
- wait\_for\_inclusion (bool) - Whether to wait for the extrinsic to be included in a block.
- wait\_for\_finalization (bool) - Whether to wait for finalization of the extrinsic.
- wait\_for\_revealed\_execution (bool) - Whether to wait for the revealed execution of transaction if mev\_protection used.

## Returns:

ExtrinsicResponse indicating success or failure, with error details if applicable.

## Return type:

bittensor.core.types.ExtrinsicResponse

<!-- image -->

## Notes

- Crowdloans Overview: &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans&gt;
- Crowdloan Lifecycle:
- &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans#crowdloanlifecycle&gt;
- Withdraw: &lt;https:/ /docs.learnbittensor.org/subnets/crowdloans/crowdloans-
- tutorial#optional-withdraw&gt;