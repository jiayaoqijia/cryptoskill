# bittensor.core.chain_data.proxy &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/proxy/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/proxy/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/proxy/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.proxy

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`ProxyAnnouncementInfo`](<#bittensor.core.chain_data.proxy.ProxyAnnouncementInfo>)
      * [`ProxyAnnouncementInfo.call_hash`](<#bittensor.core.chain_data.proxy.ProxyAnnouncementInfo.call_hash>)
      * [`ProxyAnnouncementInfo.from_dict()`](<#bittensor.core.chain_data.proxy.ProxyAnnouncementInfo.from_dict>)
      * [`ProxyAnnouncementInfo.from_query_map_record()`](<#bittensor.core.chain_data.proxy.ProxyAnnouncementInfo.from_query_map_record>)
      * [`ProxyAnnouncementInfo.height`](<#bittensor.core.chain_data.proxy.ProxyAnnouncementInfo.height>)
      * [`ProxyAnnouncementInfo.real`](<#bittensor.core.chain_data.proxy.ProxyAnnouncementInfo.real>)
    * [`ProxyConstants`](<#bittensor.core.chain_data.proxy.ProxyConstants>)
      * [`ProxyConstants.AnnouncementDepositBase`](<#bittensor.core.chain_data.proxy.ProxyConstants.AnnouncementDepositBase>)
      * [`ProxyConstants.AnnouncementDepositFactor`](<#bittensor.core.chain_data.proxy.ProxyConstants.AnnouncementDepositFactor>)
      * [`ProxyConstants.MaxPending`](<#bittensor.core.chain_data.proxy.ProxyConstants.MaxPending>)
      * [`ProxyConstants.MaxProxies`](<#bittensor.core.chain_data.proxy.ProxyConstants.MaxProxies>)
      * [`ProxyConstants.ProxyDepositBase`](<#bittensor.core.chain_data.proxy.ProxyConstants.ProxyDepositBase>)
      * [`ProxyConstants.ProxyDepositFactor`](<#bittensor.core.chain_data.proxy.ProxyConstants.ProxyDepositFactor>)
      * [`ProxyConstants.constants_names()`](<#bittensor.core.chain_data.proxy.ProxyConstants.constants_names>)
      * [`ProxyConstants.from_dict()`](<#bittensor.core.chain_data.proxy.ProxyConstants.from_dict>)
      * [`ProxyConstants.to_dict()`](<#bittensor.core.chain_data.proxy.ProxyConstants.to_dict>)
    * [`ProxyInfo`](<#bittensor.core.chain_data.proxy.ProxyInfo>)
      * [`ProxyInfo.delay`](<#bittensor.core.chain_data.proxy.ProxyInfo.delay>)
      * [`ProxyInfo.delegate`](<#bittensor.core.chain_data.proxy.ProxyInfo.delegate>)
      * [`ProxyInfo.from_query()`](<#bittensor.core.chain_data.proxy.ProxyInfo.from_query>)
      * [`ProxyInfo.from_query_map_record()`](<#bittensor.core.chain_data.proxy.ProxyInfo.from_query_map_record>)
      * [`ProxyInfo.from_tuple()`](<#bittensor.core.chain_data.proxy.ProxyInfo.from_tuple>)
      * [`ProxyInfo.proxy_type`](<#bittensor.core.chain_data.proxy.ProxyInfo.proxy_type>)
    * [`ProxyType`](<#bittensor.core.chain_data.proxy.ProxyType>)
      * [`ProxyType.Any`](<#bittensor.core.chain_data.proxy.ProxyType.Any>)
      * [`ProxyType.ChildKeys`](<#bittensor.core.chain_data.proxy.ProxyType.ChildKeys>)
      * [`ProxyType.Governance`](<#bittensor.core.chain_data.proxy.ProxyType.Governance>)
      * [`ProxyType.NonCritical`](<#bittensor.core.chain_data.proxy.ProxyType.NonCritical>)
      * [`ProxyType.NonFungible`](<#bittensor.core.chain_data.proxy.ProxyType.NonFungible>)
      * [`ProxyType.NonTransfer`](<#bittensor.core.chain_data.proxy.ProxyType.NonTransfer>)
      * [`ProxyType.Owner`](<#bittensor.core.chain_data.proxy.ProxyType.Owner>)
      * [`ProxyType.Registration`](<#bittensor.core.chain_data.proxy.ProxyType.Registration>)
      * [`ProxyType.RootClaim`](<#bittensor.core.chain_data.proxy.ProxyType.RootClaim>)
      * [`ProxyType.RootWeights`](<#bittensor.core.chain_data.proxy.ProxyType.RootWeights>)
      * [`ProxyType.Senate`](<#bittensor.core.chain_data.proxy.ProxyType.Senate>)
      * [`ProxyType.SmallTransfer`](<#bittensor.core.chain_data.proxy.ProxyType.SmallTransfer>)
      * [`ProxyType.Staking`](<#bittensor.core.chain_data.proxy.ProxyType.Staking>)
      * [`ProxyType.SubnetLeaseBeneficiary`](<#bittensor.core.chain_data.proxy.ProxyType.SubnetLeaseBeneficiary>)
      * [`ProxyType.SudoUncheckedSetCode`](<#bittensor.core.chain_data.proxy.ProxyType.SudoUncheckedSetCode>)
      * [`ProxyType.SwapHotkey`](<#bittensor.core.chain_data.proxy.ProxyType.SwapHotkey>)
      * [`ProxyType.Transfer`](<#bittensor.core.chain_data.proxy.ProxyType.Transfer>)
      * [`ProxyType.Triumvirate`](<#bittensor.core.chain_data.proxy.ProxyType.Triumvirate>)
      * [`ProxyType.all_types()`](<#bittensor.core.chain_data.proxy.ProxyType.all_types>)
      * [`ProxyType.is_valid()`](<#bittensor.core.chain_data.proxy.ProxyType.is_valid>)
      * [`ProxyType.normalize()`](<#bittensor.core.chain_data.proxy.ProxyType.normalize>)



# bittensor.core.chain_data.proxy[#](<#module-bittensor.core.chain_data.proxy> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`ProxyAnnouncementInfo`](<#bittensor.core.chain_data.proxy.ProxyAnnouncementInfo> "bittensor.core.chain_data.proxy.ProxyAnnouncementInfo") | Dataclass representing proxy announcement information.  
---|---  
[`ProxyConstants`](<#bittensor.core.chain_data.proxy.ProxyConstants> "bittensor.core.chain_data.proxy.ProxyConstants") | Fetches all runtime constants defined in the Proxy pallet.  
[`ProxyInfo`](<#bittensor.core.chain_data.proxy.ProxyInfo> "bittensor.core.chain_data.proxy.ProxyInfo") | Dataclass representing proxy relationship information.  
[`ProxyType`](<#bittensor.core.chain_data.proxy.ProxyType> "bittensor.core.chain_data.proxy.ProxyType") | Enumeration of all supported proxy types in the Bittensor network.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.proxy.ProxyAnnouncementInfo[#](<#bittensor.core.chain_data.proxy.ProxyAnnouncementInfo> "Link to this definition")
    

Dataclass representing proxy announcement information.

This class contains information about a pending proxy announcement. Announcements are used when a proxy account with a non-zero delay period (time-lock) wants to declare its intention to execute a call on behalf of the real account. The announcement must be made before the actual call can be executed, allowing the real account time to review and potentially reject the operation via reject_proxy_announcement before it takes effect. After the delay period passes, the proxy can execute the announced call via proxy_announced.

Variables:
    

  * **real** – The SS58 address of the real account on whose behalf the call will be made.

  * **call_hash** – The hash of the call that will be executed in the future (hex string with 0x prefix). This hash must match the actual call when it is executed via proxy_announced.

  * **height** – The block height at which the announcement was made. The delay period is calculated from this block.




Notes

  * Announcements are required when using delayed proxies (non-zero delay), providing an additional security layer for time-locked operations.

  * Bittensor proxies: <<https://docs.learnbittensor.org/keys/proxies>>




call_hash: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.proxy.ProxyAnnouncementInfo.call_hash> "Link to this definition")
    

classmethod from_dict(_data_)[#](<#bittensor.core.chain_data.proxy.ProxyAnnouncementInfo.from_dict> "Link to this definition")
    

Creates a list of ProxyAnnouncementInfo objects from chain announcement data.

This method decodes the raw announcement data returned from the Proxy.Announcements storage function.

Parameters:
    

**data** ([_tuple_](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)") _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _|_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]__]__,_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Tuple of announcements data from the Proxy.Announcements storage function.

Returns:
    

List of ProxyAnnouncementInfo objects representing all pending announcements.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[ProxyAnnouncementInfo](<#bittensor.core.chain_data.proxy.ProxyAnnouncementInfo> "bittensor.core.chain_data.proxy.ProxyAnnouncementInfo")]

Notes

See: <<https://docs.learnbittensor.org/keys/proxies>>

classmethod from_query_map_record(_record_)[#](<#bittensor.core.chain_data.proxy.ProxyAnnouncementInfo.from_query_map_record> "Link to this definition")
    

Returns a list of ProxyAnnouncementInfo objects from a tuple of announcements data.

Parameters:
    

**record** ([_tuple_](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_tuple_](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)") _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _|_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]__]__,_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]__]_) – Data item from query_map records call to Announcements storage function. Structure is [key, value] where key is the delegate account and value contains announcements data.

Returns:
    

  * SS58 address of the delegate account making the announcement.

  * List of ProxyAnnouncementInfo objects for all pending announcements from this delegate.




Return type:
    

Tuple containing

height: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.proxy.ProxyAnnouncementInfo.height> "Link to this definition")
    

real: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.proxy.ProxyAnnouncementInfo.real> "Link to this definition")
    

class bittensor.core.chain_data.proxy.ProxyConstants[#](<#bittensor.core.chain_data.proxy.ProxyConstants> "Link to this definition")
    

Fetches all runtime constants defined in the Proxy pallet.

Displays current values for on-chain configuration constants for the Proxy pallet. They define deposit requirements, account limits, and announcement constraints that govern the behavior of proxies.

Each attribute is fetched directly from the runtime via Subtensor.query_constant(“Proxy”, <name>) and reflects the current chain configuration at the time of retrieval.

Variables:
    

  * **AnnouncementDepositBase** – Base deposit amount (in RAO) required to announce a future proxy call. This deposit is held until the announced call is executed or cancelled.

  * **AnnouncementDepositFactor** – Additional deposit factor (in RAO) per byte of the call hash being announced. The total announcement deposit is calculated as: AnnouncementDepositBase + (call_hash_size * AnnouncementDepositFactor).

  * **MaxProxies** – Maximum number of proxy relationships that a single account can have. This limits the total number of delegates that can act on behalf of an account.

  * **MaxPending** – Maximum number of pending proxy announcements that can exist for a single account at any given time. This prevents spam and limits the storage requirements for pending announcements.

  * **ProxyDepositBase** – Base deposit amount (in RAO) required when adding a proxy relationship. This deposit is held as long as the proxy relationship exists and is returned when the proxy is removed.

  * **ProxyDepositFactor** – Additional deposit factor (in RAO) per proxy type added. The total proxy deposit is calculated as: ProxyDepositBase + (number_of_proxy_types * ProxyDepositFactor).




Notes

  * All Balance amounts are in RAO.

  * See: <<https://docs.learnbittensor.org/keys/proxies>>




AnnouncementDepositBase: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.proxy.ProxyConstants.AnnouncementDepositBase> "Link to this definition")
    

AnnouncementDepositFactor: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.proxy.ProxyConstants.AnnouncementDepositFactor> "Link to this definition")
    

MaxPending: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.proxy.ProxyConstants.MaxPending> "Link to this definition")
    

MaxProxies: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.proxy.ProxyConstants.MaxProxies> "Link to this definition")
    

ProxyDepositBase: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.proxy.ProxyConstants.ProxyDepositBase> "Link to this definition")
    

ProxyDepositFactor: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.proxy.ProxyConstants.ProxyDepositFactor> "Link to this definition")
    

classmethod constants_names()[#](<#bittensor.core.chain_data.proxy.ProxyConstants.constants_names> "Link to this definition")
    

Returns the all constant field names defined in this dataclass.

Returns:
    

List of constant field names as strings.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]

classmethod from_dict(_data_)[#](<#bittensor.core.chain_data.proxy.ProxyConstants.from_dict> "Link to this definition")
    

Creates a ProxyConstants instance from a dictionary of decoded chain constants.

Parameters:
    

**data** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")) – Dictionary mapping constant names to their decoded values (returned by Subtensor.query_constant()).

Returns:
    

ProxyConstants object with constants filled in. Fields not found in data will be set to None.

Return type:
    

[ProxyConstants](<#bittensor.core.chain_data.proxy.ProxyConstants> "bittensor.core.chain_data.proxy.ProxyConstants")

to_dict()[#](<#bittensor.core.chain_data.proxy.ProxyConstants.to_dict> "Link to this definition")
    

Converts the ProxyConstants instance to a dictionary.

Returns:
    

Dictionary mapping constant names to their values. Balance objects remain as Balance instances.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")

class bittensor.core.chain_data.proxy.ProxyInfo[#](<#bittensor.core.chain_data.proxy.ProxyInfo> "Link to this definition")
    

Dataclass representing proxy relationship information.

This class contains information about a proxy relationship between a real account and a delegate account. A proxy relationship allows the delegate to perform certain operations on behalf of the real account, with restrictions defined by the proxy type and a delay period.

Variables:
    

  * **delegate** – The SS58 address of the delegate proxy account that can act on behalf of the real account.

  * **proxy_type** – The type of proxy permissions granted to the delegate (e.g., “Any”, “NonTransfer”, “ChildKeys”, “Staking”). This determines what operations the delegate can perform.

  * **delay** – The number of blocks that must elapse between announcing a call and executing it (time-lock period). A delay of 0 allows immediate execution without announcements. Non-zero delays require the delegate to announce the call first via announce_proxy, wait for the delay period to pass, then execute it via proxy_announced, giving the real account time to review and potentially reject the call via reject_proxy_announcement before execution.




Notes

  * Bittensor proxies: <<https://docs.learnbittensor.org/keys/proxies>>

  * Creating proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>




delay: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.proxy.ProxyInfo.delay> "Link to this definition")
    

delegate: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.proxy.ProxyInfo.delegate> "Link to this definition")
    

classmethod from_query(_query_)[#](<#bittensor.core.chain_data.proxy.ProxyInfo.from_query> "Link to this definition")
    

Creates a list of ProxyInfo objects and deposit balance from a Substrate query result.

This method decodes the query result from the Proxy.Proxies storage function, extracting both the proxy relationships and the deposit amount reserved for maintaining these proxies.

Parameters:
    

**query** ([_Any_](<#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any")) – Query result from Substrate query() call to Proxy.Proxies storage function.

Returns:
    

  * List of ProxyInfo objects representing all proxy relationships for the real account.

  * Balance object representing the reserved deposit amount (in RAO).




Return type:
    

Tuple containing

Notes

The deposit is held as long as the proxy relationships exist and is returned when proxies are removed.

See: <<https://docs.learnbittensor.org/keys/proxies>>

classmethod from_query_map_record(_record_)[#](<#bittensor.core.chain_data.proxy.ProxyInfo.from_query_map_record> "Link to this definition")
    

Creates a dictionary mapping delegate addresses to their ProxyInfo lists from a query_map record.

Processes a single record from a query_map call to the Proxy.Proxies storage function. Each record represents one real account and its associated proxy/ies relationships.

Parameters:
    

**record** ([_tuple_](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_tuple_](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)") _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _|_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]__]__,_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]__]_) – Data item from query_map records call to Proxies storage function. Structure is [key, value] where key is the real account and value contains proxies data.

Returns:
    

  * SS58 address of the real account (delegator).

  * List of ProxyInfo objects representing all proxy relationships for this real account.




Return type:
    

Tuple containing

classmethod from_tuple(_data_)[#](<#bittensor.core.chain_data.proxy.ProxyInfo.from_tuple> "Link to this definition")
    

Creates a list of ProxyInfo objects from chain proxy data.

This method decodes the raw proxy data returned from the Proxy.Proxies storage function and creates structured ProxyInfo objects.

Parameters:
    

**data** (_Sequence_ _[_[_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _|_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]__]_) – Tuple of chain proxy data from the Proxy.Proxies storage function.

Returns:
    

List of ProxyInfo objects representing all proxy relationships for a real account.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[ProxyInfo](<#bittensor.core.chain_data.proxy.ProxyInfo> "bittensor.core.chain_data.proxy.ProxyInfo")]

Notes

See: <<https://docs.learnbittensor.org/keys/proxies>>

proxy_type: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.proxy.ProxyInfo.proxy_type> "Link to this definition")
    

class bittensor.core.chain_data.proxy.ProxyType[#](<#bittensor.core.chain_data.proxy.ProxyType> "Link to this definition")
    

Bases: [`str`](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [`enum.Enum`](<https://docs.python.org/3/library/enum.html#enum.Enum> "\(in Python v3.14\)")

Enumeration of all supported proxy types in the Bittensor network.

These types define the permissions that a proxy account has when acting on behalf of the real account. Each type restricts what operations the proxy can perform.

Proxy Type Descriptions:

> Any: Allows the proxy to execute any call on behalf of the real account. This is the most permissive but least
>     
> 
> secure proxy type. Use with caution.
> 
> Owner: Allows the proxy to manage subnet identity and settings. Permitted operations include:
>     
> 
>   * AdminUtils calls (except sudo_set_sn_owner_hotkey)
> 
>   * set_subnet_identity
> 
>   * update_symbol
> 
> 

> NonCritical: Allows all operations except critical ones that could harm the account. Prohibited operations:
>     
> 
>   * dissolve_network
> 
>   * root_register
> 
>   * burned_register
> 
>   * Sudo calls
> 
> 

> NonTransfer: Allows all operations except those involving token transfers. Prohibited operations:
>     
> 
>   * All Balances module calls
> 
>   * transfer_stake
> 
> 

> NonFungible: Allows all operations except token-related operations and registrations. Prohibited operations:
>     
> 
>   * All Balances module calls
> 
>   * All staking operations (add_stake, remove_stake, unstake_all, swap_stake, move_stake, transfer_stake)
> 
>   * Registration operations (burned_register, root_register)
> 
>   * Key swap operations (announce_coldkey_swap, swap_coldkey_announced, swap_hotkey)
> 
> 

> Staking: Allows only staking-related operations. Permitted operations:
>     
> 
>   * add_stake, add_stake_limit
> 
>   * remove_stake, remove_stake_limit, remove_stake_full_limit
> 
>   * unstake_all, unstake_all_alpha
> 
>   * swap_stake, swap_stake_limit
> 
>   * move_stake
> 
> 

> Registration: Allows only neuron registration operations. Permitted operations:
>     
> 
>   * burned_register
> 
>   * register
> 
> 

> Transfer: Allows only token transfer operations. Permitted operations:
>     
> 
>   * transfer_keep_alive
> 
>   * transfer_allow_death
> 
>   * transfer_all
> 
>   * transfer_stake
> 
> 

> SmallTransfer: Allows only small token transfers below a specific limit. Permitted operations:
>     
> 
>   * transfer_keep_alive (if value < SMALL_TRANSFER_LIMIT)
> 
>   * transfer_allow_death (if value < SMALL_TRANSFER_LIMIT)
> 
>   * transfer_stake (if alpha_amount < SMALL_TRANSFER_LIMIT)
> 
> 

> ChildKeys: Allows only child key management operations. Permitted operations:
>     
> 
>   * set_children
> 
>   * set_childkey_take
> 
> 

> SudoUncheckedSetCode: Allows only runtime code updates. Permitted operations:
>     
> 
>   * sudo_unchecked_weight with inner call System::set_code
> 
> 

> SwapHotkey: Allows only hotkey swap operations. Permitted operations:
>     
> 
>   * swap_hotkey
> 
> 

> SubnetLeaseBeneficiary: Allows subnet management and configuration operations. Permitted operations:
>     
> 
>   * start_call
> 
>   * Multiple AdminUtils.sudo_set_* calls for subnet parameters, network settings, weights, alpha values, etc.
> 
> 

> RootClaim: Allows only root claim operations. Permitted operations:
>     
> 
>   * claim_root
> 
>   * set_root_claim_type
> 
> 


Notes

  * The permissions described above may change over time as the Subtensor runtime evolves. For the most up-to-date and authoritative information about proxy type permissions, refer to the Subtensor source code at: <[opentensor/subtensor](<https://github.com/opentensor/subtensor/blob/main/runtime/src/lib.rs>)> Specifically, look for the impl InstanceFilter<RuntimeCall> for ProxyType implementation which defines the exact filtering logic for each proxy type.

  * The values match exactly with the ProxyType enum defined in the Subtensor runtime. Any changes to the runtime enum must be reflected here.

  * Proxy overview: <<https://docs.learnbittensor.org/keys/proxies>>

  * Creating and managing proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>

  * Pure proxies: <<https://docs.learnbittensor.org/keys/proxies/pure-proxies>>




Initialize self. See help(type(self)) for accurate signature.

Any = 'Any'[#](<#bittensor.core.chain_data.proxy.ProxyType.Any> "Link to this definition")
    

ChildKeys = 'ChildKeys'[#](<#bittensor.core.chain_data.proxy.ProxyType.ChildKeys> "Link to this definition")
    

Governance = 'Governance'[#](<#bittensor.core.chain_data.proxy.ProxyType.Governance> "Link to this definition")
    

NonCritical = 'NonCritical'[#](<#bittensor.core.chain_data.proxy.ProxyType.NonCritical> "Link to this definition")
    

NonFungible = 'NonFungible'[#](<#bittensor.core.chain_data.proxy.ProxyType.NonFungible> "Link to this definition")
    

NonTransfer = 'NonTransfer'[#](<#bittensor.core.chain_data.proxy.ProxyType.NonTransfer> "Link to this definition")
    

Owner = 'Owner'[#](<#bittensor.core.chain_data.proxy.ProxyType.Owner> "Link to this definition")
    

Registration = 'Registration'[#](<#bittensor.core.chain_data.proxy.ProxyType.Registration> "Link to this definition")
    

RootClaim = 'RootClaim'[#](<#bittensor.core.chain_data.proxy.ProxyType.RootClaim> "Link to this definition")
    

RootWeights = 'RootWeights'[#](<#bittensor.core.chain_data.proxy.ProxyType.RootWeights> "Link to this definition")
    

Senate = 'Senate'[#](<#bittensor.core.chain_data.proxy.ProxyType.Senate> "Link to this definition")
    

SmallTransfer = 'SmallTransfer'[#](<#bittensor.core.chain_data.proxy.ProxyType.SmallTransfer> "Link to this definition")
    

Staking = 'Staking'[#](<#bittensor.core.chain_data.proxy.ProxyType.Staking> "Link to this definition")
    

SubnetLeaseBeneficiary = 'SubnetLeaseBeneficiary'[#](<#bittensor.core.chain_data.proxy.ProxyType.SubnetLeaseBeneficiary> "Link to this definition")
    

SudoUncheckedSetCode = 'SudoUncheckedSetCode'[#](<#bittensor.core.chain_data.proxy.ProxyType.SudoUncheckedSetCode> "Link to this definition")
    

SwapHotkey = 'SwapHotkey'[#](<#bittensor.core.chain_data.proxy.ProxyType.SwapHotkey> "Link to this definition")
    

Transfer = 'Transfer'[#](<#bittensor.core.chain_data.proxy.ProxyType.Transfer> "Link to this definition")
    

Triumvirate = 'Triumvirate'[#](<#bittensor.core.chain_data.proxy.ProxyType.Triumvirate> "Link to this definition")
    

classmethod all_types()[#](<#bittensor.core.chain_data.proxy.ProxyType.all_types> "Link to this definition")
    

Returns a list of all proxy type values.

Returns:
    

List of all valid proxy type string values (e.g., [“Any”, “Owner”, “Staking”, …]).

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]

classmethod is_valid(_value_)[#](<#bittensor.core.chain_data.proxy.ProxyType.is_valid> "Link to this definition")
    

Checks if a string value is a valid proxy type.

Parameters:
    

**value** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – String value to validate.

Returns:
    

True if the value is a valid proxy type, False otherwise.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

classmethod normalize(_proxy_type_)[#](<#bittensor.core.chain_data.proxy.ProxyType.normalize> "Link to this definition")
    

Normalizes a proxy type to a string value.

This method handles both string and ProxyType enum values, validates the input, and returns the string representation suitable for Substrate calls.

Parameters:
    

**proxy_type** (_Union_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_ProxyType_](<#bittensor.core.chain_data.proxy.ProxyType> "bittensor.core.chain_data.proxy.ProxyType") _]_) – Either a string or ProxyType enum value.

Returns:
    

The normalized string value of the proxy type.

Raises:
    

[**ValueError**](<https://docs.python.org/3/library/exceptions.html#ValueError> "\(in Python v3.14\)") – If the proxy_type is not a valid proxy type.

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

[ __ previous bittensor.core.chain_data.proposal_vote_data ](<../proposal_vote_data/index.html> "previous page") [ next bittensor.core.chain_data.root_claim __](<../root_claim/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`ProxyAnnouncementInfo`](<#bittensor.core.chain_data.proxy.ProxyAnnouncementInfo>)
      * [`ProxyAnnouncementInfo.call_hash`](<#bittensor.core.chain_data.proxy.ProxyAnnouncementInfo.call_hash>)
      * [`ProxyAnnouncementInfo.from_dict()`](<#bittensor.core.chain_data.proxy.ProxyAnnouncementInfo.from_dict>)
      * [`ProxyAnnouncementInfo.from_query_map_record()`](<#bittensor.core.chain_data.proxy.ProxyAnnouncementInfo.from_query_map_record>)
      * [`ProxyAnnouncementInfo.height`](<#bittensor.core.chain_data.proxy.ProxyAnnouncementInfo.height>)
      * [`ProxyAnnouncementInfo.real`](<#bittensor.core.chain_data.proxy.ProxyAnnouncementInfo.real>)
    * [`ProxyConstants`](<#bittensor.core.chain_data.proxy.ProxyConstants>)
      * [`ProxyConstants.AnnouncementDepositBase`](<#bittensor.core.chain_data.proxy.ProxyConstants.AnnouncementDepositBase>)
      * [`ProxyConstants.AnnouncementDepositFactor`](<#bittensor.core.chain_data.proxy.ProxyConstants.AnnouncementDepositFactor>)
      * [`ProxyConstants.MaxPending`](<#bittensor.core.chain_data.proxy.ProxyConstants.MaxPending>)
      * [`ProxyConstants.MaxProxies`](<#bittensor.core.chain_data.proxy.ProxyConstants.MaxProxies>)
      * [`ProxyConstants.ProxyDepositBase`](<#bittensor.core.chain_data.proxy.ProxyConstants.ProxyDepositBase>)
      * [`ProxyConstants.ProxyDepositFactor`](<#bittensor.core.chain_data.proxy.ProxyConstants.ProxyDepositFactor>)
      * [`ProxyConstants.constants_names()`](<#bittensor.core.chain_data.proxy.ProxyConstants.constants_names>)
      * [`ProxyConstants.from_dict()`](<#bittensor.core.chain_data.proxy.ProxyConstants.from_dict>)
      * [`ProxyConstants.to_dict()`](<#bittensor.core.chain_data.proxy.ProxyConstants.to_dict>)
    * [`ProxyInfo`](<#bittensor.core.chain_data.proxy.ProxyInfo>)
      * [`ProxyInfo.delay`](<#bittensor.core.chain_data.proxy.ProxyInfo.delay>)
      * [`ProxyInfo.delegate`](<#bittensor.core.chain_data.proxy.ProxyInfo.delegate>)
      * [`ProxyInfo.from_query()`](<#bittensor.core.chain_data.proxy.ProxyInfo.from_query>)
      * [`ProxyInfo.from_query_map_record()`](<#bittensor.core.chain_data.proxy.ProxyInfo.from_query_map_record>)
      * [`ProxyInfo.from_tuple()`](<#bittensor.core.chain_data.proxy.ProxyInfo.from_tuple>)
      * [`ProxyInfo.proxy_type`](<#bittensor.core.chain_data.proxy.ProxyInfo.proxy_type>)
    * [`ProxyType`](<#bittensor.core.chain_data.proxy.ProxyType>)
      * [`ProxyType.Any`](<#bittensor.core.chain_data.proxy.ProxyType.Any>)
      * [`ProxyType.ChildKeys`](<#bittensor.core.chain_data.proxy.ProxyType.ChildKeys>)
      * [`ProxyType.Governance`](<#bittensor.core.chain_data.proxy.ProxyType.Governance>)
      * [`ProxyType.NonCritical`](<#bittensor.core.chain_data.proxy.ProxyType.NonCritical>)
      * [`ProxyType.NonFungible`](<#bittensor.core.chain_data.proxy.ProxyType.NonFungible>)
      * [`ProxyType.NonTransfer`](<#bittensor.core.chain_data.proxy.ProxyType.NonTransfer>)
      * [`ProxyType.Owner`](<#bittensor.core.chain_data.proxy.ProxyType.Owner>)
      * [`ProxyType.Registration`](<#bittensor.core.chain_data.proxy.ProxyType.Registration>)
      * [`ProxyType.RootClaim`](<#bittensor.core.chain_data.proxy.ProxyType.RootClaim>)
      * [`ProxyType.RootWeights`](<#bittensor.core.chain_data.proxy.ProxyType.RootWeights>)
      * [`ProxyType.Senate`](<#bittensor.core.chain_data.proxy.ProxyType.Senate>)
      * [`ProxyType.SmallTransfer`](<#bittensor.core.chain_data.proxy.ProxyType.SmallTransfer>)
      * [`ProxyType.Staking`](<#bittensor.core.chain_data.proxy.ProxyType.Staking>)
      * [`ProxyType.SubnetLeaseBeneficiary`](<#bittensor.core.chain_data.proxy.ProxyType.SubnetLeaseBeneficiary>)
      * [`ProxyType.SudoUncheckedSetCode`](<#bittensor.core.chain_data.proxy.ProxyType.SudoUncheckedSetCode>)
      * [`ProxyType.SwapHotkey`](<#bittensor.core.chain_data.proxy.ProxyType.SwapHotkey>)
      * [`ProxyType.Transfer`](<#bittensor.core.chain_data.proxy.ProxyType.Transfer>)
      * [`ProxyType.Triumvirate`](<#bittensor.core.chain_data.proxy.ProxyType.Triumvirate>)
      * [`ProxyType.all_types()`](<#bittensor.core.chain_data.proxy.ProxyType.all_types>)
      * [`ProxyType.is_valid()`](<#bittensor.core.chain_data.proxy.ProxyType.is_valid>)
      * [`ProxyType.normalize()`](<#bittensor.core.chain_data.proxy.ProxyType.normalize>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.