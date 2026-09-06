# bittensor.core.extrinsics.asyncex.move_stake &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/asyncex/move_stake/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/asyncex/move_stake/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../../_sources/autoapi/bittensor/core/extrinsics/asyncex/move_stake/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.asyncex.move_stake

##  Contents 

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`move_stake_extrinsic()`](<#bittensor.core.extrinsics.asyncex.move_stake.move_stake_extrinsic>)
    * [`swap_stake_extrinsic()`](<#bittensor.core.extrinsics.asyncex.move_stake.swap_stake_extrinsic>)
    * [`transfer_stake_extrinsic()`](<#bittensor.core.extrinsics.asyncex.move_stake.transfer_stake_extrinsic>)



# bittensor.core.extrinsics.asyncex.move_stake[#](<#module-bittensor.core.extrinsics.asyncex.move_stake> "Link to this heading")

## Functions[#](<#functions> "Link to this heading")

[`move_stake_extrinsic`](<#bittensor.core.extrinsics.asyncex.move_stake.move_stake_extrinsic> "bittensor.core.extrinsics.asyncex.move_stake.move_stake_extrinsic")(subtensor, wallet, origin_netuid, ...) | Moves stake from one hotkey to another within subnets in the Bittensor network.  
---|---  
[`swap_stake_extrinsic`](<#bittensor.core.extrinsics.asyncex.move_stake.swap_stake_extrinsic> "bittensor.core.extrinsics.asyncex.move_stake.swap_stake_extrinsic")(subtensor, wallet, hotkey_ss58, ...) | Swaps stake from one subnet to another for a given hotkey in the Bittensor network.  
[`transfer_stake_extrinsic`](<#bittensor.core.extrinsics.asyncex.move_stake.transfer_stake_extrinsic> "bittensor.core.extrinsics.asyncex.move_stake.transfer_stake_extrinsic")(subtensor, wallet, ...[, ...]) | Transfers stake from one coldkey to another in the Bittensor network.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

async bittensor.core.extrinsics.asyncex.move_stake.move_stake_extrinsic(_subtensor_ , _wallet_ , _origin_netuid_ , _origin_hotkey_ss58_ , _destination_netuid_ , _destination_hotkey_ss58_ , _amount =None_, _move_all_stake =False_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.move_stake.move_stake_extrinsic> "Link to this definition")
    

Moves stake from one hotkey to another within subnets in the Bittensor network.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Subtensor instance.

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet to move stake from.

  * **origin_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid of the source subnet.

  * **origin_hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the source hotkey.

  * **destination_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid of the destination subnet.

  * **destination_hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The SS58 address of the destination hotkey.

  * **amount** (_Optional_ _[_[_bittensor.utils.balance.Balance_](<../../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") _]_) – Amount to move.

  * **move_all_stake** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If true, moves all stake from the source hotkey to the destination hotkey.

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

async bittensor.core.extrinsics.asyncex.move_stake.swap_stake_extrinsic(_subtensor_ , _wallet_ , _hotkey_ss58_ , _origin_netuid_ , _destination_netuid_ , _amount_ , _safe_swapping =False_, _allow_partial_stake =False_, _rate_tolerance =0.005_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.move_stake.swap_stake_extrinsic> "Link to this definition")
    

Swaps stake from one subnet to another for a given hotkey in the Bittensor network.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Subtensor instance.

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet to swap stake from.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey SS58 address associated with the stake.

  * **origin_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The source subnet UID.

  * **destination_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The destination subnet UID.

  * **amount** ([_bittensor.utils.balance.Balance_](<../../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – Amount to swap.

  * **safe_swapping** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If true, enables price safety checks to protect against price impact.

  * **allow_partial_stake** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If true, allows partial stake swaps when the full amount would exceed the price tolerance.

  * **rate_tolerance** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")) – Maximum allowed increase in a price ratio (0.005 = 0.5%).

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

async bittensor.core.extrinsics.asyncex.move_stake.transfer_stake_extrinsic(_subtensor_ , _wallet_ , _destination_coldkey_ss58_ , _hotkey_ss58_ , _origin_netuid_ , _destination_netuid_ , _amount_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.move_stake.transfer_stake_extrinsic> "Link to this definition")
    

Transfers stake from one coldkey to another in the Bittensor network.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – The subtensor instance to interact with the blockchain.

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet containing the coldkey to authorize the transfer.

  * **destination_coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the destination coldkey.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the hotkey associated with the stake.

  * **origin_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Network UID of the origin subnet.

  * **destination_netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Network UID of the destination subnet.

  * **amount** ([_bittensor.utils.balance.Balance_](<../../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – The amount of stake to transfer as a Balance object.

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

[ __ previous bittensor.core.extrinsics.asyncex.mev_shield ](<../mev_shield/index.html> "previous page") [ next bittensor.core.extrinsics.asyncex.proxy __](<../proxy/index.html> "next page")

__Contents

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`move_stake_extrinsic()`](<#bittensor.core.extrinsics.asyncex.move_stake.move_stake_extrinsic>)
    * [`swap_stake_extrinsic()`](<#bittensor.core.extrinsics.asyncex.move_stake.swap_stake_extrinsic>)
    * [`transfer_stake_extrinsic()`](<#bittensor.core.extrinsics.asyncex.move_stake.transfer_stake_extrinsic>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.   

  *[*]: Keyword-only parameters separator (PEP 3102)