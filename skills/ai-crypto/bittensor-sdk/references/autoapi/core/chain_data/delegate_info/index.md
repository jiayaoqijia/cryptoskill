# bittensor.core.chain_data.delegate_info &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/delegate_info/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/delegate_info/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/delegate_info/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.delegate_info

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`DelegateInfo`](<#bittensor.core.chain_data.delegate_info.DelegateInfo>)
      * [`DelegateInfo.nominators`](<#bittensor.core.chain_data.delegate_info.DelegateInfo.nominators>)
      * [`DelegateInfo.total_stake`](<#bittensor.core.chain_data.delegate_info.DelegateInfo.total_stake>)
    * [`DelegateInfoBase`](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase>)
      * [`DelegateInfoBase.hotkey_ss58`](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase.hotkey_ss58>)
      * [`DelegateInfoBase.owner_ss58`](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase.owner_ss58>)
      * [`DelegateInfoBase.registrations`](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase.registrations>)
      * [`DelegateInfoBase.return_per_1000`](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase.return_per_1000>)
      * [`DelegateInfoBase.take`](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase.take>)
      * [`DelegateInfoBase.validator_permits`](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase.validator_permits>)
    * [`DelegatedInfo`](<#bittensor.core.chain_data.delegate_info.DelegatedInfo>)
      * [`DelegatedInfo.netuid`](<#bittensor.core.chain_data.delegate_info.DelegatedInfo.netuid>)
      * [`DelegatedInfo.stake`](<#bittensor.core.chain_data.delegate_info.DelegatedInfo.stake>)



# bittensor.core.chain_data.delegate_info[#](<#module-bittensor.core.chain_data.delegate_info> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`DelegateInfo`](<#bittensor.core.chain_data.delegate_info.DelegateInfo> "bittensor.core.chain_data.delegate_info.DelegateInfo") | Dataclass for delegate information.  
---|---  
[`DelegateInfoBase`](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase> "bittensor.core.chain_data.delegate_info.DelegateInfoBase") | Base class containing common delegate information fields.  
[`DelegatedInfo`](<#bittensor.core.chain_data.delegate_info.DelegatedInfo> "bittensor.core.chain_data.delegate_info.DelegatedInfo") | Dataclass for delegated information. This class represents a delegate's information specific to a particular subnet.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.delegate_info.DelegateInfo[#](<#bittensor.core.chain_data.delegate_info.DelegateInfo> "Link to this definition")
    

Bases: [`DelegateInfoBase`](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase> "bittensor.core.chain_data.delegate_info.DelegateInfoBase")

Dataclass for delegate information.

Additional Attributes:
    

total_stake: Total stake of the delegate mapped by netuid. nominators: Mapping of nominator SS58 addresses to their stakes per subnet.

nominators: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")]][#](<#bittensor.core.chain_data.delegate_info.DelegateInfo.nominators> "Link to this definition")
    

total_stake: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")][#](<#bittensor.core.chain_data.delegate_info.DelegateInfo.total_stake> "Link to this definition")
    

class bittensor.core.chain_data.delegate_info.DelegateInfoBase[#](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase> "Link to this definition")
    

Bases: [`bittensor.core.chain_data.info_base.InfoBase`](<../info_base/index.html#bittensor.core.chain_data.info_base.InfoBase> "bittensor.core.chain_data.info_base.InfoBase")

Base class containing common delegate information fields.

Variables:
    

  * **hotkey_ss58** – Hotkey of delegate.

  * **owner_ss58** – Coldkey of owner.

  * **take** – Take of the delegate as a percentage.

  * **validator_permits** – List of subnets that the delegate is allowed to validate on.

  * **registrations** – List of subnets that the delegate is registered on.

  * **return_per_1000** – Return per 1000 tao of the delegate over a day.




hotkey_ss58: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase.hotkey_ss58> "Link to this definition")
    

owner_ss58: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase.owner_ss58> "Link to this definition")
    

registrations: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase.registrations> "Link to this definition")
    

return_per_1000: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase.return_per_1000> "Link to this definition")
    

take: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase.take> "Link to this definition")
    

validator_permits: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase.validator_permits> "Link to this definition")
    

class bittensor.core.chain_data.delegate_info.DelegatedInfo[#](<#bittensor.core.chain_data.delegate_info.DelegatedInfo> "Link to this definition")
    

Bases: [`DelegateInfoBase`](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase> "bittensor.core.chain_data.delegate_info.DelegateInfoBase")

Dataclass for delegated information. This class represents a delegate’s information specific to a particular subnet.

Additional Attributes:
    

netuid: Network ID of the subnet. stake: Stake amount for this specific delegation.

netuid: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.delegate_info.DelegatedInfo.netuid> "Link to this definition")
    

stake: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.delegate_info.DelegatedInfo.stake> "Link to this definition")
    

[ __ previous bittensor.core.chain_data.crowdloan_info ](<../crowdloan_info/index.html> "previous page") [ next bittensor.core.chain_data.delegate_info_lite __](<../delegate_info_lite/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`DelegateInfo`](<#bittensor.core.chain_data.delegate_info.DelegateInfo>)
      * [`DelegateInfo.nominators`](<#bittensor.core.chain_data.delegate_info.DelegateInfo.nominators>)
      * [`DelegateInfo.total_stake`](<#bittensor.core.chain_data.delegate_info.DelegateInfo.total_stake>)
    * [`DelegateInfoBase`](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase>)
      * [`DelegateInfoBase.hotkey_ss58`](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase.hotkey_ss58>)
      * [`DelegateInfoBase.owner_ss58`](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase.owner_ss58>)
      * [`DelegateInfoBase.registrations`](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase.registrations>)
      * [`DelegateInfoBase.return_per_1000`](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase.return_per_1000>)
      * [`DelegateInfoBase.take`](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase.take>)
      * [`DelegateInfoBase.validator_permits`](<#bittensor.core.chain_data.delegate_info.DelegateInfoBase.validator_permits>)
    * [`DelegatedInfo`](<#bittensor.core.chain_data.delegate_info.DelegatedInfo>)
      * [`DelegatedInfo.netuid`](<#bittensor.core.chain_data.delegate_info.DelegatedInfo.netuid>)
      * [`DelegatedInfo.stake`](<#bittensor.core.chain_data.delegate_info.DelegatedInfo.stake>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.