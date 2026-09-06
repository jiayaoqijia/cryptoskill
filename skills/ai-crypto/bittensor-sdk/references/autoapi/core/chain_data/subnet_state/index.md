# bittensor.core.chain_data.subnet_state &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/subnet_state/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/subnet_state/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/subnet_state/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.subnet_state

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`SubnetState`](<#bittensor.core.chain_data.subnet_state.SubnetState>)
      * [`SubnetState.active`](<#bittensor.core.chain_data.subnet_state.SubnetState.active>)
      * [`SubnetState.alpha_stake`](<#bittensor.core.chain_data.subnet_state.SubnetState.alpha_stake>)
      * [`SubnetState.block_at_registration`](<#bittensor.core.chain_data.subnet_state.SubnetState.block_at_registration>)
      * [`SubnetState.coldkeys`](<#bittensor.core.chain_data.subnet_state.SubnetState.coldkeys>)
      * [`SubnetState.consensus`](<#bittensor.core.chain_data.subnet_state.SubnetState.consensus>)
      * [`SubnetState.dividends`](<#bittensor.core.chain_data.subnet_state.SubnetState.dividends>)
      * [`SubnetState.emission`](<#bittensor.core.chain_data.subnet_state.SubnetState.emission>)
      * [`SubnetState.emission_history`](<#bittensor.core.chain_data.subnet_state.SubnetState.emission_history>)
      * [`SubnetState.hotkeys`](<#bittensor.core.chain_data.subnet_state.SubnetState.hotkeys>)
      * [`SubnetState.incentives`](<#bittensor.core.chain_data.subnet_state.SubnetState.incentives>)
      * [`SubnetState.last_update`](<#bittensor.core.chain_data.subnet_state.SubnetState.last_update>)
      * [`SubnetState.netuid`](<#bittensor.core.chain_data.subnet_state.SubnetState.netuid>)
      * [`SubnetState.pruning_score`](<#bittensor.core.chain_data.subnet_state.SubnetState.pruning_score>)
      * [`SubnetState.rank`](<#bittensor.core.chain_data.subnet_state.SubnetState.rank>)
      * [`SubnetState.tao_stake`](<#bittensor.core.chain_data.subnet_state.SubnetState.tao_stake>)
      * [`SubnetState.total_stake`](<#bittensor.core.chain_data.subnet_state.SubnetState.total_stake>)
      * [`SubnetState.trust`](<#bittensor.core.chain_data.subnet_state.SubnetState.trust>)
      * [`SubnetState.validator_permit`](<#bittensor.core.chain_data.subnet_state.SubnetState.validator_permit>)



# bittensor.core.chain_data.subnet_state[#](<#module-bittensor.core.chain_data.subnet_state> "Link to this heading")

This module defines the SubnetState data class and associated methods for handling and decoding subnetwork states in the Bittensor network.

## Classes[#](<#classes> "Link to this heading")

[`SubnetState`](<#bittensor.core.chain_data.subnet_state.SubnetState> "bittensor.core.chain_data.subnet_state.SubnetState") |   
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.subnet_state.SubnetState[#](<#bittensor.core.chain_data.subnet_state.SubnetState> "Link to this definition")
    

Bases: [`bittensor.core.chain_data.info_base.InfoBase`](<../info_base/index.html#bittensor.core.chain_data.info_base.InfoBase> "bittensor.core.chain_data.info_base.InfoBase")

active: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.subnet_state.SubnetState.active> "Link to this definition")
    

alpha_stake: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")][#](<#bittensor.core.chain_data.subnet_state.SubnetState.alpha_stake> "Link to this definition")
    

block_at_registration: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.subnet_state.SubnetState.block_at_registration> "Link to this definition")
    

coldkeys: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.subnet_state.SubnetState.coldkeys> "Link to this definition")
    

consensus: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.subnet_state.SubnetState.consensus> "Link to this definition")
    

dividends: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.subnet_state.SubnetState.dividends> "Link to this definition")
    

emission: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")][#](<#bittensor.core.chain_data.subnet_state.SubnetState.emission> "Link to this definition")
    

emission_history: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]][#](<#bittensor.core.chain_data.subnet_state.SubnetState.emission_history> "Link to this definition")
    

hotkeys: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.subnet_state.SubnetState.hotkeys> "Link to this definition")
    

incentives: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.subnet_state.SubnetState.incentives> "Link to this definition")
    

last_update: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.subnet_state.SubnetState.last_update> "Link to this definition")
    

netuid: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.subnet_state.SubnetState.netuid> "Link to this definition")
    

pruning_score: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.subnet_state.SubnetState.pruning_score> "Link to this definition")
    

rank: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.subnet_state.SubnetState.rank> "Link to this definition")
    

tao_stake: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")][#](<#bittensor.core.chain_data.subnet_state.SubnetState.tao_stake> "Link to this definition")
    

total_stake: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")][#](<#bittensor.core.chain_data.subnet_state.SubnetState.total_stake> "Link to this definition")
    

trust: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.subnet_state.SubnetState.trust> "Link to this definition")
    

validator_permit: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.subnet_state.SubnetState.validator_permit> "Link to this definition")
    

[ __ previous bittensor.core.chain_data.subnet_info ](<../subnet_info/index.html> "previous page") [ next bittensor.core.chain_data.utils __](<../utils/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`SubnetState`](<#bittensor.core.chain_data.subnet_state.SubnetState>)
      * [`SubnetState.active`](<#bittensor.core.chain_data.subnet_state.SubnetState.active>)
      * [`SubnetState.alpha_stake`](<#bittensor.core.chain_data.subnet_state.SubnetState.alpha_stake>)
      * [`SubnetState.block_at_registration`](<#bittensor.core.chain_data.subnet_state.SubnetState.block_at_registration>)
      * [`SubnetState.coldkeys`](<#bittensor.core.chain_data.subnet_state.SubnetState.coldkeys>)
      * [`SubnetState.consensus`](<#bittensor.core.chain_data.subnet_state.SubnetState.consensus>)
      * [`SubnetState.dividends`](<#bittensor.core.chain_data.subnet_state.SubnetState.dividends>)
      * [`SubnetState.emission`](<#bittensor.core.chain_data.subnet_state.SubnetState.emission>)
      * [`SubnetState.emission_history`](<#bittensor.core.chain_data.subnet_state.SubnetState.emission_history>)
      * [`SubnetState.hotkeys`](<#bittensor.core.chain_data.subnet_state.SubnetState.hotkeys>)
      * [`SubnetState.incentives`](<#bittensor.core.chain_data.subnet_state.SubnetState.incentives>)
      * [`SubnetState.last_update`](<#bittensor.core.chain_data.subnet_state.SubnetState.last_update>)
      * [`SubnetState.netuid`](<#bittensor.core.chain_data.subnet_state.SubnetState.netuid>)
      * [`SubnetState.pruning_score`](<#bittensor.core.chain_data.subnet_state.SubnetState.pruning_score>)
      * [`SubnetState.rank`](<#bittensor.core.chain_data.subnet_state.SubnetState.rank>)
      * [`SubnetState.tao_stake`](<#bittensor.core.chain_data.subnet_state.SubnetState.tao_stake>)
      * [`SubnetState.total_stake`](<#bittensor.core.chain_data.subnet_state.SubnetState.total_stake>)
      * [`SubnetState.trust`](<#bittensor.core.chain_data.subnet_state.SubnetState.trust>)
      * [`SubnetState.validator_permit`](<#bittensor.core.chain_data.subnet_state.SubnetState.validator_permit>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.