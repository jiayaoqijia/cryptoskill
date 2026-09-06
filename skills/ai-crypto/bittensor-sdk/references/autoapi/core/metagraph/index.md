# bittensor.core.metagraph &#8212; Bittensor SDK Docs  documentation

[Skip to main content](<#main-content>)

__Back to top __ `Ctrl`+`K`

[ ![Bittensor SDK Docs  documentation - Home](../../../../_static/logo.svg) ![Bittensor SDK Docs  documentation - Home](../../../../_static/logo-dark-mode.svg) ](<../../../../index.html>)

__ Search `Ctrl`+`K`

Table of Contents

  * [API Reference](<../../../index.html>) __
    * [bittensor](<../../index.html>) __
      * [bittensor.core](<../index.html>) __
        * [bittensor.core.async_subtensor](<../async_subtensor/index.html>)
        * [bittensor.core.axon](<../axon/index.html>)
        * [bittensor.core.chain_data](<../chain_data/index.html>)
        * [bittensor.core.config](<../config/index.html>)
        * [bittensor.core.dendrite](<../dendrite/index.html>)
        * [bittensor.core.errors](<../errors/index.html>)
        * [bittensor.core.extrinsics](<../extrinsics/index.html>)
        * [bittensor.core.metagraph](<#>)
        * [bittensor.core.settings](<../settings/index.html>)
        * [bittensor.core.stream](<../stream/index.html>)
        * [bittensor.core.subtensor](<../subtensor/index.html>)
        * [bittensor.core.synapse](<../synapse/index.html>)
        * [bittensor.core.tensor](<../tensor/index.html>)
        * [bittensor.core.threadpool](<../threadpool/index.html>)
        * [bittensor.core.types](<../types/index.html>)
      * [bittensor.extras](<../../extras/index.html>) __
        * [bittensor.extras.dev_framework](<../../extras/dev_framework/index.html>)
        * [bittensor.extras.subtensor_api](<../../extras/subtensor_api/index.html>)
        * [bittensor.extras.timelock](<../../extras/timelock/index.html>)
      * [bittensor.utils](<../../utils/index.html>) __
        * [bittensor.utils.axon_utils](<../../utils/axon_utils/index.html>)
        * [bittensor.utils.balance](<../../utils/balance/index.html>)
        * [bittensor.utils.btlogging](<../../utils/btlogging/index.html>)
        * [bittensor.utils.easy_imports](<../../utils/easy_imports/index.html>)
        * [bittensor.utils.formatting](<../../utils/formatting/index.html>)
        * [bittensor.utils.liquidity](<../../utils/liquidity/index.html>)
        * [bittensor.utils.networking](<../../utils/networking/index.html>)
        * [bittensor.utils.registration](<../../utils/registration/index.html>)
        * [bittensor.utils.subnets](<../../utils/subnets/index.html>)
        * [bittensor.utils.version](<../../utils/version/index.html>)
        * [bittensor.utils.weight_utils](<../../utils/weight_utils/index.html>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/metagraph/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/metagraph/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/core/metagraph/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.metagraph

##  Contents 

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`AsyncMetagraph`](<#bittensor.core.metagraph.AsyncMetagraph>)
      * [`AsyncMetagraph.sync()`](<#bittensor.core.metagraph.AsyncMetagraph.sync>)
    * [`BaseClass`](<#bittensor.core.metagraph.BaseClass>)
    * [`METAGRAPH_STATE_DICT_NDARRAY_KEYS`](<#bittensor.core.metagraph.METAGRAPH_STATE_DICT_NDARRAY_KEYS>)
    * [`Metagraph`](<#bittensor.core.metagraph.Metagraph>)
      * [`Metagraph.sync()`](<#bittensor.core.metagraph.Metagraph.sync>)
    * [`MetagraphMixin`](<#bittensor.core.metagraph.MetagraphMixin>)
      * [`MetagraphMixin.AS`](<#bittensor.core.metagraph.MetagraphMixin.AS>)
      * [`MetagraphMixin.B`](<#bittensor.core.metagraph.MetagraphMixin.B>)
      * [`MetagraphMixin.C`](<#bittensor.core.metagraph.MetagraphMixin.C>)
      * [`MetagraphMixin.D`](<#bittensor.core.metagraph.MetagraphMixin.D>)
      * [`MetagraphMixin.E`](<#bittensor.core.metagraph.MetagraphMixin.E>)
      * [`MetagraphMixin.I`](<#bittensor.core.metagraph.MetagraphMixin.I>)
      * [`MetagraphMixin.S`](<#bittensor.core.metagraph.MetagraphMixin.S>)
      * [`MetagraphMixin.TS`](<#bittensor.core.metagraph.MetagraphMixin.TS>)
      * [`MetagraphMixin.Tv`](<#bittensor.core.metagraph.MetagraphMixin.Tv>)
      * [`MetagraphMixin.W`](<#bittensor.core.metagraph.MetagraphMixin.W>)
      * [`MetagraphMixin.active`](<#bittensor.core.metagraph.MetagraphMixin.active>)
      * [`MetagraphMixin.addresses`](<#bittensor.core.metagraph.MetagraphMixin.addresses>)
      * [`MetagraphMixin.alpha_dividends_per_hotkey`](<#bittensor.core.metagraph.MetagraphMixin.alpha_dividends_per_hotkey>)
      * [`MetagraphMixin.alpha_stake`](<#bittensor.core.metagraph.MetagraphMixin.alpha_stake>)
      * [`MetagraphMixin.axons`](<#bittensor.core.metagraph.MetagraphMixin.axons>)
      * [`MetagraphMixin.block`](<#bittensor.core.metagraph.MetagraphMixin.block>)
      * [`MetagraphMixin.block_at_registration`](<#bittensor.core.metagraph.MetagraphMixin.block_at_registration>)
      * [`MetagraphMixin.blocks_since_last_step`](<#bittensor.core.metagraph.MetagraphMixin.blocks_since_last_step>)
      * [`MetagraphMixin.bonds`](<#bittensor.core.metagraph.MetagraphMixin.bonds>)
      * [`MetagraphMixin.chain_endpoint`](<#bittensor.core.metagraph.MetagraphMixin.chain_endpoint>)
      * [`MetagraphMixin.coldkeys`](<#bittensor.core.metagraph.MetagraphMixin.coldkeys>)
      * [`MetagraphMixin.consensus`](<#bittensor.core.metagraph.MetagraphMixin.consensus>)
      * [`MetagraphMixin.dividends`](<#bittensor.core.metagraph.MetagraphMixin.dividends>)
      * [`MetagraphMixin.emission`](<#bittensor.core.metagraph.MetagraphMixin.emission>)
      * [`MetagraphMixin.emissions`](<#bittensor.core.metagraph.MetagraphMixin.emissions>)
      * [`MetagraphMixin.hotkeys`](<#bittensor.core.metagraph.MetagraphMixin.hotkeys>)
      * [`MetagraphMixin.hparams`](<#bittensor.core.metagraph.MetagraphMixin.hparams>)
      * [`MetagraphMixin.identities`](<#bittensor.core.metagraph.MetagraphMixin.identities>)
      * [`MetagraphMixin.identity`](<#bittensor.core.metagraph.MetagraphMixin.identity>)
      * [`MetagraphMixin.incentive`](<#bittensor.core.metagraph.MetagraphMixin.incentive>)
      * [`MetagraphMixin.last_step`](<#bittensor.core.metagraph.MetagraphMixin.last_step>)
      * [`MetagraphMixin.last_update`](<#bittensor.core.metagraph.MetagraphMixin.last_update>)
      * [`MetagraphMixin.lite`](<#bittensor.core.metagraph.MetagraphMixin.lite>)
      * [`MetagraphMixin.load()`](<#bittensor.core.metagraph.MetagraphMixin.load>)
      * [`MetagraphMixin.load_from_path()`](<#bittensor.core.metagraph.MetagraphMixin.load_from_path>)
      * [`MetagraphMixin.max_uids`](<#bittensor.core.metagraph.MetagraphMixin.max_uids>)
      * [`MetagraphMixin.mechanism_count`](<#bittensor.core.metagraph.MetagraphMixin.mechanism_count>)
      * [`MetagraphMixin.mechanisms_emissions_split`](<#bittensor.core.metagraph.MetagraphMixin.mechanisms_emissions_split>)
      * [`MetagraphMixin.mechid`](<#bittensor.core.metagraph.MetagraphMixin.mechid>)
      * [`MetagraphMixin.metadata()`](<#bittensor.core.metagraph.MetagraphMixin.metadata>)
      * [`MetagraphMixin.n`](<#bittensor.core.metagraph.MetagraphMixin.n>)
      * [`MetagraphMixin.name`](<#bittensor.core.metagraph.MetagraphMixin.name>)
      * [`MetagraphMixin.netuid`](<#bittensor.core.metagraph.MetagraphMixin.netuid>)
      * [`MetagraphMixin.network`](<#bittensor.core.metagraph.MetagraphMixin.network>)
      * [`MetagraphMixin.network_registered_at`](<#bittensor.core.metagraph.MetagraphMixin.network_registered_at>)
      * [`MetagraphMixin.neurons`](<#bittensor.core.metagraph.MetagraphMixin.neurons>)
      * [`MetagraphMixin.num_uids`](<#bittensor.core.metagraph.MetagraphMixin.num_uids>)
      * [`MetagraphMixin.owner_coldkey`](<#bittensor.core.metagraph.MetagraphMixin.owner_coldkey>)
      * [`MetagraphMixin.owner_hotkey`](<#bittensor.core.metagraph.MetagraphMixin.owner_hotkey>)
      * [`MetagraphMixin.pool`](<#bittensor.core.metagraph.MetagraphMixin.pool>)
      * [`MetagraphMixin.pruning_score`](<#bittensor.core.metagraph.MetagraphMixin.pruning_score>)
      * [`MetagraphMixin.ranks`](<#bittensor.core.metagraph.MetagraphMixin.ranks>)
      * [`MetagraphMixin.save()`](<#bittensor.core.metagraph.MetagraphMixin.save>)
      * [`MetagraphMixin.should_sync`](<#bittensor.core.metagraph.MetagraphMixin.should_sync>)
      * [`MetagraphMixin.stake`](<#bittensor.core.metagraph.MetagraphMixin.stake>)
      * [`MetagraphMixin.state_dict()`](<#bittensor.core.metagraph.MetagraphMixin.state_dict>)
      * [`MetagraphMixin.subtensor`](<#bittensor.core.metagraph.MetagraphMixin.subtensor>)
      * [`MetagraphMixin.symbol`](<#bittensor.core.metagraph.MetagraphMixin.symbol>)
      * [`MetagraphMixin.tao_dividends_per_hotkey`](<#bittensor.core.metagraph.MetagraphMixin.tao_dividends_per_hotkey>)
      * [`MetagraphMixin.tao_stake`](<#bittensor.core.metagraph.MetagraphMixin.tao_stake>)
      * [`MetagraphMixin.tempo`](<#bittensor.core.metagraph.MetagraphMixin.tempo>)
      * [`MetagraphMixin.trust`](<#bittensor.core.metagraph.MetagraphMixin.trust>)
      * [`MetagraphMixin.uids`](<#bittensor.core.metagraph.MetagraphMixin.uids>)
      * [`MetagraphMixin.validator_permit`](<#bittensor.core.metagraph.MetagraphMixin.validator_permit>)
      * [`MetagraphMixin.validator_trust`](<#bittensor.core.metagraph.MetagraphMixin.validator_trust>)
      * [`MetagraphMixin.version`](<#bittensor.core.metagraph.MetagraphMixin.version>)
      * [`MetagraphMixin.weights`](<#bittensor.core.metagraph.MetagraphMixin.weights>)
    * [`NonTorchMetagraph`](<#bittensor.core.metagraph.NonTorchMetagraph>)
      * [`NonTorchMetagraph.active`](<#bittensor.core.metagraph.NonTorchMetagraph.active>)
      * [`NonTorchMetagraph.alpha_stake`](<#bittensor.core.metagraph.NonTorchMetagraph.alpha_stake>)
      * [`NonTorchMetagraph.block`](<#bittensor.core.metagraph.NonTorchMetagraph.block>)
      * [`NonTorchMetagraph.bonds`](<#bittensor.core.metagraph.NonTorchMetagraph.bonds>)
      * [`NonTorchMetagraph.consensus`](<#bittensor.core.metagraph.NonTorchMetagraph.consensus>)
      * [`NonTorchMetagraph.dividends`](<#bittensor.core.metagraph.NonTorchMetagraph.dividends>)
      * [`NonTorchMetagraph.emission`](<#bittensor.core.metagraph.NonTorchMetagraph.emission>)
      * [`NonTorchMetagraph.incentive`](<#bittensor.core.metagraph.NonTorchMetagraph.incentive>)
      * [`NonTorchMetagraph.last_update`](<#bittensor.core.metagraph.NonTorchMetagraph.last_update>)
      * [`NonTorchMetagraph.load_from_path()`](<#bittensor.core.metagraph.NonTorchMetagraph.load_from_path>)
      * [`NonTorchMetagraph.n`](<#bittensor.core.metagraph.NonTorchMetagraph.n>)
      * [`NonTorchMetagraph.netuid`](<#bittensor.core.metagraph.NonTorchMetagraph.netuid>)
      * [`NonTorchMetagraph.should_sync`](<#bittensor.core.metagraph.NonTorchMetagraph.should_sync>)
      * [`NonTorchMetagraph.stake`](<#bittensor.core.metagraph.NonTorchMetagraph.stake>)
      * [`NonTorchMetagraph.subtensor`](<#bittensor.core.metagraph.NonTorchMetagraph.subtensor>)
      * [`NonTorchMetagraph.tao_stake`](<#bittensor.core.metagraph.NonTorchMetagraph.tao_stake>)
      * [`NonTorchMetagraph.total_stake`](<#bittensor.core.metagraph.NonTorchMetagraph.total_stake>)
      * [`NonTorchMetagraph.uids`](<#bittensor.core.metagraph.NonTorchMetagraph.uids>)
      * [`NonTorchMetagraph.validator_permit`](<#bittensor.core.metagraph.NonTorchMetagraph.validator_permit>)
      * [`NonTorchMetagraph.validator_trust`](<#bittensor.core.metagraph.NonTorchMetagraph.validator_trust>)
      * [`NonTorchMetagraph.version`](<#bittensor.core.metagraph.NonTorchMetagraph.version>)
      * [`NonTorchMetagraph.weights`](<#bittensor.core.metagraph.NonTorchMetagraph.weights>)
    * [`NumpyOrTorch`](<#bittensor.core.metagraph.NumpyOrTorch>)
    * [`Tensor`](<#bittensor.core.metagraph.Tensor>)
    * [`TorchMetagraph`](<#bittensor.core.metagraph.TorchMetagraph>)
      * [`TorchMetagraph.active`](<#bittensor.core.metagraph.TorchMetagraph.active>)
      * [`TorchMetagraph.alpha_stake`](<#bittensor.core.metagraph.TorchMetagraph.alpha_stake>)
      * [`TorchMetagraph.block`](<#bittensor.core.metagraph.TorchMetagraph.block>)
      * [`TorchMetagraph.bonds`](<#bittensor.core.metagraph.TorchMetagraph.bonds>)
      * [`TorchMetagraph.consensus`](<#bittensor.core.metagraph.TorchMetagraph.consensus>)
      * [`TorchMetagraph.dividends`](<#bittensor.core.metagraph.TorchMetagraph.dividends>)
      * [`TorchMetagraph.emission`](<#bittensor.core.metagraph.TorchMetagraph.emission>)
      * [`TorchMetagraph.incentive`](<#bittensor.core.metagraph.TorchMetagraph.incentive>)
      * [`TorchMetagraph.last_update`](<#bittensor.core.metagraph.TorchMetagraph.last_update>)
      * [`TorchMetagraph.load_from_path()`](<#bittensor.core.metagraph.TorchMetagraph.load_from_path>)
      * [`TorchMetagraph.n`](<#bittensor.core.metagraph.TorchMetagraph.n>)
      * [`TorchMetagraph.stake`](<#bittensor.core.metagraph.TorchMetagraph.stake>)
      * [`TorchMetagraph.tao_stake`](<#bittensor.core.metagraph.TorchMetagraph.tao_stake>)
      * [`TorchMetagraph.total_stake`](<#bittensor.core.metagraph.TorchMetagraph.total_stake>)
      * [`TorchMetagraph.uids`](<#bittensor.core.metagraph.TorchMetagraph.uids>)
      * [`TorchMetagraph.validator_permit`](<#bittensor.core.metagraph.TorchMetagraph.validator_permit>)
      * [`TorchMetagraph.validator_trust`](<#bittensor.core.metagraph.TorchMetagraph.validator_trust>)
      * [`TorchMetagraph.version`](<#bittensor.core.metagraph.TorchMetagraph.version>)
      * [`TorchMetagraph.weights`](<#bittensor.core.metagraph.TorchMetagraph.weights>)
    * [`async_metagraph()`](<#bittensor.core.metagraph.async_metagraph>)
    * [`get_save_dir()`](<#bittensor.core.metagraph.get_save_dir>)
    * [`latest_block_path()`](<#bittensor.core.metagraph.latest_block_path>)
    * [`safe_globals()`](<#bittensor.core.metagraph.safe_globals>)



# bittensor.core.metagraph[#](<#module-bittensor.core.metagraph> "Link to this heading")

## Attributes[#](<#attributes> "Link to this heading")

[`BaseClass`](<#bittensor.core.metagraph.BaseClass> "bittensor.core.metagraph.BaseClass") |   
---|---  
[`METAGRAPH_STATE_DICT_NDARRAY_KEYS`](<#bittensor.core.metagraph.METAGRAPH_STATE_DICT_NDARRAY_KEYS> "bittensor.core.metagraph.METAGRAPH_STATE_DICT_NDARRAY_KEYS") | List of keys for the metagraph state dictionary used in NDArray serialization.  
[`NumpyOrTorch`](<#bittensor.core.metagraph.NumpyOrTorch> "bittensor.core.metagraph.NumpyOrTorch") |   
[`Tensor`](<#bittensor.core.metagraph.Tensor> "bittensor.core.metagraph.Tensor") |   
  
## Classes[#](<#classes> "Link to this heading")

[`AsyncMetagraph`](<#bittensor.core.metagraph.AsyncMetagraph> "bittensor.core.metagraph.AsyncMetagraph") | Asynchronous version of the Metagraph class for non-blocking synchronization with the Bittensor network state.  
---|---  
[`Metagraph`](<#bittensor.core.metagraph.Metagraph> "bittensor.core.metagraph.Metagraph") | Synchronous implementation of the Metagraph, representing the current state of a Bittensor subnet.  
[`MetagraphMixin`](<#bittensor.core.metagraph.MetagraphMixin> "bittensor.core.metagraph.MetagraphMixin") | The metagraph class is a core component of the Bittensor network, representing the neural graph that forms the  
[`NonTorchMetagraph`](<#bittensor.core.metagraph.NonTorchMetagraph> "bittensor.core.metagraph.NonTorchMetagraph") | The metagraph class is a core component of the Bittensor network, representing the neural graph that forms the  
[`TorchMetagraph`](<#bittensor.core.metagraph.TorchMetagraph> "bittensor.core.metagraph.TorchMetagraph") | The metagraph class is a core component of the Bittensor network, representing the neural graph that forms the  
  
## Functions[#](<#functions> "Link to this heading")

[`async_metagraph`](<#bittensor.core.metagraph.async_metagraph> "bittensor.core.metagraph.async_metagraph")(netuid[, mechid, network, lite, sync, ...]) | Factory function to create an instantiated AsyncMetagraph, mainly for the ability to use sync at instantiation.  
---|---  
[`get_save_dir`](<#bittensor.core.metagraph.get_save_dir> "bittensor.core.metagraph.get_save_dir")(network, netuid[, root_dir]) | Returns a directory path given `network` and `netuid` inputs.  
[`latest_block_path`](<#bittensor.core.metagraph.latest_block_path> "bittensor.core.metagraph.latest_block_path")(dir_path) | Get the latest block path from the provided directory path.  
[`safe_globals`](<#bittensor.core.metagraph.safe_globals> "bittensor.core.metagraph.safe_globals")() | Context manager to load torch files for version 2.6+  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.metagraph.AsyncMetagraph(_netuid_ , _mechid =0_, _network =settings.DEFAULT_NETWORK_, _lite =True_, _sync =True_, _subtensor =None_)[#](<#bittensor.core.metagraph.AsyncMetagraph> "Link to this definition")
    

Bases: [`NumpyOrTorch`](<#bittensor.core.metagraph.NumpyOrTorch> "bittensor.core.metagraph.NumpyOrTorch")

Asynchronous version of the Metagraph class for non-blocking synchronization with the Bittensor network state.

This class allows developers to fetch and update metagraph data using async operations, enabling concurrent execution in event-driven environments.

Note

Prefer using the factory function async_metagraph() for initialization, which handles async synchronization automatically.

Example

metagraph = await async_metagraph(netuid=1, network=”finney”)

Initializes a new instance of the metagraph object, setting up the basic structure and parameters based on the provided arguments. This class requires Torch to be installed. This method is the entry point for creating a metagraph object, which is a central component in representing the state of the Bittensor network.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Subnet unique identifier.

  * **network** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The name of the network, which can indicate specific configurations or versions of the Bittensor

  * **network.**

  * **lite** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – A flag indicating whether to use a lite version of the metagraph. The lite version may contain less detailed information but can be quicker to initialize and sync.

  * **sync** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – A flag indicating whether to synchronize the metagraph with the network upon initialization. Synchronization involves updating the metagraph’s parameters to reflect the current state of the network.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Subnet mechanism unique identifier.

  * **subtensor** (_Optional_ _[_[_bittensor.core.async_subtensor.AsyncSubtensor_](<../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor") _]_)




Example

Initializing a metagraph object for the Bittensor network with a specific network UID:

> from bittensor.core.metagraph import Metagraph
> 
> metagraph = Metagraph(netuid=123, network=”finney”, lite=True, sync=True)

async sync(_block =None_, _lite =None_, _subtensor =None_)[#](<#bittensor.core.metagraph.AsyncMetagraph.sync> "Link to this definition")
    

Synchronizes the metagraph with the Bittensor network’s current state. It updates the metagraph’s attributes to
    

reflect the latest data from the network, ensuring the metagraph represents the most current state of the network.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – A specific block number to synchronize with. If None, the metagraph syncs with the latest block. This allows for historical analysis or specific state examination of the network.

  * **lite** (_Optional_ _[_[_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)") _]_) – If True, a lite version of the metagraph is used for quicker synchronization. This is beneficial when full detail is not necessary, allowing for reduced computational and time overhead.

  * **subtensor** (_Optional_ _[_[_bittensor.core.async_subtensor.AsyncSubtensor_](<../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor") _]_) – An instance of the subtensor class from Bittensor, providing an interface to the underlying blockchain data. If provided, this instance is used for data retrieval during synchronization.




Example

Sync the metagraph with the latest block from the subtensor, using the lite version for efficiency:
[code] 
    from bittensor.core.subtensor import Subtensor
    
    subtensor = Subtensor()
    metagraph.sync(subtensor=subtensor)
    
[/code]

Sync with a specific block number for detailed analysis:
[code] 
    from bittensor.core.subtensor import Subtensor
    
    subtensor = Subtensor()
    metagraph.sync(block=12345, lite=False, subtensor=subtensor)
    
[/code]

Note

If attempting to access data beyond the previous 300 blocks, you **must** use the `archive` network for
    

subtensor. Light nodes are configured only to store the previous 300 blocks if connecting to finney or test networks.

Example:

> from bittensor.core.subtensor import Subtensor
> 
> subtensor = Subtensor(network=’archive’) current_block = subtensor.get_current_block() history_block = current_block - 1200
> 
> metagraph.sync(block=history_block, lite=False, subtensor=subtensor)

bittensor.core.metagraph.BaseClass[#](<#bittensor.core.metagraph.BaseClass> "Link to this definition")
    

bittensor.core.metagraph.METAGRAPH_STATE_DICT_NDARRAY_KEYS = ['version', 'n', 'block', 'stake', 'consensus', 'validator_trust', 'incentive', 'emission',...[#](<#bittensor.core.metagraph.METAGRAPH_STATE_DICT_NDARRAY_KEYS> "Link to this definition")
    

List of keys for the metagraph state dictionary used in NDArray serialization.

This list defines the set of keys expected in the metagraph’s state dictionary when serializing and deserializing NumPy ndarray objects. Each key corresponds to a specific attribute or metric associated with the nodes in the metagraph.

  * **version** (str): The version identifier of the metagraph state.

  * **n** (int): The total number of nodes in the metagraph.

  * **block** (int): The current block number in the blockchain or ledger.

  * **stake** (ndarray): An array representing the stake of each node.

  * **total_stake** (float): The sum of all individual stakes in the metagraph.

  * **ranks** (ndarray): An array of rank scores assigned to each node.

  * **trust** (ndarray): An array of trust scores for the nodes.

  * **consensus** (ndarray): An array indicating consensus levels among nodes.

  * **validator_trust** (ndarray): Trust scores specific to validator nodes.

  * **incentive** (ndarray): Incentive values allocated to nodes.

  * **emission** (float): The rate of emission for new tokens or units.

  * **dividends** (ndarray): Dividend amounts distributed to nodes.

  * **active** (ndarray): Boolean array indicating active (True) or inactive (False) nodes.

  * **last_update** (int): Timestamp of the last state update.

  * **validator_permit** (ndarray): Boolean array indicating nodes permitted to validate.

  * **uids** (ndarray): Unique identifiers for each node in the metagraph.




class bittensor.core.metagraph.Metagraph(_netuid_ , _mechid =0_, _network =settings.DEFAULT_NETWORK_, _lite =True_, _sync =True_, _subtensor =None_)[#](<#bittensor.core.metagraph.Metagraph> "Link to this definition")
    

Bases: [`NumpyOrTorch`](<#bittensor.core.metagraph.NumpyOrTorch> "bittensor.core.metagraph.NumpyOrTorch")

Synchronous implementation of the Metagraph, representing the current state of a Bittensor subnet.

The Metagraph encapsulates neuron attributes such as stake, trust, incentive, weights, and connectivity, and provides methods to synchronize these values directly from the blockchain via a Subtensor instance.

Example

from bittensor.core.subtensor import Subtensor subtensor = Subtensor(network=”finney”) metagraph = Metagraph(netuid=1, network=”finney”, sync=True, subtensor=subtensor)

Initializes a new instance of the metagraph object, setting up the basic structure and parameters based on the provided arguments. This class requires Torch to be installed. This method is the entry point for creating a metagraph object, which is a central component in representing the state of the Bittensor network.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Subnet unique identifier.

  * **network** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The name of the network, which can indicate specific configurations or versions of the Bittensor

  * **network.**

  * **lite** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – A flag indicating whether to use a lite version of the metagraph. The lite version may contain less detailed information but can be quicker to initialize and sync.

  * **sync** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – A flag indicating whether to synchronize the metagraph with the network upon initialization. Synchronization involves updating the metagraph’s parameters to reflect the current state of the network.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Subnet mechanism unique identifier.

  * **subtensor** (_Optional_ _[_[_bittensor.core.subtensor.Subtensor_](<../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor") _]_)




Example

Initializing a metagraph object for the Bittensor network with a specific network UID:

> from bittensor.core.metagraph import Metagraph
> 
> metagraph = Metagraph(netuid=123, network=”finney”, lite=True, sync=True)

sync(_block =None_, _lite =None_, _subtensor =None_)[#](<#bittensor.core.metagraph.Metagraph.sync> "Link to this definition")
    

Synchronizes the metagraph with the Bittensor network’s current state. It updates the metagraph’s attributes to
    

reflect the latest data from the network, ensuring the metagraph represents the most current state of the network.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – A specific block number to synchronize with. If None, the metagraph syncs with the latest block. This allows for historical analysis or specific state examination of the network.

  * **lite** (_Optional_ _[_[_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)") _]_) – If True, a lite version of the metagraph is used for quicker synchronization. This is beneficial when full detail is not necessary, allowing for reduced computational and time overhead.

  * **subtensor** (_Optional_ _[_[_bittensor.core.subtensor.Subtensor_](<../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor") _]_) – An instance of the subtensor class from Bittensor, providing an interface to the underlying blockchain data. If provided, this instance is used for data retrieval during synchronization.




Example

Sync the metagraph with the latest block from the subtensor, using the lite version for efficiency:
[code] 
    from bittensor.core.subtensor import Subtensor
    
    subtensor = Subtensor()
    metagraph.sync(subtensor=subtensor)
    
[/code]

Sync with a specific block number for detailed analysis:
[code] 
    from bittensor.core.subtensor import Subtensor
    
    subtensor = Subtensor()
    metagraph.sync(block=12345, lite=False, subtensor=subtensor)
    
[/code]

Note

If attempting to access data beyond the previous 300 blocks, you **must** use the `archive` network for
    

subtensor. Light nodes are configured only to store the previous 300 blocks if connecting to finney or test networks.

Example:

> from bittensor.core.subtensor import Subtensor
> 
> subtensor = Subtensor(network=’archive’) current_block = subtensor.get_current_block() history_block = current_block - 1200
> 
> metagraph.sync(block=history_block, lite=False, subtensor=subtensor)

class bittensor.core.metagraph.MetagraphMixin(_netuid_ , _mechid =0_, _network =settings.DEFAULT_NETWORK_, _lite =True_, _sync =True_, _subtensor =None_)[#](<#bittensor.core.metagraph.MetagraphMixin> "Link to this definition")
    

Bases: [`abc.ABC`](<https://docs.python.org/3/library/abc.html#abc.ABC> "\(in Python v3.14\)")

The metagraph class is a core component of the Bittensor network, representing the neural graph that forms the backbone of the decentralized machine learning system.

The metagraph is a dynamic representation of the network’s state, capturing the interconnectedness and attributes of
    

neurons (participants) in the Bittensor ecosystem. This class is not just a static structure but a live reflection of the network, constantly updated and synchronized with the state of the blockchain.

In Bittensor, neurons are akin to nodes in a distributed system, each contributing computational resources and
    

participating in the network’s collective intelligence. The metagraph tracks various attributes of these neurons, such as stake, trust, and consensus, which are crucial for the network’s incentive mechanisms and the Yuma Consensus algorithm as outlined in the [NeurIPS paper](<https://bittensor.com/pdfs/academia/NeurIPS_DAO_Workshop_2022_3_3.pdf>). These attributes govern how neurons interact, how they are incentivized, and their roles within the network’s decision-making processes.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – A unique identifier that distinguishes between different instances or versions of the Bittensor network.

  * **network** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The name of the network, signifying specific configurations or iterations within the Bittensor ecosystem.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

  * **lite** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **sync** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **subtensor** (_Optional_ _[__Union_ _[_[_bittensor.core.async_subtensor.AsyncSubtensor_](<../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor") _,_[_bittensor.core.subtensor.Subtensor_](<../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor") _]__]_)



Variables:
    

  * **version** (_NDArray_) – The version number of the network, integral for tracking network updates.

  * **n** (_NDArray_) – The total number of neurons in the network, reflecting its size and complexity.

  * **block** (_NDArray_) – The current block number in the blockchain, crucial for synchronizing with the network’s latest state.

  * **stake** – Represents the cryptocurrency staked by neurons, impacting their influence and earnings within the network.

  * **ranks** – Neuron rankings as per the Yuma Consensus algorithm, influencing their incentive distribution and network authority.

  * **trust** – Scores indicating the reliability of neurons, mainly miners, within the network’s operational context.

  * **consensus** – Scores reflecting each neuron’s alignment with the network’s collective decisions.

  * **validator_trust** – Trust scores for validator neurons, crucial for network security and validation.

  * **incentive** – Rewards allocated to neurons, particularly miners, for their network contributions.

  * **emission** – The rate at which rewards are distributed to neurons.

  * **dividends** – Rewards received primarily by validators as part of the incentive mechanism.

  * **active** – Status indicating whether a neuron is actively participating in the network.

  * **last_update** – Timestamp of the latest update to a neuron’s data.

  * **validator_permit** – Indicates if a neuron is authorized to act as a validator.

  * **weights** – Inter-neuronal weights set by each neuron, influencing network dynamics.

  * **bonds** – Represents speculative investments by neurons in others, part of the reward mechanism.

  * **uids** – Unique identifiers for each neuron, essential for network operations.

  * **axons** (_List_) – Details about each neuron’s axon, critical for facilitating network communication.




The metagraph plays a pivotal role in Bittensor’s decentralized AI operations, influencing everything from data propagation to reward distribution. It embodies the principles of decentralized governance and collaborative intelligence, ensuring that the network remains adaptive, secure, and efficient.

Example

Initializing the metagraph to represent the current state of the Bittensor network:
[code] 
    from bittensor.core.metagraph import Metagraph
    metagraph = Metagraph(netuid=config.netuid, network=subtensor.network, sync=False)
    
[/code]

Synchronizing the metagraph with the network to reflect the latest state and neuron data:
[code] 
    metagraph.sync(subtensor=subtensor)
    
[/code]

Accessing metagraph properties to inform network interactions and decisions:
[code] 
    total_stake = metagraph.S
    neuron_ranks = metagraph.R
    neuron_incentives = metagraph.I
    axons = metagraph.axons
    neurons = metagraph.neurons
    
[/code]

Maintaining a local copy of hotkeys for querying and interacting with network entities:
[code] 
    hotkeys = deepcopy(metagraph.hotkeys)
    
[/code]

Initializes a new instance of the metagraph object, setting up the basic structure and parameters based on the provided arguments. This method is the entry point for creating a metagraph object, which is a central component in representing the state of the Bittensor network.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier for the network, distinguishing this instance of the metagraph within potentially multiple network configurations.

  * **network** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The name of the network, which can indicate specific configurations or versions of the Bittensor network.

  * **lite** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – A flag indicating whether to use a lite version of the metagraph. The lite version may contain less detailed information but can be quicker to initialize and sync.

  * **sync** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – A flag indicating whether to synchronize the metagraph with the network upon initialization. Synchronization involves updating the metagraph’s parameters to reflect the current state of the network.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

  * **subtensor** (_Optional_ _[__Union_ _[_[_bittensor.core.async_subtensor.AsyncSubtensor_](<../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor") _,_[_bittensor.core.subtensor.Subtensor_](<../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor") _]__]_)




Example

Initializing a metagraph object for the Bittensor network with a specific network UID:

> metagraph = Metagraph(netuid=123, network=”finney”, lite=True, sync=True)

property AS: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.AS> "Link to this definition")
    

Represents the alpha stake of each neuron in the Bittensor network.

Returns:
    

The list of alpha stake of each neuron in the network.

Return type:
    

[Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")

property B: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.B> "Link to this definition")
    

Bonds in the Bittensor network represent a speculative reward mechanism where neurons can accumulate bonds in other neurons. Bonds are akin to investments or stakes in other neurons, reflecting a belief in their future value or performance. This mechanism encourages correct weighting and collaboration among neurons while providing an additional layer of incentive.

Returns:
    

A tensor representing the bonds held by each neuron, where each value signifies the proportion of
    

bonds owned by one neuron in another.

Return type:
    

[Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")

property C: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.C> "Link to this definition")
    

Represents the consensus values of neurons in the Bittensor network. Consensus is a measure of how much a neuron’s contributions are trusted and agreed upon by the majority of the network. It is calculated based on a staked weighted trust system, where the network leverages the collective judgment of all participating peers. Higher consensus values indicate that a neuron’s contributions are more widely trusted and valued across the network.

Returns:
    

A tensor of consensus values, where each element reflects the level of trust and agreement a neuron
    

has achieved within the network.

Return type:
    

[Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")

property D: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.D> "Link to this definition")
    

Represents the dividends received by neurons in the Bittensor network. Dividends are a form of reward or distribution, typically given to neurons based on their stake, performance, and contribution to the network. They are an integral part of the network’s incentive structure, encouraging active and beneficial participation.

Returns:
    

A tensor of dividend values, where each element indicates the dividends received by a neuron,
    

reflecting their share of network rewards.

Return type:
    

[Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")

property E: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.E> "Link to this definition")
    

Denotes the emission values of neurons in the Bittensor network. Emissions refer to the distribution or release of rewards (often in the form of cryptocurrency) to neurons, typically based on their stake and performance. This mechanism is central to the network’s incentive model, ensuring that active and contributing neurons are appropriately rewarded.

Returns:
    

A tensor where each element represents the emission value for a neuron, indicating the amount of
    

reward distributed to that neuron.

Return type:
    

[Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")

property I: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.I> "Link to this definition")
    

Incentive values of neurons represent the rewards they receive for their contributions to the network. The Bittensor network employs an incentive mechanism that rewards neurons based on their informational value, stake, and consensus with other peers. This ensures that the most valuable and trusted contributions are incentivized.

Returns:
    

A tensor of incentive values, indicating the rewards or benefits accrued by each neuron based on
    

their contributions and network consensus.

Return type:
    

[Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")

property S: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.S> "Link to this definition")
    

Represents the stake of each neuron in the Bittensor network. Stake is an important concept in the Bittensor ecosystem, signifying the amount of network weight (or “stake”) each neuron holds, represented on a digital ledger. The stake influences a neuron’s ability to contribute to and benefit from the network, playing a crucial role in the distribution of incentives and decision-making processes.

Returns:
    

A tensor representing the stake of each neuron in the network. Higher values signify a greater
    

stake held by the respective neuron.

Return type:
    

[Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")

property TS: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.TS> "Link to this definition")
    

Represents the tao stake of each neuron in the Bittensor network.

Returns:
    

The list of tao stake of each neuron in the network.

Return type:
    

[Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")

property Tv: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.Tv> "Link to this definition")
    

Contains the validator trust values of neurons in the Bittensor network. Validator trust is specifically associated with neurons that act as validators within the network. This specialized form of trust reflects the validators’ reliability and integrity in their role, which is crucial for maintaining the network’s stability and security.

Validator trust values are particularly important for the network’s consensus and validation processes, determining the validators’ influence and responsibilities in these critical functions.

Returns:
    

A tensor of validator trust values, specifically applicable to neurons serving as validators, where
    

higher values denote greater trustworthiness in their validation roles.

Return type:
    

[Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")

property W: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.W> "Link to this definition")
    

Represents the weights assigned to each neuron in the Bittensor network. In the context of Bittensor, weights are crucial for determining the influence and interaction between neurons. Each neuron is responsible for setting its weights, which are then recorded on a digital ledger. These weights are reflective of the neuron’s assessment or judgment of other neurons in the network.

The weight matrix \\(W = [w_{ij}]\\) is a key component of the network’s architecture, where the :math: i^{th} row is set by neuron \\(i\\) and represents its weights towards other neurons. These weights influence the ranking and incentive mechanisms within the network. Higher weights from a neuron towards another can imply greater trust or value placed on that neuron’s contributions.

Returns:
    

A tensor of inter-peer weights, where each element \\(w_{ij}\\) represents the weight assigned by
    

neuron \\(i\\) to neuron \\(j\\). This matrix is fundamental to the network’s functioning, influencing the distribution of incentives and the inter-neuronal dynamics.

Return type:
    

[Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")

active: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.active> "Link to this definition")
    

property addresses: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")][#](<#bittensor.core.metagraph.MetagraphMixin.addresses> "Link to this definition")
    

Provides a list of IP addresses for each neuron in the Bittensor network. These addresses are used for network communication, allowing neurons to connect, interact, and exchange information with each other. IP addresses are fundamental for the network’s peer-to-peer communication infrastructure.

Returns:
    

A list of IP addresses, with each string representing the address of a neuron. These addresses
    

enable the decentralized, distributed nature of the network, facilitating direct communication and data exchange among neurons.

Return type:
    

List[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]

Note

While IP addresses are a basic aspect of network communication, specific details about their use in the Bittensor network may not be covered in the [NeurIPS paper](<https://bittensor.com/pdfs/academia/NeurIPS_DAO_Workshop_2022_3_3.pdf>). They are, however, integral to the functioning of any distributed network.

alpha_dividends_per_hotkey: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")]][#](<#bittensor.core.metagraph.MetagraphMixin.alpha_dividends_per_hotkey> "Link to this definition")
    

alpha_stake: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.alpha_stake> "Link to this definition")
    

axons: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[bittensor.core.chain_data.AxonInfo][#](<#bittensor.core.metagraph.MetagraphMixin.axons> "Link to this definition")
    

block: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.block> "Link to this definition")
    

block_at_registration: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")][#](<#bittensor.core.metagraph.MetagraphMixin.block_at_registration> "Link to this definition")
    

blocks_since_last_step: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.metagraph.MetagraphMixin.blocks_since_last_step> "Link to this definition")
    

bonds: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.bonds> "Link to this definition")
    

chain_endpoint: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.metagraph.MetagraphMixin.chain_endpoint> "Link to this definition")
    

property coldkeys: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")][#](<#bittensor.core.metagraph.MetagraphMixin.coldkeys> "Link to this definition")
    

Contains a list of `coldkeys` for each neuron in the Bittensor network.

Coldkeys are similar to hotkeys but are typically used for more secure, offline activities such as storing assets or offline signing of transactions. They are an important aspect of a neuron’s security, providing an additional layer of protection for sensitive operations and assets.

Returns:
    

A list of coldkeys, each string representing the coldkey of a neuron. These keys play a vital
    

role in the secure management of assets and sensitive operations within the network.

Return type:
    

List[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]

Note

The concept of coldkeys, while not explicitly covered in the NeurIPS paper, is a standard practice in
    

blockchain and decentralized networks for enhanced security and asset protection.

consensus: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.consensus> "Link to this definition")
    

dividends: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.dividends> "Link to this definition")
    

emission: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.emission> "Link to this definition")
    

emissions: bittensor.core.chain_data.MetagraphInfoEmissions[#](<#bittensor.core.metagraph.MetagraphMixin.emissions> "Link to this definition")
    

property hotkeys: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")][#](<#bittensor.core.metagraph.MetagraphMixin.hotkeys> "Link to this definition")
    

Represents a list of `hotkeys` for each neuron in the Bittensor network.

Hotkeys are unique identifiers used by neurons for active participation in the network, such as sending and receiving information or transactions. They are akin to public keys in cryptographic systems and are essential for identifying and authenticating neurons within the network’s operations.

Returns:
    

A list of hotkeys, with each string representing the hotkey of a corresponding neuron.

These keys are crucial for the network’s security and integrity, ensuring proper identification and
    

authorization of network participants.

Return type:
    

List[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]

Note

While the [NeurIPS paper](<https://bittensor.com/pdfs/academia/NeurIPS_DAO_Workshop_2022_3_3.pdf>) may not
    

explicitly detail the concept of hotkeys, they are a fundamental of decentralized networks for secure and authenticated interactions.

hparams: bittensor.core.chain_data.MetagraphInfoParams[#](<#bittensor.core.metagraph.MetagraphMixin.hparams> "Link to this definition")
    

identities: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[bittensor.core.chain_data.ChainIdentity | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")][#](<#bittensor.core.metagraph.MetagraphMixin.identities> "Link to this definition")
    

identity: bittensor.core.chain_data.SubnetIdentity | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.metagraph.MetagraphMixin.identity> "Link to this definition")
    

incentive: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.incentive> "Link to this definition")
    

last_step: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.metagraph.MetagraphMixin.last_step> "Link to this definition")
    

last_update: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.last_update> "Link to this definition")
    

lite = True[#](<#bittensor.core.metagraph.MetagraphMixin.lite> "Link to this definition")
    

load(_root_dir =None_)[#](<#bittensor.core.metagraph.MetagraphMixin.load> "Link to this definition")
    

Loads the state of the metagraph from the default save directory. This method is instrumental for restoring the metagraph to its last saved state. It automatically identifies the save directory based on the `network` and `netuid` properties of the metagraph, locates the latest block file in that directory, and loads all metagraph parameters from it.

This functionality is particularly beneficial when continuity in the state of the metagraph is necessary across different runtime sessions, or after a restart of the system. It ensures that the metagraph reflects the exact state it was in at the last save point, maintaining consistency in the network’s representation.

The method delegates to `load_from_path`, supplying it with the directory path constructed from the metagraph’s current `network` and `netuid` properties. This abstraction simplifies the process of loading the metagraph’s state for the user, requiring no direct path specifications.

Parameters:
    

**root_dir** (_Optional_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]__]_) – list to the file path for the root directory of your metagraph saves (i.e. [‘/’, ‘tmp’, ‘metagraphs’], defaults to [“~”, “.bittensor”, “metagraphs”]

Returns:
    

The metagraph instance after loading its state from the default directory.

Return type:
    

[metagraph](<../../extras/subtensor_api/metagraphs/index.html#bittensor.extras.subtensor_api.metagraphs.Metagraphs.metagraph> "bittensor.extras.subtensor_api.metagraphs.Metagraphs.metagraph")

Example

Load the metagraph state from the last saved snapshot in the default directory:
[code] 
    metagraph.load()
    
[/code]

After this operation, the metagraph’s parameters and neuron data are restored to their state at the time of the last save in the default directory.

Note

The default save directory is determined based on the metagraph’s `network` and `netuid` attributes. It is important to ensure that these attributes are set correctly and that the default save directory contains the appropriate state files for the metagraph.

abstractmethod load_from_path(_dir_path_)[#](<#bittensor.core.metagraph.MetagraphMixin.load_from_path> "Link to this definition")
    

Loads the state of the metagraph from a specified directory path. This method is crucial for restoring the metagraph to a specific state based on saved data. It locates the latest block file in the given directory and loads all metagraph parameters from it. This is particularly useful for analyses that require historical states of the network or for restoring previous states of the metagraph in different execution environments.

The method first identifies the latest block file in the specified directory, then loads the metagraph state including neuron attributes and parameters from this file. This ensures that the metagraph is accurately reconstituted to reflect the network state at the time of the saved block.

Parameters:
    

**dir_path** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The directory path where the metagraph’s state files are stored. This path should contain one or more saved state files, typically named in a format that includes the block number.

Returns:
    

The metagraph instance after loading its state from the specified directory path.

Return type:
    

[metagraph](<../../extras/subtensor_api/metagraphs/index.html#bittensor.extras.subtensor_api.metagraphs.Metagraphs.metagraph> "bittensor.extras.subtensor_api.metagraphs.Metagraphs.metagraph")

Example

Load the metagraph state from a specific directory:
[code] 
    dir_path = "/path/to/saved/metagraph/states"
    metagraph.load_from_path(dir_path)
    
[/code]

The metagraph is now restored to the state it was in at the time of the latest saved block in the specified directory.

Note

This method assumes that the state files in the specified directory are correctly formatted and contain valid data for the metagraph. It is essential to ensure that the directory path and the state files within it are accurate and consistent with the expected metagraph structure.

max_uids: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.metagraph.MetagraphMixin.max_uids> "Link to this definition")
    

mechanism_count: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.metagraph.MetagraphMixin.mechanism_count> "Link to this definition")
    

mechanisms_emissions_split: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")][#](<#bittensor.core.metagraph.MetagraphMixin.mechanisms_emissions_split> "Link to this definition")
    

mechid: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.metagraph.MetagraphMixin.mechid> "Link to this definition")
    

metadata()[#](<#bittensor.core.metagraph.MetagraphMixin.metadata> "Link to this definition")
    

Retrieves the metadata of the metagraph, providing key information about the current state of the Bittensor network. This metadata includes details such as the network’s unique identifier (`netuid`), the total number of neurons (`n`), the current block number, the network’s name, and the version of the Bittensor network.

Returns:
    

A dictionary containing essential metadata about the metagraph, including:

  * `netuid`: The unique identifier for the network.

  * `n`: The total number of neurons in the network.

  * `block`: The current block number in the network’s blockchain.

  * `network`: The name of the Bittensor network.

  * `version`: The version number of the Bittensor software.




Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")

Note

This metadata is crucial for understanding the current state and configuration of the network, as well as
    

for tracking its evolution over time.

n: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.n> "Link to this definition")
    

name: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.metagraph.MetagraphMixin.name> "Link to this definition")
    

netuid: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.metagraph.MetagraphMixin.netuid> "Link to this definition")
    

network: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.metagraph.MetagraphMixin.network> "Link to this definition")
    

network_registered_at: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.metagraph.MetagraphMixin.network_registered_at> "Link to this definition")
    

neurons: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[bittensor.core.chain_data.NeuronInfo | bittensor.core.chain_data.NeuronInfoLite][#](<#bittensor.core.metagraph.MetagraphMixin.neurons> "Link to this definition")
    

num_uids: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.metagraph.MetagraphMixin.num_uids> "Link to this definition")
    

owner_coldkey: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.metagraph.MetagraphMixin.owner_coldkey> "Link to this definition")
    

owner_hotkey: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.metagraph.MetagraphMixin.owner_hotkey> "Link to this definition")
    

pool: bittensor.core.chain_data.MetagraphInfoPool[#](<#bittensor.core.metagraph.MetagraphMixin.pool> "Link to this definition")
    

pruning_score: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")][#](<#bittensor.core.metagraph.MetagraphMixin.pruning_score> "Link to this definition")
    

ranks: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.ranks> "Link to this definition")
    

save(_root_dir =None_)[#](<#bittensor.core.metagraph.MetagraphMixin.save> "Link to this definition")
    

Saves the current state of the metagraph to a file on disk. This function is crucial for persisting the current
    

state of the network’s metagraph, which can later be reloaded or analyzed. The save operation includes all neuron attributes and parameters, ensuring a complete snapshot of the metagraph’s state.

Parameters:
    

**root_dir** (_Optional_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]__]_) – list to the file path for the root directory of your metagraph saves (i.e. [‘/’, ‘tmp’, ‘metagraphs’], defaults to [“~”, “.bittensor”, “metagraphs”]

Returns:
    

The metagraph instance after saving its state.

Return type:
    

[metagraph](<../../extras/subtensor_api/metagraphs/index.html#bittensor.extras.subtensor_api.metagraphs.Metagraphs.metagraph> "bittensor.extras.subtensor_api.metagraphs.Metagraphs.metagraph")

Example

Save the current state of the metagraph to the default directory:
[code] 
    metagraph.save()
    
[/code]

The saved state can later be loaded to restore or analyze the metagraph’s state at this point.

If using the default save path:
[code] 
    metagraph.load()
    
[/code]

If using a custom save path:
[code] 
    metagraph.load_from_path(dir_path)
    
[/code]

should_sync = True[#](<#bittensor.core.metagraph.MetagraphMixin.should_sync> "Link to this definition")
    

stake: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.stake> "Link to this definition")
    

state_dict()[#](<#bittensor.core.metagraph.MetagraphMixin.state_dict> "Link to this definition")
    

subtensor: [bittensor.core.async_subtensor.AsyncSubtensor](<../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor") | [bittensor.core.subtensor.Subtensor](<../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.metagraph.MetagraphMixin.subtensor> "Link to this definition")
    

symbol: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.metagraph.MetagraphMixin.symbol> "Link to this definition")
    

tao_dividends_per_hotkey: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")]][#](<#bittensor.core.metagraph.MetagraphMixin.tao_dividends_per_hotkey> "Link to this definition")
    

tao_stake: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.tao_stake> "Link to this definition")
    

tempo: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.metagraph.MetagraphMixin.tempo> "Link to this definition")
    

trust: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.trust> "Link to this definition")
    

uids: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.uids> "Link to this definition")
    

validator_permit: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.validator_permit> "Link to this definition")
    

validator_trust: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.validator_trust> "Link to this definition")
    

version: bittensor.utils.registration.torch.nn.Parameter | [tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[numpy.typing.NDArray][#](<#bittensor.core.metagraph.MetagraphMixin.version> "Link to this definition")
    

weights: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.MetagraphMixin.weights> "Link to this definition")
    

class bittensor.core.metagraph.NonTorchMetagraph(_netuid_ , _mechid =0_, _network =settings.DEFAULT_NETWORK_, _lite =True_, _sync =True_, _subtensor =None_)[#](<#bittensor.core.metagraph.NonTorchMetagraph> "Link to this definition")
    

Bases: [`MetagraphMixin`](<#bittensor.core.metagraph.MetagraphMixin> "bittensor.core.metagraph.MetagraphMixin")

The metagraph class is a core component of the Bittensor network, representing the neural graph that forms the backbone of the decentralized machine learning system.

The metagraph is a dynamic representation of the network’s state, capturing the interconnectedness and attributes of
    

neurons (participants) in the Bittensor ecosystem. This class is not just a static structure but a live reflection of the network, constantly updated and synchronized with the state of the blockchain.

In Bittensor, neurons are akin to nodes in a distributed system, each contributing computational resources and
    

participating in the network’s collective intelligence. The metagraph tracks various attributes of these neurons, such as stake, trust, and consensus, which are crucial for the network’s incentive mechanisms and the Yuma Consensus algorithm as outlined in the [NeurIPS paper](<https://bittensor.com/pdfs/academia/NeurIPS_DAO_Workshop_2022_3_3.pdf>). These attributes govern how neurons interact, how they are incentivized, and their roles within the network’s decision-making processes.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – A unique identifier that distinguishes between different instances or versions of the Bittensor network.

  * **network** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The name of the network, signifying specific configurations or iterations within the Bittensor ecosystem.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

  * **lite** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **sync** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **subtensor** (_Optional_ _[__Union_ _[_[_bittensor.core.async_subtensor.AsyncSubtensor_](<../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor") _,_[_bittensor.core.subtensor.Subtensor_](<../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor") _]__]_)



Variables:
    

  * **version** (_NDArray_) – The version number of the network, integral for tracking network updates.

  * **n** (_NDArray_) – The total number of neurons in the network, reflecting its size and complexity.

  * **block** (_NDArray_) – The current block number in the blockchain, crucial for synchronizing with the network’s latest state.

  * **stake** – Represents the cryptocurrency staked by neurons, impacting their influence and earnings within the network.

  * **ranks** – Neuron rankings as per the Yuma Consensus algorithm, influencing their incentive distribution and network authority.

  * **trust** – Scores indicating the reliability of neurons, mainly miners, within the network’s operational context.

  * **consensus** – Scores reflecting each neuron’s alignment with the network’s collective decisions.

  * **validator_trust** – Trust scores for validator neurons, crucial for network security and validation.

  * **incentive** – Rewards allocated to neurons, particularly miners, for their network contributions.

  * **emission** – The rate at which rewards are distributed to neurons.

  * **dividends** – Rewards received primarily by validators as part of the incentive mechanism.

  * **active** – Status indicating whether a neuron is actively participating in the network.

  * **last_update** – Timestamp of the latest update to a neuron’s data.

  * **validator_permit** – Indicates if a neuron is authorized to act as a validator.

  * **weights** – Inter-neuronal weights set by each neuron, influencing network dynamics.

  * **bonds** – Represents speculative investments by neurons in others, part of the reward mechanism.

  * **uids** – Unique identifiers for each neuron, essential for network operations.

  * **axons** (_List_) – Details about each neuron’s axon, critical for facilitating network communication.




The metagraph plays a pivotal role in Bittensor’s decentralized AI operations, influencing everything from data propagation to reward distribution. It embodies the principles of decentralized governance and collaborative intelligence, ensuring that the network remains adaptive, secure, and efficient.

Example

Initializing the metagraph to represent the current state of the Bittensor network:
[code] 
    from bittensor.core.metagraph import Metagraph
    metagraph = Metagraph(netuid=config.netuid, network=subtensor.network, sync=False)
    
[/code]

Synchronizing the metagraph with the network to reflect the latest state and neuron data:
[code] 
    metagraph.sync(subtensor=subtensor)
    
[/code]

Accessing metagraph properties to inform network interactions and decisions:
[code] 
    total_stake = metagraph.S
    neuron_ranks = metagraph.R
    neuron_incentives = metagraph.I
    axons = metagraph.axons
    neurons = metagraph.neurons
    
[/code]

Maintaining a local copy of hotkeys for querying and interacting with network entities:
[code] 
    hotkeys = deepcopy(metagraph.hotkeys)
    
[/code]

Initializes a new instance of the metagraph object, setting up the basic structure and parameters based on the provided arguments. This class doesn’t require installed Torch. This method is the entry point for creating a metagraph object, which is a central component in representing the state of the Bittensor network.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Subnet unique identifier.

  * **network** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The name of the network, which can indicate specific configurations or versions of the Bittensor

  * **network.**

  * **lite** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – A flag indicating whether to use a lite version of the metagraph. The lite version may contain less detailed information but can be quicker to initialize and sync.

  * **sync** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – A flag indicating whether to synchronize the metagraph with the network upon initialization. Synchronization involves updating the metagraph’s parameters to reflect the current state of the network.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Subnet mechanism unique identifier.

  * **subtensor** (_Optional_ _[__Union_ _[_[_bittensor.core.async_subtensor.AsyncSubtensor_](<../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor") _,_[_bittensor.core.subtensor.Subtensor_](<../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor") _]__]_)




Example

Initializing a metagraph object for the Bittensor network with a specific network UID:
[code] 
    from bittensor.core.metagraph import Metagraph
    
    metagraph = Metagraph(netuid=123, network="finney", lite=True, sync=True)
    
[/code]

active[#](<#bittensor.core.metagraph.NonTorchMetagraph.active> "Link to this definition")
    

alpha_stake: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.NonTorchMetagraph.alpha_stake> "Link to this definition")
    

block[#](<#bittensor.core.metagraph.NonTorchMetagraph.block> "Link to this definition")
    

bonds[#](<#bittensor.core.metagraph.NonTorchMetagraph.bonds> "Link to this definition")
    

consensus[#](<#bittensor.core.metagraph.NonTorchMetagraph.consensus> "Link to this definition")
    

dividends[#](<#bittensor.core.metagraph.NonTorchMetagraph.dividends> "Link to this definition")
    

emission[#](<#bittensor.core.metagraph.NonTorchMetagraph.emission> "Link to this definition")
    

incentive[#](<#bittensor.core.metagraph.NonTorchMetagraph.incentive> "Link to this definition")
    

last_update[#](<#bittensor.core.metagraph.NonTorchMetagraph.last_update> "Link to this definition")
    

load_from_path(_dir_path_)[#](<#bittensor.core.metagraph.NonTorchMetagraph.load_from_path> "Link to this definition")
    

Loads the state of the Metagraph from a specified directory path.

Parameters:
    

**dir_path** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The directory path where the metagraph’s state file is located.

Returns:
    

An instance of the Metagraph with the state loaded from the file.

Return type:
    

[metagraph](<../../extras/subtensor_api/metagraphs/index.html#bittensor.extras.subtensor_api.metagraphs.Metagraphs.metagraph> "bittensor.extras.subtensor_api.metagraphs.Metagraphs.metagraph")

Raises:
    

  * [**pickle.UnpicklingError**](<https://docs.python.org/3/library/pickle.html#pickle.UnpicklingError> "\(in Python v3.14\)") – If there is an error unpickling the state file.

  * [**RuntimeError**](<https://docs.python.org/3/library/exceptions.html#RuntimeError> "\(in Python v3.14\)") – If there is an error loading the state file using PyTorch.

  * [**ImportError**](<https://docs.python.org/3/library/exceptions.html#ImportError> "\(in Python v3.14\)") – If there is an error importing PyTorch.




n[#](<#bittensor.core.metagraph.NonTorchMetagraph.n> "Link to this definition")
    

netuid[#](<#bittensor.core.metagraph.NonTorchMetagraph.netuid> "Link to this definition")
    

should_sync = True[#](<#bittensor.core.metagraph.NonTorchMetagraph.should_sync> "Link to this definition")
    

stake: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.NonTorchMetagraph.stake> "Link to this definition")
    

subtensor = None[#](<#bittensor.core.metagraph.NonTorchMetagraph.subtensor> "Link to this definition")
    

tao_stake: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.NonTorchMetagraph.tao_stake> "Link to this definition")
    

total_stake: [Tensor](<../tensor/index.html#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")[#](<#bittensor.core.metagraph.NonTorchMetagraph.total_stake> "Link to this definition")
    

uids[#](<#bittensor.core.metagraph.NonTorchMetagraph.uids> "Link to this definition")
    

validator_permit[#](<#bittensor.core.metagraph.NonTorchMetagraph.validator_permit> "Link to this definition")
    

validator_trust[#](<#bittensor.core.metagraph.NonTorchMetagraph.validator_trust> "Link to this definition")
    

version[#](<#bittensor.core.metagraph.NonTorchMetagraph.version> "Link to this definition")
    

weights[#](<#bittensor.core.metagraph.NonTorchMetagraph.weights> "Link to this definition")
    

bittensor.core.metagraph.NumpyOrTorch[#](<#bittensor.core.metagraph.NumpyOrTorch> "Link to this definition")
    

bittensor.core.metagraph.Tensor[#](<#bittensor.core.metagraph.Tensor> "Link to this definition")
    

class bittensor.core.metagraph.TorchMetagraph(_netuid_ , _mechid =0_, _network =settings.DEFAULT_NETWORK_, _lite =True_, _sync =True_, _subtensor =None_)[#](<#bittensor.core.metagraph.TorchMetagraph> "Link to this definition")
    

Bases: [`MetagraphMixin`](<#bittensor.core.metagraph.MetagraphMixin> "bittensor.core.metagraph.MetagraphMixin"), [`BaseClass`](<#bittensor.core.metagraph.BaseClass> "bittensor.core.metagraph.BaseClass")

The metagraph class is a core component of the Bittensor network, representing the neural graph that forms the backbone of the decentralized machine learning system.

The metagraph is a dynamic representation of the network’s state, capturing the interconnectedness and attributes of
    

neurons (participants) in the Bittensor ecosystem. This class is not just a static structure but a live reflection of the network, constantly updated and synchronized with the state of the blockchain.

In Bittensor, neurons are akin to nodes in a distributed system, each contributing computational resources and
    

participating in the network’s collective intelligence. The metagraph tracks various attributes of these neurons, such as stake, trust, and consensus, which are crucial for the network’s incentive mechanisms and the Yuma Consensus algorithm as outlined in the [NeurIPS paper](<https://bittensor.com/pdfs/academia/NeurIPS_DAO_Workshop_2022_3_3.pdf>). These attributes govern how neurons interact, how they are incentivized, and their roles within the network’s decision-making processes.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – A unique identifier that distinguishes between different instances or versions of the Bittensor network.

  * **network** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The name of the network, signifying specific configurations or iterations within the Bittensor ecosystem.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

  * **lite** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **sync** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **subtensor** (_Optional_ _[__Union_ _[_[_bittensor.core.async_subtensor.AsyncSubtensor_](<../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor") _,_[_bittensor.core.subtensor.Subtensor_](<../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor") _]__]_)



Variables:
    

  * **version** (_NDArray_) – The version number of the network, integral for tracking network updates.

  * **n** (_NDArray_) – The total number of neurons in the network, reflecting its size and complexity.

  * **block** (_NDArray_) – The current block number in the blockchain, crucial for synchronizing with the network’s latest state.

  * **stake** – Represents the cryptocurrency staked by neurons, impacting their influence and earnings within the network.

  * **ranks** – Neuron rankings as per the Yuma Consensus algorithm, influencing their incentive distribution and network authority.

  * **trust** – Scores indicating the reliability of neurons, mainly miners, within the network’s operational context.

  * **consensus** – Scores reflecting each neuron’s alignment with the network’s collective decisions.

  * **validator_trust** – Trust scores for validator neurons, crucial for network security and validation.

  * **incentive** – Rewards allocated to neurons, particularly miners, for their network contributions.

  * **emission** – The rate at which rewards are distributed to neurons.

  * **dividends** – Rewards received primarily by validators as part of the incentive mechanism.

  * **active** – Status indicating whether a neuron is actively participating in the network.

  * **last_update** – Timestamp of the latest update to a neuron’s data.

  * **validator_permit** – Indicates if a neuron is authorized to act as a validator.

  * **weights** – Inter-neuronal weights set by each neuron, influencing network dynamics.

  * **bonds** – Represents speculative investments by neurons in others, part of the reward mechanism.

  * **uids** – Unique identifiers for each neuron, essential for network operations.

  * **axons** (_List_) – Details about each neuron’s axon, critical for facilitating network communication.




The metagraph plays a pivotal role in Bittensor’s decentralized AI operations, influencing everything from data propagation to reward distribution. It embodies the principles of decentralized governance and collaborative intelligence, ensuring that the network remains adaptive, secure, and efficient.

Example

Initializing the metagraph to represent the current state of the Bittensor network:
[code] 
    from bittensor.core.metagraph import Metagraph
    metagraph = Metagraph(netuid=config.netuid, network=subtensor.network, sync=False)
    
[/code]

Synchronizing the metagraph with the network to reflect the latest state and neuron data:
[code] 
    metagraph.sync(subtensor=subtensor)
    
[/code]

Accessing metagraph properties to inform network interactions and decisions:
[code] 
    total_stake = metagraph.S
    neuron_ranks = metagraph.R
    neuron_incentives = metagraph.I
    axons = metagraph.axons
    neurons = metagraph.neurons
    
[/code]

Maintaining a local copy of hotkeys for querying and interacting with network entities:
[code] 
    hotkeys = deepcopy(metagraph.hotkeys)
    
[/code]

Initializes a new instance of the metagraph object, setting up the basic structure and parameters based on the provided arguments. This class requires Torch to be installed. This method is the entry point for creating a metagraph object, which is a central component in representing the state of the Bittensor network.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Subnet unique identifier.

  * **network** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The name of the network, which can indicate specific configurations or versions of the Bittensor

  * **network.**

  * **lite** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – A flag indicating whether to use a lite version of the metagraph. The lite version may contain less detailed information but can be quicker to initialize and sync.

  * **sync** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – A flag indicating whether to synchronize the metagraph with the network upon initialization. Synchronization involves updating the metagraph’s parameters to reflect the current state of the network.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Subnet mechanism unique identifier.

  * **subtensor** (_Optional_ _[__Union_ _[_[_bittensor.core.async_subtensor.AsyncSubtensor_](<../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor") _,_[_bittensor.core.subtensor.Subtensor_](<../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor") _]__]_)




Example

Initializing a metagraph object for the Bittensor network with a specific network UID:

> from bittensor.core.metagraph import Metagraph
> 
> metagraph = Metagraph(netuid=123, network=”finney”, lite=True, sync=True)

active[#](<#bittensor.core.metagraph.TorchMetagraph.active> "Link to this definition")
    

alpha_stake[#](<#bittensor.core.metagraph.TorchMetagraph.alpha_stake> "Link to this definition")
    

block: bittensor.utils.registration.torch.nn.Parameter[#](<#bittensor.core.metagraph.TorchMetagraph.block> "Link to this definition")
    

bonds: bittensor.utils.registration.torch.nn.Parameter[#](<#bittensor.core.metagraph.TorchMetagraph.bonds> "Link to this definition")
    

consensus: bittensor.utils.registration.torch.nn.Parameter[#](<#bittensor.core.metagraph.TorchMetagraph.consensus> "Link to this definition")
    

dividends: bittensor.utils.registration.torch.nn.Parameter[#](<#bittensor.core.metagraph.TorchMetagraph.dividends> "Link to this definition")
    

emission: bittensor.utils.registration.torch.nn.Parameter[#](<#bittensor.core.metagraph.TorchMetagraph.emission> "Link to this definition")
    

incentive: bittensor.utils.registration.torch.nn.Parameter[#](<#bittensor.core.metagraph.TorchMetagraph.incentive> "Link to this definition")
    

last_update[#](<#bittensor.core.metagraph.TorchMetagraph.last_update> "Link to this definition")
    

load_from_path(_dir_path_)[#](<#bittensor.core.metagraph.TorchMetagraph.load_from_path> "Link to this definition")
    

Loads the metagraph state from a specified directory path.

Parameters:
    

**dir_path** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The directory path where the state file is located.

Returns:
    

The current metagraph instance with the loaded state.

Return type:
    

[metagraph](<../../extras/subtensor_api/metagraphs/index.html#bittensor.extras.subtensor_api.metagraphs.Metagraphs.metagraph> "bittensor.extras.subtensor_api.metagraphs.Metagraphs.metagraph")

Example

from bittensor.core.metagraph import Metagraph

netuid = 1 metagraph = Metagraph(netuid=netuid)

metagraph.load_from_path(“/path/to/dir”)

n: bittensor.utils.registration.torch.nn.Parameter[#](<#bittensor.core.metagraph.TorchMetagraph.n> "Link to this definition")
    

stake[#](<#bittensor.core.metagraph.TorchMetagraph.stake> "Link to this definition")
    

tao_stake[#](<#bittensor.core.metagraph.TorchMetagraph.tao_stake> "Link to this definition")
    

total_stake: bittensor.utils.registration.torch.nn.Parameter[#](<#bittensor.core.metagraph.TorchMetagraph.total_stake> "Link to this definition")
    

uids[#](<#bittensor.core.metagraph.TorchMetagraph.uids> "Link to this definition")
    

validator_permit[#](<#bittensor.core.metagraph.TorchMetagraph.validator_permit> "Link to this definition")
    

validator_trust: bittensor.utils.registration.torch.nn.Parameter[#](<#bittensor.core.metagraph.TorchMetagraph.validator_trust> "Link to this definition")
    

version[#](<#bittensor.core.metagraph.TorchMetagraph.version> "Link to this definition")
    

weights: bittensor.utils.registration.torch.nn.Parameter[#](<#bittensor.core.metagraph.TorchMetagraph.weights> "Link to this definition")
    

async bittensor.core.metagraph.async_metagraph(_netuid_ , _mechid =0_, _network =settings.DEFAULT_NETWORK_, _lite =True_, _sync =True_, _subtensor =None_)[#](<#bittensor.core.metagraph.async_metagraph> "Link to this definition")
    

Factory function to create an instantiated AsyncMetagraph, mainly for the ability to use sync at instantiation.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid of the subnet for which to create the AsyncMetagraph.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The mechid of the subnet for which to create the AsyncMetagraph.

  * **network** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The network to use for the AsyncMetagraph.

  * **lite** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to use a lite version of the AsyncMetagraph.

  * **sync** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to sync the AsyncMetagraph.

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – The subtensor to use for the AsyncMetagraph.



Returns:
    

The instantiated AsyncMetagraph.

Return type:
    

[AsyncMetagraph](<#bittensor.core.metagraph.AsyncMetagraph> "bittensor.core.metagraph.AsyncMetagraph")

bittensor.core.metagraph.get_save_dir(_network_ , _netuid_ , _root_dir =None_)[#](<#bittensor.core.metagraph.get_save_dir> "Link to this definition")
    

Returns a directory path given `network` and `netuid` inputs.

Parameters:
    

  * **network** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – Network name.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Network UID.

  * **root_dir** (_Optional_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]__]_) – list to the file path for the root directory of your metagraph saves (i.e. [‘/’, ‘tmp’, ‘metagraphs’], defaults to [“~”, “.bittensor”, “metagraphs”]



Returns:
    

Directory path.

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

bittensor.core.metagraph.latest_block_path(_dir_path_)[#](<#bittensor.core.metagraph.latest_block_path> "Link to this definition")
    

Get the latest block path from the provided directory path.

Parameters:
    

**dir_path** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – Directory path.

Returns:
    

Latest block path.

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

bittensor.core.metagraph.safe_globals()[#](<#bittensor.core.metagraph.safe_globals> "Link to this definition")
    

Context manager to load torch files for version 2.6+

[ __ previous bittensor.core.extrinsics.weights ](<../extrinsics/weights/index.html> "previous page") [ next bittensor.core.settings __](<../settings/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`AsyncMetagraph`](<#bittensor.core.metagraph.AsyncMetagraph>)
      * [`AsyncMetagraph.sync()`](<#bittensor.core.metagraph.AsyncMetagraph.sync>)
    * [`BaseClass`](<#bittensor.core.metagraph.BaseClass>)
    * [`METAGRAPH_STATE_DICT_NDARRAY_KEYS`](<#bittensor.core.metagraph.METAGRAPH_STATE_DICT_NDARRAY_KEYS>)
    * [`Metagraph`](<#bittensor.core.metagraph.Metagraph>)
      * [`Metagraph.sync()`](<#bittensor.core.metagraph.Metagraph.sync>)
    * [`MetagraphMixin`](<#bittensor.core.metagraph.MetagraphMixin>)
      * [`MetagraphMixin.AS`](<#bittensor.core.metagraph.MetagraphMixin.AS>)
      * [`MetagraphMixin.B`](<#bittensor.core.metagraph.MetagraphMixin.B>)
      * [`MetagraphMixin.C`](<#bittensor.core.metagraph.MetagraphMixin.C>)
      * [`MetagraphMixin.D`](<#bittensor.core.metagraph.MetagraphMixin.D>)
      * [`MetagraphMixin.E`](<#bittensor.core.metagraph.MetagraphMixin.E>)
      * [`MetagraphMixin.I`](<#bittensor.core.metagraph.MetagraphMixin.I>)
      * [`MetagraphMixin.S`](<#bittensor.core.metagraph.MetagraphMixin.S>)
      * [`MetagraphMixin.TS`](<#bittensor.core.metagraph.MetagraphMixin.TS>)
      * [`MetagraphMixin.Tv`](<#bittensor.core.metagraph.MetagraphMixin.Tv>)
      * [`MetagraphMixin.W`](<#bittensor.core.metagraph.MetagraphMixin.W>)
      * [`MetagraphMixin.active`](<#bittensor.core.metagraph.MetagraphMixin.active>)
      * [`MetagraphMixin.addresses`](<#bittensor.core.metagraph.MetagraphMixin.addresses>)
      * [`MetagraphMixin.alpha_dividends_per_hotkey`](<#bittensor.core.metagraph.MetagraphMixin.alpha_dividends_per_hotkey>)
      * [`MetagraphMixin.alpha_stake`](<#bittensor.core.metagraph.MetagraphMixin.alpha_stake>)
      * [`MetagraphMixin.axons`](<#bittensor.core.metagraph.MetagraphMixin.axons>)
      * [`MetagraphMixin.block`](<#bittensor.core.metagraph.MetagraphMixin.block>)
      * [`MetagraphMixin.block_at_registration`](<#bittensor.core.metagraph.MetagraphMixin.block_at_registration>)
      * [`MetagraphMixin.blocks_since_last_step`](<#bittensor.core.metagraph.MetagraphMixin.blocks_since_last_step>)
      * [`MetagraphMixin.bonds`](<#bittensor.core.metagraph.MetagraphMixin.bonds>)
      * [`MetagraphMixin.chain_endpoint`](<#bittensor.core.metagraph.MetagraphMixin.chain_endpoint>)
      * [`MetagraphMixin.coldkeys`](<#bittensor.core.metagraph.MetagraphMixin.coldkeys>)
      * [`MetagraphMixin.consensus`](<#bittensor.core.metagraph.MetagraphMixin.consensus>)
      * [`MetagraphMixin.dividends`](<#bittensor.core.metagraph.MetagraphMixin.dividends>)
      * [`MetagraphMixin.emission`](<#bittensor.core.metagraph.MetagraphMixin.emission>)
      * [`MetagraphMixin.emissions`](<#bittensor.core.metagraph.MetagraphMixin.emissions>)
      * [`MetagraphMixin.hotkeys`](<#bittensor.core.metagraph.MetagraphMixin.hotkeys>)
      * [`MetagraphMixin.hparams`](<#bittensor.core.metagraph.MetagraphMixin.hparams>)
      * [`MetagraphMixin.identities`](<#bittensor.core.metagraph.MetagraphMixin.identities>)
      * [`MetagraphMixin.identity`](<#bittensor.core.metagraph.MetagraphMixin.identity>)
      * [`MetagraphMixin.incentive`](<#bittensor.core.metagraph.MetagraphMixin.incentive>)
      * [`MetagraphMixin.last_step`](<#bittensor.core.metagraph.MetagraphMixin.last_step>)
      * [`MetagraphMixin.last_update`](<#bittensor.core.metagraph.MetagraphMixin.last_update>)
      * [`MetagraphMixin.lite`](<#bittensor.core.metagraph.MetagraphMixin.lite>)
      * [`MetagraphMixin.load()`](<#bittensor.core.metagraph.MetagraphMixin.load>)
      * [`MetagraphMixin.load_from_path()`](<#bittensor.core.metagraph.MetagraphMixin.load_from_path>)
      * [`MetagraphMixin.max_uids`](<#bittensor.core.metagraph.MetagraphMixin.max_uids>)
      * [`MetagraphMixin.mechanism_count`](<#bittensor.core.metagraph.MetagraphMixin.mechanism_count>)
      * [`MetagraphMixin.mechanisms_emissions_split`](<#bittensor.core.metagraph.MetagraphMixin.mechanisms_emissions_split>)
      * [`MetagraphMixin.mechid`](<#bittensor.core.metagraph.MetagraphMixin.mechid>)
      * [`MetagraphMixin.metadata()`](<#bittensor.core.metagraph.MetagraphMixin.metadata>)
      * [`MetagraphMixin.n`](<#bittensor.core.metagraph.MetagraphMixin.n>)
      * [`MetagraphMixin.name`](<#bittensor.core.metagraph.MetagraphMixin.name>)
      * [`MetagraphMixin.netuid`](<#bittensor.core.metagraph.MetagraphMixin.netuid>)
      * [`MetagraphMixin.network`](<#bittensor.core.metagraph.MetagraphMixin.network>)
      * [`MetagraphMixin.network_registered_at`](<#bittensor.core.metagraph.MetagraphMixin.network_registered_at>)
      * [`MetagraphMixin.neurons`](<#bittensor.core.metagraph.MetagraphMixin.neurons>)
      * [`MetagraphMixin.num_uids`](<#bittensor.core.metagraph.MetagraphMixin.num_uids>)
      * [`MetagraphMixin.owner_coldkey`](<#bittensor.core.metagraph.MetagraphMixin.owner_coldkey>)
      * [`MetagraphMixin.owner_hotkey`](<#bittensor.core.metagraph.MetagraphMixin.owner_hotkey>)
      * [`MetagraphMixin.pool`](<#bittensor.core.metagraph.MetagraphMixin.pool>)
      * [`MetagraphMixin.pruning_score`](<#bittensor.core.metagraph.MetagraphMixin.pruning_score>)
      * [`MetagraphMixin.ranks`](<#bittensor.core.metagraph.MetagraphMixin.ranks>)
      * [`MetagraphMixin.save()`](<#bittensor.core.metagraph.MetagraphMixin.save>)
      * [`MetagraphMixin.should_sync`](<#bittensor.core.metagraph.MetagraphMixin.should_sync>)
      * [`MetagraphMixin.stake`](<#bittensor.core.metagraph.MetagraphMixin.stake>)
      * [`MetagraphMixin.state_dict()`](<#bittensor.core.metagraph.MetagraphMixin.state_dict>)
      * [`MetagraphMixin.subtensor`](<#bittensor.core.metagraph.MetagraphMixin.subtensor>)
      * [`MetagraphMixin.symbol`](<#bittensor.core.metagraph.MetagraphMixin.symbol>)
      * [`MetagraphMixin.tao_dividends_per_hotkey`](<#bittensor.core.metagraph.MetagraphMixin.tao_dividends_per_hotkey>)
      * [`MetagraphMixin.tao_stake`](<#bittensor.core.metagraph.MetagraphMixin.tao_stake>)
      * [`MetagraphMixin.tempo`](<#bittensor.core.metagraph.MetagraphMixin.tempo>)
      * [`MetagraphMixin.trust`](<#bittensor.core.metagraph.MetagraphMixin.trust>)
      * [`MetagraphMixin.uids`](<#bittensor.core.metagraph.MetagraphMixin.uids>)
      * [`MetagraphMixin.validator_permit`](<#bittensor.core.metagraph.MetagraphMixin.validator_permit>)
      * [`MetagraphMixin.validator_trust`](<#bittensor.core.metagraph.MetagraphMixin.validator_trust>)
      * [`MetagraphMixin.version`](<#bittensor.core.metagraph.MetagraphMixin.version>)
      * [`MetagraphMixin.weights`](<#bittensor.core.metagraph.MetagraphMixin.weights>)
    * [`NonTorchMetagraph`](<#bittensor.core.metagraph.NonTorchMetagraph>)
      * [`NonTorchMetagraph.active`](<#bittensor.core.metagraph.NonTorchMetagraph.active>)
      * [`NonTorchMetagraph.alpha_stake`](<#bittensor.core.metagraph.NonTorchMetagraph.alpha_stake>)
      * [`NonTorchMetagraph.block`](<#bittensor.core.metagraph.NonTorchMetagraph.block>)
      * [`NonTorchMetagraph.bonds`](<#bittensor.core.metagraph.NonTorchMetagraph.bonds>)
      * [`NonTorchMetagraph.consensus`](<#bittensor.core.metagraph.NonTorchMetagraph.consensus>)
      * [`NonTorchMetagraph.dividends`](<#bittensor.core.metagraph.NonTorchMetagraph.dividends>)
      * [`NonTorchMetagraph.emission`](<#bittensor.core.metagraph.NonTorchMetagraph.emission>)
      * [`NonTorchMetagraph.incentive`](<#bittensor.core.metagraph.NonTorchMetagraph.incentive>)
      * [`NonTorchMetagraph.last_update`](<#bittensor.core.metagraph.NonTorchMetagraph.last_update>)
      * [`NonTorchMetagraph.load_from_path()`](<#bittensor.core.metagraph.NonTorchMetagraph.load_from_path>)
      * [`NonTorchMetagraph.n`](<#bittensor.core.metagraph.NonTorchMetagraph.n>)
      * [`NonTorchMetagraph.netuid`](<#bittensor.core.metagraph.NonTorchMetagraph.netuid>)
      * [`NonTorchMetagraph.should_sync`](<#bittensor.core.metagraph.NonTorchMetagraph.should_sync>)
      * [`NonTorchMetagraph.stake`](<#bittensor.core.metagraph.NonTorchMetagraph.stake>)
      * [`NonTorchMetagraph.subtensor`](<#bittensor.core.metagraph.NonTorchMetagraph.subtensor>)
      * [`NonTorchMetagraph.tao_stake`](<#bittensor.core.metagraph.NonTorchMetagraph.tao_stake>)
      * [`NonTorchMetagraph.total_stake`](<#bittensor.core.metagraph.NonTorchMetagraph.total_stake>)
      * [`NonTorchMetagraph.uids`](<#bittensor.core.metagraph.NonTorchMetagraph.uids>)
      * [`NonTorchMetagraph.validator_permit`](<#bittensor.core.metagraph.NonTorchMetagraph.validator_permit>)
      * [`NonTorchMetagraph.validator_trust`](<#bittensor.core.metagraph.NonTorchMetagraph.validator_trust>)
      * [`NonTorchMetagraph.version`](<#bittensor.core.metagraph.NonTorchMetagraph.version>)
      * [`NonTorchMetagraph.weights`](<#bittensor.core.metagraph.NonTorchMetagraph.weights>)
    * [`NumpyOrTorch`](<#bittensor.core.metagraph.NumpyOrTorch>)
    * [`Tensor`](<#bittensor.core.metagraph.Tensor>)
    * [`TorchMetagraph`](<#bittensor.core.metagraph.TorchMetagraph>)
      * [`TorchMetagraph.active`](<#bittensor.core.metagraph.TorchMetagraph.active>)
      * [`TorchMetagraph.alpha_stake`](<#bittensor.core.metagraph.TorchMetagraph.alpha_stake>)
      * [`TorchMetagraph.block`](<#bittensor.core.metagraph.TorchMetagraph.block>)
      * [`TorchMetagraph.bonds`](<#bittensor.core.metagraph.TorchMetagraph.bonds>)
      * [`TorchMetagraph.consensus`](<#bittensor.core.metagraph.TorchMetagraph.consensus>)
      * [`TorchMetagraph.dividends`](<#bittensor.core.metagraph.TorchMetagraph.dividends>)
      * [`TorchMetagraph.emission`](<#bittensor.core.metagraph.TorchMetagraph.emission>)
      * [`TorchMetagraph.incentive`](<#bittensor.core.metagraph.TorchMetagraph.incentive>)
      * [`TorchMetagraph.last_update`](<#bittensor.core.metagraph.TorchMetagraph.last_update>)
      * [`TorchMetagraph.load_from_path()`](<#bittensor.core.metagraph.TorchMetagraph.load_from_path>)
      * [`TorchMetagraph.n`](<#bittensor.core.metagraph.TorchMetagraph.n>)
      * [`TorchMetagraph.stake`](<#bittensor.core.metagraph.TorchMetagraph.stake>)
      * [`TorchMetagraph.tao_stake`](<#bittensor.core.metagraph.TorchMetagraph.tao_stake>)
      * [`TorchMetagraph.total_stake`](<#bittensor.core.metagraph.TorchMetagraph.total_stake>)
      * [`TorchMetagraph.uids`](<#bittensor.core.metagraph.TorchMetagraph.uids>)
      * [`TorchMetagraph.validator_permit`](<#bittensor.core.metagraph.TorchMetagraph.validator_permit>)
      * [`TorchMetagraph.validator_trust`](<#bittensor.core.metagraph.TorchMetagraph.validator_trust>)
      * [`TorchMetagraph.version`](<#bittensor.core.metagraph.TorchMetagraph.version>)
      * [`TorchMetagraph.weights`](<#bittensor.core.metagraph.TorchMetagraph.weights>)
    * [`async_metagraph()`](<#bittensor.core.metagraph.async_metagraph>)
    * [`get_save_dir()`](<#bittensor.core.metagraph.get_save_dir>)
    * [`latest_block_path()`](<#bittensor.core.metagraph.latest_block_path>)
    * [`safe_globals()`](<#bittensor.core.metagraph.safe_globals>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.