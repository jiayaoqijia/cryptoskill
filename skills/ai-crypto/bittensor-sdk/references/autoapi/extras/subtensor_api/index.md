# bittensor.extras.subtensor_api &#8212; Bittensor SDK Docs  documentation

[Skip to main content](<#main-content>)

__Back to top __ `Ctrl`+`K`

[ ![Bittensor SDK Docs  documentation - Home](../../../../_static/logo.svg) ![Bittensor SDK Docs  documentation - Home](../../../../_static/logo-dark-mode.svg) ](<../../../../index.html>)

__ Search `Ctrl`+`K`

Table of Contents

  * [API Reference](<../../../index.html>) __
    * [bittensor](<../../index.html>) __
      * [bittensor.core](<../../core/index.html>) __
        * [bittensor.core.async_subtensor](<../../core/async_subtensor/index.html>)
        * [bittensor.core.axon](<../../core/axon/index.html>)
        * [bittensor.core.chain_data](<../../core/chain_data/index.html>)
        * [bittensor.core.config](<../../core/config/index.html>)
        * [bittensor.core.dendrite](<../../core/dendrite/index.html>)
        * [bittensor.core.errors](<../../core/errors/index.html>)
        * [bittensor.core.extrinsics](<../../core/extrinsics/index.html>)
        * [bittensor.core.metagraph](<../../core/metagraph/index.html>)
        * [bittensor.core.settings](<../../core/settings/index.html>)
        * [bittensor.core.stream](<../../core/stream/index.html>)
        * [bittensor.core.subtensor](<../../core/subtensor/index.html>)
        * [bittensor.core.synapse](<../../core/synapse/index.html>)
        * [bittensor.core.tensor](<../../core/tensor/index.html>)
        * [bittensor.core.threadpool](<../../core/threadpool/index.html>)
        * [bittensor.core.types](<../../core/types/index.html>)
      * [bittensor.extras](<../index.html>) __
        * [bittensor.extras.dev_framework](<../dev_framework/index.html>)
        * [bittensor.extras.subtensor_api](<#>)
        * [bittensor.extras.timelock](<../timelock/index.html>)
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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/extras/subtensor_api/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/extras/subtensor_api/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/extras/subtensor_api/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.extras.subtensor_api

##  Contents 

  * [Submodules](<#submodules>)
  * [Classes](<#classes>)
  * [Package Contents](<#package-contents>)
    * [`SubtensorApi`](<#bittensor.extras.subtensor_api.SubtensorApi>)
      * [`SubtensorApi.add_args()`](<#bittensor.extras.subtensor_api.SubtensorApi.add_args>)
      * [`SubtensorApi.block`](<#bittensor.extras.subtensor_api.SubtensorApi.block>)
      * [`SubtensorApi.chain`](<#bittensor.extras.subtensor_api.SubtensorApi.chain>)
      * [`SubtensorApi.chain_endpoint`](<#bittensor.extras.subtensor_api.SubtensorApi.chain_endpoint>)
      * [`SubtensorApi.close`](<#bittensor.extras.subtensor_api.SubtensorApi.close>)
      * [`SubtensorApi.commitments`](<#bittensor.extras.subtensor_api.SubtensorApi.commitments>)
      * [`SubtensorApi.compose_call`](<#bittensor.extras.subtensor_api.SubtensorApi.compose_call>)
      * [`SubtensorApi.config`](<#bittensor.extras.subtensor_api.SubtensorApi.config>)
      * [`SubtensorApi.crowdloans`](<#bittensor.extras.subtensor_api.SubtensorApi.crowdloans>)
      * [`SubtensorApi.delegates`](<#bittensor.extras.subtensor_api.SubtensorApi.delegates>)
      * [`SubtensorApi.determine_block_hash`](<#bittensor.extras.subtensor_api.SubtensorApi.determine_block_hash>)
      * [`SubtensorApi.extrinsics`](<#bittensor.extras.subtensor_api.SubtensorApi.extrinsics>)
      * [`SubtensorApi.help`](<#bittensor.extras.subtensor_api.SubtensorApi.help>)
      * [`SubtensorApi.initialize`](<#bittensor.extras.subtensor_api.SubtensorApi.initialize>)
      * [`SubtensorApi.inner_subtensor`](<#bittensor.extras.subtensor_api.SubtensorApi.inner_subtensor>)
      * [`SubtensorApi.is_async`](<#bittensor.extras.subtensor_api.SubtensorApi.is_async>)
      * [`SubtensorApi.log_verbose`](<#bittensor.extras.subtensor_api.SubtensorApi.log_verbose>)
      * [`SubtensorApi.metagraphs`](<#bittensor.extras.subtensor_api.SubtensorApi.metagraphs>)
      * [`SubtensorApi.mev_shield`](<#bittensor.extras.subtensor_api.SubtensorApi.mev_shield>)
      * [`SubtensorApi.network`](<#bittensor.extras.subtensor_api.SubtensorApi.network>)
      * [`SubtensorApi.neurons`](<#bittensor.extras.subtensor_api.SubtensorApi.neurons>)
      * [`SubtensorApi.proxies`](<#bittensor.extras.subtensor_api.SubtensorApi.proxies>)
      * [`SubtensorApi.queries`](<#bittensor.extras.subtensor_api.SubtensorApi.queries>)
      * [`SubtensorApi.setup_config`](<#bittensor.extras.subtensor_api.SubtensorApi.setup_config>)
      * [`SubtensorApi.sign_and_send_extrinsic`](<#bittensor.extras.subtensor_api.SubtensorApi.sign_and_send_extrinsic>)
      * [`SubtensorApi.staking`](<#bittensor.extras.subtensor_api.SubtensorApi.staking>)
      * [`SubtensorApi.start_call`](<#bittensor.extras.subtensor_api.SubtensorApi.start_call>)
      * [`SubtensorApi.subnets`](<#bittensor.extras.subtensor_api.SubtensorApi.subnets>)
      * [`SubtensorApi.substrate`](<#bittensor.extras.subtensor_api.SubtensorApi.substrate>)
      * [`SubtensorApi.wait_for_block`](<#bittensor.extras.subtensor_api.SubtensorApi.wait_for_block>)
      * [`SubtensorApi.wallets`](<#bittensor.extras.subtensor_api.SubtensorApi.wallets>)



# bittensor.extras.subtensor_api[#](<#module-bittensor.extras.subtensor_api> "Link to this heading")

## Submodules[#](<#submodules> "Link to this heading")

  * [bittensor.extras.subtensor_api.chain](<chain/index.html>)
  * [bittensor.extras.subtensor_api.commitments](<commitments/index.html>)
  * [bittensor.extras.subtensor_api.crowdloans](<crowdloans/index.html>)
  * [bittensor.extras.subtensor_api.delegates](<delegates/index.html>)
  * [bittensor.extras.subtensor_api.extrinsics](<extrinsics/index.html>)
  * [bittensor.extras.subtensor_api.metagraphs](<metagraphs/index.html>)
  * [bittensor.extras.subtensor_api.mev_shield](<mev_shield/index.html>)
  * [bittensor.extras.subtensor_api.neurons](<neurons/index.html>)
  * [bittensor.extras.subtensor_api.proxy](<proxy/index.html>)
  * [bittensor.extras.subtensor_api.queries](<queries/index.html>)
  * [bittensor.extras.subtensor_api.staking](<staking/index.html>)
  * [bittensor.extras.subtensor_api.subnets](<subnets/index.html>)
  * [bittensor.extras.subtensor_api.utils](<utils/index.html>)
  * [bittensor.extras.subtensor_api.wallets](<wallets/index.html>)



## Classes[#](<#classes> "Link to this heading")

[`SubtensorApi`](<#bittensor.extras.subtensor_api.SubtensorApi> "bittensor.extras.subtensor_api.SubtensorApi") | Subtensor API class.  
---|---  
  
## Package Contents[#](<#package-contents> "Link to this heading")

class bittensor.extras.subtensor_api.SubtensorApi(_network =None_, _config =None_, _async_subtensor =False_, _legacy_methods =False_, _fallback_endpoints =None_, _retry_forever =False_, _log_verbose =False_, _mock =False_, _archive_endpoints =None_, _websocket_shutdown_timer =5.0_)[#](<#bittensor.extras.subtensor_api.SubtensorApi> "Link to this definition")
    

Subtensor API class.

Parameters:
    

  * **network** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The network to connect to.

  * **config** (_Optional_ _[_[_bittensor.core.config.Config_](<../../core/config/index.html#bittensor.core.config.Config> "bittensor.core.config.Config") _]_) – Bittensor configuration object.

  * **legacy_methods** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, all methods from the Subtensor class will be added to the root level of this class.

  * **fallback_endpoints** (_Optional_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]__]_) – List of fallback endpoints to use if default or provided network is not available.

  * **retry_forever** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to retry forever on connection errors.

  * **log_verbose** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Enables or disables verbose logging.

  * **mock** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether this is a mock instance. Mainly just for use in testing.

  * **archive_endpoints** (_Optional_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]__]_) – Similar to fallback_endpoints, but specifically only archive nodes. Will be used in cases where you are requesting a block that is too old for your current (presumably lite) node.

  * **websocket_shutdown_timer** (_Optional_ _[_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _]_) – Amount of time, in seconds, to wait after the last response from the chain to close the connection. Only applicable to AsyncSubtensor. If None is passed to this, the automatic shutdown process is disabled.

  * **async_subtensor** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))




Example

# sync version import bittensor as bt

subtensor = bt.SubtensorApi() print(subtensor.block) print(subtensor.delegates.get_delegate_identities()) subtensor.chain.tx_rate_limit()

# async version import bittensor as bt

subtensor = bt.SubtensorApi(async_subtensor=True) async with subtensor:

> print(await subtensor.block) print(await subtensor.delegates.get_delegate_identities()) print(await subtensor.chain.tx_rate_limit())

# using legacy_methods import bittensor as bt

subtensor = bt.SubtensorApi(legacy_methods=True) print(subtensor.bonds(0))

# using fallback_endpoints or retry_forever import bittensor as bt

subtensor = bt.SubtensorApi(
    

network=”finney”, fallback_endpoints=[“wss://localhost:9945”, “wss://some-other-endpoint:9945”], retry_forever=True,

) print(subtensor.block)

classmethod add_args(_parser_)[#](<#bittensor.extras.subtensor_api.SubtensorApi.add_args> "Link to this definition")
    

property block[#](<#bittensor.extras.subtensor_api.SubtensorApi.block> "Link to this definition")
    

Returns current chain block number.

property chain[#](<#bittensor.extras.subtensor_api.SubtensorApi.chain> "Link to this definition")
    

Property of interaction with chain methods.

chain_endpoint = None[#](<#bittensor.extras.subtensor_api.SubtensorApi.chain_endpoint> "Link to this definition")
    

close[#](<#bittensor.extras.subtensor_api.SubtensorApi.close> "Link to this definition")
    

property commitments[#](<#bittensor.extras.subtensor_api.SubtensorApi.commitments> "Link to this definition")
    

Property to access commitments methods.

compose_call[#](<#bittensor.extras.subtensor_api.SubtensorApi.compose_call> "Link to this definition")
    

config[#](<#bittensor.extras.subtensor_api.SubtensorApi.config> "Link to this definition")
    

property crowdloans[#](<#bittensor.extras.subtensor_api.SubtensorApi.crowdloans> "Link to this definition")
    

Property to access crowdloans methods.

property delegates[#](<#bittensor.extras.subtensor_api.SubtensorApi.delegates> "Link to this definition")
    

Property to access delegates methods.

determine_block_hash[#](<#bittensor.extras.subtensor_api.SubtensorApi.determine_block_hash> "Link to this definition")
    

property extrinsics[#](<#bittensor.extras.subtensor_api.SubtensorApi.extrinsics> "Link to this definition")
    

Property to access extrinsics methods.

help[#](<#bittensor.extras.subtensor_api.SubtensorApi.help> "Link to this definition")
    

initialize = None[#](<#bittensor.extras.subtensor_api.SubtensorApi.initialize> "Link to this definition")
    

inner_subtensor[#](<#bittensor.extras.subtensor_api.SubtensorApi.inner_subtensor> "Link to this definition")
    

is_async = False[#](<#bittensor.extras.subtensor_api.SubtensorApi.is_async> "Link to this definition")
    

log_verbose = False[#](<#bittensor.extras.subtensor_api.SubtensorApi.log_verbose> "Link to this definition")
    

property metagraphs[#](<#bittensor.extras.subtensor_api.SubtensorApi.metagraphs> "Link to this definition")
    

Property to access metagraphs methods.

property mev_shield[#](<#bittensor.extras.subtensor_api.SubtensorApi.mev_shield> "Link to this definition")
    

Property to access MEV Shield methods.

network = None[#](<#bittensor.extras.subtensor_api.SubtensorApi.network> "Link to this definition")
    

property neurons[#](<#bittensor.extras.subtensor_api.SubtensorApi.neurons> "Link to this definition")
    

Property to access neurons methods.

property proxies[#](<#bittensor.extras.subtensor_api.SubtensorApi.proxies> "Link to this definition")
    

Property to access subtensor proxy methods.

property queries[#](<#bittensor.extras.subtensor_api.SubtensorApi.queries> "Link to this definition")
    

Property to access subtensor queries methods.

setup_config[#](<#bittensor.extras.subtensor_api.SubtensorApi.setup_config> "Link to this definition")
    

sign_and_send_extrinsic[#](<#bittensor.extras.subtensor_api.SubtensorApi.sign_and_send_extrinsic> "Link to this definition")
    

property staking[#](<#bittensor.extras.subtensor_api.SubtensorApi.staking> "Link to this definition")
    

Property to access staking methods.

start_call[#](<#bittensor.extras.subtensor_api.SubtensorApi.start_call> "Link to this definition")
    

property subnets[#](<#bittensor.extras.subtensor_api.SubtensorApi.subnets> "Link to this definition")
    

Property of interaction with subnets methods.

substrate[#](<#bittensor.extras.subtensor_api.SubtensorApi.substrate> "Link to this definition")
    

wait_for_block[#](<#bittensor.extras.subtensor_api.SubtensorApi.wait_for_block> "Link to this definition")
    

property wallets[#](<#bittensor.extras.subtensor_api.SubtensorApi.wallets> "Link to this definition")
    

Property of interaction methods with cold/hotkeys, and balances, etc.

[ __ previous bittensor.extras.dev_framework.utils ](<../dev_framework/utils/index.html> "previous page") [ next bittensor.extras.subtensor_api.chain __](<chain/index.html> "next page")

__Contents

  * [Submodules](<#submodules>)
  * [Classes](<#classes>)
  * [Package Contents](<#package-contents>)
    * [`SubtensorApi`](<#bittensor.extras.subtensor_api.SubtensorApi>)
      * [`SubtensorApi.add_args()`](<#bittensor.extras.subtensor_api.SubtensorApi.add_args>)
      * [`SubtensorApi.block`](<#bittensor.extras.subtensor_api.SubtensorApi.block>)
      * [`SubtensorApi.chain`](<#bittensor.extras.subtensor_api.SubtensorApi.chain>)
      * [`SubtensorApi.chain_endpoint`](<#bittensor.extras.subtensor_api.SubtensorApi.chain_endpoint>)
      * [`SubtensorApi.close`](<#bittensor.extras.subtensor_api.SubtensorApi.close>)
      * [`SubtensorApi.commitments`](<#bittensor.extras.subtensor_api.SubtensorApi.commitments>)
      * [`SubtensorApi.compose_call`](<#bittensor.extras.subtensor_api.SubtensorApi.compose_call>)
      * [`SubtensorApi.config`](<#bittensor.extras.subtensor_api.SubtensorApi.config>)
      * [`SubtensorApi.crowdloans`](<#bittensor.extras.subtensor_api.SubtensorApi.crowdloans>)
      * [`SubtensorApi.delegates`](<#bittensor.extras.subtensor_api.SubtensorApi.delegates>)
      * [`SubtensorApi.determine_block_hash`](<#bittensor.extras.subtensor_api.SubtensorApi.determine_block_hash>)
      * [`SubtensorApi.extrinsics`](<#bittensor.extras.subtensor_api.SubtensorApi.extrinsics>)
      * [`SubtensorApi.help`](<#bittensor.extras.subtensor_api.SubtensorApi.help>)
      * [`SubtensorApi.initialize`](<#bittensor.extras.subtensor_api.SubtensorApi.initialize>)
      * [`SubtensorApi.inner_subtensor`](<#bittensor.extras.subtensor_api.SubtensorApi.inner_subtensor>)
      * [`SubtensorApi.is_async`](<#bittensor.extras.subtensor_api.SubtensorApi.is_async>)
      * [`SubtensorApi.log_verbose`](<#bittensor.extras.subtensor_api.SubtensorApi.log_verbose>)
      * [`SubtensorApi.metagraphs`](<#bittensor.extras.subtensor_api.SubtensorApi.metagraphs>)
      * [`SubtensorApi.mev_shield`](<#bittensor.extras.subtensor_api.SubtensorApi.mev_shield>)
      * [`SubtensorApi.network`](<#bittensor.extras.subtensor_api.SubtensorApi.network>)
      * [`SubtensorApi.neurons`](<#bittensor.extras.subtensor_api.SubtensorApi.neurons>)
      * [`SubtensorApi.proxies`](<#bittensor.extras.subtensor_api.SubtensorApi.proxies>)
      * [`SubtensorApi.queries`](<#bittensor.extras.subtensor_api.SubtensorApi.queries>)
      * [`SubtensorApi.setup_config`](<#bittensor.extras.subtensor_api.SubtensorApi.setup_config>)
      * [`SubtensorApi.sign_and_send_extrinsic`](<#bittensor.extras.subtensor_api.SubtensorApi.sign_and_send_extrinsic>)
      * [`SubtensorApi.staking`](<#bittensor.extras.subtensor_api.SubtensorApi.staking>)
      * [`SubtensorApi.start_call`](<#bittensor.extras.subtensor_api.SubtensorApi.start_call>)
      * [`SubtensorApi.subnets`](<#bittensor.extras.subtensor_api.SubtensorApi.subnets>)
      * [`SubtensorApi.substrate`](<#bittensor.extras.subtensor_api.SubtensorApi.substrate>)
      * [`SubtensorApi.wait_for_block`](<#bittensor.extras.subtensor_api.SubtensorApi.wait_for_block>)
      * [`SubtensorApi.wallets`](<#bittensor.extras.subtensor_api.SubtensorApi.wallets>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.