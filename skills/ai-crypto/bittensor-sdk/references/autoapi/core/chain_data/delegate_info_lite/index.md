# bittensor.core.chain_data.delegate_info_lite &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/delegate_info_lite/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/delegate_info_lite/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/delegate_info_lite/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.delegate_info_lite

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`DelegateInfoLite`](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite>)
      * [`DelegateInfoLite.delegate_ss58`](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.delegate_ss58>)
      * [`DelegateInfoLite.nominators`](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.nominators>)
      * [`DelegateInfoLite.owner_ss58`](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.owner_ss58>)
      * [`DelegateInfoLite.registrations`](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.registrations>)
      * [`DelegateInfoLite.return_per_1000`](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.return_per_1000>)
      * [`DelegateInfoLite.take`](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.take>)
      * [`DelegateInfoLite.validator_permits`](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.validator_permits>)



# bittensor.core.chain_data.delegate_info_lite[#](<#module-bittensor.core.chain_data.delegate_info_lite> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`DelegateInfoLite`](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite> "bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite") | Dataclass for DelegateLiteInfo. This is a lighter version of :func:`DelegateInfo`.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite[#](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite> "Link to this definition")
    

Bases: [`bittensor.core.chain_data.info_base.InfoBase`](<../info_base/index.html#bittensor.core.chain_data.info_base.InfoBase> "bittensor.core.chain_data.info_base.InfoBase")

Dataclass for DelegateLiteInfo. This is a lighter version of :func:`DelegateInfo`.

Parameters:
    

  * **delegate_ss58** – Hotkey of the delegate for which the information is being fetched.

  * **take** – Take of the delegate as a percentage.

  * **nominators** – Count of the nominators of the delegate.

  * **owner_ss58** – Coldkey of the owner.

  * **registrations** – List of subnets that the delegate is registered on.

  * **validator_permits** – List of subnets that the delegate is allowed to validate on.

  * **return_per_1000** – Return per 1000 TAO, for the delegate over a day.




delegate_ss58: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.delegate_ss58> "Link to this definition")
    

nominators: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.nominators> "Link to this definition")
    

owner_ss58: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.owner_ss58> "Link to this definition")
    

registrations: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.registrations> "Link to this definition")
    

return_per_1000: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.return_per_1000> "Link to this definition")
    

take: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.take> "Link to this definition")
    

validator_permits: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.validator_permits> "Link to this definition")
    

[ __ previous bittensor.core.chain_data.delegate_info ](<../delegate_info/index.html> "previous page") [ next bittensor.core.chain_data.dynamic_info __](<../dynamic_info/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`DelegateInfoLite`](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite>)
      * [`DelegateInfoLite.delegate_ss58`](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.delegate_ss58>)
      * [`DelegateInfoLite.nominators`](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.nominators>)
      * [`DelegateInfoLite.owner_ss58`](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.owner_ss58>)
      * [`DelegateInfoLite.registrations`](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.registrations>)
      * [`DelegateInfoLite.return_per_1000`](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.return_per_1000>)
      * [`DelegateInfoLite.take`](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.take>)
      * [`DelegateInfoLite.validator_permits`](<#bittensor.core.chain_data.delegate_info_lite.DelegateInfoLite.validator_permits>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.