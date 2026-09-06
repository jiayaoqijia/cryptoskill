# bittensor.extras.subtensor_api.crowdloans &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/extras/subtensor_api/crowdloans/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/extras/subtensor_api/crowdloans/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/extras/subtensor_api/crowdloans/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.extras.subtensor_api.crowdloans

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Crowdloans`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans>)
      * [`Crowdloans.contribute_crowdloan`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.contribute_crowdloan>)
      * [`Crowdloans.create_crowdloan`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.create_crowdloan>)
      * [`Crowdloans.dissolve_crowdloan`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.dissolve_crowdloan>)
      * [`Crowdloans.finalize_crowdloan`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.finalize_crowdloan>)
      * [`Crowdloans.get_crowdloan_by_id`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.get_crowdloan_by_id>)
      * [`Crowdloans.get_crowdloan_constants`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.get_crowdloan_constants>)
      * [`Crowdloans.get_crowdloan_contributions`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.get_crowdloan_contributions>)
      * [`Crowdloans.get_crowdloan_next_id`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.get_crowdloan_next_id>)
      * [`Crowdloans.get_crowdloans`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.get_crowdloans>)
      * [`Crowdloans.refund_crowdloan`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.refund_crowdloan>)
      * [`Crowdloans.update_cap_crowdloan`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.update_cap_crowdloan>)
      * [`Crowdloans.update_end_crowdloan`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.update_end_crowdloan>)
      * [`Crowdloans.update_min_contribution_crowdloan`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.update_min_contribution_crowdloan>)
      * [`Crowdloans.withdraw_crowdloan`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.withdraw_crowdloan>)



# bittensor.extras.subtensor_api.crowdloans[#](<#module-bittensor.extras.subtensor_api.crowdloans> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`Crowdloans`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans> "bittensor.extras.subtensor_api.crowdloans.Crowdloans") | Class for managing any Crowdloans operations.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.extras.subtensor_api.crowdloans.Crowdloans(_subtensor_)[#](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans> "Link to this definition")
    

Class for managing any Crowdloans operations.

Parameters:
    

**subtensor** (_Union_ _[_[_bittensor.core.subtensor.Subtensor_](<../../../core/subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor") _,_[_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../core/async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor") _]_)

contribute_crowdloan[#](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.contribute_crowdloan> "Link to this definition")
    

create_crowdloan[#](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.create_crowdloan> "Link to this definition")
    

dissolve_crowdloan[#](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.dissolve_crowdloan> "Link to this definition")
    

finalize_crowdloan[#](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.finalize_crowdloan> "Link to this definition")
    

get_crowdloan_by_id[#](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.get_crowdloan_by_id> "Link to this definition")
    

get_crowdloan_constants[#](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.get_crowdloan_constants> "Link to this definition")
    

get_crowdloan_contributions[#](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.get_crowdloan_contributions> "Link to this definition")
    

get_crowdloan_next_id[#](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.get_crowdloan_next_id> "Link to this definition")
    

get_crowdloans[#](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.get_crowdloans> "Link to this definition")
    

refund_crowdloan[#](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.refund_crowdloan> "Link to this definition")
    

update_cap_crowdloan[#](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.update_cap_crowdloan> "Link to this definition")
    

update_end_crowdloan[#](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.update_end_crowdloan> "Link to this definition")
    

update_min_contribution_crowdloan[#](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.update_min_contribution_crowdloan> "Link to this definition")
    

withdraw_crowdloan[#](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.withdraw_crowdloan> "Link to this definition")
    

[ __ previous bittensor.extras.subtensor_api.commitments ](<../commitments/index.html> "previous page") [ next bittensor.extras.subtensor_api.delegates __](<../delegates/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Crowdloans`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans>)
      * [`Crowdloans.contribute_crowdloan`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.contribute_crowdloan>)
      * [`Crowdloans.create_crowdloan`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.create_crowdloan>)
      * [`Crowdloans.dissolve_crowdloan`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.dissolve_crowdloan>)
      * [`Crowdloans.finalize_crowdloan`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.finalize_crowdloan>)
      * [`Crowdloans.get_crowdloan_by_id`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.get_crowdloan_by_id>)
      * [`Crowdloans.get_crowdloan_constants`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.get_crowdloan_constants>)
      * [`Crowdloans.get_crowdloan_contributions`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.get_crowdloan_contributions>)
      * [`Crowdloans.get_crowdloan_next_id`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.get_crowdloan_next_id>)
      * [`Crowdloans.get_crowdloans`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.get_crowdloans>)
      * [`Crowdloans.refund_crowdloan`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.refund_crowdloan>)
      * [`Crowdloans.update_cap_crowdloan`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.update_cap_crowdloan>)
      * [`Crowdloans.update_end_crowdloan`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.update_end_crowdloan>)
      * [`Crowdloans.update_min_contribution_crowdloan`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.update_min_contribution_crowdloan>)
      * [`Crowdloans.withdraw_crowdloan`](<#bittensor.extras.subtensor_api.crowdloans.Crowdloans.withdraw_crowdloan>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.