# bittensor.core.chain_data.crowdloan_info &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/crowdloan_info/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/crowdloan_info/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/crowdloan_info/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.crowdloan_info

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`CrowdloanConstants`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants>)
      * [`CrowdloanConstants.AbsoluteMinimumContribution`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.AbsoluteMinimumContribution>)
      * [`CrowdloanConstants.MaxContributors`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.MaxContributors>)
      * [`CrowdloanConstants.MaximumBlockDuration`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.MaximumBlockDuration>)
      * [`CrowdloanConstants.MinimumBlockDuration`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.MinimumBlockDuration>)
      * [`CrowdloanConstants.MinimumDeposit`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.MinimumDeposit>)
      * [`CrowdloanConstants.RefundContributorsLimit`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.RefundContributorsLimit>)
      * [`CrowdloanConstants.constants_names()`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.constants_names>)
      * [`CrowdloanConstants.from_dict()`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.from_dict>)
    * [`CrowdloanInfo`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo>)
      * [`CrowdloanInfo.call`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.call>)
      * [`CrowdloanInfo.cap`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.cap>)
      * [`CrowdloanInfo.contributors_count`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.contributors_count>)
      * [`CrowdloanInfo.creator`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.creator>)
      * [`CrowdloanInfo.deposit`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.deposit>)
      * [`CrowdloanInfo.end`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.end>)
      * [`CrowdloanInfo.finalized`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.finalized>)
      * [`CrowdloanInfo.from_dict()`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.from_dict>)
      * [`CrowdloanInfo.funds_account`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.funds_account>)
      * [`CrowdloanInfo.id`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.id>)
      * [`CrowdloanInfo.min_contribution`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.min_contribution>)
      * [`CrowdloanInfo.raised`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.raised>)
      * [`CrowdloanInfo.target_address`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.target_address>)



# bittensor.core.chain_data.crowdloan_info[#](<#module-bittensor.core.chain_data.crowdloan_info> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`CrowdloanConstants`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants> "bittensor.core.chain_data.crowdloan_info.CrowdloanConstants") | Represents all runtime constants defined in the pallet-crowdloan.  
---|---  
[`CrowdloanInfo`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo> "bittensor.core.chain_data.crowdloan_info.CrowdloanInfo") | Represents a single on-chain crowdloan campaign from the pallet-crowdloan.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.crowdloan_info.CrowdloanConstants[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants> "Link to this definition")
    

Represents all runtime constants defined in the pallet-crowdloan.

These attributes correspond directly to on-chain configuration constants exposed by the Crowdloan pallet. They define contribution limits, duration bounds, pallet identifiers, and refund behavior that govern how crowdloan campaigns operate within the Subtensor network.

Each attribute is fetched directly from the runtime via Subtensor.substrate.get_constant(“Crowdloan”, <name>) and reflects the current chain configuration at the time of retrieval.

Variables:
    

  * **AbsoluteMinimumContribution** – The absolute minimum amount required to contribute to any crowdloan.

  * **MaxContributors** – The maximum number of unique contributors allowed per crowdloan.

  * **MaximumBlockDuration** – The maximum allowed duration (in blocks) for a crowdloan campaign.

  * **MinimumDeposit** – The minimum deposit required from the creator to open a new crowdloan.

  * **MinimumBlockDuration** – The minimum allowed duration (in blocks) for a crowdloan campaign.

  * **RefundContributorsLimit** – The maximum number of contributors that can be refunded in single on-chain refund call.




Note

All Balance amounts are in RAO.

AbsoluteMinimumContribution: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.AbsoluteMinimumContribution> "Link to this definition")
    

MaxContributors: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.MaxContributors> "Link to this definition")
    

MaximumBlockDuration: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.MaximumBlockDuration> "Link to this definition")
    

MinimumBlockDuration: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.MinimumBlockDuration> "Link to this definition")
    

MinimumDeposit: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.MinimumDeposit> "Link to this definition")
    

RefundContributorsLimit: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.RefundContributorsLimit> "Link to this definition")
    

classmethod constants_names()[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.constants_names> "Link to this definition")
    

Returns the list of all constant field names defined in this dataclass.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]

classmethod from_dict(_data_)[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.from_dict> "Link to this definition")
    

Creates a CrowdloanConstants instance from a dictionary of decoded chain constants.

Parameters:
    

**data** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")) – Dictionary mapping constant names to their decoded values (returned by Subtensor.query_constant()).

Returns:
    

The structured dataclass with constants filled in.

Return type:
    

[CrowdloanConstants](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants> "bittensor.core.chain_data.crowdloan_info.CrowdloanConstants")

class bittensor.core.chain_data.crowdloan_info.CrowdloanInfo[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo> "Link to this definition")
    

Represents a single on-chain crowdloan campaign from the pallet-crowdloan.

Each instance reflects the current state of a specific crowdloan as stored in chain storage. It includes funding details, creator information, contribution totals, and optional call/target data that define what happens upon successful finalization.

Variables:
    

  * **id** – The unique identifier (index) of the crowdloan.

  * **creator** – The SS58 address of the creator (campaign initiator).

  * **deposit** – The creator’s initial deposit locked to open the crowdloan.

  * **min_contribution** – The minimum contribution amount allowed per participant.

  * **end** – The block number when the campaign ends.

  * **cap** – The maximum amount to be raised (funding cap).

  * **funds_account** – The account ID holding the crowdloan’s funds.

  * **raised** – The total amount raised so far.

  * **target_address** – Optional SS58 address to which funds are transferred upon success.

  * **call** – Optional encoded runtime call (e.g., a register_leased_network extrinsic) to execute on finalize.

  * **finalized** – Whether the crowdloan has been finalized on-chain.

  * **contributors_count** – Number of unique contributors currently participating.




call: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.call> "Link to this definition")
    

cap: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.cap> "Link to this definition")
    

contributors_count: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.contributors_count> "Link to this definition")
    

creator: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.creator> "Link to this definition")
    

deposit: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.deposit> "Link to this definition")
    

end: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.end> "Link to this definition")
    

finalized: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.finalized> "Link to this definition")
    

classmethod from_dict(_idx_ , _data_)[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.from_dict> "Link to this definition")
    

Returns a CrowdloanInfo object from decoded chain data.

Parameters:
    

  * **idx** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

  * **data** ([_bittensor.core.types.CrowdloansResponse_](<../../types/index.html#bittensor.core.types.CrowdloansResponse> "bittensor.core.types.CrowdloansResponse"))



Return type:
    

[CrowdloanInfo](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo> "bittensor.core.chain_data.crowdloan_info.CrowdloanInfo")

funds_account: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.funds_account> "Link to this definition")
    

id: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.id> "Link to this definition")
    

min_contribution: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.min_contribution> "Link to this definition")
    

raised: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.raised> "Link to this definition")
    

target_address: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.target_address> "Link to this definition")
    

[ __ previous bittensor.core.chain_data.coldkey_swap ](<../coldkey_swap/index.html> "previous page") [ next bittensor.core.chain_data.delegate_info __](<../delegate_info/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`CrowdloanConstants`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants>)
      * [`CrowdloanConstants.AbsoluteMinimumContribution`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.AbsoluteMinimumContribution>)
      * [`CrowdloanConstants.MaxContributors`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.MaxContributors>)
      * [`CrowdloanConstants.MaximumBlockDuration`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.MaximumBlockDuration>)
      * [`CrowdloanConstants.MinimumBlockDuration`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.MinimumBlockDuration>)
      * [`CrowdloanConstants.MinimumDeposit`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.MinimumDeposit>)
      * [`CrowdloanConstants.RefundContributorsLimit`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.RefundContributorsLimit>)
      * [`CrowdloanConstants.constants_names()`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.constants_names>)
      * [`CrowdloanConstants.from_dict()`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanConstants.from_dict>)
    * [`CrowdloanInfo`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo>)
      * [`CrowdloanInfo.call`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.call>)
      * [`CrowdloanInfo.cap`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.cap>)
      * [`CrowdloanInfo.contributors_count`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.contributors_count>)
      * [`CrowdloanInfo.creator`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.creator>)
      * [`CrowdloanInfo.deposit`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.deposit>)
      * [`CrowdloanInfo.end`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.end>)
      * [`CrowdloanInfo.finalized`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.finalized>)
      * [`CrowdloanInfo.from_dict()`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.from_dict>)
      * [`CrowdloanInfo.funds_account`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.funds_account>)
      * [`CrowdloanInfo.id`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.id>)
      * [`CrowdloanInfo.min_contribution`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.min_contribution>)
      * [`CrowdloanInfo.raised`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.raised>)
      * [`CrowdloanInfo.target_address`](<#bittensor.core.chain_data.crowdloan_info.CrowdloanInfo.target_address>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.