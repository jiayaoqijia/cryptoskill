# bittensor.extras.subtensor_api.extrinsics &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/extras/subtensor_api/extrinsics/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/extras/subtensor_api/extrinsics/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/extras/subtensor_api/extrinsics/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.extras.subtensor_api.extrinsics

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Extrinsics`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics>)
      * [`Extrinsics.add_liquidity`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.add_liquidity>)
      * [`Extrinsics.add_stake`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.add_stake>)
      * [`Extrinsics.add_stake_burn`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.add_stake_burn>)
      * [`Extrinsics.add_stake_multiple`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.add_stake_multiple>)
      * [`Extrinsics.announce_coldkey_swap`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.announce_coldkey_swap>)
      * [`Extrinsics.burned_register`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.burned_register>)
      * [`Extrinsics.claim_root`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.claim_root>)
      * [`Extrinsics.clear_coldkey_swap_announcement`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.clear_coldkey_swap_announcement>)
      * [`Extrinsics.commit_weights`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.commit_weights>)
      * [`Extrinsics.contribute_crowdloan`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.contribute_crowdloan>)
      * [`Extrinsics.create_crowdloan`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.create_crowdloan>)
      * [`Extrinsics.dispute_coldkey_swap`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.dispute_coldkey_swap>)
      * [`Extrinsics.dissolve_crowdloan`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.dissolve_crowdloan>)
      * [`Extrinsics.finalize_crowdloan`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.finalize_crowdloan>)
      * [`Extrinsics.get_extrinsic_fee`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.get_extrinsic_fee>)
      * [`Extrinsics.modify_liquidity`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.modify_liquidity>)
      * [`Extrinsics.move_stake`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.move_stake>)
      * [`Extrinsics.refund_crowdloan`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.refund_crowdloan>)
      * [`Extrinsics.register`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.register>)
      * [`Extrinsics.register_limit`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.register_limit>)
      * [`Extrinsics.register_subnet`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.register_subnet>)
      * [`Extrinsics.remove_liquidity`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.remove_liquidity>)
      * [`Extrinsics.reveal_weights`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.reveal_weights>)
      * [`Extrinsics.root_register`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.root_register>)
      * [`Extrinsics.root_set_pending_childkey_cooldown`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.root_set_pending_childkey_cooldown>)
      * [`Extrinsics.serve_axon`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.serve_axon>)
      * [`Extrinsics.set_children`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.set_children>)
      * [`Extrinsics.set_commitment`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.set_commitment>)
      * [`Extrinsics.set_root_claim_type`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.set_root_claim_type>)
      * [`Extrinsics.set_subnet_identity`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.set_subnet_identity>)
      * [`Extrinsics.set_weights`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.set_weights>)
      * [`Extrinsics.start_call`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.start_call>)
      * [`Extrinsics.swap_coldkey_announced`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.swap_coldkey_announced>)
      * [`Extrinsics.swap_stake`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.swap_stake>)
      * [`Extrinsics.toggle_user_liquidity`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.toggle_user_liquidity>)
      * [`Extrinsics.transfer`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.transfer>)
      * [`Extrinsics.transfer_stake`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.transfer_stake>)
      * [`Extrinsics.unstake`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.unstake>)
      * [`Extrinsics.unstake_all`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.unstake_all>)
      * [`Extrinsics.unstake_multiple`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.unstake_multiple>)
      * [`Extrinsics.update_cap_crowdloan`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.update_cap_crowdloan>)
      * [`Extrinsics.update_end_crowdloan`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.update_end_crowdloan>)
      * [`Extrinsics.update_min_contribution_crowdloan`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.update_min_contribution_crowdloan>)
      * [`Extrinsics.validate_extrinsic_params`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.validate_extrinsic_params>)
      * [`Extrinsics.withdraw_crowdloan`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.withdraw_crowdloan>)



# bittensor.extras.subtensor_api.extrinsics[#](<#module-bittensor.extras.subtensor_api.extrinsics> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`Extrinsics`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics> "bittensor.extras.subtensor_api.extrinsics.Extrinsics") | Class for managing extrinsic operations.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.extras.subtensor_api.extrinsics.Extrinsics(_subtensor_)[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics> "Link to this definition")
    

Class for managing extrinsic operations.

Parameters:
    

**subtensor** (_Union_ _[_[_bittensor.core.subtensor.Subtensor_](<../../../core/subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor") _,_[_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../core/async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor") _]_)

add_liquidity[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.add_liquidity> "Link to this definition")
    

add_stake[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.add_stake> "Link to this definition")
    

add_stake_burn[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.add_stake_burn> "Link to this definition")
    

add_stake_multiple[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.add_stake_multiple> "Link to this definition")
    

announce_coldkey_swap[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.announce_coldkey_swap> "Link to this definition")
    

burned_register[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.burned_register> "Link to this definition")
    

claim_root[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.claim_root> "Link to this definition")
    

clear_coldkey_swap_announcement[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.clear_coldkey_swap_announcement> "Link to this definition")
    

commit_weights[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.commit_weights> "Link to this definition")
    

contribute_crowdloan[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.contribute_crowdloan> "Link to this definition")
    

create_crowdloan[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.create_crowdloan> "Link to this definition")
    

dispute_coldkey_swap[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.dispute_coldkey_swap> "Link to this definition")
    

dissolve_crowdloan[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.dissolve_crowdloan> "Link to this definition")
    

finalize_crowdloan[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.finalize_crowdloan> "Link to this definition")
    

get_extrinsic_fee[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.get_extrinsic_fee> "Link to this definition")
    

modify_liquidity[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.modify_liquidity> "Link to this definition")
    

move_stake[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.move_stake> "Link to this definition")
    

refund_crowdloan[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.refund_crowdloan> "Link to this definition")
    

register[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.register> "Link to this definition")
    

register_limit[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.register_limit> "Link to this definition")
    

register_subnet[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.register_subnet> "Link to this definition")
    

remove_liquidity[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.remove_liquidity> "Link to this definition")
    

reveal_weights[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.reveal_weights> "Link to this definition")
    

root_register[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.root_register> "Link to this definition")
    

root_set_pending_childkey_cooldown[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.root_set_pending_childkey_cooldown> "Link to this definition")
    

serve_axon[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.serve_axon> "Link to this definition")
    

set_children[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.set_children> "Link to this definition")
    

set_commitment[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.set_commitment> "Link to this definition")
    

set_root_claim_type[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.set_root_claim_type> "Link to this definition")
    

set_subnet_identity[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.set_subnet_identity> "Link to this definition")
    

set_weights[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.set_weights> "Link to this definition")
    

start_call[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.start_call> "Link to this definition")
    

swap_coldkey_announced[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.swap_coldkey_announced> "Link to this definition")
    

swap_stake[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.swap_stake> "Link to this definition")
    

toggle_user_liquidity[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.toggle_user_liquidity> "Link to this definition")
    

transfer[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.transfer> "Link to this definition")
    

transfer_stake[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.transfer_stake> "Link to this definition")
    

unstake[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.unstake> "Link to this definition")
    

unstake_all[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.unstake_all> "Link to this definition")
    

unstake_multiple[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.unstake_multiple> "Link to this definition")
    

update_cap_crowdloan[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.update_cap_crowdloan> "Link to this definition")
    

update_end_crowdloan[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.update_end_crowdloan> "Link to this definition")
    

update_min_contribution_crowdloan[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.update_min_contribution_crowdloan> "Link to this definition")
    

validate_extrinsic_params[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.validate_extrinsic_params> "Link to this definition")
    

withdraw_crowdloan[#](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.withdraw_crowdloan> "Link to this definition")
    

[ __ previous bittensor.extras.subtensor_api.delegates ](<../delegates/index.html> "previous page") [ next bittensor.extras.subtensor_api.metagraphs __](<../metagraphs/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Extrinsics`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics>)
      * [`Extrinsics.add_liquidity`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.add_liquidity>)
      * [`Extrinsics.add_stake`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.add_stake>)
      * [`Extrinsics.add_stake_burn`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.add_stake_burn>)
      * [`Extrinsics.add_stake_multiple`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.add_stake_multiple>)
      * [`Extrinsics.announce_coldkey_swap`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.announce_coldkey_swap>)
      * [`Extrinsics.burned_register`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.burned_register>)
      * [`Extrinsics.claim_root`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.claim_root>)
      * [`Extrinsics.clear_coldkey_swap_announcement`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.clear_coldkey_swap_announcement>)
      * [`Extrinsics.commit_weights`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.commit_weights>)
      * [`Extrinsics.contribute_crowdloan`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.contribute_crowdloan>)
      * [`Extrinsics.create_crowdloan`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.create_crowdloan>)
      * [`Extrinsics.dispute_coldkey_swap`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.dispute_coldkey_swap>)
      * [`Extrinsics.dissolve_crowdloan`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.dissolve_crowdloan>)
      * [`Extrinsics.finalize_crowdloan`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.finalize_crowdloan>)
      * [`Extrinsics.get_extrinsic_fee`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.get_extrinsic_fee>)
      * [`Extrinsics.modify_liquidity`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.modify_liquidity>)
      * [`Extrinsics.move_stake`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.move_stake>)
      * [`Extrinsics.refund_crowdloan`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.refund_crowdloan>)
      * [`Extrinsics.register`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.register>)
      * [`Extrinsics.register_limit`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.register_limit>)
      * [`Extrinsics.register_subnet`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.register_subnet>)
      * [`Extrinsics.remove_liquidity`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.remove_liquidity>)
      * [`Extrinsics.reveal_weights`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.reveal_weights>)
      * [`Extrinsics.root_register`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.root_register>)
      * [`Extrinsics.root_set_pending_childkey_cooldown`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.root_set_pending_childkey_cooldown>)
      * [`Extrinsics.serve_axon`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.serve_axon>)
      * [`Extrinsics.set_children`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.set_children>)
      * [`Extrinsics.set_commitment`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.set_commitment>)
      * [`Extrinsics.set_root_claim_type`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.set_root_claim_type>)
      * [`Extrinsics.set_subnet_identity`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.set_subnet_identity>)
      * [`Extrinsics.set_weights`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.set_weights>)
      * [`Extrinsics.start_call`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.start_call>)
      * [`Extrinsics.swap_coldkey_announced`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.swap_coldkey_announced>)
      * [`Extrinsics.swap_stake`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.swap_stake>)
      * [`Extrinsics.toggle_user_liquidity`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.toggle_user_liquidity>)
      * [`Extrinsics.transfer`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.transfer>)
      * [`Extrinsics.transfer_stake`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.transfer_stake>)
      * [`Extrinsics.unstake`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.unstake>)
      * [`Extrinsics.unstake_all`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.unstake_all>)
      * [`Extrinsics.unstake_multiple`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.unstake_multiple>)
      * [`Extrinsics.update_cap_crowdloan`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.update_cap_crowdloan>)
      * [`Extrinsics.update_end_crowdloan`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.update_end_crowdloan>)
      * [`Extrinsics.update_min_contribution_crowdloan`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.update_min_contribution_crowdloan>)
      * [`Extrinsics.validate_extrinsic_params`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.validate_extrinsic_params>)
      * [`Extrinsics.withdraw_crowdloan`](<#bittensor.extras.subtensor_api.extrinsics.Extrinsics.withdraw_crowdloan>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.