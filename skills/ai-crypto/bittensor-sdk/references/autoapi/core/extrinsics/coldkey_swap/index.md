# bittensor.core.extrinsics.coldkey_swap &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/coldkey_swap/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/coldkey_swap/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/extrinsics/coldkey_swap/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.coldkey_swap

##  Contents 

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`announce_coldkey_swap_extrinsic()`](<#bittensor.core.extrinsics.coldkey_swap.announce_coldkey_swap_extrinsic>)
    * [`clear_coldkey_swap_announcement_extrinsic()`](<#bittensor.core.extrinsics.coldkey_swap.clear_coldkey_swap_announcement_extrinsic>)
    * [`dispute_coldkey_swap_extrinsic()`](<#bittensor.core.extrinsics.coldkey_swap.dispute_coldkey_swap_extrinsic>)
    * [`remove_coldkey_swap_announcement_extrinsic()`](<#bittensor.core.extrinsics.coldkey_swap.remove_coldkey_swap_announcement_extrinsic>)
    * [`swap_coldkey_announced_extrinsic()`](<#bittensor.core.extrinsics.coldkey_swap.swap_coldkey_announced_extrinsic>)



# bittensor.core.extrinsics.coldkey_swap[#](<#module-bittensor.core.extrinsics.coldkey_swap> "Link to this heading")

## Functions[#](<#functions> "Link to this heading")

[`announce_coldkey_swap_extrinsic`](<#bittensor.core.extrinsics.coldkey_swap.announce_coldkey_swap_extrinsic> "bittensor.core.extrinsics.coldkey_swap.announce_coldkey_swap_extrinsic")(subtensor, wallet, ...) | Announces a coldkey swap by submitting the BlakeTwo256 hash of the new coldkey.  
---|---  
[`clear_coldkey_swap_announcement_extrinsic`](<#bittensor.core.extrinsics.coldkey_swap.clear_coldkey_swap_announcement_extrinsic> "bittensor.core.extrinsics.coldkey_swap.clear_coldkey_swap_announcement_extrinsic")(subtensor, ...) | Clears (withdraws) a pending coldkey swap announcement.  
[`dispute_coldkey_swap_extrinsic`](<#bittensor.core.extrinsics.coldkey_swap.dispute_coldkey_swap_extrinsic> "bittensor.core.extrinsics.coldkey_swap.dispute_coldkey_swap_extrinsic")(subtensor, wallet, *[, ...]) | Disputes the coldkey swap announcement for the current coldkey.  
[`remove_coldkey_swap_announcement_extrinsic`](<#bittensor.core.extrinsics.coldkey_swap.remove_coldkey_swap_announcement_extrinsic> "bittensor.core.extrinsics.coldkey_swap.remove_coldkey_swap_announcement_extrinsic")(subtensor, ...) | Removes a coldkey swap announcement.  
[`swap_coldkey_announced_extrinsic`](<#bittensor.core.extrinsics.coldkey_swap.swap_coldkey_announced_extrinsic> "bittensor.core.extrinsics.coldkey_swap.swap_coldkey_announced_extrinsic")(subtensor, wallet, ...) | Executes a previously announced coldkey swap.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

bittensor.core.extrinsics.coldkey_swap.announce_coldkey_swap_extrinsic(_subtensor_ , _wallet_ , _new_coldkey_ss58_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.coldkey_swap.announce_coldkey_swap_extrinsic> "Link to this definition")
    

Announces a coldkey swap by submitting the BlakeTwo256 hash of the new coldkey.

This extrinsic allows a coldkey to declare its intention to swap to a new coldkey address. The announcement must be made before the actual swap can be executed, and a delay period must pass before execution is allowed. After making an announcement, all transactions from the coldkey are blocked except for swap_coldkey_announced.

Parameters:
    

  * **subtensor** ([_bittensor.core.subtensor.Subtensor_](<../../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor")) – Subtensor instance with the connection to the chain.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (should be the current coldkey wallet).

  * **new_coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the new coldkey that will replace the current one.

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

Notes

  * A swap cost is charged when making the first announcement (not when reannouncing).

  * After making an announcement, all transactions from the coldkey are blocked except for swap_coldkey_announced.

  * The swap can only be executed after the delay period has passed (check via get_coldkey_swap_announcement).

  * The destination coldkey cannot have any staking hotkeys. It must be completely new without any staking activity.

  * See: <<https://docs.learnbittensor.org/keys/coldkey-swap>>




bittensor.core.extrinsics.coldkey_swap.clear_coldkey_swap_announcement_extrinsic(_subtensor_ , _wallet_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.coldkey_swap.clear_coldkey_swap_announcement_extrinsic> "Link to this definition")
    

Clears (withdraws) a pending coldkey swap announcement.

Callable by the coldkey that has an active, undisputed swap announcement. The reannouncement delay must have elapsed past the execution block before the announcement can be cleared.

Parameters:
    

  * **subtensor** ([_bittensor.core.subtensor.Subtensor_](<../../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor")) – Subtensor instance with the connection to the chain.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (should be the current coldkey with an active announcement).

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * The coldkey must have an active, undisputed swap announcement.

  * The reannouncement delay must have elapsed past the execution block.




bittensor.core.extrinsics.coldkey_swap.dispute_coldkey_swap_extrinsic(_subtensor_ , _wallet_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.coldkey_swap.dispute_coldkey_swap_extrinsic> "Link to this definition")
    

Disputes the coldkey swap announcement for the current coldkey.

Callable by the coldkey that has an active swap announcement. Marks the swap as disputed. The account is blocked until root calls reset_coldkey_swap.

Parameters:
    

  * **subtensor** ([_bittensor.core.subtensor.Subtensor_](<../../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor")) – Subtensor instance with the connection to the chain.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (should be the current coldkey with an active announcement).

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * The coldkey must have an active swap announcement.

  * After disputing, only root can clear the state via reset_coldkey_swap.




bittensor.core.extrinsics.coldkey_swap.remove_coldkey_swap_announcement_extrinsic(_subtensor_ , _wallet_ , _coldkey_ss58_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.coldkey_swap.remove_coldkey_swap_announcement_extrinsic> "Link to this definition")
    

Removes a coldkey swap announcement.

This extrinsic can only called by root. It removes a pending coldkey swap announcement for the specified coldkey.

Parameters:
    

  * **subtensor** ([_bittensor.core.subtensor.Subtensor_](<../../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor")) – Subtensor instance with the connection to the chain.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (must be root/admin wallet).

  * **coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the coldkey to remove the swap announcement for.

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

Notes

  * This function can only called by root.

  * See: <<https://docs.learnbittensor.org/keys/coldkey-swap>>




bittensor.core.extrinsics.coldkey_swap.swap_coldkey_announced_extrinsic(_subtensor_ , _wallet_ , _new_coldkey_ss58_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.coldkey_swap.swap_coldkey_announced_extrinsic> "Link to this definition")
    

Executes a previously announced coldkey swap.

This extrinsic executes a coldkey swap that was previously announced via announce_coldkey_swap_extrinsic. The new coldkey address must match the hash that was announced, and the delay period must have passed.

Parameters:
    

  * **subtensor** ([_bittensor.core.subtensor.Subtensor_](<../../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor")) – Subtensor instance with the connection to the chain.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (should be the current coldkey wallet that made the announcement).

  * **new_coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the new coldkey to swap to. This must match the hash that was announced.

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

Notes

  * The new coldkey hash must match the hash that was announced.

  * The delay period must have passed (check via get_coldkey_swap_announcement).

  * All assets, stakes, subnet ownerships, and hotkey associations are transferred from the old coldkey to the new one.

  * See: <<https://docs.learnbittensor.org/keys/coldkey-swap>>




[ __ previous bittensor.core.extrinsics.children ](<../children/index.html> "previous page") [ next bittensor.core.extrinsics.crowdloan __](<../crowdloan/index.html> "next page")

__Contents

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`announce_coldkey_swap_extrinsic()`](<#bittensor.core.extrinsics.coldkey_swap.announce_coldkey_swap_extrinsic>)
    * [`clear_coldkey_swap_announcement_extrinsic()`](<#bittensor.core.extrinsics.coldkey_swap.clear_coldkey_swap_announcement_extrinsic>)
    * [`dispute_coldkey_swap_extrinsic()`](<#bittensor.core.extrinsics.coldkey_swap.dispute_coldkey_swap_extrinsic>)
    * [`remove_coldkey_swap_announcement_extrinsic()`](<#bittensor.core.extrinsics.coldkey_swap.remove_coldkey_swap_announcement_extrinsic>)
    * [`swap_coldkey_announced_extrinsic()`](<#bittensor.core.extrinsics.coldkey_swap.swap_coldkey_announced_extrinsic>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.   

  *[*]: Keyword-only parameters separator (PEP 3102)