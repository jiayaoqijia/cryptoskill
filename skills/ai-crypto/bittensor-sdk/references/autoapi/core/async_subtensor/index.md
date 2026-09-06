# bittensor.core.async_subtensor &#8212; Bittensor SDK Docs  documentation

[Skip to main content](<#main-content>)

__Back to top __ `Ctrl`+`K`

[ ![Bittensor SDK Docs  documentation - Home](../../../../_static/logo.svg) ![Bittensor SDK Docs  documentation - Home](../../../../_static/logo-dark-mode.svg) ](<../../../../index.html>)

__ Search `Ctrl`+`K`

Table of Contents

  * [API Reference](<../../../index.html>) __
    * [bittensor](<../../index.html>) __
      * [bittensor.core](<../index.html>) __
        * [bittensor.core.async_subtensor](<#>)
        * [bittensor.core.axon](<../axon/index.html>)
        * [bittensor.core.chain_data](<../chain_data/index.html>)
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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/async_subtensor/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/async_subtensor/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/core/async_subtensor/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.async_subtensor

##  Contents 

  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`AsyncSubtensor`](<#bittensor.core.async_subtensor.AsyncSubtensor>)
      * [`AsyncSubtensor.add_liquidity()`](<#bittensor.core.async_subtensor.AsyncSubtensor.add_liquidity>)
      * [`AsyncSubtensor.add_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.add_proxy>)
      * [`AsyncSubtensor.add_stake()`](<#bittensor.core.async_subtensor.AsyncSubtensor.add_stake>)
      * [`AsyncSubtensor.add_stake_burn()`](<#bittensor.core.async_subtensor.AsyncSubtensor.add_stake_burn>)
      * [`AsyncSubtensor.add_stake_multiple()`](<#bittensor.core.async_subtensor.AsyncSubtensor.add_stake_multiple>)
      * [`AsyncSubtensor.all_subnets()`](<#bittensor.core.async_subtensor.AsyncSubtensor.all_subnets>)
      * [`AsyncSubtensor.announce_coldkey_swap()`](<#bittensor.core.async_subtensor.AsyncSubtensor.announce_coldkey_swap>)
      * [`AsyncSubtensor.announce_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.announce_proxy>)
      * [`AsyncSubtensor.block`](<#bittensor.core.async_subtensor.AsyncSubtensor.block>)
      * [`AsyncSubtensor.blocks_since_last_step()`](<#bittensor.core.async_subtensor.AsyncSubtensor.blocks_since_last_step>)
      * [`AsyncSubtensor.blocks_since_last_update()`](<#bittensor.core.async_subtensor.AsyncSubtensor.blocks_since_last_update>)
      * [`AsyncSubtensor.blocks_until_next_epoch()`](<#bittensor.core.async_subtensor.AsyncSubtensor.blocks_until_next_epoch>)
      * [`AsyncSubtensor.bonds()`](<#bittensor.core.async_subtensor.AsyncSubtensor.bonds>)
      * [`AsyncSubtensor.burned_register()`](<#bittensor.core.async_subtensor.AsyncSubtensor.burned_register>)
      * [`AsyncSubtensor.claim_root()`](<#bittensor.core.async_subtensor.AsyncSubtensor.claim_root>)
      * [`AsyncSubtensor.clear_coldkey_swap_announcement()`](<#bittensor.core.async_subtensor.AsyncSubtensor.clear_coldkey_swap_announcement>)
      * [`AsyncSubtensor.close()`](<#bittensor.core.async_subtensor.AsyncSubtensor.close>)
      * [`AsyncSubtensor.commit_reveal_enabled()`](<#bittensor.core.async_subtensor.AsyncSubtensor.commit_reveal_enabled>)
      * [`AsyncSubtensor.commit_weights()`](<#bittensor.core.async_subtensor.AsyncSubtensor.commit_weights>)
      * [`AsyncSubtensor.compose_call()`](<#bittensor.core.async_subtensor.AsyncSubtensor.compose_call>)
      * [`AsyncSubtensor.contribute_crowdloan()`](<#bittensor.core.async_subtensor.AsyncSubtensor.contribute_crowdloan>)
      * [`AsyncSubtensor.create_crowdloan()`](<#bittensor.core.async_subtensor.AsyncSubtensor.create_crowdloan>)
      * [`AsyncSubtensor.create_pure_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.create_pure_proxy>)
      * [`AsyncSubtensor.determine_block_hash()`](<#bittensor.core.async_subtensor.AsyncSubtensor.determine_block_hash>)
      * [`AsyncSubtensor.difficulty()`](<#bittensor.core.async_subtensor.AsyncSubtensor.difficulty>)
      * [`AsyncSubtensor.dispute_coldkey_swap()`](<#bittensor.core.async_subtensor.AsyncSubtensor.dispute_coldkey_swap>)
      * [`AsyncSubtensor.dissolve_crowdloan()`](<#bittensor.core.async_subtensor.AsyncSubtensor.dissolve_crowdloan>)
      * [`AsyncSubtensor.does_hotkey_exist()`](<#bittensor.core.async_subtensor.AsyncSubtensor.does_hotkey_exist>)
      * [`AsyncSubtensor.filter_netuids_by_registered_hotkeys()`](<#bittensor.core.async_subtensor.AsyncSubtensor.filter_netuids_by_registered_hotkeys>)
      * [`AsyncSubtensor.finalize_crowdloan()`](<#bittensor.core.async_subtensor.AsyncSubtensor.finalize_crowdloan>)
      * [`AsyncSubtensor.get_admin_freeze_window()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_admin_freeze_window>)
      * [`AsyncSubtensor.get_all_commitments()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_commitments>)
      * [`AsyncSubtensor.get_all_ema_tao_inflow()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_ema_tao_inflow>)
      * [`AsyncSubtensor.get_all_metagraphs_info()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_metagraphs_info>)
      * [`AsyncSubtensor.get_all_neuron_certificates()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_neuron_certificates>)
      * [`AsyncSubtensor.get_all_revealed_commitments()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_revealed_commitments>)
      * [`AsyncSubtensor.get_all_subnets_info()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_subnets_info>)
      * [`AsyncSubtensor.get_all_subnets_netuid()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_subnets_netuid>)
      * [`AsyncSubtensor.get_auto_stakes()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_auto_stakes>)
      * [`AsyncSubtensor.get_balance()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_balance>)
      * [`AsyncSubtensor.get_balances()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_balances>)
      * [`AsyncSubtensor.get_block_hash()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_block_hash>)
      * [`AsyncSubtensor.get_block_info()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_block_info>)
      * [`AsyncSubtensor.get_children()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_children>)
      * [`AsyncSubtensor.get_children_pending()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_children_pending>)
      * [`AsyncSubtensor.get_coldkey_swap_announcement()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_announcement>)
      * [`AsyncSubtensor.get_coldkey_swap_announcement_delay()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_announcement_delay>)
      * [`AsyncSubtensor.get_coldkey_swap_announcements()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_announcements>)
      * [`AsyncSubtensor.get_coldkey_swap_constants()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_constants>)
      * [`AsyncSubtensor.get_coldkey_swap_dispute()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_dispute>)
      * [`AsyncSubtensor.get_coldkey_swap_disputes()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_disputes>)
      * [`AsyncSubtensor.get_coldkey_swap_reannouncement_delay()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_reannouncement_delay>)
      * [`AsyncSubtensor.get_commitment()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_commitment>)
      * [`AsyncSubtensor.get_commitment_metadata()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_commitment_metadata>)
      * [`AsyncSubtensor.get_crowdloan_by_id()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_crowdloan_by_id>)
      * [`AsyncSubtensor.get_crowdloan_constants()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_crowdloan_constants>)
      * [`AsyncSubtensor.get_crowdloan_contributions()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_crowdloan_contributions>)
      * [`AsyncSubtensor.get_crowdloan_next_id()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_crowdloan_next_id>)
      * [`AsyncSubtensor.get_crowdloans()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_crowdloans>)
      * [`AsyncSubtensor.get_current_block()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_current_block>)
      * [`AsyncSubtensor.get_delegate_by_hotkey()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_delegate_by_hotkey>)
      * [`AsyncSubtensor.get_delegate_identities()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_delegate_identities>)
      * [`AsyncSubtensor.get_delegate_take()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_delegate_take>)
      * [`AsyncSubtensor.get_delegated()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_delegated>)
      * [`AsyncSubtensor.get_delegates()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_delegates>)
      * [`AsyncSubtensor.get_ema_tao_inflow()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_ema_tao_inflow>)
      * [`AsyncSubtensor.get_existential_deposit()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_existential_deposit>)
      * [`AsyncSubtensor.get_extrinsic_fee()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_extrinsic_fee>)
      * [`AsyncSubtensor.get_hotkey_owner()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_hotkey_owner>)
      * [`AsyncSubtensor.get_hotkey_stake`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_hotkey_stake>)
      * [`AsyncSubtensor.get_hyperparameter()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_hyperparameter>)
      * [`AsyncSubtensor.get_last_bonds_reset()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_last_bonds_reset>)
      * [`AsyncSubtensor.get_last_commitment_bonds_reset_block()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_last_commitment_bonds_reset_block>)
      * [`AsyncSubtensor.get_liquidity_list()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_liquidity_list>)
      * [`AsyncSubtensor.get_mechanism_count()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_mechanism_count>)
      * [`AsyncSubtensor.get_mechanism_emission_split()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_mechanism_emission_split>)
      * [`AsyncSubtensor.get_metagraph_info()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_metagraph_info>)
      * [`AsyncSubtensor.get_mev_shield_current_key()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_mev_shield_current_key>)
      * [`AsyncSubtensor.get_mev_shield_next_key()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_mev_shield_next_key>)
      * [`AsyncSubtensor.get_minimum_required_stake()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_minimum_required_stake>)
      * [`AsyncSubtensor.get_netuids_for_hotkey()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_netuids_for_hotkey>)
      * [`AsyncSubtensor.get_neuron_certificate()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_neuron_certificate>)
      * [`AsyncSubtensor.get_neuron_for_pubkey_and_subnet()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_neuron_for_pubkey_and_subnet>)
      * [`AsyncSubtensor.get_next_epoch_start_block()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_next_epoch_start_block>)
      * [`AsyncSubtensor.get_owned_hotkeys()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_owned_hotkeys>)
      * [`AsyncSubtensor.get_parents()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_parents>)
      * [`AsyncSubtensor.get_proxies()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_proxies>)
      * [`AsyncSubtensor.get_proxies_for_real_account()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_proxies_for_real_account>)
      * [`AsyncSubtensor.get_proxy_announcement()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_proxy_announcement>)
      * [`AsyncSubtensor.get_proxy_announcements()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_proxy_announcements>)
      * [`AsyncSubtensor.get_proxy_constants()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_proxy_constants>)
      * [`AsyncSubtensor.get_revealed_commitment()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_revealed_commitment>)
      * [`AsyncSubtensor.get_revealed_commitment_by_hotkey()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_revealed_commitment_by_hotkey>)
      * [`AsyncSubtensor.get_root_alpha_dividends_per_subnet()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_root_alpha_dividends_per_subnet>)
      * [`AsyncSubtensor.get_root_claim_type()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_root_claim_type>)
      * [`AsyncSubtensor.get_root_claimable_all_rates()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_root_claimable_all_rates>)
      * [`AsyncSubtensor.get_root_claimable_rate()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_root_claimable_rate>)
      * [`AsyncSubtensor.get_root_claimable_stake()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_root_claimable_stake>)
      * [`AsyncSubtensor.get_root_claimed()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_root_claimed>)
      * [`AsyncSubtensor.get_stake()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake>)
      * [`AsyncSubtensor.get_stake_add_fee()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_add_fee>)
      * [`AsyncSubtensor.get_stake_for_coldkey_and_hotkey()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_for_coldkey_and_hotkey>)
      * [`AsyncSubtensor.get_stake_for_hotkey()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_for_hotkey>)
      * [`AsyncSubtensor.get_stake_info_for_coldkey()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_info_for_coldkey>)
      * [`AsyncSubtensor.get_stake_info_for_coldkeys()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_info_for_coldkeys>)
      * [`AsyncSubtensor.get_stake_movement_fee()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_movement_fee>)
      * [`AsyncSubtensor.get_stake_weight()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_weight>)
      * [`AsyncSubtensor.get_staking_hotkeys()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_staking_hotkeys>)
      * [`AsyncSubtensor.get_start_call_delay()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_start_call_delay>)
      * [`AsyncSubtensor.get_subnet_burn_cost()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_burn_cost>)
      * [`AsyncSubtensor.get_subnet_hyperparameters()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_hyperparameters>)
      * [`AsyncSubtensor.get_subnet_info()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_info>)
      * [`AsyncSubtensor.get_subnet_owner_hotkey()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_owner_hotkey>)
      * [`AsyncSubtensor.get_subnet_price()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_price>)
      * [`AsyncSubtensor.get_subnet_prices()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_prices>)
      * [`AsyncSubtensor.get_subnet_reveal_period_epochs()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_reveal_period_epochs>)
      * [`AsyncSubtensor.get_subnet_validator_permits()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_validator_permits>)
      * [`AsyncSubtensor.get_timelocked_weight_commits()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_timelocked_weight_commits>)
      * [`AsyncSubtensor.get_timestamp()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_timestamp>)
      * [`AsyncSubtensor.get_total_subnets()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_total_subnets>)
      * [`AsyncSubtensor.get_transfer_fee()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_transfer_fee>)
      * [`AsyncSubtensor.get_uid_for_hotkey_on_subnet()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_uid_for_hotkey_on_subnet>)
      * [`AsyncSubtensor.get_unstake_fee()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_unstake_fee>)
      * [`AsyncSubtensor.get_vote_data()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_vote_data>)
      * [`AsyncSubtensor.immunity_period()`](<#bittensor.core.async_subtensor.AsyncSubtensor.immunity_period>)
      * [`AsyncSubtensor.initialize()`](<#bittensor.core.async_subtensor.AsyncSubtensor.initialize>)
      * [`AsyncSubtensor.is_fast_blocks()`](<#bittensor.core.async_subtensor.AsyncSubtensor.is_fast_blocks>)
      * [`AsyncSubtensor.is_hotkey_delegate()`](<#bittensor.core.async_subtensor.AsyncSubtensor.is_hotkey_delegate>)
      * [`AsyncSubtensor.is_hotkey_registered()`](<#bittensor.core.async_subtensor.AsyncSubtensor.is_hotkey_registered>)
      * [`AsyncSubtensor.is_hotkey_registered_any()`](<#bittensor.core.async_subtensor.AsyncSubtensor.is_hotkey_registered_any>)
      * [`AsyncSubtensor.is_hotkey_registered_on_subnet()`](<#bittensor.core.async_subtensor.AsyncSubtensor.is_hotkey_registered_on_subnet>)
      * [`AsyncSubtensor.is_in_admin_freeze_window()`](<#bittensor.core.async_subtensor.AsyncSubtensor.is_in_admin_freeze_window>)
      * [`AsyncSubtensor.is_subnet_active()`](<#bittensor.core.async_subtensor.AsyncSubtensor.is_subnet_active>)
      * [`AsyncSubtensor.kill_pure_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.kill_pure_proxy>)
      * [`AsyncSubtensor.last_drand_round()`](<#bittensor.core.async_subtensor.AsyncSubtensor.last_drand_round>)
      * [`AsyncSubtensor.log_verbose`](<#bittensor.core.async_subtensor.AsyncSubtensor.log_verbose>)
      * [`AsyncSubtensor.max_weight_limit()`](<#bittensor.core.async_subtensor.AsyncSubtensor.max_weight_limit>)
      * [`AsyncSubtensor.metagraph()`](<#bittensor.core.async_subtensor.AsyncSubtensor.metagraph>)
      * [`AsyncSubtensor.mev_submit_encrypted()`](<#bittensor.core.async_subtensor.AsyncSubtensor.mev_submit_encrypted>)
      * [`AsyncSubtensor.min_allowed_weights()`](<#bittensor.core.async_subtensor.AsyncSubtensor.min_allowed_weights>)
      * [`AsyncSubtensor.modify_liquidity()`](<#bittensor.core.async_subtensor.AsyncSubtensor.modify_liquidity>)
      * [`AsyncSubtensor.move_stake()`](<#bittensor.core.async_subtensor.AsyncSubtensor.move_stake>)
      * [`AsyncSubtensor.neuron_for_uid()`](<#bittensor.core.async_subtensor.AsyncSubtensor.neuron_for_uid>)
      * [`AsyncSubtensor.neurons()`](<#bittensor.core.async_subtensor.AsyncSubtensor.neurons>)
      * [`AsyncSubtensor.neurons_lite()`](<#bittensor.core.async_subtensor.AsyncSubtensor.neurons_lite>)
      * [`AsyncSubtensor.poke_deposit()`](<#bittensor.core.async_subtensor.AsyncSubtensor.poke_deposit>)
      * [`AsyncSubtensor.proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.proxy>)
      * [`AsyncSubtensor.proxy_announced()`](<#bittensor.core.async_subtensor.AsyncSubtensor.proxy_announced>)
      * [`AsyncSubtensor.query_constant()`](<#bittensor.core.async_subtensor.AsyncSubtensor.query_constant>)
      * [`AsyncSubtensor.query_identity()`](<#bittensor.core.async_subtensor.AsyncSubtensor.query_identity>)
      * [`AsyncSubtensor.query_map()`](<#bittensor.core.async_subtensor.AsyncSubtensor.query_map>)
      * [`AsyncSubtensor.query_map_subtensor()`](<#bittensor.core.async_subtensor.AsyncSubtensor.query_map_subtensor>)
      * [`AsyncSubtensor.query_module()`](<#bittensor.core.async_subtensor.AsyncSubtensor.query_module>)
      * [`AsyncSubtensor.query_runtime_api()`](<#bittensor.core.async_subtensor.AsyncSubtensor.query_runtime_api>)
      * [`AsyncSubtensor.query_subtensor()`](<#bittensor.core.async_subtensor.AsyncSubtensor.query_subtensor>)
      * [`AsyncSubtensor.recycle()`](<#bittensor.core.async_subtensor.AsyncSubtensor.recycle>)
      * [`AsyncSubtensor.refund_crowdloan()`](<#bittensor.core.async_subtensor.AsyncSubtensor.refund_crowdloan>)
      * [`AsyncSubtensor.register()`](<#bittensor.core.async_subtensor.AsyncSubtensor.register>)
      * [`AsyncSubtensor.register_limit()`](<#bittensor.core.async_subtensor.AsyncSubtensor.register_limit>)
      * [`AsyncSubtensor.register_subnet()`](<#bittensor.core.async_subtensor.AsyncSubtensor.register_subnet>)
      * [`AsyncSubtensor.reject_proxy_announcement()`](<#bittensor.core.async_subtensor.AsyncSubtensor.reject_proxy_announcement>)
      * [`AsyncSubtensor.remove_liquidity()`](<#bittensor.core.async_subtensor.AsyncSubtensor.remove_liquidity>)
      * [`AsyncSubtensor.remove_proxies()`](<#bittensor.core.async_subtensor.AsyncSubtensor.remove_proxies>)
      * [`AsyncSubtensor.remove_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.remove_proxy>)
      * [`AsyncSubtensor.remove_proxy_announcement()`](<#bittensor.core.async_subtensor.AsyncSubtensor.remove_proxy_announcement>)
      * [`AsyncSubtensor.reveal_weights()`](<#bittensor.core.async_subtensor.AsyncSubtensor.reveal_weights>)
      * [`AsyncSubtensor.root_register()`](<#bittensor.core.async_subtensor.AsyncSubtensor.root_register>)
      * [`AsyncSubtensor.root_set_pending_childkey_cooldown()`](<#bittensor.core.async_subtensor.AsyncSubtensor.root_set_pending_childkey_cooldown>)
      * [`AsyncSubtensor.serve_axon()`](<#bittensor.core.async_subtensor.AsyncSubtensor.serve_axon>)
      * [`AsyncSubtensor.set_auto_stake()`](<#bittensor.core.async_subtensor.AsyncSubtensor.set_auto_stake>)
      * [`AsyncSubtensor.set_children()`](<#bittensor.core.async_subtensor.AsyncSubtensor.set_children>)
      * [`AsyncSubtensor.set_commitment()`](<#bittensor.core.async_subtensor.AsyncSubtensor.set_commitment>)
      * [`AsyncSubtensor.set_delegate_take()`](<#bittensor.core.async_subtensor.AsyncSubtensor.set_delegate_take>)
      * [`AsyncSubtensor.set_reveal_commitment()`](<#bittensor.core.async_subtensor.AsyncSubtensor.set_reveal_commitment>)
      * [`AsyncSubtensor.set_root_claim_type()`](<#bittensor.core.async_subtensor.AsyncSubtensor.set_root_claim_type>)
      * [`AsyncSubtensor.set_subnet_identity()`](<#bittensor.core.async_subtensor.AsyncSubtensor.set_subnet_identity>)
      * [`AsyncSubtensor.set_weights()`](<#bittensor.core.async_subtensor.AsyncSubtensor.set_weights>)
      * [`AsyncSubtensor.sign_and_send_extrinsic()`](<#bittensor.core.async_subtensor.AsyncSubtensor.sign_and_send_extrinsic>)
      * [`AsyncSubtensor.sim_swap()`](<#bittensor.core.async_subtensor.AsyncSubtensor.sim_swap>)
      * [`AsyncSubtensor.start_call()`](<#bittensor.core.async_subtensor.AsyncSubtensor.start_call>)
      * [`AsyncSubtensor.state_call()`](<#bittensor.core.async_subtensor.AsyncSubtensor.state_call>)
      * [`AsyncSubtensor.subnet()`](<#bittensor.core.async_subtensor.AsyncSubtensor.subnet>)
      * [`AsyncSubtensor.subnet_exists()`](<#bittensor.core.async_subtensor.AsyncSubtensor.subnet_exists>)
      * [`AsyncSubtensor.subnetwork_n()`](<#bittensor.core.async_subtensor.AsyncSubtensor.subnetwork_n>)
      * [`AsyncSubtensor.substrate`](<#bittensor.core.async_subtensor.AsyncSubtensor.substrate>)
      * [`AsyncSubtensor.swap_coldkey_announced()`](<#bittensor.core.async_subtensor.AsyncSubtensor.swap_coldkey_announced>)
      * [`AsyncSubtensor.swap_stake()`](<#bittensor.core.async_subtensor.AsyncSubtensor.swap_stake>)
      * [`AsyncSubtensor.tempo()`](<#bittensor.core.async_subtensor.AsyncSubtensor.tempo>)
      * [`AsyncSubtensor.toggle_user_liquidity()`](<#bittensor.core.async_subtensor.AsyncSubtensor.toggle_user_liquidity>)
      * [`AsyncSubtensor.transfer()`](<#bittensor.core.async_subtensor.AsyncSubtensor.transfer>)
      * [`AsyncSubtensor.transfer_stake()`](<#bittensor.core.async_subtensor.AsyncSubtensor.transfer_stake>)
      * [`AsyncSubtensor.tx_rate_limit()`](<#bittensor.core.async_subtensor.AsyncSubtensor.tx_rate_limit>)
      * [`AsyncSubtensor.unstake()`](<#bittensor.core.async_subtensor.AsyncSubtensor.unstake>)
      * [`AsyncSubtensor.unstake_all()`](<#bittensor.core.async_subtensor.AsyncSubtensor.unstake_all>)
      * [`AsyncSubtensor.unstake_multiple()`](<#bittensor.core.async_subtensor.AsyncSubtensor.unstake_multiple>)
      * [`AsyncSubtensor.update_cap_crowdloan()`](<#bittensor.core.async_subtensor.AsyncSubtensor.update_cap_crowdloan>)
      * [`AsyncSubtensor.update_end_crowdloan()`](<#bittensor.core.async_subtensor.AsyncSubtensor.update_end_crowdloan>)
      * [`AsyncSubtensor.update_min_contribution_crowdloan()`](<#bittensor.core.async_subtensor.AsyncSubtensor.update_min_contribution_crowdloan>)
      * [`AsyncSubtensor.validate_extrinsic_params()`](<#bittensor.core.async_subtensor.AsyncSubtensor.validate_extrinsic_params>)
      * [`AsyncSubtensor.wait_for_block()`](<#bittensor.core.async_subtensor.AsyncSubtensor.wait_for_block>)
      * [`AsyncSubtensor.weights()`](<#bittensor.core.async_subtensor.AsyncSubtensor.weights>)
      * [`AsyncSubtensor.weights_rate_limit()`](<#bittensor.core.async_subtensor.AsyncSubtensor.weights_rate_limit>)
      * [`AsyncSubtensor.withdraw_crowdloan()`](<#bittensor.core.async_subtensor.AsyncSubtensor.withdraw_crowdloan>)
    * [`get_async_subtensor()`](<#bittensor.core.async_subtensor.get_async_subtensor>)



# bittensor.core.async_subtensor[#](<#module-bittensor.core.async_subtensor> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`AsyncSubtensor`](<#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor") | Asynchronous interface for interacting with the Bittensor blockchain.  
---|---  
  
## Functions[#](<#functions> "Link to this heading")

[`get_async_subtensor`](<#bittensor.core.async_subtensor.get_async_subtensor> "bittensor.core.async_subtensor.get_async_subtensor")([network, config, mock, log_verbose]) | Factory method to create an initialized AsyncSubtensor instance.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.async_subtensor.AsyncSubtensor(_network =None_, _config =None_, _log_verbose =False_, _fallback_endpoints =None_, _retry_forever =False_, _archive_endpoints =None_, _websocket_shutdown_timer =5.0_, _mock =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor> "Link to this definition")
    

Bases: [`bittensor.core.types.SubtensorMixin`](<../types/index.html#bittensor.core.types.SubtensorMixin> "bittensor.core.types.SubtensorMixin")

Asynchronous interface for interacting with the Bittensor blockchain.

This class provides a thin layer over the Substrate Interface offering async functionality for Bittensor. This includes frequently-used calls for querying blockchain data, managing stakes and liquidity positions, registering neurons, submitting weights, and many other functions for participating in Bittensor.

Notes

Key Bittensor concepts used throughout this class:

  * **Coldkey** : The key pair corresponding to a user’s overall wallet. Used to transfer, stake, manage subnets.

  * **Hotkey** : A key pair (each wallet may have zero, one, or more) used for neuron operations (mining and validation).

  * **Netuid** : Unique identifier for a subnet (0 is the Root Subnet)

  * **UID** : Unique identifier for a neuron registered to a hotkey on a specific subnet.

  * **Metagraph** : Data structure containing the complete state of a subnet at a block.

  * **TAO** : The base network token; subnet 0 stake is in TAO

  * **Alpha** : Subnet-specific token representing some quantity of TAO staked into a subnet.

  * **Rao** : Smallest unit of TAO (1 TAO = 1e9 Rao)

  * Bittensor Glossary <<https://docs.learnbittensor.org/glossary>>

  * Wallets, Coldkeys and Hotkeys in Bittensor <<https://docs.learnbittensor.org/keys/wallets>>




Initializes an AsyncSubtensor instance for blockchain interaction.

Parameters:
    

  * **network** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The network name to connect to (e.g., finney for Bittensor mainnet, test, for Bittensor test network, local for a locally deployed blockchain). If None, uses the default network from config.

  * **config** (_Optional_ _[_[_bittensor.core.config.Config_](<../config/index.html#bittensor.core.config.Config> "bittensor.core.config.Config") _]_) – Configuration object for the AsyncSubtensor instance. If None, uses the default configuration.

  * **log_verbose** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Enables or disables verbose logging.

  * **fallback_endpoints** (_Optional_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]__]_) – List of fallback WebSocket endpoints to use if the primary network endpoint is unavailable. These are tried in order when the default endpoint fails.

  * **retry_forever** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to retry connection attempts indefinitely on connection errors.

  * **mock** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether this is a mock instance. FOR TESTING ONLY.

  * **archive_endpoints** (_Optional_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]__]_) – List of archive node endpoints for queries requiring historical block data beyond the retention period of lite nodes. These are only used when requesting blocks that the current node is unable to serve.

  * **websocket_shutdown_timer** (_Optional_ _[_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _]_) – Amount of time (in seconds) to wait after the last response from the chain before automatically closing the WebSocket connection. Pass None to disable automatic shutdown entirely.



Returns:
    

None

async add_liquidity(_wallet_ , _netuid_ , _liquidity_ , _price_low_ , _price_high_ , _hotkey_ss58 =None_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.add_liquidity> "Link to this definition")
    

Adds liquidity to the specified price range.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet used to sign the extrinsic (must be unlocked).

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The UID of the target subnet for which the call is being initiated.

  * **liquidity** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – The amount of liquidity to be added.

  * **price_low** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – The lower bound of the price tick range. In TAO.

  * **price_high** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – The upper bound of the price tick range. In TAO.

  * **hotkey_ss58** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hotkey with staked TAO in Alpha. If not passed then the wallet hotkey is used.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Note

Adding is allowed even when user liquidity is enabled in specified subnet. Call toggle_user_liquidity method to enable/disable user liquidity.

async add_proxy(_wallet_ , _delegate_ss58_ , _proxy_type_ , _delay_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.add_proxy> "Link to this definition")
    

Adds a proxy relationship.

This method creates a proxy relationship where the delegate can execute calls on behalf of the real account (the wallet owner) with restrictions defined by the proxy type and a delay period. A deposit is required and held as long as the proxy relationship exists.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object.

  * **delegate_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the delegate proxy account.

  * **proxy_type** (_Union_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,__bittensor.core.chain_data.ProxyType_ _]_) – The type of proxy permissions (e.g., “Any”, “NonTransfer”, “Governance”, “Staking”). Can be a string or ProxyType enum value. For available proxy types and their permissions, see the documentation link in the Notes section below.

  * **delay** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Optionally, include a delay in blocks. The number of blocks that must elapse between announcing and executing a proxied transaction. A delay of 0 means the proxy can be used immediately without announcements. A non-zero delay creates a time-lock, requiring the proxy to announce calls via [`announce_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.announce_proxy> "bittensor.core.async_subtensor.AsyncSubtensor.announce_proxy") before execution, giving the real account time to review and reject unwanted operations via [`reject_proxy_announcement()`](<#bittensor.core.async_subtensor.AsyncSubtensor.reject_proxy_announcement> "bittensor.core.async_subtensor.AsyncSubtensor.reject_proxy_announcement").

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * A deposit is required when adding a proxy. The deposit amount is determined by runtime constants and is returned when the proxy is removed. Use [`get_proxy_constants()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_proxy_constants> "bittensor.core.async_subtensor.AsyncSubtensor.get_proxy_constants") to check current deposit requirements.

  * For available proxy types and their specific permissions, see: <<https://docs.learnbittensor.org/keys/proxies#types-of-proxies>>

  * Bittensor proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>




Warning

The Any proxy type is dangerous as it grants full permissions to the proxy, including the ability to make transfers and manage the account completely. Use with extreme caution.

async add_stake(_wallet_ , _netuid_ , _hotkey_ss58_ , _amount_ , _safe_staking =False_, _allow_partial_stake =False_, _rate_tolerance =0.005_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.add_stake> "Link to this definition")
    

Adds a stake from the specified wallet to the neuron identified by the SS58 address of its hotkey in specified subnet. Staking is a fundamental process in the Bittensor network that enables neurons to participate actively and earn incentives.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet to be used for staking.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet to which the neuron belongs.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The ss58 address of the hotkey account to stake to default to the wallet’s hotkey.

  * **amount** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – The amount of TAO to stake.

  * **safe_staking** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, enables price safety checks to protect against fluctuating prices. The stake will only execute if the price change doesn’t exceed the rate tolerance.

  * **allow_partial_stake** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True and safe_staking is enabled, allows partial staking when the full amount would exceed the price tolerance. If false, the entire stake fails if it would exceed the tolerance.

  * **rate_tolerance** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")) – The maximum allowed price change ratio when staking. For example, 0.005 = 0.5% maximum price increase. Only used when safe_staking is True.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the staking transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

This function enables neurons to increase their stake in the network, enhancing their influence and potential. When safe_staking is enabled, it provides protection against price fluctuations during the time stake is executed and the time it is actually processed by the chain.

Notes

  * Price Protection: <<https://docs.learnbittensor.org/learn/price-protection>>

  * Rate Limits: <<https://docs.learnbittensor.org/learn/chain-rate-limits#staking-operations-rate-limits>>




async add_stake_burn(_wallet_ , _netuid_ , _hotkey_ss58_ , _amount_ , _limit_price =None_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.add_stake_burn> "Link to this definition")
    

Executes a subnet buyback by staking TAO and immediately burning the resulting Alpha.

Only the subnet owner can call this method, and it is rate-limited to one call per subnet tempo.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet used to sign the extrinsic (must be the subnet owner).

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the hotkey account to stake to.

  * **amount** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – The amount of TAO to use for the buyback.

  * **limit_price** (_Optional_ _[_[_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") _]_) – Optional limit price expressed in units of RAO per one Alpha.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

async add_stake_multiple(_wallet_ , _netuids_ , _hotkey_ss58s_ , _amounts_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.add_stake_multiple> "Link to this definition")
    

Adds stakes to multiple neurons identified by their hotkey SS58 addresses. This bulk operation allows for efficient staking across different neurons from a single wallet.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet used for staking.

  * **netuids** ([_bittensor.core.types.UIDs_](<../types/index.html#bittensor.core.types.UIDs> "bittensor.core.types.UIDs")) – List of subnet UIDs.

  * **hotkey_ss58s** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – List of SS58 addresses of hotkeys to stake to.

  * **amounts** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") _]_) – List of corresponding TAO amounts to bet for each netuid and hotkey.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be finalized on the blockchain.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Price Protection: <<https://docs.learnbittensor.org/learn/price-protection>>

  * Rate Limits: <<https://docs.learnbittensor.org/learn/chain-rate-limits#staking-operations-rate-limits>>




async all_subnets(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.all_subnets> "Link to this definition")
    

Queries the blockchain for comprehensive information about all subnets, including their dynamic parameters and operational status.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

A list of DynamicInfo objects, each containing detailed information about a subnet, or None if the query fails.

Return type:
    

Optional[[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[DynamicInfo](<../chain_data/dynamic_info/index.html#bittensor.core.chain_data.dynamic_info.DynamicInfo> "bittensor.core.chain_data.dynamic_info.DynamicInfo")]]

async announce_coldkey_swap(_wallet_ , _new_coldkey_ss58_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.announce_coldkey_swap> "Link to this definition")
    

Announces a coldkey swap by submitting the BlakeTwo256 hash of the new coldkey.

This method allows a coldkey to declare its intention to swap to a new coldkey address. The announcement must be made before the actual swap can be executed, and a delay period must pass before execution is allowed. After making an announcement, all transactions from the coldkey are blocked except for swap_coldkey_announced.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (should be the current coldkey wallet).

  * **new_coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the new coldkey that will replace the current one.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If `True`, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If `False`, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning `False` if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * A swap cost is charged when making the first announcement (not when reannouncing).

  * After making an announcement, all transactions from the coldkey are blocked except for
    

swap_coldkey_announced.

  * The swap can only be executed after the delay period has passed (check via
    

get_coldkey_swap_announcement).

  * See: <<https://docs.learnbittensor.org/keys/coldkey-swap>>




async announce_proxy(_wallet_ , _real_account_ss58_ , _call_hash_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.announce_proxy> "Link to this definition")
    

Announces a future call that will be executed through a proxy.

This method allows a proxy account to declare its intention to execute a specific call on behalf of a real account after a delay period. The real account can review and either approve (via [`proxy_announced()`](<#bittensor.core.async_subtensor.AsyncSubtensor.proxy_announced> "bittensor.core.async_subtensor.AsyncSubtensor.proxy_announced")) or reject (via [`reject_proxy_announcement()`](<#bittensor.core.async_subtensor.AsyncSubtensor.reject_proxy_announcement> "bittensor.core.async_subtensor.AsyncSubtensor.reject_proxy_announcement")) the announcement.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (should be the proxy account wallet).

  * **real_account_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the real account on whose behalf the call will be made.

  * **call_hash** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hash of the call that will be executed in the future.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * A deposit is required when making an announcement. The deposit is returned when the announcement is executed, rejected, or removed. The announcement can be executed after the delay period has passed.

  * Bittensor proxies: <<https://docs.learnbittensor.org/keys/proxies>>




property block[#](<#bittensor.core.async_subtensor.AsyncSubtensor.block> "Link to this definition")
    

Provides an asynchronous getter to retrieve the current block number.

Returns:
    

The current blockchain block number.

async blocks_since_last_step(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.blocks_since_last_step> "Link to this definition")
    

Queries the blockchain to determine how many blocks have passed since the last epoch step for a specific subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnetwork.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

The number of blocks since the last step in the subnet, or None if the query fails.

Return type:
    

Optional[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

Notes

  * <<https://docs.learnbittensor.org/glossary#epoch>>




async blocks_since_last_update(_netuid_ , _uid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.blocks_since_last_update> "Link to this definition")
    

Returns the number of blocks since the last update, or None if the subnetwork or UID does not exist.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnetwork.

  * **uid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the neuron.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number for this query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block for the query. Do not specify if using reuse_block or block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

The number of blocks since the last update, or None if the subnetwork or UID does not exist.

Return type:
    

Optional[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

async blocks_until_next_epoch(_netuid_ , _tempo =None_, _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.blocks_until_next_epoch> "Link to this definition")
    

Returns the number of blocks until the next epoch of subnet with provided netuid.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnetwork.

  * **tempo** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The tempo of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

The number of blocks until the next epoch of the subnet with provided netuid.

Return type:
    

Optional[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

async bonds(_netuid_ , _mechid =0_, _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.bonds> "Link to this definition")
    

Retrieves the bond distribution set by subnet validators within a specific subnet.

Bonds represent a validator’s accumulated assessment of each miner’s performance over time, which serves as the starting point of Yuma Consensus.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Subnet identifier.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Subnet mechanism identifier (default 0 for primary mechanism).

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number for this query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block for the query. Do not specify if using reuse_block or block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

  * validator_uid: The UID of the validator
    
    * bonds: List of (miner_uid, bond_value) pairs




Bond values are u16-normalized (0-65535, where 65535 = 1.0 or 100%).

Return type:
    

List of tuples, where each tuple contains

Example

# Get bonds for subnet 1 bonds = await subtensor.bonds(netuid=1) print(bonds[0]) # example output: (5, [(0, 32767), (1, 16383), (3, 8191)]) # This means validator UID 5 has bonds: 50% to miner 0, 25% to miner 1, 12.5% to miner 3

Notes

  * See: <<https://docs.learnbittensor.org/glossary#validator-miner-bonds>>

  * See: <<https://docs.learnbittensor.org/glossary#yuma-consensus>>




async burned_register(_wallet_ , _netuid_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.burned_register> "Link to this definition")
    

Registers a neuron on the Bittensor network by recycling TAO. This method of registration involves recycling TAO tokens, allowing them to be re-mined by performing work on the network.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet associated with the neuron to be registered.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be finalized on the blockchain.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Rate Limits: <<https://docs.learnbittensor.org/learn/chain-rate-limits#registration-rate-limits>>




async claim_root(_wallet_ , _netuids_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.claim_root> "Link to this definition")
    

Submit an extrinsic to manually claim accumulated root dividends from one or more subnets.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance.

  * **netuids** ([_bittensor.core.types.UIDs_](<../types/index.html#bittensor.core.types.UIDs> "bittensor.core.types.UIDs")) – Iterable of subnet IDs to claim from in this call (the chain enforces a maximum number per transaction).

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Number of blocks during which the transaction remains valid after submission. If the extrinsic is not included in a block within this window, it will expire and be rejected.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to raise a Python exception instead of returning a failed ExtrinsicResponse.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait until the extrinsic is included in a block before returning.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic in a block before returning.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

ExtrinsicResponse describing the result of the extrinsic execution.

Notes

  * Only Alpha dividends are claimed; the underlying TAO stake on the Root Subnet remains unchanged.

  * The current root claim type (Swap or Keep) determines whether claimed Alpha is converted to TAO and restaked on root or left as Alpha on the originating subnets.

  * See: <<https://docs.learnbittensor.org/staking-and-delegation/root-claims>>

  * See also: <<https://docs.learnbittensor.org/staking-and-delegation/root-claims/managing-root-claims>>

  * Transaction fees: <<https://docs.learnbittensor.org/learn/fees>>




async clear_coldkey_swap_announcement(_wallet_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.clear_coldkey_swap_announcement> "Link to this definition")
    

Clears (withdraws) a pending coldkey swap announcement.

Callable by the coldkey that has an active, undisputed swap announcement. The reannouncement delay must have elapsed past the execution block before the announcement can be cleared.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (should be the current coldkey with an active announcement).

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If `True`, encrypts and submits the transaction through the MEV Shield pallet.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning `False` if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * The coldkey must have an active, undisputed swap announcement.

  * The reannouncement delay must have elapsed past the execution block.




async close()[#](<#bittensor.core.async_subtensor.AsyncSubtensor.close> "Link to this definition")
    

Closes the connection to the blockchain.

Use this to explicitly clean up resources and close the network connection instead of waiting for garbage collection.

Returns:
    

None

Example

sub = bt.AsyncSubtensor(network=”finney”)

# Initialize the connection

await subtensor.initialize()

# calls to subtensor

await subtensor.close()

async commit_reveal_enabled(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.commit_reveal_enabled> "Link to this definition")
    

Check if commit-reveal mechanism is enabled for a given subnet at a specific block.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet for which to check the commit-reveal mechanism.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

True if commit-reveal mechanism is enabled, False otherwise.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

Notes

  * <<https://docs.learnbittensor.org/glossary#commit-reveal>>

  * <<https://docs.learnbittensor.org/subnets/subnet-hyperparameters>>




async commit_weights(_wallet_ , _netuid_ , _salt_ , _uids_ , _weights_ , _mechid =0_, _version_key =version_as_int_, _max_attempts =5_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =16_, _raise_error =True_, _wait_for_inclusion =False_, _wait_for_finalization =False_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.commit_weights> "Link to this definition")
    

Commits a hash of the subnet validator’s weight vector to the Bittensor blockchain using the provided wallet. This action serves as a commitment or snapshot of the validator’s current weight distribution.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet associated with the neuron committing the weights.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **salt** ([_bittensor.core.types.Salt_](<../types/index.html#bittensor.core.types.Salt> "bittensor.core.types.Salt")) – list of randomly generated integers as salt to generated weighted hash.

  * **uids** ([_bittensor.core.types.UIDs_](<../types/index.html#bittensor.core.types.UIDs> "bittensor.core.types.UIDs")) – NumPy array of neuron UIDs for which weights are being committed.

  * **weights** ([_bittensor.core.types.Weights_](<../types/index.html#bittensor.core.types.Weights> "bittensor.core.types.Weights")) – NumPy array of weight values corresponding to each UID.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet mechanism unique identifier.

  * **version_key** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Version key for compatibility with the network.

  * **max_attempts** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The number of maximum attempts to commit weights.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

This function allows subnet validators to create a tamper-proof record of their weight vector at a specific point in time, creating a foundation of transparency and accountability for the Bittensor network.

Notes

  * <<https://docs.learnbittensor.org/glossary#commit-reveal>>

  * Rate Limits: <<https://docs.learnbittensor.org/learn/chain-rate-limits#weights-setting-rate-limit>>




async compose_call(_call_module_ , _call_function_ , _call_params_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.compose_call> "Link to this definition")
    

Dynamically compose a GenericCall using on-chain Substrate metadata after validating the provided parameters.

Parameters:
    

  * **call_module** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – Pallet name (e.g. “SubtensorModule”, “AdminUtils”).

  * **call_function** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – Function name (e.g. “set_weights”, “sudo_set_tempo”).

  * **call_params** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_Any_](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any") _]_) – Dictionary of parameters for the call.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The blockchain block_hash representation of the block id.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain block hash.



Returns:
    

Composed call object ready for extrinsic submission.

Return type:
    

GenericCall

Notes

For detailed documentation and examples of composing calls, including the CallBuilder utility, see: <<https://docs.learnbittensor.org/sdk/call>>

async contribute_crowdloan(_wallet_ , _crowdloan_id_ , _amount_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.contribute_crowdloan> "Link to this definition")
    

Contributes TAO to an active crowdloan campaign.

Contributions must occur before the crowdloan’s end block and are subject to minimum contribution requirements. If a contribution would push the total raised above the cap, it is automatically clipped to fit the remaining amount. Once the cap is reached, further contributions are rejected.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet instance used to sign the transaction (coldkey pays, coldkey receives emissions).

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to contribute to.

  * **amount** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – Amount to contribute (TAO). Must meet or exceed the campaign’s min_contribution.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, raises an exception rather than returning failure in the response.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

ExtrinsicResponse indicating success or failure, with error details if applicable.

Return type:
    

[bittensor.core.types.ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Contributions can be withdrawn before finalization via withdraw_crowdloan.

  * If the campaign does not reach its cap by the end block, contributors can be refunded via refund_crowdloan.

  * Contributions are counted toward MaxContributors limit per crowdloan.

  * Crowdloans Overview: <<https://docs.learnbittensor.org/subnets/crowdloans>>

  * Crowdloan Tutorial: <<https://docs.learnbittensor.org/subnets/crowdloans/crowdloans-tutorial#step-4-contribute-to-the-crowdloan>>




async create_crowdloan(_wallet_ , _deposit_ , _min_contribution_ , _cap_ , _end_ , _call =None_, _target_address =None_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.create_crowdloan> "Link to this definition")
    

Creates a new crowdloan campaign on-chain.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance used to sign the transaction.

  * **deposit** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – Initial deposit in RAO from the creator.

  * **min_contribution** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – Minimum contribution amount.

  * **cap** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – Maximum cap to be raised.

  * **end** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Block number when the campaign ends.

  * **call** (_Optional_ _[__scalecodec.GenericCall_ _]_) – Runtime call data (e.g., subtensor::register_leased_network).

  * **target_address** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – SS58 address to transfer funds to on success.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

ExtrinsicResponse indicating success or failure. On success, the crowdloan ID can be extracted from the Crowdloan.Created event in the response.

Return type:
    

[bittensor.core.types.ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Creator cannot update call or target_address after creation.

  * Creator can update cap, end, and min_contribution before finalization via update_* methods.

  * Use get_crowdloan_next_id to determine the ID that will be assigned to the new crowdloan.

  * Crowdloans Overview: <<https://docs.learnbittensor.org/subnets/crowdloans>>

  * Crowdloan Tutorial: <<https://docs.learnbittensor.org/subnets/crowdloans/crowdloans-tutorial#step-3-create-a-crowdloan>>




async create_pure_proxy(_wallet_ , _proxy_type_ , _delay_ , _index_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.create_pure_proxy> "Link to this definition")
    

Creates a pure proxy account.

A pure proxy is a keyless account that can only be controlled through proxy relationships. Unlike regular proxies, pure proxies do not have their own private keys, making them more secure for certain use cases. The pure proxy address is deterministically generated based on the spawner account, proxy type, delay, and index.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object.

  * **proxy_type** (_Union_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,__bittensor.core.chain_data.ProxyType_ _]_) – The type of proxy permissions for the pure proxy. Can be a string or ProxyType enum value. For available proxy types and their permissions, see the documentation link in the Notes section below.

  * **delay** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Optionally, include a delay in blocks. The number of blocks that must elapse between announcing and executing a proxied transaction. A delay of 0 means the pure proxy can be used immediately without any announcement period. A non-zero delay creates a time-lock, requiring announcements before execution to give the spawner time to review/reject.

  * **index** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – A salt value (u16, range 0-65535) used to generate unique pure proxy addresses. This should generally be left as 0 unless you are creating batches of proxies. When creating multiple pure proxies with identical parameters (same proxy_type and delay), different index values will produce different SS58 addresses. This is not a sequential counter—you can use any unique values (e.g., 0, 100, 7, 42) in any order. The index must be preserved as it’s required for [`kill_pure_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.kill_pure_proxy> "bittensor.core.async_subtensor.AsyncSubtensor.kill_pure_proxy"). If creating multiple pure proxies in a single batch transaction, each must have a unique index value.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * The pure proxy account address can be extracted from the “PureCreated” event in the response. Store the spawner address, proxy_type, index, height, and ext_index as they are required to kill the pure proxy later via [`kill_pure_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.kill_pure_proxy> "bittensor.core.async_subtensor.AsyncSubtensor.kill_pure_proxy").

  * For available proxy types and their specific permissions, see: <<https://docs.learnbittensor.org/keys/proxies#types-of-proxies>>

  * Bittensor proxies: <<https://docs.learnbittensor.org/keys/proxies/pure-proxies>>




Warning

The Any proxy type is dangerous as it grants full permissions to the proxy, including the ability to make transfers and kill the proxy. Use with extreme caution.

async determine_block_hash(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.determine_block_hash> "Link to this definition")
    

Determine the block hash for the block specified with the provided parameters.

Ensures that only one of the block specification parameters is used and returns the appropriate block hash for blockchain queries.

Parameter precedence (in order):
    

  1. If reuse_block=True and block or block_hash is set → raises ValueError

  2. If both block and block_hash are set → validates they match, raises ValueError if not

  3. If only block_hash is set → returns it directly

  4. If only block is set → fetches and returns its hash

  5. If none are set → returns None




Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to get the hash for. If specifying along with block_hash, the hash of block will be checked and compared with the supplied block hash, raising a ValueError if the two do not match.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the blockchain block (hex string prefixed with 0x). If specifying along with block, the hash of block will be checked and compared with the supplied block hash, raising a ValueError if the two do not match.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block or block_hash.



Returns:
    

The block hash (hex string with 0x prefix) if one can be determined, None otherwise.

Return type:
    

Optional[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]

Notes

  * <<https://docs.learnbittensor.org/glossary#block>>




async difficulty(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.difficulty> "Link to this definition")
    

Retrieves the ‘Difficulty’ hyperparameter for a specified subnet in the Bittensor network.

This parameter determines the computational challenge required for neurons to participate in consensus and
    

validation processes, using proof of work (POW) registration.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

The value of the ‘Difficulty’ hyperparameter if the subnet exists, None otherwise.

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

Notes

Burn registration is much more common on Bittensor subnets currently, compared to POW registration.

  * <<https://docs.learnbittensor.org/subnets/subnet-hyperparameters>>

  * <<https://docs.learnbittensor.org/validators#validator-registration>>

  * <<https://docs.learnbittensor.org/miners#miner-registration>>




async dispute_coldkey_swap(_wallet_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.dispute_coldkey_swap> "Link to this definition")
    

Disputes the coldkey swap announcement for the current coldkey.

Callable by the coldkey that has an active swap announcement. Marks the swap as disputed. The account is blocked until root calls reset_coldkey_swap.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (should be the current coldkey with an active announcement).

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If `True`, encrypts and submits the transaction through the MEV Shield pallet.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning `False` if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * The coldkey must have an active swap announcement.

  * After disputing, only root can clear the state via reset_coldkey_swap.




async dissolve_crowdloan(_wallet_ , _crowdloan_id_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.dissolve_crowdloan> "Link to this definition")
    

Dissolves a failed or refunded crowdloan, cleaning up storage and returning the creator’s deposit.

This permanently removes the crowdloan from on-chain storage and returns the creator’s deposit. Can only be called by the creator after all non-creator contributors have been refunded via refund_crowdloan. This is the final step in the lifecycle of a failed crowdloan (one that did not reach its cap by the end block).

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet instance used to sign the transaction (must be the creator’s coldkey).

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to dissolve.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after submission.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, raises an exception rather than returning failure in the response.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

ExtrinsicResponse indicating success or failure, with error details if applicable.

Return type:
    

[bittensor.core.types.ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Only the creator can dissolve their own crowdloan.

  * All non-creator contributors must be refunded first via refund_crowdloan.

  * The creator’s deposit (and any remaining contribution above deposit) is returned.

  * After dissolution, the crowdloan is permanently removed from chain storage.

  * Crowdloans Overview: <<https://docs.learnbittensor.org/subnets/crowdloans>>

  * Refund and Dissolve: <<https://docs.learnbittensor.org/subnets/crowdloans/crowdloans-tutorial#alternative-path-refund-and-dissolve>>




async does_hotkey_exist(_hotkey_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.does_hotkey_exist> "Link to this definition")
    

Returns true if the hotkey has been associated with a coldkey through account creation.

This method queries the Subtensor’s Owner storage map to check if the hotkey has been paired with a coldkey, as it must be before it (the hotkey) can be used for neuron registration.

The Owner storage map defaults to the zero address (5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM) for unused hotkeys. This method returns True if the Owner value is anything other than this default.

Parameters:
    

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the hotkey.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

True if the hotkey has been associated with a coldkey, False otherwise.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

Notes

  * <<https://docs.learnbittensor.org/glossary#hotkey>>




async filter_netuids_by_registered_hotkeys(_all_netuids_ , _filter_for_netuids_ , _all_hotkeys_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.filter_netuids_by_registered_hotkeys> "Link to this definition")
    

Filters netuids by combining netuids from all_netuids and netuids with registered hotkeys.

If filter_for_netuids is empty/None:
    

Returns all netuids where hotkeys from all_hotkeys are registered.

If filter_for_netuids is provided:
    

Returns the union of: \- Netuids from all_netuids that are in filter_for_netuids, AND \- Netuids with registered hotkeys that are in filter_for_netuids

This allows you to get netuids that are either in your specified list (all_netuids) or have registered hotkeys, as long as they match filter_for_netuids.

Parameters:
    

  * **all_netuids** (_Iterable_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – A list of netuids to consider for filtering.

  * **filter_for_netuids** (_Iterable_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – A subset of netuids to restrict the result to. If None/empty, returns all netuids with registered hotkeys.

  * **all_hotkeys** (_Iterable_ _[__bittensor_wallet.Wallet_ _]_) – Hotkeys to check for registration.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – hash of the blockchain block number at which to perform the query.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – whether to reuse the last-used blockchain hash when retrieving info.



Returns:
    

The filtered list of netuids (union of filtered all_netuids and registered hotkeys).

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

async finalize_crowdloan(_wallet_ , _crowdloan_id_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.finalize_crowdloan> "Link to this definition")
    

Finalizes a successful crowdloan after the cap is fully raised and the end block has passed.

Finalization executes the stored call (e.g., register_leased_network) or transfers raised funds to the target address. For subnet lease crowdloans, this registers the subnet, creates a SubnetLeaseBeneficiary proxy for the creator, and records contributor shares for pro-rata emissions distribution. Leftover funds (after registration and proxy costs) are refunded to contributors.

Only the creator can finalize, and finalization can only occur after both the end block is reached and the total raised equals the cap.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet instance used to sign the transaction (must be the creator’s coldkey).

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to finalize.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after submission.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, raises an exception rather than returning failure in the response.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

ExtrinsicResponse indicating success or failure. On success, a subnet lease is created (if applicable) and contributor shares are recorded for emissions.

Return type:
    

[bittensor.core.types.ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Only the creator can finalize.

  * Finalization requires raised == cap and current_block >= end.

  * For subnet leases, emissions are swapped to TAO and distributed to contributors’ coldkeys during the lease.

  * Leftover cap (after subnet lock + proxy deposit) is refunded to contributors pro-rata.

  * Crowdloans Overview: <<https://docs.learnbittensor.org/subnets/crowdloans>>

  * Crowdloan Tutorial: <<https://docs.learnbittensor.org/subnets/crowdloans/crowdloans-tutorial#step-5-finalize-the-crowdloan>>

  * Emissions Distribution: <<https://docs.learnbittensor.org/subnets/crowdloans#emissions-distribution-during-a-lease>>




async get_admin_freeze_window(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_admin_freeze_window> "Link to this definition")
    

Returns the duration, in blocks, of the administrative freeze window at the end of each epoch.

The admin freeze window is a period at the end of each epoch during which subnet owner operations are prohibited. This prevents subnet owners from modifying hyperparameters or performing certain administrative actions right before validators submit weights at the epoch boundary.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

10 blocks, ~2 minutes).

Return type:
    

The number of blocks in the administrative freeze window (default

Notes

  * <<https://docs.learnbittensor.org/learn/chain-rate-limits#administrative-freeze-window>>




async get_all_commitments(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_commitments> "Link to this definition")
    

Retrieves raw commitment metadata from a given subnet.

This method retrieves all commitment data for all neurons in a specific subnet. This is useful for analyzing the commit-reveal patterns across an entire subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnetwork.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

commitment with the commitment as a string.

Return type:
    

A mapping of the ss58

Example

# TODO add example of how to handle realistic commitment data

async get_all_ema_tao_inflow(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_ema_tao_inflow> "Link to this definition")
    

Retrieves the EMA (exponential moving average) of net TAO flows for all subnets.

The EMA tracks net TAO flows (staking minus unstaking) with a 30-day half-life (~86.8 day window), smoothing out short-term fluctuations while capturing sustained staking trends. This metric determines the subnet’s share of TAO emissions under the current, flow-based model. Positive values indicate net inflow (more staking than unstaking), negative values indicate net outflow. Subnets with negative EMA flows receive zero emissions.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

Dict mapping netuid to (last_updated_block, ema_flow). The Balance represents the EMA of net TAO flow in TAO units. Positive values indicate sustained net inflow, negative values indicate sustained net outflow.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")]]

The EMA uses a smoothing factor α ≈ 0.000003209, creating a 30-day half-life and ~86.8 day window. Only direct stake/unstake operations count toward flows; neuron registrations and root claims are excluded. Subnet 0 (root network) does not have an EMA TAO flow value.

Notes

  * Flow-based emissions: <<https://docs.learnbittensor.org/learn/emissions#tao-reserve-injection>>

  * EMA smoothing: <<https://docs.learnbittensor.org/learn/ema>>




async get_all_metagraphs_info(_all_mechanisms =False_, _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_metagraphs_info> "Link to this definition")
    

Retrieves a list of MetagraphInfo objects for all subnets

Parameters:
    

  * **all_mechanisms** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True then returns all mechanisms, otherwise only those with index 0 for all subnets.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the blockchain block number at which to perform the query.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash when retrieving info.



Returns:
    

List of MetagraphInfo objects for all existing subnets.

Return type:
    

Optional[[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[bittensor.core.chain_data.MetagraphInfo]]

Notes

  * <<https://docs.learnbittensor.org/glossary#metagraph>>




async get_all_neuron_certificates(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_neuron_certificates> "Link to this definition")
    

Retrieves the TLS certificates for neurons within a specified subnet (netuid) of the Bittensor network.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the parameter from. Do not specify if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to use the last-used block. Do not set if using block_hash or block.



Returns:
    

Dictionary mapping neuron hotkey SS58 addresses to their Certificate objects. Only includes neurons that have registered certificates.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [bittensor.utils.Certificate](<../../utils/index.html#bittensor.utils.Certificate> "bittensor.utils.Certificate")]

Notes

This method is used for certificate discovery to establish mutual TLS communication between neurons. \- <<https://docs.learnbittensor.org/subnets/neuron-tls-certificates>>

async get_all_revealed_commitments(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_revealed_commitments> "Link to this definition")
    

Retrieves all revealed commitments for a given subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnetwork.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

A dictionary mapping hotkey addresses to tuples of (reveal_block, commitment_message) pairs. Each validator can have multiple revealed commitments (up to 10 most recent).

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")], Ellipsis]]

Example

# sample return value

{

> “5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY”: ( (12, “Alice message 1”), (152, “Alice message 2”) ),
> 
> “5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty”: ( (12, “Bob message 1”), (147, “Bob message 2”) ),

}

Notes

  * <<https://docs.learnbittensor.org/glossary#commit-reveal>>




async get_all_subnets_info(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_subnets_info> "Link to this definition")
    

Retrieves detailed information about all subnets within the Bittensor network.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

A list of SubnetInfo objects, each containing detailed information about a subnet.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[bittensor.core.chain_data.SubnetInfo]

async get_all_subnets_netuid(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_subnets_netuid> "Link to this definition")
    

Retrieves the list of all subnet unique identifiers (netuids) currently present in the Bittensor network.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the subnet unique identifiers from.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

A list of subnet netuids.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

This function provides a comprehensive view of the subnets within the Bittensor network, offering insights into its diversity and scale.

async get_auto_stakes(_coldkey_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_auto_stakes> "Link to this definition")
    

Fetches auto stake destinations for a given wallet across all subnets.

Parameters:
    

  * **coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – Coldkey ss58 address.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash for the query.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

  * netuid: The unique identifier of the subnet.

  * hotkey: The hotkey of the wallet.




Return type:
    

Dictionary mapping netuid to hotkey, where

Notes

  * <<https://docs.learnbittensor.org/miners/autostaking>>




async get_balance(_address_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_balance> "Link to this definition")
    

Retrieves the balance for given coldkey.

This method queries the System module’s Account storage to get the current balance of a coldkey address. The balance represents the amount of TAO tokens held by the specified address.

Parameters:
    

  * **address** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The coldkey address in SS58 format.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

The balance object containing the account’s TAO balance.

Return type:
    

[Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

async get_balances(_* addresses_, _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_balances> "Link to this definition")
    

Retrieves the balance for given coldkey(s).

This method efficiently queries multiple coldkey addresses in a single batch operation, returning a dictionary mapping each address to its corresponding balance. This is more efficient than calling get_balance multiple times.

Parameters:
    

  * ***addresses** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – Variable number of coldkey addresses in SS58 format.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

A dictionary mapping each address to its Balance object.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")]

async get_block_hash(_block =None_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_block_hash> "Link to this definition")
    

Retrieves the hash of a specific block on the Bittensor blockchain.

The block hash is a unique identifier representing the cryptographic hash of the block’s content, ensuring its integrity and immutability. It is a fundamental aspect of blockchain technology, providing a secure reference to each block’s data. It is crucial for verifying transactions, ensuring data consistency, and maintaining the trustworthiness of the blockchain.

Parameters:
    

**block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number for which the hash is to be retrieved. If None, returns the latest block hash.

Returns:
    

The cryptographic hash of the specified block.

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

Notes

  * <<https://docs.learnbittensor.org/glossary#block>>




async get_block_info(_block =None_, _block_hash =None_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_block_info> "Link to this definition")
    

Retrieve complete information about a specific block from the Subtensor chain.

This method aggregates multiple low-level RPC calls into a single structured response, returning both the raw on-chain data and high-level decoded metadata for the given block.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number for which the hash is to be retrieved.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the block from.



Returns:
    

A dataclass containing all available information about the specified block, including:

>   * number: The block number.
> 
>   * hash: The corresponding block hash.
> 
>   * timestamp: The timestamp of the block (based on the Timestamp.Now extrinsic).
> 
>   * header: The raw block header returned by the node RPC.
> 
>   * extrinsics: The list of decoded extrinsics included in the block.
> 
>   * explorer: The link to block explorer service. Always related with finney block data.
> 
> 


Return type:
    

BlockInfo instance

async get_children(_hotkey_ss58_ , _netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_children> "Link to this definition")
    

Retrieves the children of a given hotkey and netuid.

This method queries the SubtensorModule’s ChildKeys storage function to get the children and formats them before returning as a tuple. It provides information about the child neurons that a validator has set for weight distribution.

Parameters:
    

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey value.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid value.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

A tuple containing a boolean indicating success or failure, a list of formatted children with their
    

proportions, and an error message (if applicable).

Return type:
    

[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"), [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"), [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]], [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]

Example

# Get children for a hotkey in subnet 1 success, children, error = await subtensor.get_children(hotkey=”5F…”, netuid=1) if success:

> for proportion, child_hotkey in children:
>     
> 
> print(f”Child {child_hotkey}: {proportion}”)

Notes

  * <<https://docs.learnbittensor.org/validators/child-hotkeys>>




async get_children_pending(_hotkey_ss58_ , _netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_children_pending> "Link to this definition")
    

Retrieves the pending children of a given hotkey and netuid.

This method queries the SubtensorModule’s PendingChildKeys storage function to get children that are pending approval or in a cooldown period. These are children that have been proposed but not yet finalized.

Parameters:
    

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey value.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid value.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number for which the children are to be retrieved.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the subnet unique identifiers from.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

A tuple containing:
    

  * list[tuple[float, str]]: A list of children with their proportions.

  * int: The cool-down block number.




Return type:
    

[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

Notes

  * <<https://docs.learnbittensor.org/validators/child-hotkeys>>




async get_coldkey_swap_announcement(_coldkey_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_announcement> "Link to this definition")
    

Retrieves coldkey swap announcement for a specific coldkey.

This method queries the SubtensorModule.ColdkeySwapAnnouncements storage for an announcement made by the given coldkey. Announcements allow a coldkey to declare its intention to swap to a new coldkey address after a delay period.

Parameters:
    

  * **coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the coldkey whose announcement to retrieve.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query. If None, queries the latest block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

ColdkeySwapAnnouncementInfo if announcement exists, None otherwise. Contains the execution block and
    

new coldkey hash.

Return type:
    

Optional[bittensor.core.chain_data.ColdkeySwapAnnouncementInfo]

Notes

  * If the coldkey has no announcement, returns None.

  * See: <<https://docs.learnbittensor.org/keys/coldkey-swap>>




async get_coldkey_swap_announcement_delay(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_announcement_delay> "Link to this definition")
    

Retrieves the ColdkeySwapAnnouncementDelay storage value.

This method queries the SubtensorModule.ColdkeySwapAnnouncementDelay storage value, which defines the number of blocks that must elapse after making an announcement before the swap can be executed.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query. If None, queries the latest block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

The number of blocks that must elapse before swap execution (integer).

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

Notes

  * This is a storage value (can be changed via admin extrinsics), not a runtime constant.

  * See: <<https://docs.learnbittensor.org/keys/coldkey-swap>>




async get_coldkey_swap_announcements(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_announcements> "Link to this definition")
    

Retrieves all coldkey swap announcements from the chain.

This method queries the SubtensorModule.ColdkeySwapAnnouncements storage map across all coldkeys and returns a list of all active announcements.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query. If None, queries the latest block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

List of ColdkeySwapAnnouncementInfo objects representing all active coldkey swap announcements on the chain.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[bittensor.core.chain_data.ColdkeySwapAnnouncementInfo]

Notes

  * This method queries all announcements on the chain, which may be resource-intensive for large networks. Consider using [`get_coldkey_swap_announcement()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_announcement> "bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_announcement") for querying specific coldkeys.

  * See: <<https://docs.learnbittensor.org/keys/coldkey-swap>>




async get_coldkey_swap_constants(_constants =None_, _as_dict =False_, _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_constants> "Link to this definition")
    

Fetches runtime configuration constants for coldkey swap operations.

This method retrieves on-chain runtime constants that define cost requirements for coldkey swap operations. Note: For delay values (ColdkeySwapAnnouncementDelay and ColdkeySwapReannouncementDelay), use the dedicated query methods get_coldkey_swap_announcement_delay() and get_coldkey_swap_reannouncement_delay() instead, as these are storage values, not runtime constants.

Parameters:
    

  * **constants** (_Optional_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]__]_) – Optional list of specific constant names to fetch. If omitted, all constants defined in ColdkeySwapConstants.constants_names() are queried. Valid constant names include: “KeySwapCost”.

  * **as_dict** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, returns the constants as a dictionary instead of a ColdkeySwapConstants object.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query. If None, queries the latest block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

ColdkeySwapConstants object containing all requested constants. If as_dict is True: Dictionary mapping constant names to their values (integers for cost in RAO).

Return type:
    

If as_dict is False

Notes

  * All amounts are returned in RAO. Values reflect the current chain configuration at the specified block.

  * KeySwapCost is a runtime constant (queryable via constants).

  * See: <<https://docs.learnbittensor.org/keys/coldkey-swap>>




async get_coldkey_swap_dispute(_coldkey_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_dispute> "Link to this definition")
    

Retrieves coldkey swap dispute for a specific coldkey.

This method queries the SubtensorModule.ColdkeySwapDisputes storage for a dispute recorded for the given coldkey. When a coldkey swap is disputed, the account is frozen until a root-only reset clears it.

Parameters:
    

  * **coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the coldkey whose dispute to retrieve.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query. If None, queries the latest block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

ColdkeySwapDisputeInfo if dispute exists, None otherwise. Contains the disputed block number.

Return type:
    

Optional[bittensor.core.chain_data.ColdkeySwapDisputeInfo]

Notes

  * If the coldkey has no dispute, returns None.

  * See: <<https://docs.learnbittensor.org/keys/coldkey-swap>>




async get_coldkey_swap_disputes(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_disputes> "Link to this definition")
    

Retrieves all coldkey swap disputes from the chain.

This method queries the SubtensorModule.ColdkeySwapDisputes storage map across all coldkeys and returns a list of all active disputes.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query. If None, queries the latest block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

List of ColdkeySwapDisputeInfo objects representing all active coldkey swap disputes on the chain.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[bittensor.core.chain_data.ColdkeySwapDisputeInfo]

Notes

  * This method queries all disputes on the chain, which may be resource-intensive for large networks. Consider using [`get_coldkey_swap_dispute()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_dispute> "bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_dispute") for querying specific coldkeys.

  * See: <<https://docs.learnbittensor.org/keys/coldkey-swap>>




async get_coldkey_swap_reannouncement_delay(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_reannouncement_delay> "Link to this definition")
    

Retrieves the ColdkeySwapReannouncementDelay storage value.

This method queries the SubtensorModule.ColdkeySwapReannouncementDelay storage value, which defines the number of blocks that must elapse between the original announcement and a reannouncement.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query. If None, queries the latest block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

The number of blocks that must elapse before reannouncement (integer).

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

Notes

  * This is a storage value (can be changed via admin extrinsics), not a runtime constant.

  * See: <<https://docs.learnbittensor.org/keys/coldkey-swap>>




async get_commitment(_netuid_ , _uid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_commitment> "Link to this definition")
    

Retrieves the on-chain commitment for a specific neuron in the Bittensor network.

This method retrieves the commitment data that a neuron has published to the blockchain. Commitments are used in the commit-reveal mechanism for secure weight setting and other network operations.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnetwork.

  * **uid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the neuron.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

The commitment data as a string.

# TODO: add a real example of how to handle realistic commitment data, or chop example

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

Notes

  * <<https://docs.learnbittensor.org/glossary#commit-reveal>>




async get_commitment_metadata(_netuid_ , _hotkey_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_commitment_metadata> "Link to this definition")
    

Fetches raw commitment metadata from specific subnet for given hotkey.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique subnet identifier.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey ss58 address.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block at which to check the hotkey ownership.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain hash.



Returns:
    

The raw commitment metadata. Returns a dict when commitment data exists, or an empty string when no commitment is found for the given hotkey on the subnet.

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") | [bittensor.core.types.CommitmentOfResponse](<../types/index.html#bittensor.core.types.CommitmentOfResponse> "bittensor.core.types.CommitmentOfResponse")

Notes

  * <<https://docs.learnbittensor.org/glossary#commit-reveal>>




async get_crowdloan_by_id(_crowdloan_id_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_crowdloan_by_id> "Link to this definition")
    

Retrieves detailed information about a specific crowdloan campaign.

Parameters:
    

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Unique identifier of the crowdloan (auto-incremented starting from 0).

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to query. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

campaign ID, creator address, creator’s deposit, minimum contribution amount, end block, funding cap, funds account address, amount raised, optional target address, optional embedded call, finalization status, and contributor count. Returns None if the crowdloan does not exist.

Return type:
    

CrowdloanInfo object containing

Notes

  * Crowdloans Overview: <<https://docs.learnbittensor.org/subnets/crowdloans>>




async get_crowdloan_constants(_constants =None_, _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_crowdloan_constants> "Link to this definition")
    

Retrieves runtime configuration constants governing crowdloan behavior and limits on the Bittensor blockchain.

If a list of constant names is provided, only those constants will be queried. Otherwise, all known constants defined in CrowdloanConstants.field_names() are fetched.

These constants define requirements and operational limits for crowdloan campaigns:
    

AbsoluteMinimumContribution: Minimum amount per contribution (TAO). MaxContributors: Maximum number of unique contributors per crowdloan. MaximumBlockDuration: Maximum duration (in blocks) for a crowdloan campaign (60 days = 432,000 blocks on

> production).

MinimumDeposit: Minimum deposit required from the creator (TAO). MinimumBlockDuration: Minimum duration (in blocks) for a crowdloan campaign (7 days = 50,400 blocks on

> production).

RefundContributorsLimit: Maximum number of contributors refunded per refund_crowdloan call (typically 50).

Parameters:
    

  * **constants** (_Optional_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]__]_) – Specific constant names to query. If None, retrieves all constants from CrowdloanConstants.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to query. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

A CrowdloanConstants data object containing the queried constants. Missing constants return None.

Return type:
    

bittensor.core.chain_data.CrowdloanConstants

Notes

These constants enforce contribution floors, duration bounds, and refund batching limits.

  * Crowdloans Overview: <<https://docs.learnbittensor.org/subnets/crowdloans>>




async get_crowdloan_contributions(_crowdloan_id_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_crowdloan_contributions> "Link to this definition")
    

Retrieves all contributions made to a specific crowdloan campaign.

Returns a mapping of contributor coldkey addresses to their contribution amounts in Rao.

Parameters:
    

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to query. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

Dictionary mapping contributor SS58 addresses to their Balance contribution amounts (in Rao). Returns empty dictionary if the crowdloan has no contributions or does not exist.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")]

Notes

Contributions are clipped to the remaining cap. Once the cap is reached, no further contributions are accepted.

  * Crowdloans Overview: <<https://docs.learnbittensor.org/subnets/crowdloans>>

  * Crowdloan Tutorial: <<https://docs.learnbittensor.org/subnets/crowdloans/crowdloans-tutorial#step-4-contribute-to-the-crowdloan>>




async get_crowdloan_next_id(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_crowdloan_next_id> "Link to this definition")
    

Retrieves the next available crowdloan identifier.

Crowdloan IDs are allocated sequentially starting from 0. This method returns the ID that will be assigned to the next crowdloan created via [`create_crowdloan()`](<#bittensor.core.async_subtensor.AsyncSubtensor.create_crowdloan> "bittensor.core.async_subtensor.AsyncSubtensor.create_crowdloan").

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to query. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

The next crowdloan ID (integer) to be assigned.

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

Notes

  * Crowdloans Overview: <<https://docs.learnbittensor.org/subnets/crowdloans>>

  * Crowdloan Tutorial: <<https://docs.learnbittensor.org/subnets/crowdloans/crowdloans-tutorial#get-the-crowdloan-id>>




async get_crowdloans(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_crowdloans> "Link to this definition")
    

Retrieves all existing crowdloan campaigns with their metadata.

Returns comprehensive information for all crowdloans registered on the blockchain, including both active and finalized campaigns.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to query. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

campaign ID, creator address, creator’s deposit, minimum contribution amount, end block, funding cap, funds account address, amount raised, optional target address, optional embedded call, finalization status, and contributor count. Returns empty list if no crowdloans exist.

Return type:
    

List of CrowdloanInfo objects, each containing

Notes

  * Crowdloans Overview: <<https://docs.learnbittensor.org/subnets/crowdloans>>

  * Crowdloan Lifecycle: <<https://docs.learnbittensor.org/subnets/crowdloans#crowdloan-lifecycle>>




async get_current_block()[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_current_block> "Link to this definition")
    

Returns the current block number on the Bittensor blockchain.

This function provides the latest block number, indicating the most recent state of the blockchain.

Returns:
    

The current chain block number.

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

Notes

  * <<https://docs.learnbittensor.org/glossary#block>>




async get_delegate_by_hotkey(_hotkey_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_delegate_by_hotkey> "Link to this definition")
    

Retrieves detailed information about a delegate neuron (validator) based on its hotkey. This function provides a comprehensive view of the delegate’s status, including its stakes, nominators, and reward distribution.

Parameters:
    

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the delegate’s hotkey.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

Detailed information about the delegate neuron, None if not found.

Return type:
    

Optional[bittensor.core.chain_data.DelegateInfo]

Notes

  * <<https://docs.learnbittensor.org/glossary#delegate>>

  * <<https://docs.learnbittensor.org/glossary#nominator>>




async get_delegate_identities(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_delegate_identities> "Link to this definition")
    

Fetches delegate identities.

Delegates are validators that accept stake from other TAO holders (nominators/delegators). This method retrieves the on-chain identity information for all delegates, including display name, legal name, web URLs, and other metadata they have set.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

Dictionary mapping delegate SS58 addresses to their ChainIdentity objects.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [bittensor.core.chain_data.chain_identity.ChainIdentity](<../chain_data/chain_identity/index.html#bittensor.core.chain_data.chain_identity.ChainIdentity> "bittensor.core.chain_data.chain_identity.ChainIdentity")]

Notes

  * <<https://docs.learnbittensor.org/staking-and-delegation/delegation>>




async get_delegate_take(_hotkey_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_delegate_take> "Link to this definition")
    

Retrieves the delegate ‘take’ percentage for a neuron identified by its hotkey. The ‘take’ represents the percentage of rewards that the delegate claims from its nominators’ stakes.

Parameters:
    

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the neuron’s hotkey.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

The delegate take percentage.

Return type:
    

[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")

Notes

  * <<https://docs.learnbittensor.org/staking-and-delegation/delegation>>




async get_delegated(_coldkey_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_delegated> "Link to this definition")
    

Retrieves delegates and their associated stakes for a given nominator coldkey.

This method identifies all delegates (validators) that a specific coldkey has staked tokens to, along with stake amounts and other delegation information. This is useful for account holders to understand their stake allocations and involvement in the network’s delegation and consensus mechanisms.

Parameters:
    

  * **coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the account’s coldkey.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

List of DelegatedInfo objects containing stake amounts and delegate information. Returns empty list if no delegations exist for the coldkey.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[bittensor.core.chain_data.delegate_info.DelegatedInfo](<../chain_data/delegate_info/index.html#bittensor.core.chain_data.delegate_info.DelegatedInfo> "bittensor.core.chain_data.delegate_info.DelegatedInfo")]

Notes

  * <<https://docs.learnbittensor.org/staking-and-delegation/delegation>>




async get_delegates(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_delegates> "Link to this definition")
    

Fetches all delegates registered on the chain.

Delegates are validators that accept stake from other TAO holders (nominators/delegators). This method retrieves comprehensive information about all delegates including their hotkeys, total stake, nominator count, take percentage, and other metadata.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

List of DelegateInfo objects containing comprehensive delegate information. Returns empty list if no delegates are registered.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[bittensor.core.chain_data.DelegateInfo]

Notes

  * <<https://docs.learnbittensor.org/staking-and-delegation/delegation>>




async get_ema_tao_inflow(_netuid_ , _block =None_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_ema_tao_inflow> "Link to this definition")
    

Retrieves the EMA (exponential moving average) of net TAO flow for a specific subnet.

The EMA tracks net TAO flows (staking minus unstaking) with a 30-day half-life (~86.8 day window), smoothing out short-term fluctuations while capturing sustained staking trends. This metric determines the subnet’s share of TAO emissions under the current, flow-based model. Positive values indicate net inflow (more staking than unstaking), negative values indicate net outflow. Subnets with negative EMA flows receive zero emissions.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet to query.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. If None, uses latest finalized block.



Returns:
    

Tuple of (last_updated_block, ema_flow) where ema_flow is the EMA of net TAO flow in TAO units. Returns None if the subnet does not exist or if querying subnet 0 (root network).

Return type:
    

Optional[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")]]

The EMA uses a smoothing factor α ≈ 0.000003209, creating a 30-day half-life and ~86.8 day window. Only direct stake/unstake operations count toward flows; neuron registrations and root claims are excluded. Subnet 0 (root network) does not have an EMA TAO flow value and will return None.

Notes

  * Flow-based emissions: <<https://docs.learnbittensor.org/learn/emissions#tao-reserve-injection>>

  * EMA smoothing: <<https://docs.learnbittensor.org/learn/ema>>




async get_existential_deposit(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_existential_deposit> "Link to this definition")
    

Retrieves the existential deposit amount for the Bittensor blockchain.

The existential deposit is the minimum amount of TAO required for an account to exist on the blockchain. Accounts with balances below this threshold can be reaped (removed) to conserve network resources and prevent blockchain bloat from dust accounts.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – Block hash at which to query the deposit amount. If None, the current block is used.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain block hash.



Returns:
    

The existential deposit amount in RAO.

Return type:
    

[bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

Notes

  * <<https://docs.learnbittensor.org/glossary#existential-deposit>>




async get_extrinsic_fee(_call_ , _keypair_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_extrinsic_fee> "Link to this definition")
    

Gets the extrinsic fee for a given extrinsic call and keypair.

This method estimates the transaction fee that will be charged for submitting the extrinsic to the blockchain. The fee is returned in Rao (the smallest unit of TAO, where 1 TAO = 1e9 Rao).

Parameters:
    

  * **call** (_scalecodec.GenericCall_) – The extrinsic GenericCall object representing the transaction to estimate.

  * **keypair** (_bittensor_wallet.Keypair_) – The keypair associated with the extrinsic (used to determine the account paying the fee).



Returns:
    

Balance object representing the extrinsic fee in Rao.

Return type:
    

[bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

Example

# Estimate fee before sending a transfer call = await subtensor.compose_call(

> call_module=”Balances”, call_function=”transfer_allow_death”, call_params={“dest”: destination_ss58, “value”: amount.rao}

) fee = await subtensor.get_extrinsic_fee(call=call, keypair=wallet.coldkey) print(f”Estimated fee: {fee.tao} TAO”)

Notes

To create the GenericCall object, use the compose_call method with proper parameters. \- <<https://docs.learnbittensor.org/learn/fees>>

async get_hotkey_owner(_hotkey_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_hotkey_owner> "Link to this definition")
    

Retrieves the owner of the given hotkey at a specific block hash. This function queries the blockchain for the owner of the provided hotkey. If the hotkey does not exist at the specified block hash, it returns None.

Parameters:
    

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the hotkey.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block at which to check the hotkey ownership.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain hash.



Returns:
    

The SS58 address of the owner if the hotkey exists, or None if it doesn’t.

Return type:
    

Optional[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]

Notes

  * <<https://docs.learnbittensor.org/glossary#hotkey>>

  * <<https://docs.learnbittensor.org/glossary#subnet>>

  * <<https://docs.learnbittensor.org/glossary#neuron>>




get_hotkey_stake[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_hotkey_stake> "Link to this definition")
    

async get_hyperparameter(_param_name_ , _netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_hyperparameter> "Link to this definition")
    

Retrieves a specified hyperparameter for a specific subnet.

This method queries the blockchain for subnet-specific hyperparameters such as difficulty, tempo, immunity period, and other network configuration values. Return types and units vary by parameter.

Parameters:
    

  * **param_name** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The name of the hyperparameter storage function to retrieve.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

The value of the specified hyperparameter if the subnet exists, None otherwise. Return type varies by parameter (int, float, bool, or Balance).

Return type:
    

Optional[[Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any")]

Notes

  * <<https://docs.learnbittensor.org/subnets/subnet-hyperparameters>>




async get_last_bonds_reset(_netuid_ , _hotkey_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_last_bonds_reset> "Link to this definition")
    

Retrieves the block number when bonds were last reset for a specific hotkey on a subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network uid to fetch from.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey of the neuron for which to fetch the last bonds reset.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the parameter from. Do not specify if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to use the last-used block. Do not set if using block_hash or block.



Returns:
    

A ScaleType object containing the block number when bonds were last reset, or None if no bonds reset has occurred.

Return type:
    

scalecodec.base.ScaleType[Optional[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]]

Notes

  * <<https://docs.learnbittensor.org/resources/glossary#validator-miner-bonds>>

  * <<https://docs.learnbittensor.org/resources/glossary#commit-reveal>>




async get_last_commitment_bonds_reset_block(_netuid_ , _uid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_last_commitment_bonds_reset_block> "Link to this definition")
    

Retrieves the last block number when the bonds reset were triggered by publish_metadata for a specific neuron.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnetwork.

  * **uid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the neuron.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the parameter from. Do not specify if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to use the last-used block. Do not set if using block_hash or block.



Returns:
    

The block number when the bonds were last reset, or None if not found.

Return type:
    

Optional[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

async get_liquidity_list(_wallet_ , _netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_liquidity_list> "Link to this definition")
    

Retrieves all liquidity positions for the given wallet on a specified subnet (netuid). Calculates associated fee rewards based on current global and tick-level fee data.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Wallet instance to fetch positions for.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Subnet unique id.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number for which the children are to be retrieved.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the subnet unique identifiers from.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

List of liquidity positions, or None if subnet does not exist.

Return type:
    

Optional[[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[bittensor.utils.liquidity.LiquidityPosition](<../../utils/liquidity/index.html#bittensor.utils.liquidity.LiquidityPosition> "bittensor.utils.liquidity.LiquidityPosition")]]

Notes

  * <<https://docs.learnbittensor.org/liquidity-positions/>

  * <<https://docs.learnbittensor.org/liquidity-positions/managing-liquidity-positions>>




async get_mechanism_count(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_mechanism_count> "Link to this definition")
    

Retrieves the number of mechanisms for the given subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Subnet identifier.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the stake from. Do not specify if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to use the last-used block. Do not set if using block_hash or block.



Returns:
    

The number of mechanisms for the given subnet.

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

Notes

  * <<https://docs.learnbittensor.org/subnets/understanding-multiple-mech-subnets>>




async get_mechanism_emission_split(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_mechanism_emission_split> "Link to this definition")
    

Returns the emission percentages allocated to each subnet mechanism.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the stake from. Do not specify if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to use the last-used block. Do not set if using block_hash or block.



Returns:
    

A list of integers representing the percentage of emission allocated to each subnet mechanism (rounded to whole numbers). Returns None if emission is evenly split or if the data is unavailable.

Return type:
    

Optional[[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]]

Notes

  * <<https://docs.learnbittensor.org/subnets/understanding-multiple-mech-subnets>>




async get_metagraph_info(_netuid_ , _mechid =0_, _selected_indices =None_, _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_metagraph_info> "Link to this definition")
    

Retrieves full or partial metagraph information for the specified subnet (netuid).

A metagraph is a data structure that contains comprehensive information about the current state of a subnet, including detailed information on all the nodes (neurons) such as subnet validator stakes and subnet weights in the subnet. Metagraph aids in calculating emissions.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet to query.

  * **selected_indices** (_Optional_ _[__Union_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[__bittensor.core.chain_data.SelectiveMetagraphIndex_ _]__,_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]__]__]_) – Optional list of SelectiveMetagraphIndex or int values specifying which fields to retrieve. If not provided, all available fields will be returned.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the blockchain block number at which to perform the query.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash when retrieving info.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Subnet mechanism unique identifier.



Returns:
    

MetagraphInfo object with the requested subnet mechanism data, None if the subnet mechanism does not exist.

Return type:
    

Optional[bittensor.core.chain_data.MetagraphInfo]

Example

# Retrieve all fields from the metagraph from subnet 2 mechanism 0 meta_info = subtensor.get_metagraph_info(netuid=2)

# Retrieve all fields from the metagraph from subnet 2 mechanism 1 meta_info = subtensor.get_metagraph_info(netuid=2, mechid=1)

# Retrieve selective data from the metagraph from subnet 2 mechanism 0 partial_meta_info = subtensor.get_metagraph_info(

> netuid=2, selected_indices=[SelectiveMetagraphIndex.Name, SelectiveMetagraphIndex.OwnerHotkeys]

)

# Retrieve selective data from the metagraph from subnet 2 mechanism 1 partial_meta_info = subtensor.get_metagraph_info(

> netuid=2, mechid=1, selected_indices=[SelectiveMetagraphIndex.Name, SelectiveMetagraphIndex.OwnerHotkeys]

)

Notes

  * <<https://docs.learnbittensor.org/subnets/metagraph>>




async get_mev_shield_current_key(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_mev_shield_current_key> "Link to this definition")
    

Retrieves the CurrentKey from the MevShield pallet storage.

The CurrentKey contains the ML-KEM-768 public key that is currently being used for encryption in this block. This key is rotated from NextKey at the beginning of each block.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the stake from. Do not specify if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to use the last-used block. Do not set if using block_hash or block.



Returns:
    

The ML-KEM-768 public key as bytes (1184 bytes for ML-KEM-768)

Return type:
    

Optional[[bytes](<../../extras/dev_framework/calls/non_sudo_calls/index.html#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes> "bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes")]

Note

If CurrentKey is not set (None in storage), this function returns None. This can happen if no validator has announced a key yet.

async get_mev_shield_next_key(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_mev_shield_next_key> "Link to this definition")
    

Retrieves the NextKey from the MevShield pallet storage.

The NextKey contains the ML-KEM-768 public key that will be used for encryption in the next block. This key is rotated from NextKey to CurrentKey at the beginning of each block.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the stake from. Do not specify if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to use the last-used block. Do not set if using block_hash or block.



Returns:
    

The ML-KEM-768 public key as bytes (1184 bytes for ML-KEM-768)

Return type:
    

Optional[[bytes](<../../extras/dev_framework/calls/non_sudo_calls/index.html#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes> "bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes")]

Note

If NextKey is not set (None in storage), this function returns None. This can happen if no validator has announced the next key yet.

async get_minimum_required_stake()[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_minimum_required_stake> "Link to this definition")
    

Returns the minimum required stake threshold for nominator cleanup operations.

This threshold is used ONLY for cleanup after unstaking operations. If a nominator’s remaining stake falls below this minimum after an unstake, the remaining stake is forcefully cleared and returned to the coldkey to prevent dust accounts.

This is NOT the minimum checked during staking operations. The actual minimum for staking is determined by DefaultMinStake (typically 0.001 TAO plus fees).

Returns:
    

The minimum stake threshold as a Balance object. Nominator stakes below this amount are automatically cleared after unstake operations.

Return type:
    

[bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

Notes

  * <<https://docs.learnbittensor.org/staking-and-delegation/delegation>>




async get_netuids_for_hotkey(_hotkey_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_netuids_for_hotkey> "Link to this definition")
    

Retrieves a list of subnet UIDs (netuids) where a given hotkey is a member. This function identifies the specific subnets within the Bittensor network where the neuron associated with the hotkey is active.

Parameters:
    

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the neuron’s hotkey.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the blockchain block number at which to perform the query.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash when retrieving info.



Returns:
    

A list of netuids where the neuron is a member.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

Notes

  * <<https://docs.learnbittensor.org/glossary#hotkey>>




async get_neuron_certificate(_hotkey_ss58_ , _netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_neuron_certificate> "Link to this definition")
    

Retrieves the TLS certificate for a specific neuron identified by its unique identifier (UID) within a specified subnet (netuid) of the Bittensor network.

Parameters:
    

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the neuron’s hotkey.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the parameter from. Do not specify if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to use the last-used block. Do not set if using block_hash or block.



Returns:
    

Certificate object containing the neuron’s TLS public key and algorithm, or None if the neuron has not registered a certificate.

Return type:
    

Optional[[bittensor.utils.Certificate](<../../utils/index.html#bittensor.utils.Certificate> "bittensor.utils.Certificate")]

This function is used for certificate discovery for setting up mutual tls communication between neurons.

async get_neuron_for_pubkey_and_subnet(_hotkey_ss58_ , _netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_neuron_for_pubkey_and_subnet> "Link to this definition")
    

Retrieves information about a neuron based on its public key (hotkey SS58 address) and the specific subnet UID (netuid). This function provides detailed neuron information for a particular subnet within the Bittensor network.

Parameters:
    

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the neuron’s hotkey.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The blockchain block number at which to perform the query.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain block hash.



Returns:
    

Detailed information about the neuron if found, None otherwise.

Return type:
    

bittensor.core.chain_data.NeuronInfo

This function is crucial for accessing specific neuron data and understanding its status, stake, and other attributes within a particular subnet of the Bittensor ecosystem.

async get_next_epoch_start_block(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_next_epoch_start_block> "Link to this definition")
    

Calculates the first block number of the next epoch for the given subnet.

If block is not provided, the current chain block will be used. Epochs are determined based on the subnet’s tempo (i.e., blocks per epoch). The result is the block number at which the next epoch will begin.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The reference block to calculate from. If None, uses the current chain block height.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The blockchain block number at which to perform the query.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain block hash.



Returns:
    

The block number at which the next epoch will start.

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

Notes

  * <<https://docs.learnbittensor.org/glossary#tempo>>




async get_owned_hotkeys(_coldkey_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_owned_hotkeys> "Link to this definition")
    

Retrieves all hotkeys owned by a specific coldkey address.

Parameters:
    

  * **coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the coldkey to query.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the blockchain block number for the query.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain block hash.



Returns:
    

A list of hotkey SS58 addresses owned by the coldkey.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]

async get_parents(_hotkey_ss58_ , _netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_parents> "Link to this definition")
    

This method retrieves the parent of a given hotkey and netuid. It queries the SubtensorModule’s ParentKeys storage function to get the children and formats them before returning as a tuple.

Parameters:
    

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The child hotkey SS58.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid value.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

A list of formatted parents [(proportion, parent)]

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"), [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]]

Notes

  * <<https://docs.learnbittensor.org/validators/child-hotkeys>>

  * [`get_children()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_children> "bittensor.core.async_subtensor.AsyncSubtensor.get_children") for retrieving child keys




async get_proxies(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_proxies> "Link to this definition")
    

Retrieves all proxy relationships from the chain.

This method queries the Proxy.Proxies storage map across all accounts and returns a dictionary mapping each real account (delegator) to its list of proxy relationships.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query. If None, queries the latest block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

Dictionary mapping real account SS58 addresses to lists of ProxyInfo objects. Each ProxyInfo contains the
    

delegate address, proxy type, and delay for that proxy relationship.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[bittensor.core.chain_data.ProxyInfo]]

Notes

  * This method queries all proxy relationships on the chain, which may be resource-intensive for large networks. Consider using [`get_proxies_for_real_account()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_proxies_for_real_account> "bittensor.core.async_subtensor.AsyncSubtensor.get_proxies_for_real_account") for querying specific accounts.

  * See: <<https://docs.learnbittensor.org/keys/proxies>>




async get_proxies_for_real_account(_real_account_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_proxies_for_real_account> "Link to this definition")
    

Returns proxy/ies associated with the provided real account.

This method queries the Proxy.Proxies storage for a specific real account and returns all proxy relationships where this real account is the delegator. It also returns the deposit amount reserved for these proxies.

Parameters:
    

  * **real_account_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the real account (delegator) whose proxies to retrieve.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

  * List of ProxyInfo objects representing all proxy relationships for the real account. Each ProxyInfo
    

contains delegate address, proxy type, and delay.

  * Balance object representing the reserved deposit amount for these proxies. This deposit is held as
    

long as the proxy relationships exist and is returned when proxies are removed.




Return type:
    

Tuple containing

Notes

  * If the account has no proxies, returns an empty list and a zero balance.

  * See: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>




async get_proxy_announcement(_delegate_account_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_proxy_announcement> "Link to this definition")
    

Retrieves proxy announcements for a specific delegate account.

This method queries the Proxy.Announcements storage for announcements made by the given delegate proxy account. Announcements allow a proxy to declare its intention to execute a call on behalf of a real account after a delay period.

Parameters:
    

  * **delegate_account_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the delegate proxy account whose announcements to retrieve.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query. If None, queries the latest block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

List of ProxyAnnouncementInfo objects. Each object contains the real account address, call hash, and block
    

height at which the announcement was made.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[bittensor.core.chain_data.ProxyAnnouncementInfo]

Notes

  * If the delegate has no announcements, returns an empty list.

  * See: <<https://docs.learnbittensor.org/keys/proxies>>




async get_proxy_announcements(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_proxy_announcements> "Link to this definition")
    

Retrieves all proxy announcements from the chain.

This method queries the Proxy.Announcements storage map across all delegate accounts and returns a dictionary mapping each delegate to its list of pending announcements.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query. If None, queries the latest block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

Dictionary mapping delegate account SS58 addresses to lists of ProxyAnnouncementInfo objects. Each ProxyAnnouncementInfo contains the real account address, call hash, and block height.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[bittensor.core.chain_data.ProxyAnnouncementInfo]]

Notes

  * This method queries all announcements on the chain, which may be resource-intensive for large networks. Consider using [`get_proxy_announcement()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_proxy_announcement> "bittensor.core.async_subtensor.AsyncSubtensor.get_proxy_announcement") for querying specific delegates.

  * See: <<https://docs.learnbittensor.org/keys/proxies>>




async get_proxy_constants(_constants =None_, _as_dict =False_, _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_proxy_constants> "Link to this definition")
    

Fetches runtime configuration constants from the Proxy pallet.

This method retrieves on-chain configuration constants that define deposit requirements, proxy limits, and announcement constraints for the Proxy pallet. These constants govern how proxy accounts operate within the Subtensor network.

Parameters:
    

  * **constants** (_Optional_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]__]_) – Optional list of specific constant names to fetch. If omitted, all constants defined in ProxyConstants.constants_names() are queried. Valid constant names include: “AnnouncementDepositBase”, “AnnouncementDepositFactor”, “MaxProxies”, “MaxPending”, “ProxyDepositBase”, “ProxyDepositFactor”.

  * **as_dict** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, returns the constants as a dictionary instead of a ProxyConstants object.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query. If None, queries the latest block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

ProxyConstants object containing all requested constants. If as_dict is True: Dictionary mapping constant names to their values (Balance objects for deposit

> constants, integers for limit constants).

Return type:
    

If as_dict is False

Notes

  * All Balance amounts are returned in RAO. Constants reflect the current chain configuration at the specified block.

  * See: <<https://docs.learnbittensor.org/keys/proxies>>




async get_revealed_commitment(_netuid_ , _uid_ , _block =None_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_revealed_commitment> "Link to this definition")
    

Returns uid related revealed commitment for a given netuid.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnetwork.

  * **uid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The neuron uid to retrieve the commitment from.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to retrieve the commitment from.



Returns:
    

A tuple of reveal block and commitment message.

Return type:
    

Optional[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")], Ellipsis]]

Example

# sample return value

( (12, “Alice message 1”), (152, “Alice message 2”) )

( (12, “Bob message 1”), (147, “Bob message 2”) )

Notes

  * <<https://docs.learnbittensor.org/glossary#commit-reveal>>




async get_revealed_commitment_by_hotkey(_netuid_ , _hotkey_ss58 =None_, _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_revealed_commitment_by_hotkey> "Link to this definition")
    

Retrieves hotkey related revealed commitment for a given subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnetwork.

  * **hotkey_ss58** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The ss58 address of the committee member.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

A tuple of reveal block and commitment message.

Return type:
    

Optional[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")], Ellipsis]]

# TODO: add example to clarify return ordering and units; @roman can you help w this? .. admonition:: Notes

>   * <<https://docs.learnbittensor.org/glossary#commit-reveal>>
> 
> 


async get_root_alpha_dividends_per_subnet(_hotkey_ss58_ , _netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_root_alpha_dividends_per_subnet> "Link to this definition")
    

Retrieves the root alpha dividends per subnet for a given hotkey.

This storage tracks the root alpha dividends that a hotkey has received on a specific subnet. It is updated during block emission distribution when root alpha is distributed to validators.

Parameters:
    

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The ss58 address of the root validator hotkey.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

The root alpha dividends for this hotkey on this subnet in Rao, with unit set to netuid.

Return type:
    

[Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

async get_root_claim_type(_coldkey_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_root_claim_type> "Link to this definition")
    

Return the configured root claim type for a given coldkey.

The root claim type controls how dividends from staking to the Root Subnet (subnet 0) are processed when they are claimed:

  * Swap (default): Alpha dividends are swapped to TAO at claim time and restaked on the root subnet.

  * Keep: Alpha dividends remain as Alpha on the originating subnets.




Parameters:
    

  * **coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the coldkey whose root claim preference to query.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to query the claim type. Do not specify if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not specify if using block or block_hash.



Returns:
    

The root claim type as a string, either Swap or Keep, or dict for “KeepSubnets” in format {“KeepSubnets”: {“subnets”: [1, 2, 3]}}.

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") | [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]]]

Notes

  * The claim type applies to both automatic and manual root claims; it does not affect the original TAO stake on subnet 0, only how Alpha dividends are treated.

  * See: <<https://docs.learnbittensor.org/staking-and-delegation/root-claims>>

  * See also: <<https://docs.learnbittensor.org/staking-and-delegation/root-claims/managing-root-claims>>




async get_root_claimable_all_rates(_hotkey_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_root_claimable_all_rates> "Link to this definition")
    

Retrieves all root claimable rates from a given hotkey address for all subnets with this validator.

Parameters:
    

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the root validator hotkey.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to query. Do not specify if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not specify if using block or block_hash.



Returns:
    

Dictionary mapping netuid to a float claimable rate (approximately in the range [0.0, 1.0]) for that subnet. Missing entries imply no claimable Alpha dividends for that subnet.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")]

Notes

  * See: <<https://docs.learnbittensor.org/staking-and-delegation/root-claims/managing-root-claims>>




async get_root_claimable_rate(_hotkey_ss58_ , _netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_root_claimable_rate> "Link to this definition")
    

Return the fraction of root stake currently claimable on a subnet.

This method returns a normalized rate representing how much Alpha dividends are currently claimable on the given subnet relative to the validator’s root stake. It is primarily a low-level helper; most users should call [`get_root_claimable_stake()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_root_claimable_stake> "bittensor.core.async_subtensor.AsyncSubtensor.get_root_claimable_stake") instead to obtain a Balance.

Parameters:
    

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the root validator hotkey.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet whose claimable rate to compute.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to query. Do not specify if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not specify if using block or block_hash.



Returns:
    

A float representing the claimable rate for this subnet (approximately in the range [0.0, 1.0]). A value of 0.0 means there are currently no claimable Alpha dividends on the subnet.

Return type:
    

[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")

Notes

  * Use [`get_root_claimable_stake()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_root_claimable_stake> "bittensor.core.async_subtensor.AsyncSubtensor.get_root_claimable_stake") to retrieve the actual claimable amount as a Balance object.

  * See: <<https://docs.learnbittensor.org/staking-and-delegation/root-claims/managing-root-claims>>




async get_root_claimable_stake(_coldkey_ss58_ , _hotkey_ss58_ , _netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_root_claimable_stake> "Link to this definition")
    

Return the currently claimable Alpha staking dividends for a coldkey from a root validator on a subnet.

Parameters:
    

  * **coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the delegator’s coldkey.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the root validator hotkey.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet ID where Alpha dividends will be claimed.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to query. Do not specify if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not specify if using block or block_hash.



Returns:
    

Balance representing the Alpha stake currently available to claim on the specified subnet (unit is the subnet’s Alpha token).

Return type:
    

[bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

Notes

  * After a successful manual or automatic claim, this value typically drops to zero for that subnet until new dividends accumulate.

  * The underlying TAO stake on the Root Subnet remains unaffected; only Alpha dividends are moved or swapped according to the configured root claim type.

  * See: <<https://docs.learnbittensor.org/staking-and-delegation/root-claims>>

  * See also: <<https://docs.learnbittensor.org/staking-and-delegation/root-claims/managing-root-claims>>




async get_root_claimed(_coldkey_ss58_ , _hotkey_ss58_ , _netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_root_claimed> "Link to this definition")
    

Return the total Alpha dividends already claimed for a coldkey from a root validator on a subnet.

Parameters:
    

  * **coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the delegator’s coldkey.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the root validator hotkey.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to query. Do not specify if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not specify if using block or block_hash.



Returns:
    

Balance representing the cumulative Alpha stake that has already been claimed from the root validator on the specified subnet.

Return type:
    

[bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

Notes

  * See: <<https://docs.learnbittensor.org/staking-and-delegation/root-claims/managing-root-claims>>




async get_stake(_coldkey_ss58_ , _hotkey_ss58_ , _netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake> "Link to this definition")
    

Returns the amount of Alpha staked by a specific coldkey to a specific hotkey within a given subnet.

Parameters:
    

  * **coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the coldkey that delegated the stake. This address owns the stake.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the hotkey which the stake is on.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet to query.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The specific block number at which to retrieve the stake information. or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the stake from. Do not specify if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to use the last-used block hash. Do not set if using block_hash or block.



Returns:
    

An object representing the amount of Alpha (TAO ONLY if the subnet’s netuid is 0) currently staked from the
    

specified coldkey to the specified hotkey within the given subnet.

Return type:
    

[bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

async get_stake_add_fee(_amount_ , _netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_add_fee> "Link to this definition")
    

Calculates the fee for adding new stake to a hotkey.

Parameters:
    

  * **amount** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – Amount of stake to add in TAO

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Netuid of subnet

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number for which the children are to be retrieved.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the subnet unique identifiers from.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

The calculated stake fee as a Balance object in TAO.

Return type:
    

[bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

Notes

  * <<https://docs.learnbittensor.org/learn/fees>>




async get_stake_for_coldkey_and_hotkey(_coldkey_ss58_ , _hotkey_ss58_ , _netuids =None_, _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_for_coldkey_and_hotkey> "Link to this definition")
    

Retrieves all coldkey-hotkey pairing stake across specified (or all) subnets

Parameters:
    

  * **coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the coldkey.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the hotkey.

  * **netuids** (_Optional_ _[_[_bittensor.core.types.UIDs_](<../types/index.html#bittensor.core.types.UIDs> "bittensor.core.types.UIDs") _]_) – The subnet IDs to query for. Set to None for all subnets.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number for which the children are to be retrieved.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the subnet unique identifiers from.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

A netuid to StakeInfo mapping of all stakes across all subnets.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), bittensor.core.chain_data.StakeInfo]

async get_stake_for_hotkey(_hotkey_ss58_ , _netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_for_hotkey> "Link to this definition")
    

Retrieves the total stake for a given hotkey on a specific subnet.

Parameters:
    

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the hotkey.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet ID to query for.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the stake from.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

The total stake for the hotkey on the specified subnet.

Return type:
    

[Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

async get_stake_info_for_coldkey(_coldkey_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_info_for_coldkey> "Link to this definition")
    

Retrieves the stake information for a given coldkey.

Parameters:
    

  * **coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the coldkey.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number at which to query the stake information.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the blockchain block number for the query.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

List of StakeInfo objects.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[bittensor.core.chain_data.StakeInfo]

async get_stake_info_for_coldkeys(_coldkey_ss58s_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_info_for_coldkeys> "Link to this definition")
    

Retrieves the stake information for multiple coldkeys.

Parameters:
    

  * **coldkey_ss58s** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – A list of SS58 addresses of the coldkeys to query.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number at which to query the stake information.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the blockchain block number for the query.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

The dictionary mapping coldkey addresses to a list of StakeInfo objects.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[bittensor.core.chain_data.StakeInfo]]

async get_stake_movement_fee(_origin_netuid_ , _destination_netuid_ , _amount_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_movement_fee> "Link to this definition")
    

Calculates the fee for moving stake between hotkeys/subnets/coldkeys.

Parameters:
    

  * **origin_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Netuid of source subnet.

  * **destination_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Netuid of the destination subnet.

  * **amount** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – Amount of stake to move.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number for which the children are to be retrieved.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the subnet unique identifiers from.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

The calculated stake fee as a Balance object

Return type:
    

[bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

Notes

  * <<https://docs.learnbittensor.org/learn/fees>>




async get_stake_weight(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_weight> "Link to this definition")
    

Retrieves the stake weight for all hotkeys in a given subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Netuid of subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number for which the children are to be retrieved.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the subnet unique identifiers from.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

A list of stake weights for all hotkeys in the specified subnet.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")]

async get_staking_hotkeys(_coldkey_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_staking_hotkeys> "Link to this definition")
    

Retrieves the hotkeys that have staked for a given coldkey.

Parameters:
    

  * **coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the coldkey.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number at which to query the stake information.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the blockchain block number for the query.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

A list of hotkey SS58 addresses that have staked for the given coldkey.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]

async get_start_call_delay(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_start_call_delay> "Link to this definition")
    

Retrieves the start call delay in blocks.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The blockchain block_hash of the block id.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

Amount of blocks after the start call can be executed.

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

async get_subnet_burn_cost(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_burn_cost> "Link to this definition")
    

Retrieves the burn cost for registering a new subnet within the Bittensor network. This cost represents the
    

amount of Tao that needs to be locked or burned to establish a new

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The blockchain block_hash of the block id.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

The burn cost for subnet registration.

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

The subnet burn cost is an important economic parameter, reflecting the network’s mechanisms for controlling
    

the proliferation of subnets and ensuring their commitment to the network’s long-term viability.

async get_subnet_hyperparameters(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_hyperparameters> "Link to this definition")
    

Retrieves the hyperparameters for a specific subnet within the Bittensor network. These hyperparameters define the operational settings and rules governing the subnet’s behavior.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network UID of the subnet to query.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the blockchain block number for the query.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain hash.



Returns:
    

The subnet’s hyperparameters, or None if not available.

Return type:
    

Optional[bittensor.core.chain_data.SubnetHyperparameters]

Understanding the hyperparameters is crucial for comprehending how subnets are configured and managed, and how they interact with the network’s consensus and incentive mechanisms.

async get_subnet_info(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_info> "Link to this definition")
    

Retrieves detailed information about subnet within the Bittensor network. This function provides comprehensive data on subnet, including its characteristics and operational parameters.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number for which the children are to be retrieved.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the subnet unique identifiers from.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

A SubnetInfo objects, each containing detailed information about a subnet.

Return type:
    

[SubnetInfo](<../chain_data/subnet_info/index.html#bittensor.core.chain_data.subnet_info.SubnetInfo> "bittensor.core.chain_data.subnet_info.SubnetInfo")

Gaining insights into the subnet’s details assists in understanding the network’s composition, the roles of different subnets, and their unique features.

async get_subnet_owner_hotkey(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_owner_hotkey> "Link to this definition")
    

Retrieves the hotkey of the subnet owner for a given network UID.

This function queries the subtensor network to fetch the hotkey of the owner of a subnet specified by its netuid. If no data is found or the query fails, the function returns None.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network UID of the subnet to fetch the owner’s hotkey for.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The blockchain block_hash representation of the block id.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain block hash.



Returns:
    

The hotkey of the subnet owner if available; None otherwise.

Return type:
    

Optional[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]

async get_subnet_price(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_price> "Link to this definition")
    

Gets the current Alpha price in TAO for the specified subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the stake from. Do not specify if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to use the last-used block. Do not set if using block_hash or block.



Returns:
    

The current Alpha price in TAO units for the specified subnet.

Return type:
    

[bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

Notes

Subnet 0 (root network) always returns 1 TAO since it uses TAO directly rather than Alpha.

async get_subnet_prices(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_prices> "Link to this definition")
    

Gets the current Alpha price in TAO for all subnets.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number for which the children are to be retrieved.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the subnet unique identifiers from.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

A dictionary mapping subnet unique ID (netuid) to the current Alpha price in TAO units.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")]

Notes

Subnet 0 (root network) always has a price of 1 TAO since it uses TAO directly rather than Alpha.

async get_subnet_reveal_period_epochs(_netuid_ , _block =None_, _block_hash =None_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_reveal_period_epochs> "Link to this definition")
    

Retrieves the SubnetRevealPeriodEpochs hyperparameter for a specified subnet.

This hyperparameter determines the number of epochs that must pass before a committed weight can be revealed in the commit-reveal mechanism.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query. Do not specify if using block_hash.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block.



Returns:
    

The number of epochs in the reveal period for the subnet.

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

Notes

  * <<https://docs.learnbittensor.org/glossary#commit-reveal>>




async get_subnet_validator_permits(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_validator_permits> "Link to this definition")
    

Retrieves the list of validator permits for a given subnet as boolean values.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnetwork.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The blockchain block_hash representation of the block id.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain block hash.



Returns:
    

A list of boolean values representing validator permits, or None if not available.

Return type:
    

Optional[[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")]]

async get_timelocked_weight_commits(_netuid_ , _mechid =0_, _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_timelocked_weight_commits> "Link to this definition")
    

Retrieves CRv4 (Commit-Reveal version 4) weight commit information for a specific subnet.

This method retrieves timelocked weight commitments made by validators using the commit-reveal mechanism. The raw byte/vector encoding from the chain is automatically parsed and converted into a structured format via WeightCommitInfo.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Subnet mechanism identifier (default 0 for primary mechanism).

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

  * ss58_address: The SS58 address of the committer.

  * commit_block: The block number when the commitment was made.

  * commit_message: The commit message (encoded commitment data).

  * reveal_round: The drand round when the commitment can be revealed.




Return type:
    

A list of commit details, where each item is a tuple containing

Notes

The list may be empty if there are no commits found. \- <<https://docs.learnbittensor.org/resources/glossary#commit-reveal>>

async get_timestamp(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_timestamp> "Link to this definition")
    

Retrieves the datetime timestamp for a given block.

This method queries the Timestamp pallet to get the block’s timestamp. The on-chain timestamp is stored in milliseconds (Unix timestamp in milliseconds), which is automatically converted to a Python datetime object (Unix timestamp in seconds).

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

A datetime object representing the timestamp of the specified block.

Return type:
    

[datetime.datetime](<https://docs.python.org/3/library/datetime.html#datetime.datetime> "\(in Python v3.14\)")

Notes

  * <<https://docs.learnbittensor.org/resources/glossary#block>>




async get_total_subnets(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_total_subnets> "Link to this definition")
    

Retrieves the total number of subnets within the Bittensor network as of a specific blockchain block.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The blockchain block_hash representation of block id.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

The total number of subnets in the network.

Return type:
    

Optional[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

async get_transfer_fee(_wallet_ , _destination_ss58_ , _amount_ , _keep_alive =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_transfer_fee> "Link to this definition")
    

Calculates the transaction fee for transferring tokens from a wallet to a specified destination address. This function simulates the transfer to estimate the associated cost, taking into account the current network conditions and transaction complexity.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet from which the transfer is initiated.

  * **destination_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the destination account.

  * **amount** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – The amount of tokens to be transferred, specified as a Balance object, or in Tao (float) or Rao (int) units.

  * **keep_alive** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether the transfer fee should be calculated based on keeping the wallet alive (existential deposit) or not.



Returns:
    

The estimated transaction fee for the transfer, represented as a Balance
    

object.

Return type:
    

[bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

Notes

  * <<https://docs.learnbittensor.org/learn/fees>>




async get_uid_for_hotkey_on_subnet(_hotkey_ss58_ , _netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_uid_for_hotkey_on_subnet> "Link to this definition")
    

Retrieves the unique identifier (UID) for a neuron’s hotkey on a specific subnet.

Parameters:
    

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the neuron’s hotkey.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The blockchain block_hash representation of the block id.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain block hash.



Returns:
    

The UID of the neuron if it is registered on the subnet, None otherwise.

Return type:
    

Optional[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

The UID is a critical identifier within the network, linking the neuron’s hotkey to its operational and governance activities on a particular subnet.

async get_unstake_fee(_netuid_ , _amount_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_unstake_fee> "Link to this definition")
    

Calculates the fee for unstaking from a hotkey.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **amount** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – Amount of stake to unstake in TAO.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The blockchain block_hash representation of the block id.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain block hash.



Returns:
    

The calculated stake fee as a Balance object in Alpha.

Return type:
    

[bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

Notes

  * <<https://docs.learnbittensor.org/learn/fees>>




async get_vote_data(_proposal_hash_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.get_vote_data> "Link to this definition")
    

Retrieves the voting data for a specific proposal on the Bittensor blockchain. This data includes information about how senate members have voted on the proposal.

Parameters:
    

  * **proposal_hash** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hash of the proposal for which voting data is requested.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the blockchain block number to query the voting data.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain block hash.



Returns:
    

An object containing the proposal’s voting data, or None if not found.

Return type:
    

Optional[bittensor.core.chain_data.ProposalVoteData]

This function is important for tracking and understanding the decision-making processes within the Bittensor network, particularly how proposals are received and acted upon by the governing body.

async immunity_period(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.immunity_period> "Link to this definition")
    

Retrieves the ‘ImmunityPeriod’ hyperparameter for a specific subnet. This parameter defines the duration during which new neurons are protected from certain network penalties or restrictions.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The blockchain block_hash representation of the block id.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain block hash.



Returns:
    

The value of the ‘ImmunityPeriod’ hyperparameter if the subnet exists, None otherwise.

Return type:
    

Optional[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

The ‘ImmunityPeriod’ is a critical aspect of the network’s governance system, ensuring that new participants have a grace period to establish themselves and contribute to the network without facing immediate punitive actions.

async initialize()[#](<#bittensor.core.async_subtensor.AsyncSubtensor.initialize> "Link to this definition")
    

Establishes connection to the blockchain.

This method establishes the connection to the Bittensor blockchain and should be called after creating an AsyncSubtensor instance before making any queries.

When using the async with context manager, this method is called automatically and does not need to be invoked explicitly.

Returns:
    

The initialized instance (self) for method chaining.

Return type:
    

[AsyncSubtensor](<#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")

Example

subtensor = AsyncSubtensor(network=”finney”)

# Initialize the connection

await subtensor.initialize()

# calls to subtensor

await subtensor.close()

async is_fast_blocks()[#](<#bittensor.core.async_subtensor.AsyncSubtensor.is_fast_blocks> "Link to this definition")
    

Checks if the node is running with fast blocks enabled.

Fast blocks have a block time of 0.25 seconds, compared to the standard 12-second block time. This affects transaction timing and network synchronization.

Returns:
    

True if fast blocks are enabled, False otherwise.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

Notes

  * <<https://docs.learnbittensor.org/resources/glossary#fast-blocks>>




async is_hotkey_delegate(_hotkey_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.is_hotkey_delegate> "Link to this definition")
    

Determines whether a given hotkey (public key) is a delegate on the Bittensor network. This function checks if the neuron associated with the hotkey is part of the network’s delegation system.

Parameters:
    

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the neuron’s hotkey.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the blockchain block number for the query.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

True if the hotkey is a delegate, False otherwise.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

Being a delegate is a significant status within the Bittensor network, indicating a neuron’s involvement in consensus and governance processes.

async is_hotkey_registered(_hotkey_ss58_ , _netuid =None_, _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.is_hotkey_registered> "Link to this definition")
    

Determines whether a given hotkey (public key) is registered in the Bittensor network, either globally across any subnet or specifically on a specified subnet. This function checks the registration status of a neuron identified by its hotkey, which is crucial for validating its participation and activities within the network.

Parameters:
    

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the neuron’s hotkey.

  * **netuid** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The unique identifier of the subnet to check the registration.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number for which the children are to be retrieved.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block to retrieve the subnet unique identifiers from.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

True if the hotkey is registered in the specified context (either any subnet or a specific subnet),
    

False otherwise.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

This function is important for verifying the active status of neurons in the Bittensor network. It aids in understanding whether a neuron is eligible to participate in network processes such as consensus, validation, and incentive distribution based on its registration status.

async is_hotkey_registered_any(_hotkey_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.is_hotkey_registered_any> "Link to this definition")
    

Checks if a neuron’s hotkey is registered on any subnet within the Bittensor network.

Parameters:
    

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the neuron’s hotkey.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The blockchain block_hash representation of block id.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

True if the hotkey is registered on any subnet, False otherwise.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

async is_hotkey_registered_on_subnet(_hotkey_ss58_ , _netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.is_hotkey_registered_on_subnet> "Link to this definition")
    

Checks if the hotkey is registered on a given subnet.

Parameters:
    

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the hotkey to check.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

True if the hotkey is registered on the specified subnet, False otherwise.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

Notes

  * <<https://docs.learnbittensor.org/glossary#hotkey>>




async is_in_admin_freeze_window(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.is_in_admin_freeze_window> "Link to this definition")
    

Returns True if the current block is within the terminal freeze window of the tempo for the given subnet. During this window, admin ops are prohibited to avoid interference with validator weight submissions.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The blockchain block_hash representation of the block id.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain block hash.



Returns:
    

True if in freeze window, else False.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

async is_subnet_active(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.is_subnet_active> "Link to this definition")
    

Verifies if a subnet with the provided netuid is active.

A subnet is considered active if the start_call extrinsic has been executed. A newly registered subnet may exist but not be active until the subnet owner calls start_call to begin emissions.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

True if the subnet is active (emissions have started), False otherwise.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

Notes

  * <<https://docs.learnbittensor.org/subnets/working-with-subnets>>




async kill_pure_proxy(_wallet_ , _pure_proxy_ss58_ , _spawner_ , _proxy_type_ , _index_ , _height_ , _ext_index_ , _force_proxy_type =ProxyType.Any_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.kill_pure_proxy> "Link to this definition")
    

Kills (removes) a pure proxy account.

This method removes a pure proxy account that was previously created via [`create_pure_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.create_pure_proxy> "bittensor.core.async_subtensor.AsyncSubtensor.create_pure_proxy"). The kill_pure call must be executed through the pure proxy account itself, with the spawner acting as an “Any” proxy. This method automatically handles this by executing the call via [`proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.proxy> "bittensor.core.async_subtensor.AsyncSubtensor.proxy").

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object. The wallet.coldkey.ss58_address must be the spawner of the pure proxy (the account that created it via [`create_pure_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.create_pure_proxy> "bittensor.core.async_subtensor.AsyncSubtensor.create_pure_proxy")). The spawner must have an “Any” proxy relationship with the pure proxy.

  * **pure_proxy_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the pure proxy account to be killed. This is the address that was returned in the [`create_pure_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.create_pure_proxy> "bittensor.core.async_subtensor.AsyncSubtensor.create_pure_proxy") response.

  * **spawner** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the spawner account (the account that originally created the pure proxy via [`create_pure_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.create_pure_proxy> "bittensor.core.async_subtensor.AsyncSubtensor.create_pure_proxy")). This should match wallet.coldkey.ss58_address.

  * **proxy_type** (_Union_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,__bittensor.core.chain_data.ProxyType_ _]_) – The type of proxy permissions. Can be a string or ProxyType enum value. Must match the proxy_type used when creating the pure proxy.

  * **index** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The salt value (u16, range 0-65535) originally used in [`create_pure_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.create_pure_proxy> "bittensor.core.async_subtensor.AsyncSubtensor.create_pure_proxy") to generate this pure proxy’s address. This value, combined with proxy_type, delay, and spawner, uniquely identifies the pure proxy to be killed. Must match exactly the index used during creation.

  * **height** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The block number at which the pure proxy was created. This is returned in the “PureCreated” event from [`create_pure_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.create_pure_proxy> "bittensor.core.async_subtensor.AsyncSubtensor.create_pure_proxy") and is required to identify the exact creation transaction.

  * **ext_index** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The extrinsic index within the block at which the pure proxy was created. This is returned in the “PureCreated” event from [`create_pure_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.create_pure_proxy> "bittensor.core.async_subtensor.AsyncSubtensor.create_pure_proxy") and specifies the position of the creation extrinsic within the block. Together with height, this uniquely identifies the creation transaction.

  * **force_proxy_type** (_Optional_ _[__Union_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,__bittensor.core.chain_data.ProxyType_ _]__]_) – The proxy type relationship to use when executing kill_pure through the proxy mechanism. Since pure proxies are keyless and cannot sign transactions, the spawner must act as a proxy for the pure proxy to execute kill_pure. This parameter specifies which proxy type relationship between the spawner and the pure proxy account should be used. The spawner must have a proxy relationship of this type (or Any) with the pure proxy account. Defaults to ProxyType.Any for maximum compatibility. If None, Substrate will automatically select an available proxy type from the spawner’s proxy relationships.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * The kill_pure call must be executed through the pure proxy account itself, with the spawner acting as an Any proxy. This method automatically handles this by executing the call via [`proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.proxy> "bittensor.core.async_subtensor.AsyncSubtensor.proxy"). The spawner must have an Any proxy relationship with the pure proxy for this to work.

  * Bittensor proxies: <<https://docs.learnbittensor.org/keys/proxies/pure-proxies>>




Warning

All access to this account will be lost. Any funds remaining in the pure proxy account will become permanently inaccessible after this operation.

async last_drand_round()[#](<#bittensor.core.async_subtensor.AsyncSubtensor.last_drand_round> "Link to this definition")
    

Retrieves the last drand round emitted in Bittensor.

Drand (distributed randomness) rounds are used to determine when committed weights can be revealed in the commit-reveal mechanism. This method returns the most recent drand round number, which corresponds to the timing for weight reveals.

Returns:
    

The latest drand round number emitted in Bittensor, or None if no round has been stored.

Return type:
    

Optional[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

Notes

  * <<https://docs.learnbittensor.org/resources/glossary#drandtime-lock-encryption>>




log_verbose = False[#](<#bittensor.core.async_subtensor.AsyncSubtensor.log_verbose> "Link to this definition")
    

async max_weight_limit(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.max_weight_limit> "Link to this definition")
    

Returns the MaxWeightsLimit hyperparameter for a subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnetwork.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block at which to query. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

The stored maximum weight limit as a normalized float in [0, 1], or None if the subnetwork
    

does not exist. Note: this value is not enforced - the weight validation code uses a hardcoded u16::MAX
    

instead.

Return type:
    

Optional[[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")]

Notes

  * This hyperparameter is now a constant rather than a settable variable.

  * <<https://docs.learnbittensor.org/subnets/subnet-hyperparameters>>




async metagraph(_netuid_ , _mechid =0_, _lite =True_, _block =None_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.metagraph> "Link to this definition")
    

Returns a synced metagraph for a specified subnet within the Bittensor network. The metagraph represents the network’s structure, including neuron connections and interactions.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network UID of the subnet to query.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Subnet mechanism identifier.

  * **lite** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, returns a metagraph using a lightweight sync (no weights, no bonds).

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Block number for synchronization, or None for the latest block.



Returns:
    

The metagraph representing the subnet’s structure and neuron relationships.

Return type:
    

[bittensor.core.metagraph.AsyncMetagraph](<../metagraph/index.html#bittensor.core.metagraph.AsyncMetagraph> "bittensor.core.metagraph.AsyncMetagraph")

The metagraph is an essential tool for understanding the topology and dynamics of the Bittensor network’s decentralized architecture, particularly in relation to neuron interconnectivity and consensus processes.

async mev_submit_encrypted(_wallet_ , _call_ , _sign_with ='coldkey'_, _*_ , _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_, _blocks_for_revealed_execution =3_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.mev_submit_encrypted> "Link to this definition")
    

Submits an encrypted extrinsic to the MEV Shield pallet.

This function encrypts a call using ML-KEM-768 + XChaCha20Poly1305 and submits it to the MevShield pallet. The extrinsic remains encrypted in the transaction pool until it is included in a block and decrypted by validators.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet used to sign the extrinsic (must be unlocked, coldkey will be used for signing).

  * **call** (_scalecodec.GenericCall_) – The GenericCall object to encrypt and submit.

  * **sign_with** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The keypair to use for signing the inner call/extrinsic. Can be either “coldkey” or “hotkey”.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the executed event, indicating that validators have successfully decrypted and executed the inner call. If True, the function will poll subsequent blocks for the event matching this submission’s commitment.

  * **blocks_for_revealed_execution** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Maximum number of blocks to poll for the executed event after inclusion. The function checks blocks from start_block to start_block + blocks_for_revealed_execution. Returns immediately if the event is found before the block limit is reached.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Raises:
    

  * [**ValueError**](<https://docs.python.org/3/library/exceptions.html#ValueError> "\(in Python v3.14\)") – If NextKey is not available in storage or encryption fails.

  * **SubstrateRequestException** – If the extrinsic fails to be submitted or included.




Note

The encryption uses the public key from NextKey storage, which rotates every block. The payload structure is: payload_core = signer_bytes (32B) + nonce (u32 LE, 4B) + SCALE(call) plaintext = payload_core + b”x01” + signature (64B for sr25519) commitment = blake2_256(payload_core)

Notes

For detailed documentation and examples of MEV Shield protection, see: <<https://docs.learnbittensor.org/sdk/mev-protection>>

For creating GenericCall objects to use with this method, see: <<https://docs.learnbittensor.org/sdk/call>>

async min_allowed_weights(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.min_allowed_weights> "Link to this definition")
    

Returns the MinAllowedWeights hyperparameter for a subnet.

This hyperparameter sets the minimum length of the weights vector that a validator must submit. It checks weights.len() >= MinAllowedWeights. For example, a validator could submit [1000, 0, 0, 0] to satisfy MinAllowedWeights=4, but this would fail if MinAllowedWeights were set to 5. This ensures validators distribute attention across the subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnetwork.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block at which to query. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

The minimum number of required weight connections, or None if the subnetwork does not
    

exist or the parameter is not found.

Return type:
    

Optional[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

Notes

  * <<https://docs.learnbittensor.org/subnets/subnet-hyperparameters>>




async modify_liquidity(_wallet_ , _netuid_ , _position_id_ , _liquidity_delta_ , _hotkey_ss58 =None_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.modify_liquidity> "Link to this definition")
    

Modifies liquidity in liquidity position by adding or removing liquidity from it.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet used to sign the extrinsic (must be unlocked).

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The UID of the target subnet for which the call is being initiated.

  * **position_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The id of the position record in the pool.

  * **liquidity_delta** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – The amount of liquidity to be added or removed (add if positive or remove if negative).

  * **hotkey_ss58** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hotkey with staked TAO in Alpha. If not passed then the wallet hotkey is used.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Example

import bittensor as bt subtensor = bt.AsyncSubtensor(network=”local”) await subtensor.initialize() my_wallet = bt.Wallet()

# if liquidity_delta is negative my_liquidity_delta = Balance.from_tao(100) * -1 await subtensor.modify_liquidity(

> wallet=my_wallet, netuid=123, position_id=2, liquidity_delta=my_liquidity_delta

)

# if liquidity_delta is positive my_liquidity_delta = Balance.from_tao(120) await subtensor.modify_liquidity(

> wallet=my_wallet, netuid=123, position_id=2, liquidity_delta=my_liquidity_delta

)

Note

Modifying is allowed even when user liquidity is enabled in specified subnet. Call toggle_user_liquidity to enable/disable user liquidity.

async move_stake(_wallet_ , _origin_netuid_ , _origin_hotkey_ss58_ , _destination_netuid_ , _destination_hotkey_ss58_ , _amount =None_, _move_all_stake =False_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.move_stake> "Link to this definition")
    

Moves stake to a different hotkey and/or subnet.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet to move stake from.

  * **origin_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid of the source subnet.

  * **origin_hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the source hotkey.

  * **destination_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid of the destination subnet.

  * **destination_hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the destination hotkey.

  * **amount** (_Optional_ _[_[_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") _]_) – Amount of stake to move.

  * **move_all_stake** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, moves all stake from the source hotkey to the destination hotkey.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – I`f` True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be finalized on the blockchain.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Price Protection: <<https://docs.learnbittensor.org/learn/price-protection>>

  * Rate Limits: <<https://docs.learnbittensor.org/learn/chain-rate-limits#staking-operations-rate-limits>>




async neuron_for_uid(_uid_ , _netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.neuron_for_uid> "Link to this definition")
    

Retrieves detailed information about a specific neuron identified by its unique identifier (UID) within a specified subnet (netuid) of the Bittensor network. This function provides a comprehensive view of a neuron’s attributes, including its stake, rank, and operational status.

Parameters:
    

  * **uid** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The unique identifier of the neuron.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the blockchain block number for the query.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain block hash.



Returns:
    

Detailed information about the neuron if found, a null neuron otherwise

Return type:
    

bittensor.core.chain_data.NeuronInfo

This function is crucial for analyzing individual neurons’ contributions and status within a specific subnet, offering insights into their roles in the network’s consensus and validation mechanisms.

async neurons(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.neurons> "Link to this definition")
    

Retrieves a list of all neurons within a specified subnet of the Bittensor network. This function provides a snapshot of the subnet’s neuron population, including each neuron’s attributes and network interactions.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the blockchain block number for the query.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain block hash.



Returns:
    

A list of NeuronInfo objects detailing each neuron’s characteristics in the subnet.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[bittensor.core.chain_data.NeuronInfo]

Understanding the distribution and status of neurons within a subnet is key to comprehending the network’s decentralized structure and the dynamics of its consensus and governance processes.

async neurons_lite(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.neurons_lite> "Link to this definition")
    

Retrieves a list of neurons in a ‘lite’ format from a specific subnet of the Bittensor network. This function provides a streamlined view of the neurons, focusing on key attributes such as stake and network participation.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the blockchain block number for the query.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain block hash.



Returns:
    

A list of simplified neuron information for the subnet.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[bittensor.core.chain_data.NeuronInfoLite]

This function offers a quick overview of the neuron population within a subnet, facilitating efficient analysis of the network’s decentralized structure and neuron dynamics.

async poke_deposit(_wallet_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.poke_deposit> "Link to this definition")
    

Adjusts deposits made for proxies and announcements based on current values.

This method recalculates and updates the locked deposit amounts for both proxy relationships and announcements for the signing account. It can be used to potentially lower the locked amount if the deposit requirements have changed (e.g., due to runtime upgrades or changes in the number of proxies/announcements).

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (the account whose deposits will be adjusted).

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Note

This method automatically adjusts deposits for both proxy relationships and announcements. No parameters are needed as it operates on the account’s current state.

When to use:
    

  * After runtime upgrade, if deposit constants have changed.

  * After removing proxies/announcements, to free up excess locked funds.

  * Periodically to optimize locked deposit amounts.




async proxy(_wallet_ , _real_account_ss58_ , _force_proxy_type_ , _call_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.proxy> "Link to this definition")
    

Executes a call on behalf of the real account through a proxy.

This method allows a proxy account (delegate) to execute a call on behalf of the real account (delegator). The call is subject to the permissions defined by the proxy type and must respect the delay period if one was set when the proxy was added.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (should be the proxy account wallet).

  * **real_account_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the real account on whose behalf the call is being made.

  * **force_proxy_type** (_Optional_ _[__Union_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,__bittensor.core.chain_data.ProxyType_ _]__]_) – The type of proxy to use for the call. If None, any proxy type can be used. Otherwise, must match one of the allowed proxy types. Can be a string or ProxyType enum value.

  * **call** (_scalecodec.GenericCall_) – The inner call to be executed on behalf of the real account.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * The call must be permitted by the proxy type. For example, a “NonTransfer” proxy cannot execute transfer calls. The delay period must also have passed since the proxy was added.




async proxy_announced(_wallet_ , _delegate_ss58_ , _real_account_ss58_ , _force_proxy_type_ , _call_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.proxy_announced> "Link to this definition")
    

Executes an announced call on behalf of the real account through a proxy.

This method executes a call that was previously announced via [`announce_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.announce_proxy> "bittensor.core.async_subtensor.AsyncSubtensor.announce_proxy"). The call must match the call_hash that was announced, and the delay period must have passed since the announcement was made. The real account has the opportunity to review and reject the announcement before execution.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (should be the proxy account wallet that made the announcement).

  * **delegate_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the delegate proxy account that made the announcement.

  * **real_account_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the real account on whose behalf the call will be made.

  * **force_proxy_type** (_Optional_ _[__Union_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,__bittensor.core.chain_data.ProxyType_ _]__]_) – The type of proxy to use for the call. If None, any proxy type can be used. Otherwise, must match one of the allowed proxy types. Can be a string or ProxyType enum value.

  * **call** (_scalecodec.GenericCall_) – The inner call to be executed on behalf of the real account (must match the announced call_hash).

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * The call_hash of the provided call must match the call_hash that was announced. The announcement must not have been rejected by the real account, and the delay period must have passed.




async query_constant(_module_name_ , _constant_name_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.query_constant> "Link to this definition")
    

Retrieves a constant from the specified module on the Bittensor blockchain.

Use this function for nonstandard queries to constants defined within the Bittensor blockchain, if these cannot be accessed through other, standard getter methods.

Parameters:
    

  * **module_name** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The name of the module containing the constant (e.g., Balances, SubtensorModule).

  * **constant_name** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The name of the constant to retrieve (e.g., ExistentialDeposit).

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

A SCALE-decoded object if found, None otherwise. Access the actual value using .value attribute. Common types include int (for counts/blocks), Balance objects (for amounts in Rao), and booleans.

Return type:
    

Optional[scalecodec.base.ScaleType[scalecodec.ScaleValue]]

async query_identity(_coldkey_ss58_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.query_identity> "Link to this definition")
    

Queries the identity of a neuron on the Bittensor blockchain using the given key. This function retrieves detailed identity information about a specific neuron, which is a crucial aspect of the network’s decentralized identity and governance system.

Parameters:
    

  * **coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – Coldkey used to query the neuron’s identity (technically the neuron’s coldkey SS58 address).

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the blockchain block number at which to perform the query.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain block hash.



Returns:
    

An object containing the identity information of the neuron if found, None otherwise.

Return type:
    

Optional[[bittensor.core.chain_data.chain_identity.ChainIdentity](<../chain_data/chain_identity/index.html#bittensor.core.chain_data.chain_identity.ChainIdentity> "bittensor.core.chain_data.chain_identity.ChainIdentity")]

The identity information can include various attributes such as the neuron’s stake, rank, and other network-specific details, providing insights into the neuron’s role and status within the Bittensor network.

Note

See the [Bittensor CLI documentation](<https://docs.bittensor.com/reference/btcli>) for supported identity parameters.

async query_map(_module_ , _name_ , _params =None_, _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.query_map> "Link to this definition")
    

Queries map storage from any module on the Bittensor blockchain.

Use this function for nonstandard queries to map storage defined within the Bittensor blockchain, if these cannot be accessed through other, standard getter methods.

Parameters:
    

  * **module** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The name of the module from which to query the map storage (e.g., “SubtensorModule”, “System”).

  * **name** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The specific storage function within the module to query (e.g., “Bonds”, “Weights”).

  * **params** (_Optional_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _]_) – Parameters to be passed to the query.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

A data structure representing the map storage if found, None otherwise.

Return type:
    

AsyncQueryMapResult

async query_map_subtensor(_name_ , _params =None_, _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.query_map_subtensor> "Link to this definition")
    

Queries map storage from the Subtensor module on the Bittensor blockchain.

Use this function for nonstandard queries to map storage defined within the Bittensor blockchain, if these cannot be accessed through other, standard getter methods.

Parameters:
    

  * **name** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The name of the map storage function to query.

  * **params** (_Optional_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _]_) – A list of parameters to pass to the query function.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

An object containing the map-like data structure, or None if not found.

Return type:
    

async_substrate_interface.AsyncQueryMapResult

async query_module(_module_ , _name_ , _params =None_, _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.query_module> "Link to this definition")
    

Queries any module storage on the Bittensor blockchain with the specified parameters and block number. This function is a generic query interface that allows for flexible and diverse data retrieval from various blockchain modules. Use this function for nonstandard queries to storage defined within the Bittensor blockchain, if these cannot be accessed through other, standard getter methods.

Parameters:
    

  * **module** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The name of the module from which to query data.

  * **name** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The name of the storage function within the module.

  * **params** (_Optional_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _]_) – A list of parameters to pass to the query function.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

An object containing the requested data if found, None otherwise.

Return type:
    

scalecodec.base.ScaleType[scalecodec.ScaleValue]

async query_runtime_api(_runtime_api_ , _method_ , _params_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.query_runtime_api> "Link to this definition")
    

Queries the runtime API of the Bittensor blockchain, providing a way to interact with the underlying runtime and retrieve data encoded in Scale Bytes format. Use this function for nonstandard queries to the runtime

> environment, if these cannot be accessed through other, standard getter methods.

Parameters:
    

  * **runtime_api** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The name of the runtime API to query.

  * **method** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The specific method within the runtime API to call.

  * **params** (_Optional_ _[__Union_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_Any_](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any") _]__,_[_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_Any_](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any") _]__]__]_) – The parameters to pass to the method call.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

The decoded result from the runtime API call, or None if the call fails.

Return type:
    

[Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any")

async query_subtensor(_name_ , _params =None_, _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.query_subtensor> "Link to this definition")
    

Queries named storage from the Subtensor module on the Bittensor blockchain.

Use this function for nonstandard queries to storage defined within the Bittensor blockchain, if these cannot be accessed through other, standard getter methods.

Parameters:
    

  * **name** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The name of the storage function to query.

  * **params** (_Optional_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _]_) – A list of parameters to pass to the query function.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

An object containing the requested data.

Return type:
    

query_response

async recycle(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.recycle> "Link to this definition")
    

Retrieves the ‘Burn’ hyperparameter for a specified subnet.

The ‘Burn’ parameter represents the amount of TAO that is recycled when registering a neuron on this subnet. Recycled tokens are removed from circulation but can be re-emitted, unlike burned tokens which are permanently removed.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block at which to query. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

The amount of TAO recycled per neuron registration, or None if the subnet does not exist.

Return type:
    

Optional[[bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")]

Notes

  * <<https://docs.learnbittensor.org/resources/glossary#recycling-and-burning>>




async refund_crowdloan(_wallet_ , _crowdloan_id_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.refund_crowdloan> "Link to this definition")
    

Refunds contributors from a failed crowdloan campaign that did not reach its cap.

Refunds are batched, processing up to RefundContributorsLimit (default 50) contributors per call. For campaigns with more contributors, multiple calls are required. Only non-creator contributors are refunded; the creator’s deposit remains until dissolution via dissolve_crowdloan.

Only the crowdloan creator can call this method for a non-finalized crowdloan.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet instance used to sign the transaction (must be the crowdloan creator).

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to refund.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after submission.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, raises an exception rather than returning failure in the response.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

ExtrinsicResponse indicating success or failure, with error details if applicable.

Return type:
    

[bittensor.core.types.ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Crowdloans Overview: <<https://docs.learnbittensor.org/subnets/crowdloans>>

  * Crowdloan Lifecycle: <<https://docs.learnbittensor.org/subnets/crowdloans#crowdloan-lifecycle>>

  * Refund and Dissolve: <<https://docs.learnbittensor.org/subnets/crowdloans/crowdloans-tutorial#alternative-path-refund-and-dissolve>>




async register(_wallet_ , _netuid_ , _limit_price =None_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.register> "Link to this definition")
    

Registers a neuron on the Bittensor network by recycling TAO, with automatic price protection.

Uses `register_limit` under the hood. If `limit_price` is not provided, it is automatically calculated as the current recycle (burn) cost plus a 0.5% tolerance to protect against price fluctuations.

For root subnet (`netuid == 0`), delegates to `root_register_extrinsic`.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet associated with the neuron to be registered.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **limit_price** (_Optional_ _[_[_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") _]_) – Maximum acceptable burn price as a Balance instance. If `None`, automatically calculated as `recycle * 1.005` (0.5% tolerance). If the on-chain burn price exceeds this value, the transaction will fail with RegistrationPriceLimitExceeded.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If `True`, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If `False`, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning `False` if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be finalized on the blockchain.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Rate Limits: <<https://docs.learnbittensor.org/learn/chain-rate-limits#registration-rate-limits>>




async register_limit(_wallet_ , _netuid_ , _limit_price_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.register_limit> "Link to this definition")
    

Registers a neuron on the Bittensor network by recycling TAO, with a maximum burn price limit.

Unlike `burned_register`, this method includes a `limit_price` parameter that ensures the registration will only proceed if the current on-chain burn price does not exceed the specified maximum. This protects against unexpected price spikes between reading the price and submitting the transaction.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet associated with the neuron to be registered.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **limit_price** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – Maximum acceptable burn price as a Balance instance. If the on-chain burn price exceeds this value, the transaction will fail with RegistrationPriceLimitExceeded.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If `True`, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If `False`, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning `False` if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be finalized on the blockchain.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Rate Limits: <<https://docs.learnbittensor.org/learn/chain-rate-limits#registration-rate-limits>>




async register_subnet(_wallet_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.register_subnet> "Link to this definition")
    

Registers a new subnetwork on the Bittensor network.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet to be used for subnet registration.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Rate Limits: <<https://docs.learnbittensor.org/learn/chain-rate-limits#network-registration-rate-limit>>




async reject_proxy_announcement(_wallet_ , _delegate_ss58_ , _call_hash_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.reject_proxy_announcement> "Link to this definition")
    

Rejects an announcement made by a proxy delegate.

This method allows the real account to reject an announcement made by a proxy delegate, preventing the announced call from being executed. Once rejected, the announcement cannot be executed and the announcement deposit is returned to the delegate.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (should be the real account wallet).

  * **delegate_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the delegate proxy account whose announcement is being rejected.

  * **call_hash** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hash of the call that was announced and is now being rejected.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Once rejected, the announcement cannot be executed. The delegate’s announcement deposit is returned.




async remove_liquidity(_wallet_ , _netuid_ , _position_id_ , _hotkey_ss58 =None_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.remove_liquidity> "Link to this definition")
    

Remove liquidity and credit balances back to wallet’s hotkey stake.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet used to sign the extrinsic (must be unlocked).

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The UID of the target subnet for which the call is being initiated.

  * **position_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The id of the position record in the pool.

  * **hotkey_ss58** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hotkey with staked TAO in Alpha. If not passed then the wallet hotkey is used.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Note

  * Adding is allowed even when user liquidity is enabled in specified subnet. Call toggle_user_liquidity extrinsic to enable/disable user liquidity.

  * To get the position_id use get_liquidity_list method.




async remove_proxies(_wallet_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.remove_proxies> "Link to this definition")
    

Removes all proxy relationships for the account in a single transaction.

This method removes all proxy relationships for the signing account in a single call, which is more efficient than removing them one by one using [`remove_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.remove_proxy> "bittensor.core.async_subtensor.AsyncSubtensor.remove_proxy"). The deposit for all proxies will be returned to the account.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object. The account whose proxies will be removed (the delegator). All proxy relationships where wallet.coldkey.ss58_address is the real account will be removed.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts` and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * This removes all proxy relationships for the account, regardless of proxy type or delegate. Use [`remove_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.remove_proxy> "bittensor.core.async_subtensor.AsyncSubtensor.remove_proxy") if you need to remove specific proxy relationships selectively.




async remove_proxy(_wallet_ , _delegate_ss58_ , _proxy_type_ , _delay_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.remove_proxy> "Link to this definition")
    

Removes a specific proxy relationship.

This method removes a single proxy relationship between the real account and a delegate. The parameters must exactly match those used when the proxy was added via [`add_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.add_proxy> "bittensor.core.async_subtensor.AsyncSubtensor.add_proxy"). The deposit for this proxy will be returned to the account.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object.

  * **delegate_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the delegate proxy account to remove.

  * **proxy_type** (_Union_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,__bittensor.core.chain_data.ProxyType_ _]_) – The type of proxy permissions to remove. Can be a string or ProxyType enum value.

  * **delay** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The announcement delay value (in blocks) for the proxy being removed. Must exactly match the delay value that was set when the proxy was originally added via [`add_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.add_proxy> "bittensor.core.async_subtensor.AsyncSubtensor.add_proxy"). This is a required identifier for the specific proxy relationship, not a delay before removal takes effect (removal is immediate).

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * The delegate_ss58, proxy_type, and delay parameters must exactly match those used when the proxy was added. Use [`get_proxies_for_real_account()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_proxies_for_real_account> "bittensor.core.async_subtensor.AsyncSubtensor.get_proxies_for_real_account") to retrieve the exact parameters for existing proxies.




async remove_proxy_announcement(_wallet_ , _real_account_ss58_ , _call_hash_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.remove_proxy_announcement> "Link to this definition")
    

Removes an announcement made by a proxy account.

This method allows the proxy account to remove its own announcement before it is executed or rejected. This frees up the announcement deposit and prevents the call from being executed. Only the proxy account that made the announcement can remove it.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (should be the proxy account wallet that made the announcement).

  * **real_account_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the real account on whose behalf the call was announced.

  * **call_hash** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hash of the call that was announced and is now being removed.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Only the proxy account that made the announcement can remove it. The real account can reject it via [`reject_proxy_announcement()`](<#bittensor.core.async_subtensor.AsyncSubtensor.reject_proxy_announcement> "bittensor.core.async_subtensor.AsyncSubtensor.reject_proxy_announcement"), but cannot remove it directly.




async reveal_weights(_wallet_ , _netuid_ , _uids_ , _weights_ , _salt_ , _mechid =0_, _max_attempts =5_, _version_key =version_as_int_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =16_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.reveal_weights> "Link to this definition")
    

Reveals the weights for a specific subnet on the Bittensor blockchain using the provided wallet. This action serves as a revelation of the neuron’s previously committed weight distribution.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **uids** ([_bittensor.core.types.UIDs_](<../types/index.html#bittensor.core.types.UIDs> "bittensor.core.types.UIDs")) – NumPy array of neuron UIDs for which weights are being revealed.

  * **weights** ([_bittensor.core.types.Weights_](<../types/index.html#bittensor.core.types.Weights> "bittensor.core.types.Weights")) – NumPy array of weight values corresponding to each UID.

  * **salt** ([_bittensor.core.types.Salt_](<../types/index.html#bittensor.core.types.Salt> "bittensor.core.types.Salt")) – NumPy array of salt values corresponding to the hash function.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet mechanism unique identifier.

  * **max_attempts** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The number of maximum attempts to reveal weights.

  * **version_key** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Version key for compatibility with the network.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be finalized on the blockchain.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

This function allows neurons to reveal their previously committed weight distribution, ensuring transparency and accountability within the Bittensor network.

Notes

  * <<https://docs.learnbittensor.org/glossary#commit-reveal>>

  * Rate Limits: <<https://docs.learnbittensor.org/learn/chain-rate-limits#weights-setting-rate-limit>>




async root_register(_wallet_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.root_register> "Link to this definition")
    

Register neuron by recycling some TAO.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet associated with the neuron to be registered.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be finalized on the blockchain.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Rate Limits: <<https://docs.learnbittensor.org/learn/chain-rate-limits#registration-rate-limits>>




async root_set_pending_childkey_cooldown(_wallet_ , _cooldown_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.root_set_pending_childkey_cooldown> "Link to this definition")
    

Sets the pending childkey cooldown.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – bittensor wallet instance.

  * **cooldown** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – the number of blocks to setting pending childkey cooldown.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be finalized on the blockchain.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Note

This operation can only be successfully performed if your wallet has root privileges.

async serve_axon(_netuid_ , _axon_ , _certificate =None_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.serve_axon> "Link to this definition")
    

Registers an Axon endpoint on the network for receiving queries from other neurons.

This method publishes your neuron’s IP address, port, and protocol information to the blockchain, making it discoverable by other neurons in the subnet. Optionally, you can include a TLS certificate to enable secure, encrypted communication via mutual TLS (mTLS).

When a certificate is provided, the blockchain stores both your endpoint information and your TLS public key, allowing other neurons to discover your certificate and establish encrypted connections. When re-serving with updated metadata (including a new certificate), the previous values are overwritten.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnetwork.

  * **axon** ([_bittensor.core.axon.Axon_](<../axon/index.html#bittensor.core.axon.Axon> "bittensor.core.axon.Axon")) – The Axon instance containing your endpoint configuration (IP, port, protocol).

  * **certificate** (_Optional_ _[_[_bittensor.utils.Certificate_](<../../utils/index.html#bittensor.utils.Certificate> "bittensor.utils.Certificate") _]_) – Optional TLS certificate for secure communication. Should contain a public key (up to 64 bytes) and algorithm identifier. If None, standard unencrypted serving is used.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after submission. If not included in a block within this period, the transaction expires.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, raises an exception on failure instead of returning an error response.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, waits for the transaction to be included in a block before returning.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, waits for the transaction to be finalized on the blockchain.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

ExtrinsicResponse containing the success status and transaction details. On success, the response includes the external IP and port that were registered.

Return type:
    

[bittensor.core.types.ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Rate Limits: <<https://docs.learnbittensor.org/learn/chain-rate-limits#serving-rate-limits>>




async set_auto_stake(_wallet_ , _netuid_ , _hotkey_ss58_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.set_auto_stake> "Link to this definition")
    

Sets the coldkey to automatically stake to the hotkey within specific subnet mechanism.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet unique identifier.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the validator’s hotkey to which the miner automatically stakes all rewards received from the specified subnet immediately upon receipt.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If T`rue`, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Note

Use the get_auto_stakes method to get the hotkey address of the validator where auto stake is set.

async set_children(_wallet_ , _hotkey_ss58_ , _netuid_ , _children_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.set_children> "Link to this definition")
    

Allows a coldkey to set children-keys.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – bittensor wallet instance.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the neuron’s hotkey.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid value.

  * **children** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_tuple_](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)") _[_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _,_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]__]_) – A list of children with their proportions.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be finalized on the blockchain.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Raises:
    

  * [**DuplicateChild**](<../errors/index.html#bittensor.core.errors.DuplicateChild> "bittensor.core.errors.DuplicateChild") – There are duplicates in the list of children.

  * [**InvalidChild**](<../errors/index.html#bittensor.core.errors.InvalidChild> "bittensor.core.errors.InvalidChild") – Child is the hotkey.

  * [**NonAssociatedColdKey**](<../errors/index.html#bittensor.core.errors.NonAssociatedColdKey> "bittensor.core.errors.NonAssociatedColdKey") – The coldkey does not own the hotkey or the child is the same as the hotkey.

  * [**NotEnoughStakeToSetChildkeys**](<../errors/index.html#bittensor.core.errors.NotEnoughStakeToSetChildkeys> "bittensor.core.errors.NotEnoughStakeToSetChildkeys") – Parent key doesn’t have minimum own stake.

  * [**ProportionOverflow**](<../errors/index.html#bittensor.core.errors.ProportionOverflow> "bittensor.core.errors.ProportionOverflow") – The sum of the proportions does exceed uint64.

  * [**RegistrationNotPermittedOnRootSubnet**](<../errors/index.html#bittensor.core.errors.RegistrationNotPermittedOnRootSubnet> "bittensor.core.errors.RegistrationNotPermittedOnRootSubnet") – Attempting to register a child on the root network.

  * [**SubnetNotExists**](<../errors/index.html#bittensor.core.errors.SubnetNotExists> "bittensor.core.errors.SubnetNotExists") – Attempting to register to a non-existent network.

  * [**TooManyChildren**](<../errors/index.html#bittensor.core.errors.TooManyChildren> "bittensor.core.errors.TooManyChildren") – Too many children in request.

  * [**TxRateLimitExceeded**](<../errors/index.html#bittensor.core.errors.TxRateLimitExceeded> "bittensor.core.errors.TxRateLimitExceeded") – Hotkey hit the rate limit.

  * **bittensor_wallet.errors.KeyFileError** – Failed to decode keyfile data.

  * **bittensor_wallet.errors.PasswordError** – Decryption failed or wrong password for decryption provided.




Notes

  * Rate Limits: <<https://docs.learnbittensor.org/learn/chain-rate-limits#child-hotkey-operations-rate-limit>>




async set_commitment(_wallet_ , _netuid_ , _data_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.set_commitment> "Link to this definition")
    

Commits arbitrary data to the Bittensor network by publishing metadata. # TODO: check with @roman, is this about ‘arbitrary data’ or ‘commit-reveal’? we need a real example here if this is important.

> This method allows neurons to publish arbitrary data to the blockchain, which can be used for various purposes such as sharing model updates, configuration data, or other network-relevant information. The data is encoded and stored on-chain as metadata.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet associated with the neuron committing the data.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnetwork.

  * **data** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The data string to be committed to the network. The data will be encoded as bytes before submission.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

The data is automatically encoded as bytes before submission. There may be size limits on metadata payloads enforced by the chain.

  * <<https://docs.learnbittensor.org/resources/glossary#commit-reveal>>

  * <<https://docs.learnbittensor.org/concepts/commit-reveal>>




async set_delegate_take(_wallet_ , _hotkey_ss58_ , _take_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.set_delegate_take> "Link to this definition")
    

Sets the delegate ‘take’ percentage for a neuron identified by its hotkey. The ‘take’ represents the percentage of rewards that the delegate claims from its nominators’ stakes.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – bittensor wallet instance.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the neuron’s hotkey.

  * **take** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")) – Percentage reward for the delegate.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be finalized on the blockchain.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Raises:
    

  * [**DelegateTakeTooHigh**](<../errors/index.html#bittensor.core.errors.DelegateTakeTooHigh> "bittensor.core.errors.DelegateTakeTooHigh") – Delegate take is too high.

  * [**DelegateTakeTooLow**](<../errors/index.html#bittensor.core.errors.DelegateTakeTooLow> "bittensor.core.errors.DelegateTakeTooLow") – Delegate take is too low.

  * [**DelegateTxRateLimitExceeded**](<../errors/index.html#bittensor.core.errors.DelegateTxRateLimitExceeded> "bittensor.core.errors.DelegateTxRateLimitExceeded") – A transactor exceeded the rate limit for delegate transaction.

  * [**HotKeyAccountNotExists**](<../errors/index.html#bittensor.core.errors.HotKeyAccountNotExists> "bittensor.core.errors.HotKeyAccountNotExists") – The hotkey does not exist.

  * [**NonAssociatedColdKey**](<../errors/index.html#bittensor.core.errors.NonAssociatedColdKey> "bittensor.core.errors.NonAssociatedColdKey") – Request to stake, unstake, or subscribe is made by a coldkey that is not associated with the hotkey account.

  * **bittensor_wallet.errors.PasswordError** – Decryption failed or wrong password for decryption provided.

  * **bittensor_wallet.errors.KeyFileError** – Failed to decode keyfile data.




The delegate take is a critical parameter in the network’s incentive structure, influencing the distribution of rewards among neurons and their nominators.

Notes

  * Rate Limits: <<https://docs.learnbittensor.org/learn/chain-rate-limits#delegate-take-rate-limit>>




async set_reveal_commitment(_wallet_ , _netuid_ , _data_ , _blocks_until_reveal =360_, _block_time =12_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.set_reveal_commitment> "Link to this definition")
    

Commits arbitrary data to the Bittensor network using timelock encryption for reveal scheduling.

This method commits data that will be automatically revealed after a specified number of blocks using drand timelock encryption. The data is encrypted using get_encrypted_commitment, which uses drand rounds to ensure the data cannot be revealed before the specified reveal time.

# TODO: check with @roman, is this about ‘arbitrary data’ or ‘commit-reveal’? we need a real example here if this is important, and documentating a real commit reveal flow.

Parameters:
    

  * **wallet** – The wallet associated with the neuron committing the data.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnetwork.

  * **data** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The data to be committed to the network.

  * **blocks_until_reveal** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The number of blocks from now after which the data will be revealed. Then number of blocks in one epoch.

  * **block_time** (_Union_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _,_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _]_) – The number of seconds between each block (default 12.0 for standard blocks, 10.0 for fast blocks).

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution. The response’s “data” field contains {“encrypted”: encrypted, “reveal_round”: reveal_round} on success.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

A commitment can be set once per subnet epoch and is reset at the next epoch automatically. The timelock encryption ensures the data cannot be revealed before the specified drand round.

  * <<https://docs.learnbittensor.org/resources/glossary#commit-reveal>>

  * <<https://docs.learnbittensor.org/resources/glossary#drandtime-lock-encryption>>

  * <<https://docs.learnbittensor.org/concepts/commit-reveal>>




async set_root_claim_type(_wallet_ , _new_root_claim_type_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.set_root_claim_type> "Link to this definition")
    

Submit an extrinsic to set the root claim type for the wallet’s coldkey.

The root claim type determines how future Alpha dividends from subnets are handled when they are claimed for the wallet’s coldkey:

  * Swap: Alpha dividends are swapped to TAO at claim time and restaked on the Root Subnet (default).

  * Keep: Alpha dividends remain as Alpha on the originating subnets.




Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance.

  * **new_root_claim_type** (_Literal_ _[__'Swap'__,__'Keep'__]__|__RootClaimType_ _|__dict_) – The new root claim type to set. Can be: \- String: “Swap” or “Keep” \- RootClaimType: RootClaimType.Swap, RootClaimType.Keep \- Dict: {“KeepSubnets”: {“subnets”: [1, 2, 3]}} \- Callable: RootClaimType.KeepSubnets([1, 2, 3])

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Number of blocks for which the transaction remains valid after submission. If the extrinsic is not included in a block within this window, it will expire and be rejected.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to raise a Python exception instead of returning a failed ExtrinsicResponse.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait until the extrinsic is included in a block before returning.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic in a block before returning.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

ExtrinsicResponse describing the result of the extrinsic execution.

Notes

  * This setting applies to both automatic and manual root claims going forward; it does not retroactively change how already-claimed dividends were processed.

  * Only the treatment of Alpha dividends is affected; the underlying TAO stake on the Root Subnet is unchanged.

  * See: <<https://docs.learnbittensor.org/staking-and-delegation/root-claims>>

  * See also: <<https://docs.learnbittensor.org/staking-and-delegation/root-claims/managing-root-claims>>




async set_subnet_identity(_wallet_ , _netuid_ , _subnet_identity_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.set_subnet_identity> "Link to this definition")
    

Sets the identity of a subnet for a specific wallet and network.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet instance that will authorize the transaction.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique ID of the network on which the operation takes place.

  * **subnet_identity** (_bittensor.core.chain_data.SubnetIdentity_) – The identity data of the subnet including attributes like name, GitHub repository, contact, URL, discord, description, and any additional metadata.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be finalized on the blockchain.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

async set_weights(_wallet_ , _netuid_ , _uids_ , _weights_ , _mechid =0_, _block_time =12.0_, _commit_reveal_version =4_, _max_attempts =5_, _version_key =version_as_int_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.set_weights> "Link to this definition")
    

Sets the weight vector for a neuron acting as a validator, specifying the weights assigned to subnet miners based on their performance evaluation.

This method allows subnet validators to submit their weight vectors, which rank the value of each subnet miner’s work. These weight vectors are used by the Yuma Consensus algorithm to compute emissions for both validators and miners.

The method automatically handles both commit-reveal-enabled subnets (CRv4) and direct weight setting. For commit-reveal subnets, weights are committed first and then revealed after the reveal period. The method respects rate limiting constraints enforced by _blocks_weight_limit.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet associated with the subnet validator setting the weights.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **uids** ([_bittensor.core.types.UIDs_](<../types/index.html#bittensor.core.types.UIDs> "bittensor.core.types.UIDs")) – The list of subnet miner neuron UIDs that the weights are being set for.

  * **weights** ([_bittensor.core.types.Weights_](<../types/index.html#bittensor.core.types.Weights> "bittensor.core.types.Weights")) – The corresponding weights to be set for each UID, representing the validator’s evaluation of each miner’s performance.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet mechanism unique identifier (default 0 for primary mechanism).

  * **block_time** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")) – The block duration in seconds (default 12.0). Used for timing calculations in commit-reveal operations.

  * **commit_reveal_version** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The version of the commit-reveal protocol to use (default 4 for CRv4).

  * **max_attempts** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The maximum number of attempts to set weights if rate limiting is encountered (default 5).

  * **version_key** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Version key for compatibility with the network.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be finalized on the blockchain.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Example

# Set weights directly (for non-commit-reveal subnets) response = await subtensor.set_weights(

> wallet=wallet, netuid=1, uids=[0, 1, 2], weights=[0.5, 0.3, 0.2]

)

# For commit-reveal subnets, the method automatically handles commit and reveal phases

Notes

This function is crucial in the Yuma Consensus mechanism, where each validator’s weight vector contributes to the overall weight matrix used to calculate emissions and maintain network consensus.

  * <<https://docs.learnbittensor.org/resources/glossary#yuma-consensus>>

  * <<https://docs.learnbittensor.org/concepts/commit-reveal>>

  * Rate Limits: <<https://docs.learnbittensor.org/learn/chain-rate-limits#weights-setting-rate-limit>>




async sign_and_send_extrinsic(_call_ , _wallet_ , _sign_with ='coldkey'_, _use_nonce =False_, _nonce_key ='hotkey'_, _nonce =None_, _*_ , _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =False_, _calling_function =None_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.sign_and_send_extrinsic> "Link to this definition")
    

Helper method to sign and submit an extrinsic call to chain.

Parameters:
    

  * **call** (_scalecodec.GenericCall_) – A prepared Call object

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet whose coldkey will be used to sign the extrinsic

  * **sign_with** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The wallet’s keypair to use for the signing. Options are “coldkey”, “hotkey”, “coldkeypub”

  * **use_nonce** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Unique identifier for the transaction related with hot/coldkey.

  * **nonce_key** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The type on nonce to use. Options are “hotkey” or “coldkey”.

  * **nonce** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The nonce to use for the transaction. If not provided, it will be fetched from the chain.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises the relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait until the extrinsic call is included on the chain

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait until the extrinsic call is finalized on the chain

  * **calling_function** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The name of the calling function.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Raises:
    

**SubstrateRequestException** – Substrate request exception.

async sim_swap(_origin_netuid_ , _destination_netuid_ , _amount_ , _block_hash =None_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.sim_swap> "Link to this definition")
    

Simulates a swap/stake operation and calculates the fees and resulting amounts.

This method queries the SimSwap Runtime API to calculate the swap fees (in Alpha or TAO) and the quantities of Alpha or TAO tokens expected as output from the transaction. This simulation does NOT include the blockchain extrinsic transaction fee (the fee to submit the transaction itself).

When moving stake between subnets, the operation may involve swapping Alpha (subnet-specific stake token) to TAO (the base network token), then TAO to Alpha on the destination subnet. For subnet 0 (root network), all stake is in TAO.

Parameters:
    

  * **origin_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Netuid of the source subnet (0 if add stake).

  * **destination_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Netuid of the destination subnet.

  * **amount** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – Amount to swap/stake as a Balance object. Use Balance.from_tao(…) or Balance.from_rao(…) to create the amount.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the blockchain block for the query. If None, uses the current chain head.



Returns:
    

Object containing alpha_fee, tao_fee, alpha_amount, and tao_amount fields representing the swap fees and output amounts.

Return type:
    

[SimSwapResult](<../chain_data/sim_swap/index.html#bittensor.core.chain_data.sim_swap.SimSwapResult> "bittensor.core.chain_data.sim_swap.SimSwapResult")

Example

# Simulate staking 100 TAO stake to subnet 1 result = await subtensor.sim_swap(

> origin_netuid=0, destination_netuid=1, amount=Balance.from_tao(100)

) print(f”Fee: {result.tao_fee.tao} TAO, Output: {result.alpha_amount} Alpha”)

Notes

  * **Alpha** : Subnet-specific stake token (dynamic TAO)

  * **TAO** : Base network token; subnet 0 uses TAO directly

  * The returned fees do NOT include the extrinsic transaction fee

  * Transaction Fees: <<https://docs.learnbittensor.org/learn/fees>>

  * Glossary: <<https://docs.learnbittensor.org/glossary>>




async start_call(_wallet_ , _netuid_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =False_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.start_call> "Link to this definition")
    

Submits a start_call extrinsic to the blockchain to trigger emission start for a subnet.

This method initiates the emission mechanism for a newly registered subnet. Once called, the subnet becomes “active” and begins receiving TAO emissions. Only the subnet owner (the wallet that registered the subnet) is authorized to call this method.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet used to sign the extrinsic (must be unlocked and must be the subnet owner).

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the target subnet for which emissions are being started.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

Only the subnet owner can call this method. After successful execution, the subnet becomes active and eligible for TAO emissions.

  * <<https://docs.learnbittensor.org/subnets/create-a-subnet>>




async state_call(_method_ , _data_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.state_call> "Link to this definition")
    

Makes a state call to the Bittensor blockchain, allowing for direct queries of the blockchain’s state. This function is typically used for advanced, nonstandard queries not provided by other getter methods.

Use this method when you need to query runtime APIs or storage functions that don’t have dedicated wrapper methods in the SDK. For standard queries, prefer the specific getter methods (e.g., get_balance, get_stake) which provide better type safety and error handling.

Parameters:
    

  * **method** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The runtime API method name (e.g., “SubnetInfoRuntimeApi”, “get_metagraph”).

  * **data** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – Hex-encoded string of the SCALE-encoded parameters to pass to the method.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to query. Do not specify if using block_hash or reuse_block.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The block hash at which to check the parameter. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

The result of the rpc call.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any"), [Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any")]

async subnet(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.subnet> "Link to this definition")
    

Retrieves the subnet information for a single subnet in the Bittensor network.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to get the subnets at.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the blockchain block number for the query.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain block hash.



Returns:
    

A DynamicInfo object, containing detailed information about a subnet.

Return type:
    

Optional[bittensor.core.chain_data.DynamicInfo]

async subnet_exists(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.subnet_exists> "Link to this definition")
    

Checks if a subnet with the specified unique identifier (netuid) exists within the Bittensor network.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the blockchain block number at which to check the subnet existence.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

True if the subnet exists, False otherwise.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

This function is critical for verifying the presence of specific subnets in the network, enabling a deeper understanding of the network’s structure and composition.

async subnetwork_n(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.subnetwork_n> "Link to this definition")
    

Returns the current number of registered neurons (UIDs) in a subnet.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnetwork.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block at which to query. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

The current number of registered neurons in the subnet, or None if the subnetwork does not exist.

Return type:
    

Optional[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

substrate[#](<#bittensor.core.async_subtensor.AsyncSubtensor.substrate> "Link to this definition")
    

async swap_coldkey_announced(_wallet_ , _new_coldkey_ss58_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.swap_coldkey_announced> "Link to this definition")
    

Executes a previously announced coldkey swap.

This method executes a coldkey swap that was previously announced via announce_coldkey_swap. The new coldkey address must match the hash that was announced, and the delay period must have passed.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (should be the current coldkey wallet that made the announcement).

  * **new_coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the new coldkey to swap to. This must match the hash that was announced.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If `True`, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If `False`, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning `False` if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * The new coldkey hash must match the hash that was announced.

  * The delay period must have passed (check via get_coldkey_swap_announcement).

  * All assets, stakes, subnet ownerships, and hotkey associations are transferred from the old coldkey to the new one.

  * See: <<https://docs.learnbittensor.org/keys/coldkey-swap>>




async swap_stake(_wallet_ , _hotkey_ss58_ , _origin_netuid_ , _destination_netuid_ , _amount_ , _safe_swapping =False_, _allow_partial_stake =False_, _rate_tolerance =0.005_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.swap_stake> "Link to this definition")
    

Moves stake between subnets while keeping the same coldkey-hotkey pair ownership.

This method swaps stake from one subnet to another, effectively moving the same stake amount (minus fees) from the origin subnet to the destination subnet. Like subnet hopping - same owner, same hotkey, just changing which subnet the stake is in.

The amount parameter is specified as a Balance object (in TAO or Alpha units depending on the subnet). The actual amount received may be less due to swap fees and potential slippage. When safe_swapping is enabled, the method uses price ratio checks to protect against unfavorable price movements during the swap.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet to swap stake from.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the hotkey whose stake is being swapped.

  * **origin_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid from which stake is removed.

  * **destination_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid to which stake is added.

  * **amount** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – The amount to swap as a Balance object (in TAO or Alpha units). The actual amount received may be less due to swap fees and slippage.

  * **safe_swapping** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, enables price safety checks to protect against fluctuating prices. The swap will only execute if the price ratio between subnets doesn’t exceed the rate tolerance.

  * **allow_partial_stake** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True and safe_swapping is enabled, allows partial stake swaps when the full amount would exceed the price tolerance. If False, the entire swap fails if it would exceed the tolerance.

  * **rate_tolerance** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")) – The maximum allowed increase in the price ratio between subnets (origin_price/destination_price). For example, 0.005 = 0.5% maximum increase. Only used when safe_swapping is True.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

The price ratio for swap_stake in safe mode is calculated as: origin_subnet_price / destination_subnet_price. When safe_swapping is enabled, the swap will only execute if: \- With allow_partial_stake=False: The entire swap amount can be executed without the price ratio

> increasing more than rate_tolerance.

  * With allow_partial_stake=True: A partial amount will be swapped up to the point where the price ratio would increase by rate_tolerance.

  * Price Protection: <<https://docs.learnbittensor.org/learn/price-protection>>

  * Rate Limits: <<https://docs.learnbittensor.org/learn/chain-rate-limits#staking-operations-rate-limits>>

  * <<https://docs.learnbittensor.org/navigating-subtensor/swap-stake>>




async tempo(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.tempo> "Link to this definition")
    

Returns the Tempo hyperparameter for a subnet.

Tempo determines the length of an epoch in blocks. It defines how frequently the subnet’s consensus mechanism runs, calculating emissions and updating rankings. A tempo of 360 blocks equals approximately 72 minutes (360 blocks × 12 seconds per block).

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnetwork.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block at which to query. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

The tempo value in blocks, or None if the subnetwork does not exist.

Return type:
    

Optional[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

Notes

  * <<https://docs.learnbittensor.org/resources/glossary#tempo>>

  * <<https://docs.learnbittensor.org/resources/glossary#epoch>>




async toggle_user_liquidity(_wallet_ , _netuid_ , _enable_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.toggle_user_liquidity> "Link to this definition")
    

Toggles the user liquidity feature for a specified subnet.

This method enables or disables user liquidity positions for a subnet. Only the subnet owner (the wallet that registered the subnet) is authorized to call this method.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet used to sign the extrinsic (must be unlocked and must be the subnet owner).

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the target subnet for which user liquidity is being toggled.

  * **enable** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Boolean indicating whether to enable (True) or disable (False) user liquidity.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

Only the subnet owner can execute this call successfully.

  * <<https://docs.learnbittensor.org/liquidity-positions/liquidity-positions>>




async transfer(_wallet_ , _destination_ss58_ , _amount_ , _transfer_all =False_, _keep_alive =True_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =False_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.transfer> "Link to this definition")
    

Transfers TAO tokens from the source wallet to a destination address.

This method transfers TAO tokens from the wallet’s coldkey to the specified destination address. The amount is specified as a Balance object (in TAO or Rao units). Use get_transfer_fee to pre-estimate the transaction fee before sending.

When keep_alive=True, the transfer ensures the source account maintains at least the existential deposit amount. If keep_alive=False, the transfer may reduce the source account balance below the existential deposit, which could result in the account being reaped (removed) from the chain.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Source wallet for the transfer (must be unlocked).

  * **destination_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – Destination SS58 address for the transfer.

  * **amount** (_Optional_ _[_[_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") _]_) – Amount of TAO to transfer as a Balance object. If None and transfer_all=True, transfers all available balance minus fees and existential deposit (if keep_alive=True).

  * **transfer_all** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, transfers all available tokens (minus fees and existential deposit if keep_alive=True). Ignored if amount is specified.

  * **keep_alive** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, ensures the source account maintains at least the existential deposit amount. If False, the transfer may reduce the balance below the existential deposit, potentially causing the account to be reaped.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

The existential deposit is the minimum balance required to keep an account alive on the chain. Use [`get_existential_deposit()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_existential_deposit> "bittensor.core.async_subtensor.AsyncSubtensor.get_existential_deposit") to query the current value.

  * <<https://docs.learnbittensor.org/resources/glossary#existential-deposit>>

  * <<https://docs.learnbittensor.org/resources/glossary#transfer>>




async transfer_stake(_wallet_ , _destination_coldkey_ss58_ , _hotkey_ss58_ , _origin_netuid_ , _destination_netuid_ , _amount_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.transfer_stake> "Link to this definition")
    

Transfers stake from one subnet to another while changing the coldkey owner.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet to transfer stake from.

  * **destination_coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The destination coldkey SS58 address.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey SS58 address associated with the stake.

  * **origin_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The source subnet UID.

  * **destination_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The destination subnet UID.

  * **amount** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – Amount to transfer.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Price Protection: <<https://docs.learnbittensor.org/learn/price-protection>>

  * Rate Limits: <<https://docs.learnbittensor.org/learn/chain-rate-limits#staking-operations-rate-limits>>




async tx_rate_limit(_block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.tx_rate_limit> "Link to this definition")
    

Retrieves the transaction rate limit for the Bittensor network as of a specific blockchain block. This rate limit sets the maximum number of transactions that can be processed within a given time frame.

Parameters:
    

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the blockchain block number at which to check the subnet existence.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash.



Returns:
    

The transaction rate limit of the network, None if not available.

Return type:
    

Optional[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

The transaction rate limit is an essential parameter for ensuring the stability and scalability of the Bittensor network. It helps in managing network load and preventing congestion, thereby maintaining efficient and timely transaction processing.

async unstake(_wallet_ , _netuid_ , _hotkey_ss58_ , _amount_ , _allow_partial_stake =False_, _safe_unstaking =False_, _rate_tolerance =0.005_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.unstake> "Link to this definition")
    

Removes a specified amount of stake from a single hotkey account. This function is critical for adjusting individual neuron stakes within the Bittensor network.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet associated with the neuron from which the stake is being removed.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the hotkey account to unstake from.

  * **amount** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – The amount of alpha to unstake. If not specified, unstakes all. Alpha amount.

  * **allow_partial_stake** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True and safe_staking is enabled, allows partial unstaking when the full amount would exceed the price tolerance. If false, the entire unstake fails if it would exceed the tolerance.

  * **rate_tolerance** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")) – The maximum allowed price change ratio when unstaking. For example, 0.005 = 0.5% maximum price decrease. Only used when safe_staking is True.

  * **safe_unstaking** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, enables price safety checks to protect against fluctuating prices. The unstake will only execute if the price change doesn’t exceed the rate tolerance.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If T`rue`, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

This function supports flexible stake management, allowing neurons to adjust their network participation and potential reward accruals.

Notes

  * Price Protection: <<https://docs.learnbittensor.org/learn/price-protection>>

  * Rate Limits: <<https://docs.learnbittensor.org/learn/chain-rate-limits#staking-operations-rate-limits>>




async unstake_all(_wallet_ , _netuid_ , _hotkey_ss58_ , _rate_tolerance =0.005_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.unstake_all> "Link to this definition")
    

Unstakes all TAO/Alpha associated with a hotkey from the specified subnet on the Bittensor network.

This method unstakes all stake from a hotkey on a specific subnet. When rate_tolerance is specified, the method uses safe unstaking behavior to protect against unfavorable price movements due to liquidity/price impact. The rate_tolerance parameter limits the maximum price change ratio during the unstaking operation.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet of the stake owner (must be unlocked).

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the hotkey to unstake from.

  * **rate_tolerance** (_Optional_ _[_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _]_) – The maximum allowed price change ratio when unstaking (default 0.005 = 0.5% maximum price decrease). If None, unstaking proceeds without price limit protection. Only used for subnets with liquidity pools where price impact may occur.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If` True`, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Example

# If you would like to unstake all stakes in all subnets safely, use default rate_tolerance or pass your

# value:

import bittensor as bt subtensor = bt.AsyncSubtensor() wallet = bt.Wallet(“my_wallet”) netuid = 14 hotkey = “5%SOME_HOTKEY_WHERE_IS_YOUR_STAKE_NOW%” wallet_stakes = await subtensor.get_stake_info_for_coldkey(coldkey_ss58=wallet.coldkey.ss58_address) for stake in wallet_stakes:

> result = await subtensor.unstake_all(
>     
> 
> wallet=wallet, hotkey_ss58=stake.hotkey_ss58, netuid=stake.netuid,
> 
> ) print(result)

# If you would like to unstake all stakes in all subnets unsafely, use rate_tolerance=None:

import bittensor as bt subtensor = bt.AsyncSubtensor() wallet = bt.Wallet(“my_wallet”) netuid = 14 hotkey = “5%SOME_HOTKEY_WHERE_IS_YOUR_STAKE_NOW%” wallet_stakes = await subtensor.get_stake_info_for_coldkey(coldkey_ss58=wallet.coldkey.ss58_address) for stake in wallet_stakes:

> result = await subtensor.unstake_all(
>     
> 
> wallet=wallet, hotkey_ss58=stake.hotkey_ss58, netuid=stake.netuid, rate_tolerance=None,
> 
> ) print(result)

Notes

  * Slippage: <<https://docs.learnbittensor.org/learn/slippage>>

  * Price Protection: <<https://docs.learnbittensor.org/learn/price-protection>>

  * Rate Limits: <<https://docs.learnbittensor.org/learn/chain-rate-limits#staking-operations-rate-limits>>

  * Managing Stake with SDK: <<https://docs.learnbittensor.org/staking-and-delegation/managing-stake-sdk>>




async unstake_multiple(_wallet_ , _netuids_ , _hotkey_ss58s_ , _amounts =None_, _unstake_all =False_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.unstake_multiple> "Link to this definition")
    

Performs batch unstaking from multiple hotkey accounts, allowing a neuron to reduce its staked amounts efficiently. This function is useful for managing the distribution of stakes across multiple neurons.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet linked to the coldkey from which the stakes are being withdrawn.

  * **netuids** ([_bittensor.core.types.UIDs_](<../types/index.html#bittensor.core.types.UIDs> "bittensor.core.types.UIDs")) – Subnets unique IDs.

  * **hotkey_ss58s** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – A list of hotkey SS58 addresses to unstake from.

  * **amounts** (_Optional_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") _]__]_) – The amounts of TAO to unstake from each hotkey. If not provided, unstakes all.

  * **unstake_all** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, unstakes all tokens. Amounts are ignored.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Slippage: <<https://docs.learnbittensor.org/learn/slippage>>

  * Price Protection: <<https://docs.learnbittensor.org/learn/price-protection>>

  * Rate Limits: <<https://docs.learnbittensor.org/learn/chain-rate-limits#staking-operations-rate-limits>>

  * Managing Stake with SDK: <<https://docs.learnbittensor.org/staking-and-delegation/managing-stake-sdk>>




async update_cap_crowdloan(_wallet_ , _crowdloan_id_ , _new_cap_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.update_cap_crowdloan> "Link to this definition")
    

Updates the fundraising cap of an active (non-finalized) crowdloan.

Allows the creator to adjust the maximum total contribution amount before finalization. The new cap must be at least equal to the amount already raised. This is useful for adjusting campaign goals based on contributor feedback or changing subnet costs.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet instance used to sign the transaction (must be the creator’s coldkey).

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to update.

  * **new_cap** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – The new fundraising cap (TAO). Must be >= raised.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after submission.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, raises an exception rather than returning failure in the response.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

ExtrinsicResponse indicating success or failure, with error details if applicable.

Return type:
    

[bittensor.core.types.ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Only the creator can update the cap.

  * The crowdloan must not be finalized.

  * The new cap must be >= the total funds already raised.

  * Crowdloans Overview: <<https://docs.learnbittensor.org/subnets/crowdloans>>

  * Update Parameters: <<https://docs.learnbittensor.org/subnets/crowdloans#crowdloan-lifecycle>>




async update_end_crowdloan(_wallet_ , _crowdloan_id_ , _new_end_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.update_end_crowdloan> "Link to this definition")
    

Updates the end block of an active (non-finalized) crowdloan.

Allows the creator to extend (or shorten) the contribution period before finalization. The new end block must be in the future and respect the minimum and maximum duration bounds defined in the runtime constants. This is useful for extending campaigns that need more time to reach their cap or shortening campaigns with sufficient contributions.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet instance used to sign the transaction (must be the creator’s coldkey).

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to update.

  * **new_end** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The new block number at which the crowdloan will end. Must be between MinimumBlockDuration (7 days = 50,400 blocks) and MaximumBlockDuration (60 days = 432,000 blocks) from the current block.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after submission.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, raises an exception rather than returning failure in the response.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

ExtrinsicResponse indicating success or failure, with error details if applicable.

Return type:
    

[bittensor.core.types.ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Only the creator can update the end block.

  * The crowdloan must not be finalized.

  * The new end block must respect duration bounds (MinimumBlockDuration to MaximumBlockDuration).

  * Crowdloans Overview: <<https://docs.learnbittensor.org/subnets/crowdloans>>

  * Update Parameters: <<https://docs.learnbittensor.org/subnets/crowdloans#crowdloan-lifecycle>>




async update_min_contribution_crowdloan(_wallet_ , _crowdloan_id_ , _new_min_contribution_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.update_min_contribution_crowdloan> "Link to this definition")
    

Updates the minimum contribution amount of an active (non-finalized) crowdloan.

Allows the creator to adjust the minimum per-contribution amount before finalization. The new value must meet or exceed the AbsoluteMinimumContribution constant. This is useful for adjusting contribution requirements based on the number of expected contributors or campaign strategy.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet instance used to sign the transaction (must be the creator’s coldkey).

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to update.

  * **new_min_contribution** ([_bittensor.utils.balance.Balance_](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – The new minimum contribution amount (TAO). Must be >= AbsoluteMinimumContribution.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after submission.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, raises an exception rather than returning failure in the response.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

ExtrinsicResponse indicating success or failure, with error details if applicable.

Return type:
    

[bittensor.core.types.ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Only the creator can update the minimum contribution.

  * The crowdloan must not be finalized.

  * The new minimum must be >= AbsoluteMinimumContribution (check via get_crowdloan_constants).

  * Crowdloans Overview: <<https://docs.learnbittensor.org/subnets/crowdloans>>

  * Update Parameters: <<https://docs.learnbittensor.org/subnets/crowdloans#crowdloan-lifecycle>>




async validate_extrinsic_params(_call_module_ , _call_function_ , _call_params_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.validate_extrinsic_params> "Link to this definition")
    

Validate and filter extrinsic parameters against on-chain metadata.

This method checks that the provided parameters match the expected signature of the given extrinsic (module and function) as defined in the Substrate metadata. It raises explicit errors for missing or invalid parameters and silently ignores any extra keys not present in the function definition.

Parameters:
    

  * **call_module** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The pallet name, e.g. “SubtensorModule” or “AdminUtils”.

  * **call_function** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The extrinsic function name, e.g. “set_weights” or “sudo_set_tempo”.

  * **call_params** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_Any_](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any") _]_) – A dictionary of parameters to validate.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The blockchain block_hash representation of the block id.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain block hash.



Returns:
    

A filtered dictionary containing only the parameters that are valid for the specified extrinsic.

Raises:
    

  * [**ValueError**](<https://docs.python.org/3/library/exceptions.html#ValueError> "\(in Python v3.14\)") – If the given module or function is not found in the chain metadata.

  * [**KeyError**](<https://docs.python.org/3/library/exceptions.html#KeyError> "\(in Python v3.14\)") – If one or more required parameters are missing.




Notes

This method does not compose or submit the extrinsic. It only ensures that call_params conforms to the expected schema derived from on-chain metadata. See also compose_call and sign_and_send_extrinsic.

async wait_for_block(_block =None_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.wait_for_block> "Link to this definition")
    

Waits until a specific block is reached on the chain. If no block is specified, waits for the next block.

Parameters:
    

**block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The block number to wait for. If None, waits for the next block.

Returns:
    

True if the target block was reached, False if timeout occurred.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

Example

# Waits for a specific block await subtensor.wait_for_block(block=1234)

async weights(_netuid_ , _mechid =0_, _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.weights> "Link to this definition")
    

Retrieves the weight distribution set by neurons within a specific subnet of the Bittensor network. This function maps each neuron’s UID to the weights it assigns to other neurons, reflecting the network’s trust and value assignment mechanisms.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Subnet unique identifier.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Subnet mechanism unique identifier.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The blockchain block_hash representation of the block id.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used blockchain block hash.



Returns:
    

A list of tuples mapping each neuron’s UID to its assigned weights.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]]]]

The weight distribution is a key factor in the network’s consensus algorithm and the ranking of neurons, influencing their influence and reward allocation within the subnet.

async weights_rate_limit(_netuid_ , _block =None_, _block_hash =None_, _reuse_block =False_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.weights_rate_limit> "Link to this definition")
    

Returns the WeightsSetRateLimit hyperparameter for a subnet.

This hyperparameter limits how many times a validator can set weights per epoch. It prevents validators from spamming weight updates and ensures stable consensus calculations. Once the limit is reached, validators must wait until the next epoch to set weights again.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnetwork.

  * **block** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The blockchain block number for the query.

  * **block_hash** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hash of the block at which to query. Do not set if using block or reuse_block.

  * **reuse_block** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to reuse the last-used block hash. Do not set if using block_hash or block.



Returns:
    

The maximum number of weight set operations allowed per epoch, or None if the subnetwork does not
    

exist or the parameter is not found.

Return type:
    

Optional[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

async withdraw_crowdloan(_wallet_ , _crowdloan_id_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.async_subtensor.AsyncSubtensor.withdraw_crowdloan> "Link to this definition")
    

Withdraws a contribution from an active (not yet finalized or dissolved) crowdloan.

Contributors can withdraw their contributions at any time before finalization. For regular contributors, the full contribution amount is returned. For the creator, only amounts exceeding the initial deposit can be withdrawn; the deposit itself remains locked until dissolution.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet instance used to sign the transaction (coldkey must match a contributor).

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to withdraw from.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after submission, after which it will be rejected.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, raises an exception rather than returning False in the response, in case the transaction fails.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

ExtrinsicResponse indicating success or failure, with error details if applicable.

Return type:
    

[bittensor.core.types.ExtrinsicResponse](<../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Crowdloans Overview: <<https://docs.learnbittensor.org/subnets/crowdloans>>

  * Crowdloan Lifecycle: <<https://docs.learnbittensor.org/subnets/crowdloans#crowdloan-lifecycle>>

  * Withdraw: <<https://docs.learnbittensor.org/subnets/crowdloans/crowdloans-tutorial#optional-withdraw>>




async bittensor.core.async_subtensor.get_async_subtensor(_network =None_, _config =None_, _mock =False_, _log_verbose =False_)[#](<#bittensor.core.async_subtensor.get_async_subtensor> "Link to this definition")
    

Factory method to create an initialized AsyncSubtensor instance.

This function creates an AsyncSubtensor instance and automatically initializes the connection to the blockchain. This is useful when you don’t want to manually call await subtensor.initialize() after instantiation.

Parameters:
    

  * **network** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The network name to connect to (e.g., finney for Bittensor mainnet, test for test network, local for a locally deployed blockchain). If None, uses the default network from config.

  * **config** (_Optional_ _[_[_bittensor.core.config.Config_](<../config/index.html#bittensor.core.config.Config> "bittensor.core.config.Config") _]_) – Configuration object for the AsyncSubtensor instance. If None, uses the default configuration.

  * **mock** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether this is a mock instance. FOR TESTING ONLY.

  * **log_verbose** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Enables or disables verbose logging.



Returns:
    

An initialized AsyncSubtensor instance ready for use.

Return type:
    

[AsyncSubtensor](<#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")

Example

# Create and initialize in one step subtensor = await get_async_subtensor(network=”finney”)

# Ready to use immediately block = await subtensor.get_current_block()

[ __ previous bittensor.core ](<../index.html> "previous page") [ next bittensor.core.axon __](<../axon/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`AsyncSubtensor`](<#bittensor.core.async_subtensor.AsyncSubtensor>)
      * [`AsyncSubtensor.add_liquidity()`](<#bittensor.core.async_subtensor.AsyncSubtensor.add_liquidity>)
      * [`AsyncSubtensor.add_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.add_proxy>)
      * [`AsyncSubtensor.add_stake()`](<#bittensor.core.async_subtensor.AsyncSubtensor.add_stake>)
      * [`AsyncSubtensor.add_stake_burn()`](<#bittensor.core.async_subtensor.AsyncSubtensor.add_stake_burn>)
      * [`AsyncSubtensor.add_stake_multiple()`](<#bittensor.core.async_subtensor.AsyncSubtensor.add_stake_multiple>)
      * [`AsyncSubtensor.all_subnets()`](<#bittensor.core.async_subtensor.AsyncSubtensor.all_subnets>)
      * [`AsyncSubtensor.announce_coldkey_swap()`](<#bittensor.core.async_subtensor.AsyncSubtensor.announce_coldkey_swap>)
      * [`AsyncSubtensor.announce_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.announce_proxy>)
      * [`AsyncSubtensor.block`](<#bittensor.core.async_subtensor.AsyncSubtensor.block>)
      * [`AsyncSubtensor.blocks_since_last_step()`](<#bittensor.core.async_subtensor.AsyncSubtensor.blocks_since_last_step>)
      * [`AsyncSubtensor.blocks_since_last_update()`](<#bittensor.core.async_subtensor.AsyncSubtensor.blocks_since_last_update>)
      * [`AsyncSubtensor.blocks_until_next_epoch()`](<#bittensor.core.async_subtensor.AsyncSubtensor.blocks_until_next_epoch>)
      * [`AsyncSubtensor.bonds()`](<#bittensor.core.async_subtensor.AsyncSubtensor.bonds>)
      * [`AsyncSubtensor.burned_register()`](<#bittensor.core.async_subtensor.AsyncSubtensor.burned_register>)
      * [`AsyncSubtensor.claim_root()`](<#bittensor.core.async_subtensor.AsyncSubtensor.claim_root>)
      * [`AsyncSubtensor.clear_coldkey_swap_announcement()`](<#bittensor.core.async_subtensor.AsyncSubtensor.clear_coldkey_swap_announcement>)
      * [`AsyncSubtensor.close()`](<#bittensor.core.async_subtensor.AsyncSubtensor.close>)
      * [`AsyncSubtensor.commit_reveal_enabled()`](<#bittensor.core.async_subtensor.AsyncSubtensor.commit_reveal_enabled>)
      * [`AsyncSubtensor.commit_weights()`](<#bittensor.core.async_subtensor.AsyncSubtensor.commit_weights>)
      * [`AsyncSubtensor.compose_call()`](<#bittensor.core.async_subtensor.AsyncSubtensor.compose_call>)
      * [`AsyncSubtensor.contribute_crowdloan()`](<#bittensor.core.async_subtensor.AsyncSubtensor.contribute_crowdloan>)
      * [`AsyncSubtensor.create_crowdloan()`](<#bittensor.core.async_subtensor.AsyncSubtensor.create_crowdloan>)
      * [`AsyncSubtensor.create_pure_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.create_pure_proxy>)
      * [`AsyncSubtensor.determine_block_hash()`](<#bittensor.core.async_subtensor.AsyncSubtensor.determine_block_hash>)
      * [`AsyncSubtensor.difficulty()`](<#bittensor.core.async_subtensor.AsyncSubtensor.difficulty>)
      * [`AsyncSubtensor.dispute_coldkey_swap()`](<#bittensor.core.async_subtensor.AsyncSubtensor.dispute_coldkey_swap>)
      * [`AsyncSubtensor.dissolve_crowdloan()`](<#bittensor.core.async_subtensor.AsyncSubtensor.dissolve_crowdloan>)
      * [`AsyncSubtensor.does_hotkey_exist()`](<#bittensor.core.async_subtensor.AsyncSubtensor.does_hotkey_exist>)
      * [`AsyncSubtensor.filter_netuids_by_registered_hotkeys()`](<#bittensor.core.async_subtensor.AsyncSubtensor.filter_netuids_by_registered_hotkeys>)
      * [`AsyncSubtensor.finalize_crowdloan()`](<#bittensor.core.async_subtensor.AsyncSubtensor.finalize_crowdloan>)
      * [`AsyncSubtensor.get_admin_freeze_window()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_admin_freeze_window>)
      * [`AsyncSubtensor.get_all_commitments()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_commitments>)
      * [`AsyncSubtensor.get_all_ema_tao_inflow()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_ema_tao_inflow>)
      * [`AsyncSubtensor.get_all_metagraphs_info()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_metagraphs_info>)
      * [`AsyncSubtensor.get_all_neuron_certificates()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_neuron_certificates>)
      * [`AsyncSubtensor.get_all_revealed_commitments()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_revealed_commitments>)
      * [`AsyncSubtensor.get_all_subnets_info()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_subnets_info>)
      * [`AsyncSubtensor.get_all_subnets_netuid()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_all_subnets_netuid>)
      * [`AsyncSubtensor.get_auto_stakes()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_auto_stakes>)
      * [`AsyncSubtensor.get_balance()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_balance>)
      * [`AsyncSubtensor.get_balances()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_balances>)
      * [`AsyncSubtensor.get_block_hash()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_block_hash>)
      * [`AsyncSubtensor.get_block_info()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_block_info>)
      * [`AsyncSubtensor.get_children()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_children>)
      * [`AsyncSubtensor.get_children_pending()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_children_pending>)
      * [`AsyncSubtensor.get_coldkey_swap_announcement()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_announcement>)
      * [`AsyncSubtensor.get_coldkey_swap_announcement_delay()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_announcement_delay>)
      * [`AsyncSubtensor.get_coldkey_swap_announcements()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_announcements>)
      * [`AsyncSubtensor.get_coldkey_swap_constants()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_constants>)
      * [`AsyncSubtensor.get_coldkey_swap_dispute()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_dispute>)
      * [`AsyncSubtensor.get_coldkey_swap_disputes()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_disputes>)
      * [`AsyncSubtensor.get_coldkey_swap_reannouncement_delay()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_coldkey_swap_reannouncement_delay>)
      * [`AsyncSubtensor.get_commitment()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_commitment>)
      * [`AsyncSubtensor.get_commitment_metadata()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_commitment_metadata>)
      * [`AsyncSubtensor.get_crowdloan_by_id()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_crowdloan_by_id>)
      * [`AsyncSubtensor.get_crowdloan_constants()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_crowdloan_constants>)
      * [`AsyncSubtensor.get_crowdloan_contributions()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_crowdloan_contributions>)
      * [`AsyncSubtensor.get_crowdloan_next_id()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_crowdloan_next_id>)
      * [`AsyncSubtensor.get_crowdloans()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_crowdloans>)
      * [`AsyncSubtensor.get_current_block()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_current_block>)
      * [`AsyncSubtensor.get_delegate_by_hotkey()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_delegate_by_hotkey>)
      * [`AsyncSubtensor.get_delegate_identities()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_delegate_identities>)
      * [`AsyncSubtensor.get_delegate_take()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_delegate_take>)
      * [`AsyncSubtensor.get_delegated()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_delegated>)
      * [`AsyncSubtensor.get_delegates()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_delegates>)
      * [`AsyncSubtensor.get_ema_tao_inflow()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_ema_tao_inflow>)
      * [`AsyncSubtensor.get_existential_deposit()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_existential_deposit>)
      * [`AsyncSubtensor.get_extrinsic_fee()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_extrinsic_fee>)
      * [`AsyncSubtensor.get_hotkey_owner()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_hotkey_owner>)
      * [`AsyncSubtensor.get_hotkey_stake`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_hotkey_stake>)
      * [`AsyncSubtensor.get_hyperparameter()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_hyperparameter>)
      * [`AsyncSubtensor.get_last_bonds_reset()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_last_bonds_reset>)
      * [`AsyncSubtensor.get_last_commitment_bonds_reset_block()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_last_commitment_bonds_reset_block>)
      * [`AsyncSubtensor.get_liquidity_list()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_liquidity_list>)
      * [`AsyncSubtensor.get_mechanism_count()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_mechanism_count>)
      * [`AsyncSubtensor.get_mechanism_emission_split()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_mechanism_emission_split>)
      * [`AsyncSubtensor.get_metagraph_info()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_metagraph_info>)
      * [`AsyncSubtensor.get_mev_shield_current_key()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_mev_shield_current_key>)
      * [`AsyncSubtensor.get_mev_shield_next_key()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_mev_shield_next_key>)
      * [`AsyncSubtensor.get_minimum_required_stake()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_minimum_required_stake>)
      * [`AsyncSubtensor.get_netuids_for_hotkey()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_netuids_for_hotkey>)
      * [`AsyncSubtensor.get_neuron_certificate()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_neuron_certificate>)
      * [`AsyncSubtensor.get_neuron_for_pubkey_and_subnet()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_neuron_for_pubkey_and_subnet>)
      * [`AsyncSubtensor.get_next_epoch_start_block()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_next_epoch_start_block>)
      * [`AsyncSubtensor.get_owned_hotkeys()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_owned_hotkeys>)
      * [`AsyncSubtensor.get_parents()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_parents>)
      * [`AsyncSubtensor.get_proxies()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_proxies>)
      * [`AsyncSubtensor.get_proxies_for_real_account()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_proxies_for_real_account>)
      * [`AsyncSubtensor.get_proxy_announcement()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_proxy_announcement>)
      * [`AsyncSubtensor.get_proxy_announcements()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_proxy_announcements>)
      * [`AsyncSubtensor.get_proxy_constants()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_proxy_constants>)
      * [`AsyncSubtensor.get_revealed_commitment()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_revealed_commitment>)
      * [`AsyncSubtensor.get_revealed_commitment_by_hotkey()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_revealed_commitment_by_hotkey>)
      * [`AsyncSubtensor.get_root_alpha_dividends_per_subnet()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_root_alpha_dividends_per_subnet>)
      * [`AsyncSubtensor.get_root_claim_type()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_root_claim_type>)
      * [`AsyncSubtensor.get_root_claimable_all_rates()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_root_claimable_all_rates>)
      * [`AsyncSubtensor.get_root_claimable_rate()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_root_claimable_rate>)
      * [`AsyncSubtensor.get_root_claimable_stake()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_root_claimable_stake>)
      * [`AsyncSubtensor.get_root_claimed()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_root_claimed>)
      * [`AsyncSubtensor.get_stake()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake>)
      * [`AsyncSubtensor.get_stake_add_fee()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_add_fee>)
      * [`AsyncSubtensor.get_stake_for_coldkey_and_hotkey()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_for_coldkey_and_hotkey>)
      * [`AsyncSubtensor.get_stake_for_hotkey()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_for_hotkey>)
      * [`AsyncSubtensor.get_stake_info_for_coldkey()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_info_for_coldkey>)
      * [`AsyncSubtensor.get_stake_info_for_coldkeys()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_info_for_coldkeys>)
      * [`AsyncSubtensor.get_stake_movement_fee()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_movement_fee>)
      * [`AsyncSubtensor.get_stake_weight()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_stake_weight>)
      * [`AsyncSubtensor.get_staking_hotkeys()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_staking_hotkeys>)
      * [`AsyncSubtensor.get_start_call_delay()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_start_call_delay>)
      * [`AsyncSubtensor.get_subnet_burn_cost()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_burn_cost>)
      * [`AsyncSubtensor.get_subnet_hyperparameters()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_hyperparameters>)
      * [`AsyncSubtensor.get_subnet_info()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_info>)
      * [`AsyncSubtensor.get_subnet_owner_hotkey()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_owner_hotkey>)
      * [`AsyncSubtensor.get_subnet_price()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_price>)
      * [`AsyncSubtensor.get_subnet_prices()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_prices>)
      * [`AsyncSubtensor.get_subnet_reveal_period_epochs()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_reveal_period_epochs>)
      * [`AsyncSubtensor.get_subnet_validator_permits()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_subnet_validator_permits>)
      * [`AsyncSubtensor.get_timelocked_weight_commits()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_timelocked_weight_commits>)
      * [`AsyncSubtensor.get_timestamp()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_timestamp>)
      * [`AsyncSubtensor.get_total_subnets()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_total_subnets>)
      * [`AsyncSubtensor.get_transfer_fee()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_transfer_fee>)
      * [`AsyncSubtensor.get_uid_for_hotkey_on_subnet()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_uid_for_hotkey_on_subnet>)
      * [`AsyncSubtensor.get_unstake_fee()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_unstake_fee>)
      * [`AsyncSubtensor.get_vote_data()`](<#bittensor.core.async_subtensor.AsyncSubtensor.get_vote_data>)
      * [`AsyncSubtensor.immunity_period()`](<#bittensor.core.async_subtensor.AsyncSubtensor.immunity_period>)
      * [`AsyncSubtensor.initialize()`](<#bittensor.core.async_subtensor.AsyncSubtensor.initialize>)
      * [`AsyncSubtensor.is_fast_blocks()`](<#bittensor.core.async_subtensor.AsyncSubtensor.is_fast_blocks>)
      * [`AsyncSubtensor.is_hotkey_delegate()`](<#bittensor.core.async_subtensor.AsyncSubtensor.is_hotkey_delegate>)
      * [`AsyncSubtensor.is_hotkey_registered()`](<#bittensor.core.async_subtensor.AsyncSubtensor.is_hotkey_registered>)
      * [`AsyncSubtensor.is_hotkey_registered_any()`](<#bittensor.core.async_subtensor.AsyncSubtensor.is_hotkey_registered_any>)
      * [`AsyncSubtensor.is_hotkey_registered_on_subnet()`](<#bittensor.core.async_subtensor.AsyncSubtensor.is_hotkey_registered_on_subnet>)
      * [`AsyncSubtensor.is_in_admin_freeze_window()`](<#bittensor.core.async_subtensor.AsyncSubtensor.is_in_admin_freeze_window>)
      * [`AsyncSubtensor.is_subnet_active()`](<#bittensor.core.async_subtensor.AsyncSubtensor.is_subnet_active>)
      * [`AsyncSubtensor.kill_pure_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.kill_pure_proxy>)
      * [`AsyncSubtensor.last_drand_round()`](<#bittensor.core.async_subtensor.AsyncSubtensor.last_drand_round>)
      * [`AsyncSubtensor.log_verbose`](<#bittensor.core.async_subtensor.AsyncSubtensor.log_verbose>)
      * [`AsyncSubtensor.max_weight_limit()`](<#bittensor.core.async_subtensor.AsyncSubtensor.max_weight_limit>)
      * [`AsyncSubtensor.metagraph()`](<#bittensor.core.async_subtensor.AsyncSubtensor.metagraph>)
      * [`AsyncSubtensor.mev_submit_encrypted()`](<#bittensor.core.async_subtensor.AsyncSubtensor.mev_submit_encrypted>)
      * [`AsyncSubtensor.min_allowed_weights()`](<#bittensor.core.async_subtensor.AsyncSubtensor.min_allowed_weights>)
      * [`AsyncSubtensor.modify_liquidity()`](<#bittensor.core.async_subtensor.AsyncSubtensor.modify_liquidity>)
      * [`AsyncSubtensor.move_stake()`](<#bittensor.core.async_subtensor.AsyncSubtensor.move_stake>)
      * [`AsyncSubtensor.neuron_for_uid()`](<#bittensor.core.async_subtensor.AsyncSubtensor.neuron_for_uid>)
      * [`AsyncSubtensor.neurons()`](<#bittensor.core.async_subtensor.AsyncSubtensor.neurons>)
      * [`AsyncSubtensor.neurons_lite()`](<#bittensor.core.async_subtensor.AsyncSubtensor.neurons_lite>)
      * [`AsyncSubtensor.poke_deposit()`](<#bittensor.core.async_subtensor.AsyncSubtensor.poke_deposit>)
      * [`AsyncSubtensor.proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.proxy>)
      * [`AsyncSubtensor.proxy_announced()`](<#bittensor.core.async_subtensor.AsyncSubtensor.proxy_announced>)
      * [`AsyncSubtensor.query_constant()`](<#bittensor.core.async_subtensor.AsyncSubtensor.query_constant>)
      * [`AsyncSubtensor.query_identity()`](<#bittensor.core.async_subtensor.AsyncSubtensor.query_identity>)
      * [`AsyncSubtensor.query_map()`](<#bittensor.core.async_subtensor.AsyncSubtensor.query_map>)
      * [`AsyncSubtensor.query_map_subtensor()`](<#bittensor.core.async_subtensor.AsyncSubtensor.query_map_subtensor>)
      * [`AsyncSubtensor.query_module()`](<#bittensor.core.async_subtensor.AsyncSubtensor.query_module>)
      * [`AsyncSubtensor.query_runtime_api()`](<#bittensor.core.async_subtensor.AsyncSubtensor.query_runtime_api>)
      * [`AsyncSubtensor.query_subtensor()`](<#bittensor.core.async_subtensor.AsyncSubtensor.query_subtensor>)
      * [`AsyncSubtensor.recycle()`](<#bittensor.core.async_subtensor.AsyncSubtensor.recycle>)
      * [`AsyncSubtensor.refund_crowdloan()`](<#bittensor.core.async_subtensor.AsyncSubtensor.refund_crowdloan>)
      * [`AsyncSubtensor.register()`](<#bittensor.core.async_subtensor.AsyncSubtensor.register>)
      * [`AsyncSubtensor.register_limit()`](<#bittensor.core.async_subtensor.AsyncSubtensor.register_limit>)
      * [`AsyncSubtensor.register_subnet()`](<#bittensor.core.async_subtensor.AsyncSubtensor.register_subnet>)
      * [`AsyncSubtensor.reject_proxy_announcement()`](<#bittensor.core.async_subtensor.AsyncSubtensor.reject_proxy_announcement>)
      * [`AsyncSubtensor.remove_liquidity()`](<#bittensor.core.async_subtensor.AsyncSubtensor.remove_liquidity>)
      * [`AsyncSubtensor.remove_proxies()`](<#bittensor.core.async_subtensor.AsyncSubtensor.remove_proxies>)
      * [`AsyncSubtensor.remove_proxy()`](<#bittensor.core.async_subtensor.AsyncSubtensor.remove_proxy>)
      * [`AsyncSubtensor.remove_proxy_announcement()`](<#bittensor.core.async_subtensor.AsyncSubtensor.remove_proxy_announcement>)
      * [`AsyncSubtensor.reveal_weights()`](<#bittensor.core.async_subtensor.AsyncSubtensor.reveal_weights>)
      * [`AsyncSubtensor.root_register()`](<#bittensor.core.async_subtensor.AsyncSubtensor.root_register>)
      * [`AsyncSubtensor.root_set_pending_childkey_cooldown()`](<#bittensor.core.async_subtensor.AsyncSubtensor.root_set_pending_childkey_cooldown>)
      * [`AsyncSubtensor.serve_axon()`](<#bittensor.core.async_subtensor.AsyncSubtensor.serve_axon>)
      * [`AsyncSubtensor.set_auto_stake()`](<#bittensor.core.async_subtensor.AsyncSubtensor.set_auto_stake>)
      * [`AsyncSubtensor.set_children()`](<#bittensor.core.async_subtensor.AsyncSubtensor.set_children>)
      * [`AsyncSubtensor.set_commitment()`](<#bittensor.core.async_subtensor.AsyncSubtensor.set_commitment>)
      * [`AsyncSubtensor.set_delegate_take()`](<#bittensor.core.async_subtensor.AsyncSubtensor.set_delegate_take>)
      * [`AsyncSubtensor.set_reveal_commitment()`](<#bittensor.core.async_subtensor.AsyncSubtensor.set_reveal_commitment>)
      * [`AsyncSubtensor.set_root_claim_type()`](<#bittensor.core.async_subtensor.AsyncSubtensor.set_root_claim_type>)
      * [`AsyncSubtensor.set_subnet_identity()`](<#bittensor.core.async_subtensor.AsyncSubtensor.set_subnet_identity>)
      * [`AsyncSubtensor.set_weights()`](<#bittensor.core.async_subtensor.AsyncSubtensor.set_weights>)
      * [`AsyncSubtensor.sign_and_send_extrinsic()`](<#bittensor.core.async_subtensor.AsyncSubtensor.sign_and_send_extrinsic>)
      * [`AsyncSubtensor.sim_swap()`](<#bittensor.core.async_subtensor.AsyncSubtensor.sim_swap>)
      * [`AsyncSubtensor.start_call()`](<#bittensor.core.async_subtensor.AsyncSubtensor.start_call>)
      * [`AsyncSubtensor.state_call()`](<#bittensor.core.async_subtensor.AsyncSubtensor.state_call>)
      * [`AsyncSubtensor.subnet()`](<#bittensor.core.async_subtensor.AsyncSubtensor.subnet>)
      * [`AsyncSubtensor.subnet_exists()`](<#bittensor.core.async_subtensor.AsyncSubtensor.subnet_exists>)
      * [`AsyncSubtensor.subnetwork_n()`](<#bittensor.core.async_subtensor.AsyncSubtensor.subnetwork_n>)
      * [`AsyncSubtensor.substrate`](<#bittensor.core.async_subtensor.AsyncSubtensor.substrate>)
      * [`AsyncSubtensor.swap_coldkey_announced()`](<#bittensor.core.async_subtensor.AsyncSubtensor.swap_coldkey_announced>)
      * [`AsyncSubtensor.swap_stake()`](<#bittensor.core.async_subtensor.AsyncSubtensor.swap_stake>)
      * [`AsyncSubtensor.tempo()`](<#bittensor.core.async_subtensor.AsyncSubtensor.tempo>)
      * [`AsyncSubtensor.toggle_user_liquidity()`](<#bittensor.core.async_subtensor.AsyncSubtensor.toggle_user_liquidity>)
      * [`AsyncSubtensor.transfer()`](<#bittensor.core.async_subtensor.AsyncSubtensor.transfer>)
      * [`AsyncSubtensor.transfer_stake()`](<#bittensor.core.async_subtensor.AsyncSubtensor.transfer_stake>)
      * [`AsyncSubtensor.tx_rate_limit()`](<#bittensor.core.async_subtensor.AsyncSubtensor.tx_rate_limit>)
      * [`AsyncSubtensor.unstake()`](<#bittensor.core.async_subtensor.AsyncSubtensor.unstake>)
      * [`AsyncSubtensor.unstake_all()`](<#bittensor.core.async_subtensor.AsyncSubtensor.unstake_all>)
      * [`AsyncSubtensor.unstake_multiple()`](<#bittensor.core.async_subtensor.AsyncSubtensor.unstake_multiple>)
      * [`AsyncSubtensor.update_cap_crowdloan()`](<#bittensor.core.async_subtensor.AsyncSubtensor.update_cap_crowdloan>)
      * [`AsyncSubtensor.update_end_crowdloan()`](<#bittensor.core.async_subtensor.AsyncSubtensor.update_end_crowdloan>)
      * [`AsyncSubtensor.update_min_contribution_crowdloan()`](<#bittensor.core.async_subtensor.AsyncSubtensor.update_min_contribution_crowdloan>)
      * [`AsyncSubtensor.validate_extrinsic_params()`](<#bittensor.core.async_subtensor.AsyncSubtensor.validate_extrinsic_params>)
      * [`AsyncSubtensor.wait_for_block()`](<#bittensor.core.async_subtensor.AsyncSubtensor.wait_for_block>)
      * [`AsyncSubtensor.weights()`](<#bittensor.core.async_subtensor.AsyncSubtensor.weights>)
      * [`AsyncSubtensor.weights_rate_limit()`](<#bittensor.core.async_subtensor.AsyncSubtensor.weights_rate_limit>)
      * [`AsyncSubtensor.withdraw_crowdloan()`](<#bittensor.core.async_subtensor.AsyncSubtensor.withdraw_crowdloan>)
    * [`get_async_subtensor()`](<#bittensor.core.async_subtensor.get_async_subtensor>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.   

  *[*]: Keyword-only parameters separator (PEP 3102)