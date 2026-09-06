# bittensor.core.extrinsics.unstaking &#8212; Bittensor SDK Docs  documentation

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
        * [bittensor.core.chain_data](<../../chain_data/index.html>)
        * [bittensor.core.config](<../../config/index.html>)
        * [bittensor.core.dendrite](<../../dendrite/index.html>)
        * [bittensor.core.errors](<../../errors/index.html>)
        * [bittensor.core.extrinsics](<../index.html>)
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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/unstaking/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/unstaking/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/extrinsics/unstaking/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.unstaking

##  Contents 

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`unstake_all_extrinsic()`](<#bittensor.core.extrinsics.unstaking.unstake_all_extrinsic>)
    * [`unstake_extrinsic()`](<#bittensor.core.extrinsics.unstaking.unstake_extrinsic>)
    * [`unstake_multiple_extrinsic()`](<#bittensor.core.extrinsics.unstaking.unstake_multiple_extrinsic>)



# bittensor.core.extrinsics.unstaking[#](<#module-bittensor.core.extrinsics.unstaking> "Link to this heading")

## Functions[#](<#functions> "Link to this heading")

[`unstake_all_extrinsic`](<#bittensor.core.extrinsics.unstaking.unstake_all_extrinsic> "bittensor.core.extrinsics.unstaking.unstake_all_extrinsic")(subtensor, wallet, netuid, ...) | Unstakes all TAO/Alpha associated with a hotkey from the specified subnets on the Bittensor network.  
---|---  
[`unstake_extrinsic`](<#bittensor.core.extrinsics.unstaking.unstake_extrinsic> "bittensor.core.extrinsics.unstaking.unstake_extrinsic")(subtensor, wallet, netuid, ...[, ...]) | Removes stake into the wallet coldkey from the specified hotkey `uid`.  
[`unstake_multiple_extrinsic`](<#bittensor.core.extrinsics.unstaking.unstake_multiple_extrinsic> "bittensor.core.extrinsics.unstaking.unstake_multiple_extrinsic")(subtensor, wallet, netuids, ...) | Removes stake from each `hotkey_ss58` in the list, using each amount, to a common coldkey.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

bittensor.core.extrinsics.unstaking.unstake_all_extrinsic(_subtensor_ , _wallet_ , _netuid_ , _hotkey_ss58_ , _rate_tolerance =0.005_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.unstaking.unstake_all_extrinsic> "Link to this definition")
    

Unstakes all TAO/Alpha associated with a hotkey from the specified subnets on the Bittensor network.

Parameters:
    

  * **subtensor** ([_bittensor.core.subtensor.Subtensor_](<../../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor")) – Subtensor instance.

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet of the stake owner.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the hotkey to unstake from.

  * **rate_tolerance** (_Optional_ _[_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _]_) – The maximum allowed price change ratio when unstaking. For example, 0.005 = 0.5% maximum price decrease. If not passed (None), then unstaking goes without price limit.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

bittensor.core.extrinsics.unstaking.unstake_extrinsic(_subtensor_ , _wallet_ , _netuid_ , _hotkey_ss58_ , _amount_ , _allow_partial_stake =False_, _rate_tolerance =0.005_, _safe_unstaking =False_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.unstaking.unstake_extrinsic> "Link to this definition")
    

Removes stake into the wallet coldkey from the specified hotkey `uid`.

Parameters:
    

  * **subtensor** ([_bittensor.core.subtensor.Subtensor_](<../../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor")) – Subtensor instance.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The `ss58` address of the hotkey to unstake from.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Subnet unique id.

  * **amount** ([_bittensor.utils.balance.Balance_](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – Amount to stake as Bittensor balance.

  * **allow_partial_stake** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If true, allows partial unstaking if price tolerance exceeded.

  * **rate_tolerance** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")) – Maximum allowed price decrease percentage (0.005 = 0.5%).

  * **safe_unstaking** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If true, enables price safety checks.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

bittensor.core.extrinsics.unstaking.unstake_multiple_extrinsic(_subtensor_ , _wallet_ , _netuids_ , _hotkey_ss58s_ , _amounts =None_, _rate_tolerance =0.05_, _unstake_all =False_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.unstaking.unstake_multiple_extrinsic> "Link to this definition")
    

Removes stake from each `hotkey_ss58` in the list, using each amount, to a common coldkey.

Parameters:
    

  * **subtensor** ([_bittensor.core.subtensor.Subtensor_](<../../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor")) – Subtensor instance.

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet with the coldkey to unstake to.

  * **netuids** ([_bittensor.core.types.UIDs_](<../../types/index.html#bittensor.core.types.UIDs> "bittensor.core.types.UIDs")) – List of subnets unique IDs to unstake from.

  * **hotkey_ss58s** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – List of hotkeys to unstake from.

  * **amounts** (_Optional_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_bittensor.utils.balance.Balance_](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") _]__]_) – List of amounts to unstake. If `None`, unstake all.

  * **rate_tolerance** (_Optional_ _[_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _]_) – Maximum allowed price decrease percentage (0.005 = 0.5%).

  * **unstake_all** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If true, unstakes all tokens.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Note

The data field in the returned ExtrinsicResponse contains the results of each individual internal unstake_extrinsic or unstake_all_extrinsic call. Each entry maps a tuple key (idx, hotkey_ss58, netuid) to either:

>   * the corresponding ExtrinsicResponse object if the unstaking attempt was executed, or
> 
>   * None if the unstaking was skipped due to failing validation (e.g., wrong balance, zero amount, etc.).
> 
> 


In the key, idx is the index the unstake attempt. This allows the caller to inspect which specific operations were attempted and which were not.

[ __ previous bittensor.core.extrinsics.transfer ](<../transfer/index.html> "previous page") [ next bittensor.core.extrinsics.utils __](<../utils/index.html> "next page")

__Contents

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`unstake_all_extrinsic()`](<#bittensor.core.extrinsics.unstaking.unstake_all_extrinsic>)
    * [`unstake_extrinsic()`](<#bittensor.core.extrinsics.unstaking.unstake_extrinsic>)
    * [`unstake_multiple_extrinsic()`](<#bittensor.core.extrinsics.unstaking.unstake_multiple_extrinsic>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.   

  *[*]: Keyword-only parameters separator (PEP 3102)