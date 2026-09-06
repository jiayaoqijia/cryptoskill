# bittensor.core.extrinsics.pallets.proxy &#8212; Bittensor SDK Docs  documentation

[Skip to main content](<#main-content>)

__Back to top __ `Ctrl`+`K`

[ ![Bittensor SDK Docs  documentation - Home](../../../../../../_static/logo.svg) ![Bittensor SDK Docs  documentation - Home](../../../../../../_static/logo-dark-mode.svg) ](<../../../../../../index.html>)

__ Search `Ctrl`+`K`

Table of Contents

  * [API Reference](<../../../../../index.html>) __
    * [bittensor](<../../../../index.html>) __
      * [bittensor.core](<../../../index.html>) __
        * [bittensor.core.async_subtensor](<../../../async_subtensor/index.html>)
        * [bittensor.core.axon](<../../../axon/index.html>)
        * [bittensor.core.chain_data](<../../../chain_data/index.html>)
        * [bittensor.core.config](<../../../config/index.html>)
        * [bittensor.core.dendrite](<../../../dendrite/index.html>)
        * [bittensor.core.errors](<../../../errors/index.html>)
        * [bittensor.core.extrinsics](<../../index.html>)
        * [bittensor.core.metagraph](<../../../metagraph/index.html>)
        * [bittensor.core.settings](<../../../settings/index.html>)
        * [bittensor.core.stream](<../../../stream/index.html>)
        * [bittensor.core.subtensor](<../../../subtensor/index.html>)
        * [bittensor.core.synapse](<../../../synapse/index.html>)
        * [bittensor.core.tensor](<../../../tensor/index.html>)
        * [bittensor.core.threadpool](<../../../threadpool/index.html>)
        * [bittensor.core.types](<../../../types/index.html>)
      * [bittensor.extras](<../../../../extras/index.html>) __
        * [bittensor.extras.dev_framework](<../../../../extras/dev_framework/index.html>)
        * [bittensor.extras.subtensor_api](<../../../../extras/subtensor_api/index.html>)
        * [bittensor.extras.timelock](<../../../../extras/timelock/index.html>)
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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/pallets/proxy/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/pallets/proxy/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../../_sources/autoapi/bittensor/core/extrinsics/pallets/proxy/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.pallets.proxy

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Proxy`](<#bittensor.core.extrinsics.pallets.proxy.Proxy>)
      * [`Proxy.add_proxy()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.add_proxy>)
      * [`Proxy.announce()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.announce>)
      * [`Proxy.create_pure()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.create_pure>)
      * [`Proxy.kill_pure()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.kill_pure>)
      * [`Proxy.poke_deposit()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.poke_deposit>)
      * [`Proxy.proxy()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.proxy>)
      * [`Proxy.proxy_announced()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.proxy_announced>)
      * [`Proxy.reject_announcement()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.reject_announcement>)
      * [`Proxy.remove_announcement()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.remove_announcement>)
      * [`Proxy.remove_proxies()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.remove_proxies>)
      * [`Proxy.remove_proxy()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.remove_proxy>)



# bittensor.core.extrinsics.pallets.proxy[#](<#module-bittensor.core.extrinsics.pallets.proxy> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`Proxy`](<#bittensor.core.extrinsics.pallets.proxy.Proxy> "bittensor.core.extrinsics.pallets.proxy.Proxy") | Factory class for creating GenericCall objects for Proxy pallet functions.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.extrinsics.pallets.proxy.Proxy[#](<#bittensor.core.extrinsics.pallets.proxy.Proxy> "Link to this definition")
    

Bases: [`bittensor.core.extrinsics.pallets.base.CallBuilder`](<../base/index.html#bittensor.core.extrinsics.pallets.base.CallBuilder> "bittensor.core.extrinsics.pallets.base.CallBuilder")

Factory class for creating GenericCall objects for Proxy pallet functions.

This class provides methods to create GenericCall instances for all Proxy pallet extrinsics.

Works with both sync (Subtensor) and async (AsyncSubtensor) instances. For async operations, pass an AsyncSubtensor instance and await the result.

Example

# Sync usage

call = Proxy(subtensor).add_proxy(delegate=”5DE..”, proxy_type=”Any”, delay=0)

response = subtensor.sign_and_send_extrinsic(call=call, …)

# Async usage

call = await Proxy(async_subtensor).add_proxy(delegate=”5DE..”, proxy_type=”Any”, delay=0)

response = await async_subtensor.sign_and_send_extrinsic(call=call, …)

add_proxy(_delegate_ , _proxy_type_ , _delay_)[#](<#bittensor.core.extrinsics.pallets.proxy.Proxy.add_proxy> "Link to this definition")
    

Add a proxy relationship between existing wallets.

Parameters:
    

  * **delegate** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the delegate proxy account.

  * **proxy_type** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The type of proxy permissions (e.g., Any, NonTransfer, Staking). For available proxy types and their permissions, see the documentation link in the Notes section below.

  * **delay** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Optionally, include a delay in blocks. The time-lock period for proxy announcements. A delay of 0 means immediate execution without announcements.



Returns:
    

GenericCall instance for the Proxy.addProxy extrinsic.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

Notes

  * For available proxy types and their specific permissions, see: <<https://docs.learnbittensor.org/keys/proxies#types-of-proxies>>

  * See Working with Proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>




announce(_real_ , _call_hash_)[#](<#bittensor.core.extrinsics.pallets.proxy.Proxy.announce> "Link to this definition")
    

Create a call to announce a future proxied operation.

Parameters:
    

  * **real** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the real account on whose behalf the call will be made.

  * **call_hash** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hash of the call that will be executed in the future (hex string with 0x prefix).



Returns:
    

GenericCall instance for the Proxy.announce extrinsic.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

Notes

  * A deposit is required when making an announcement. The deposit is returned when the announcement is executed, rejected, or removed. The announcement can be executed after the delay period has passed.

  * See Working with Proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>




create_pure(_proxy_type_ , _delay_ , _index_)[#](<#bittensor.core.extrinsics.pallets.proxy.Proxy.create_pure> "Link to this definition")
    

Create a pure proxy account.

Parameters:
    

  * **proxy_type** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The type of proxy permissions for the pure proxy (e.g., Any, NonTransfer, Staking). For available proxy types and their permissions, see the documentation link in the Notes section below.

  * **delay** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Optionally, include a delay in blocks. The time-lock period for proxy announcements. A delay of 0 means immediate execution without announcements.

  * **index** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – A salt value (u16, range 0-65535) used to generate unique pure proxy addresses. This should generally be left as 0 unless you are creating batches of proxies. Must be preserved for kill_pure.



Returns:
    

GenericCall instance for the Proxy.createPure extrinsic.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

Notes

  * For available proxy types and their specific permissions, see: <<https://docs.learnbittensor.org/keys/proxies#types-of-proxies>>

  * See Pure Proxies: <<https://docs.learnbittensor.org/keys/proxies/pure-proxies>>




kill_pure(_spawner_ , _proxy_type_ , _index_ , _height_ , _ext_index_)[#](<#bittensor.core.extrinsics.pallets.proxy.Proxy.kill_pure> "Link to this definition")
    

Destroy a pure proxy account.

Parameters:
    

  * **spawner** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the account that spawned the pure proxy (the account that called create_pure).

  * **proxy_type** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The type of proxy permissions that were used when creating the pure proxy. Must match the value used in create_pure.

  * **index** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The salt value (u16, range 0-65535) originally used in create_pure to generate this pure proxy’s address. Must match exactly the index used during creation.

  * **height** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The block number at which the pure proxy was created. This is returned in the PureCreated event from create_pure.

  * **ext_index** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The extrinsic index within the block at which the pure proxy was created. This is returned in the PureCreated event from create_pure.



Returns:
    

GenericCall instance for the Proxy.killPure extrinsic.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

Notes

See Pure Proxies: <<https://docs.learnbittensor.org/keys/proxies/pure-proxies>>

Warning

All access to this account will be lost. Any funds remaining in the pure proxy account will become permanently inaccessible after this operation.

poke_deposit()[#](<#bittensor.core.extrinsics.pallets.proxy.Proxy.poke_deposit> "Link to this definition")
    

Adjust proxy and announcement deposits based on current runtime values.

Returns:
    

GenericCall instance for the Proxy.pokeDeposit extrinsic.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

Notes

  * This can be used by accounts to possibly lower their locked amount. The function automatically recalculates deposits for both proxy relationships and announcements for the signing account. The transaction fee is waived if the deposit amount has changed.

  * See Working with Proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>




proxy(_real_ , _force_proxy_type_ , _call_)[#](<#bittensor.core.extrinsics.pallets.proxy.Proxy.proxy> "Link to this definition")
    

Create a call to execute an operation through a proxy relationship.

Parameters:
    

  * **real** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the real account on whose behalf the call is being made.

  * **force_proxy_type** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The type of proxy to use for the call. If None, any proxy type can be used. Otherwise, must match one of the allowed proxy types that the signing account has for the real account.

  * **call** (_scalecodec.GenericCall_) – The inner call to be executed on behalf of the real account.



Returns:
    

GenericCall instance for the Proxy.proxy extrinsic.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

Notes

  * The call must be permitted by the proxy type. For example, a NonTransfer proxy cannot execute transfer calls.

  * See Working with Proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>




proxy_announced(_delegate_ , _real_ , _force_proxy_type_ , _call_)[#](<#bittensor.core.extrinsics.pallets.proxy.Proxy.proxy_announced> "Link to this definition")
    

Create a call to execute a previously announced proxied operation.

Parameters:
    

  * **delegate** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the delegate proxy account that made the announcement.

  * **real** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the real account on whose behalf the call will be made.

  * **force_proxy_type** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The type of proxy to use for the call. If None, any proxy type can be used. Otherwise, must match one of the allowed proxy types.

  * **call** (_scalecodec.GenericCall_) – The inner call to be executed on behalf of the real account. The hash of this call must match the call_hash that was announced.



Returns:
    

GenericCall instance for the Proxy.proxyAnnounced extrinsic.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

Notes

  * The call_hash of the provided call must match the call_hash that was announced. The announcement must not have been rejected by the real account, and the delay period must have passed.

  * See Working with Proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>




reject_announcement(_delegate_ , _call_hash_)[#](<#bittensor.core.extrinsics.pallets.proxy.Proxy.reject_announcement> "Link to this definition")
    

Reject a proxy announcement.

Parameters:
    

  * **delegate** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the delegate proxy account whose announcement is being rejected.

  * **call_hash** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hash of the call that was announced and is now being rejected (hex string with 0x prefix).



Returns:
    

GenericCall instance for the Proxy.rejectAnnouncement extrinsic.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

Notes

  * Once rejected, the announcement cannot be executed. The delegate’s announcement deposit is returned.

  * See Working with Proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>




remove_announcement(_real_ , _call_hash_)[#](<#bittensor.core.extrinsics.pallets.proxy.Proxy.remove_announcement> "Link to this definition")
    

Remove an announcement made by the signing proxy account.

Parameters:
    

  * **real** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the real account on whose behalf the call was announced.

  * **call_hash** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hash of the call that was announced and is now being removed (hex string with 0x prefix).



Returns:
    

GenericCall instance for the Proxy.removeAnnouncement extrinsic.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

Notes

  * Removing an announcement frees up the announcement deposit.

  * See Working with Proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>




remove_proxies()[#](<#bittensor.core.extrinsics.pallets.proxy.Proxy.remove_proxies> "Link to this definition")
    

Remove all proxy relationships for the signing account.

Returns:
    

GenericCall instance for the Proxy.removeProxies extrinsic.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

Notes

  * This removes all proxy relationships in a single call, which is more efficient than removing them one by one.

  * See Working with Proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>




remove_proxy(_delegate_ , _proxy_type_ , _delay_)[#](<#bittensor.core.extrinsics.pallets.proxy.Proxy.remove_proxy> "Link to this definition")
    

Remove a specific proxy relationship.

Parameters:
    

  * **delegate** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the delegate proxy account to remove.

  * **proxy_type** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The type of proxy permissions to remove. Must match the value used when the proxy was added.

  * **delay** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The announcement delay value (in blocks) for the proxy being removed. Must exactly match the delay value that was set when the proxy was originally added. This is a required identifier for the specific proxy relationship.



Returns:
    

GenericCall instance for the Proxy.removeProxy extrinsic.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

Notes

See Working with Proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>

[ __ previous bittensor.core.extrinsics.pallets.mev_shield ](<../mev_shield/index.html> "previous page") [ next bittensor.core.extrinsics.pallets.subtensor_module __](<../subtensor_module/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Proxy`](<#bittensor.core.extrinsics.pallets.proxy.Proxy>)
      * [`Proxy.add_proxy()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.add_proxy>)
      * [`Proxy.announce()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.announce>)
      * [`Proxy.create_pure()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.create_pure>)
      * [`Proxy.kill_pure()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.kill_pure>)
      * [`Proxy.poke_deposit()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.poke_deposit>)
      * [`Proxy.proxy()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.proxy>)
      * [`Proxy.proxy_announced()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.proxy_announced>)
      * [`Proxy.reject_announcement()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.reject_announcement>)
      * [`Proxy.remove_announcement()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.remove_announcement>)
      * [`Proxy.remove_proxies()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.remove_proxies>)
      * [`Proxy.remove_proxy()`](<#bittensor.core.extrinsics.pallets.proxy.Proxy.remove_proxy>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.