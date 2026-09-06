# bittensor.utils.subnets &#8212; Bittensor SDK Docs  documentation

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
      * [bittensor.extras](<../../extras/index.html>) __
        * [bittensor.extras.dev_framework](<../../extras/dev_framework/index.html>)
        * [bittensor.extras.subtensor_api](<../../extras/subtensor_api/index.html>)
        * [bittensor.extras.timelock](<../../extras/timelock/index.html>)
      * [bittensor.utils](<../index.html>) __
        * [bittensor.utils.axon_utils](<../axon_utils/index.html>)
        * [bittensor.utils.balance](<../balance/index.html>)
        * [bittensor.utils.btlogging](<../btlogging/index.html>)
        * [bittensor.utils.easy_imports](<../easy_imports/index.html>)
        * [bittensor.utils.formatting](<../formatting/index.html>)
        * [bittensor.utils.liquidity](<../liquidity/index.html>)
        * [bittensor.utils.networking](<../networking/index.html>)
        * [bittensor.utils.registration](<../registration/index.html>)
        * [bittensor.utils.subnets](<#>)
        * [bittensor.utils.version](<../version/index.html>)
        * [bittensor.utils.weight_utils](<../weight_utils/index.html>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/utils/subnets/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/utils/subnets/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/utils/subnets/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.utils.subnets

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`SubnetsAPI`](<#bittensor.utils.subnets.SubnetsAPI>)
      * [`SubnetsAPI.dendrite`](<#bittensor.utils.subnets.SubnetsAPI.dendrite>)
      * [`SubnetsAPI.prepare_synapse()`](<#bittensor.utils.subnets.SubnetsAPI.prepare_synapse>)
      * [`SubnetsAPI.process_responses()`](<#bittensor.utils.subnets.SubnetsAPI.process_responses>)
      * [`SubnetsAPI.query_api()`](<#bittensor.utils.subnets.SubnetsAPI.query_api>)
      * [`SubnetsAPI.wallet`](<#bittensor.utils.subnets.SubnetsAPI.wallet>)



# bittensor.utils.subnets[#](<#module-bittensor.utils.subnets> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`SubnetsAPI`](<#bittensor.utils.subnets.SubnetsAPI> "bittensor.utils.subnets.SubnetsAPI") | This class is not used within the bittensor package, but is actively used by the community.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.utils.subnets.SubnetsAPI(_wallet_)[#](<#bittensor.utils.subnets.SubnetsAPI> "Link to this definition")
    

Bases: [`abc.ABC`](<https://docs.python.org/3/library/abc.html#abc.ABC> "\(in Python v3.14\)")

This class is not used within the bittensor package, but is actively used by the community.

Parameters:
    

**wallet** (_bittensor_wallet.Wallet_)

dendrite[#](<#bittensor.utils.subnets.SubnetsAPI.dendrite> "Link to this definition")
    

abstractmethod prepare_synapse(_* args_, _** kwargs_)[#](<#bittensor.utils.subnets.SubnetsAPI.prepare_synapse> "Link to this definition")
    

Prepare the synapse-specific payload.

Return type:
    

[Any](<../../core/chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any")

abstractmethod process_responses(_responses_)[#](<#bittensor.utils.subnets.SubnetsAPI.process_responses> "Link to this definition")
    

Process the responses from the network.

Parameters:
    

**responses** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[__Union_ _[_[_bittensor.core.synapse.Synapse_](<../../core/synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse") _,_[_Any_](<../../core/chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any") _]__]_)

Return type:
    

[Any](<../../core/chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any")

async query_api(_axons_ , _deserialize =False_, _timeout =12_, _** kwargs_)[#](<#bittensor.utils.subnets.SubnetsAPI.query_api> "Link to this definition")
    

Queries the API nodes of a subnet using the given synapse and bespoke query function.

Parameters:
    

  * **axons** (_Union_ _[_[_bittensor.core.axon.Axon_](<../../core/axon/index.html#bittensor.core.axon.Axon> "bittensor.core.axon.Axon") _,_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_bittensor.core.axon.Axon_](<../../core/axon/index.html#bittensor.core.axon.Axon> "bittensor.core.axon.Axon") _]__]_) – The list of axon(s) to query.

  * **deserialize** (_Optional_ _[_[_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)") _]_) – Whether to deserialize the responses.

  * **timeout** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The timeout in seconds for the query.

  * ****kwargs** – Keyword arguments for the prepare_synapse_fn.



Returns:
    

The result of the process_responses_fn.

Return type:
    

[Any](<../../core/chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any")

wallet[#](<#bittensor.utils.subnets.SubnetsAPI.wallet> "Link to this definition")
    

[ __ previous bittensor.utils.registration.torch_utils ](<../registration/torch_utils/index.html> "previous page") [ next bittensor.utils.version __](<../version/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`SubnetsAPI`](<#bittensor.utils.subnets.SubnetsAPI>)
      * [`SubnetsAPI.dendrite`](<#bittensor.utils.subnets.SubnetsAPI.dendrite>)
      * [`SubnetsAPI.prepare_synapse()`](<#bittensor.utils.subnets.SubnetsAPI.prepare_synapse>)
      * [`SubnetsAPI.process_responses()`](<#bittensor.utils.subnets.SubnetsAPI.process_responses>)
      * [`SubnetsAPI.query_api()`](<#bittensor.utils.subnets.SubnetsAPI.query_api>)
      * [`SubnetsAPI.wallet`](<#bittensor.utils.subnets.SubnetsAPI.wallet>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.