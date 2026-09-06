# bittensor.extras.subtensor_api.wallets &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/extras/subtensor_api/wallets/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/extras/subtensor_api/wallets/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/extras/subtensor_api/wallets/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.extras.subtensor_api.wallets

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Wallets`](<#bittensor.extras.subtensor_api.wallets.Wallets>)
      * [`Wallets.does_hotkey_exist`](<#bittensor.extras.subtensor_api.wallets.Wallets.does_hotkey_exist>)
      * [`Wallets.filter_netuids_by_registered_hotkeys`](<#bittensor.extras.subtensor_api.wallets.Wallets.filter_netuids_by_registered_hotkeys>)
      * [`Wallets.get_balance`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_balance>)
      * [`Wallets.get_balances`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_balances>)
      * [`Wallets.get_children`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_children>)
      * [`Wallets.get_children_pending`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_children_pending>)
      * [`Wallets.get_coldkey_swap_announcement`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_announcement>)
      * [`Wallets.get_coldkey_swap_announcement_delay`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_announcement_delay>)
      * [`Wallets.get_coldkey_swap_announcements`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_announcements>)
      * [`Wallets.get_coldkey_swap_constants`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_constants>)
      * [`Wallets.get_coldkey_swap_dispute`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_dispute>)
      * [`Wallets.get_coldkey_swap_disputes`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_disputes>)
      * [`Wallets.get_coldkey_swap_reannouncement_delay`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_reannouncement_delay>)
      * [`Wallets.get_delegate_by_hotkey`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_delegate_by_hotkey>)
      * [`Wallets.get_delegate_take`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_delegate_take>)
      * [`Wallets.get_delegated`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_delegated>)
      * [`Wallets.get_hotkey_owner`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_hotkey_owner>)
      * [`Wallets.get_hotkey_stake`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_hotkey_stake>)
      * [`Wallets.get_minimum_required_stake`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_minimum_required_stake>)
      * [`Wallets.get_netuids_for_hotkey`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_netuids_for_hotkey>)
      * [`Wallets.get_owned_hotkeys`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_owned_hotkeys>)
      * [`Wallets.get_parents`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_parents>)
      * [`Wallets.get_stake`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_stake>)
      * [`Wallets.get_stake_add_fee`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_stake_add_fee>)
      * [`Wallets.get_stake_for_coldkey_and_hotkey`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_stake_for_coldkey_and_hotkey>)
      * [`Wallets.get_stake_for_hotkey`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_stake_for_hotkey>)
      * [`Wallets.get_stake_info_for_coldkey`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_stake_info_for_coldkey>)
      * [`Wallets.get_stake_movement_fee`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_stake_movement_fee>)
      * [`Wallets.get_transfer_fee`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_transfer_fee>)
      * [`Wallets.get_unstake_fee`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_unstake_fee>)
      * [`Wallets.is_hotkey_delegate`](<#bittensor.extras.subtensor_api.wallets.Wallets.is_hotkey_delegate>)
      * [`Wallets.is_hotkey_registered`](<#bittensor.extras.subtensor_api.wallets.Wallets.is_hotkey_registered>)
      * [`Wallets.is_hotkey_registered_any`](<#bittensor.extras.subtensor_api.wallets.Wallets.is_hotkey_registered_any>)
      * [`Wallets.is_hotkey_registered_on_subnet`](<#bittensor.extras.subtensor_api.wallets.Wallets.is_hotkey_registered_on_subnet>)
      * [`Wallets.set_children`](<#bittensor.extras.subtensor_api.wallets.Wallets.set_children>)
      * [`Wallets.transfer`](<#bittensor.extras.subtensor_api.wallets.Wallets.transfer>)



# bittensor.extras.subtensor_api.wallets[#](<#module-bittensor.extras.subtensor_api.wallets> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`Wallets`](<#bittensor.extras.subtensor_api.wallets.Wallets> "bittensor.extras.subtensor_api.wallets.Wallets") | Class for managing coldkey, hotkey, wallet operations.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.extras.subtensor_api.wallets.Wallets(_subtensor_)[#](<#bittensor.extras.subtensor_api.wallets.Wallets> "Link to this definition")
    

Class for managing coldkey, hotkey, wallet operations.

Parameters:
    

**subtensor** (_Union_ _[_[_bittensor.core.subtensor.Subtensor_](<../../../core/subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor") _,_[_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../core/async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor") _]_)

does_hotkey_exist[#](<#bittensor.extras.subtensor_api.wallets.Wallets.does_hotkey_exist> "Link to this definition")
    

filter_netuids_by_registered_hotkeys[#](<#bittensor.extras.subtensor_api.wallets.Wallets.filter_netuids_by_registered_hotkeys> "Link to this definition")
    

get_balance[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_balance> "Link to this definition")
    

get_balances[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_balances> "Link to this definition")
    

get_children[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_children> "Link to this definition")
    

get_children_pending[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_children_pending> "Link to this definition")
    

get_coldkey_swap_announcement[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_announcement> "Link to this definition")
    

get_coldkey_swap_announcement_delay[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_announcement_delay> "Link to this definition")
    

get_coldkey_swap_announcements[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_announcements> "Link to this definition")
    

get_coldkey_swap_constants[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_constants> "Link to this definition")
    

get_coldkey_swap_dispute[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_dispute> "Link to this definition")
    

get_coldkey_swap_disputes[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_disputes> "Link to this definition")
    

get_coldkey_swap_reannouncement_delay[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_reannouncement_delay> "Link to this definition")
    

get_delegate_by_hotkey[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_delegate_by_hotkey> "Link to this definition")
    

get_delegate_take[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_delegate_take> "Link to this definition")
    

get_delegated[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_delegated> "Link to this definition")
    

get_hotkey_owner[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_hotkey_owner> "Link to this definition")
    

get_hotkey_stake[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_hotkey_stake> "Link to this definition")
    

get_minimum_required_stake[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_minimum_required_stake> "Link to this definition")
    

get_netuids_for_hotkey[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_netuids_for_hotkey> "Link to this definition")
    

get_owned_hotkeys[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_owned_hotkeys> "Link to this definition")
    

get_parents[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_parents> "Link to this definition")
    

get_stake[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_stake> "Link to this definition")
    

get_stake_add_fee[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_stake_add_fee> "Link to this definition")
    

get_stake_for_coldkey_and_hotkey[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_stake_for_coldkey_and_hotkey> "Link to this definition")
    

get_stake_for_hotkey[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_stake_for_hotkey> "Link to this definition")
    

get_stake_info_for_coldkey[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_stake_info_for_coldkey> "Link to this definition")
    

get_stake_movement_fee[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_stake_movement_fee> "Link to this definition")
    

get_transfer_fee[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_transfer_fee> "Link to this definition")
    

get_unstake_fee[#](<#bittensor.extras.subtensor_api.wallets.Wallets.get_unstake_fee> "Link to this definition")
    

is_hotkey_delegate[#](<#bittensor.extras.subtensor_api.wallets.Wallets.is_hotkey_delegate> "Link to this definition")
    

is_hotkey_registered[#](<#bittensor.extras.subtensor_api.wallets.Wallets.is_hotkey_registered> "Link to this definition")
    

is_hotkey_registered_any[#](<#bittensor.extras.subtensor_api.wallets.Wallets.is_hotkey_registered_any> "Link to this definition")
    

is_hotkey_registered_on_subnet[#](<#bittensor.extras.subtensor_api.wallets.Wallets.is_hotkey_registered_on_subnet> "Link to this definition")
    

set_children[#](<#bittensor.extras.subtensor_api.wallets.Wallets.set_children> "Link to this definition")
    

transfer[#](<#bittensor.extras.subtensor_api.wallets.Wallets.transfer> "Link to this definition")
    

[ __ previous bittensor.extras.subtensor_api.utils ](<../utils/index.html> "previous page") [ next bittensor.extras.timelock __](<../../timelock/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Wallets`](<#bittensor.extras.subtensor_api.wallets.Wallets>)
      * [`Wallets.does_hotkey_exist`](<#bittensor.extras.subtensor_api.wallets.Wallets.does_hotkey_exist>)
      * [`Wallets.filter_netuids_by_registered_hotkeys`](<#bittensor.extras.subtensor_api.wallets.Wallets.filter_netuids_by_registered_hotkeys>)
      * [`Wallets.get_balance`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_balance>)
      * [`Wallets.get_balances`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_balances>)
      * [`Wallets.get_children`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_children>)
      * [`Wallets.get_children_pending`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_children_pending>)
      * [`Wallets.get_coldkey_swap_announcement`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_announcement>)
      * [`Wallets.get_coldkey_swap_announcement_delay`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_announcement_delay>)
      * [`Wallets.get_coldkey_swap_announcements`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_announcements>)
      * [`Wallets.get_coldkey_swap_constants`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_constants>)
      * [`Wallets.get_coldkey_swap_dispute`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_dispute>)
      * [`Wallets.get_coldkey_swap_disputes`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_disputes>)
      * [`Wallets.get_coldkey_swap_reannouncement_delay`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_coldkey_swap_reannouncement_delay>)
      * [`Wallets.get_delegate_by_hotkey`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_delegate_by_hotkey>)
      * [`Wallets.get_delegate_take`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_delegate_take>)
      * [`Wallets.get_delegated`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_delegated>)
      * [`Wallets.get_hotkey_owner`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_hotkey_owner>)
      * [`Wallets.get_hotkey_stake`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_hotkey_stake>)
      * [`Wallets.get_minimum_required_stake`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_minimum_required_stake>)
      * [`Wallets.get_netuids_for_hotkey`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_netuids_for_hotkey>)
      * [`Wallets.get_owned_hotkeys`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_owned_hotkeys>)
      * [`Wallets.get_parents`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_parents>)
      * [`Wallets.get_stake`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_stake>)
      * [`Wallets.get_stake_add_fee`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_stake_add_fee>)
      * [`Wallets.get_stake_for_coldkey_and_hotkey`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_stake_for_coldkey_and_hotkey>)
      * [`Wallets.get_stake_for_hotkey`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_stake_for_hotkey>)
      * [`Wallets.get_stake_info_for_coldkey`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_stake_info_for_coldkey>)
      * [`Wallets.get_stake_movement_fee`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_stake_movement_fee>)
      * [`Wallets.get_transfer_fee`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_transfer_fee>)
      * [`Wallets.get_unstake_fee`](<#bittensor.extras.subtensor_api.wallets.Wallets.get_unstake_fee>)
      * [`Wallets.is_hotkey_delegate`](<#bittensor.extras.subtensor_api.wallets.Wallets.is_hotkey_delegate>)
      * [`Wallets.is_hotkey_registered`](<#bittensor.extras.subtensor_api.wallets.Wallets.is_hotkey_registered>)
      * [`Wallets.is_hotkey_registered_any`](<#bittensor.extras.subtensor_api.wallets.Wallets.is_hotkey_registered_any>)
      * [`Wallets.is_hotkey_registered_on_subnet`](<#bittensor.extras.subtensor_api.wallets.Wallets.is_hotkey_registered_on_subnet>)
      * [`Wallets.set_children`](<#bittensor.extras.subtensor_api.wallets.Wallets.set_children>)
      * [`Wallets.transfer`](<#bittensor.extras.subtensor_api.wallets.Wallets.transfer>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.