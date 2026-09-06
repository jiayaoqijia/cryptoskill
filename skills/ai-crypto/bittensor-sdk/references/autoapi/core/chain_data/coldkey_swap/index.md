# bittensor.core.chain_data.coldkey_swap &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/coldkey_swap/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/coldkey_swap/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/coldkey_swap/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.coldkey_swap

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`ColdkeySwapAnnouncementInfo`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo>)
      * [`ColdkeySwapAnnouncementInfo.coldkey`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo.coldkey>)
      * [`ColdkeySwapAnnouncementInfo.execution_block`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo.execution_block>)
      * [`ColdkeySwapAnnouncementInfo.from_query()`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo.from_query>)
      * [`ColdkeySwapAnnouncementInfo.from_record()`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo.from_record>)
      * [`ColdkeySwapAnnouncementInfo.new_coldkey_hash`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo.new_coldkey_hash>)
    * [`ColdkeySwapConstants`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapConstants>)
      * [`ColdkeySwapConstants.KeySwapCost`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapConstants.KeySwapCost>)
      * [`ColdkeySwapConstants.constants_names()`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapConstants.constants_names>)
      * [`ColdkeySwapConstants.from_dict()`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapConstants.from_dict>)
      * [`ColdkeySwapConstants.to_dict()`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapConstants.to_dict>)
    * [`ColdkeySwapDisputeInfo`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo>)
      * [`ColdkeySwapDisputeInfo.coldkey`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo.coldkey>)
      * [`ColdkeySwapDisputeInfo.disputed_block`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo.disputed_block>)
      * [`ColdkeySwapDisputeInfo.from_query()`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo.from_query>)
      * [`ColdkeySwapDisputeInfo.from_record()`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo.from_record>)



# bittensor.core.chain_data.coldkey_swap[#](<#module-bittensor.core.chain_data.coldkey_swap> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`ColdkeySwapAnnouncementInfo`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo> "bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo") | Information about a coldkey swap announcement.  
---|---  
[`ColdkeySwapConstants`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapConstants> "bittensor.core.chain_data.coldkey_swap.ColdkeySwapConstants") | Represents runtime constants for coldkey swap operations in the SubtensorModule.  
[`ColdkeySwapDisputeInfo`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo> "bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo") | Information about a coldkey swap dispute.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo[#](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo> "Link to this definition")
    

Information about a coldkey swap announcement.

This class contains information about a pending coldkey swap announcement. Announcements are used when a coldkey wants to declare its intention to swap to a new coldkey address. The announcement must be made before the actual swap can be executed, allowing time for verification and security checks.

Variables:
    

  * **coldkey** – The SS58 address of the coldkey that made the announcement.

  * **execution_block** – The block number when the swap can be executed (after the delay period has passed).

  * **new_coldkey_hash** – The BlakeTwo256 hash of the new coldkey AccountId (hex string with 0x prefix). This hash must match the actual new coldkey when the swap is executed.




Notes

  * The announcement is stored on-chain and can be queried via get_coldkey_swap_announcement().

  * After making an announcement, all transactions from coldkey are blocked except for swap_coldkey_announced.

  * The swap can only be executed after the execution_block has been reached.

  * See: <<https://docs.learnbittensor.org/keys/coldkey-swap>>




coldkey: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo.coldkey> "Link to this definition")
    

execution_block: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo.execution_block> "Link to this definition")
    

classmethod from_query(_coldkey_ss58_ , _query_)[#](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo.from_query> "Link to this definition")
    

Creates a ColdkeySwapAnnouncementInfo object from a Substrate query result.

Parameters:
    

  * **coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the coldkey that made the announcement.

  * **query** (_scalecodec.base.ScaleType_) – Query result from Substrate query() call to ColdkeySwapAnnouncements storage function.



Returns:
    

ColdkeySwapAnnouncementInfo if announcement exists, None otherwise.

Return type:
    

Optional[[ColdkeySwapAnnouncementInfo](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo> "bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo")]

classmethod from_record(_record_)[#](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo.from_record> "Link to this definition")
    

Creates a ColdkeySwapAnnouncementInfo object from a query_map record.

Parameters:
    

**record** ([_tuple_](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")) – Data item from query_map records call to ColdkeySwapAnnouncements storage function. Structure is [key, value] where key is the coldkey AccountId and value contains (BlockNumber, Hash) tuple.

Returns:
    

ColdkeySwapAnnouncementInfo object with announcement details for the coldkey from the record.

Return type:
    

[ColdkeySwapAnnouncementInfo](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo> "bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo")

new_coldkey_hash: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo.new_coldkey_hash> "Link to this definition")
    

class bittensor.core.chain_data.coldkey_swap.ColdkeySwapConstants[#](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapConstants> "Link to this definition")
    

Represents runtime constants for coldkey swap operations in the SubtensorModule.

This class contains runtime constants that define cost requirements for coldkey swap operations. Note: For delay values (ColdkeySwapAnnouncementDelay and ColdkeySwapReannouncementDelay), use the dedicated query methods get_coldkey_swap_announcement_delay() and get_coldkey_swap_reannouncement_delay() instead, as these are storage values, not runtime constants.

Variables:
    

**KeySwapCost** – The cost in RAO required to make a coldkey swap announcement. This cost is charged when making the first announcement (not when reannouncing). This is a runtime constant (queryable via constants).

Notes

  * All amounts are in RAO.

  * Values reflect the current chain configuration at the time of retrieval.

  * See: <<https://docs.learnbittensor.org/keys/coldkey-swap>>




KeySwapCost: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapConstants.KeySwapCost> "Link to this definition")
    

classmethod constants_names()[#](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapConstants.constants_names> "Link to this definition")
    

Returns the list of all constant field names defined in this dataclass.

Returns:
    

List of constant field names as strings.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]

classmethod from_dict(_data_)[#](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapConstants.from_dict> "Link to this definition")
    

Creates a ColdkeySwapConstants instance from a dictionary of decoded chain constants.

Parameters:
    

**data** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")) – Dictionary mapping constant names to their decoded values (returned by Subtensor.query_constant()).

Returns:
    

ColdkeySwapConstants object with constants filled in. Fields not found in data will be set to None.

Return type:
    

[ColdkeySwapConstants](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapConstants> "bittensor.core.chain_data.coldkey_swap.ColdkeySwapConstants")

to_dict()[#](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapConstants.to_dict> "Link to this definition")
    

Converts the ColdkeySwapConstants instance to a dictionary.

Returns:
    

Dictionary mapping constant names to their values.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")

class bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo[#](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo> "Link to this definition")
    

Information about a coldkey swap dispute.

This class contains information about a disputed coldkey swap. When a coldkey swap is disputed, the account is frozen until the triumvirate resolves it via a root-only reset.

Variables:
    

  * **coldkey** – The SS58 address of the coldkey that was disputed.

  * **disputed_block** – The block number when the dispute was recorded.




Notes

  * The dispute is stored on-chain in ColdkeySwapDisputes storage.

  * While disputed, the coldkey can only perform announce_coldkey_swap, swap_coldkey_announced, or dispute_coldkey_swap (or MEV-protected calls).

  * See: <<https://docs.learnbittensor.org/keys/coldkey-swap>>




coldkey: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo.coldkey> "Link to this definition")
    

disputed_block: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo.disputed_block> "Link to this definition")
    

classmethod from_query(_coldkey_ss58_ , _query_)[#](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo.from_query> "Link to this definition")
    

Creates a ColdkeySwapDisputeInfo object from a Substrate query result.

Parameters:
    

  * **coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the coldkey that was disputed.

  * **query** (_scalecodec.base.ScaleType_) – Query result from Substrate query() call to ColdkeySwapDisputes storage function.



Returns:
    

ColdkeySwapDisputeInfo if dispute exists, None otherwise.

Return type:
    

Optional[[ColdkeySwapDisputeInfo](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo> "bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo")]

classmethod from_record(_record_)[#](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo.from_record> "Link to this definition")
    

Creates a ColdkeySwapDisputeInfo object from a query_map record.

Parameters:
    

**record** ([_tuple_](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Data item from query_map records call to ColdkeySwapDisputes storage function. Structure is [key, value] where key is the coldkey AccountId and value is the disputed block number.

Returns:
    

ColdkeySwapDisputeInfo object with dispute details for the coldkey from the record.

Return type:
    

[ColdkeySwapDisputeInfo](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo> "bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo")

[ __ previous bittensor.core.chain_data.chain_identity ](<../chain_identity/index.html> "previous page") [ next bittensor.core.chain_data.crowdloan_info __](<../crowdloan_info/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`ColdkeySwapAnnouncementInfo`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo>)
      * [`ColdkeySwapAnnouncementInfo.coldkey`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo.coldkey>)
      * [`ColdkeySwapAnnouncementInfo.execution_block`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo.execution_block>)
      * [`ColdkeySwapAnnouncementInfo.from_query()`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo.from_query>)
      * [`ColdkeySwapAnnouncementInfo.from_record()`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo.from_record>)
      * [`ColdkeySwapAnnouncementInfo.new_coldkey_hash`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapAnnouncementInfo.new_coldkey_hash>)
    * [`ColdkeySwapConstants`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapConstants>)
      * [`ColdkeySwapConstants.KeySwapCost`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapConstants.KeySwapCost>)
      * [`ColdkeySwapConstants.constants_names()`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapConstants.constants_names>)
      * [`ColdkeySwapConstants.from_dict()`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapConstants.from_dict>)
      * [`ColdkeySwapConstants.to_dict()`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapConstants.to_dict>)
    * [`ColdkeySwapDisputeInfo`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo>)
      * [`ColdkeySwapDisputeInfo.coldkey`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo.coldkey>)
      * [`ColdkeySwapDisputeInfo.disputed_block`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo.disputed_block>)
      * [`ColdkeySwapDisputeInfo.from_query()`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo.from_query>)
      * [`ColdkeySwapDisputeInfo.from_record()`](<#bittensor.core.chain_data.coldkey_swap.ColdkeySwapDisputeInfo.from_record>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.