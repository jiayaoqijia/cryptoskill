# bittensor.core.chain_data &#8212; Bittensor SDK Docs  documentation

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
        * [bittensor.core.chain_data](<#>)
        * [bittensor.core.config](<../config/index.html>)
        * [bittensor.core.dendrite](<../dendrite/index.html>)
        * [bittensor.core.errors](<../errors/index.html>)
        * [bittensor.core.extrinsics](<../extrinsics/index.html>)
        * [bittensor.core.metagraph](<../metagraph/index.html>)
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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/core/chain_data/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data

##  Contents 

  * [Submodules](<#submodules>)
  * [Attributes](<#attributes>)
  * [Package Contents](<#package-contents>)
    * [`ProposalCallData`](<#bittensor.core.chain_data.ProposalCallData>)



# bittensor.core.chain_data[#](<#module-bittensor.core.chain_data> "Link to this heading")

This module provides data structures and functions for working with the Bittensor network, including neuron and subnet information, SCALE encoding/decoding, and custom RPC type registry.

## Submodules[#](<#submodules> "Link to this heading")

  * [bittensor.core.chain_data.axon_info](<axon_info/index.html>)
  * [bittensor.core.chain_data.chain_identity](<chain_identity/index.html>)
  * [bittensor.core.chain_data.coldkey_swap](<coldkey_swap/index.html>)
  * [bittensor.core.chain_data.crowdloan_info](<crowdloan_info/index.html>)
  * [bittensor.core.chain_data.delegate_info](<delegate_info/index.html>)
  * [bittensor.core.chain_data.delegate_info_lite](<delegate_info_lite/index.html>)
  * [bittensor.core.chain_data.dynamic_info](<dynamic_info/index.html>)
  * [bittensor.core.chain_data.info_base](<info_base/index.html>)
  * [bittensor.core.chain_data.ip_info](<ip_info/index.html>)
  * [bittensor.core.chain_data.metagraph_info](<metagraph_info/index.html>)
  * [bittensor.core.chain_data.neuron_info](<neuron_info/index.html>)
  * [bittensor.core.chain_data.neuron_info_lite](<neuron_info_lite/index.html>)
  * [bittensor.core.chain_data.prometheus_info](<prometheus_info/index.html>)
  * [bittensor.core.chain_data.proposal_vote_data](<proposal_vote_data/index.html>)
  * [bittensor.core.chain_data.proxy](<proxy/index.html>)
  * [bittensor.core.chain_data.root_claim](<root_claim/index.html>)
  * [bittensor.core.chain_data.scheduled_coldkey_swap_info](<scheduled_coldkey_swap_info/index.html>)
  * [bittensor.core.chain_data.sim_swap](<sim_swap/index.html>)
  * [bittensor.core.chain_data.stake_info](<stake_info/index.html>)
  * [bittensor.core.chain_data.subnet_hyperparameters](<subnet_hyperparameters/index.html>)
  * [bittensor.core.chain_data.subnet_identity](<subnet_identity/index.html>)
  * [bittensor.core.chain_data.subnet_info](<subnet_info/index.html>)
  * [bittensor.core.chain_data.subnet_state](<subnet_state/index.html>)
  * [bittensor.core.chain_data.utils](<utils/index.html>)
  * [bittensor.core.chain_data.weight_commit_info](<weight_commit_info/index.html>)



## Attributes[#](<#attributes> "Link to this heading")

[`ProposalCallData`](<#bittensor.core.chain_data.ProposalCallData> "bittensor.core.chain_data.ProposalCallData") |   
---|---  
  
## Package Contents[#](<#package-contents> "Link to this heading")

bittensor.core.chain_data.ProposalCallData[#](<#bittensor.core.chain_data.ProposalCallData> "Link to this definition")
    

[ __ previous bittensor.core.axon ](<../axon/index.html> "previous page") [ next bittensor.core.chain_data.axon_info __](<axon_info/index.html> "next page")

__Contents

  * [Submodules](<#submodules>)
  * [Attributes](<#attributes>)
  * [Package Contents](<#package-contents>)
    * [`ProposalCallData`](<#bittensor.core.chain_data.ProposalCallData>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.