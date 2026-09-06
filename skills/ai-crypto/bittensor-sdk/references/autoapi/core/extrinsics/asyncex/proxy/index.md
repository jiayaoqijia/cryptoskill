# bittensor.core.extrinsics.asyncex.proxy &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/asyncex/proxy/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/asyncex/proxy/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../../_sources/autoapi/bittensor/core/extrinsics/asyncex/proxy/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.asyncex.proxy

##  Contents 

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`add_proxy_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.add_proxy_extrinsic>)
    * [`announce_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.announce_extrinsic>)
    * [`create_pure_proxy_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.create_pure_proxy_extrinsic>)
    * [`kill_pure_proxy_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.kill_pure_proxy_extrinsic>)
    * [`poke_deposit_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.poke_deposit_extrinsic>)
    * [`proxy_announced_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.proxy_announced_extrinsic>)
    * [`proxy_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.proxy_extrinsic>)
    * [`reject_announcement_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.reject_announcement_extrinsic>)
    * [`remove_announcement_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.remove_announcement_extrinsic>)
    * [`remove_proxies_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.remove_proxies_extrinsic>)
    * [`remove_proxy_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.remove_proxy_extrinsic>)



# bittensor.core.extrinsics.asyncex.proxy[#](<#module-bittensor.core.extrinsics.asyncex.proxy> "Link to this heading")

## Functions[#](<#functions> "Link to this heading")

[`add_proxy_extrinsic`](<#bittensor.core.extrinsics.asyncex.proxy.add_proxy_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.add_proxy_extrinsic")(subtensor, wallet, delegate_ss58, ...) | Adds a proxy relationship.  
---|---  
[`announce_extrinsic`](<#bittensor.core.extrinsics.asyncex.proxy.announce_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.announce_extrinsic")(subtensor, wallet, ...[, ...]) | Announces a future call that will be executed through a proxy.  
[`create_pure_proxy_extrinsic`](<#bittensor.core.extrinsics.asyncex.proxy.create_pure_proxy_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.create_pure_proxy_extrinsic")(subtensor, wallet, ...[, ...]) | Creates a pure proxy account.  
[`kill_pure_proxy_extrinsic`](<#bittensor.core.extrinsics.asyncex.proxy.kill_pure_proxy_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.kill_pure_proxy_extrinsic")(subtensor, wallet, ...[, ...]) | Kills (removes) a pure proxy account.  
[`poke_deposit_extrinsic`](<#bittensor.core.extrinsics.asyncex.proxy.poke_deposit_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.poke_deposit_extrinsic")(subtensor, wallet, *[, ...]) | Adjusts deposits made for proxies and announcements based on current values.  
[`proxy_announced_extrinsic`](<#bittensor.core.extrinsics.asyncex.proxy.proxy_announced_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.proxy_announced_extrinsic")(subtensor, wallet, ...[, ...]) | Executes an announced call on behalf of the real account through a proxy.  
[`proxy_extrinsic`](<#bittensor.core.extrinsics.asyncex.proxy.proxy_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.proxy_extrinsic")(subtensor, wallet, real_account_ss58, ...) | Executes a call on behalf of the real account through a proxy.  
[`reject_announcement_extrinsic`](<#bittensor.core.extrinsics.asyncex.proxy.reject_announcement_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.reject_announcement_extrinsic")(subtensor, wallet, ...) | Rejects an announcement made by a proxy delegate.  
[`remove_announcement_extrinsic`](<#bittensor.core.extrinsics.asyncex.proxy.remove_announcement_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.remove_announcement_extrinsic")(subtensor, wallet, ...) | Removes an announcement made by a proxy account.  
[`remove_proxies_extrinsic`](<#bittensor.core.extrinsics.asyncex.proxy.remove_proxies_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.remove_proxies_extrinsic")(subtensor, wallet, *[, ...]) | Removes all proxy relationships for the account.  
[`remove_proxy_extrinsic`](<#bittensor.core.extrinsics.asyncex.proxy.remove_proxy_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.remove_proxy_extrinsic")(subtensor, wallet, ...[, ...]) | Removes a proxy relationship.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

async bittensor.core.extrinsics.asyncex.proxy.add_proxy_extrinsic(_subtensor_ , _wallet_ , _delegate_ss58_ , _proxy_type_ , _delay_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.proxy.add_proxy_extrinsic> "Link to this definition")
    

Adds a proxy relationship.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Subtensor instance with the connection to the chain.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object.

  * **delegate_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the delegate proxy account.

  * **proxy_type** (_Union_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_bittensor.core.chain_data.proxy.ProxyType_](<../../../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType> "bittensor.core.chain_data.proxy.ProxyType") _]_) – The type of proxy permissions (e.g., `"Any"`, `"NonTransfer"`, `"Governance"`, `"Staking"`). Can be a string or `ProxyType` enum value. For available proxy types and their permissions, see the documentation link in the Notes section below.

  * **delay** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Optionally, include a delay in blocks. The number of blocks that must elapse between announcing and executing a proxied transaction (time-lock period). A delay of `0` means the proxy can be used immediately without announcements. A non-zero delay creates a time-lock, requiring the proxy to announce calls first, wait for the delay period, then execute them, giving the real account time to review and reject unwanted operations.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If `True`, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If `False`, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning `False` if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * A deposit is required when adding a proxy. The deposit amount is determined by runtime constants and is returned when the proxy is removed.

  * For available proxy types and their specific permissions, see: <<https://docs.learnbittensor.org/keys/proxies#types-of-proxies>>

  * See Working with Proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>




Warning

  * The `"Any"` proxy type is dangerous as it grants full permissions to the proxy, including the ability to make transfers and manage the account completely. Use with extreme caution.

  * If `wait_for_inclusion=False` or when `block_hash` is not available, the extrinsic receipt may not contain triggered events. This means that any data that would normally be extracted from blockchain events (such as proxy relationship details) will not be available in the response. To ensure complete event data is available, either pass `wait_for_inclusion=True` when calling this function, or retrieve the data manually from the blockchain using the extrinsic hash.




async bittensor.core.extrinsics.asyncex.proxy.announce_extrinsic(_subtensor_ , _wallet_ , _real_account_ss58_ , _call_hash_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.proxy.announce_extrinsic> "Link to this definition")
    

Announces a future call that will be executed through a proxy.

This extrinsic allows a proxy account to declare its intention to execute a specific call on behalf of a real account after a delay period. The real account can review and either approve or reject the announcement.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Subtensor instance with the connection to the chain.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (should be the proxy account wallet).

  * **real_account_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the real account on whose behalf the call will be made.

  * **call_hash** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hash of the call that will be executed in the future (hex string with `0x` prefix).

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If `True`, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If `False`, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning `False` if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * A deposit is required when making an announcement. The deposit is returned when the announcement is executed, rejected, or removed. The announcement can be executed after the delay period has passed.

  * See Working with Proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>




async bittensor.core.extrinsics.asyncex.proxy.create_pure_proxy_extrinsic(_subtensor_ , _wallet_ , _proxy_type_ , _delay_ , _index_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.proxy.create_pure_proxy_extrinsic> "Link to this definition")
    

Creates a pure proxy account.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Subtensor instance with the connection to the chain.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object.

  * **proxy_type** (_Union_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_bittensor.core.chain_data.proxy.ProxyType_](<../../../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType> "bittensor.core.chain_data.proxy.ProxyType") _]_) – The type of proxy permissions for the pure proxy. Can be a string or `ProxyType` enum value. For available proxy types and their permissions, see the documentation link in the Notes section below.

  * **delay** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Optionally, include a delay in blocks. The number of blocks that must elapse between announcing and executing a proxied transaction (time-lock period). A delay of `0` means the pure proxy can be used immediately without any announcement period. A non-zero delay creates a time-lock, requiring announcements before execution to give the spawner time to review/reject.

  * **index** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – A salt value (u16, range `0-65535`) used to generate unique pure proxy addresses. This should generally be left as `0` unless you are creating batches of proxies. When creating multiple pure proxies with identical parameters (same `proxy_type` and `delay`), different index values will produce different SS58 addresses. This is not a sequential counter—you can use any unique values (e.g., 0, 100, 7, 42) in any order. The index must be preserved as it’s required for [`kill_pure_proxy_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.kill_pure_proxy_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.kill_pure_proxy_extrinsic"). If creating multiple pure proxies in a single batch transaction, each must have a unique index value.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If `True`, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If `False`, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning `False` if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * The pure proxy account address can be extracted from the “PureCreated” event in the response. Store the spawner address, proxy_type, index, height, and ext_index as they are required to kill the pure proxy later.

  * For available proxy types and their specific permissions, see: <<https://docs.learnbittensor.org/keys/proxies#types-of-proxies>>

  * See Pure Proxies: <<https://docs.learnbittensor.org/keys/proxies/pure-proxies>>




Warning

  * The `"Any"` proxy type is dangerous as it grants full permissions to the proxy, including the ability to make transfers and kill the proxy. Use with extreme caution.

  * If `wait_for_inclusion=False` or when `block_hash` is not available, the extrinsic receipt may not contain triggered events. This means that any data that would normally be extracted from blockchain events (such as the pure proxy account address) will not be available in the response. To ensure complete event data is available, either pass `wait_for_inclusion=True` when calling this function, or retrieve the data manually from the blockchain using the extrinsic hash.




async bittensor.core.extrinsics.asyncex.proxy.kill_pure_proxy_extrinsic(_subtensor_ , _wallet_ , _pure_proxy_ss58_ , _spawner_ , _proxy_type_ , _index_ , _height_ , _ext_index_ , _force_proxy_type =ProxyType.Any_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.proxy.kill_pure_proxy_extrinsic> "Link to this definition")
    

Kills (removes) a pure proxy account.

This method removes a pure proxy account that was previously created via create_pure_proxy(). The kill_pure call must be executed through the pure proxy account itself, with the spawner acting as an “Any” proxy. This method automatically handles this by executing the call via proxy().

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Subtensor instance with the connection to the chain.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object. The wallet.coldkey.ss58_address must be the spawner of the pure proxy (the account that created it via [`create_pure_proxy_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.create_pure_proxy_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.create_pure_proxy_extrinsic")). The spawner must have an Any proxy relationship with the pure proxy.

  * **pure_proxy_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the pure proxy account to be killed. This is the address that was returned in the [`create_pure_proxy_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.create_pure_proxy_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.create_pure_proxy_extrinsic") response.

  * **spawner** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the spawner account (the account that originally created the pure proxy via [`create_pure_proxy_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.create_pure_proxy_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.create_pure_proxy_extrinsic")). This should match wallet.coldkey.ss58_address.

  * **proxy_type** (_Union_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_bittensor.core.chain_data.proxy.ProxyType_](<../../../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType> "bittensor.core.chain_data.proxy.ProxyType") _]_) – The type of proxy permissions that were used when creating the pure proxy. This must match exactly the proxy_type that was passed to [`create_pure_proxy_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.create_pure_proxy_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.create_pure_proxy_extrinsic").

  * **index** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The salt value (u16, range 0-65535) originally used in [`create_pure_proxy_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.create_pure_proxy_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.create_pure_proxy_extrinsic") to generate this pure proxy’s address. This value, combined with proxy_type, delay, and spawner, uniquely identifies the pure proxy to be killed. Must match exactly the index used during creation.

  * **height** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The block number at which the pure proxy was created. This is returned in the PureCreated event from [`create_pure_proxy_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.create_pure_proxy_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.create_pure_proxy_extrinsic") and is required to identify the exact creation transaction.

  * **ext_index** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The extrinsic index within the block at which the pure proxy was created. This is returned in the PureCreated event from [`create_pure_proxy_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.create_pure_proxy_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.create_pure_proxy_extrinsic") and specifies the position of the creation extrinsic within the block. Together with height, this uniquely identifies the creation transaction.

  * **force_proxy_type** (_Optional_ _[__Union_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_bittensor.core.chain_data.proxy.ProxyType_](<../../../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType> "bittensor.core.chain_data.proxy.ProxyType") _]__]_) – The proxy type relationship to use when executing kill_pure through the proxy mechanism. Since pure proxies are keyless and cannot sign transactions, the spawner must act as a proxy for the pure proxy to execute kill_pure. This parameter specifies which proxy type relationship between the spawner and the pure proxy account should be used. The spawner must have a proxy relationship of this type (or Any) with the pure proxy account. Defaults to ProxyType.Any for maximum compatibility. If None, Substrate will automatically select an available proxy type from the spawner’s proxy relationships.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * The kill_pure call must be executed through the pure proxy account itself, with the spawner acting as a proxy. This method automatically handles this by executing the call via [`proxy_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.proxy_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.proxy_extrinsic"). By default, force_proxy_type is set to ProxyType.Any, meaning the spawner must have an Any proxy relationship with the pure proxy. If you pass a different force_proxy_type, the spawner must have that specific proxy type relationship with the pure proxy.

  * See Pure Proxies: <<https://docs.learnbittensor.org/keys/proxies/pure-proxies>>




Warning

All access to this account will be lost. Any funds remaining in the pure proxy account will become permanently inaccessible after this operation.

Example

# After creating a pure proxy create_response = subtensor.proxies.create_pure_proxy(

> wallet=spawner_wallet, proxy_type=ProxyType.Any, # Type of proxy permissions for the pure proxy delay=0, index=0,

) pure_proxy_ss58 = create_response.data[“pure_account”] spawner = create_response.data[“spawner”] proxy_type_used = create_response.data[“proxy_type”] # The proxy_type used during creation height = create_response.data[“height”] ext_index = create_response.data[“ext_index”]

# Kill the pure proxy # Note: force_proxy_type defaults to ProxyType.Any (spawner must have Any proxy relationship) kill_response = subtensor.proxies.kill_pure_proxy(

> wallet=spawner_wallet, pure_proxy_ss58=pure_proxy_ss58, spawner=spawner, proxy_type=proxy_type_used, # Must match the proxy_type used during creation index=0, height=height, ext_index=ext_index, # force_proxy_type=ProxyType.Any, # Optional: defaults to ProxyType.Any

)

async bittensor.core.extrinsics.asyncex.proxy.poke_deposit_extrinsic(_subtensor_ , _wallet_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.proxy.poke_deposit_extrinsic> "Link to this definition")
    

Adjusts deposits made for proxies and announcements based on current values.

This can be used by accounts to possibly lower their locked amount. The function automatically recalculates deposits for both proxy relationships and announcements for the signing account. The transaction fee is waived if the deposit amount has changed.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Subtensor instance with the connection to the chain.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (the account whose deposits will be adjusted).

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning `False` if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

When to use:
    

  * After runtime upgrade, if deposit constants have changed.

  * After removing proxies/announcements, to free up excess locked funds.

  * Periodically to optimize locked deposit amounts.




  * See Working with Proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>




async bittensor.core.extrinsics.asyncex.proxy.proxy_announced_extrinsic(_subtensor_ , _wallet_ , _delegate_ss58_ , _real_account_ss58_ , _force_proxy_type_ , _call_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.proxy.proxy_announced_extrinsic> "Link to this definition")
    

Executes an announced call on behalf of the real account through a proxy.

This extrinsic executes a call that was previously announced via [`announce_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.announce_extrinsic> "bittensor.core.extrinsics.asyncex.proxy.announce_extrinsic"). The call must match the `call_hash` that was announced, and the delay period must have passed.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Subtensor instance with the connection to the chain.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (should be the proxy account wallet that made the announcement).

  * **delegate_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the delegate proxy account that made the announcement.

  * **real_account_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the real account on whose behalf the call will be made.

  * **force_proxy_type** (_Optional_ _[__Union_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_bittensor.core.chain_data.proxy.ProxyType_](<../../../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType> "bittensor.core.chain_data.proxy.ProxyType") _]__]_) – The type of proxy to use for the call. If `None`, any proxy type can be used. Otherwise, must match one of the allowed proxy types. Can be a string or `ProxyType` enum value.

  * **call** (_scalecodec.types.GenericCall_) – The inner call to be executed on behalf of the real account (must match the announced `call_hash`).

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If `True`, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If `False`, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning `False` if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * The `call_hash` of the provided call must match the `call_hash` that was announced. The announcement must not have been rejected by the real account, and the delay period must have passed.

  * See Working with Proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>




async bittensor.core.extrinsics.asyncex.proxy.proxy_extrinsic(_subtensor_ , _wallet_ , _real_account_ss58_ , _force_proxy_type_ , _call_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.proxy.proxy_extrinsic> "Link to this definition")
    

Executes a call on behalf of the real account through a proxy.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Subtensor instance with the connection to the chain.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (should be the proxy account wallet).

  * **real_account_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the real account on whose behalf the call is being made.

  * **force_proxy_type** (_Optional_ _[__Union_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_bittensor.core.chain_data.proxy.ProxyType_](<../../../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType> "bittensor.core.chain_data.proxy.ProxyType") _]__]_) – The type of proxy to use for the call. If `None`, any proxy type can be used. Otherwise, must match one of the allowed proxy types. Can be a string or `ProxyType` enum value.

  * **call** (_scalecodec.types.GenericCall_) – The inner call to be executed on behalf of the real account.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning `False` if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * The call must be permitted by the proxy type. For example, a `"NonTransfer"` proxy cannot execute transfer calls.

  * See Working with Proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>




async bittensor.core.extrinsics.asyncex.proxy.reject_announcement_extrinsic(_subtensor_ , _wallet_ , _delegate_ss58_ , _call_hash_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.proxy.reject_announcement_extrinsic> "Link to this definition")
    

Rejects an announcement made by a proxy delegate.

This extrinsic allows the real account to reject an announcement made by a proxy delegate, preventing the announced call from being executed. Once rejected, the announcement cannot be executed and the announcement deposit is returned to the delegate.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Subtensor instance with the connection to the chain.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (should be the real account wallet).

  * **delegate_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the delegate proxy account whose announcement is being rejected.

  * **call_hash** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hash of the call that was announced and is now being rejected (hex string with `0x` prefix).

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If `True`, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If `False`, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning `False` if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Once rejected, the announcement cannot be executed. The delegate’s announcement deposit is returned.

  * See Working with Proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>




async bittensor.core.extrinsics.asyncex.proxy.remove_announcement_extrinsic(_subtensor_ , _wallet_ , _real_account_ss58_ , _call_hash_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.proxy.remove_announcement_extrinsic> "Link to this definition")
    

Removes an announcement made by a proxy account.

This extrinsic allows the proxy account to remove its own announcement before it is executed or rejected. This frees up the announcement deposit.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Subtensor instance with the connection to the chain.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (should be the proxy account wallet that made the announcement).

  * **real_account_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the real account on whose behalf the call was announced.

  * **call_hash** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hash of the call that was announced and is now being removed (hex string with `0x` prefix).

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If `True`, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If `False`, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning `False` if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Removing an announcement frees up the announcement deposit.

  * See Working with Proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>




async bittensor.core.extrinsics.asyncex.proxy.remove_proxies_extrinsic(_subtensor_ , _wallet_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.proxy.remove_proxies_extrinsic> "Link to this definition")
    

Removes all proxy relationships for the account.

This removes all proxy relationships in a single call, which is more efficient than removing them one by one. The deposit for all proxies will be returned.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Subtensor instance with the connection to the chain.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (the account whose proxies will be removed).

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning `False` if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * This removes all proxy relationships for the account, regardless of proxy type or delegate.

  * See Working with Proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>




async bittensor.core.extrinsics.asyncex.proxy.remove_proxy_extrinsic(_subtensor_ , _wallet_ , _delegate_ss58_ , _proxy_type_ , _delay_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.proxy.remove_proxy_extrinsic> "Link to this definition")
    

Removes a proxy relationship.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Subtensor instance with the connection to the chain.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object.

  * **delegate_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the delegate proxy account to remove.

  * **proxy_type** (_Union_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_bittensor.core.chain_data.proxy.ProxyType_](<../../../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType> "bittensor.core.chain_data.proxy.ProxyType") _]_) – The type of proxy permissions to remove. Can be a string or `ProxyType` enum value.

  * **delay** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The announcement delay value (in blocks) for the proxy being removed. Must exactly match the delay value that was set when the proxy was originally added. This is a required identifier for the specific proxy relationship, not a delay before removal takes effect (removal is immediate).

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If `True`, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If `False`, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning `False` if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * The delegate_ss58, proxy_type, and delay parameters must exactly match those used when the proxy was added.

  * See Working with Proxies: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>




[ __ previous bittensor.core.extrinsics.asyncex.move_stake ](<../move_stake/index.html> "previous page") [ next bittensor.core.extrinsics.asyncex.registration __](<../registration/index.html> "next page")

__Contents

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`add_proxy_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.add_proxy_extrinsic>)
    * [`announce_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.announce_extrinsic>)
    * [`create_pure_proxy_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.create_pure_proxy_extrinsic>)
    * [`kill_pure_proxy_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.kill_pure_proxy_extrinsic>)
    * [`poke_deposit_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.poke_deposit_extrinsic>)
    * [`proxy_announced_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.proxy_announced_extrinsic>)
    * [`proxy_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.proxy_extrinsic>)
    * [`reject_announcement_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.reject_announcement_extrinsic>)
    * [`remove_announcement_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.remove_announcement_extrinsic>)
    * [`remove_proxies_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.remove_proxies_extrinsic>)
    * [`remove_proxy_extrinsic()`](<#bittensor.core.extrinsics.asyncex.proxy.remove_proxy_extrinsic>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.   

  *[*]: Keyword-only parameters separator (PEP 3102)