# bittensor.core.extrinsics.staking &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/staking/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/staking/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/extrinsics/staking/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.staking

##  Contents 

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`add_stake_burn_extrinsic()`](<#bittensor.core.extrinsics.staking.add_stake_burn_extrinsic>)
    * [`add_stake_extrinsic()`](<#bittensor.core.extrinsics.staking.add_stake_extrinsic>)
    * [`add_stake_multiple_extrinsic()`](<#bittensor.core.extrinsics.staking.add_stake_multiple_extrinsic>)
    * [`set_auto_stake_extrinsic()`](<#bittensor.core.extrinsics.staking.set_auto_stake_extrinsic>)



# bittensor.core.extrinsics.staking[#](<#module-bittensor.core.extrinsics.staking> "Link to this heading")

## Functions[#](<#functions> "Link to this heading")

[`add_stake_burn_extrinsic`](<#bittensor.core.extrinsics.staking.add_stake_burn_extrinsic> "bittensor.core.extrinsics.staking.add_stake_burn_extrinsic")(subtensor, wallet, netuid, ...) | Executes a subnet buyback by staking TAO and immediately burning the resulting Alpha.  
---|---  
[`add_stake_extrinsic`](<#bittensor.core.extrinsics.staking.add_stake_extrinsic> "bittensor.core.extrinsics.staking.add_stake_extrinsic")(subtensor, wallet, netuid, ...[, ...]) | Adds a stake from the specified wallet to the neuron identified by the SS58 address of its hotkey in specified subnet.  
[`add_stake_multiple_extrinsic`](<#bittensor.core.extrinsics.staking.add_stake_multiple_extrinsic> "bittensor.core.extrinsics.staking.add_stake_multiple_extrinsic")(subtensor, wallet, ...[, ...]) | Adds stake to each `hotkey_ss58` in the list, using each amount, from a common coldkey on subnet with  
[`set_auto_stake_extrinsic`](<#bittensor.core.extrinsics.staking.set_auto_stake_extrinsic> "bittensor.core.extrinsics.staking.set_auto_stake_extrinsic")(subtensor, wallet, netuid, ...) | Sets the coldkey to automatically stake to the hotkey within specific subnet mechanism.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

bittensor.core.extrinsics.staking.add_stake_burn_extrinsic(_subtensor_ , _wallet_ , _netuid_ , _hotkey_ss58_ , _amount_ , _limit_price =None_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.staking.add_stake_burn_extrinsic> "Link to this definition")
    

Executes a subnet buyback by staking TAO and immediately burning the resulting Alpha.

Parameters:
    

  * **subtensor** ([_bittensor.core.subtensor.Subtensor_](<../../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor")) – Subtensor instance with the connection to the chain.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The ss58 address of the hotkey account to stake to.

  * **amount** ([_bittensor.utils.balance.Balance_](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – Amount to stake as Bittensor balance in TAO always.

  * **limit_price** (_Optional_ _[_[_bittensor.utils.balance.Balance_](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") _]_) – Optional limit price expressed in units of RAO per one Alpha.

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

Raises:
    

**SubstrateRequestException** – Raised if the extrinsic fails to be included in the block within the timeout.

Notes

The data field in the returned ExtrinsicResponse contains extra information about the extrinsic execution.

bittensor.core.extrinsics.staking.add_stake_extrinsic(_subtensor_ , _wallet_ , _netuid_ , _hotkey_ss58_ , _amount_ , _safe_staking =False_, _allow_partial_stake =False_, _rate_tolerance =0.005_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.staking.add_stake_extrinsic> "Link to this definition")
    

Adds a stake from the specified wallet to the neuron identified by the SS58 address of its hotkey in specified subnet. Staking is a fundamental process in the Bittensor network that enables neurons to participate actively and earn incentives.

Parameters:
    

  * **subtensor** ([_bittensor.core.subtensor.Subtensor_](<../../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor")) – Subtensor instance with the connection to the chain.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet to which the neuron belongs.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The ss58 address of the hotkey account to stake to default to the wallet’s hotkey.

  * **amount** ([_bittensor.utils.balance.Balance_](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – Amount to stake as Bittensor balance in TAO always.

  * **safe_staking** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, enables price safety checks.

  * **allow_partial_stake** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, allows partial unstaking if price tolerance exceeded.

  * **rate_tolerance** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")) – Maximum allowed price increase percentage (0.005 = 0.5%).

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the staking transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Raises:
    

**SubstrateRequestException** – Raised if the extrinsic fails to be included in the block within the timeout.

Notes

The data field in the returned ExtrinsicResponse contains extra information about the extrinsic execution.

bittensor.core.extrinsics.staking.add_stake_multiple_extrinsic(_subtensor_ , _wallet_ , _netuids_ , _hotkey_ss58s_ , _amounts_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.staking.add_stake_multiple_extrinsic> "Link to this definition")
    

Adds stake to each `hotkey_ss58` in the list, using each amount, from a common coldkey on subnet with corresponding netuid.

Parameters:
    

  * **subtensor** ([_bittensor.core.subtensor.Subtensor_](<../../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor")) – Subtensor instance with the connection to the chain.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object for the coldkey.

  * **netuids** ([_bittensor.core.types.UIDs_](<../../types/index.html#bittensor.core.types.UIDs> "bittensor.core.types.UIDs")) – List of netuids to stake to.

  * **hotkey_ss58s** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – List of hotkeys to stake to.

  * **amounts** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_bittensor.utils.balance.Balance_](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") _]_) – List of corresponding TAO amounts to bet for each netuid and hotkey.

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

The data field in the returned ExtrinsicResponse contains the results of each individual internal add_stake_extrinsic call. Each entry maps a tuple key (idx, hotkey_ss58, netuid) to either:

>   * the corresponding ExtrinsicResponse object if the staking attempt was executed, or
> 
>   * None if the staking was skipped due to failing validation (e.g., wrong balance, zero amount, etc.).
> 
> 


In the key, idx is the index the stake attempt. This allows the caller to inspect which specific operations were attempted and which were not.

bittensor.core.extrinsics.staking.set_auto_stake_extrinsic(_subtensor_ , _wallet_ , _netuid_ , _hotkey_ss58_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.staking.set_auto_stake_extrinsic> "Link to this definition")
    

Sets the coldkey to automatically stake to the hotkey within specific subnet mechanism.

Parameters:
    

  * **subtensor** ([_bittensor.core.subtensor.Subtensor_](<../../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor")) – AsyncSubtensor instance.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet unique identifier.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the validator’s hotkey to which the miner automatically stakes all rewards received from the specified subnet immediately upon receipt.

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

[ __ previous bittensor.core.extrinsics.serving ](<../serving/index.html> "previous page") [ next bittensor.core.extrinsics.start_call __](<../start_call/index.html> "next page")

__Contents

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`add_stake_burn_extrinsic()`](<#bittensor.core.extrinsics.staking.add_stake_burn_extrinsic>)
    * [`add_stake_extrinsic()`](<#bittensor.core.extrinsics.staking.add_stake_extrinsic>)
    * [`add_stake_multiple_extrinsic()`](<#bittensor.core.extrinsics.staking.add_stake_multiple_extrinsic>)
    * [`set_auto_stake_extrinsic()`](<#bittensor.core.extrinsics.staking.set_auto_stake_extrinsic>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.   

  *[*]: Keyword-only parameters separator (PEP 3102)