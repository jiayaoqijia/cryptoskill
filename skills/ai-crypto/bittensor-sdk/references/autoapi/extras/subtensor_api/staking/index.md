# bittensor.extras.subtensor_api.staking &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/extras/subtensor_api/staking/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/extras/subtensor_api/staking/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/extras/subtensor_api/staking/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.extras.subtensor_api.staking

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Staking`](<#bittensor.extras.subtensor_api.staking.Staking>)
      * [`Staking.add_stake`](<#bittensor.extras.subtensor_api.staking.Staking.add_stake>)
      * [`Staking.add_stake_burn`](<#bittensor.extras.subtensor_api.staking.Staking.add_stake_burn>)
      * [`Staking.add_stake_multiple`](<#bittensor.extras.subtensor_api.staking.Staking.add_stake_multiple>)
      * [`Staking.claim_root`](<#bittensor.extras.subtensor_api.staking.Staking.claim_root>)
      * [`Staking.get_auto_stakes`](<#bittensor.extras.subtensor_api.staking.Staking.get_auto_stakes>)
      * [`Staking.get_hotkey_stake`](<#bittensor.extras.subtensor_api.staking.Staking.get_hotkey_stake>)
      * [`Staking.get_minimum_required_stake`](<#bittensor.extras.subtensor_api.staking.Staking.get_minimum_required_stake>)
      * [`Staking.get_root_alpha_dividends_per_subnet`](<#bittensor.extras.subtensor_api.staking.Staking.get_root_alpha_dividends_per_subnet>)
      * [`Staking.get_root_claim_type`](<#bittensor.extras.subtensor_api.staking.Staking.get_root_claim_type>)
      * [`Staking.get_root_claimable_all_rates`](<#bittensor.extras.subtensor_api.staking.Staking.get_root_claimable_all_rates>)
      * [`Staking.get_root_claimable_rate`](<#bittensor.extras.subtensor_api.staking.Staking.get_root_claimable_rate>)
      * [`Staking.get_root_claimable_stake`](<#bittensor.extras.subtensor_api.staking.Staking.get_root_claimable_stake>)
      * [`Staking.get_root_claimed`](<#bittensor.extras.subtensor_api.staking.Staking.get_root_claimed>)
      * [`Staking.get_stake`](<#bittensor.extras.subtensor_api.staking.Staking.get_stake>)
      * [`Staking.get_stake_add_fee`](<#bittensor.extras.subtensor_api.staking.Staking.get_stake_add_fee>)
      * [`Staking.get_stake_for_coldkey_and_hotkey`](<#bittensor.extras.subtensor_api.staking.Staking.get_stake_for_coldkey_and_hotkey>)
      * [`Staking.get_stake_info_for_coldkey`](<#bittensor.extras.subtensor_api.staking.Staking.get_stake_info_for_coldkey>)
      * [`Staking.get_stake_info_for_coldkeys`](<#bittensor.extras.subtensor_api.staking.Staking.get_stake_info_for_coldkeys>)
      * [`Staking.get_stake_movement_fee`](<#bittensor.extras.subtensor_api.staking.Staking.get_stake_movement_fee>)
      * [`Staking.get_stake_weight`](<#bittensor.extras.subtensor_api.staking.Staking.get_stake_weight>)
      * [`Staking.get_staking_hotkeys`](<#bittensor.extras.subtensor_api.staking.Staking.get_staking_hotkeys>)
      * [`Staking.get_unstake_fee`](<#bittensor.extras.subtensor_api.staking.Staking.get_unstake_fee>)
      * [`Staking.move_stake`](<#bittensor.extras.subtensor_api.staking.Staking.move_stake>)
      * [`Staking.set_auto_stake`](<#bittensor.extras.subtensor_api.staking.Staking.set_auto_stake>)
      * [`Staking.set_root_claim_type`](<#bittensor.extras.subtensor_api.staking.Staking.set_root_claim_type>)
      * [`Staking.sim_swap`](<#bittensor.extras.subtensor_api.staking.Staking.sim_swap>)
      * [`Staking.swap_stake`](<#bittensor.extras.subtensor_api.staking.Staking.swap_stake>)
      * [`Staking.transfer_stake`](<#bittensor.extras.subtensor_api.staking.Staking.transfer_stake>)
      * [`Staking.unstake`](<#bittensor.extras.subtensor_api.staking.Staking.unstake>)
      * [`Staking.unstake_all`](<#bittensor.extras.subtensor_api.staking.Staking.unstake_all>)
      * [`Staking.unstake_multiple`](<#bittensor.extras.subtensor_api.staking.Staking.unstake_multiple>)



# bittensor.extras.subtensor_api.staking[#](<#module-bittensor.extras.subtensor_api.staking> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`Staking`](<#bittensor.extras.subtensor_api.staking.Staking> "bittensor.extras.subtensor_api.staking.Staking") | Class for managing staking operations.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.extras.subtensor_api.staking.Staking(_subtensor_)[#](<#bittensor.extras.subtensor_api.staking.Staking> "Link to this definition")
    

Class for managing staking operations.

Parameters:
    

**subtensor** (_Union_ _[_[_bittensor.core.subtensor.Subtensor_](<../../../core/subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor") _,_[_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../core/async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor") _]_)

add_stake[#](<#bittensor.extras.subtensor_api.staking.Staking.add_stake> "Link to this definition")
    

add_stake_burn[#](<#bittensor.extras.subtensor_api.staking.Staking.add_stake_burn> "Link to this definition")
    

add_stake_multiple[#](<#bittensor.extras.subtensor_api.staking.Staking.add_stake_multiple> "Link to this definition")
    

claim_root[#](<#bittensor.extras.subtensor_api.staking.Staking.claim_root> "Link to this definition")
    

get_auto_stakes[#](<#bittensor.extras.subtensor_api.staking.Staking.get_auto_stakes> "Link to this definition")
    

get_hotkey_stake[#](<#bittensor.extras.subtensor_api.staking.Staking.get_hotkey_stake> "Link to this definition")
    

get_minimum_required_stake[#](<#bittensor.extras.subtensor_api.staking.Staking.get_minimum_required_stake> "Link to this definition")
    

get_root_alpha_dividends_per_subnet[#](<#bittensor.extras.subtensor_api.staking.Staking.get_root_alpha_dividends_per_subnet> "Link to this definition")
    

get_root_claim_type[#](<#bittensor.extras.subtensor_api.staking.Staking.get_root_claim_type> "Link to this definition")
    

get_root_claimable_all_rates[#](<#bittensor.extras.subtensor_api.staking.Staking.get_root_claimable_all_rates> "Link to this definition")
    

get_root_claimable_rate[#](<#bittensor.extras.subtensor_api.staking.Staking.get_root_claimable_rate> "Link to this definition")
    

get_root_claimable_stake[#](<#bittensor.extras.subtensor_api.staking.Staking.get_root_claimable_stake> "Link to this definition")
    

get_root_claimed[#](<#bittensor.extras.subtensor_api.staking.Staking.get_root_claimed> "Link to this definition")
    

get_stake[#](<#bittensor.extras.subtensor_api.staking.Staking.get_stake> "Link to this definition")
    

get_stake_add_fee[#](<#bittensor.extras.subtensor_api.staking.Staking.get_stake_add_fee> "Link to this definition")
    

get_stake_for_coldkey_and_hotkey[#](<#bittensor.extras.subtensor_api.staking.Staking.get_stake_for_coldkey_and_hotkey> "Link to this definition")
    

get_stake_info_for_coldkey[#](<#bittensor.extras.subtensor_api.staking.Staking.get_stake_info_for_coldkey> "Link to this definition")
    

get_stake_info_for_coldkeys[#](<#bittensor.extras.subtensor_api.staking.Staking.get_stake_info_for_coldkeys> "Link to this definition")
    

get_stake_movement_fee[#](<#bittensor.extras.subtensor_api.staking.Staking.get_stake_movement_fee> "Link to this definition")
    

get_stake_weight[#](<#bittensor.extras.subtensor_api.staking.Staking.get_stake_weight> "Link to this definition")
    

get_staking_hotkeys[#](<#bittensor.extras.subtensor_api.staking.Staking.get_staking_hotkeys> "Link to this definition")
    

get_unstake_fee[#](<#bittensor.extras.subtensor_api.staking.Staking.get_unstake_fee> "Link to this definition")
    

move_stake[#](<#bittensor.extras.subtensor_api.staking.Staking.move_stake> "Link to this definition")
    

set_auto_stake[#](<#bittensor.extras.subtensor_api.staking.Staking.set_auto_stake> "Link to this definition")
    

set_root_claim_type[#](<#bittensor.extras.subtensor_api.staking.Staking.set_root_claim_type> "Link to this definition")
    

sim_swap[#](<#bittensor.extras.subtensor_api.staking.Staking.sim_swap> "Link to this definition")
    

swap_stake[#](<#bittensor.extras.subtensor_api.staking.Staking.swap_stake> "Link to this definition")
    

transfer_stake[#](<#bittensor.extras.subtensor_api.staking.Staking.transfer_stake> "Link to this definition")
    

unstake[#](<#bittensor.extras.subtensor_api.staking.Staking.unstake> "Link to this definition")
    

unstake_all[#](<#bittensor.extras.subtensor_api.staking.Staking.unstake_all> "Link to this definition")
    

unstake_multiple[#](<#bittensor.extras.subtensor_api.staking.Staking.unstake_multiple> "Link to this definition")
    

[ __ previous bittensor.extras.subtensor_api.queries ](<../queries/index.html> "previous page") [ next bittensor.extras.subtensor_api.subnets __](<../subnets/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Staking`](<#bittensor.extras.subtensor_api.staking.Staking>)
      * [`Staking.add_stake`](<#bittensor.extras.subtensor_api.staking.Staking.add_stake>)
      * [`Staking.add_stake_burn`](<#bittensor.extras.subtensor_api.staking.Staking.add_stake_burn>)
      * [`Staking.add_stake_multiple`](<#bittensor.extras.subtensor_api.staking.Staking.add_stake_multiple>)
      * [`Staking.claim_root`](<#bittensor.extras.subtensor_api.staking.Staking.claim_root>)
      * [`Staking.get_auto_stakes`](<#bittensor.extras.subtensor_api.staking.Staking.get_auto_stakes>)
      * [`Staking.get_hotkey_stake`](<#bittensor.extras.subtensor_api.staking.Staking.get_hotkey_stake>)
      * [`Staking.get_minimum_required_stake`](<#bittensor.extras.subtensor_api.staking.Staking.get_minimum_required_stake>)
      * [`Staking.get_root_alpha_dividends_per_subnet`](<#bittensor.extras.subtensor_api.staking.Staking.get_root_alpha_dividends_per_subnet>)
      * [`Staking.get_root_claim_type`](<#bittensor.extras.subtensor_api.staking.Staking.get_root_claim_type>)
      * [`Staking.get_root_claimable_all_rates`](<#bittensor.extras.subtensor_api.staking.Staking.get_root_claimable_all_rates>)
      * [`Staking.get_root_claimable_rate`](<#bittensor.extras.subtensor_api.staking.Staking.get_root_claimable_rate>)
      * [`Staking.get_root_claimable_stake`](<#bittensor.extras.subtensor_api.staking.Staking.get_root_claimable_stake>)
      * [`Staking.get_root_claimed`](<#bittensor.extras.subtensor_api.staking.Staking.get_root_claimed>)
      * [`Staking.get_stake`](<#bittensor.extras.subtensor_api.staking.Staking.get_stake>)
      * [`Staking.get_stake_add_fee`](<#bittensor.extras.subtensor_api.staking.Staking.get_stake_add_fee>)
      * [`Staking.get_stake_for_coldkey_and_hotkey`](<#bittensor.extras.subtensor_api.staking.Staking.get_stake_for_coldkey_and_hotkey>)
      * [`Staking.get_stake_info_for_coldkey`](<#bittensor.extras.subtensor_api.staking.Staking.get_stake_info_for_coldkey>)
      * [`Staking.get_stake_info_for_coldkeys`](<#bittensor.extras.subtensor_api.staking.Staking.get_stake_info_for_coldkeys>)
      * [`Staking.get_stake_movement_fee`](<#bittensor.extras.subtensor_api.staking.Staking.get_stake_movement_fee>)
      * [`Staking.get_stake_weight`](<#bittensor.extras.subtensor_api.staking.Staking.get_stake_weight>)
      * [`Staking.get_staking_hotkeys`](<#bittensor.extras.subtensor_api.staking.Staking.get_staking_hotkeys>)
      * [`Staking.get_unstake_fee`](<#bittensor.extras.subtensor_api.staking.Staking.get_unstake_fee>)
      * [`Staking.move_stake`](<#bittensor.extras.subtensor_api.staking.Staking.move_stake>)
      * [`Staking.set_auto_stake`](<#bittensor.extras.subtensor_api.staking.Staking.set_auto_stake>)
      * [`Staking.set_root_claim_type`](<#bittensor.extras.subtensor_api.staking.Staking.set_root_claim_type>)
      * [`Staking.sim_swap`](<#bittensor.extras.subtensor_api.staking.Staking.sim_swap>)
      * [`Staking.swap_stake`](<#bittensor.extras.subtensor_api.staking.Staking.swap_stake>)
      * [`Staking.transfer_stake`](<#bittensor.extras.subtensor_api.staking.Staking.transfer_stake>)
      * [`Staking.unstake`](<#bittensor.extras.subtensor_api.staking.Staking.unstake>)
      * [`Staking.unstake_all`](<#bittensor.extras.subtensor_api.staking.Staking.unstake_all>)
      * [`Staking.unstake_multiple`](<#bittensor.extras.subtensor_api.staking.Staking.unstake_multiple>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.