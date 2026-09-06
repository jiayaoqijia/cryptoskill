# bittensor.extras.dev_framework.calls.pallets &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/extras/dev_framework/calls/pallets/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/extras/dev_framework/calls/pallets/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../../_sources/autoapi/bittensor/extras/dev_framework/calls/pallets/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.extras.dev_framework.calls.pallets

##  Contents 

  * [Attributes](<#attributes>)
  * [Module Contents](<#module-contents>)
    * [`AdminUtils`](<#bittensor.extras.dev_framework.calls.pallets.AdminUtils>)
    * [`Balances`](<#bittensor.extras.dev_framework.calls.pallets.Balances>)
    * [`BaseFee`](<#bittensor.extras.dev_framework.calls.pallets.BaseFee>)
    * [`Commitments`](<#bittensor.extras.dev_framework.calls.pallets.Commitments>)
    * [`Contracts`](<#bittensor.extras.dev_framework.calls.pallets.Contracts>)
    * [`Crowdloan`](<#bittensor.extras.dev_framework.calls.pallets.Crowdloan>)
    * [`Drand`](<#bittensor.extras.dev_framework.calls.pallets.Drand>)
    * [`EVM`](<#bittensor.extras.dev_framework.calls.pallets.EVM>)
    * [`Ethereum`](<#bittensor.extras.dev_framework.calls.pallets.Ethereum>)
    * [`Grandpa`](<#bittensor.extras.dev_framework.calls.pallets.Grandpa>)
    * [`MevShield`](<#bittensor.extras.dev_framework.calls.pallets.MevShield>)
    * [`Multisig`](<#bittensor.extras.dev_framework.calls.pallets.Multisig>)
    * [`Preimage`](<#bittensor.extras.dev_framework.calls.pallets.Preimage>)
    * [`Proxy`](<#bittensor.extras.dev_framework.calls.pallets.Proxy>)
    * [`Registry`](<#bittensor.extras.dev_framework.calls.pallets.Registry>)
    * [`SafeMode`](<#bittensor.extras.dev_framework.calls.pallets.SafeMode>)
    * [`Scheduler`](<#bittensor.extras.dev_framework.calls.pallets.Scheduler>)
    * [`SubtensorModule`](<#bittensor.extras.dev_framework.calls.pallets.SubtensorModule>)
    * [`Sudo`](<#bittensor.extras.dev_framework.calls.pallets.Sudo>)
    * [`Swap`](<#bittensor.extras.dev_framework.calls.pallets.Swap>)
    * [`System`](<#bittensor.extras.dev_framework.calls.pallets.System>)
    * [`Timestamp`](<#bittensor.extras.dev_framework.calls.pallets.Timestamp>)
    * [`Utility`](<#bittensor.extras.dev_framework.calls.pallets.Utility>)



# bittensor.extras.dev_framework.calls.pallets[#](<#module-bittensor.extras.dev_framework.calls.pallets> "Link to this heading")

” Subtensor spec version: 397

## Attributes[#](<#attributes> "Link to this heading")

[`AdminUtils`](<#bittensor.extras.dev_framework.calls.pallets.AdminUtils> "bittensor.extras.dev_framework.calls.pallets.AdminUtils") |   
---|---  
[`Balances`](<#bittensor.extras.dev_framework.calls.pallets.Balances> "bittensor.extras.dev_framework.calls.pallets.Balances") |   
[`BaseFee`](<#bittensor.extras.dev_framework.calls.pallets.BaseFee> "bittensor.extras.dev_framework.calls.pallets.BaseFee") |   
[`Commitments`](<#bittensor.extras.dev_framework.calls.pallets.Commitments> "bittensor.extras.dev_framework.calls.pallets.Commitments") |   
[`Contracts`](<#bittensor.extras.dev_framework.calls.pallets.Contracts> "bittensor.extras.dev_framework.calls.pallets.Contracts") |   
[`Crowdloan`](<#bittensor.extras.dev_framework.calls.pallets.Crowdloan> "bittensor.extras.dev_framework.calls.pallets.Crowdloan") |   
[`Drand`](<#bittensor.extras.dev_framework.calls.pallets.Drand> "bittensor.extras.dev_framework.calls.pallets.Drand") |   
[`EVM`](<#bittensor.extras.dev_framework.calls.pallets.EVM> "bittensor.extras.dev_framework.calls.pallets.EVM") |   
[`Ethereum`](<#bittensor.extras.dev_framework.calls.pallets.Ethereum> "bittensor.extras.dev_framework.calls.pallets.Ethereum") |   
[`Grandpa`](<#bittensor.extras.dev_framework.calls.pallets.Grandpa> "bittensor.extras.dev_framework.calls.pallets.Grandpa") |   
[`MevShield`](<#bittensor.extras.dev_framework.calls.pallets.MevShield> "bittensor.extras.dev_framework.calls.pallets.MevShield") |   
[`Multisig`](<#bittensor.extras.dev_framework.calls.pallets.Multisig> "bittensor.extras.dev_framework.calls.pallets.Multisig") |   
[`Preimage`](<#bittensor.extras.dev_framework.calls.pallets.Preimage> "bittensor.extras.dev_framework.calls.pallets.Preimage") |   
[`Proxy`](<#bittensor.extras.dev_framework.calls.pallets.Proxy> "bittensor.extras.dev_framework.calls.pallets.Proxy") |   
[`Registry`](<#bittensor.extras.dev_framework.calls.pallets.Registry> "bittensor.extras.dev_framework.calls.pallets.Registry") |   
[`SafeMode`](<#bittensor.extras.dev_framework.calls.pallets.SafeMode> "bittensor.extras.dev_framework.calls.pallets.SafeMode") |   
[`Scheduler`](<#bittensor.extras.dev_framework.calls.pallets.Scheduler> "bittensor.extras.dev_framework.calls.pallets.Scheduler") |   
[`SubtensorModule`](<#bittensor.extras.dev_framework.calls.pallets.SubtensorModule> "bittensor.extras.dev_framework.calls.pallets.SubtensorModule") |   
[`Sudo`](<#bittensor.extras.dev_framework.calls.pallets.Sudo> "bittensor.extras.dev_framework.calls.pallets.Sudo") |   
[`Swap`](<#bittensor.extras.dev_framework.calls.pallets.Swap> "bittensor.extras.dev_framework.calls.pallets.Swap") |   
[`System`](<#bittensor.extras.dev_framework.calls.pallets.System> "bittensor.extras.dev_framework.calls.pallets.System") |   
[`Timestamp`](<#bittensor.extras.dev_framework.calls.pallets.Timestamp> "bittensor.extras.dev_framework.calls.pallets.Timestamp") |   
[`Utility`](<#bittensor.extras.dev_framework.calls.pallets.Utility> "bittensor.extras.dev_framework.calls.pallets.Utility") |   
  
## Module Contents[#](<#module-contents> "Link to this heading")

bittensor.extras.dev_framework.calls.pallets.AdminUtils = 'AdminUtils'[#](<#bittensor.extras.dev_framework.calls.pallets.AdminUtils> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.Balances = 'Balances'[#](<#bittensor.extras.dev_framework.calls.pallets.Balances> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.BaseFee = 'BaseFee'[#](<#bittensor.extras.dev_framework.calls.pallets.BaseFee> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.Commitments = 'Commitments'[#](<#bittensor.extras.dev_framework.calls.pallets.Commitments> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.Contracts = 'Contracts'[#](<#bittensor.extras.dev_framework.calls.pallets.Contracts> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.Crowdloan = 'Crowdloan'[#](<#bittensor.extras.dev_framework.calls.pallets.Crowdloan> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.Drand = 'Drand'[#](<#bittensor.extras.dev_framework.calls.pallets.Drand> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.EVM = 'EVM'[#](<#bittensor.extras.dev_framework.calls.pallets.EVM> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.Ethereum = 'Ethereum'[#](<#bittensor.extras.dev_framework.calls.pallets.Ethereum> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.Grandpa = 'Grandpa'[#](<#bittensor.extras.dev_framework.calls.pallets.Grandpa> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.MevShield = 'MevShield'[#](<#bittensor.extras.dev_framework.calls.pallets.MevShield> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.Multisig = 'Multisig'[#](<#bittensor.extras.dev_framework.calls.pallets.Multisig> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.Preimage = 'Preimage'[#](<#bittensor.extras.dev_framework.calls.pallets.Preimage> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.Proxy = 'Proxy'[#](<#bittensor.extras.dev_framework.calls.pallets.Proxy> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.Registry = 'Registry'[#](<#bittensor.extras.dev_framework.calls.pallets.Registry> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.SafeMode = 'SafeMode'[#](<#bittensor.extras.dev_framework.calls.pallets.SafeMode> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.Scheduler = 'Scheduler'[#](<#bittensor.extras.dev_framework.calls.pallets.Scheduler> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.SubtensorModule = 'SubtensorModule'[#](<#bittensor.extras.dev_framework.calls.pallets.SubtensorModule> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.Sudo = 'Sudo'[#](<#bittensor.extras.dev_framework.calls.pallets.Sudo> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.Swap = 'Swap'[#](<#bittensor.extras.dev_framework.calls.pallets.Swap> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.System = 'System'[#](<#bittensor.extras.dev_framework.calls.pallets.System> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.Timestamp = 'Timestamp'[#](<#bittensor.extras.dev_framework.calls.pallets.Timestamp> "Link to this definition")
    

bittensor.extras.dev_framework.calls.pallets.Utility = 'Utility'[#](<#bittensor.extras.dev_framework.calls.pallets.Utility> "Link to this definition")
    

[ __ previous bittensor.extras.dev_framework.calls.non_sudo_calls ](<../non_sudo_calls/index.html> "previous page") [ next bittensor.extras.dev_framework.calls.sudo_calls __](<../sudo_calls/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Module Contents](<#module-contents>)
    * [`AdminUtils`](<#bittensor.extras.dev_framework.calls.pallets.AdminUtils>)
    * [`Balances`](<#bittensor.extras.dev_framework.calls.pallets.Balances>)
    * [`BaseFee`](<#bittensor.extras.dev_framework.calls.pallets.BaseFee>)
    * [`Commitments`](<#bittensor.extras.dev_framework.calls.pallets.Commitments>)
    * [`Contracts`](<#bittensor.extras.dev_framework.calls.pallets.Contracts>)
    * [`Crowdloan`](<#bittensor.extras.dev_framework.calls.pallets.Crowdloan>)
    * [`Drand`](<#bittensor.extras.dev_framework.calls.pallets.Drand>)
    * [`EVM`](<#bittensor.extras.dev_framework.calls.pallets.EVM>)
    * [`Ethereum`](<#bittensor.extras.dev_framework.calls.pallets.Ethereum>)
    * [`Grandpa`](<#bittensor.extras.dev_framework.calls.pallets.Grandpa>)
    * [`MevShield`](<#bittensor.extras.dev_framework.calls.pallets.MevShield>)
    * [`Multisig`](<#bittensor.extras.dev_framework.calls.pallets.Multisig>)
    * [`Preimage`](<#bittensor.extras.dev_framework.calls.pallets.Preimage>)
    * [`Proxy`](<#bittensor.extras.dev_framework.calls.pallets.Proxy>)
    * [`Registry`](<#bittensor.extras.dev_framework.calls.pallets.Registry>)
    * [`SafeMode`](<#bittensor.extras.dev_framework.calls.pallets.SafeMode>)
    * [`Scheduler`](<#bittensor.extras.dev_framework.calls.pallets.Scheduler>)
    * [`SubtensorModule`](<#bittensor.extras.dev_framework.calls.pallets.SubtensorModule>)
    * [`Sudo`](<#bittensor.extras.dev_framework.calls.pallets.Sudo>)
    * [`Swap`](<#bittensor.extras.dev_framework.calls.pallets.Swap>)
    * [`System`](<#bittensor.extras.dev_framework.calls.pallets.System>)
    * [`Timestamp`](<#bittensor.extras.dev_framework.calls.pallets.Timestamp>)
    * [`Utility`](<#bittensor.extras.dev_framework.calls.pallets.Utility>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.