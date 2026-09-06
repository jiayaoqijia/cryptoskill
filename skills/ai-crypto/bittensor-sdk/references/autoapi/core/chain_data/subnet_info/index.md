# bittensor.core.chain_data.subnet_info &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/subnet_info/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/subnet_info/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/subnet_info/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.subnet_info

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`SubnetInfo`](<#bittensor.core.chain_data.subnet_info.SubnetInfo>)
      * [`SubnetInfo.blocks_since_epoch`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.blocks_since_epoch>)
      * [`SubnetInfo.burn`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.burn>)
      * [`SubnetInfo.connection_requirements`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.connection_requirements>)
      * [`SubnetInfo.difficulty`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.difficulty>)
      * [`SubnetInfo.emission_value`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.emission_value>)
      * [`SubnetInfo.immunity_period`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.immunity_period>)
      * [`SubnetInfo.kappa`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.kappa>)
      * [`SubnetInfo.max_allowed_validators`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.max_allowed_validators>)
      * [`SubnetInfo.max_n`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.max_n>)
      * [`SubnetInfo.max_weight_limit`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.max_weight_limit>)
      * [`SubnetInfo.min_allowed_weights`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.min_allowed_weights>)
      * [`SubnetInfo.modality`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.modality>)
      * [`SubnetInfo.netuid`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.netuid>)
      * [`SubnetInfo.owner_ss58`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.owner_ss58>)
      * [`SubnetInfo.rho`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.rho>)
      * [`SubnetInfo.scaling_law_power`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.scaling_law_power>)
      * [`SubnetInfo.subnetwork_n`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.subnetwork_n>)
      * [`SubnetInfo.tempo`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.tempo>)



# bittensor.core.chain_data.subnet_info[#](<#module-bittensor.core.chain_data.subnet_info> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`SubnetInfo`](<#bittensor.core.chain_data.subnet_info.SubnetInfo> "bittensor.core.chain_data.subnet_info.SubnetInfo") | Dataclass for subnet info.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.subnet_info.SubnetInfo[#](<#bittensor.core.chain_data.subnet_info.SubnetInfo> "Link to this definition")
    

Bases: [`bittensor.core.chain_data.info_base.InfoBase`](<../info_base/index.html#bittensor.core.chain_data.info_base.InfoBase> "bittensor.core.chain_data.info_base.InfoBase")

Dataclass for subnet info.

blocks_since_epoch: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_info.SubnetInfo.blocks_since_epoch> "Link to this definition")
    

burn: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.subnet_info.SubnetInfo.burn> "Link to this definition")
    

connection_requirements: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.subnet_info.SubnetInfo.connection_requirements> "Link to this definition")
    

difficulty: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_info.SubnetInfo.difficulty> "Link to this definition")
    

emission_value: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_info.SubnetInfo.emission_value> "Link to this definition")
    

immunity_period: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_info.SubnetInfo.immunity_period> "Link to this definition")
    

kappa: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_info.SubnetInfo.kappa> "Link to this definition")
    

max_allowed_validators: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_info.SubnetInfo.max_allowed_validators> "Link to this definition")
    

max_n: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_info.SubnetInfo.max_n> "Link to this definition")
    

max_weight_limit: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_info.SubnetInfo.max_weight_limit> "Link to this definition")
    

min_allowed_weights: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_info.SubnetInfo.min_allowed_weights> "Link to this definition")
    

modality: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_info.SubnetInfo.modality> "Link to this definition")
    

netuid: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_info.SubnetInfo.netuid> "Link to this definition")
    

owner_ss58: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_info.SubnetInfo.owner_ss58> "Link to this definition")
    

rho: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_info.SubnetInfo.rho> "Link to this definition")
    

scaling_law_power: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_info.SubnetInfo.scaling_law_power> "Link to this definition")
    

subnetwork_n: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_info.SubnetInfo.subnetwork_n> "Link to this definition")
    

tempo: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_info.SubnetInfo.tempo> "Link to this definition")
    

[ __ previous bittensor.core.chain_data.subnet_identity ](<../subnet_identity/index.html> "previous page") [ next bittensor.core.chain_data.subnet_state __](<../subnet_state/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`SubnetInfo`](<#bittensor.core.chain_data.subnet_info.SubnetInfo>)
      * [`SubnetInfo.blocks_since_epoch`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.blocks_since_epoch>)
      * [`SubnetInfo.burn`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.burn>)
      * [`SubnetInfo.connection_requirements`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.connection_requirements>)
      * [`SubnetInfo.difficulty`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.difficulty>)
      * [`SubnetInfo.emission_value`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.emission_value>)
      * [`SubnetInfo.immunity_period`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.immunity_period>)
      * [`SubnetInfo.kappa`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.kappa>)
      * [`SubnetInfo.max_allowed_validators`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.max_allowed_validators>)
      * [`SubnetInfo.max_n`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.max_n>)
      * [`SubnetInfo.max_weight_limit`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.max_weight_limit>)
      * [`SubnetInfo.min_allowed_weights`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.min_allowed_weights>)
      * [`SubnetInfo.modality`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.modality>)
      * [`SubnetInfo.netuid`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.netuid>)
      * [`SubnetInfo.owner_ss58`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.owner_ss58>)
      * [`SubnetInfo.rho`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.rho>)
      * [`SubnetInfo.scaling_law_power`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.scaling_law_power>)
      * [`SubnetInfo.subnetwork_n`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.subnetwork_n>)
      * [`SubnetInfo.tempo`](<#bittensor.core.chain_data.subnet_info.SubnetInfo.tempo>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.