# bittensor.extras.subtensor_api.mev_shield &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/extras/subtensor_api/mev_shield/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/extras/subtensor_api/mev_shield/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/extras/subtensor_api/mev_shield/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.extras.subtensor_api.mev_shield

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`MevShield`](<#bittensor.extras.subtensor_api.mev_shield.MevShield>)
      * [`MevShield.get_mev_shield_current_key`](<#bittensor.extras.subtensor_api.mev_shield.MevShield.get_mev_shield_current_key>)
      * [`MevShield.get_mev_shield_next_key`](<#bittensor.extras.subtensor_api.mev_shield.MevShield.get_mev_shield_next_key>)
      * [`MevShield.mev_submit_encrypted`](<#bittensor.extras.subtensor_api.mev_shield.MevShield.mev_submit_encrypted>)



# bittensor.extras.subtensor_api.mev_shield[#](<#module-bittensor.extras.subtensor_api.mev_shield> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`MevShield`](<#bittensor.extras.subtensor_api.mev_shield.MevShield> "bittensor.extras.subtensor_api.mev_shield.MevShield") | Class for managing MEV Shield operations.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.extras.subtensor_api.mev_shield.MevShield(_subtensor_)[#](<#bittensor.extras.subtensor_api.mev_shield.MevShield> "Link to this definition")
    

Class for managing MEV Shield operations.

Parameters:
    

**subtensor** (_Union_ _[_[_bittensor.core.subtensor.Subtensor_](<../../../core/subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor") _,_[_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../core/async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor") _]_)

get_mev_shield_current_key[#](<#bittensor.extras.subtensor_api.mev_shield.MevShield.get_mev_shield_current_key> "Link to this definition")
    

get_mev_shield_next_key[#](<#bittensor.extras.subtensor_api.mev_shield.MevShield.get_mev_shield_next_key> "Link to this definition")
    

mev_submit_encrypted[#](<#bittensor.extras.subtensor_api.mev_shield.MevShield.mev_submit_encrypted> "Link to this definition")
    

[ __ previous bittensor.extras.subtensor_api.metagraphs ](<../metagraphs/index.html> "previous page") [ next bittensor.extras.subtensor_api.neurons __](<../neurons/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`MevShield`](<#bittensor.extras.subtensor_api.mev_shield.MevShield>)
      * [`MevShield.get_mev_shield_current_key`](<#bittensor.extras.subtensor_api.mev_shield.MevShield.get_mev_shield_current_key>)
      * [`MevShield.get_mev_shield_next_key`](<#bittensor.extras.subtensor_api.mev_shield.MevShield.get_mev_shield_next_key>)
      * [`MevShield.mev_submit_encrypted`](<#bittensor.extras.subtensor_api.mev_shield.MevShield.mev_submit_encrypted>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.