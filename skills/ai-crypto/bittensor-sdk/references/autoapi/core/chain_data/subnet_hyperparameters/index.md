# bittensor.core.chain_data.subnet_hyperparameters &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/subnet_hyperparameters/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/subnet_hyperparameters/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/subnet_hyperparameters/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.subnet_hyperparameters

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`SubnetHyperparameters`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters>)
      * [`SubnetHyperparameters.activity_cutoff`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.activity_cutoff>)
      * [`SubnetHyperparameters.adjustment_alpha`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.adjustment_alpha>)
      * [`SubnetHyperparameters.adjustment_interval`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.adjustment_interval>)
      * [`SubnetHyperparameters.alpha_high`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.alpha_high>)
      * [`SubnetHyperparameters.alpha_low`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.alpha_low>)
      * [`SubnetHyperparameters.alpha_sigmoid_steepness`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.alpha_sigmoid_steepness>)
      * [`SubnetHyperparameters.bonds_moving_avg`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.bonds_moving_avg>)
      * [`SubnetHyperparameters.bonds_reset_enabled`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.bonds_reset_enabled>)
      * [`SubnetHyperparameters.commit_reveal_period`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.commit_reveal_period>)
      * [`SubnetHyperparameters.commit_reveal_weights_enabled`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.commit_reveal_weights_enabled>)
      * [`SubnetHyperparameters.difficulty`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.difficulty>)
      * [`SubnetHyperparameters.immunity_period`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.immunity_period>)
      * [`SubnetHyperparameters.kappa`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.kappa>)
      * [`SubnetHyperparameters.liquid_alpha_enabled`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.liquid_alpha_enabled>)
      * [`SubnetHyperparameters.max_burn`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.max_burn>)
      * [`SubnetHyperparameters.max_difficulty`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.max_difficulty>)
      * [`SubnetHyperparameters.max_regs_per_block`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.max_regs_per_block>)
      * [`SubnetHyperparameters.max_validators`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.max_validators>)
      * [`SubnetHyperparameters.max_weight_limit`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.max_weight_limit>)
      * [`SubnetHyperparameters.min_allowed_weights`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.min_allowed_weights>)
      * [`SubnetHyperparameters.min_burn`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.min_burn>)
      * [`SubnetHyperparameters.min_difficulty`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.min_difficulty>)
      * [`SubnetHyperparameters.registration_allowed`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.registration_allowed>)
      * [`SubnetHyperparameters.rho`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.rho>)
      * [`SubnetHyperparameters.serving_rate_limit`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.serving_rate_limit>)
      * [`SubnetHyperparameters.subnet_is_active`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.subnet_is_active>)
      * [`SubnetHyperparameters.target_regs_per_interval`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.target_regs_per_interval>)
      * [`SubnetHyperparameters.tempo`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.tempo>)
      * [`SubnetHyperparameters.transfers_enabled`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.transfers_enabled>)
      * [`SubnetHyperparameters.user_liquidity_enabled`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.user_liquidity_enabled>)
      * [`SubnetHyperparameters.weights_rate_limit`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.weights_rate_limit>)
      * [`SubnetHyperparameters.weights_version`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.weights_version>)
      * [`SubnetHyperparameters.yuma_version`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.yuma_version>)



# bittensor.core.chain_data.subnet_hyperparameters[#](<#module-bittensor.core.chain_data.subnet_hyperparameters> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`SubnetHyperparameters`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters> "bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters") | This class represents the hyperparameters for a subnet.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters> "Link to this definition")
    

Bases: [`bittensor.core.chain_data.info_base.InfoBase`](<../info_base/index.html#bittensor.core.chain_data.info_base.InfoBase> "bittensor.core.chain_data.info_base.InfoBase")

This class represents the hyperparameters for a subnet.

Variables:
    

  * **rho** – The rate of decay of some value.

  * **kappa** – A constant multiplier used in calculations.

  * **immunity_period** – The period during which immunity is active.

  * **min_allowed_weights** – Minimum allowed weights.

  * **max_weight_limit** – Maximum weight limit.

  * **tempo** – The tempo or rate of operation.

  * **min_difficulty** – Minimum difficulty for some operations.

  * **max_difficulty** – Maximum difficulty for some operations.

  * **weights_version** – The version number of the weights used.

  * **weights_rate_limit** – Rate limit for processing weights.

  * **adjustment_interval** – Interval at which adjustments are made.

  * **activity_cutoff** – Activity cutoff threshold.

  * **registration_allowed** – Indicates if registration is allowed.

  * **target_regs_per_interval** – Target number of registrations per interval.

  * **min_burn** – Minimum burn value.

  * **max_burn** – Maximum burn value.

  * **bonds_moving_avg** – Moving average of bonds.

  * **max_regs_per_block** – Maximum number of registrations per block.

  * **serving_rate_limit** – Limit on the rate of service.

  * **max_validators** – Maximum number of validators.

  * **adjustment_alpha** – Alpha value for adjustments.

  * **difficulty** – Difficulty level.

  * **commit_reveal_period** – Interval for commit-reveal weights.

  * **commit_reveal_weights_enabled** – Flag indicating if commit-reveal weights are enabled.

  * **alpha_high** – High value of alpha.

  * **alpha_low** – Low value of alpha.

  * **liquid_alpha_enabled** – Flag indicating if liquid alpha is enabled.

  * **alpha_sigmoid_steepness** – Sigmoid steepness parameter for converting miner-validator alignment into alpha.

  * **yuma_version** – Version of yuma.

  * **subnet_is_active** – Indicates if subnet is active after START CALL.

  * **transfers_enabled** – Flag indicating if transfers are enabled.

  * **bonds_reset_enabled** – Flag indicating if bonds are reset enabled.

  * **user_liquidity_enabled** – Flag indicating if user liquidity is enabled.




activity_cutoff: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.activity_cutoff> "Link to this definition")
    

adjustment_alpha: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.adjustment_alpha> "Link to this definition")
    

adjustment_interval: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.adjustment_interval> "Link to this definition")
    

alpha_high: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.alpha_high> "Link to this definition")
    

alpha_low: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.alpha_low> "Link to this definition")
    

alpha_sigmoid_steepness: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.alpha_sigmoid_steepness> "Link to this definition")
    

bonds_moving_avg: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.bonds_moving_avg> "Link to this definition")
    

bonds_reset_enabled: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.bonds_reset_enabled> "Link to this definition")
    

commit_reveal_period: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.commit_reveal_period> "Link to this definition")
    

commit_reveal_weights_enabled: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.commit_reveal_weights_enabled> "Link to this definition")
    

difficulty: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.difficulty> "Link to this definition")
    

immunity_period: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.immunity_period> "Link to this definition")
    

kappa: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.kappa> "Link to this definition")
    

liquid_alpha_enabled: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.liquid_alpha_enabled> "Link to this definition")
    

max_burn: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.max_burn> "Link to this definition")
    

max_difficulty: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.max_difficulty> "Link to this definition")
    

max_regs_per_block: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.max_regs_per_block> "Link to this definition")
    

max_validators: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.max_validators> "Link to this definition")
    

max_weight_limit: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.max_weight_limit> "Link to this definition")
    

min_allowed_weights: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.min_allowed_weights> "Link to this definition")
    

min_burn: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.min_burn> "Link to this definition")
    

min_difficulty: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.min_difficulty> "Link to this definition")
    

registration_allowed: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.registration_allowed> "Link to this definition")
    

rho: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.rho> "Link to this definition")
    

serving_rate_limit: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.serving_rate_limit> "Link to this definition")
    

subnet_is_active: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.subnet_is_active> "Link to this definition")
    

target_regs_per_interval: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.target_regs_per_interval> "Link to this definition")
    

tempo: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.tempo> "Link to this definition")
    

transfers_enabled: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.transfers_enabled> "Link to this definition")
    

user_liquidity_enabled: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.user_liquidity_enabled> "Link to this definition")
    

weights_rate_limit: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.weights_rate_limit> "Link to this definition")
    

weights_version: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.weights_version> "Link to this definition")
    

yuma_version: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.yuma_version> "Link to this definition")
    

[ __ previous bittensor.core.chain_data.stake_info ](<../stake_info/index.html> "previous page") [ next bittensor.core.chain_data.subnet_identity __](<../subnet_identity/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`SubnetHyperparameters`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters>)
      * [`SubnetHyperparameters.activity_cutoff`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.activity_cutoff>)
      * [`SubnetHyperparameters.adjustment_alpha`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.adjustment_alpha>)
      * [`SubnetHyperparameters.adjustment_interval`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.adjustment_interval>)
      * [`SubnetHyperparameters.alpha_high`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.alpha_high>)
      * [`SubnetHyperparameters.alpha_low`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.alpha_low>)
      * [`SubnetHyperparameters.alpha_sigmoid_steepness`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.alpha_sigmoid_steepness>)
      * [`SubnetHyperparameters.bonds_moving_avg`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.bonds_moving_avg>)
      * [`SubnetHyperparameters.bonds_reset_enabled`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.bonds_reset_enabled>)
      * [`SubnetHyperparameters.commit_reveal_period`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.commit_reveal_period>)
      * [`SubnetHyperparameters.commit_reveal_weights_enabled`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.commit_reveal_weights_enabled>)
      * [`SubnetHyperparameters.difficulty`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.difficulty>)
      * [`SubnetHyperparameters.immunity_period`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.immunity_period>)
      * [`SubnetHyperparameters.kappa`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.kappa>)
      * [`SubnetHyperparameters.liquid_alpha_enabled`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.liquid_alpha_enabled>)
      * [`SubnetHyperparameters.max_burn`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.max_burn>)
      * [`SubnetHyperparameters.max_difficulty`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.max_difficulty>)
      * [`SubnetHyperparameters.max_regs_per_block`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.max_regs_per_block>)
      * [`SubnetHyperparameters.max_validators`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.max_validators>)
      * [`SubnetHyperparameters.max_weight_limit`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.max_weight_limit>)
      * [`SubnetHyperparameters.min_allowed_weights`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.min_allowed_weights>)
      * [`SubnetHyperparameters.min_burn`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.min_burn>)
      * [`SubnetHyperparameters.min_difficulty`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.min_difficulty>)
      * [`SubnetHyperparameters.registration_allowed`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.registration_allowed>)
      * [`SubnetHyperparameters.rho`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.rho>)
      * [`SubnetHyperparameters.serving_rate_limit`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.serving_rate_limit>)
      * [`SubnetHyperparameters.subnet_is_active`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.subnet_is_active>)
      * [`SubnetHyperparameters.target_regs_per_interval`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.target_regs_per_interval>)
      * [`SubnetHyperparameters.tempo`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.tempo>)
      * [`SubnetHyperparameters.transfers_enabled`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.transfers_enabled>)
      * [`SubnetHyperparameters.user_liquidity_enabled`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.user_liquidity_enabled>)
      * [`SubnetHyperparameters.weights_rate_limit`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.weights_rate_limit>)
      * [`SubnetHyperparameters.weights_version`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.weights_version>)
      * [`SubnetHyperparameters.yuma_version`](<#bittensor.core.chain_data.subnet_hyperparameters.SubnetHyperparameters.yuma_version>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.