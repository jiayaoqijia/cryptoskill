# bittensor.extras.subtensor_api.chain &#8212; Bittensor SDK Docs  documentation

[Skip to main content](<#main-content>)

__Back to top __ `Ctrl`+`K`

[ ![Bittensor SDK Docs  documentation - Home](../../../../../_static/logo.svg) ![Bittensor SDK Docs  documentation - Home](../../../../../_static/logo-dark-mode.svg) ](<../../../../../index.html>)

__ Search `Ctrl`+`K`

Table of Contents

  * [API Reference](<../../../../index.html>) __
    * [bittensor](<../../../index.html>) __
      * [bittensor.core](<../../../core/index.html>) __
        * [bittensor.core.async_subtensor](<../../../core/async_subtensor/index.html>)
        * [bittensor.core.axon](<../../../core/axon/index.html>)
        * [bittensor.core.chain_data](<../../../core/chain_data/index.html>)
        * [bittensor.core.config](<../../../core/config/index.html>)
        * [bittensor.core.dendrite](<../../../core/dendrite/index.html>)
        * [bittensor.core.errors](<../../../core/errors/index.html>)
        * [bittensor.core.extrinsics](<../../../core/extrinsics/index.html>)
        * [bittensor.core.metagraph](<../../../core/metagraph/index.html>)
        * [bittensor.core.settings](<../../../core/settings/index.html>)
        * [bittensor.core.stream](<../../../core/stream/index.html>)
        * [bittensor.core.subtensor](<../../../core/subtensor/index.html>)
        * [bittensor.core.synapse](<../../../core/synapse/index.html>)
        * [bittensor.core.tensor](<../../../core/tensor/index.html>)
        * [bittensor.core.threadpool](<../../../core/threadpool/index.html>)
        * [bittensor.core.types](<../../../core/types/index.html>)
      * [bittensor.extras](<../../index.html>) __
        * [bittensor.extras.dev_framework](<../../dev_framework/index.html>)
        * [bittensor.extras.subtensor_api](<../index.html>)
        * [bittensor.extras.timelock](<../../timelock/index.html>)
      * [bittensor.utils](<../../../utils/index.html>) __
        * [bittensor.utils.axon_utils](<../../../utils/axon_utils/index.html>)
        * [bittensor.utils.balance](<../../../utils/balance/index.html>)
        * [bittensor.utils.btlogging](<../../../utils/btlogging/index.html>)
        * [bittensor.utils.easy_imports](<../../../utils/easy_imports/index.html>)
        * [bittensor.utils.formatting](<../../../utils/formatting/index.html>)
        * [bittensor.utils.liquidity](<../../../utils/liquidity/index.html>)
        * [bittensor.utils.networking](<../../../utils/networking/index.html>)
        * [bittensor.utils.registration](<../../../utils/registration/index.html>)
        * [bittensor.utils.subnets](<../../../utils/subnets/index.html>)
        * [bittensor.utils.version](<../../../utils/version/index.html>)
        * [bittensor.utils.weight_utils](<../../../utils/weight_utils/index.html>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/extras/subtensor_api/chain/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/extras/subtensor_api/chain/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/extras/subtensor_api/chain/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.extras.subtensor_api.chain

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Chain`](<#bittensor.extras.subtensor_api.chain.Chain>)
      * [`Chain.get_admin_freeze_window`](<#bittensor.extras.subtensor_api.chain.Chain.get_admin_freeze_window>)
      * [`Chain.get_block_hash`](<#bittensor.extras.subtensor_api.chain.Chain.get_block_hash>)
      * [`Chain.get_block_info`](<#bittensor.extras.subtensor_api.chain.Chain.get_block_info>)
      * [`Chain.get_current_block`](<#bittensor.extras.subtensor_api.chain.Chain.get_current_block>)
      * [`Chain.get_delegate_identities`](<#bittensor.extras.subtensor_api.chain.Chain.get_delegate_identities>)
      * [`Chain.get_existential_deposit`](<#bittensor.extras.subtensor_api.chain.Chain.get_existential_deposit>)
      * [`Chain.get_minimum_required_stake`](<#bittensor.extras.subtensor_api.chain.Chain.get_minimum_required_stake>)
      * [`Chain.get_start_call_delay`](<#bittensor.extras.subtensor_api.chain.Chain.get_start_call_delay>)
      * [`Chain.get_timestamp`](<#bittensor.extras.subtensor_api.chain.Chain.get_timestamp>)
      * [`Chain.get_vote_data`](<#bittensor.extras.subtensor_api.chain.Chain.get_vote_data>)
      * [`Chain.is_fast_blocks`](<#bittensor.extras.subtensor_api.chain.Chain.is_fast_blocks>)
      * [`Chain.is_in_admin_freeze_window`](<#bittensor.extras.subtensor_api.chain.Chain.is_in_admin_freeze_window>)
      * [`Chain.last_drand_round`](<#bittensor.extras.subtensor_api.chain.Chain.last_drand_round>)
      * [`Chain.state_call`](<#bittensor.extras.subtensor_api.chain.Chain.state_call>)
      * [`Chain.tx_rate_limit`](<#bittensor.extras.subtensor_api.chain.Chain.tx_rate_limit>)



# bittensor.extras.subtensor_api.chain[#](<#module-bittensor.extras.subtensor_api.chain> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`Chain`](<#bittensor.extras.subtensor_api.chain.Chain> "bittensor.extras.subtensor_api.chain.Chain") | Class for managing chain state operations.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.extras.subtensor_api.chain.Chain(_subtensor_)[#](<#bittensor.extras.subtensor_api.chain.Chain> "Link to this definition")
    

Class for managing chain state operations.

Parameters:
    

**subtensor** (_Union_ _[_[_bittensor.core.subtensor.Subtensor_](<../../../core/subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor") _,_[_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../core/async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor") _]_)

get_admin_freeze_window[#](<#bittensor.extras.subtensor_api.chain.Chain.get_admin_freeze_window> "Link to this definition")
    

get_block_hash[#](<#bittensor.extras.subtensor_api.chain.Chain.get_block_hash> "Link to this definition")
    

get_block_info[#](<#bittensor.extras.subtensor_api.chain.Chain.get_block_info> "Link to this definition")
    

get_current_block[#](<#bittensor.extras.subtensor_api.chain.Chain.get_current_block> "Link to this definition")
    

get_delegate_identities[#](<#bittensor.extras.subtensor_api.chain.Chain.get_delegate_identities> "Link to this definition")
    

get_existential_deposit[#](<#bittensor.extras.subtensor_api.chain.Chain.get_existential_deposit> "Link to this definition")
    

get_minimum_required_stake[#](<#bittensor.extras.subtensor_api.chain.Chain.get_minimum_required_stake> "Link to this definition")
    

get_start_call_delay[#](<#bittensor.extras.subtensor_api.chain.Chain.get_start_call_delay> "Link to this definition")
    

get_timestamp[#](<#bittensor.extras.subtensor_api.chain.Chain.get_timestamp> "Link to this definition")
    

get_vote_data[#](<#bittensor.extras.subtensor_api.chain.Chain.get_vote_data> "Link to this definition")
    

is_fast_blocks[#](<#bittensor.extras.subtensor_api.chain.Chain.is_fast_blocks> "Link to this definition")
    

is_in_admin_freeze_window[#](<#bittensor.extras.subtensor_api.chain.Chain.is_in_admin_freeze_window> "Link to this definition")
    

last_drand_round[#](<#bittensor.extras.subtensor_api.chain.Chain.last_drand_round> "Link to this definition")
    

state_call[#](<#bittensor.extras.subtensor_api.chain.Chain.state_call> "Link to this definition")
    

tx_rate_limit[#](<#bittensor.extras.subtensor_api.chain.Chain.tx_rate_limit> "Link to this definition")
    

[ __ previous bittensor.extras.subtensor_api ](<../index.html> "previous page") [ next bittensor.extras.subtensor_api.commitments __](<../commitments/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Chain`](<#bittensor.extras.subtensor_api.chain.Chain>)
      * [`Chain.get_admin_freeze_window`](<#bittensor.extras.subtensor_api.chain.Chain.get_admin_freeze_window>)
      * [`Chain.get_block_hash`](<#bittensor.extras.subtensor_api.chain.Chain.get_block_hash>)
      * [`Chain.get_block_info`](<#bittensor.extras.subtensor_api.chain.Chain.get_block_info>)
      * [`Chain.get_current_block`](<#bittensor.extras.subtensor_api.chain.Chain.get_current_block>)
      * [`Chain.get_delegate_identities`](<#bittensor.extras.subtensor_api.chain.Chain.get_delegate_identities>)
      * [`Chain.get_existential_deposit`](<#bittensor.extras.subtensor_api.chain.Chain.get_existential_deposit>)
      * [`Chain.get_minimum_required_stake`](<#bittensor.extras.subtensor_api.chain.Chain.get_minimum_required_stake>)
      * [`Chain.get_start_call_delay`](<#bittensor.extras.subtensor_api.chain.Chain.get_start_call_delay>)
      * [`Chain.get_timestamp`](<#bittensor.extras.subtensor_api.chain.Chain.get_timestamp>)
      * [`Chain.get_vote_data`](<#bittensor.extras.subtensor_api.chain.Chain.get_vote_data>)
      * [`Chain.is_fast_blocks`](<#bittensor.extras.subtensor_api.chain.Chain.is_fast_blocks>)
      * [`Chain.is_in_admin_freeze_window`](<#bittensor.extras.subtensor_api.chain.Chain.is_in_admin_freeze_window>)
      * [`Chain.last_drand_round`](<#bittensor.extras.subtensor_api.chain.Chain.last_drand_round>)
      * [`Chain.state_call`](<#bittensor.extras.subtensor_api.chain.Chain.state_call>)
      * [`Chain.tx_rate_limit`](<#bittensor.extras.subtensor_api.chain.Chain.tx_rate_limit>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.