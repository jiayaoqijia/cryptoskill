# bittensor.core.extrinsics.pallets.admin_utils &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/pallets/admin_utils/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/pallets/admin_utils/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../../_sources/autoapi/bittensor/core/extrinsics/pallets/admin_utils/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.pallets.admin_utils

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`AdminUtils`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils>)
      * [`AdminUtils.schedule_grandpa_change()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.schedule_grandpa_change>)
      * [`AdminUtils.sudo_set_activity_cutoff()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_activity_cutoff>)
      * [`AdminUtils.sudo_set_adjustment_alpha()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_adjustment_alpha>)
      * [`AdminUtils.sudo_set_adjustment_interval()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_adjustment_interval>)
      * [`AdminUtils.sudo_set_admin_freeze_window()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_admin_freeze_window>)
      * [`AdminUtils.sudo_set_alpha_sigmoid_steepness()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_alpha_sigmoid_steepness>)
      * [`AdminUtils.sudo_set_alpha_values()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_alpha_values>)
      * [`AdminUtils.sudo_set_bonds_moving_average()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_bonds_moving_average>)
      * [`AdminUtils.sudo_set_bonds_penalty()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_bonds_penalty>)
      * [`AdminUtils.sudo_set_bonds_reset_enabled()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_bonds_reset_enabled>)
      * [`AdminUtils.sudo_set_ck_burn()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_ck_burn>)
      * [`AdminUtils.sudo_set_coldkey_swap_schedule_duration()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_coldkey_swap_schedule_duration>)
      * [`AdminUtils.sudo_set_commit_reveal_version()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_commit_reveal_version>)
      * [`AdminUtils.sudo_set_commit_reveal_weights_enabled()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_commit_reveal_weights_enabled>)
      * [`AdminUtils.sudo_set_commit_reveal_weights_interval()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_commit_reveal_weights_interval>)
      * [`AdminUtils.sudo_set_default_take()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_default_take>)
      * [`AdminUtils.sudo_set_difficulty()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_difficulty>)
      * [`AdminUtils.sudo_set_dissolve_network_schedule_duration()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_dissolve_network_schedule_duration>)
      * [`AdminUtils.sudo_set_ema_price_halving_period()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_ema_price_halving_period>)
      * [`AdminUtils.sudo_set_evm_chain_id()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_evm_chain_id>)
      * [`AdminUtils.sudo_set_immunity_period()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_immunity_period>)
      * [`AdminUtils.sudo_set_kappa()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_kappa>)
      * [`AdminUtils.sudo_set_liquid_alpha_enabled()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_liquid_alpha_enabled>)
      * [`AdminUtils.sudo_set_lock_reduction_interval()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_lock_reduction_interval>)
      * [`AdminUtils.sudo_set_max_allowed_uids()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_max_allowed_uids>)
      * [`AdminUtils.sudo_set_max_allowed_validators()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_max_allowed_validators>)
      * [`AdminUtils.sudo_set_max_burn()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_max_burn>)
      * [`AdminUtils.sudo_set_max_difficulty()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_max_difficulty>)
      * [`AdminUtils.sudo_set_max_registrations_per_block()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_max_registrations_per_block>)
      * [`AdminUtils.sudo_set_mechanism_count()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_mechanism_count>)
      * [`AdminUtils.sudo_set_mechanism_emission_split()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_mechanism_emission_split>)
      * [`AdminUtils.sudo_set_min_allowed_uids()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_min_allowed_uids>)
      * [`AdminUtils.sudo_set_min_allowed_weights()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_min_allowed_weights>)
      * [`AdminUtils.sudo_set_min_burn()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_min_burn>)
      * [`AdminUtils.sudo_set_min_delegate_take()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_min_delegate_take>)
      * [`AdminUtils.sudo_set_min_difficulty()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_min_difficulty>)
      * [`AdminUtils.sudo_set_network_immunity_period()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_network_immunity_period>)
      * [`AdminUtils.sudo_set_network_min_lock_cost()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_network_min_lock_cost>)
      * [`AdminUtils.sudo_set_network_pow_registration_allowed()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_network_pow_registration_allowed>)
      * [`AdminUtils.sudo_set_network_rate_limit()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_network_rate_limit>)
      * [`AdminUtils.sudo_set_network_registration_allowed()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_network_registration_allowed>)
      * [`AdminUtils.sudo_set_nominator_min_required_stake()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_nominator_min_required_stake>)
      * [`AdminUtils.sudo_set_owner_hparam_rate_limit()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_owner_hparam_rate_limit>)
      * [`AdminUtils.sudo_set_owner_immune_neuron_limit()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_owner_immune_neuron_limit>)
      * [`AdminUtils.sudo_set_rao_recycled()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_rao_recycled>)
      * [`AdminUtils.sudo_set_recycle_or_burn()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_recycle_or_burn>)
      * [`AdminUtils.sudo_set_rho()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_rho>)
      * [`AdminUtils.sudo_set_serving_rate_limit()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_serving_rate_limit>)
      * [`AdminUtils.sudo_set_sn_owner_hotkey()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_sn_owner_hotkey>)
      * [`AdminUtils.sudo_set_stake_threshold()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_stake_threshold>)
      * [`AdminUtils.sudo_set_subnet_limit()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_subnet_limit>)
      * [`AdminUtils.sudo_set_subnet_moving_alpha()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_subnet_moving_alpha>)
      * [`AdminUtils.sudo_set_subnet_owner_cut()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_subnet_owner_cut>)
      * [`AdminUtils.sudo_set_subnet_owner_hotkey()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_subnet_owner_hotkey>)
      * [`AdminUtils.sudo_set_subtoken_enabled()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_subtoken_enabled>)
      * [`AdminUtils.sudo_set_tao_flow_cutoff()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_tao_flow_cutoff>)
      * [`AdminUtils.sudo_set_tao_flow_normalization_exponent()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_tao_flow_normalization_exponent>)
      * [`AdminUtils.sudo_set_tao_flow_smoothing_factor()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_tao_flow_smoothing_factor>)
      * [`AdminUtils.sudo_set_target_registrations_per_interval()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_target_registrations_per_interval>)
      * [`AdminUtils.sudo_set_tempo()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_tempo>)
      * [`AdminUtils.sudo_set_toggle_transfer()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_toggle_transfer>)
      * [`AdminUtils.sudo_set_total_issuance()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_total_issuance>)
      * [`AdminUtils.sudo_set_tx_delegate_take_rate_limit()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_tx_delegate_take_rate_limit>)
      * [`AdminUtils.sudo_set_tx_rate_limit()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_tx_rate_limit>)
      * [`AdminUtils.sudo_set_weights_set_rate_limit()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_weights_set_rate_limit>)
      * [`AdminUtils.sudo_set_weights_version_key()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_weights_version_key>)
      * [`AdminUtils.sudo_set_yuma3_enabled()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_yuma3_enabled>)
      * [`AdminUtils.sudo_toggle_evm_precompile()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_toggle_evm_precompile>)
      * [`AdminUtils.sudo_trim_to_max_allowed_uids()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_trim_to_max_allowed_uids>)
      * [`AdminUtils.swap_authorities()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.swap_authorities>)



# bittensor.core.extrinsics.pallets.admin_utils[#](<#module-bittensor.core.extrinsics.pallets.admin_utils> "Link to this heading")

WARNING: This module contains administrative utilities that should ONLY be used for local development and testing purposes. These functions provide direct access to critical network parameters and should never be used in production environments as they can potentially disrupt network stability.

The AdminUtils module contains powerful administrative functions that can modify core network parameters. Improper use of these functions outside of development/testing contexts could have severe consequences for network operation.

## Classes[#](<#classes> "Link to this heading")

[`AdminUtils`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils> "bittensor.core.extrinsics.pallets.admin_utils.AdminUtils") | Factory class for creating GenericCall objects for AdminUtils pallet functions.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.extrinsics.pallets.admin_utils.AdminUtils[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils> "Link to this definition")
    

Bases: [`bittensor.core.extrinsics.pallets.base.CallBuilder`](<../base/index.html#bittensor.core.extrinsics.pallets.base.CallBuilder> "bittensor.core.extrinsics.pallets.base.CallBuilder")

Factory class for creating GenericCall objects for AdminUtils pallet functions.

This class provides methods to create GenericCall instances for all AdminUtils pallet extrinsics.

Works with both sync (Subtensor) and async (AsyncSubtensor) instances. For async operations, pass an AsyncSubtensor instance and await the result.

Example

# Sync usage call = AdminUtils(subtensor).sudo_set_default_take(default_take=100) response = subtensor.sign_and_send_extrinsic(call=call, …)

# Async usage call = await AdminUtils(async_subtensor).sudo_set_default_take(default_take=100) response = await async_subtensor.sign_and_send_extrinsic(call=call, …)

schedule_grandpa_change(_next_authorities_ , _in_blocks_ , _forced =None_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.schedule_grandpa_change> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function schedule_grandpa_change.

A public interface for pallet_grandpa::Pallet::schedule_grandpa_change.

Schedule a change in the authorities.

The change will be applied at the end of execution of the block in_blocks after the current block. This value may be 0, in which case the change is applied at the end of the current block.

If the forced parameter is defined, this indicates that the current set has been synchronously determined to be offline and that after in_blocks the given change should be applied. The given block number indicates the median last finalized block number and it should be used as the canon block when starting the new grandpa voter.

No change should be signaled while any change is pending. Returns an error if a change is already pending.

Parameters:
    

  * **next_authorities** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_tuple_](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)") _]_) – The list of next authorities (AuthorityList).

  * **in_blocks** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The number of blocks after which the change is applied.

  * **forced** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Optional block number for forced change.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_activity_cutoff(_netuid_ , _activity_cutoff_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_activity_cutoff> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_activity_cutoff.

The extrinsic sets the activity cutoff for a subnet. It is only callable by the root account or subnet owner. The extrinsic will call the Subtensor pallet to set the activity cutoff.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **activity_cutoff** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The activity cutoff value (u16).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_adjustment_alpha(_netuid_ , _adjustment_alpha_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_adjustment_alpha> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_adjustment_alpha.

The extrinsic sets the adjustment alpha for a subnet. It is only callable by the root account or subnet owner. The extrinsic will call the Subtensor pallet to set the adjustment alpha.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **adjustment_alpha** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The adjustment alpha value (u64).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_adjustment_interval(_netuid_ , _adjustment_interval_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_adjustment_interval> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_adjustment_interval.

The extrinsic sets the adjustment interval for a subnet. It is only callable by the root account, not changeable by the subnet owner. The extrinsic will call the Subtensor pallet to set the adjustment interval.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **adjustment_interval** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The adjustment interval (u16).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_admin_freeze_window(_window_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_admin_freeze_window> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_admin_freeze_window.

Sets the admin freeze window length (in blocks) at the end of a tempo. Only callable by root.

Parameters:
    

**window** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The admin freeze window length in blocks (u16).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_alpha_sigmoid_steepness(_netuid_ , _steepness_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_alpha_sigmoid_steepness> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_alpha_sigmoid_steepness.

Sets the Steepness for the alpha sigmoid function.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier for the subnet.

  * **steepness** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The Steepness for the alpha sigmoid function. (range is 0-int16::MAX, negative values are reserved for future use).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_alpha_values(_netuid_ , _alpha_low_ , _alpha_high_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_alpha_values> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_alpha_values.

Sets values for liquid alpha.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **alpha_low** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The low alpha value (u16).

  * **alpha_high** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The high alpha value (u16).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_bonds_moving_average(_netuid_ , _bonds_moving_average_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_bonds_moving_average> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_bonds_moving_average.

The extrinsic sets the bonds moving average for a subnet. It is only callable by the root account or subnet owner. The extrinsic will call the Subtensor pallet to set the bonds moving average.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **bonds_moving_average** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The bonds moving average value (u64).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_bonds_penalty(_netuid_ , _bonds_penalty_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_bonds_penalty> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_bonds_penalty.

The extrinsic sets the bonds penalty for a subnet. It is only callable by the root account or subnet owner. The extrinsic will call the Subtensor pallet to set the bonds penalty.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **bonds_penalty** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The bonds penalty value (u16).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_bonds_reset_enabled(_netuid_ , _enabled_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_bonds_reset_enabled> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_bonds_reset_enabled.

Enables or disables Bonds Reset for a given subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier for the subnet.

  * **enabled** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – A boolean flag to enable or disable Bonds Reset.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_ck_burn(_burn_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_ck_burn> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_ck_burn.

Sets the childkey burn for a subnet. It is only callable by the root account. The extrinsic will call the Subtensor pallet to set the childkey burn.

Parameters:
    

**burn** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The childkey burn value (u64).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_coldkey_swap_schedule_duration(_duration_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_coldkey_swap_schedule_duration> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_coldkey_swap_schedule_duration.

Sets the duration of the coldkey swap schedule.

This extrinsic allows the root account to set the duration for the coldkey swap schedule. The coldkey swap schedule determines how long it takes for a coldkey swap operation to complete.

Parameters:
    

**duration** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The new duration for the coldkey swap schedule, in number of blocks.

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_commit_reveal_version(_version_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_commit_reveal_version> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_commit_reveal_version.

Sets the commit-reveal weights version for all subnets.

Parameters:
    

**version** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The commit-reveal weights version (u16).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_commit_reveal_weights_enabled(_netuid_ , _enabled_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_commit_reveal_weights_enabled> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_commit_reveal_weights_enabled.

The extrinsic enabled/disables commit/reaveal for a given subnet. It is only callable by the root account or subnet owner. The extrinsic will call the Subtensor pallet to set the value.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **enabled** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether commit/reveal weights is enabled (bool).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_commit_reveal_weights_interval(_netuid_ , _interval_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_commit_reveal_weights_interval> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_commit_reveal_weights_interval.

Sets the commit-reveal weights periods for a specific subnet.

This extrinsic allows the subnet owner or root account to set the duration (in epochs) during which committed weights must be revealed. The commit-reveal mechanism ensures that users commit weights in advance and reveal them only within a specified period.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet for which the periods are being set.

  * **interval** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The number of epochs that define the commit-reveal period.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_default_take(_default_take_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_default_take> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_default_take.

The extrinsic sets the default take for the network. It is only callable by the root account. The extrinsic will call the Subtensor pallet to set the default take.

Parameters:
    

**default_take** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The default take value (u16).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_difficulty(_netuid_ , _difficulty_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_difficulty> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_difficulty.

The extrinsic sets the difficulty for a subnet. It is only callable by the root account or subnet owner. The extrinsic will call the Subtensor pallet to set the difficulty.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **difficulty** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The difficulty value (u64).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_dissolve_network_schedule_duration(_duration_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_dissolve_network_schedule_duration> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_dissolve_network_schedule_duration.

Sets the duration of the dissolve network schedule.

This extrinsic allows the root account to set the duration for the dissolve network schedule. The dissolve network schedule determines how long it takes for a network dissolution operation to complete.

Parameters:
    

**duration** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The new duration for the dissolve network schedule, in number of blocks.

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_ema_price_halving_period(_netuid_ , _ema_halving_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_ema_price_halving_period> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_ema_price_halving_period.

Sets the number of blocks for EMA price to halve.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier for the subnet.

  * **ema_halving** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Number of blocks for EMA price to halve.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_evm_chain_id(_chain_id_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_evm_chain_id> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_evm_chain_id.

Sets the EVM ChainID.

Parameters:
    

**chain_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The u64 chain ID.

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_immunity_period(_netuid_ , _immunity_period_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_immunity_period> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_immunity_period.

The extrinsic sets the immunity period for a subnet. It is only callable by the root account or subnet owner. The extrinsic will call the Subtensor pallet to set the immunity period.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **immunity_period** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The immunity period (u16).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_kappa(_netuid_ , _kappa_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_kappa> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_kappa.

The extrinsic sets the kappa for a subnet. It is only callable by the root account or subnet owner. The extrinsic will call the Subtensor pallet to set the kappa.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **kappa** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The kappa value (u16).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_liquid_alpha_enabled(_netuid_ , _enabled_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_liquid_alpha_enabled> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_liquid_alpha_enabled.

Enables or disables Liquid Alpha for a given subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier for the subnet.

  * **enabled** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – A boolean flag to enable or disable Liquid Alpha.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_lock_reduction_interval(_interval_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_lock_reduction_interval> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_lock_reduction_interval.

The extrinsic sets the lock reduction interval for the network. It is only callable by the root account. The extrinsic will call the Subtensor pallet to set the lock reduction interval.

Parameters:
    

**interval** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The lock reduction interval (u64).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_max_allowed_uids(_netuid_ , _max_allowed_uids_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_max_allowed_uids> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_max_allowed_uids.

The extrinsic sets the maximum allowed UIDs for a subnet. It is only callable by the root account and subnet owner. The extrinsic will call the Subtensor pallet to set the maximum allowed UIDs for a subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **max_allowed_uids** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The maximum allowed UIDs (u16).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_max_allowed_validators(_netuid_ , _max_allowed_validators_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_max_allowed_validators> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_max_allowed_validators.

The extrinsic sets the maximum allowed validators for a subnet. It is only callable by the root account. The extrinsic will call the Subtensor pallet to set the maximum allowed validators.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **max_allowed_validators** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The maximum allowed validators (u16).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_max_burn(_netuid_ , _max_burn_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_max_burn> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_max_burn.

The extrinsic sets the maximum burn for a subnet. It is only callable by root and subnet owner. The extrinsic will call the Subtensor pallet to set the maximum burn.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **max_burn** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The maximum burn value in RAO (TaoCurrency).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_max_difficulty(_netuid_ , _max_difficulty_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_max_difficulty> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_max_difficulty.

The extrinsic sets the maximum difficulty for a subnet. It is only callable by the root account or subnet owner. The extrinsic will call the Subtensor pallet to set the maximum difficulty.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **max_difficulty** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The maximum difficulty value (u64).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_max_registrations_per_block(_netuid_ , _max_registrations_per_block_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_max_registrations_per_block> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_max_registrations_per_block.

The extrinsic sets the maximum registrations per block for a subnet. It is only callable by the root account. The extrinsic will call the Subtensor pallet to set the maximum registrations per block.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **max_registrations_per_block** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The maximum registrations per block (u16).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_mechanism_count(_netuid_ , _mechanism_count_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_mechanism_count> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_mechanism_count.

Sets the desired number of mechanisms in a subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **mechanism_count** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The desired number of mechanisms (MechId).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_mechanism_emission_split(_netuid_ , _maybe_split =None_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_mechanism_emission_split> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_mechanism_emission_split.

Sets the emission split between mechanisms in a subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **maybe_split** (_Optional_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]__]_) – Optional list of emission split values (Option<Vec<u16>>).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_min_allowed_uids(_netuid_ , _min_allowed_uids_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_min_allowed_uids> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_min_allowed_uids.

The extrinsic sets the minimum allowed UIDs for a subnet. It is only callable by the root account.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **min_allowed_uids** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The minimum allowed UIDs (u16).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_min_allowed_weights(_netuid_ , _min_allowed_weights_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_min_allowed_weights> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_min_allowed_weights.

The extrinsic sets the minimum allowed weights for a subnet. It is only callable by the root account or subnet owner. The extrinsic will call the Subtensor pallet to set the minimum allowed weights.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **min_allowed_weights** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The minimum allowed weights (u16).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_min_burn(_netuid_ , _min_burn_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_min_burn> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_min_burn.

The extrinsic sets the minimum burn for a subnet. It is only callable by root and subnet owner. The extrinsic will call the Subtensor pallet to set the minimum burn.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **min_burn** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The minimum burn value in RAO (TaoCurrency).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_min_delegate_take(_take_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_min_delegate_take> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_min_delegate_take.

The extrinsic sets the minimum delegate take. It is only callable by the root account. The extrinsic will call the Subtensor pallet to set the minimum delegate take.

Parameters:
    

**take** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The minimum delegate take value (u16).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_min_difficulty(_netuid_ , _min_difficulty_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_min_difficulty> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_min_difficulty.

The extrinsic sets the minimum difficulty for a subnet. It is only callable by the root account or subnet owner. The extrinsic will call the Subtensor pallet to set the minimum difficulty.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **min_difficulty** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The minimum difficulty value (u64).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_network_immunity_period(_immunity_period_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_network_immunity_period> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_network_immunity_period.

The extrinsic sets the immunity period for the network. It is only callable by the root account. The extrinsic will call the Subtensor pallet to set the immunity period for the network.

Parameters:
    

**immunity_period** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The immunity period (u64).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_network_min_lock_cost(_lock_cost_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_network_min_lock_cost> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_network_min_lock_cost.

The extrinsic sets the min lock cost for the network. It is only callable by the root account. The extrinsic will call the Subtensor pallet to set the min lock cost for the network.

Parameters:
    

**lock_cost** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The lock cost value in RAO (TaoCurrency).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_network_pow_registration_allowed(_netuid_ , _registration_allowed_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_network_pow_registration_allowed> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_network_pow_registration_allowed.

The extrinsic sets the network PoW registration allowed for a subnet. It is only callable by the root account or subnet owner. The extrinsic will call the Subtensor pallet to set the network PoW registration allowed.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **registration_allowed** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether PoW registration is allowed (bool).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_network_rate_limit(_rate_limit_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_network_rate_limit> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_network_rate_limit.

The extrinsic sets the network rate limit for the network. It is only callable by the root account. The extrinsic will call the Subtensor pallet to set the network rate limit.

Parameters:
    

**rate_limit** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network rate limit (u64).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_network_registration_allowed(_netuid_ , _registration_allowed_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_network_registration_allowed> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_network_registration_allowed.

The extrinsic sets the network registration allowed for a subnet. It is only callable by the root account or subnet owner. The extrinsic will call the Subtensor pallet to set the network registration allowed.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **registration_allowed** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether registration is allowed (bool).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_nominator_min_required_stake(_min_stake_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_nominator_min_required_stake> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_nominator_min_required_stake.

The extrinsic sets the minimum stake required for nominators. It is only callable by the root account. The extrinsic will call the Subtensor pallet to set the minimum stake required for nominators.

Parameters:
    

**min_stake** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The minimum stake required for nominators (u64).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_owner_hparam_rate_limit(_epochs_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_owner_hparam_rate_limit> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_owner_hparam_rate_limit.

Sets the owner hyperparameter rate limit in epochs (global multiplier). Only callable by root.

Parameters:
    

**epochs** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The owner hyperparameter rate limit in epochs (u16).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_owner_immune_neuron_limit(_netuid_ , _immune_neurons_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_owner_immune_neuron_limit> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_owner_immune_neuron_limit.

Sets the number of immune owner neurons.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **immune_neurons** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The number of immune owner neurons (u16).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_rao_recycled(_netuid_ , _rao_recycled_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_rao_recycled> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_rao_recycled.

The extrinsic sets the recycled RAO for a subnet. It is only callable by the root account. The extrinsic will call the Subtensor pallet to set the recycled RAO.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **rao_recycled** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The recycled RAO value in RAO (TaoCurrency).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_recycle_or_burn(_netuid_ , _recycle_or_burn_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_recycle_or_burn> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_recycle_or_burn.

Set the behaviour of the “burn” UID(s) for a given subnet. If set to Burn, the miner emission sent to the burn UID(s) will be burned. If set to Recycle, the miner emission sent to the burn UID(s) will be recycled.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier for the subnet.

  * **recycle_or_burn** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The desired behaviour of the “burn” UID(s) for the subnet.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_rho(_netuid_ , _rho_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_rho> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_rho.

The extrinsic sets the rho for a subnet. It is only callable by the root account or subnet owner. The extrinsic will call the Subtensor pallet to set the rho.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **rho** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The rho value (u16).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_serving_rate_limit(_netuid_ , _serving_rate_limit_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_serving_rate_limit> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_serving_rate_limit.

The extrinsic sets the serving rate limit for a subnet. It is only callable by the root account or subnet owner. The extrinsic will call the Subtensor pallet to set the serving rate limit.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **serving_rate_limit** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The serving rate limit (u64).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_sn_owner_hotkey(_netuid_ , _hotkey_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_sn_owner_hotkey> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_sn_owner_hotkey.

Sets or updates the hotkey account associated with the owner of a specific subnet.

This function allows either the root origin or the current subnet owner to set or update the hotkey for a given subnet. The subnet must already exist. To prevent abuse, the call is rate-limited to once per configured interval (default: one week) per subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet whose owner hotkey is being set.

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The new hotkey account to associate with the subnet owner.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_stake_threshold(_min_stake_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_stake_threshold> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_stake_threshold.

The extrinsic sets the weights min stake. It is only callable by the root account. The extrinsic will call the Subtensor pallet to set the weights min stake.

Parameters:
    

**min_stake** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The minimum stake value (u64).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_subnet_limit(_max_subnets_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_subnet_limit> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_subnet_limit.

The extrinsic sets the subnet limit for the network. It is only callable by the root account. The extrinsic will call the Subtensor pallet to set the subnet limit.

Parameters:
    

**max_subnets** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The maximum number of subnets (u16).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_subnet_moving_alpha(_alpha_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_subnet_moving_alpha> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_subnet_moving_alpha.

Sets the new moving alpha value for the SubnetMovingAlpha.

Parameters:
    

**alpha** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")) – The new moving alpha value (I96F32).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_subnet_owner_cut(_subnet_owner_cut_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_subnet_owner_cut> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_subnet_owner_cut.

The extrinsic sets the subnet owner cut for a subnet. It is only callable by the root account. The extrinsic will call the Subtensor pallet to set the subnet owner cut.

Parameters:
    

**subnet_owner_cut** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet owner cut value (u16).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_subnet_owner_hotkey(_netuid_ , _hotkey_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_subnet_owner_hotkey> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_subnet_owner_hotkey.

Change the SubnetOwnerHotkey for a given subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier for the subnet.

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The new hotkey for the subnet owner.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_subtoken_enabled(_netuid_ , _subtoken_enabled_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_subtoken_enabled> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_subtoken_enabled.

Enables or disables subtoken trading for a given subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **subtoken_enabled** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – A boolean indicating whether subtoken trading should be enabled or disabled.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_tao_flow_cutoff(_flow_cutoff_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_tao_flow_cutoff> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_tao_flow_cutoff.

Sets TAO flow cutoff value (A).

Parameters:
    

**flow_cutoff** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")) – The TAO flow cutoff value (I64F64).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_tao_flow_normalization_exponent(_exponent_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_tao_flow_normalization_exponent> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_tao_flow_normalization_exponent.

Sets TAO flow normalization exponent (p).

Parameters:
    

**exponent** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")) – The TAO flow normalization exponent (U64F64).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_tao_flow_smoothing_factor(_smoothing_factor_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_tao_flow_smoothing_factor> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_tao_flow_smoothing_factor.

Sets TAO flow smoothing factor (alpha).

Parameters:
    

**smoothing_factor** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The TAO flow smoothing factor (u64).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_target_registrations_per_interval(_netuid_ , _target_registrations_per_interval_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_target_registrations_per_interval> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_target_registrations_per_interval.

The extrinsic sets the target registrations per interval for a subnet. It is only callable by the root account. The extrinsic will call the Subtensor pallet to set the target registrations per interval.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **target_registrations_per_interval** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The target registrations per interval (u16).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_tempo(_netuid_ , _tempo_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_tempo> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_tempo.

The extrinsic sets the tempo for a subnet. It is only callable by the root account. The extrinsic will call the Subtensor pallet to set the tempo.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **tempo** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The tempo value (u16).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_toggle_transfer(_netuid_ , _toggle_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_toggle_transfer> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_toggle_transfer.

Enable or disable atomic alpha transfers for a given subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier for the subnet.

  * **toggle** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – A boolean flag to enable or disable Liquid Alpha.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_total_issuance(_total_issuance_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_total_issuance> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_total_issuance.

The extrinsic sets the total issuance for the network. It is only callable by the root account. The extrinsic will call the Subtensor pallet to set the issuance for the network.

Parameters:
    

**total_issuance** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The total issuance value in RAO (TaoCurrency).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_tx_delegate_take_rate_limit(_tx_rate_limit_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_tx_delegate_take_rate_limit> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_tx_delegate_take_rate_limit.

The extrinsic sets the rate limit for delegate take transactions. It is only callable by the root account. The extrinsic will call the Subtensor pallet to set the rate limit for delegate take transactions.

Parameters:
    

**tx_rate_limit** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The transaction rate limit (u64).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_tx_rate_limit(_tx_rate_limit_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_tx_rate_limit> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_tx_rate_limit.

The extrinsic sets the transaction rate limit for the network. It is only callable by the root account. The extrinsic will call the Subtensor pallet to set the transaction rate limit.

Parameters:
    

**tx_rate_limit** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The transaction rate limit (u64).

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_weights_set_rate_limit(_netuid_ , _weights_set_rate_limit_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_weights_set_rate_limit> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_weights_set_rate_limit.

The extrinsic sets the weights set rate limit for a subnet. It is only callable by the root account. The extrinsic will call the Subtensor pallet to set the weights set rate limit.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **weights_set_rate_limit** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The weights set rate limit (u64).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_weights_version_key(_netuid_ , _weights_version_key_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_weights_version_key> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_weights_version_key.

The extrinsic sets the weights version key for a subnet. It is only callable by the root account or subnet owner. The extrinsic will call the Subtensor pallet to set the weights version key.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **weights_version_key** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The weights version key (u64).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_set_yuma3_enabled(_netuid_ , _enabled_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_yuma3_enabled> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_set_yuma3_enabled.

Enables or disables Yuma3 for a given subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier for the subnet.

  * **enabled** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – A boolean flag to enable or disable Yuma3.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_toggle_evm_precompile(_precompile_id_ , _enabled_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_toggle_evm_precompile> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_toggle_evm_precompile.

Toggles the enablement of an EVM precompile.

Parameters:
    

  * **precompile_id** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The identifier of the EVM precompile to toggle.

  * **enabled** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – The new enablement state of the precompile.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

sudo_trim_to_max_allowed_uids(_netuid_ , _max_n_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_trim_to_max_allowed_uids> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function sudo_trim_to_max_allowed_uids.

Trims the maximum number of UIDs for a subnet.

The trimming is done by sorting the UIDs by emission descending and then trimming the lowest emitters while preserving temporally and owner immune UIDs. The UIDs are then compressed to the left and storage is migrated to the new compressed UIDs.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network identifier.

  * **max_n** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The maximum number of UIDs (u16).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

swap_authorities(_new_authorities_)[#](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.swap_authorities> "Link to this definition")
    

Returns GenericCall instance for AdminUtils function swap_authorities.

The extrinsic sets the new authorities for Aura consensus. It is only callable by the root account. The extrinsic will call the Aura pallet to change the authorities.

Parameters:
    

**new_authorities** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – List of new authority identifiers.

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

[ __ previous bittensor.core.extrinsics.pallets ](<../index.html> "previous page") [ next bittensor.core.extrinsics.pallets.balances __](<../balances/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`AdminUtils`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils>)
      * [`AdminUtils.schedule_grandpa_change()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.schedule_grandpa_change>)
      * [`AdminUtils.sudo_set_activity_cutoff()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_activity_cutoff>)
      * [`AdminUtils.sudo_set_adjustment_alpha()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_adjustment_alpha>)
      * [`AdminUtils.sudo_set_adjustment_interval()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_adjustment_interval>)
      * [`AdminUtils.sudo_set_admin_freeze_window()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_admin_freeze_window>)
      * [`AdminUtils.sudo_set_alpha_sigmoid_steepness()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_alpha_sigmoid_steepness>)
      * [`AdminUtils.sudo_set_alpha_values()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_alpha_values>)
      * [`AdminUtils.sudo_set_bonds_moving_average()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_bonds_moving_average>)
      * [`AdminUtils.sudo_set_bonds_penalty()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_bonds_penalty>)
      * [`AdminUtils.sudo_set_bonds_reset_enabled()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_bonds_reset_enabled>)
      * [`AdminUtils.sudo_set_ck_burn()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_ck_burn>)
      * [`AdminUtils.sudo_set_coldkey_swap_schedule_duration()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_coldkey_swap_schedule_duration>)
      * [`AdminUtils.sudo_set_commit_reveal_version()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_commit_reveal_version>)
      * [`AdminUtils.sudo_set_commit_reveal_weights_enabled()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_commit_reveal_weights_enabled>)
      * [`AdminUtils.sudo_set_commit_reveal_weights_interval()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_commit_reveal_weights_interval>)
      * [`AdminUtils.sudo_set_default_take()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_default_take>)
      * [`AdminUtils.sudo_set_difficulty()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_difficulty>)
      * [`AdminUtils.sudo_set_dissolve_network_schedule_duration()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_dissolve_network_schedule_duration>)
      * [`AdminUtils.sudo_set_ema_price_halving_period()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_ema_price_halving_period>)
      * [`AdminUtils.sudo_set_evm_chain_id()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_evm_chain_id>)
      * [`AdminUtils.sudo_set_immunity_period()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_immunity_period>)
      * [`AdminUtils.sudo_set_kappa()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_kappa>)
      * [`AdminUtils.sudo_set_liquid_alpha_enabled()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_liquid_alpha_enabled>)
      * [`AdminUtils.sudo_set_lock_reduction_interval()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_lock_reduction_interval>)
      * [`AdminUtils.sudo_set_max_allowed_uids()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_max_allowed_uids>)
      * [`AdminUtils.sudo_set_max_allowed_validators()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_max_allowed_validators>)
      * [`AdminUtils.sudo_set_max_burn()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_max_burn>)
      * [`AdminUtils.sudo_set_max_difficulty()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_max_difficulty>)
      * [`AdminUtils.sudo_set_max_registrations_per_block()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_max_registrations_per_block>)
      * [`AdminUtils.sudo_set_mechanism_count()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_mechanism_count>)
      * [`AdminUtils.sudo_set_mechanism_emission_split()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_mechanism_emission_split>)
      * [`AdminUtils.sudo_set_min_allowed_uids()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_min_allowed_uids>)
      * [`AdminUtils.sudo_set_min_allowed_weights()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_min_allowed_weights>)
      * [`AdminUtils.sudo_set_min_burn()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_min_burn>)
      * [`AdminUtils.sudo_set_min_delegate_take()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_min_delegate_take>)
      * [`AdminUtils.sudo_set_min_difficulty()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_min_difficulty>)
      * [`AdminUtils.sudo_set_network_immunity_period()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_network_immunity_period>)
      * [`AdminUtils.sudo_set_network_min_lock_cost()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_network_min_lock_cost>)
      * [`AdminUtils.sudo_set_network_pow_registration_allowed()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_network_pow_registration_allowed>)
      * [`AdminUtils.sudo_set_network_rate_limit()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_network_rate_limit>)
      * [`AdminUtils.sudo_set_network_registration_allowed()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_network_registration_allowed>)
      * [`AdminUtils.sudo_set_nominator_min_required_stake()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_nominator_min_required_stake>)
      * [`AdminUtils.sudo_set_owner_hparam_rate_limit()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_owner_hparam_rate_limit>)
      * [`AdminUtils.sudo_set_owner_immune_neuron_limit()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_owner_immune_neuron_limit>)
      * [`AdminUtils.sudo_set_rao_recycled()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_rao_recycled>)
      * [`AdminUtils.sudo_set_recycle_or_burn()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_recycle_or_burn>)
      * [`AdminUtils.sudo_set_rho()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_rho>)
      * [`AdminUtils.sudo_set_serving_rate_limit()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_serving_rate_limit>)
      * [`AdminUtils.sudo_set_sn_owner_hotkey()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_sn_owner_hotkey>)
      * [`AdminUtils.sudo_set_stake_threshold()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_stake_threshold>)
      * [`AdminUtils.sudo_set_subnet_limit()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_subnet_limit>)
      * [`AdminUtils.sudo_set_subnet_moving_alpha()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_subnet_moving_alpha>)
      * [`AdminUtils.sudo_set_subnet_owner_cut()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_subnet_owner_cut>)
      * [`AdminUtils.sudo_set_subnet_owner_hotkey()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_subnet_owner_hotkey>)
      * [`AdminUtils.sudo_set_subtoken_enabled()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_subtoken_enabled>)
      * [`AdminUtils.sudo_set_tao_flow_cutoff()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_tao_flow_cutoff>)
      * [`AdminUtils.sudo_set_tao_flow_normalization_exponent()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_tao_flow_normalization_exponent>)
      * [`AdminUtils.sudo_set_tao_flow_smoothing_factor()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_tao_flow_smoothing_factor>)
      * [`AdminUtils.sudo_set_target_registrations_per_interval()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_target_registrations_per_interval>)
      * [`AdminUtils.sudo_set_tempo()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_tempo>)
      * [`AdminUtils.sudo_set_toggle_transfer()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_toggle_transfer>)
      * [`AdminUtils.sudo_set_total_issuance()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_total_issuance>)
      * [`AdminUtils.sudo_set_tx_delegate_take_rate_limit()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_tx_delegate_take_rate_limit>)
      * [`AdminUtils.sudo_set_tx_rate_limit()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_tx_rate_limit>)
      * [`AdminUtils.sudo_set_weights_set_rate_limit()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_weights_set_rate_limit>)
      * [`AdminUtils.sudo_set_weights_version_key()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_weights_version_key>)
      * [`AdminUtils.sudo_set_yuma3_enabled()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_set_yuma3_enabled>)
      * [`AdminUtils.sudo_toggle_evm_precompile()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_toggle_evm_precompile>)
      * [`AdminUtils.sudo_trim_to_max_allowed_uids()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.sudo_trim_to_max_allowed_uids>)
      * [`AdminUtils.swap_authorities()`](<#bittensor.core.extrinsics.pallets.admin_utils.AdminUtils.swap_authorities>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.