# bittensor.extras.dev_framework.calls.sudo_calls &#8212; Bittensor SDK Docs  documentation

[Skip to main content](<#main-content>)

__Back to top __ `Ctrl`+`K`

[ ![Bittensor SDK Docs  documentation - Home](../../../../../../_static/logo.svg) ![Bittensor SDK Docs  documentation - Home](../../../../../../_static/logo-dark-mode.svg) ](<../../../../../../index.html>)

__ Search `Ctrl`+`K`

Table of Contents

  * [API Reference](<../../../../../index.html>) __
    * [bittensor](<../../../../index.html>) __
      * [bittensor.core](<../../../../core/index.html>) __
        * [bittensor.core.async_subtensor](<../../../../core/async_subtensor/index.html>)
        * [bittensor.core.axon](<../../../../core/axon/index.html>)
        * [bittensor.core.chain_data](<../../../../core/chain_data/index.html>)
        * [bittensor.core.config](<../../../../core/config/index.html>)
        * [bittensor.core.dendrite](<../../../../core/dendrite/index.html>)
        * [bittensor.core.errors](<../../../../core/errors/index.html>)
        * [bittensor.core.extrinsics](<../../../../core/extrinsics/index.html>)
        * [bittensor.core.metagraph](<../../../../core/metagraph/index.html>)
        * [bittensor.core.settings](<../../../../core/settings/index.html>)
        * [bittensor.core.stream](<../../../../core/stream/index.html>)
        * [bittensor.core.subtensor](<../../../../core/subtensor/index.html>)
        * [bittensor.core.synapse](<../../../../core/synapse/index.html>)
        * [bittensor.core.tensor](<../../../../core/tensor/index.html>)
        * [bittensor.core.threadpool](<../../../../core/threadpool/index.html>)
        * [bittensor.core.types](<../../../../core/types/index.html>)
      * [bittensor.extras](<../../../index.html>) __
        * [bittensor.extras.dev_framework](<../../index.html>)
        * [bittensor.extras.subtensor_api](<../../../subtensor_api/index.html>)
        * [bittensor.extras.timelock](<../../../timelock/index.html>)
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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/extras/dev_framework/calls/sudo_calls/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/extras/dev_framework/calls/sudo_calls/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../../_sources/autoapi/bittensor/extras/dev_framework/calls/sudo_calls/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.extras.dev_framework.calls.sudo_calls

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`SUDO_AS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS>)
      * [`SUDO_AS.call`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS.call>)
      * [`SUDO_AS.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS.pallet>)
      * [`SUDO_AS.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS.sudo>)
      * [`SUDO_AS.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS.wallet>)
      * [`SUDO_AS.who`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS.who>)
    * [`SUDO_SET_ACTIVITY_CUTOFF`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF>)
      * [`SUDO_SET_ACTIVITY_CUTOFF.activity_cutoff`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF.activity_cutoff>)
      * [`SUDO_SET_ACTIVITY_CUTOFF.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF.netuid>)
      * [`SUDO_SET_ACTIVITY_CUTOFF.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF.pallet>)
      * [`SUDO_SET_ACTIVITY_CUTOFF.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF.sudo>)
      * [`SUDO_SET_ACTIVITY_CUTOFF.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF.wallet>)
    * [`SUDO_SET_ADJUSTMENT_ALPHA`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA>)
      * [`SUDO_SET_ADJUSTMENT_ALPHA.adjustment_alpha`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA.adjustment_alpha>)
      * [`SUDO_SET_ADJUSTMENT_ALPHA.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA.netuid>)
      * [`SUDO_SET_ADJUSTMENT_ALPHA.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA.pallet>)
      * [`SUDO_SET_ADJUSTMENT_ALPHA.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA.sudo>)
      * [`SUDO_SET_ADJUSTMENT_ALPHA.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA.wallet>)
    * [`SUDO_SET_ADJUSTMENT_INTERVAL`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL>)
      * [`SUDO_SET_ADJUSTMENT_INTERVAL.adjustment_interval`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL.adjustment_interval>)
      * [`SUDO_SET_ADJUSTMENT_INTERVAL.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL.netuid>)
      * [`SUDO_SET_ADJUSTMENT_INTERVAL.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL.pallet>)
      * [`SUDO_SET_ADJUSTMENT_INTERVAL.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL.sudo>)
      * [`SUDO_SET_ADJUSTMENT_INTERVAL.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL.wallet>)
    * [`SUDO_SET_ADMIN_FREEZE_WINDOW`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADMIN_FREEZE_WINDOW>)
      * [`SUDO_SET_ADMIN_FREEZE_WINDOW.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADMIN_FREEZE_WINDOW.pallet>)
      * [`SUDO_SET_ADMIN_FREEZE_WINDOW.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADMIN_FREEZE_WINDOW.sudo>)
      * [`SUDO_SET_ADMIN_FREEZE_WINDOW.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADMIN_FREEZE_WINDOW.wallet>)
      * [`SUDO_SET_ADMIN_FREEZE_WINDOW.window`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADMIN_FREEZE_WINDOW.window>)
    * [`SUDO_SET_ALPHA_SIGMOID_STEEPNESS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS>)
      * [`SUDO_SET_ALPHA_SIGMOID_STEEPNESS.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS.netuid>)
      * [`SUDO_SET_ALPHA_SIGMOID_STEEPNESS.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS.pallet>)
      * [`SUDO_SET_ALPHA_SIGMOID_STEEPNESS.steepness`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS.steepness>)
      * [`SUDO_SET_ALPHA_SIGMOID_STEEPNESS.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS.sudo>)
      * [`SUDO_SET_ALPHA_SIGMOID_STEEPNESS.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS.wallet>)
    * [`SUDO_SET_ALPHA_VALUES`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES>)
      * [`SUDO_SET_ALPHA_VALUES.alpha_high`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES.alpha_high>)
      * [`SUDO_SET_ALPHA_VALUES.alpha_low`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES.alpha_low>)
      * [`SUDO_SET_ALPHA_VALUES.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES.netuid>)
      * [`SUDO_SET_ALPHA_VALUES.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES.pallet>)
      * [`SUDO_SET_ALPHA_VALUES.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES.sudo>)
      * [`SUDO_SET_ALPHA_VALUES.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES.wallet>)
    * [`SUDO_SET_BONDS_MOVING_AVERAGE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE>)
      * [`SUDO_SET_BONDS_MOVING_AVERAGE.bonds_moving_average`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE.bonds_moving_average>)
      * [`SUDO_SET_BONDS_MOVING_AVERAGE.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE.netuid>)
      * [`SUDO_SET_BONDS_MOVING_AVERAGE.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE.pallet>)
      * [`SUDO_SET_BONDS_MOVING_AVERAGE.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE.sudo>)
      * [`SUDO_SET_BONDS_MOVING_AVERAGE.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE.wallet>)
    * [`SUDO_SET_BONDS_PENALTY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY>)
      * [`SUDO_SET_BONDS_PENALTY.bonds_penalty`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY.bonds_penalty>)
      * [`SUDO_SET_BONDS_PENALTY.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY.netuid>)
      * [`SUDO_SET_BONDS_PENALTY.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY.pallet>)
      * [`SUDO_SET_BONDS_PENALTY.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY.sudo>)
      * [`SUDO_SET_BONDS_PENALTY.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY.wallet>)
    * [`SUDO_SET_BONDS_RESET_ENABLED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED>)
      * [`SUDO_SET_BONDS_RESET_ENABLED.enabled`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED.enabled>)
      * [`SUDO_SET_BONDS_RESET_ENABLED.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED.netuid>)
      * [`SUDO_SET_BONDS_RESET_ENABLED.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED.pallet>)
      * [`SUDO_SET_BONDS_RESET_ENABLED.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED.sudo>)
      * [`SUDO_SET_BONDS_RESET_ENABLED.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED.wallet>)
    * [`SUDO_SET_BURN_HALF_LIFE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE>)
      * [`SUDO_SET_BURN_HALF_LIFE.burn_half_life`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE.burn_half_life>)
      * [`SUDO_SET_BURN_HALF_LIFE.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE.netuid>)
      * [`SUDO_SET_BURN_HALF_LIFE.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE.pallet>)
      * [`SUDO_SET_BURN_HALF_LIFE.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE.sudo>)
      * [`SUDO_SET_BURN_HALF_LIFE.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE.wallet>)
    * [`SUDO_SET_BURN_INCREASE_MULT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT>)
      * [`SUDO_SET_BURN_INCREASE_MULT.burn_increase_mult`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT.burn_increase_mult>)
      * [`SUDO_SET_BURN_INCREASE_MULT.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT.netuid>)
      * [`SUDO_SET_BURN_INCREASE_MULT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT.pallet>)
      * [`SUDO_SET_BURN_INCREASE_MULT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT.sudo>)
      * [`SUDO_SET_BURN_INCREASE_MULT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT.wallet>)
    * [`SUDO_SET_CK_BURN`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_CK_BURN>)
      * [`SUDO_SET_CK_BURN.burn`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_CK_BURN.burn>)
      * [`SUDO_SET_CK_BURN.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_CK_BURN.pallet>)
      * [`SUDO_SET_CK_BURN.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_CK_BURN.sudo>)
      * [`SUDO_SET_CK_BURN.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_CK_BURN.wallet>)
    * [`SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY>)
      * [`SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY.duration`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY.duration>)
      * [`SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY.pallet>)
      * [`SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY.sudo>)
      * [`SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY.wallet>)
    * [`SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY>)
      * [`SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY.duration`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY.duration>)
      * [`SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY.pallet>)
      * [`SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY.sudo>)
      * [`SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY.wallet>)
    * [`SUDO_SET_COMMIT_REVEAL_VERSION`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_VERSION>)
      * [`SUDO_SET_COMMIT_REVEAL_VERSION.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_VERSION.pallet>)
      * [`SUDO_SET_COMMIT_REVEAL_VERSION.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_VERSION.sudo>)
      * [`SUDO_SET_COMMIT_REVEAL_VERSION.version`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_VERSION.version>)
      * [`SUDO_SET_COMMIT_REVEAL_VERSION.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_VERSION.wallet>)
    * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED>)
      * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.enabled`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.enabled>)
      * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.netuid>)
      * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.pallet>)
      * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.sudo>)
      * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.wallet>)
    * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL>)
      * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.interval`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.interval>)
      * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.netuid>)
      * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.pallet>)
      * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.sudo>)
      * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.wallet>)
    * [`SUDO_SET_DEFAULT_TAKE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DEFAULT_TAKE>)
      * [`SUDO_SET_DEFAULT_TAKE.default_take`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DEFAULT_TAKE.default_take>)
      * [`SUDO_SET_DEFAULT_TAKE.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DEFAULT_TAKE.pallet>)
      * [`SUDO_SET_DEFAULT_TAKE.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DEFAULT_TAKE.sudo>)
      * [`SUDO_SET_DEFAULT_TAKE.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DEFAULT_TAKE.wallet>)
    * [`SUDO_SET_DIFFICULTY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY>)
      * [`SUDO_SET_DIFFICULTY.difficulty`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY.difficulty>)
      * [`SUDO_SET_DIFFICULTY.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY.netuid>)
      * [`SUDO_SET_DIFFICULTY.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY.pallet>)
      * [`SUDO_SET_DIFFICULTY.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY.sudo>)
      * [`SUDO_SET_DIFFICULTY.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY.wallet>)
    * [`SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION>)
      * [`SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION.duration`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION.duration>)
      * [`SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION.pallet>)
      * [`SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION.sudo>)
      * [`SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION.wallet>)
    * [`SUDO_SET_EMA_PRICE_HALVING_PERIOD`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD>)
      * [`SUDO_SET_EMA_PRICE_HALVING_PERIOD.ema_halving`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD.ema_halving>)
      * [`SUDO_SET_EMA_PRICE_HALVING_PERIOD.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD.netuid>)
      * [`SUDO_SET_EMA_PRICE_HALVING_PERIOD.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD.pallet>)
      * [`SUDO_SET_EMA_PRICE_HALVING_PERIOD.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD.sudo>)
      * [`SUDO_SET_EMA_PRICE_HALVING_PERIOD.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD.wallet>)
    * [`SUDO_SET_EVM_CHAIN_ID`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EVM_CHAIN_ID>)
      * [`SUDO_SET_EVM_CHAIN_ID.chain_id`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EVM_CHAIN_ID.chain_id>)
      * [`SUDO_SET_EVM_CHAIN_ID.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EVM_CHAIN_ID.pallet>)
      * [`SUDO_SET_EVM_CHAIN_ID.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EVM_CHAIN_ID.sudo>)
      * [`SUDO_SET_EVM_CHAIN_ID.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EVM_CHAIN_ID.wallet>)
    * [`SUDO_SET_IMMUNITY_PERIOD`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD>)
      * [`SUDO_SET_IMMUNITY_PERIOD.immunity_period`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD.immunity_period>)
      * [`SUDO_SET_IMMUNITY_PERIOD.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD.netuid>)
      * [`SUDO_SET_IMMUNITY_PERIOD.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD.pallet>)
      * [`SUDO_SET_IMMUNITY_PERIOD.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD.sudo>)
      * [`SUDO_SET_IMMUNITY_PERIOD.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD.wallet>)
    * [`SUDO_SET_KAPPA`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA>)
      * [`SUDO_SET_KAPPA.kappa`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA.kappa>)
      * [`SUDO_SET_KAPPA.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA.netuid>)
      * [`SUDO_SET_KAPPA.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA.pallet>)
      * [`SUDO_SET_KAPPA.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA.sudo>)
      * [`SUDO_SET_KAPPA.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA.wallet>)
    * [`SUDO_SET_LIQUID_ALPHA_ENABLED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED>)
      * [`SUDO_SET_LIQUID_ALPHA_ENABLED.enabled`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED.enabled>)
      * [`SUDO_SET_LIQUID_ALPHA_ENABLED.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED.netuid>)
      * [`SUDO_SET_LIQUID_ALPHA_ENABLED.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED.pallet>)
      * [`SUDO_SET_LIQUID_ALPHA_ENABLED.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED.sudo>)
      * [`SUDO_SET_LIQUID_ALPHA_ENABLED.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED.wallet>)
    * [`SUDO_SET_LOCK_REDUCTION_INTERVAL`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LOCK_REDUCTION_INTERVAL>)
      * [`SUDO_SET_LOCK_REDUCTION_INTERVAL.interval`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LOCK_REDUCTION_INTERVAL.interval>)
      * [`SUDO_SET_LOCK_REDUCTION_INTERVAL.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LOCK_REDUCTION_INTERVAL.pallet>)
      * [`SUDO_SET_LOCK_REDUCTION_INTERVAL.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LOCK_REDUCTION_INTERVAL.sudo>)
      * [`SUDO_SET_LOCK_REDUCTION_INTERVAL.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LOCK_REDUCTION_INTERVAL.wallet>)
    * [`SUDO_SET_MAX_ALLOWED_UIDS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS>)
      * [`SUDO_SET_MAX_ALLOWED_UIDS.max_allowed_uids`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS.max_allowed_uids>)
      * [`SUDO_SET_MAX_ALLOWED_UIDS.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS.netuid>)
      * [`SUDO_SET_MAX_ALLOWED_UIDS.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS.pallet>)
      * [`SUDO_SET_MAX_ALLOWED_UIDS.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS.sudo>)
      * [`SUDO_SET_MAX_ALLOWED_UIDS.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS.wallet>)
    * [`SUDO_SET_MAX_ALLOWED_VALIDATORS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS>)
      * [`SUDO_SET_MAX_ALLOWED_VALIDATORS.max_allowed_validators`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS.max_allowed_validators>)
      * [`SUDO_SET_MAX_ALLOWED_VALIDATORS.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS.netuid>)
      * [`SUDO_SET_MAX_ALLOWED_VALIDATORS.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS.pallet>)
      * [`SUDO_SET_MAX_ALLOWED_VALIDATORS.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS.sudo>)
      * [`SUDO_SET_MAX_ALLOWED_VALIDATORS.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS.wallet>)
    * [`SUDO_SET_MAX_BURN`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN>)
      * [`SUDO_SET_MAX_BURN.max_burn`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN.max_burn>)
      * [`SUDO_SET_MAX_BURN.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN.netuid>)
      * [`SUDO_SET_MAX_BURN.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN.pallet>)
      * [`SUDO_SET_MAX_BURN.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN.sudo>)
      * [`SUDO_SET_MAX_BURN.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN.wallet>)
    * [`SUDO_SET_MAX_CHILDKEY_TAKE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_CHILDKEY_TAKE>)
      * [`SUDO_SET_MAX_CHILDKEY_TAKE.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_CHILDKEY_TAKE.pallet>)
      * [`SUDO_SET_MAX_CHILDKEY_TAKE.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_CHILDKEY_TAKE.sudo>)
      * [`SUDO_SET_MAX_CHILDKEY_TAKE.take`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_CHILDKEY_TAKE.take>)
      * [`SUDO_SET_MAX_CHILDKEY_TAKE.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_CHILDKEY_TAKE.wallet>)
    * [`SUDO_SET_MAX_DIFFICULTY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY>)
      * [`SUDO_SET_MAX_DIFFICULTY.max_difficulty`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY.max_difficulty>)
      * [`SUDO_SET_MAX_DIFFICULTY.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY.netuid>)
      * [`SUDO_SET_MAX_DIFFICULTY.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY.pallet>)
      * [`SUDO_SET_MAX_DIFFICULTY.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY.sudo>)
      * [`SUDO_SET_MAX_DIFFICULTY.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY.wallet>)
    * [`SUDO_SET_MAX_MECHANISM_COUNT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_MECHANISM_COUNT>)
      * [`SUDO_SET_MAX_MECHANISM_COUNT.max_mechanism_count`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_MECHANISM_COUNT.max_mechanism_count>)
      * [`SUDO_SET_MAX_MECHANISM_COUNT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_MECHANISM_COUNT.pallet>)
      * [`SUDO_SET_MAX_MECHANISM_COUNT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_MECHANISM_COUNT.sudo>)
      * [`SUDO_SET_MAX_MECHANISM_COUNT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_MECHANISM_COUNT.wallet>)
    * [`SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK>)
      * [`SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.max_registrations_per_block`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.max_registrations_per_block>)
      * [`SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.netuid>)
      * [`SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.pallet>)
      * [`SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.sudo>)
      * [`SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.wallet>)
    * [`SUDO_SET_MECHANISM_COUNT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT>)
      * [`SUDO_SET_MECHANISM_COUNT.mechanism_count`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT.mechanism_count>)
      * [`SUDO_SET_MECHANISM_COUNT.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT.netuid>)
      * [`SUDO_SET_MECHANISM_COUNT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT.pallet>)
      * [`SUDO_SET_MECHANISM_COUNT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT.sudo>)
      * [`SUDO_SET_MECHANISM_COUNT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT.wallet>)
    * [`SUDO_SET_MECHANISM_EMISSION_SPLIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT>)
      * [`SUDO_SET_MECHANISM_EMISSION_SPLIT.maybe_split`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT.maybe_split>)
      * [`SUDO_SET_MECHANISM_EMISSION_SPLIT.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT.netuid>)
      * [`SUDO_SET_MECHANISM_EMISSION_SPLIT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT.pallet>)
      * [`SUDO_SET_MECHANISM_EMISSION_SPLIT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT.sudo>)
      * [`SUDO_SET_MECHANISM_EMISSION_SPLIT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT.wallet>)
    * [`SUDO_SET_MIN_ALLOWED_UIDS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS>)
      * [`SUDO_SET_MIN_ALLOWED_UIDS.min_allowed_uids`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS.min_allowed_uids>)
      * [`SUDO_SET_MIN_ALLOWED_UIDS.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS.netuid>)
      * [`SUDO_SET_MIN_ALLOWED_UIDS.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS.pallet>)
      * [`SUDO_SET_MIN_ALLOWED_UIDS.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS.sudo>)
      * [`SUDO_SET_MIN_ALLOWED_UIDS.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS.wallet>)
    * [`SUDO_SET_MIN_ALLOWED_WEIGHTS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS>)
      * [`SUDO_SET_MIN_ALLOWED_WEIGHTS.min_allowed_weights`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS.min_allowed_weights>)
      * [`SUDO_SET_MIN_ALLOWED_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS.netuid>)
      * [`SUDO_SET_MIN_ALLOWED_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS.pallet>)
      * [`SUDO_SET_MIN_ALLOWED_WEIGHTS.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS.sudo>)
      * [`SUDO_SET_MIN_ALLOWED_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS.wallet>)
    * [`SUDO_SET_MIN_BURN`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN>)
      * [`SUDO_SET_MIN_BURN.min_burn`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN.min_burn>)
      * [`SUDO_SET_MIN_BURN.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN.netuid>)
      * [`SUDO_SET_MIN_BURN.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN.pallet>)
      * [`SUDO_SET_MIN_BURN.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN.sudo>)
      * [`SUDO_SET_MIN_BURN.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN.wallet>)
    * [`SUDO_SET_MIN_CHILDKEY_TAKE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_CHILDKEY_TAKE>)
      * [`SUDO_SET_MIN_CHILDKEY_TAKE.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_CHILDKEY_TAKE.pallet>)
      * [`SUDO_SET_MIN_CHILDKEY_TAKE.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_CHILDKEY_TAKE.sudo>)
      * [`SUDO_SET_MIN_CHILDKEY_TAKE.take`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_CHILDKEY_TAKE.take>)
      * [`SUDO_SET_MIN_CHILDKEY_TAKE.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_CHILDKEY_TAKE.wallet>)
    * [`SUDO_SET_MIN_DELEGATE_TAKE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DELEGATE_TAKE>)
      * [`SUDO_SET_MIN_DELEGATE_TAKE.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DELEGATE_TAKE.pallet>)
      * [`SUDO_SET_MIN_DELEGATE_TAKE.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DELEGATE_TAKE.sudo>)
      * [`SUDO_SET_MIN_DELEGATE_TAKE.take`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DELEGATE_TAKE.take>)
      * [`SUDO_SET_MIN_DELEGATE_TAKE.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DELEGATE_TAKE.wallet>)
    * [`SUDO_SET_MIN_DIFFICULTY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY>)
      * [`SUDO_SET_MIN_DIFFICULTY.min_difficulty`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY.min_difficulty>)
      * [`SUDO_SET_MIN_DIFFICULTY.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY.netuid>)
      * [`SUDO_SET_MIN_DIFFICULTY.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY.pallet>)
      * [`SUDO_SET_MIN_DIFFICULTY.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY.sudo>)
      * [`SUDO_SET_MIN_DIFFICULTY.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY.wallet>)
    * [`SUDO_SET_MIN_NON_IMMUNE_UIDS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS>)
      * [`SUDO_SET_MIN_NON_IMMUNE_UIDS.min`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS.min>)
      * [`SUDO_SET_MIN_NON_IMMUNE_UIDS.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS.netuid>)
      * [`SUDO_SET_MIN_NON_IMMUNE_UIDS.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS.pallet>)
      * [`SUDO_SET_MIN_NON_IMMUNE_UIDS.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS.sudo>)
      * [`SUDO_SET_MIN_NON_IMMUNE_UIDS.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS.wallet>)
    * [`SUDO_SET_NETWORK_IMMUNITY_PERIOD`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_IMMUNITY_PERIOD>)
      * [`SUDO_SET_NETWORK_IMMUNITY_PERIOD.immunity_period`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_IMMUNITY_PERIOD.immunity_period>)
      * [`SUDO_SET_NETWORK_IMMUNITY_PERIOD.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_IMMUNITY_PERIOD.pallet>)
      * [`SUDO_SET_NETWORK_IMMUNITY_PERIOD.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_IMMUNITY_PERIOD.sudo>)
      * [`SUDO_SET_NETWORK_IMMUNITY_PERIOD.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_IMMUNITY_PERIOD.wallet>)
    * [`SUDO_SET_NETWORK_MIN_LOCK_COST`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_MIN_LOCK_COST>)
      * [`SUDO_SET_NETWORK_MIN_LOCK_COST.lock_cost`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_MIN_LOCK_COST.lock_cost>)
      * [`SUDO_SET_NETWORK_MIN_LOCK_COST.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_MIN_LOCK_COST.pallet>)
      * [`SUDO_SET_NETWORK_MIN_LOCK_COST.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_MIN_LOCK_COST.sudo>)
      * [`SUDO_SET_NETWORK_MIN_LOCK_COST.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_MIN_LOCK_COST.wallet>)
    * [`SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED>)
      * [`SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.netuid>)
      * [`SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.pallet>)
      * [`SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.registration_allowed`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.registration_allowed>)
      * [`SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.sudo>)
      * [`SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.wallet>)
    * [`SUDO_SET_NETWORK_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_RATE_LIMIT>)
      * [`SUDO_SET_NETWORK_RATE_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_RATE_LIMIT.pallet>)
      * [`SUDO_SET_NETWORK_RATE_LIMIT.rate_limit`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_RATE_LIMIT.rate_limit>)
      * [`SUDO_SET_NETWORK_RATE_LIMIT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_RATE_LIMIT.sudo>)
      * [`SUDO_SET_NETWORK_RATE_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_RATE_LIMIT.wallet>)
    * [`SUDO_SET_NETWORK_REGISTRATION_ALLOWED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED>)
      * [`SUDO_SET_NETWORK_REGISTRATION_ALLOWED.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED.netuid>)
      * [`SUDO_SET_NETWORK_REGISTRATION_ALLOWED.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED.pallet>)
      * [`SUDO_SET_NETWORK_REGISTRATION_ALLOWED.registration_allowed`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED.registration_allowed>)
      * [`SUDO_SET_NETWORK_REGISTRATION_ALLOWED.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED.sudo>)
      * [`SUDO_SET_NETWORK_REGISTRATION_ALLOWED.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED.wallet>)
    * [`SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE>)
      * [`SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE.min_stake`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE.min_stake>)
      * [`SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE.pallet>)
      * [`SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE.sudo>)
      * [`SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE.wallet>)
    * [`SUDO_SET_NUM_ROOT_CLAIMS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NUM_ROOT_CLAIMS>)
      * [`SUDO_SET_NUM_ROOT_CLAIMS.new_value`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NUM_ROOT_CLAIMS.new_value>)
      * [`SUDO_SET_NUM_ROOT_CLAIMS.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NUM_ROOT_CLAIMS.pallet>)
      * [`SUDO_SET_NUM_ROOT_CLAIMS.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NUM_ROOT_CLAIMS.sudo>)
      * [`SUDO_SET_NUM_ROOT_CLAIMS.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NUM_ROOT_CLAIMS.wallet>)
    * [`SUDO_SET_OWNER_HPARAM_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_HPARAM_RATE_LIMIT>)
      * [`SUDO_SET_OWNER_HPARAM_RATE_LIMIT.epochs`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_HPARAM_RATE_LIMIT.epochs>)
      * [`SUDO_SET_OWNER_HPARAM_RATE_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_HPARAM_RATE_LIMIT.pallet>)
      * [`SUDO_SET_OWNER_HPARAM_RATE_LIMIT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_HPARAM_RATE_LIMIT.sudo>)
      * [`SUDO_SET_OWNER_HPARAM_RATE_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_HPARAM_RATE_LIMIT.wallet>)
    * [`SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT>)
      * [`SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.immune_neurons`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.immune_neurons>)
      * [`SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.netuid>)
      * [`SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.pallet>)
      * [`SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.sudo>)
      * [`SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.wallet>)
    * [`SUDO_SET_RAO_RECYCLED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED>)
      * [`SUDO_SET_RAO_RECYCLED.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED.netuid>)
      * [`SUDO_SET_RAO_RECYCLED.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED.pallet>)
      * [`SUDO_SET_RAO_RECYCLED.rao_recycled`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED.rao_recycled>)
      * [`SUDO_SET_RAO_RECYCLED.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED.sudo>)
      * [`SUDO_SET_RAO_RECYCLED.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED.wallet>)
    * [`SUDO_SET_RECYCLE_OR_BURN`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN>)
      * [`SUDO_SET_RECYCLE_OR_BURN.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN.netuid>)
      * [`SUDO_SET_RECYCLE_OR_BURN.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN.pallet>)
      * [`SUDO_SET_RECYCLE_OR_BURN.recycle_or_burn`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN.recycle_or_burn>)
      * [`SUDO_SET_RECYCLE_OR_BURN.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN.sudo>)
      * [`SUDO_SET_RECYCLE_OR_BURN.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN.wallet>)
    * [`SUDO_SET_RHO`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO>)
      * [`SUDO_SET_RHO.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO.netuid>)
      * [`SUDO_SET_RHO.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO.pallet>)
      * [`SUDO_SET_RHO.rho`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO.rho>)
      * [`SUDO_SET_RHO.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO.sudo>)
      * [`SUDO_SET_RHO.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO.wallet>)
    * [`SUDO_SET_ROOT_CLAIM_THRESHOLD`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD>)
      * [`SUDO_SET_ROOT_CLAIM_THRESHOLD.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD.netuid>)
      * [`SUDO_SET_ROOT_CLAIM_THRESHOLD.new_value`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD.new_value>)
      * [`SUDO_SET_ROOT_CLAIM_THRESHOLD.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD.pallet>)
      * [`SUDO_SET_ROOT_CLAIM_THRESHOLD.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD.sudo>)
      * [`SUDO_SET_ROOT_CLAIM_THRESHOLD.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD.wallet>)
    * [`SUDO_SET_SERVING_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT>)
      * [`SUDO_SET_SERVING_RATE_LIMIT.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT.netuid>)
      * [`SUDO_SET_SERVING_RATE_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT.pallet>)
      * [`SUDO_SET_SERVING_RATE_LIMIT.serving_rate_limit`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT.serving_rate_limit>)
      * [`SUDO_SET_SERVING_RATE_LIMIT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT.sudo>)
      * [`SUDO_SET_SERVING_RATE_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT.wallet>)
    * [`SUDO_SET_SN_OWNER_HOTKEY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY>)
      * [`SUDO_SET_SN_OWNER_HOTKEY.hotkey`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY.hotkey>)
      * [`SUDO_SET_SN_OWNER_HOTKEY.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY.netuid>)
      * [`SUDO_SET_SN_OWNER_HOTKEY.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY.pallet>)
      * [`SUDO_SET_SN_OWNER_HOTKEY.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY.sudo>)
      * [`SUDO_SET_SN_OWNER_HOTKEY.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY.wallet>)
    * [`SUDO_SET_STAKE_THRESHOLD`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_STAKE_THRESHOLD>)
      * [`SUDO_SET_STAKE_THRESHOLD.min_stake`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_STAKE_THRESHOLD.min_stake>)
      * [`SUDO_SET_STAKE_THRESHOLD.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_STAKE_THRESHOLD.pallet>)
      * [`SUDO_SET_STAKE_THRESHOLD.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_STAKE_THRESHOLD.sudo>)
      * [`SUDO_SET_STAKE_THRESHOLD.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_STAKE_THRESHOLD.wallet>)
    * [`SUDO_SET_START_CALL_DELAY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_START_CALL_DELAY>)
      * [`SUDO_SET_START_CALL_DELAY.delay`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_START_CALL_DELAY.delay>)
      * [`SUDO_SET_START_CALL_DELAY.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_START_CALL_DELAY.pallet>)
      * [`SUDO_SET_START_CALL_DELAY.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_START_CALL_DELAY.sudo>)
      * [`SUDO_SET_START_CALL_DELAY.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_START_CALL_DELAY.wallet>)
    * [`SUDO_SET_SUBNET_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_LIMIT>)
      * [`SUDO_SET_SUBNET_LIMIT.max_subnets`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_LIMIT.max_subnets>)
      * [`SUDO_SET_SUBNET_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_LIMIT.pallet>)
      * [`SUDO_SET_SUBNET_LIMIT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_LIMIT.sudo>)
      * [`SUDO_SET_SUBNET_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_LIMIT.wallet>)
    * [`SUDO_SET_SUBNET_MOVING_ALPHA`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_MOVING_ALPHA>)
      * [`SUDO_SET_SUBNET_MOVING_ALPHA.alpha`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_MOVING_ALPHA.alpha>)
      * [`SUDO_SET_SUBNET_MOVING_ALPHA.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_MOVING_ALPHA.pallet>)
      * [`SUDO_SET_SUBNET_MOVING_ALPHA.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_MOVING_ALPHA.sudo>)
      * [`SUDO_SET_SUBNET_MOVING_ALPHA.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_MOVING_ALPHA.wallet>)
    * [`SUDO_SET_SUBNET_OWNER_CUT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_CUT>)
      * [`SUDO_SET_SUBNET_OWNER_CUT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_CUT.pallet>)
      * [`SUDO_SET_SUBNET_OWNER_CUT.subnet_owner_cut`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_CUT.subnet_owner_cut>)
      * [`SUDO_SET_SUBNET_OWNER_CUT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_CUT.sudo>)
      * [`SUDO_SET_SUBNET_OWNER_CUT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_CUT.wallet>)
    * [`SUDO_SET_SUBNET_OWNER_HOTKEY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY>)
      * [`SUDO_SET_SUBNET_OWNER_HOTKEY.hotkey`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY.hotkey>)
      * [`SUDO_SET_SUBNET_OWNER_HOTKEY.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY.netuid>)
      * [`SUDO_SET_SUBNET_OWNER_HOTKEY.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY.pallet>)
      * [`SUDO_SET_SUBNET_OWNER_HOTKEY.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY.sudo>)
      * [`SUDO_SET_SUBNET_OWNER_HOTKEY.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY.wallet>)
    * [`SUDO_SET_SUBTOKEN_ENABLED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED>)
      * [`SUDO_SET_SUBTOKEN_ENABLED.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED.netuid>)
      * [`SUDO_SET_SUBTOKEN_ENABLED.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED.pallet>)
      * [`SUDO_SET_SUBTOKEN_ENABLED.subtoken_enabled`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED.subtoken_enabled>)
      * [`SUDO_SET_SUBTOKEN_ENABLED.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED.sudo>)
      * [`SUDO_SET_SUBTOKEN_ENABLED.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED.wallet>)
    * [`SUDO_SET_TAO_FLOW_CUTOFF`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_CUTOFF>)
      * [`SUDO_SET_TAO_FLOW_CUTOFF.flow_cutoff`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_CUTOFF.flow_cutoff>)
      * [`SUDO_SET_TAO_FLOW_CUTOFF.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_CUTOFF.pallet>)
      * [`SUDO_SET_TAO_FLOW_CUTOFF.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_CUTOFF.sudo>)
      * [`SUDO_SET_TAO_FLOW_CUTOFF.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_CUTOFF.wallet>)
    * [`SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT>)
      * [`SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT.exponent`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT.exponent>)
      * [`SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT.pallet>)
      * [`SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT.sudo>)
      * [`SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT.wallet>)
    * [`SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR>)
      * [`SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR.pallet>)
      * [`SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR.smoothing_factor`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR.smoothing_factor>)
      * [`SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR.sudo>)
      * [`SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR.wallet>)
    * [`SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL>)
      * [`SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.netuid>)
      * [`SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.pallet>)
      * [`SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.sudo>)
      * [`SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.target_registrations_per_interval`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.target_registrations_per_interval>)
      * [`SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.wallet>)
    * [`SUDO_SET_TEMPO`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO>)
      * [`SUDO_SET_TEMPO.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO.netuid>)
      * [`SUDO_SET_TEMPO.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO.pallet>)
      * [`SUDO_SET_TEMPO.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO.sudo>)
      * [`SUDO_SET_TEMPO.tempo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO.tempo>)
      * [`SUDO_SET_TEMPO.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO.wallet>)
    * [`SUDO_SET_TOGGLE_TRANSFER`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER>)
      * [`SUDO_SET_TOGGLE_TRANSFER.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER.netuid>)
      * [`SUDO_SET_TOGGLE_TRANSFER.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER.pallet>)
      * [`SUDO_SET_TOGGLE_TRANSFER.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER.sudo>)
      * [`SUDO_SET_TOGGLE_TRANSFER.toggle`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER.toggle>)
      * [`SUDO_SET_TOGGLE_TRANSFER.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER.wallet>)
    * [`SUDO_SET_TOTAL_ISSUANCE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOTAL_ISSUANCE>)
      * [`SUDO_SET_TOTAL_ISSUANCE.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOTAL_ISSUANCE.pallet>)
      * [`SUDO_SET_TOTAL_ISSUANCE.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOTAL_ISSUANCE.sudo>)
      * [`SUDO_SET_TOTAL_ISSUANCE.total_issuance`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOTAL_ISSUANCE.total_issuance>)
      * [`SUDO_SET_TOTAL_ISSUANCE.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOTAL_ISSUANCE.wallet>)
    * [`SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT>)
      * [`SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT.pallet>)
      * [`SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT.sudo>)
      * [`SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT.tx_rate_limit`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT.tx_rate_limit>)
      * [`SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT.wallet>)
    * [`SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT>)
      * [`SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT.pallet>)
      * [`SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT.sudo>)
      * [`SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT.tx_rate_limit`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT.tx_rate_limit>)
      * [`SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT.wallet>)
    * [`SUDO_SET_TX_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_RATE_LIMIT>)
      * [`SUDO_SET_TX_RATE_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_RATE_LIMIT.pallet>)
      * [`SUDO_SET_TX_RATE_LIMIT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_RATE_LIMIT.sudo>)
      * [`SUDO_SET_TX_RATE_LIMIT.tx_rate_limit`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_RATE_LIMIT.tx_rate_limit>)
      * [`SUDO_SET_TX_RATE_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_RATE_LIMIT.wallet>)
    * [`SUDO_SET_VOTING_POWER_EMA_ALPHA`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA>)
      * [`SUDO_SET_VOTING_POWER_EMA_ALPHA.alpha`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA.alpha>)
      * [`SUDO_SET_VOTING_POWER_EMA_ALPHA.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA.netuid>)
      * [`SUDO_SET_VOTING_POWER_EMA_ALPHA.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA.pallet>)
      * [`SUDO_SET_VOTING_POWER_EMA_ALPHA.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA.sudo>)
      * [`SUDO_SET_VOTING_POWER_EMA_ALPHA.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA.wallet>)
    * [`SUDO_SET_WEIGHTS_SET_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT>)
      * [`SUDO_SET_WEIGHTS_SET_RATE_LIMIT.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT.netuid>)
      * [`SUDO_SET_WEIGHTS_SET_RATE_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT.pallet>)
      * [`SUDO_SET_WEIGHTS_SET_RATE_LIMIT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT.sudo>)
      * [`SUDO_SET_WEIGHTS_SET_RATE_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT.wallet>)
      * [`SUDO_SET_WEIGHTS_SET_RATE_LIMIT.weights_set_rate_limit`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT.weights_set_rate_limit>)
    * [`SUDO_SET_WEIGHTS_VERSION_KEY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY>)
      * [`SUDO_SET_WEIGHTS_VERSION_KEY.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY.netuid>)
      * [`SUDO_SET_WEIGHTS_VERSION_KEY.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY.pallet>)
      * [`SUDO_SET_WEIGHTS_VERSION_KEY.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY.sudo>)
      * [`SUDO_SET_WEIGHTS_VERSION_KEY.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY.wallet>)
      * [`SUDO_SET_WEIGHTS_VERSION_KEY.weights_version_key`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY.weights_version_key>)
    * [`SUDO_SET_YUMA3_ENABLED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED>)
      * [`SUDO_SET_YUMA3_ENABLED.enabled`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED.enabled>)
      * [`SUDO_SET_YUMA3_ENABLED.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED.netuid>)
      * [`SUDO_SET_YUMA3_ENABLED.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED.pallet>)
      * [`SUDO_SET_YUMA3_ENABLED.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED.sudo>)
      * [`SUDO_SET_YUMA3_ENABLED.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED.wallet>)
    * [`SUDO_TOGGLE_EVM_PRECOMPILE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE>)
      * [`SUDO_TOGGLE_EVM_PRECOMPILE.enabled`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE.enabled>)
      * [`SUDO_TOGGLE_EVM_PRECOMPILE.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE.pallet>)
      * [`SUDO_TOGGLE_EVM_PRECOMPILE.precompile_id`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE.precompile_id>)
      * [`SUDO_TOGGLE_EVM_PRECOMPILE.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE.sudo>)
      * [`SUDO_TOGGLE_EVM_PRECOMPILE.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE.wallet>)
    * [`SUDO_TRIM_TO_MAX_ALLOWED_UIDS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS>)
      * [`SUDO_TRIM_TO_MAX_ALLOWED_UIDS.max_n`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS.max_n>)
      * [`SUDO_TRIM_TO_MAX_ALLOWED_UIDS.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS.netuid>)
      * [`SUDO_TRIM_TO_MAX_ALLOWED_UIDS.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS.pallet>)
      * [`SUDO_TRIM_TO_MAX_ALLOWED_UIDS.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS.sudo>)
      * [`SUDO_TRIM_TO_MAX_ALLOWED_UIDS.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS.wallet>)
    * [`SUDO_UNCHECKED_WEIGHT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT>)
      * [`SUDO_UNCHECKED_WEIGHT.call`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT.call>)
      * [`SUDO_UNCHECKED_WEIGHT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT.pallet>)
      * [`SUDO_UNCHECKED_WEIGHT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT.sudo>)
      * [`SUDO_UNCHECKED_WEIGHT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT.wallet>)
      * [`SUDO_UNCHECKED_WEIGHT.weight`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT.weight>)



# bittensor.extras.dev_framework.calls.sudo_calls[#](<#module-bittensor.extras.dev_framework.calls.sudo_calls> "Link to this heading")

This file is auto-generated. Do not edit manually.

For developers: \- Use the function recreate_calls_subpackage() to regenerate this file. \- The command lists are built dynamically from the current Subtensor metadata (Subtensor.substrate.metadata). \- Each command is represented as a namedtuple with fields:

>   * System arguments: wallet, pallet (and sudo for sudo calls).
> 
>   * Additional arguments: taken from the extrinsic definition (with type hints for reference).
> 
> 


  * These namedtuples are intended as convenient templates for building commands in tests and end-to-end scenarios.




Note

Any manual changes will be overwritten the next time the generator is run. Subtensor spec version: 397

## Classes[#](<#classes> "Link to this heading")

[`SUDO_AS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS") |   
---|---  
[`SUDO_SET_ACTIVITY_CUTOFF`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF") |   
[`SUDO_SET_ADJUSTMENT_ALPHA`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA") |   
[`SUDO_SET_ADJUSTMENT_INTERVAL`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL") |   
[`SUDO_SET_ADMIN_FREEZE_WINDOW`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADMIN_FREEZE_WINDOW> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADMIN_FREEZE_WINDOW") |   
[`SUDO_SET_ALPHA_SIGMOID_STEEPNESS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS") |   
[`SUDO_SET_ALPHA_VALUES`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES") |   
[`SUDO_SET_BONDS_MOVING_AVERAGE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE") |   
[`SUDO_SET_BONDS_PENALTY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY") |   
[`SUDO_SET_BONDS_RESET_ENABLED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED") |   
[`SUDO_SET_BURN_HALF_LIFE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE") |   
[`SUDO_SET_BURN_INCREASE_MULT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT") |   
[`SUDO_SET_CK_BURN`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_CK_BURN> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_CK_BURN") |   
[`SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY") |   
[`SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY") |   
[`SUDO_SET_COMMIT_REVEAL_VERSION`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_VERSION> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_VERSION") |   
[`SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED") |   
[`SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL") |   
[`SUDO_SET_DEFAULT_TAKE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DEFAULT_TAKE> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DEFAULT_TAKE") |   
[`SUDO_SET_DIFFICULTY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY") |   
[`SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION") |   
[`SUDO_SET_EMA_PRICE_HALVING_PERIOD`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD") |   
[`SUDO_SET_EVM_CHAIN_ID`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EVM_CHAIN_ID> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EVM_CHAIN_ID") |   
[`SUDO_SET_IMMUNITY_PERIOD`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD") |   
[`SUDO_SET_KAPPA`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA") |   
[`SUDO_SET_LIQUID_ALPHA_ENABLED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED") |   
[`SUDO_SET_LOCK_REDUCTION_INTERVAL`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LOCK_REDUCTION_INTERVAL> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LOCK_REDUCTION_INTERVAL") |   
[`SUDO_SET_MAX_ALLOWED_UIDS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS") |   
[`SUDO_SET_MAX_ALLOWED_VALIDATORS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS") |   
[`SUDO_SET_MAX_BURN`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN") |   
[`SUDO_SET_MAX_CHILDKEY_TAKE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_CHILDKEY_TAKE> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_CHILDKEY_TAKE") |   
[`SUDO_SET_MAX_DIFFICULTY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY") |   
[`SUDO_SET_MAX_MECHANISM_COUNT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_MECHANISM_COUNT> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_MECHANISM_COUNT") |   
[`SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK") |   
[`SUDO_SET_MECHANISM_COUNT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT") |   
[`SUDO_SET_MECHANISM_EMISSION_SPLIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT") |   
[`SUDO_SET_MIN_ALLOWED_UIDS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS") |   
[`SUDO_SET_MIN_ALLOWED_WEIGHTS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS") |   
[`SUDO_SET_MIN_BURN`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN") |   
[`SUDO_SET_MIN_CHILDKEY_TAKE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_CHILDKEY_TAKE> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_CHILDKEY_TAKE") |   
[`SUDO_SET_MIN_DELEGATE_TAKE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DELEGATE_TAKE> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DELEGATE_TAKE") |   
[`SUDO_SET_MIN_DIFFICULTY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY") |   
[`SUDO_SET_MIN_NON_IMMUNE_UIDS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS") |   
[`SUDO_SET_NETWORK_IMMUNITY_PERIOD`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_IMMUNITY_PERIOD> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_IMMUNITY_PERIOD") |   
[`SUDO_SET_NETWORK_MIN_LOCK_COST`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_MIN_LOCK_COST> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_MIN_LOCK_COST") |   
[`SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED") |   
[`SUDO_SET_NETWORK_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_RATE_LIMIT> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_RATE_LIMIT") |   
[`SUDO_SET_NETWORK_REGISTRATION_ALLOWED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED") |   
[`SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE") |   
[`SUDO_SET_NUM_ROOT_CLAIMS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NUM_ROOT_CLAIMS> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NUM_ROOT_CLAIMS") |   
[`SUDO_SET_OWNER_HPARAM_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_HPARAM_RATE_LIMIT> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_HPARAM_RATE_LIMIT") |   
[`SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT") |   
[`SUDO_SET_RAO_RECYCLED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED") |   
[`SUDO_SET_RECYCLE_OR_BURN`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN") |   
[`SUDO_SET_RHO`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO") |   
[`SUDO_SET_ROOT_CLAIM_THRESHOLD`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD") |   
[`SUDO_SET_SERVING_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT") |   
[`SUDO_SET_SN_OWNER_HOTKEY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY") |   
[`SUDO_SET_STAKE_THRESHOLD`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_STAKE_THRESHOLD> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_STAKE_THRESHOLD") |   
[`SUDO_SET_START_CALL_DELAY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_START_CALL_DELAY> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_START_CALL_DELAY") |   
[`SUDO_SET_SUBNET_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_LIMIT> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_LIMIT") |   
[`SUDO_SET_SUBNET_MOVING_ALPHA`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_MOVING_ALPHA> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_MOVING_ALPHA") |   
[`SUDO_SET_SUBNET_OWNER_CUT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_CUT> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_CUT") |   
[`SUDO_SET_SUBNET_OWNER_HOTKEY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY") |   
[`SUDO_SET_SUBTOKEN_ENABLED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED") |   
[`SUDO_SET_TAO_FLOW_CUTOFF`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_CUTOFF> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_CUTOFF") |   
[`SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT") |   
[`SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR") |   
[`SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL") |   
[`SUDO_SET_TEMPO`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO") |   
[`SUDO_SET_TOGGLE_TRANSFER`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER") |   
[`SUDO_SET_TOTAL_ISSUANCE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOTAL_ISSUANCE> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOTAL_ISSUANCE") |   
[`SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT") |   
[`SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT") |   
[`SUDO_SET_TX_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_RATE_LIMIT> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_RATE_LIMIT") |   
[`SUDO_SET_VOTING_POWER_EMA_ALPHA`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA") |   
[`SUDO_SET_WEIGHTS_SET_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT") |   
[`SUDO_SET_WEIGHTS_VERSION_KEY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY") |   
[`SUDO_SET_YUMA3_ENABLED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED") |   
[`SUDO_TOGGLE_EVM_PRECOMPILE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE") |   
[`SUDO_TRIM_TO_MAX_ALLOWED_UIDS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS") |   
[`SUDO_UNCHECKED_WEIGHT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT> "bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT") |   
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

call[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS.call> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS.wallet> "Link to this definition")
    

who[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS.who> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

activity_cutoff[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF.activity_cutoff> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

adjustment_alpha[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA.adjustment_alpha> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

adjustment_interval[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL.adjustment_interval> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADMIN_FREEZE_WINDOW[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADMIN_FREEZE_WINDOW> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADMIN_FREEZE_WINDOW.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADMIN_FREEZE_WINDOW.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADMIN_FREEZE_WINDOW.wallet> "Link to this definition")
    

window[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADMIN_FREEZE_WINDOW.window> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS.pallet> "Link to this definition")
    

steepness[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS.steepness> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

alpha_high[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES.alpha_high> "Link to this definition")
    

alpha_low[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES.alpha_low> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

bonds_moving_average[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE.bonds_moving_average> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

bonds_penalty[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY.bonds_penalty> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

enabled[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED.enabled> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

burn_half_life[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE.burn_half_life> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

burn_increase_mult[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT.burn_increase_mult> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_CK_BURN[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_CK_BURN> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

burn[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_CK_BURN.burn> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_CK_BURN.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_CK_BURN.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_CK_BURN.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

duration[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY.duration> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

duration[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY.duration> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_VERSION[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_VERSION> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_VERSION.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_VERSION.sudo> "Link to this definition")
    

version[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_VERSION.version> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_VERSION.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

enabled[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.enabled> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

interval[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.interval> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DEFAULT_TAKE[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DEFAULT_TAKE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

default_take[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DEFAULT_TAKE.default_take> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DEFAULT_TAKE.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DEFAULT_TAKE.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DEFAULT_TAKE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

difficulty[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY.difficulty> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

duration[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION.duration> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

ema_halving[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD.ema_halving> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EVM_CHAIN_ID[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EVM_CHAIN_ID> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

chain_id[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EVM_CHAIN_ID.chain_id> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EVM_CHAIN_ID.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EVM_CHAIN_ID.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EVM_CHAIN_ID.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

immunity_period[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD.immunity_period> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

kappa[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA.kappa> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

enabled[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED.enabled> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LOCK_REDUCTION_INTERVAL[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LOCK_REDUCTION_INTERVAL> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

interval[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LOCK_REDUCTION_INTERVAL.interval> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LOCK_REDUCTION_INTERVAL.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LOCK_REDUCTION_INTERVAL.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LOCK_REDUCTION_INTERVAL.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

max_allowed_uids[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS.max_allowed_uids> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

max_allowed_validators[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS.max_allowed_validators> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

max_burn[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN.max_burn> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_CHILDKEY_TAKE[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_CHILDKEY_TAKE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_CHILDKEY_TAKE.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_CHILDKEY_TAKE.sudo> "Link to this definition")
    

take[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_CHILDKEY_TAKE.take> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_CHILDKEY_TAKE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

max_difficulty[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY.max_difficulty> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_MECHANISM_COUNT[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_MECHANISM_COUNT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

max_mechanism_count[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_MECHANISM_COUNT.max_mechanism_count> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_MECHANISM_COUNT.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_MECHANISM_COUNT.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_MECHANISM_COUNT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

max_registrations_per_block[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.max_registrations_per_block> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

mechanism_count[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT.mechanism_count> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

maybe_split[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT.maybe_split> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

min_allowed_uids[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS.min_allowed_uids> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

min_allowed_weights[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS.min_allowed_weights> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

min_burn[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN.min_burn> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_CHILDKEY_TAKE[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_CHILDKEY_TAKE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_CHILDKEY_TAKE.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_CHILDKEY_TAKE.sudo> "Link to this definition")
    

take[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_CHILDKEY_TAKE.take> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_CHILDKEY_TAKE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DELEGATE_TAKE[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DELEGATE_TAKE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DELEGATE_TAKE.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DELEGATE_TAKE.sudo> "Link to this definition")
    

take[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DELEGATE_TAKE.take> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DELEGATE_TAKE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

min_difficulty[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY.min_difficulty> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

min[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS.min> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_IMMUNITY_PERIOD[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_IMMUNITY_PERIOD> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

immunity_period[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_IMMUNITY_PERIOD.immunity_period> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_IMMUNITY_PERIOD.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_IMMUNITY_PERIOD.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_IMMUNITY_PERIOD.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_MIN_LOCK_COST[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_MIN_LOCK_COST> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

lock_cost[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_MIN_LOCK_COST.lock_cost> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_MIN_LOCK_COST.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_MIN_LOCK_COST.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_MIN_LOCK_COST.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.pallet> "Link to this definition")
    

registration_allowed[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.registration_allowed> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_RATE_LIMIT[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_RATE_LIMIT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_RATE_LIMIT.pallet> "Link to this definition")
    

rate_limit[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_RATE_LIMIT.rate_limit> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_RATE_LIMIT.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_RATE_LIMIT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED.pallet> "Link to this definition")
    

registration_allowed[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED.registration_allowed> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

min_stake[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE.min_stake> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NUM_ROOT_CLAIMS[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NUM_ROOT_CLAIMS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

new_value[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NUM_ROOT_CLAIMS.new_value> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NUM_ROOT_CLAIMS.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NUM_ROOT_CLAIMS.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NUM_ROOT_CLAIMS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_HPARAM_RATE_LIMIT[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_HPARAM_RATE_LIMIT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

epochs[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_HPARAM_RATE_LIMIT.epochs> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_HPARAM_RATE_LIMIT.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_HPARAM_RATE_LIMIT.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_HPARAM_RATE_LIMIT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

immune_neurons[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.immune_neurons> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED.pallet> "Link to this definition")
    

rao_recycled[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED.rao_recycled> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN.pallet> "Link to this definition")
    

recycle_or_burn[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN.recycle_or_burn> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO.pallet> "Link to this definition")
    

rho[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO.rho> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD.netuid> "Link to this definition")
    

new_value[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD.new_value> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT.pallet> "Link to this definition")
    

serving_rate_limit[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT.serving_rate_limit> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY.hotkey> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_STAKE_THRESHOLD[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_STAKE_THRESHOLD> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

min_stake[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_STAKE_THRESHOLD.min_stake> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_STAKE_THRESHOLD.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_STAKE_THRESHOLD.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_STAKE_THRESHOLD.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_START_CALL_DELAY[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_START_CALL_DELAY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

delay[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_START_CALL_DELAY.delay> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_START_CALL_DELAY.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_START_CALL_DELAY.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_START_CALL_DELAY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_LIMIT[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_LIMIT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

max_subnets[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_LIMIT.max_subnets> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_LIMIT.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_LIMIT.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_LIMIT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_MOVING_ALPHA[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_MOVING_ALPHA> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

alpha[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_MOVING_ALPHA.alpha> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_MOVING_ALPHA.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_MOVING_ALPHA.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_MOVING_ALPHA.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_CUT[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_CUT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_CUT.pallet> "Link to this definition")
    

subnet_owner_cut[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_CUT.subnet_owner_cut> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_CUT.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_CUT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY.hotkey> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED.pallet> "Link to this definition")
    

subtoken_enabled[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED.subtoken_enabled> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_CUTOFF[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_CUTOFF> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

flow_cutoff[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_CUTOFF.flow_cutoff> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_CUTOFF.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_CUTOFF.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_CUTOFF.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

exponent[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT.exponent> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR.pallet> "Link to this definition")
    

smoothing_factor[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR.smoothing_factor> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.sudo> "Link to this definition")
    

target_registrations_per_interval[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.target_registrations_per_interval> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO.sudo> "Link to this definition")
    

tempo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO.tempo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER.sudo> "Link to this definition")
    

toggle[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER.toggle> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOTAL_ISSUANCE[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOTAL_ISSUANCE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOTAL_ISSUANCE.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOTAL_ISSUANCE.sudo> "Link to this definition")
    

total_issuance[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOTAL_ISSUANCE.total_issuance> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOTAL_ISSUANCE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT.sudo> "Link to this definition")
    

tx_rate_limit[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT.tx_rate_limit> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT.sudo> "Link to this definition")
    

tx_rate_limit[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT.tx_rate_limit> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_RATE_LIMIT[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_RATE_LIMIT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_RATE_LIMIT.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_RATE_LIMIT.sudo> "Link to this definition")
    

tx_rate_limit[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_RATE_LIMIT.tx_rate_limit> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_RATE_LIMIT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

alpha[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA.alpha> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT.wallet> "Link to this definition")
    

weights_set_rate_limit[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT.weights_set_rate_limit> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY.wallet> "Link to this definition")
    

weights_version_key[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY.weights_version_key> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

enabled[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED.enabled> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

enabled[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE.enabled> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE.pallet> "Link to this definition")
    

precompile_id[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE.precompile_id> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

max_n[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS.max_n> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

call[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT.call> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT.pallet> "Link to this definition")
    

sudo[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT.sudo> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT.wallet> "Link to this definition")
    

weight[#](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT.weight> "Link to this definition")
    

[ __ previous bittensor.extras.dev_framework.calls.pallets ](<../pallets/index.html> "previous page") [ next bittensor.extras.dev_framework.subnet __](<../../subnet/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`SUDO_AS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS>)
      * [`SUDO_AS.call`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS.call>)
      * [`SUDO_AS.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS.pallet>)
      * [`SUDO_AS.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS.sudo>)
      * [`SUDO_AS.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS.wallet>)
      * [`SUDO_AS.who`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_AS.who>)
    * [`SUDO_SET_ACTIVITY_CUTOFF`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF>)
      * [`SUDO_SET_ACTIVITY_CUTOFF.activity_cutoff`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF.activity_cutoff>)
      * [`SUDO_SET_ACTIVITY_CUTOFF.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF.netuid>)
      * [`SUDO_SET_ACTIVITY_CUTOFF.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF.pallet>)
      * [`SUDO_SET_ACTIVITY_CUTOFF.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF.sudo>)
      * [`SUDO_SET_ACTIVITY_CUTOFF.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ACTIVITY_CUTOFF.wallet>)
    * [`SUDO_SET_ADJUSTMENT_ALPHA`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA>)
      * [`SUDO_SET_ADJUSTMENT_ALPHA.adjustment_alpha`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA.adjustment_alpha>)
      * [`SUDO_SET_ADJUSTMENT_ALPHA.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA.netuid>)
      * [`SUDO_SET_ADJUSTMENT_ALPHA.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA.pallet>)
      * [`SUDO_SET_ADJUSTMENT_ALPHA.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA.sudo>)
      * [`SUDO_SET_ADJUSTMENT_ALPHA.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_ALPHA.wallet>)
    * [`SUDO_SET_ADJUSTMENT_INTERVAL`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL>)
      * [`SUDO_SET_ADJUSTMENT_INTERVAL.adjustment_interval`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL.adjustment_interval>)
      * [`SUDO_SET_ADJUSTMENT_INTERVAL.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL.netuid>)
      * [`SUDO_SET_ADJUSTMENT_INTERVAL.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL.pallet>)
      * [`SUDO_SET_ADJUSTMENT_INTERVAL.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL.sudo>)
      * [`SUDO_SET_ADJUSTMENT_INTERVAL.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADJUSTMENT_INTERVAL.wallet>)
    * [`SUDO_SET_ADMIN_FREEZE_WINDOW`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADMIN_FREEZE_WINDOW>)
      * [`SUDO_SET_ADMIN_FREEZE_WINDOW.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADMIN_FREEZE_WINDOW.pallet>)
      * [`SUDO_SET_ADMIN_FREEZE_WINDOW.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADMIN_FREEZE_WINDOW.sudo>)
      * [`SUDO_SET_ADMIN_FREEZE_WINDOW.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADMIN_FREEZE_WINDOW.wallet>)
      * [`SUDO_SET_ADMIN_FREEZE_WINDOW.window`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ADMIN_FREEZE_WINDOW.window>)
    * [`SUDO_SET_ALPHA_SIGMOID_STEEPNESS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS>)
      * [`SUDO_SET_ALPHA_SIGMOID_STEEPNESS.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS.netuid>)
      * [`SUDO_SET_ALPHA_SIGMOID_STEEPNESS.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS.pallet>)
      * [`SUDO_SET_ALPHA_SIGMOID_STEEPNESS.steepness`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS.steepness>)
      * [`SUDO_SET_ALPHA_SIGMOID_STEEPNESS.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS.sudo>)
      * [`SUDO_SET_ALPHA_SIGMOID_STEEPNESS.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_SIGMOID_STEEPNESS.wallet>)
    * [`SUDO_SET_ALPHA_VALUES`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES>)
      * [`SUDO_SET_ALPHA_VALUES.alpha_high`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES.alpha_high>)
      * [`SUDO_SET_ALPHA_VALUES.alpha_low`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES.alpha_low>)
      * [`SUDO_SET_ALPHA_VALUES.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES.netuid>)
      * [`SUDO_SET_ALPHA_VALUES.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES.pallet>)
      * [`SUDO_SET_ALPHA_VALUES.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES.sudo>)
      * [`SUDO_SET_ALPHA_VALUES.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ALPHA_VALUES.wallet>)
    * [`SUDO_SET_BONDS_MOVING_AVERAGE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE>)
      * [`SUDO_SET_BONDS_MOVING_AVERAGE.bonds_moving_average`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE.bonds_moving_average>)
      * [`SUDO_SET_BONDS_MOVING_AVERAGE.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE.netuid>)
      * [`SUDO_SET_BONDS_MOVING_AVERAGE.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE.pallet>)
      * [`SUDO_SET_BONDS_MOVING_AVERAGE.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE.sudo>)
      * [`SUDO_SET_BONDS_MOVING_AVERAGE.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_MOVING_AVERAGE.wallet>)
    * [`SUDO_SET_BONDS_PENALTY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY>)
      * [`SUDO_SET_BONDS_PENALTY.bonds_penalty`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY.bonds_penalty>)
      * [`SUDO_SET_BONDS_PENALTY.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY.netuid>)
      * [`SUDO_SET_BONDS_PENALTY.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY.pallet>)
      * [`SUDO_SET_BONDS_PENALTY.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY.sudo>)
      * [`SUDO_SET_BONDS_PENALTY.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_PENALTY.wallet>)
    * [`SUDO_SET_BONDS_RESET_ENABLED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED>)
      * [`SUDO_SET_BONDS_RESET_ENABLED.enabled`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED.enabled>)
      * [`SUDO_SET_BONDS_RESET_ENABLED.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED.netuid>)
      * [`SUDO_SET_BONDS_RESET_ENABLED.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED.pallet>)
      * [`SUDO_SET_BONDS_RESET_ENABLED.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED.sudo>)
      * [`SUDO_SET_BONDS_RESET_ENABLED.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BONDS_RESET_ENABLED.wallet>)
    * [`SUDO_SET_BURN_HALF_LIFE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE>)
      * [`SUDO_SET_BURN_HALF_LIFE.burn_half_life`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE.burn_half_life>)
      * [`SUDO_SET_BURN_HALF_LIFE.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE.netuid>)
      * [`SUDO_SET_BURN_HALF_LIFE.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE.pallet>)
      * [`SUDO_SET_BURN_HALF_LIFE.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE.sudo>)
      * [`SUDO_SET_BURN_HALF_LIFE.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_HALF_LIFE.wallet>)
    * [`SUDO_SET_BURN_INCREASE_MULT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT>)
      * [`SUDO_SET_BURN_INCREASE_MULT.burn_increase_mult`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT.burn_increase_mult>)
      * [`SUDO_SET_BURN_INCREASE_MULT.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT.netuid>)
      * [`SUDO_SET_BURN_INCREASE_MULT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT.pallet>)
      * [`SUDO_SET_BURN_INCREASE_MULT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT.sudo>)
      * [`SUDO_SET_BURN_INCREASE_MULT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_BURN_INCREASE_MULT.wallet>)
    * [`SUDO_SET_CK_BURN`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_CK_BURN>)
      * [`SUDO_SET_CK_BURN.burn`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_CK_BURN.burn>)
      * [`SUDO_SET_CK_BURN.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_CK_BURN.pallet>)
      * [`SUDO_SET_CK_BURN.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_CK_BURN.sudo>)
      * [`SUDO_SET_CK_BURN.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_CK_BURN.wallet>)
    * [`SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY>)
      * [`SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY.duration`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY.duration>)
      * [`SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY.pallet>)
      * [`SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY.sudo>)
      * [`SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_ANNOUNCEMENT_DELAY.wallet>)
    * [`SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY>)
      * [`SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY.duration`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY.duration>)
      * [`SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY.pallet>)
      * [`SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY.sudo>)
      * [`SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COLDKEY_SWAP_REANNOUNCEMENT_DELAY.wallet>)
    * [`SUDO_SET_COMMIT_REVEAL_VERSION`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_VERSION>)
      * [`SUDO_SET_COMMIT_REVEAL_VERSION.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_VERSION.pallet>)
      * [`SUDO_SET_COMMIT_REVEAL_VERSION.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_VERSION.sudo>)
      * [`SUDO_SET_COMMIT_REVEAL_VERSION.version`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_VERSION.version>)
      * [`SUDO_SET_COMMIT_REVEAL_VERSION.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_VERSION.wallet>)
    * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED>)
      * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.enabled`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.enabled>)
      * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.netuid>)
      * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.pallet>)
      * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.sudo>)
      * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_ENABLED.wallet>)
    * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL>)
      * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.interval`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.interval>)
      * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.netuid>)
      * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.pallet>)
      * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.sudo>)
      * [`SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_COMMIT_REVEAL_WEIGHTS_INTERVAL.wallet>)
    * [`SUDO_SET_DEFAULT_TAKE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DEFAULT_TAKE>)
      * [`SUDO_SET_DEFAULT_TAKE.default_take`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DEFAULT_TAKE.default_take>)
      * [`SUDO_SET_DEFAULT_TAKE.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DEFAULT_TAKE.pallet>)
      * [`SUDO_SET_DEFAULT_TAKE.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DEFAULT_TAKE.sudo>)
      * [`SUDO_SET_DEFAULT_TAKE.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DEFAULT_TAKE.wallet>)
    * [`SUDO_SET_DIFFICULTY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY>)
      * [`SUDO_SET_DIFFICULTY.difficulty`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY.difficulty>)
      * [`SUDO_SET_DIFFICULTY.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY.netuid>)
      * [`SUDO_SET_DIFFICULTY.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY.pallet>)
      * [`SUDO_SET_DIFFICULTY.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY.sudo>)
      * [`SUDO_SET_DIFFICULTY.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DIFFICULTY.wallet>)
    * [`SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION>)
      * [`SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION.duration`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION.duration>)
      * [`SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION.pallet>)
      * [`SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION.sudo>)
      * [`SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_DISSOLVE_NETWORK_SCHEDULE_DURATION.wallet>)
    * [`SUDO_SET_EMA_PRICE_HALVING_PERIOD`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD>)
      * [`SUDO_SET_EMA_PRICE_HALVING_PERIOD.ema_halving`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD.ema_halving>)
      * [`SUDO_SET_EMA_PRICE_HALVING_PERIOD.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD.netuid>)
      * [`SUDO_SET_EMA_PRICE_HALVING_PERIOD.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD.pallet>)
      * [`SUDO_SET_EMA_PRICE_HALVING_PERIOD.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD.sudo>)
      * [`SUDO_SET_EMA_PRICE_HALVING_PERIOD.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EMA_PRICE_HALVING_PERIOD.wallet>)
    * [`SUDO_SET_EVM_CHAIN_ID`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EVM_CHAIN_ID>)
      * [`SUDO_SET_EVM_CHAIN_ID.chain_id`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EVM_CHAIN_ID.chain_id>)
      * [`SUDO_SET_EVM_CHAIN_ID.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EVM_CHAIN_ID.pallet>)
      * [`SUDO_SET_EVM_CHAIN_ID.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EVM_CHAIN_ID.sudo>)
      * [`SUDO_SET_EVM_CHAIN_ID.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_EVM_CHAIN_ID.wallet>)
    * [`SUDO_SET_IMMUNITY_PERIOD`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD>)
      * [`SUDO_SET_IMMUNITY_PERIOD.immunity_period`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD.immunity_period>)
      * [`SUDO_SET_IMMUNITY_PERIOD.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD.netuid>)
      * [`SUDO_SET_IMMUNITY_PERIOD.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD.pallet>)
      * [`SUDO_SET_IMMUNITY_PERIOD.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD.sudo>)
      * [`SUDO_SET_IMMUNITY_PERIOD.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_IMMUNITY_PERIOD.wallet>)
    * [`SUDO_SET_KAPPA`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA>)
      * [`SUDO_SET_KAPPA.kappa`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA.kappa>)
      * [`SUDO_SET_KAPPA.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA.netuid>)
      * [`SUDO_SET_KAPPA.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA.pallet>)
      * [`SUDO_SET_KAPPA.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA.sudo>)
      * [`SUDO_SET_KAPPA.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_KAPPA.wallet>)
    * [`SUDO_SET_LIQUID_ALPHA_ENABLED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED>)
      * [`SUDO_SET_LIQUID_ALPHA_ENABLED.enabled`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED.enabled>)
      * [`SUDO_SET_LIQUID_ALPHA_ENABLED.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED.netuid>)
      * [`SUDO_SET_LIQUID_ALPHA_ENABLED.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED.pallet>)
      * [`SUDO_SET_LIQUID_ALPHA_ENABLED.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED.sudo>)
      * [`SUDO_SET_LIQUID_ALPHA_ENABLED.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LIQUID_ALPHA_ENABLED.wallet>)
    * [`SUDO_SET_LOCK_REDUCTION_INTERVAL`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LOCK_REDUCTION_INTERVAL>)
      * [`SUDO_SET_LOCK_REDUCTION_INTERVAL.interval`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LOCK_REDUCTION_INTERVAL.interval>)
      * [`SUDO_SET_LOCK_REDUCTION_INTERVAL.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LOCK_REDUCTION_INTERVAL.pallet>)
      * [`SUDO_SET_LOCK_REDUCTION_INTERVAL.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LOCK_REDUCTION_INTERVAL.sudo>)
      * [`SUDO_SET_LOCK_REDUCTION_INTERVAL.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_LOCK_REDUCTION_INTERVAL.wallet>)
    * [`SUDO_SET_MAX_ALLOWED_UIDS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS>)
      * [`SUDO_SET_MAX_ALLOWED_UIDS.max_allowed_uids`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS.max_allowed_uids>)
      * [`SUDO_SET_MAX_ALLOWED_UIDS.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS.netuid>)
      * [`SUDO_SET_MAX_ALLOWED_UIDS.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS.pallet>)
      * [`SUDO_SET_MAX_ALLOWED_UIDS.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS.sudo>)
      * [`SUDO_SET_MAX_ALLOWED_UIDS.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_UIDS.wallet>)
    * [`SUDO_SET_MAX_ALLOWED_VALIDATORS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS>)
      * [`SUDO_SET_MAX_ALLOWED_VALIDATORS.max_allowed_validators`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS.max_allowed_validators>)
      * [`SUDO_SET_MAX_ALLOWED_VALIDATORS.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS.netuid>)
      * [`SUDO_SET_MAX_ALLOWED_VALIDATORS.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS.pallet>)
      * [`SUDO_SET_MAX_ALLOWED_VALIDATORS.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS.sudo>)
      * [`SUDO_SET_MAX_ALLOWED_VALIDATORS.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_ALLOWED_VALIDATORS.wallet>)
    * [`SUDO_SET_MAX_BURN`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN>)
      * [`SUDO_SET_MAX_BURN.max_burn`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN.max_burn>)
      * [`SUDO_SET_MAX_BURN.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN.netuid>)
      * [`SUDO_SET_MAX_BURN.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN.pallet>)
      * [`SUDO_SET_MAX_BURN.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN.sudo>)
      * [`SUDO_SET_MAX_BURN.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_BURN.wallet>)
    * [`SUDO_SET_MAX_CHILDKEY_TAKE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_CHILDKEY_TAKE>)
      * [`SUDO_SET_MAX_CHILDKEY_TAKE.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_CHILDKEY_TAKE.pallet>)
      * [`SUDO_SET_MAX_CHILDKEY_TAKE.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_CHILDKEY_TAKE.sudo>)
      * [`SUDO_SET_MAX_CHILDKEY_TAKE.take`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_CHILDKEY_TAKE.take>)
      * [`SUDO_SET_MAX_CHILDKEY_TAKE.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_CHILDKEY_TAKE.wallet>)
    * [`SUDO_SET_MAX_DIFFICULTY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY>)
      * [`SUDO_SET_MAX_DIFFICULTY.max_difficulty`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY.max_difficulty>)
      * [`SUDO_SET_MAX_DIFFICULTY.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY.netuid>)
      * [`SUDO_SET_MAX_DIFFICULTY.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY.pallet>)
      * [`SUDO_SET_MAX_DIFFICULTY.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY.sudo>)
      * [`SUDO_SET_MAX_DIFFICULTY.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_DIFFICULTY.wallet>)
    * [`SUDO_SET_MAX_MECHANISM_COUNT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_MECHANISM_COUNT>)
      * [`SUDO_SET_MAX_MECHANISM_COUNT.max_mechanism_count`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_MECHANISM_COUNT.max_mechanism_count>)
      * [`SUDO_SET_MAX_MECHANISM_COUNT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_MECHANISM_COUNT.pallet>)
      * [`SUDO_SET_MAX_MECHANISM_COUNT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_MECHANISM_COUNT.sudo>)
      * [`SUDO_SET_MAX_MECHANISM_COUNT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_MECHANISM_COUNT.wallet>)
    * [`SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK>)
      * [`SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.max_registrations_per_block`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.max_registrations_per_block>)
      * [`SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.netuid>)
      * [`SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.pallet>)
      * [`SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.sudo>)
      * [`SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MAX_REGISTRATIONS_PER_BLOCK.wallet>)
    * [`SUDO_SET_MECHANISM_COUNT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT>)
      * [`SUDO_SET_MECHANISM_COUNT.mechanism_count`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT.mechanism_count>)
      * [`SUDO_SET_MECHANISM_COUNT.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT.netuid>)
      * [`SUDO_SET_MECHANISM_COUNT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT.pallet>)
      * [`SUDO_SET_MECHANISM_COUNT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT.sudo>)
      * [`SUDO_SET_MECHANISM_COUNT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_COUNT.wallet>)
    * [`SUDO_SET_MECHANISM_EMISSION_SPLIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT>)
      * [`SUDO_SET_MECHANISM_EMISSION_SPLIT.maybe_split`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT.maybe_split>)
      * [`SUDO_SET_MECHANISM_EMISSION_SPLIT.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT.netuid>)
      * [`SUDO_SET_MECHANISM_EMISSION_SPLIT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT.pallet>)
      * [`SUDO_SET_MECHANISM_EMISSION_SPLIT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT.sudo>)
      * [`SUDO_SET_MECHANISM_EMISSION_SPLIT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MECHANISM_EMISSION_SPLIT.wallet>)
    * [`SUDO_SET_MIN_ALLOWED_UIDS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS>)
      * [`SUDO_SET_MIN_ALLOWED_UIDS.min_allowed_uids`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS.min_allowed_uids>)
      * [`SUDO_SET_MIN_ALLOWED_UIDS.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS.netuid>)
      * [`SUDO_SET_MIN_ALLOWED_UIDS.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS.pallet>)
      * [`SUDO_SET_MIN_ALLOWED_UIDS.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS.sudo>)
      * [`SUDO_SET_MIN_ALLOWED_UIDS.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_UIDS.wallet>)
    * [`SUDO_SET_MIN_ALLOWED_WEIGHTS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS>)
      * [`SUDO_SET_MIN_ALLOWED_WEIGHTS.min_allowed_weights`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS.min_allowed_weights>)
      * [`SUDO_SET_MIN_ALLOWED_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS.netuid>)
      * [`SUDO_SET_MIN_ALLOWED_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS.pallet>)
      * [`SUDO_SET_MIN_ALLOWED_WEIGHTS.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS.sudo>)
      * [`SUDO_SET_MIN_ALLOWED_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_ALLOWED_WEIGHTS.wallet>)
    * [`SUDO_SET_MIN_BURN`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN>)
      * [`SUDO_SET_MIN_BURN.min_burn`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN.min_burn>)
      * [`SUDO_SET_MIN_BURN.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN.netuid>)
      * [`SUDO_SET_MIN_BURN.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN.pallet>)
      * [`SUDO_SET_MIN_BURN.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN.sudo>)
      * [`SUDO_SET_MIN_BURN.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_BURN.wallet>)
    * [`SUDO_SET_MIN_CHILDKEY_TAKE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_CHILDKEY_TAKE>)
      * [`SUDO_SET_MIN_CHILDKEY_TAKE.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_CHILDKEY_TAKE.pallet>)
      * [`SUDO_SET_MIN_CHILDKEY_TAKE.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_CHILDKEY_TAKE.sudo>)
      * [`SUDO_SET_MIN_CHILDKEY_TAKE.take`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_CHILDKEY_TAKE.take>)
      * [`SUDO_SET_MIN_CHILDKEY_TAKE.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_CHILDKEY_TAKE.wallet>)
    * [`SUDO_SET_MIN_DELEGATE_TAKE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DELEGATE_TAKE>)
      * [`SUDO_SET_MIN_DELEGATE_TAKE.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DELEGATE_TAKE.pallet>)
      * [`SUDO_SET_MIN_DELEGATE_TAKE.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DELEGATE_TAKE.sudo>)
      * [`SUDO_SET_MIN_DELEGATE_TAKE.take`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DELEGATE_TAKE.take>)
      * [`SUDO_SET_MIN_DELEGATE_TAKE.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DELEGATE_TAKE.wallet>)
    * [`SUDO_SET_MIN_DIFFICULTY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY>)
      * [`SUDO_SET_MIN_DIFFICULTY.min_difficulty`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY.min_difficulty>)
      * [`SUDO_SET_MIN_DIFFICULTY.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY.netuid>)
      * [`SUDO_SET_MIN_DIFFICULTY.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY.pallet>)
      * [`SUDO_SET_MIN_DIFFICULTY.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY.sudo>)
      * [`SUDO_SET_MIN_DIFFICULTY.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_DIFFICULTY.wallet>)
    * [`SUDO_SET_MIN_NON_IMMUNE_UIDS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS>)
      * [`SUDO_SET_MIN_NON_IMMUNE_UIDS.min`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS.min>)
      * [`SUDO_SET_MIN_NON_IMMUNE_UIDS.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS.netuid>)
      * [`SUDO_SET_MIN_NON_IMMUNE_UIDS.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS.pallet>)
      * [`SUDO_SET_MIN_NON_IMMUNE_UIDS.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS.sudo>)
      * [`SUDO_SET_MIN_NON_IMMUNE_UIDS.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_MIN_NON_IMMUNE_UIDS.wallet>)
    * [`SUDO_SET_NETWORK_IMMUNITY_PERIOD`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_IMMUNITY_PERIOD>)
      * [`SUDO_SET_NETWORK_IMMUNITY_PERIOD.immunity_period`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_IMMUNITY_PERIOD.immunity_period>)
      * [`SUDO_SET_NETWORK_IMMUNITY_PERIOD.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_IMMUNITY_PERIOD.pallet>)
      * [`SUDO_SET_NETWORK_IMMUNITY_PERIOD.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_IMMUNITY_PERIOD.sudo>)
      * [`SUDO_SET_NETWORK_IMMUNITY_PERIOD.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_IMMUNITY_PERIOD.wallet>)
    * [`SUDO_SET_NETWORK_MIN_LOCK_COST`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_MIN_LOCK_COST>)
      * [`SUDO_SET_NETWORK_MIN_LOCK_COST.lock_cost`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_MIN_LOCK_COST.lock_cost>)
      * [`SUDO_SET_NETWORK_MIN_LOCK_COST.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_MIN_LOCK_COST.pallet>)
      * [`SUDO_SET_NETWORK_MIN_LOCK_COST.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_MIN_LOCK_COST.sudo>)
      * [`SUDO_SET_NETWORK_MIN_LOCK_COST.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_MIN_LOCK_COST.wallet>)
    * [`SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED>)
      * [`SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.netuid>)
      * [`SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.pallet>)
      * [`SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.registration_allowed`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.registration_allowed>)
      * [`SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.sudo>)
      * [`SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_POW_REGISTRATION_ALLOWED.wallet>)
    * [`SUDO_SET_NETWORK_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_RATE_LIMIT>)
      * [`SUDO_SET_NETWORK_RATE_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_RATE_LIMIT.pallet>)
      * [`SUDO_SET_NETWORK_RATE_LIMIT.rate_limit`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_RATE_LIMIT.rate_limit>)
      * [`SUDO_SET_NETWORK_RATE_LIMIT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_RATE_LIMIT.sudo>)
      * [`SUDO_SET_NETWORK_RATE_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_RATE_LIMIT.wallet>)
    * [`SUDO_SET_NETWORK_REGISTRATION_ALLOWED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED>)
      * [`SUDO_SET_NETWORK_REGISTRATION_ALLOWED.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED.netuid>)
      * [`SUDO_SET_NETWORK_REGISTRATION_ALLOWED.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED.pallet>)
      * [`SUDO_SET_NETWORK_REGISTRATION_ALLOWED.registration_allowed`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED.registration_allowed>)
      * [`SUDO_SET_NETWORK_REGISTRATION_ALLOWED.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED.sudo>)
      * [`SUDO_SET_NETWORK_REGISTRATION_ALLOWED.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NETWORK_REGISTRATION_ALLOWED.wallet>)
    * [`SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE>)
      * [`SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE.min_stake`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE.min_stake>)
      * [`SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE.pallet>)
      * [`SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE.sudo>)
      * [`SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NOMINATOR_MIN_REQUIRED_STAKE.wallet>)
    * [`SUDO_SET_NUM_ROOT_CLAIMS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NUM_ROOT_CLAIMS>)
      * [`SUDO_SET_NUM_ROOT_CLAIMS.new_value`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NUM_ROOT_CLAIMS.new_value>)
      * [`SUDO_SET_NUM_ROOT_CLAIMS.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NUM_ROOT_CLAIMS.pallet>)
      * [`SUDO_SET_NUM_ROOT_CLAIMS.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NUM_ROOT_CLAIMS.sudo>)
      * [`SUDO_SET_NUM_ROOT_CLAIMS.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_NUM_ROOT_CLAIMS.wallet>)
    * [`SUDO_SET_OWNER_HPARAM_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_HPARAM_RATE_LIMIT>)
      * [`SUDO_SET_OWNER_HPARAM_RATE_LIMIT.epochs`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_HPARAM_RATE_LIMIT.epochs>)
      * [`SUDO_SET_OWNER_HPARAM_RATE_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_HPARAM_RATE_LIMIT.pallet>)
      * [`SUDO_SET_OWNER_HPARAM_RATE_LIMIT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_HPARAM_RATE_LIMIT.sudo>)
      * [`SUDO_SET_OWNER_HPARAM_RATE_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_HPARAM_RATE_LIMIT.wallet>)
    * [`SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT>)
      * [`SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.immune_neurons`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.immune_neurons>)
      * [`SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.netuid>)
      * [`SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.pallet>)
      * [`SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.sudo>)
      * [`SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_OWNER_IMMUNE_NEURON_LIMIT.wallet>)
    * [`SUDO_SET_RAO_RECYCLED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED>)
      * [`SUDO_SET_RAO_RECYCLED.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED.netuid>)
      * [`SUDO_SET_RAO_RECYCLED.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED.pallet>)
      * [`SUDO_SET_RAO_RECYCLED.rao_recycled`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED.rao_recycled>)
      * [`SUDO_SET_RAO_RECYCLED.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED.sudo>)
      * [`SUDO_SET_RAO_RECYCLED.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RAO_RECYCLED.wallet>)
    * [`SUDO_SET_RECYCLE_OR_BURN`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN>)
      * [`SUDO_SET_RECYCLE_OR_BURN.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN.netuid>)
      * [`SUDO_SET_RECYCLE_OR_BURN.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN.pallet>)
      * [`SUDO_SET_RECYCLE_OR_BURN.recycle_or_burn`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN.recycle_or_burn>)
      * [`SUDO_SET_RECYCLE_OR_BURN.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN.sudo>)
      * [`SUDO_SET_RECYCLE_OR_BURN.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RECYCLE_OR_BURN.wallet>)
    * [`SUDO_SET_RHO`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO>)
      * [`SUDO_SET_RHO.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO.netuid>)
      * [`SUDO_SET_RHO.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO.pallet>)
      * [`SUDO_SET_RHO.rho`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO.rho>)
      * [`SUDO_SET_RHO.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO.sudo>)
      * [`SUDO_SET_RHO.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_RHO.wallet>)
    * [`SUDO_SET_ROOT_CLAIM_THRESHOLD`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD>)
      * [`SUDO_SET_ROOT_CLAIM_THRESHOLD.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD.netuid>)
      * [`SUDO_SET_ROOT_CLAIM_THRESHOLD.new_value`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD.new_value>)
      * [`SUDO_SET_ROOT_CLAIM_THRESHOLD.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD.pallet>)
      * [`SUDO_SET_ROOT_CLAIM_THRESHOLD.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD.sudo>)
      * [`SUDO_SET_ROOT_CLAIM_THRESHOLD.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_ROOT_CLAIM_THRESHOLD.wallet>)
    * [`SUDO_SET_SERVING_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT>)
      * [`SUDO_SET_SERVING_RATE_LIMIT.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT.netuid>)
      * [`SUDO_SET_SERVING_RATE_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT.pallet>)
      * [`SUDO_SET_SERVING_RATE_LIMIT.serving_rate_limit`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT.serving_rate_limit>)
      * [`SUDO_SET_SERVING_RATE_LIMIT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT.sudo>)
      * [`SUDO_SET_SERVING_RATE_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SERVING_RATE_LIMIT.wallet>)
    * [`SUDO_SET_SN_OWNER_HOTKEY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY>)
      * [`SUDO_SET_SN_OWNER_HOTKEY.hotkey`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY.hotkey>)
      * [`SUDO_SET_SN_OWNER_HOTKEY.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY.netuid>)
      * [`SUDO_SET_SN_OWNER_HOTKEY.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY.pallet>)
      * [`SUDO_SET_SN_OWNER_HOTKEY.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY.sudo>)
      * [`SUDO_SET_SN_OWNER_HOTKEY.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SN_OWNER_HOTKEY.wallet>)
    * [`SUDO_SET_STAKE_THRESHOLD`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_STAKE_THRESHOLD>)
      * [`SUDO_SET_STAKE_THRESHOLD.min_stake`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_STAKE_THRESHOLD.min_stake>)
      * [`SUDO_SET_STAKE_THRESHOLD.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_STAKE_THRESHOLD.pallet>)
      * [`SUDO_SET_STAKE_THRESHOLD.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_STAKE_THRESHOLD.sudo>)
      * [`SUDO_SET_STAKE_THRESHOLD.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_STAKE_THRESHOLD.wallet>)
    * [`SUDO_SET_START_CALL_DELAY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_START_CALL_DELAY>)
      * [`SUDO_SET_START_CALL_DELAY.delay`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_START_CALL_DELAY.delay>)
      * [`SUDO_SET_START_CALL_DELAY.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_START_CALL_DELAY.pallet>)
      * [`SUDO_SET_START_CALL_DELAY.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_START_CALL_DELAY.sudo>)
      * [`SUDO_SET_START_CALL_DELAY.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_START_CALL_DELAY.wallet>)
    * [`SUDO_SET_SUBNET_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_LIMIT>)
      * [`SUDO_SET_SUBNET_LIMIT.max_subnets`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_LIMIT.max_subnets>)
      * [`SUDO_SET_SUBNET_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_LIMIT.pallet>)
      * [`SUDO_SET_SUBNET_LIMIT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_LIMIT.sudo>)
      * [`SUDO_SET_SUBNET_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_LIMIT.wallet>)
    * [`SUDO_SET_SUBNET_MOVING_ALPHA`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_MOVING_ALPHA>)
      * [`SUDO_SET_SUBNET_MOVING_ALPHA.alpha`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_MOVING_ALPHA.alpha>)
      * [`SUDO_SET_SUBNET_MOVING_ALPHA.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_MOVING_ALPHA.pallet>)
      * [`SUDO_SET_SUBNET_MOVING_ALPHA.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_MOVING_ALPHA.sudo>)
      * [`SUDO_SET_SUBNET_MOVING_ALPHA.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_MOVING_ALPHA.wallet>)
    * [`SUDO_SET_SUBNET_OWNER_CUT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_CUT>)
      * [`SUDO_SET_SUBNET_OWNER_CUT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_CUT.pallet>)
      * [`SUDO_SET_SUBNET_OWNER_CUT.subnet_owner_cut`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_CUT.subnet_owner_cut>)
      * [`SUDO_SET_SUBNET_OWNER_CUT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_CUT.sudo>)
      * [`SUDO_SET_SUBNET_OWNER_CUT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_CUT.wallet>)
    * [`SUDO_SET_SUBNET_OWNER_HOTKEY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY>)
      * [`SUDO_SET_SUBNET_OWNER_HOTKEY.hotkey`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY.hotkey>)
      * [`SUDO_SET_SUBNET_OWNER_HOTKEY.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY.netuid>)
      * [`SUDO_SET_SUBNET_OWNER_HOTKEY.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY.pallet>)
      * [`SUDO_SET_SUBNET_OWNER_HOTKEY.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY.sudo>)
      * [`SUDO_SET_SUBNET_OWNER_HOTKEY.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBNET_OWNER_HOTKEY.wallet>)
    * [`SUDO_SET_SUBTOKEN_ENABLED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED>)
      * [`SUDO_SET_SUBTOKEN_ENABLED.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED.netuid>)
      * [`SUDO_SET_SUBTOKEN_ENABLED.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED.pallet>)
      * [`SUDO_SET_SUBTOKEN_ENABLED.subtoken_enabled`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED.subtoken_enabled>)
      * [`SUDO_SET_SUBTOKEN_ENABLED.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED.sudo>)
      * [`SUDO_SET_SUBTOKEN_ENABLED.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_SUBTOKEN_ENABLED.wallet>)
    * [`SUDO_SET_TAO_FLOW_CUTOFF`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_CUTOFF>)
      * [`SUDO_SET_TAO_FLOW_CUTOFF.flow_cutoff`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_CUTOFF.flow_cutoff>)
      * [`SUDO_SET_TAO_FLOW_CUTOFF.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_CUTOFF.pallet>)
      * [`SUDO_SET_TAO_FLOW_CUTOFF.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_CUTOFF.sudo>)
      * [`SUDO_SET_TAO_FLOW_CUTOFF.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_CUTOFF.wallet>)
    * [`SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT>)
      * [`SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT.exponent`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT.exponent>)
      * [`SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT.pallet>)
      * [`SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT.sudo>)
      * [`SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_NORMALIZATION_EXPONENT.wallet>)
    * [`SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR>)
      * [`SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR.pallet>)
      * [`SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR.smoothing_factor`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR.smoothing_factor>)
      * [`SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR.sudo>)
      * [`SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TAO_FLOW_SMOOTHING_FACTOR.wallet>)
    * [`SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL>)
      * [`SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.netuid>)
      * [`SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.pallet>)
      * [`SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.sudo>)
      * [`SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.target_registrations_per_interval`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.target_registrations_per_interval>)
      * [`SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TARGET_REGISTRATIONS_PER_INTERVAL.wallet>)
    * [`SUDO_SET_TEMPO`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO>)
      * [`SUDO_SET_TEMPO.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO.netuid>)
      * [`SUDO_SET_TEMPO.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO.pallet>)
      * [`SUDO_SET_TEMPO.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO.sudo>)
      * [`SUDO_SET_TEMPO.tempo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO.tempo>)
      * [`SUDO_SET_TEMPO.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TEMPO.wallet>)
    * [`SUDO_SET_TOGGLE_TRANSFER`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER>)
      * [`SUDO_SET_TOGGLE_TRANSFER.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER.netuid>)
      * [`SUDO_SET_TOGGLE_TRANSFER.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER.pallet>)
      * [`SUDO_SET_TOGGLE_TRANSFER.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER.sudo>)
      * [`SUDO_SET_TOGGLE_TRANSFER.toggle`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER.toggle>)
      * [`SUDO_SET_TOGGLE_TRANSFER.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOGGLE_TRANSFER.wallet>)
    * [`SUDO_SET_TOTAL_ISSUANCE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOTAL_ISSUANCE>)
      * [`SUDO_SET_TOTAL_ISSUANCE.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOTAL_ISSUANCE.pallet>)
      * [`SUDO_SET_TOTAL_ISSUANCE.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOTAL_ISSUANCE.sudo>)
      * [`SUDO_SET_TOTAL_ISSUANCE.total_issuance`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOTAL_ISSUANCE.total_issuance>)
      * [`SUDO_SET_TOTAL_ISSUANCE.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TOTAL_ISSUANCE.wallet>)
    * [`SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT>)
      * [`SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT.pallet>)
      * [`SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT.sudo>)
      * [`SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT.tx_rate_limit`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT.tx_rate_limit>)
      * [`SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_CHILDKEY_TAKE_RATE_LIMIT.wallet>)
    * [`SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT>)
      * [`SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT.pallet>)
      * [`SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT.sudo>)
      * [`SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT.tx_rate_limit`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT.tx_rate_limit>)
      * [`SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_DELEGATE_TAKE_RATE_LIMIT.wallet>)
    * [`SUDO_SET_TX_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_RATE_LIMIT>)
      * [`SUDO_SET_TX_RATE_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_RATE_LIMIT.pallet>)
      * [`SUDO_SET_TX_RATE_LIMIT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_RATE_LIMIT.sudo>)
      * [`SUDO_SET_TX_RATE_LIMIT.tx_rate_limit`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_RATE_LIMIT.tx_rate_limit>)
      * [`SUDO_SET_TX_RATE_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_TX_RATE_LIMIT.wallet>)
    * [`SUDO_SET_VOTING_POWER_EMA_ALPHA`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA>)
      * [`SUDO_SET_VOTING_POWER_EMA_ALPHA.alpha`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA.alpha>)
      * [`SUDO_SET_VOTING_POWER_EMA_ALPHA.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA.netuid>)
      * [`SUDO_SET_VOTING_POWER_EMA_ALPHA.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA.pallet>)
      * [`SUDO_SET_VOTING_POWER_EMA_ALPHA.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA.sudo>)
      * [`SUDO_SET_VOTING_POWER_EMA_ALPHA.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_VOTING_POWER_EMA_ALPHA.wallet>)
    * [`SUDO_SET_WEIGHTS_SET_RATE_LIMIT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT>)
      * [`SUDO_SET_WEIGHTS_SET_RATE_LIMIT.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT.netuid>)
      * [`SUDO_SET_WEIGHTS_SET_RATE_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT.pallet>)
      * [`SUDO_SET_WEIGHTS_SET_RATE_LIMIT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT.sudo>)
      * [`SUDO_SET_WEIGHTS_SET_RATE_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT.wallet>)
      * [`SUDO_SET_WEIGHTS_SET_RATE_LIMIT.weights_set_rate_limit`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_SET_RATE_LIMIT.weights_set_rate_limit>)
    * [`SUDO_SET_WEIGHTS_VERSION_KEY`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY>)
      * [`SUDO_SET_WEIGHTS_VERSION_KEY.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY.netuid>)
      * [`SUDO_SET_WEIGHTS_VERSION_KEY.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY.pallet>)
      * [`SUDO_SET_WEIGHTS_VERSION_KEY.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY.sudo>)
      * [`SUDO_SET_WEIGHTS_VERSION_KEY.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY.wallet>)
      * [`SUDO_SET_WEIGHTS_VERSION_KEY.weights_version_key`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_WEIGHTS_VERSION_KEY.weights_version_key>)
    * [`SUDO_SET_YUMA3_ENABLED`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED>)
      * [`SUDO_SET_YUMA3_ENABLED.enabled`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED.enabled>)
      * [`SUDO_SET_YUMA3_ENABLED.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED.netuid>)
      * [`SUDO_SET_YUMA3_ENABLED.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED.pallet>)
      * [`SUDO_SET_YUMA3_ENABLED.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED.sudo>)
      * [`SUDO_SET_YUMA3_ENABLED.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_SET_YUMA3_ENABLED.wallet>)
    * [`SUDO_TOGGLE_EVM_PRECOMPILE`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE>)
      * [`SUDO_TOGGLE_EVM_PRECOMPILE.enabled`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE.enabled>)
      * [`SUDO_TOGGLE_EVM_PRECOMPILE.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE.pallet>)
      * [`SUDO_TOGGLE_EVM_PRECOMPILE.precompile_id`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE.precompile_id>)
      * [`SUDO_TOGGLE_EVM_PRECOMPILE.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE.sudo>)
      * [`SUDO_TOGGLE_EVM_PRECOMPILE.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TOGGLE_EVM_PRECOMPILE.wallet>)
    * [`SUDO_TRIM_TO_MAX_ALLOWED_UIDS`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS>)
      * [`SUDO_TRIM_TO_MAX_ALLOWED_UIDS.max_n`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS.max_n>)
      * [`SUDO_TRIM_TO_MAX_ALLOWED_UIDS.netuid`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS.netuid>)
      * [`SUDO_TRIM_TO_MAX_ALLOWED_UIDS.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS.pallet>)
      * [`SUDO_TRIM_TO_MAX_ALLOWED_UIDS.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS.sudo>)
      * [`SUDO_TRIM_TO_MAX_ALLOWED_UIDS.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_TRIM_TO_MAX_ALLOWED_UIDS.wallet>)
    * [`SUDO_UNCHECKED_WEIGHT`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT>)
      * [`SUDO_UNCHECKED_WEIGHT.call`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT.call>)
      * [`SUDO_UNCHECKED_WEIGHT.pallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT.pallet>)
      * [`SUDO_UNCHECKED_WEIGHT.sudo`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT.sudo>)
      * [`SUDO_UNCHECKED_WEIGHT.wallet`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT.wallet>)
      * [`SUDO_UNCHECKED_WEIGHT.weight`](<#bittensor.extras.dev_framework.calls.sudo_calls.SUDO_UNCHECKED_WEIGHT.weight>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.