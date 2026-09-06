# bittensor.core.extrinsics.pallets.subtensor_module &#8212; Bittensor SDK Docs  documentation

[Skip to main content](<#main-content>)

__Back to top __ `Ctrl`+`K`

[ ![Bittensor SDK Docs  documentation - Home](../../../../../../_static/logo.svg) ![Bittensor SDK Docs  documentation - Home](../../../../../../_static/logo-dark-mode.svg) ](<../../../../../../index.html>)

__ Search `Ctrl`+`K`

Table of Contents

  * [API Reference](<../../../../../index.html>) __
    * [bittensor](<../../../../index.html>) __
      * [bittensor.core](<../../../index.html>) __
        * [bittensor.core.async_subtensor](<../../../async_subtensor/index.html>)
        * [bittensor.core.axon](<../../../axon/index.html>)
        * [bittensor.core.chain_data](<../../../chain_data/index.html>)
        * [bittensor.core.config](<../../../config/index.html>)
        * [bittensor.core.dendrite](<../../../dendrite/index.html>)
        * [bittensor.core.errors](<../../../errors/index.html>)
        * [bittensor.core.extrinsics](<../../index.html>)
        * [bittensor.core.metagraph](<../../../metagraph/index.html>)
        * [bittensor.core.settings](<../../../settings/index.html>)
        * [bittensor.core.stream](<../../../stream/index.html>)
        * [bittensor.core.subtensor](<../../../subtensor/index.html>)
        * [bittensor.core.synapse](<../../../synapse/index.html>)
        * [bittensor.core.tensor](<../../../tensor/index.html>)
        * [bittensor.core.threadpool](<../../../threadpool/index.html>)
        * [bittensor.core.types](<../../../types/index.html>)
      * [bittensor.extras](<../../../../extras/index.html>) __
        * [bittensor.extras.dev_framework](<../../../../extras/dev_framework/index.html>)
        * [bittensor.extras.subtensor_api](<../../../../extras/subtensor_api/index.html>)
        * [bittensor.extras.timelock](<../../../../extras/timelock/index.html>)
      * [bittensor.utils](<../../../../utils/index.html>) __
        * [bittensor.utils.axon_utils](<../../../../utils/axon_utils/index.html>)
        * [bittensor.utils.balance](<../../../../utils/balance/index.html>)
        * [bittensor.utils.btlogging](<../../../../utils/btlogging/index.html>)
        * [bittensor.utils.easy_imports](<../../../../utils/easy_imports/index.html>)
        * [bittensor.utils.formatting](<../../../../utils/formatting/index.html>)
        * [bittensor.utils.liquidity](<../../../../utils/liquidity/index.html>)
        * [bittensor.utils.networking](<../../../../utils/networking/index.html>)
        * [bittensor.utils.registration](<../../../../utils/registration/index.html>)
        * [bittensor.utils.subnets](<../../../../utils/subnets/index.html>)
        * [bittensor.utils.version](<../../../../utils/version/index.html>)
        * [bittensor.utils.weight_utils](<../../../../utils/weight_utils/index.html>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/pallets/subtensor_module/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/pallets/subtensor_module/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../../_sources/autoapi/bittensor/core/extrinsics/pallets/subtensor_module/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.pallets.subtensor_module

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`SubtensorModule`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule>)
      * [`SubtensorModule.add_stake()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.add_stake>)
      * [`SubtensorModule.add_stake_burn()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.add_stake_burn>)
      * [`SubtensorModule.add_stake_limit()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.add_stake_limit>)
      * [`SubtensorModule.announce_coldkey_swap()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.announce_coldkey_swap>)
      * [`SubtensorModule.burned_register()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.burned_register>)
      * [`SubtensorModule.claim_root()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.claim_root>)
      * [`SubtensorModule.clear_coldkey_swap_announcement()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.clear_coldkey_swap_announcement>)
      * [`SubtensorModule.commit_mechanism_weights()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.commit_mechanism_weights>)
      * [`SubtensorModule.commit_timelocked_mechanism_weights()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.commit_timelocked_mechanism_weights>)
      * [`SubtensorModule.decrease_take()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.decrease_take>)
      * [`SubtensorModule.dispute_coldkey_swap()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.dispute_coldkey_swap>)
      * [`SubtensorModule.increase_take()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.increase_take>)
      * [`SubtensorModule.move_stake()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.move_stake>)
      * [`SubtensorModule.register_limit()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.register_limit>)
      * [`SubtensorModule.register_network()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.register_network>)
      * [`SubtensorModule.remove_coldkey_swap_announcement()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.remove_coldkey_swap_announcement>)
      * [`SubtensorModule.remove_stake()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.remove_stake>)
      * [`SubtensorModule.remove_stake_full_limit()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.remove_stake_full_limit>)
      * [`SubtensorModule.remove_stake_limit()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.remove_stake_limit>)
      * [`SubtensorModule.reset_coldkey_swap()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.reset_coldkey_swap>)
      * [`SubtensorModule.reveal_mechanism_weights()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.reveal_mechanism_weights>)
      * [`SubtensorModule.root_register()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.root_register>)
      * [`SubtensorModule.serve_axon()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.serve_axon>)
      * [`SubtensorModule.serve_axon_tls()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.serve_axon_tls>)
      * [`SubtensorModule.set_children()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.set_children>)
      * [`SubtensorModule.set_coldkey_auto_stake_hotkey()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.set_coldkey_auto_stake_hotkey>)
      * [`SubtensorModule.set_mechanism_weights()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.set_mechanism_weights>)
      * [`SubtensorModule.set_pending_childkey_cooldown()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.set_pending_childkey_cooldown>)
      * [`SubtensorModule.set_root_claim_type()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.set_root_claim_type>)
      * [`SubtensorModule.set_subnet_identity()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.set_subnet_identity>)
      * [`SubtensorModule.start_call()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.start_call>)
      * [`SubtensorModule.swap_coldkey()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.swap_coldkey>)
      * [`SubtensorModule.swap_coldkey_announced()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.swap_coldkey_announced>)
      * [`SubtensorModule.swap_stake()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.swap_stake>)
      * [`SubtensorModule.swap_stake_limit()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.swap_stake_limit>)
      * [`SubtensorModule.transfer_stake()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.transfer_stake>)



# bittensor.core.extrinsics.pallets.subtensor_module[#](<#module-bittensor.core.extrinsics.pallets.subtensor_module> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`SubtensorModule`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule> "bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule") | Factory class for creating GenericCall objects for SubtensorModule pallet functions.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule> "Link to this definition")
    

Bases: [`bittensor.core.extrinsics.pallets.base.CallBuilder`](<../base/index.html#bittensor.core.extrinsics.pallets.base.CallBuilder> "bittensor.core.extrinsics.pallets.base.CallBuilder")

Factory class for creating GenericCall objects for SubtensorModule pallet functions.

This class provides methods to create GenericCall instances for all SubtensorModule pallet extrinsics.

Works with both sync (Subtensor) and async (AsyncSubtensor) instances. For async operations, pass an AsyncSubtensor instance and await the result.

Example

# Sync usage call = SubtensorModule(subtensor).start_call(netuid=14) response = subtensor.sign_and_send_extrinsic(call=call, …)

# Async usage call = await SubtensorModule(async_subtensor).start_call(netuid=14) response = await async_subtensor.sign_and_send_extrinsic(call=call, …)

add_stake(_netuid_ , _hotkey_ , _amount_staked_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.add_stake> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.add_stake.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid of the subnet to add stake to.

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey SS58 address associated with validator.

  * **amount_staked** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Amount of stake in RAO to add.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

add_stake_burn(_netuid_ , _hotkey_ , _amount_ , _limit =None_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.add_stake_burn> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.add_stake_burn.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid of the subnet to buy back on.

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey SS58 address associated with the buyback.

  * **amount** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Amount of TAO in RAO to use for the buyback.

  * **limit** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Optional limit price expressed in units of RAO per one Alpha.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

add_stake_limit(_netuid_ , _hotkey_ , _amount_staked_ , _limit_price_ , _allow_partial_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.add_stake_limit> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.add_stake_limit.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid of the subnet to add stake to.

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey SS58 address associated with validator.

  * **amount_staked** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Amount of stake in RAO to add.

  * **limit_price** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")) – The limit price expressed in units of RAO per one Alpha.

  * **allow_partial** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, allows partial unstaking if price tolerance exceeded.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

announce_coldkey_swap(_new_coldkey_hash_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.announce_coldkey_swap> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.announce_coldkey_swap.

Parameters:
    

**new_coldkey_hash** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The BlakeTwo256 hash of the new coldkey AccountId (hex string with 0x prefix).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

burned_register(_netuid_ , _hotkey_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.burned_register> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.burned_register.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid of the subnet to register on.

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey SS58 address associated with the neuron.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

claim_root(_subnets_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.claim_root> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.claim_root.

Parameters:
    

**subnets** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The netuids of the subnets to claim root for. Think about it as netuids.

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

clear_coldkey_swap_announcement()[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.clear_coldkey_swap_announcement> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.clear_coldkey_swap_announcement.

Callable by the coldkey that has an active swap announcement. Withdraws the announcement after the reannouncement delay has elapsed past the execution block.

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

commit_mechanism_weights(_netuid_ , _mecid_ , _commit_hash_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.commit_mechanism_weights> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.commit_mechanism_weights.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **mecid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet mechanism unique identifier.

  * **commit_hash** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hash of the commitment.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

commit_timelocked_mechanism_weights(_netuid_ , _mecid_ , _commit_ , _reveal_round_ , _commit_reveal_version_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.commit_timelocked_mechanism_weights> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.commit_mechanism_weights.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **mecid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet mechanism unique identifier.

  * **commit** ([_bytes_](<../../../../extras/dev_framework/calls/non_sudo_calls/index.html#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes> "bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes")) – Raw bytes of the encrypted and compressed uids & weights values for setting weights.

  * **reveal_round** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Drand round number when weights have to be revealed. Based on Drand Quicknet network.

  * **commit_reveal_version** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The version of the commit-reveal in the chain.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

decrease_take(_hotkey_ , _take_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.decrease_take> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.decrease_take.

Parameters:
    

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the hotkey to set take for.

  * **take** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The percentage of rewards that the delegate claims from nominators.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

dispute_coldkey_swap()[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.dispute_coldkey_swap> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.dispute_coldkey_swap.

Callable by the coldkey that has an active swap announcement. Marks the swap as disputed; the account is blocked until root calls reset_coldkey_swap.

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

increase_take(_hotkey_ , _take_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.increase_take> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.increase_take.

Parameters:
    

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the hotkey to set take for.

  * **take** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The percentage of rewards that the delegate claims from nominators.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

move_stake(_origin_netuid_ , _origin_hotkey_ss58_ , _destination_netuid_ , _destination_hotkey_ss58_ , _alpha_amount_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.move_stake> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.move_stake.

Parameters:
    

  * **origin_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid of the source subnet.

  * **origin_hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the source hotkey.

  * **destination_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid of the destination subnet.

  * **destination_hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the destination hotkey.

  * **alpha_amount** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Amount of origin Balance to move.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

register_limit(_netuid_ , _hotkey_ , _limit_price_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.register_limit> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.register_limit.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid of the subnet to register on.

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey SS58 address associated with the neuron.

  * **limit_price** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Maximum acceptable burn price in RAO. If on-chain burn exceeds this, the transaction fails with RegistrationPriceLimitExceeded.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

register_network(_hotkey_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.register_network> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.register_network.

Parameters:
    

**hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey SS58 address associated with the subnet owner.

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

remove_coldkey_swap_announcement(_coldkey_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.remove_coldkey_swap_announcement> "Link to this definition")
    

Returns GenericCall that resets coldkey swap for the given coldkey (root only).

Deprecated. Use [`reset_coldkey_swap()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.reset_coldkey_swap> "bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.reset_coldkey_swap") instead. This shim exists for compatibility; the runtime call is SubtensorModule.reset_coldkey_swap, which clears both announcement and dispute.

Parameters:
    

**coldkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the coldkey to reset the swap for.

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

remove_stake(_netuid_ , _hotkey_ , _amount_unstaked_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.remove_stake> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.remove_stake.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid of the subnet to remove stake from.

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey SS58 address associated with validator.

  * **amount_unstaked** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Amount of stake in RAO to remove/unstake from the validator.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

remove_stake_full_limit(_netuid_ , _hotkey_ , _limit_price =None_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.remove_stake_full_limit> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.remove_stake_full_limit.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid of the subnet to remove stake from.

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey SS58 address associated with validator.

  * **limit_price** (_Optional_ _[_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _]_) – The limit price expressed in units of RAO per one Alpha.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

remove_stake_limit(_netuid_ , _hotkey_ , _amount_unstaked_ , _limit_price_ , _allow_partial_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.remove_stake_limit> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.remove_stake_full.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid of the subnet to remove stake from.

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey SS58 address associated with validator.

  * **amount_unstaked** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Amount of stake in RAO to remove/unstake from the validator.

  * **limit_price** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")) – The limit price expressed in units of RAO per one Alpha.

  * **allow_partial** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Allows partial stake execution of the amount.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

reset_coldkey_swap(_coldkey_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.reset_coldkey_swap> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.reset_coldkey_swap.

Only callable by root. Clears the coldkey swap announcement and dispute for the given coldkey.

Parameters:
    

**coldkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the coldkey to reset the swap for.

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

reveal_mechanism_weights(_netuid_ , _mecid_ , _uids_ , _values_ , _salt_ , _version_key_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.reveal_mechanism_weights> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.reveal_mechanism_weights.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **mecid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet mechanism unique identifier.

  * **uids** ([_bittensor.core.types.UIDs_](<../../../types/index.html#bittensor.core.types.UIDs> "bittensor.core.types.UIDs")) – List of neuron UIDs for which weights are being revealed. Think like UIDs.

  * **values** ([_bittensor.core.types.Weights_](<../../../types/index.html#bittensor.core.types.Weights> "bittensor.core.types.Weights")) – List of weight values corresponding to each UID. Think like Weights.

  * **salt** ([_bittensor.core.types.Salt_](<../../../types/index.html#bittensor.core.types.Salt> "bittensor.core.types.Salt")) – The salt used to generate the hash.

  * **version_key** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Version key for compatibility with the network.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

root_register(_hotkey_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.root_register> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.root_register.

Parameters:
    

**hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey SS58 address associated with the neuron.

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

serve_axon(_netuid_ , _version_ , _ip_ , _port_ , _ip_type_ , _protocol_ , _placeholder1 =0_, _placeholder2 =0_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.serve_axon> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.serve_axon.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network uid to serve on.

  * **version** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The bittensor version identifier.

  * **ip** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Integer representation of endpoint ip.

  * **port** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Endpoint port number i.e., `9221`.

  * **ip_type** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The endpoint ip version.

  * **protocol** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – An `int` representation of the protocol.

  * **placeholder1** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Placeholder for further extra params.

  * **placeholder2** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Placeholder for further extra params.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

serve_axon_tls(_netuid_ , _version_ , _ip_ , _port_ , _ip_type_ , _protocol_ , _placeholder1 =0_, _placeholder2 =0_, _certificate =None_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.serve_axon_tls> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.serve_axon_tls.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network uid to serve on.

  * **version** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The bittensor version identifier.

  * **ip** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Integer representation of endpoint ip.

  * **port** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Endpoint port number i.e., `9221`.

  * **ip_type** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The endpoint ip version.

  * **protocol** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – An `int` representation of the protocol.

  * **placeholder1** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Placeholder for further extra params.

  * **placeholder2** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Placeholder for further extra params.

  * **certificate** (_Optional_ _[_[_bittensor.utils.Certificate_](<../../../../utils/index.html#bittensor.utils.Certificate> "bittensor.utils.Certificate") _]_) – Certificate to use for TLS. If `None`, no TLS will be used.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

set_children(_hotkey_ , _netuid_ , _children_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.set_children> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.set_children.

Parameters:
    

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey SS58 address associated with the neuron.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid of the subnet to set children for.

  * **children** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_tuple_](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)") _[_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _,_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]__]_) – List of tuples containing the proportion of stake to assign to each child hotkey.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

set_coldkey_auto_stake_hotkey(_netuid_ , _hotkey_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.set_coldkey_auto_stake_hotkey> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.set_coldkey_auto_stake_hotkey.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid of the subnet to set auto stake hotkey for.

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey SS58 address associated with the validator neuron.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

set_mechanism_weights(_netuid_ , _mecid_ , _dests_ , _weights_ , _version_key_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.set_mechanism_weights> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.set_mechanism_weights.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **mecid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet mechanism unique identifier.

  * **dests** ([_bittensor.core.types.UIDs_](<../../../types/index.html#bittensor.core.types.UIDs> "bittensor.core.types.UIDs")) – List of neuron UIDs for which weights are being revealed. Think like UIDs.

  * **weights** ([_bittensor.core.types.Weights_](<../../../types/index.html#bittensor.core.types.Weights> "bittensor.core.types.Weights")) – List of weight values corresponding to each UID.

  * **version_key** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Version key for compatibility with the network.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

set_pending_childkey_cooldown(_cooldown_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.set_pending_childkey_cooldown> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.set_pending_childkey_cooldown.

Parameters:
    

**cooldown** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The pending childkey cooldown period in seconds.

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

set_root_claim_type(_new_root_claim_type_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.set_root_claim_type> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.set_root_claim_type.

Parameters:
    

**new_root_claim_type** (_Literal_ _[__'Swap'__,__'Keep'__]__|__dict_) – The new root claim type. Can be: \- String: “Swap” or “Keep” \- Dict: {“KeepSubnets”: {“subnets”: [1, 2, 3]}}

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

set_subnet_identity(_netuid_ , _subnet_name_ , _github_repo_ , _subnet_contact_ , _subnet_url_ , _discord_ , _description_ , _logo_url_ , _additional_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.set_subnet_identity> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.set_subnet_identity.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid of the subnet to set identity for.

  * **subnet_name** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The name of the subnet.

  * **github_repo** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The GitHub repository URL of the subnet.

  * **subnet_contact** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The contact information of the subnet owner.

  * **subnet_url** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The URL of the subnet.

  * **logo_url** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The URL of the subnet logo.

  * **discord** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The Discord server URL of the subnet.

  * **description** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The description of the subnet.

  * **additional** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – Additional information about the subnet.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

start_call(_netuid_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.start_call> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.start_call.

Parameters:
    

**netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid of the subnet to to be activated.

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

swap_coldkey(_old_coldkey_ , _new_coldkey_ , _swap_cost_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.swap_coldkey> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.swap_coldkey.

Only callable by root. Performs a coldkey swap without an announcement; swap_cost is charged from old_coldkey in RAO.

Parameters:
    

  * **old_coldkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the coldkey to swap from.

  * **new_coldkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the coldkey to swap to.

  * **swap_cost** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Cost in RAO charged from old_coldkey (use 0 for no charge).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

swap_coldkey_announced(_new_coldkey_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.swap_coldkey_announced> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.swap_coldkey_announced.

Parameters:
    

**new_coldkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the new coldkey to swap to. The BlakeTwo256 hash of this coldkey must match the hash that was announced.

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

swap_stake(_hotkey_ , _origin_netuid_ , _destination_netuid_ , _alpha_amount_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.swap_stake> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.swap_stake.

Parameters:
    

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey SS58 address associated with the stake.

  * **origin_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The source subnet UID.

  * **destination_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The destination subnet UID.

  * **alpha_amount** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Amount of stake in RAO to swap.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

swap_stake_limit(_hotkey_ , _origin_netuid_ , _destination_netuid_ , _alpha_amount_ , _limit_price_ , _allow_partial_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.swap_stake_limit> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.swap_stake_limit.

Parameters:
    

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey SS58 address associated with the stake.

  * **origin_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The source subnet UID.

  * **destination_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The destination subnet UID.

  * **alpha_amount** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The amount of stake in RAO to swap.

  * **allow_partial** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If true, allows partial stake swaps when the full amount would exceed the price tolerance.

  * **limit_price** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")) – Maximum allowed increase in a price ratio (0.005 = 0.5%).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

transfer_stake(_destination_coldkey_ , _hotkey_ , _origin_netuid_ , _destination_netuid_ , _alpha_amount_)[#](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.transfer_stake> "Link to this definition")
    

Returns GenericCall instance for Subtensor function SubtensorModule.transfer_stake.

Parameters:
    

  * **destination_coldkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the destination coldkey.

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the hotkey associated with the stake.

  * **origin_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Network UID of the origin subnet.

  * **destination_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Network UID of the destination subnet.

  * **alpha_amount** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The amount of stake in RAO to transfer as a Balance object.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

[ __ previous bittensor.core.extrinsics.pallets.proxy ](<../proxy/index.html> "previous page") [ next bittensor.core.extrinsics.pallets.sudo __](<../sudo/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`SubtensorModule`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule>)
      * [`SubtensorModule.add_stake()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.add_stake>)
      * [`SubtensorModule.add_stake_burn()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.add_stake_burn>)
      * [`SubtensorModule.add_stake_limit()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.add_stake_limit>)
      * [`SubtensorModule.announce_coldkey_swap()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.announce_coldkey_swap>)
      * [`SubtensorModule.burned_register()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.burned_register>)
      * [`SubtensorModule.claim_root()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.claim_root>)
      * [`SubtensorModule.clear_coldkey_swap_announcement()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.clear_coldkey_swap_announcement>)
      * [`SubtensorModule.commit_mechanism_weights()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.commit_mechanism_weights>)
      * [`SubtensorModule.commit_timelocked_mechanism_weights()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.commit_timelocked_mechanism_weights>)
      * [`SubtensorModule.decrease_take()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.decrease_take>)
      * [`SubtensorModule.dispute_coldkey_swap()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.dispute_coldkey_swap>)
      * [`SubtensorModule.increase_take()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.increase_take>)
      * [`SubtensorModule.move_stake()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.move_stake>)
      * [`SubtensorModule.register_limit()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.register_limit>)
      * [`SubtensorModule.register_network()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.register_network>)
      * [`SubtensorModule.remove_coldkey_swap_announcement()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.remove_coldkey_swap_announcement>)
      * [`SubtensorModule.remove_stake()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.remove_stake>)
      * [`SubtensorModule.remove_stake_full_limit()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.remove_stake_full_limit>)
      * [`SubtensorModule.remove_stake_limit()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.remove_stake_limit>)
      * [`SubtensorModule.reset_coldkey_swap()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.reset_coldkey_swap>)
      * [`SubtensorModule.reveal_mechanism_weights()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.reveal_mechanism_weights>)
      * [`SubtensorModule.root_register()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.root_register>)
      * [`SubtensorModule.serve_axon()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.serve_axon>)
      * [`SubtensorModule.serve_axon_tls()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.serve_axon_tls>)
      * [`SubtensorModule.set_children()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.set_children>)
      * [`SubtensorModule.set_coldkey_auto_stake_hotkey()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.set_coldkey_auto_stake_hotkey>)
      * [`SubtensorModule.set_mechanism_weights()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.set_mechanism_weights>)
      * [`SubtensorModule.set_pending_childkey_cooldown()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.set_pending_childkey_cooldown>)
      * [`SubtensorModule.set_root_claim_type()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.set_root_claim_type>)
      * [`SubtensorModule.set_subnet_identity()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.set_subnet_identity>)
      * [`SubtensorModule.start_call()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.start_call>)
      * [`SubtensorModule.swap_coldkey()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.swap_coldkey>)
      * [`SubtensorModule.swap_coldkey_announced()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.swap_coldkey_announced>)
      * [`SubtensorModule.swap_stake()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.swap_stake>)
      * [`SubtensorModule.swap_stake_limit()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.swap_stake_limit>)
      * [`SubtensorModule.transfer_stake()`](<#bittensor.core.extrinsics.pallets.subtensor_module.SubtensorModule.transfer_stake>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.