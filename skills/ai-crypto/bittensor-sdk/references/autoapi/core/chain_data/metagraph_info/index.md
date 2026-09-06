# bittensor.core.chain_data.metagraph_info &#8212; Bittensor SDK Docs  documentation

[Skip to main content](<#main-content>)

__Back to top __ `Ctrl`+`K`

[ ![Bittensor SDK Docs  documentation - Home](../../../../../_static/logo.svg) ![Bittensor SDK Docs  documentation - Home](../../../../../_static/logo-dark-mode.svg) ](<../../../../../index.html>)

__ Search `Ctrl`+`K`

Table of Contents

  * [API Reference](<../../../../index.html>) __
    * [bittensor](<../../../index.html>) __
      * [bittensor.core](<../../index.html>) __
        * [bittensor.core.async_subtensor](<../../async_subtensor/index.html>)
        * [bittensor.core.axon](<../../axon/index.html>)
        * [bittensor.core.chain_data](<../index.html>)
        * [bittensor.core.config](<../../config/index.html>)
        * [bittensor.core.dendrite](<../../dendrite/index.html>)
        * [bittensor.core.errors](<../../errors/index.html>)
        * [bittensor.core.extrinsics](<../../extrinsics/index.html>)
        * [bittensor.core.metagraph](<../../metagraph/index.html>)
        * [bittensor.core.settings](<../../settings/index.html>)
        * [bittensor.core.stream](<../../stream/index.html>)
        * [bittensor.core.subtensor](<../../subtensor/index.html>)
        * [bittensor.core.synapse](<../../synapse/index.html>)
        * [bittensor.core.tensor](<../../tensor/index.html>)
        * [bittensor.core.threadpool](<../../threadpool/index.html>)
        * [bittensor.core.types](<../../types/index.html>)
      * [bittensor.extras](<../../../extras/index.html>) __
        * [bittensor.extras.dev_framework](<../../../extras/dev_framework/index.html>)
        * [bittensor.extras.subtensor_api](<../../../extras/subtensor_api/index.html>)
        * [bittensor.extras.timelock](<../../../extras/timelock/index.html>)
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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/metagraph_info/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/metagraph_info/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/metagraph_info/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.metagraph_info

##  Contents 

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`MetagraphInfo`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo>)
      * [`MetagraphInfo.active`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.active>)
      * [`MetagraphInfo.activity_cutoff`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.activity_cutoff>)
      * [`MetagraphInfo.adjustment_alpha`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.adjustment_alpha>)
      * [`MetagraphInfo.adjustment_interval`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.adjustment_interval>)
      * [`MetagraphInfo.alpha_dividends_per_hotkey`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_dividends_per_hotkey>)
      * [`MetagraphInfo.alpha_high`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_high>)
      * [`MetagraphInfo.alpha_in`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_in>)
      * [`MetagraphInfo.alpha_in_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_in_emission>)
      * [`MetagraphInfo.alpha_low`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_low>)
      * [`MetagraphInfo.alpha_out`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_out>)
      * [`MetagraphInfo.alpha_out_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_out_emission>)
      * [`MetagraphInfo.alpha_stake`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_stake>)
      * [`MetagraphInfo.axons`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.axons>)
      * [`MetagraphInfo.block`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.block>)
      * [`MetagraphInfo.block_at_registration`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.block_at_registration>)
      * [`MetagraphInfo.blocks_since_last_step`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.blocks_since_last_step>)
      * [`MetagraphInfo.bonds_moving_avg`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.bonds_moving_avg>)
      * [`MetagraphInfo.burn`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.burn>)
      * [`MetagraphInfo.coldkeys`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.coldkeys>)
      * [`MetagraphInfo.commit_reveal_period`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.commit_reveal_period>)
      * [`MetagraphInfo.commit_reveal_weights_enabled`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.commit_reveal_weights_enabled>)
      * [`MetagraphInfo.commitments`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.commitments>)
      * [`MetagraphInfo.consensus`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.consensus>)
      * [`MetagraphInfo.difficulty`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.difficulty>)
      * [`MetagraphInfo.dividends`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.dividends>)
      * [`MetagraphInfo.emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.emission>)
      * [`MetagraphInfo.hotkeys`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.hotkeys>)
      * [`MetagraphInfo.identities`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.identities>)
      * [`MetagraphInfo.identity`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.identity>)
      * [`MetagraphInfo.immunity_period`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.immunity_period>)
      * [`MetagraphInfo.incentives`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.incentives>)
      * [`MetagraphInfo.kappa`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.kappa>)
      * [`MetagraphInfo.last_step`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.last_step>)
      * [`MetagraphInfo.last_update`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.last_update>)
      * [`MetagraphInfo.liquid_alpha_enabled`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.liquid_alpha_enabled>)
      * [`MetagraphInfo.max_burn`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.max_burn>)
      * [`MetagraphInfo.max_difficulty`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.max_difficulty>)
      * [`MetagraphInfo.max_regs_per_block`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.max_regs_per_block>)
      * [`MetagraphInfo.max_uids`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.max_uids>)
      * [`MetagraphInfo.max_validators`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.max_validators>)
      * [`MetagraphInfo.max_weights_limit`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.max_weights_limit>)
      * [`MetagraphInfo.mechid`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.mechid>)
      * [`MetagraphInfo.min_allowed_weights`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.min_allowed_weights>)
      * [`MetagraphInfo.min_burn`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.min_burn>)
      * [`MetagraphInfo.min_difficulty`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.min_difficulty>)
      * [`MetagraphInfo.moving_price`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.moving_price>)
      * [`MetagraphInfo.name`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.name>)
      * [`MetagraphInfo.netuid`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.netuid>)
      * [`MetagraphInfo.network_registered_at`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.network_registered_at>)
      * [`MetagraphInfo.num_uids`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.num_uids>)
      * [`MetagraphInfo.owner_coldkey`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.owner_coldkey>)
      * [`MetagraphInfo.owner_hotkey`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.owner_hotkey>)
      * [`MetagraphInfo.pending_alpha_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.pending_alpha_emission>)
      * [`MetagraphInfo.pending_root_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.pending_root_emission>)
      * [`MetagraphInfo.pow_registration_allowed`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.pow_registration_allowed>)
      * [`MetagraphInfo.pruning_score`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.pruning_score>)
      * [`MetagraphInfo.rank`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.rank>)
      * [`MetagraphInfo.registration_allowed`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.registration_allowed>)
      * [`MetagraphInfo.rho`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.rho>)
      * [`MetagraphInfo.serving_rate_limit`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.serving_rate_limit>)
      * [`MetagraphInfo.subnet_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.subnet_emission>)
      * [`MetagraphInfo.subnet_volume`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.subnet_volume>)
      * [`MetagraphInfo.symbol`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.symbol>)
      * [`MetagraphInfo.tao_dividends_per_hotkey`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.tao_dividends_per_hotkey>)
      * [`MetagraphInfo.tao_in`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.tao_in>)
      * [`MetagraphInfo.tao_in_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.tao_in_emission>)
      * [`MetagraphInfo.tao_stake`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.tao_stake>)
      * [`MetagraphInfo.target_regs_per_interval`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.target_regs_per_interval>)
      * [`MetagraphInfo.tempo`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.tempo>)
      * [`MetagraphInfo.total_stake`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.total_stake>)
      * [`MetagraphInfo.trust`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.trust>)
      * [`MetagraphInfo.validator_permit`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.validator_permit>)
      * [`MetagraphInfo.validators`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.validators>)
      * [`MetagraphInfo.weights_rate_limit`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.weights_rate_limit>)
      * [`MetagraphInfo.weights_version`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.weights_version>)
    * [`MetagraphInfoEmissions`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions>)
      * [`MetagraphInfoEmissions.alpha_in_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions.alpha_in_emission>)
      * [`MetagraphInfoEmissions.alpha_out_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions.alpha_out_emission>)
      * [`MetagraphInfoEmissions.pending_alpha_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions.pending_alpha_emission>)
      * [`MetagraphInfoEmissions.pending_root_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions.pending_root_emission>)
      * [`MetagraphInfoEmissions.subnet_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions.subnet_emission>)
      * [`MetagraphInfoEmissions.tao_in_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions.tao_in_emission>)
    * [`MetagraphInfoParams`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams>)
      * [`MetagraphInfoParams.activity_cutoff`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.activity_cutoff>)
      * [`MetagraphInfoParams.adjustment_alpha`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.adjustment_alpha>)
      * [`MetagraphInfoParams.adjustment_interval`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.adjustment_interval>)
      * [`MetagraphInfoParams.alpha_high`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.alpha_high>)
      * [`MetagraphInfoParams.alpha_low`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.alpha_low>)
      * [`MetagraphInfoParams.bonds_moving_avg`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.bonds_moving_avg>)
      * [`MetagraphInfoParams.burn`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.burn>)
      * [`MetagraphInfoParams.commit_reveal_period`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.commit_reveal_period>)
      * [`MetagraphInfoParams.commit_reveal_weights_enabled`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.commit_reveal_weights_enabled>)
      * [`MetagraphInfoParams.difficulty`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.difficulty>)
      * [`MetagraphInfoParams.immunity_period`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.immunity_period>)
      * [`MetagraphInfoParams.kappa`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.kappa>)
      * [`MetagraphInfoParams.liquid_alpha_enabled`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.liquid_alpha_enabled>)
      * [`MetagraphInfoParams.max_burn`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.max_burn>)
      * [`MetagraphInfoParams.max_difficulty`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.max_difficulty>)
      * [`MetagraphInfoParams.max_regs_per_block`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.max_regs_per_block>)
      * [`MetagraphInfoParams.max_validators`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.max_validators>)
      * [`MetagraphInfoParams.max_weights_limit`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.max_weights_limit>)
      * [`MetagraphInfoParams.min_allowed_weights`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.min_allowed_weights>)
      * [`MetagraphInfoParams.min_burn`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.min_burn>)
      * [`MetagraphInfoParams.min_difficulty`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.min_difficulty>)
      * [`MetagraphInfoParams.pow_registration_allowed`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.pow_registration_allowed>)
      * [`MetagraphInfoParams.registration_allowed`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.registration_allowed>)
      * [`MetagraphInfoParams.rho`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.rho>)
      * [`MetagraphInfoParams.serving_rate_limit`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.serving_rate_limit>)
      * [`MetagraphInfoParams.target_regs_per_interval`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.target_regs_per_interval>)
      * [`MetagraphInfoParams.tempo`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.tempo>)
      * [`MetagraphInfoParams.weights_rate_limit`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.weights_rate_limit>)
      * [`MetagraphInfoParams.weights_version`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.weights_version>)
    * [`MetagraphInfoPool`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoPool>)
      * [`MetagraphInfoPool.alpha_in`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoPool.alpha_in>)
      * [`MetagraphInfoPool.alpha_out`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoPool.alpha_out>)
      * [`MetagraphInfoPool.moving_price`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoPool.moving_price>)
      * [`MetagraphInfoPool.subnet_volume`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoPool.subnet_volume>)
      * [`MetagraphInfoPool.tao_in`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoPool.tao_in>)
    * [`SELECTIVE_METAGRAPH_COMMITMENTS_OFFSET`](<#bittensor.core.chain_data.metagraph_info.SELECTIVE_METAGRAPH_COMMITMENTS_OFFSET>)
    * [`SelectiveMetagraphIndex`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex>)
      * [`SelectiveMetagraphIndex.Active`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Active>)
      * [`SelectiveMetagraphIndex.ActivityCutoff`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.ActivityCutoff>)
      * [`SelectiveMetagraphIndex.AdjustmentAlpha`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AdjustmentAlpha>)
      * [`SelectiveMetagraphIndex.AdjustmentInterval`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AdjustmentInterval>)
      * [`SelectiveMetagraphIndex.AlphaDividendsPerHotkey`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaDividendsPerHotkey>)
      * [`SelectiveMetagraphIndex.AlphaHigh`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaHigh>)
      * [`SelectiveMetagraphIndex.AlphaIn`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaIn>)
      * [`SelectiveMetagraphIndex.AlphaInEmission`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaInEmission>)
      * [`SelectiveMetagraphIndex.AlphaLow`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaLow>)
      * [`SelectiveMetagraphIndex.AlphaOut`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaOut>)
      * [`SelectiveMetagraphIndex.AlphaOutEmission`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaOutEmission>)
      * [`SelectiveMetagraphIndex.AlphaStake`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaStake>)
      * [`SelectiveMetagraphIndex.Axons`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Axons>)
      * [`SelectiveMetagraphIndex.Block`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Block>)
      * [`SelectiveMetagraphIndex.BlockAtRegistration`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.BlockAtRegistration>)
      * [`SelectiveMetagraphIndex.BlocksSinceLastStep`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.BlocksSinceLastStep>)
      * [`SelectiveMetagraphIndex.BondsMovingAvg`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.BondsMovingAvg>)
      * [`SelectiveMetagraphIndex.Burn`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Burn>)
      * [`SelectiveMetagraphIndex.Coldkeys`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Coldkeys>)
      * [`SelectiveMetagraphIndex.CommitRevealPeriod`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.CommitRevealPeriod>)
      * [`SelectiveMetagraphIndex.CommitRevealWeightsEnabled`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.CommitRevealWeightsEnabled>)
      * [`SelectiveMetagraphIndex.Commitments`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Commitments>)
      * [`SelectiveMetagraphIndex.Consensus`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Consensus>)
      * [`SelectiveMetagraphIndex.Difficulty`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Difficulty>)
      * [`SelectiveMetagraphIndex.Dividends`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Dividends>)
      * [`SelectiveMetagraphIndex.Emission`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Emission>)
      * [`SelectiveMetagraphIndex.Hotkeys`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Hotkeys>)
      * [`SelectiveMetagraphIndex.Identities`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Identities>)
      * [`SelectiveMetagraphIndex.Identity`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Identity>)
      * [`SelectiveMetagraphIndex.ImmunityPeriod`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.ImmunityPeriod>)
      * [`SelectiveMetagraphIndex.Incentives`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Incentives>)
      * [`SelectiveMetagraphIndex.Kappa`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Kappa>)
      * [`SelectiveMetagraphIndex.LastStep`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.LastStep>)
      * [`SelectiveMetagraphIndex.LastUpdate`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.LastUpdate>)
      * [`SelectiveMetagraphIndex.LiquidAlphaEnabled`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.LiquidAlphaEnabled>)
      * [`SelectiveMetagraphIndex.MaxBurn`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MaxBurn>)
      * [`SelectiveMetagraphIndex.MaxDifficulty`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MaxDifficulty>)
      * [`SelectiveMetagraphIndex.MaxRegsPerBlock`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MaxRegsPerBlock>)
      * [`SelectiveMetagraphIndex.MaxUids`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MaxUids>)
      * [`SelectiveMetagraphIndex.MaxValidators`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MaxValidators>)
      * [`SelectiveMetagraphIndex.MaxWeightsLimit`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MaxWeightsLimit>)
      * [`SelectiveMetagraphIndex.MinAllowedWeights`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MinAllowedWeights>)
      * [`SelectiveMetagraphIndex.MinBurn`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MinBurn>)
      * [`SelectiveMetagraphIndex.MinDifficulty`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MinDifficulty>)
      * [`SelectiveMetagraphIndex.MovingPrice`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MovingPrice>)
      * [`SelectiveMetagraphIndex.Name`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Name>)
      * [`SelectiveMetagraphIndex.Netuid`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Netuid>)
      * [`SelectiveMetagraphIndex.NetworkRegisteredAt`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.NetworkRegisteredAt>)
      * [`SelectiveMetagraphIndex.NumUids`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.NumUids>)
      * [`SelectiveMetagraphIndex.OwnerColdkey`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.OwnerColdkey>)
      * [`SelectiveMetagraphIndex.OwnerHotkey`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.OwnerHotkey>)
      * [`SelectiveMetagraphIndex.PendingAlphaEmission`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.PendingAlphaEmission>)
      * [`SelectiveMetagraphIndex.PendingRootEmission`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.PendingRootEmission>)
      * [`SelectiveMetagraphIndex.PowRegistrationAllowed`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.PowRegistrationAllowed>)
      * [`SelectiveMetagraphIndex.PruningScore`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.PruningScore>)
      * [`SelectiveMetagraphIndex.Rank`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Rank>)
      * [`SelectiveMetagraphIndex.RegistrationAllowed`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.RegistrationAllowed>)
      * [`SelectiveMetagraphIndex.Rho`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Rho>)
      * [`SelectiveMetagraphIndex.ServingRateLimit`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.ServingRateLimit>)
      * [`SelectiveMetagraphIndex.SubnetEmission`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.SubnetEmission>)
      * [`SelectiveMetagraphIndex.SubnetVolume`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.SubnetVolume>)
      * [`SelectiveMetagraphIndex.Symbol`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Symbol>)
      * [`SelectiveMetagraphIndex.TaoDividendsPerHotkey`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.TaoDividendsPerHotkey>)
      * [`SelectiveMetagraphIndex.TaoIn`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.TaoIn>)
      * [`SelectiveMetagraphIndex.TaoInEmission`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.TaoInEmission>)
      * [`SelectiveMetagraphIndex.TaoStake`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.TaoStake>)
      * [`SelectiveMetagraphIndex.TargetRegsPerInterval`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.TargetRegsPerInterval>)
      * [`SelectiveMetagraphIndex.Tempo`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Tempo>)
      * [`SelectiveMetagraphIndex.TotalStake`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.TotalStake>)
      * [`SelectiveMetagraphIndex.Trust`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Trust>)
      * [`SelectiveMetagraphIndex.ValidatorPermit`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.ValidatorPermit>)
      * [`SelectiveMetagraphIndex.Validators`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Validators>)
      * [`SelectiveMetagraphIndex.WeightsRateLimit`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.WeightsRateLimit>)
      * [`SelectiveMetagraphIndex.WeightsVersion`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.WeightsVersion>)
      * [`SelectiveMetagraphIndex.all_indices()`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.all_indices>)
    * [`get_selective_metagraph_commitments()`](<#bittensor.core.chain_data.metagraph_info.get_selective_metagraph_commitments>)
    * [`process_nested()`](<#bittensor.core.chain_data.metagraph_info.process_nested>)



# bittensor.core.chain_data.metagraph_info[#](<#module-bittensor.core.chain_data.metagraph_info> "Link to this heading")

## Attributes[#](<#attributes> "Link to this heading")

[`SELECTIVE_METAGRAPH_COMMITMENTS_OFFSET`](<#bittensor.core.chain_data.metagraph_info.SELECTIVE_METAGRAPH_COMMITMENTS_OFFSET> "bittensor.core.chain_data.metagraph_info.SELECTIVE_METAGRAPH_COMMITMENTS_OFFSET") |   
---|---  
  
## Classes[#](<#classes> "Link to this heading")

[`MetagraphInfo`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo> "bittensor.core.chain_data.metagraph_info.MetagraphInfo") |   
---|---  
[`MetagraphInfoEmissions`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions> "bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions") | Emissions presented in tao values.  
[`MetagraphInfoParams`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams> "bittensor.core.chain_data.metagraph_info.MetagraphInfoParams") |   
[`MetagraphInfoPool`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoPool> "bittensor.core.chain_data.metagraph_info.MetagraphInfoPool") | Pool presented in tao values.  
[`SelectiveMetagraphIndex`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex> "bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex") | Create a collection of name/value pairs.  
  
## Functions[#](<#functions> "Link to this heading")

[`get_selective_metagraph_commitments`](<#bittensor.core.chain_data.metagraph_info.get_selective_metagraph_commitments> "bittensor.core.chain_data.metagraph_info.get_selective_metagraph_commitments")(decoded) | Returns a tuple of hotkeys and commitments from decoded chain data if provided, else None.  
---|---  
[`process_nested`](<#bittensor.core.chain_data.metagraph_info.process_nested> "bittensor.core.chain_data.metagraph_info.process_nested")(data, chr_transform) | Processes nested data structures by applying a transformation function to their elements.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.metagraph_info.MetagraphInfo[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo> "Link to this definition")
    

Bases: [`bittensor.core.chain_data.info_base.InfoBase`](<../info_base/index.html#bittensor.core.chain_data.info_base.InfoBase> "bittensor.core.chain_data.info_base.InfoBase")

active: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.active> "Link to this definition")
    

activity_cutoff: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.activity_cutoff> "Link to this definition")
    

adjustment_alpha: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.adjustment_alpha> "Link to this definition")
    

adjustment_interval: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.adjustment_interval> "Link to this definition")
    

alpha_dividends_per_hotkey: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")]][#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_dividends_per_hotkey> "Link to this definition")
    

alpha_high: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_high> "Link to this definition")
    

alpha_in: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_in> "Link to this definition")
    

alpha_in_emission: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_in_emission> "Link to this definition")
    

alpha_low: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_low> "Link to this definition")
    

alpha_out: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_out> "Link to this definition")
    

alpha_out_emission: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_out_emission> "Link to this definition")
    

alpha_stake: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")][#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_stake> "Link to this definition")
    

axons: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[bittensor.core.chain_data.axon_info.AxonInfo](<../axon_info/index.html#bittensor.core.chain_data.axon_info.AxonInfo> "bittensor.core.chain_data.axon_info.AxonInfo")][#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.axons> "Link to this definition")
    

block: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.block> "Link to this definition")
    

block_at_registration: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.block_at_registration> "Link to this definition")
    

blocks_since_last_step: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.blocks_since_last_step> "Link to this definition")
    

bonds_moving_avg: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.bonds_moving_avg> "Link to this definition")
    

burn: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.burn> "Link to this definition")
    

coldkeys: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.coldkeys> "Link to this definition")
    

commit_reveal_period: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.commit_reveal_period> "Link to this definition")
    

commit_reveal_weights_enabled: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.commit_reveal_weights_enabled> "Link to this definition")
    

commitments: [tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]] | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.commitments> "Link to this definition")
    

consensus: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.consensus> "Link to this definition")
    

difficulty: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.difficulty> "Link to this definition")
    

dividends: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.dividends> "Link to this definition")
    

emission: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")][#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.emission> "Link to this definition")
    

hotkeys: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.hotkeys> "Link to this definition")
    

identities: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[bittensor.core.chain_data.chain_identity.ChainIdentity](<../chain_identity/index.html#bittensor.core.chain_data.chain_identity.ChainIdentity> "bittensor.core.chain_data.chain_identity.ChainIdentity") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.identities> "Link to this definition")
    

identity: [bittensor.core.chain_data.subnet_identity.SubnetIdentity](<../subnet_identity/index.html#bittensor.core.chain_data.subnet_identity.SubnetIdentity> "bittensor.core.chain_data.subnet_identity.SubnetIdentity") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.identity> "Link to this definition")
    

immunity_period: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.immunity_period> "Link to this definition")
    

incentives: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.incentives> "Link to this definition")
    

kappa: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.kappa> "Link to this definition")
    

last_step: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.last_step> "Link to this definition")
    

last_update: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.last_update> "Link to this definition")
    

liquid_alpha_enabled: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.liquid_alpha_enabled> "Link to this definition")
    

max_burn: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.max_burn> "Link to this definition")
    

max_difficulty: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.max_difficulty> "Link to this definition")
    

max_regs_per_block: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.max_regs_per_block> "Link to this definition")
    

max_uids: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.max_uids> "Link to this definition")
    

max_validators: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.max_validators> "Link to this definition")
    

max_weights_limit: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.max_weights_limit> "Link to this definition")
    

mechid: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.mechid> "Link to this definition")
    

min_allowed_weights: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.min_allowed_weights> "Link to this definition")
    

min_burn: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.min_burn> "Link to this definition")
    

min_difficulty: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.min_difficulty> "Link to this definition")
    

moving_price: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.moving_price> "Link to this definition")
    

name: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.name> "Link to this definition")
    

netuid: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.netuid> "Link to this definition")
    

network_registered_at: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.network_registered_at> "Link to this definition")
    

num_uids: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.num_uids> "Link to this definition")
    

owner_coldkey: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.owner_coldkey> "Link to this definition")
    

owner_hotkey: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.owner_hotkey> "Link to this definition")
    

pending_alpha_emission: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.pending_alpha_emission> "Link to this definition")
    

pending_root_emission: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.pending_root_emission> "Link to this definition")
    

pow_registration_allowed: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.pow_registration_allowed> "Link to this definition")
    

pruning_score: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.pruning_score> "Link to this definition")
    

rank: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.rank> "Link to this definition")
    

registration_allowed: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.registration_allowed> "Link to this definition")
    

rho: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.rho> "Link to this definition")
    

serving_rate_limit: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.serving_rate_limit> "Link to this definition")
    

subnet_emission: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.subnet_emission> "Link to this definition")
    

subnet_volume: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.subnet_volume> "Link to this definition")
    

symbol: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.symbol> "Link to this definition")
    

tao_dividends_per_hotkey: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")]][#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.tao_dividends_per_hotkey> "Link to this definition")
    

tao_in: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.tao_in> "Link to this definition")
    

tao_in_emission: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.tao_in_emission> "Link to this definition")
    

tao_stake: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")][#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.tao_stake> "Link to this definition")
    

target_regs_per_interval: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.target_regs_per_interval> "Link to this definition")
    

tempo: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.tempo> "Link to this definition")
    

total_stake: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")][#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.total_stake> "Link to this definition")
    

trust: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.trust> "Link to this definition")
    

validator_permit: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.validator_permit> "Link to this definition")
    

validators: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")] | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.validators> "Link to this definition")
    

weights_rate_limit: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.weights_rate_limit> "Link to this definition")
    

weights_version: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.weights_version> "Link to this definition")
    

class bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions> "Link to this definition")
    

Emissions presented in tao values.

alpha_in_emission: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions.alpha_in_emission> "Link to this definition")
    

alpha_out_emission: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions.alpha_out_emission> "Link to this definition")
    

pending_alpha_emission: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions.pending_alpha_emission> "Link to this definition")
    

pending_root_emission: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions.pending_root_emission> "Link to this definition")
    

subnet_emission: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions.subnet_emission> "Link to this definition")
    

tao_in_emission: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions.tao_in_emission> "Link to this definition")
    

class bittensor.core.chain_data.metagraph_info.MetagraphInfoParams[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams> "Link to this definition")
    

activity_cutoff: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.activity_cutoff> "Link to this definition")
    

adjustment_alpha: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.adjustment_alpha> "Link to this definition")
    

adjustment_interval: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.adjustment_interval> "Link to this definition")
    

alpha_high: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.alpha_high> "Link to this definition")
    

alpha_low: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.alpha_low> "Link to this definition")
    

bonds_moving_avg: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.bonds_moving_avg> "Link to this definition")
    

burn: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.burn> "Link to this definition")
    

commit_reveal_period: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.commit_reveal_period> "Link to this definition")
    

commit_reveal_weights_enabled: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.commit_reveal_weights_enabled> "Link to this definition")
    

difficulty: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.difficulty> "Link to this definition")
    

immunity_period: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.immunity_period> "Link to this definition")
    

kappa: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.kappa> "Link to this definition")
    

liquid_alpha_enabled: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.liquid_alpha_enabled> "Link to this definition")
    

max_burn: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.max_burn> "Link to this definition")
    

max_difficulty: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.max_difficulty> "Link to this definition")
    

max_regs_per_block: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.max_regs_per_block> "Link to this definition")
    

max_validators: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.max_validators> "Link to this definition")
    

max_weights_limit: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.max_weights_limit> "Link to this definition")
    

min_allowed_weights: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.min_allowed_weights> "Link to this definition")
    

min_burn: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.min_burn> "Link to this definition")
    

min_difficulty: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.min_difficulty> "Link to this definition")
    

pow_registration_allowed: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.pow_registration_allowed> "Link to this definition")
    

registration_allowed: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.registration_allowed> "Link to this definition")
    

rho: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.rho> "Link to this definition")
    

serving_rate_limit: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.serving_rate_limit> "Link to this definition")
    

target_regs_per_interval: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.target_regs_per_interval> "Link to this definition")
    

tempo: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.tempo> "Link to this definition")
    

weights_rate_limit: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.weights_rate_limit> "Link to this definition")
    

weights_version: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.weights_version> "Link to this definition")
    

class bittensor.core.chain_data.metagraph_info.MetagraphInfoPool[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoPool> "Link to this definition")
    

Pool presented in tao values.

alpha_in: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoPool.alpha_in> "Link to this definition")
    

alpha_out: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoPool.alpha_out> "Link to this definition")
    

moving_price: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoPool.moving_price> "Link to this definition")
    

subnet_volume: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoPool.subnet_volume> "Link to this definition")
    

tao_in: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoPool.tao_in> "Link to this definition")
    

bittensor.core.chain_data.metagraph_info.SELECTIVE_METAGRAPH_COMMITMENTS_OFFSET = 14[#](<#bittensor.core.chain_data.metagraph_info.SELECTIVE_METAGRAPH_COMMITMENTS_OFFSET> "Link to this definition")
    

class bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex> "Link to this definition")
    

Bases: [`enum.Enum`](<https://docs.python.org/3/library/enum.html#enum.Enum> "\(in Python v3.14\)")

Create a collection of name/value pairs.

Example enumeration:
[code] 
    >>> class Color(Enum):
    ...     RED = 1
    ...     BLUE = 2
    ...     GREEN = 3
    
[/code]

Access them by:

  * attribute access:
[code] >>> Color.RED
        <Color.RED: 1>
        
[/code]

  * value lookup:
[code] >>> Color(1)
        <Color.RED: 1>
        
[/code]

  * name lookup:
[code] >>> Color['RED']
        <Color.RED: 1>
        
[/code]




Enumerations can be iterated over, and know how many members they have:
[code] 
    >>> len(Color)
    3
    
[/code]
[code] 
    >>> list(Color)
    [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]
    
[/code]

Methods can be added to enumerations, and members can have their own attributes – see the documentation for details.

Active = 56[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Active> "Link to this definition")
    

ActivityCutoff = 28[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.ActivityCutoff> "Link to this definition")
    

AdjustmentAlpha = 41[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AdjustmentAlpha> "Link to this definition")
    

AdjustmentInterval = 42[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AdjustmentInterval> "Link to this definition")
    

AlphaDividendsPerHotkey = 71[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaDividendsPerHotkey> "Link to this definition")
    

AlphaHigh = 49[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaHigh> "Link to this definition")
    

AlphaIn = 12[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaIn> "Link to this definition")
    

AlphaInEmission = 16[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaInEmission> "Link to this definition")
    

AlphaLow = 50[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaLow> "Link to this definition")
    

AlphaOut = 13[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaOut> "Link to this definition")
    

AlphaOutEmission = 15[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaOutEmission> "Link to this definition")
    

AlphaStake = 67[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaStake> "Link to this definition")
    

Axons = 55[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Axons> "Link to this definition")
    

Block = 7[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Block> "Link to this definition")
    

BlockAtRegistration = 66[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.BlockAtRegistration> "Link to this definition")
    

BlocksSinceLastStep = 10[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.BlocksSinceLastStep> "Link to this definition")
    

BondsMovingAvg = 51[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.BondsMovingAvg> "Link to this definition")
    

Burn = 32[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Burn> "Link to this definition")
    

Coldkeys = 53[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Coldkeys> "Link to this definition")
    

CommitRevealPeriod = 47[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.CommitRevealPeriod> "Link to this definition")
    

CommitRevealWeightsEnabled = 46[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.CommitRevealWeightsEnabled> "Link to this definition")
    

Commitments = 73[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Commitments> "Link to this definition")
    

Consensus = 63[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Consensus> "Link to this definition")
    

Difficulty = 33[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Difficulty> "Link to this definition")
    

Dividends = 61[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Dividends> "Link to this definition")
    

Emission = 60[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Emission> "Link to this definition")
    

Hotkeys = 52[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Hotkeys> "Link to this definition")
    

Identities = 54[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Identities> "Link to this definition")
    

Identity = 3[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Identity> "Link to this definition")
    

ImmunityPeriod = 36[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.ImmunityPeriod> "Link to this definition")
    

Incentives = 62[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Incentives> "Link to this definition")
    

Kappa = 23[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Kappa> "Link to this definition")
    

LastStep = 9[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.LastStep> "Link to this definition")
    

LastUpdate = 59[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.LastUpdate> "Link to this definition")
    

LiquidAlphaEnabled = 48[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.LiquidAlphaEnabled> "Link to this definition")
    

MaxBurn = 40[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MaxBurn> "Link to this definition")
    

MaxDifficulty = 38[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MaxDifficulty> "Link to this definition")
    

MaxRegsPerBlock = 44[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MaxRegsPerBlock> "Link to this definition")
    

MaxUids = 31[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MaxUids> "Link to this definition")
    

MaxValidators = 29[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MaxValidators> "Link to this definition")
    

MaxWeightsLimit = 25[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MaxWeightsLimit> "Link to this definition")
    

MinAllowedWeights = 24[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MinAllowedWeights> "Link to this definition")
    

MinBurn = 39[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MinBurn> "Link to this definition")
    

MinDifficulty = 37[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MinDifficulty> "Link to this definition")
    

MovingPrice = 21[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MovingPrice> "Link to this definition")
    

Name = 1[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Name> "Link to this definition")
    

Netuid = 0[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Netuid> "Link to this definition")
    

NetworkRegisteredAt = 4[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.NetworkRegisteredAt> "Link to this definition")
    

NumUids = 30[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.NumUids> "Link to this definition")
    

OwnerColdkey = 6[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.OwnerColdkey> "Link to this definition")
    

OwnerHotkey = 5[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.OwnerHotkey> "Link to this definition")
    

PendingAlphaEmission = 18[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.PendingAlphaEmission> "Link to this definition")
    

PendingRootEmission = 19[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.PendingRootEmission> "Link to this definition")
    

PowRegistrationAllowed = 35[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.PowRegistrationAllowed> "Link to this definition")
    

PruningScore = 58[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.PruningScore> "Link to this definition")
    

Rank = 65[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Rank> "Link to this definition")
    

RegistrationAllowed = 34[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.RegistrationAllowed> "Link to this definition")
    

Rho = 22[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Rho> "Link to this definition")
    

ServingRateLimit = 45[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.ServingRateLimit> "Link to this definition")
    

SubnetEmission = 11[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.SubnetEmission> "Link to this definition")
    

SubnetVolume = 20[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.SubnetVolume> "Link to this definition")
    

Symbol = 2[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Symbol> "Link to this definition")
    

TaoDividendsPerHotkey = 70[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.TaoDividendsPerHotkey> "Link to this definition")
    

TaoIn = 14[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.TaoIn> "Link to this definition")
    

TaoInEmission = 17[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.TaoInEmission> "Link to this definition")
    

TaoStake = 68[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.TaoStake> "Link to this definition")
    

TargetRegsPerInterval = 43[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.TargetRegsPerInterval> "Link to this definition")
    

Tempo = 8[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Tempo> "Link to this definition")
    

TotalStake = 69[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.TotalStake> "Link to this definition")
    

Trust = 64[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Trust> "Link to this definition")
    

ValidatorPermit = 57[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.ValidatorPermit> "Link to this definition")
    

Validators = 72[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Validators> "Link to this definition")
    

WeightsRateLimit = 27[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.WeightsRateLimit> "Link to this definition")
    

WeightsVersion = 26[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.WeightsVersion> "Link to this definition")
    

static all_indices()[#](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.all_indices> "Link to this definition")
    

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

bittensor.core.chain_data.metagraph_info.get_selective_metagraph_commitments(_decoded_)[#](<#bittensor.core.chain_data.metagraph_info.get_selective_metagraph_commitments> "Link to this definition")
    

Returns a tuple of hotkeys and commitments from decoded chain data if provided, else None.

Parameters:
    

**decoded** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)"))

Return type:
    

Optional[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]]]

bittensor.core.chain_data.metagraph_info.process_nested(_data_ , _chr_transform_)[#](<#bittensor.core.chain_data.metagraph_info.process_nested> "Link to this definition")
    

Processes nested data structures by applying a transformation function to their elements.

Parameters:
    

**data** (_Union_ _[_[_tuple_](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)") _,_[_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)") _]_)

Return type:
    

Optional[Union[[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)"), [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")]]

[ __ previous bittensor.core.chain_data.ip_info ](<../ip_info/index.html> "previous page") [ next bittensor.core.chain_data.neuron_info __](<../neuron_info/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`MetagraphInfo`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo>)
      * [`MetagraphInfo.active`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.active>)
      * [`MetagraphInfo.activity_cutoff`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.activity_cutoff>)
      * [`MetagraphInfo.adjustment_alpha`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.adjustment_alpha>)
      * [`MetagraphInfo.adjustment_interval`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.adjustment_interval>)
      * [`MetagraphInfo.alpha_dividends_per_hotkey`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_dividends_per_hotkey>)
      * [`MetagraphInfo.alpha_high`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_high>)
      * [`MetagraphInfo.alpha_in`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_in>)
      * [`MetagraphInfo.alpha_in_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_in_emission>)
      * [`MetagraphInfo.alpha_low`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_low>)
      * [`MetagraphInfo.alpha_out`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_out>)
      * [`MetagraphInfo.alpha_out_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_out_emission>)
      * [`MetagraphInfo.alpha_stake`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.alpha_stake>)
      * [`MetagraphInfo.axons`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.axons>)
      * [`MetagraphInfo.block`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.block>)
      * [`MetagraphInfo.block_at_registration`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.block_at_registration>)
      * [`MetagraphInfo.blocks_since_last_step`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.blocks_since_last_step>)
      * [`MetagraphInfo.bonds_moving_avg`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.bonds_moving_avg>)
      * [`MetagraphInfo.burn`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.burn>)
      * [`MetagraphInfo.coldkeys`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.coldkeys>)
      * [`MetagraphInfo.commit_reveal_period`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.commit_reveal_period>)
      * [`MetagraphInfo.commit_reveal_weights_enabled`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.commit_reveal_weights_enabled>)
      * [`MetagraphInfo.commitments`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.commitments>)
      * [`MetagraphInfo.consensus`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.consensus>)
      * [`MetagraphInfo.difficulty`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.difficulty>)
      * [`MetagraphInfo.dividends`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.dividends>)
      * [`MetagraphInfo.emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.emission>)
      * [`MetagraphInfo.hotkeys`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.hotkeys>)
      * [`MetagraphInfo.identities`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.identities>)
      * [`MetagraphInfo.identity`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.identity>)
      * [`MetagraphInfo.immunity_period`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.immunity_period>)
      * [`MetagraphInfo.incentives`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.incentives>)
      * [`MetagraphInfo.kappa`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.kappa>)
      * [`MetagraphInfo.last_step`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.last_step>)
      * [`MetagraphInfo.last_update`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.last_update>)
      * [`MetagraphInfo.liquid_alpha_enabled`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.liquid_alpha_enabled>)
      * [`MetagraphInfo.max_burn`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.max_burn>)
      * [`MetagraphInfo.max_difficulty`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.max_difficulty>)
      * [`MetagraphInfo.max_regs_per_block`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.max_regs_per_block>)
      * [`MetagraphInfo.max_uids`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.max_uids>)
      * [`MetagraphInfo.max_validators`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.max_validators>)
      * [`MetagraphInfo.max_weights_limit`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.max_weights_limit>)
      * [`MetagraphInfo.mechid`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.mechid>)
      * [`MetagraphInfo.min_allowed_weights`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.min_allowed_weights>)
      * [`MetagraphInfo.min_burn`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.min_burn>)
      * [`MetagraphInfo.min_difficulty`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.min_difficulty>)
      * [`MetagraphInfo.moving_price`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.moving_price>)
      * [`MetagraphInfo.name`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.name>)
      * [`MetagraphInfo.netuid`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.netuid>)
      * [`MetagraphInfo.network_registered_at`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.network_registered_at>)
      * [`MetagraphInfo.num_uids`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.num_uids>)
      * [`MetagraphInfo.owner_coldkey`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.owner_coldkey>)
      * [`MetagraphInfo.owner_hotkey`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.owner_hotkey>)
      * [`MetagraphInfo.pending_alpha_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.pending_alpha_emission>)
      * [`MetagraphInfo.pending_root_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.pending_root_emission>)
      * [`MetagraphInfo.pow_registration_allowed`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.pow_registration_allowed>)
      * [`MetagraphInfo.pruning_score`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.pruning_score>)
      * [`MetagraphInfo.rank`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.rank>)
      * [`MetagraphInfo.registration_allowed`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.registration_allowed>)
      * [`MetagraphInfo.rho`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.rho>)
      * [`MetagraphInfo.serving_rate_limit`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.serving_rate_limit>)
      * [`MetagraphInfo.subnet_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.subnet_emission>)
      * [`MetagraphInfo.subnet_volume`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.subnet_volume>)
      * [`MetagraphInfo.symbol`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.symbol>)
      * [`MetagraphInfo.tao_dividends_per_hotkey`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.tao_dividends_per_hotkey>)
      * [`MetagraphInfo.tao_in`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.tao_in>)
      * [`MetagraphInfo.tao_in_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.tao_in_emission>)
      * [`MetagraphInfo.tao_stake`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.tao_stake>)
      * [`MetagraphInfo.target_regs_per_interval`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.target_regs_per_interval>)
      * [`MetagraphInfo.tempo`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.tempo>)
      * [`MetagraphInfo.total_stake`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.total_stake>)
      * [`MetagraphInfo.trust`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.trust>)
      * [`MetagraphInfo.validator_permit`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.validator_permit>)
      * [`MetagraphInfo.validators`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.validators>)
      * [`MetagraphInfo.weights_rate_limit`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.weights_rate_limit>)
      * [`MetagraphInfo.weights_version`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfo.weights_version>)
    * [`MetagraphInfoEmissions`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions>)
      * [`MetagraphInfoEmissions.alpha_in_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions.alpha_in_emission>)
      * [`MetagraphInfoEmissions.alpha_out_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions.alpha_out_emission>)
      * [`MetagraphInfoEmissions.pending_alpha_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions.pending_alpha_emission>)
      * [`MetagraphInfoEmissions.pending_root_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions.pending_root_emission>)
      * [`MetagraphInfoEmissions.subnet_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions.subnet_emission>)
      * [`MetagraphInfoEmissions.tao_in_emission`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoEmissions.tao_in_emission>)
    * [`MetagraphInfoParams`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams>)
      * [`MetagraphInfoParams.activity_cutoff`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.activity_cutoff>)
      * [`MetagraphInfoParams.adjustment_alpha`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.adjustment_alpha>)
      * [`MetagraphInfoParams.adjustment_interval`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.adjustment_interval>)
      * [`MetagraphInfoParams.alpha_high`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.alpha_high>)
      * [`MetagraphInfoParams.alpha_low`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.alpha_low>)
      * [`MetagraphInfoParams.bonds_moving_avg`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.bonds_moving_avg>)
      * [`MetagraphInfoParams.burn`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.burn>)
      * [`MetagraphInfoParams.commit_reveal_period`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.commit_reveal_period>)
      * [`MetagraphInfoParams.commit_reveal_weights_enabled`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.commit_reveal_weights_enabled>)
      * [`MetagraphInfoParams.difficulty`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.difficulty>)
      * [`MetagraphInfoParams.immunity_period`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.immunity_period>)
      * [`MetagraphInfoParams.kappa`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.kappa>)
      * [`MetagraphInfoParams.liquid_alpha_enabled`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.liquid_alpha_enabled>)
      * [`MetagraphInfoParams.max_burn`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.max_burn>)
      * [`MetagraphInfoParams.max_difficulty`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.max_difficulty>)
      * [`MetagraphInfoParams.max_regs_per_block`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.max_regs_per_block>)
      * [`MetagraphInfoParams.max_validators`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.max_validators>)
      * [`MetagraphInfoParams.max_weights_limit`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.max_weights_limit>)
      * [`MetagraphInfoParams.min_allowed_weights`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.min_allowed_weights>)
      * [`MetagraphInfoParams.min_burn`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.min_burn>)
      * [`MetagraphInfoParams.min_difficulty`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.min_difficulty>)
      * [`MetagraphInfoParams.pow_registration_allowed`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.pow_registration_allowed>)
      * [`MetagraphInfoParams.registration_allowed`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.registration_allowed>)
      * [`MetagraphInfoParams.rho`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.rho>)
      * [`MetagraphInfoParams.serving_rate_limit`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.serving_rate_limit>)
      * [`MetagraphInfoParams.target_regs_per_interval`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.target_regs_per_interval>)
      * [`MetagraphInfoParams.tempo`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.tempo>)
      * [`MetagraphInfoParams.weights_rate_limit`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.weights_rate_limit>)
      * [`MetagraphInfoParams.weights_version`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoParams.weights_version>)
    * [`MetagraphInfoPool`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoPool>)
      * [`MetagraphInfoPool.alpha_in`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoPool.alpha_in>)
      * [`MetagraphInfoPool.alpha_out`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoPool.alpha_out>)
      * [`MetagraphInfoPool.moving_price`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoPool.moving_price>)
      * [`MetagraphInfoPool.subnet_volume`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoPool.subnet_volume>)
      * [`MetagraphInfoPool.tao_in`](<#bittensor.core.chain_data.metagraph_info.MetagraphInfoPool.tao_in>)
    * [`SELECTIVE_METAGRAPH_COMMITMENTS_OFFSET`](<#bittensor.core.chain_data.metagraph_info.SELECTIVE_METAGRAPH_COMMITMENTS_OFFSET>)
    * [`SelectiveMetagraphIndex`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex>)
      * [`SelectiveMetagraphIndex.Active`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Active>)
      * [`SelectiveMetagraphIndex.ActivityCutoff`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.ActivityCutoff>)
      * [`SelectiveMetagraphIndex.AdjustmentAlpha`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AdjustmentAlpha>)
      * [`SelectiveMetagraphIndex.AdjustmentInterval`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AdjustmentInterval>)
      * [`SelectiveMetagraphIndex.AlphaDividendsPerHotkey`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaDividendsPerHotkey>)
      * [`SelectiveMetagraphIndex.AlphaHigh`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaHigh>)
      * [`SelectiveMetagraphIndex.AlphaIn`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaIn>)
      * [`SelectiveMetagraphIndex.AlphaInEmission`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaInEmission>)
      * [`SelectiveMetagraphIndex.AlphaLow`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaLow>)
      * [`SelectiveMetagraphIndex.AlphaOut`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaOut>)
      * [`SelectiveMetagraphIndex.AlphaOutEmission`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaOutEmission>)
      * [`SelectiveMetagraphIndex.AlphaStake`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.AlphaStake>)
      * [`SelectiveMetagraphIndex.Axons`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Axons>)
      * [`SelectiveMetagraphIndex.Block`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Block>)
      * [`SelectiveMetagraphIndex.BlockAtRegistration`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.BlockAtRegistration>)
      * [`SelectiveMetagraphIndex.BlocksSinceLastStep`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.BlocksSinceLastStep>)
      * [`SelectiveMetagraphIndex.BondsMovingAvg`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.BondsMovingAvg>)
      * [`SelectiveMetagraphIndex.Burn`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Burn>)
      * [`SelectiveMetagraphIndex.Coldkeys`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Coldkeys>)
      * [`SelectiveMetagraphIndex.CommitRevealPeriod`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.CommitRevealPeriod>)
      * [`SelectiveMetagraphIndex.CommitRevealWeightsEnabled`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.CommitRevealWeightsEnabled>)
      * [`SelectiveMetagraphIndex.Commitments`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Commitments>)
      * [`SelectiveMetagraphIndex.Consensus`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Consensus>)
      * [`SelectiveMetagraphIndex.Difficulty`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Difficulty>)
      * [`SelectiveMetagraphIndex.Dividends`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Dividends>)
      * [`SelectiveMetagraphIndex.Emission`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Emission>)
      * [`SelectiveMetagraphIndex.Hotkeys`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Hotkeys>)
      * [`SelectiveMetagraphIndex.Identities`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Identities>)
      * [`SelectiveMetagraphIndex.Identity`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Identity>)
      * [`SelectiveMetagraphIndex.ImmunityPeriod`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.ImmunityPeriod>)
      * [`SelectiveMetagraphIndex.Incentives`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Incentives>)
      * [`SelectiveMetagraphIndex.Kappa`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Kappa>)
      * [`SelectiveMetagraphIndex.LastStep`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.LastStep>)
      * [`SelectiveMetagraphIndex.LastUpdate`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.LastUpdate>)
      * [`SelectiveMetagraphIndex.LiquidAlphaEnabled`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.LiquidAlphaEnabled>)
      * [`SelectiveMetagraphIndex.MaxBurn`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MaxBurn>)
      * [`SelectiveMetagraphIndex.MaxDifficulty`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MaxDifficulty>)
      * [`SelectiveMetagraphIndex.MaxRegsPerBlock`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MaxRegsPerBlock>)
      * [`SelectiveMetagraphIndex.MaxUids`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MaxUids>)
      * [`SelectiveMetagraphIndex.MaxValidators`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MaxValidators>)
      * [`SelectiveMetagraphIndex.MaxWeightsLimit`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MaxWeightsLimit>)
      * [`SelectiveMetagraphIndex.MinAllowedWeights`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MinAllowedWeights>)
      * [`SelectiveMetagraphIndex.MinBurn`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MinBurn>)
      * [`SelectiveMetagraphIndex.MinDifficulty`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MinDifficulty>)
      * [`SelectiveMetagraphIndex.MovingPrice`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.MovingPrice>)
      * [`SelectiveMetagraphIndex.Name`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Name>)
      * [`SelectiveMetagraphIndex.Netuid`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Netuid>)
      * [`SelectiveMetagraphIndex.NetworkRegisteredAt`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.NetworkRegisteredAt>)
      * [`SelectiveMetagraphIndex.NumUids`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.NumUids>)
      * [`SelectiveMetagraphIndex.OwnerColdkey`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.OwnerColdkey>)
      * [`SelectiveMetagraphIndex.OwnerHotkey`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.OwnerHotkey>)
      * [`SelectiveMetagraphIndex.PendingAlphaEmission`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.PendingAlphaEmission>)
      * [`SelectiveMetagraphIndex.PendingRootEmission`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.PendingRootEmission>)
      * [`SelectiveMetagraphIndex.PowRegistrationAllowed`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.PowRegistrationAllowed>)
      * [`SelectiveMetagraphIndex.PruningScore`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.PruningScore>)
      * [`SelectiveMetagraphIndex.Rank`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Rank>)
      * [`SelectiveMetagraphIndex.RegistrationAllowed`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.RegistrationAllowed>)
      * [`SelectiveMetagraphIndex.Rho`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Rho>)
      * [`SelectiveMetagraphIndex.ServingRateLimit`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.ServingRateLimit>)
      * [`SelectiveMetagraphIndex.SubnetEmission`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.SubnetEmission>)
      * [`SelectiveMetagraphIndex.SubnetVolume`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.SubnetVolume>)
      * [`SelectiveMetagraphIndex.Symbol`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Symbol>)
      * [`SelectiveMetagraphIndex.TaoDividendsPerHotkey`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.TaoDividendsPerHotkey>)
      * [`SelectiveMetagraphIndex.TaoIn`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.TaoIn>)
      * [`SelectiveMetagraphIndex.TaoInEmission`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.TaoInEmission>)
      * [`SelectiveMetagraphIndex.TaoStake`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.TaoStake>)
      * [`SelectiveMetagraphIndex.TargetRegsPerInterval`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.TargetRegsPerInterval>)
      * [`SelectiveMetagraphIndex.Tempo`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Tempo>)
      * [`SelectiveMetagraphIndex.TotalStake`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.TotalStake>)
      * [`SelectiveMetagraphIndex.Trust`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Trust>)
      * [`SelectiveMetagraphIndex.ValidatorPermit`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.ValidatorPermit>)
      * [`SelectiveMetagraphIndex.Validators`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.Validators>)
      * [`SelectiveMetagraphIndex.WeightsRateLimit`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.WeightsRateLimit>)
      * [`SelectiveMetagraphIndex.WeightsVersion`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.WeightsVersion>)
      * [`SelectiveMetagraphIndex.all_indices()`](<#bittensor.core.chain_data.metagraph_info.SelectiveMetagraphIndex.all_indices>)
    * [`get_selective_metagraph_commitments()`](<#bittensor.core.chain_data.metagraph_info.get_selective_metagraph_commitments>)
    * [`process_nested()`](<#bittensor.core.chain_data.metagraph_info.process_nested>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.