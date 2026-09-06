# bittensor.core.extrinsics.asyncex.sudo &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/asyncex/sudo/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/asyncex/sudo/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../../_sources/autoapi/bittensor/core/extrinsics/asyncex/sudo/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.asyncex.sudo

##  Contents 

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`reset_coldkey_swap_extrinsic()`](<#bittensor.core.extrinsics.asyncex.sudo.reset_coldkey_swap_extrinsic>)
    * [`sudo_set_admin_freeze_window_extrinsic()`](<#bittensor.core.extrinsics.asyncex.sudo.sudo_set_admin_freeze_window_extrinsic>)
    * [`sudo_set_coldkey_swap_announcement_delay_extrinsic()`](<#bittensor.core.extrinsics.asyncex.sudo.sudo_set_coldkey_swap_announcement_delay_extrinsic>)
    * [`sudo_set_coldkey_swap_reannouncement_delay_extrinsic()`](<#bittensor.core.extrinsics.asyncex.sudo.sudo_set_coldkey_swap_reannouncement_delay_extrinsic>)
    * [`sudo_set_mechanism_count_extrinsic()`](<#bittensor.core.extrinsics.asyncex.sudo.sudo_set_mechanism_count_extrinsic>)
    * [`sudo_set_mechanism_emission_split_extrinsic()`](<#bittensor.core.extrinsics.asyncex.sudo.sudo_set_mechanism_emission_split_extrinsic>)
    * [`swap_coldkey_extrinsic()`](<#bittensor.core.extrinsics.asyncex.sudo.swap_coldkey_extrinsic>)



# bittensor.core.extrinsics.asyncex.sudo[#](<#module-bittensor.core.extrinsics.asyncex.sudo> "Link to this heading")

## Functions[#](<#functions> "Link to this heading")

[`reset_coldkey_swap_extrinsic`](<#bittensor.core.extrinsics.asyncex.sudo.reset_coldkey_swap_extrinsic> "bittensor.core.extrinsics.asyncex.sudo.reset_coldkey_swap_extrinsic")(subtensor, wallet, ...[, ...]) | Resets the coldkey swap state for the given coldkey (root only).  
---|---  
[`sudo_set_admin_freeze_window_extrinsic`](<#bittensor.core.extrinsics.asyncex.sudo.sudo_set_admin_freeze_window_extrinsic> "bittensor.core.extrinsics.asyncex.sudo.sudo_set_admin_freeze_window_extrinsic")(subtensor, ...) | Sets the admin freeze window length (in blocks) at the end of a tempo.  
[`sudo_set_coldkey_swap_announcement_delay_extrinsic`](<#bittensor.core.extrinsics.asyncex.sudo.sudo_set_coldkey_swap_announcement_delay_extrinsic> "bittensor.core.extrinsics.asyncex.sudo.sudo_set_coldkey_swap_announcement_delay_extrinsic")(...) | Sets the announcement delay for coldkey swap.  
[`sudo_set_coldkey_swap_reannouncement_delay_extrinsic`](<#bittensor.core.extrinsics.asyncex.sudo.sudo_set_coldkey_swap_reannouncement_delay_extrinsic> "bittensor.core.extrinsics.asyncex.sudo.sudo_set_coldkey_swap_reannouncement_delay_extrinsic")(...) | Sets the reannouncement delay for coldkey swap.  
[`sudo_set_mechanism_count_extrinsic`](<#bittensor.core.extrinsics.asyncex.sudo.sudo_set_mechanism_count_extrinsic> "bittensor.core.extrinsics.asyncex.sudo.sudo_set_mechanism_count_extrinsic")(subtensor, wallet, ...) | Sets the number of subnet mechanisms.  
[`sudo_set_mechanism_emission_split_extrinsic`](<#bittensor.core.extrinsics.asyncex.sudo.sudo_set_mechanism_emission_split_extrinsic> "bittensor.core.extrinsics.asyncex.sudo.sudo_set_mechanism_emission_split_extrinsic")(subtensor, ...) | Sets the emission split between mechanisms in a provided subnet.  
[`swap_coldkey_extrinsic`](<#bittensor.core.extrinsics.asyncex.sudo.swap_coldkey_extrinsic> "bittensor.core.extrinsics.asyncex.sudo.swap_coldkey_extrinsic")(subtensor, wallet, ...[, ...]) | Performs a root-only coldkey swap without an announcement.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

async bittensor.core.extrinsics.asyncex.sudo.reset_coldkey_swap_extrinsic(_subtensor_ , _wallet_ , _coldkey_ss58_ , _*_ , _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_)[#](<#bittensor.core.extrinsics.asyncex.sudo.reset_coldkey_swap_extrinsic> "Link to this definition")
    

Resets the coldkey swap state for the given coldkey (root only).

Clears the coldkey swap announcement and dispute for the specified coldkey. Only callable by root.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – AsyncSubtensor instance.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (must be root/admin wallet).

  * **coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the coldkey to reset the swap for.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * This function can only be called by root.




async bittensor.core.extrinsics.asyncex.sudo.sudo_set_admin_freeze_window_extrinsic(_subtensor_ , _wallet_ , _window_ , _*_ , _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_)[#](<#bittensor.core.extrinsics.asyncex.sudo.sudo_set_admin_freeze_window_extrinsic> "Link to this definition")
    

Sets the admin freeze window length (in blocks) at the end of a tempo.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – AsyncSubtensor instance.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance.

  * **window** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The amount of blocks to freeze in the end of a tempo.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

async bittensor.core.extrinsics.asyncex.sudo.sudo_set_coldkey_swap_announcement_delay_extrinsic(_subtensor_ , _wallet_ , _duration_ , _*_ , _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_)[#](<#bittensor.core.extrinsics.asyncex.sudo.sudo_set_coldkey_swap_announcement_delay_extrinsic> "Link to this definition")
    

Sets the announcement delay for coldkey swap.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – AsyncSubtensor instance.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance.

  * **duration** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The announcement delay in blocks.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

async bittensor.core.extrinsics.asyncex.sudo.sudo_set_coldkey_swap_reannouncement_delay_extrinsic(_subtensor_ , _wallet_ , _duration_ , _*_ , _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_)[#](<#bittensor.core.extrinsics.asyncex.sudo.sudo_set_coldkey_swap_reannouncement_delay_extrinsic> "Link to this definition")
    

Sets the reannouncement delay for coldkey swap.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – AsyncSubtensor instance.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance.

  * **duration** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The reannouncement delay in blocks.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

async bittensor.core.extrinsics.asyncex.sudo.sudo_set_mechanism_count_extrinsic(_subtensor_ , _wallet_ , _netuid_ , _mech_count_ , _*_ , _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_)[#](<#bittensor.core.extrinsics.asyncex.sudo.sudo_set_mechanism_count_extrinsic> "Link to this definition")
    

Sets the number of subnet mechanisms.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Subtensor instance.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet unique identifier.

  * **mech_count** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The amount of subnet mechanism to be set.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

async bittensor.core.extrinsics.asyncex.sudo.sudo_set_mechanism_emission_split_extrinsic(_subtensor_ , _wallet_ , _netuid_ , _maybe_split_ , _*_ , _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_)[#](<#bittensor.core.extrinsics.asyncex.sudo.sudo_set_mechanism_emission_split_extrinsic> "Link to this definition")
    

Sets the emission split between mechanisms in a provided subnet.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – AsyncSubtensor instance.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet unique identifier.

  * **maybe_split** ([_bittensor.core.types.Weights_](<../../../types/index.html#bittensor.core.types.Weights> "bittensor.core.types.Weights")) – List of emission weights (positive integers) for each subnet mechanism.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Note

The maybe_split list defines the relative emission share for each subnet mechanism. Its length must match the number of active mechanisms in the subnet or be shorter, but not equal to zero. For example, [3, 1, 1] distributes emissions in a 3:1:1 ratio across subnet mechanisms 0, 1, and 2. Each mechanism’s emission share is calculated as: share[i] = maybe_split[i] / sum(maybe_split)

async bittensor.core.extrinsics.asyncex.sudo.swap_coldkey_extrinsic(_subtensor_ , _wallet_ , _old_coldkey_ss58_ , _new_coldkey_ss58_ , _swap_cost_ , _*_ , _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_)[#](<#bittensor.core.extrinsics.asyncex.sudo.swap_coldkey_extrinsic> "Link to this definition")
    

Performs a root-only coldkey swap without an announcement.

Only callable by root. Transfers all stake and associations from old_coldkey to new_coldkey; swap_cost (in RAO) is charged from old_coldkey. Use 0 for no charge.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – AsyncSubtensor instance.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object (must be root/admin wallet).

  * **old_coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the coldkey to swap from.

  * **new_coldkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – SS58 address of the coldkey to swap to.

  * **swap_cost** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Cost in RAO charged from old_coldkey (use 0 for no charge).

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * This function can only called by root.




[ __ previous bittensor.core.extrinsics.asyncex.start_call ](<../start_call/index.html> "previous page") [ next bittensor.core.extrinsics.asyncex.take __](<../take/index.html> "next page")

__Contents

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`reset_coldkey_swap_extrinsic()`](<#bittensor.core.extrinsics.asyncex.sudo.reset_coldkey_swap_extrinsic>)
    * [`sudo_set_admin_freeze_window_extrinsic()`](<#bittensor.core.extrinsics.asyncex.sudo.sudo_set_admin_freeze_window_extrinsic>)
    * [`sudo_set_coldkey_swap_announcement_delay_extrinsic()`](<#bittensor.core.extrinsics.asyncex.sudo.sudo_set_coldkey_swap_announcement_delay_extrinsic>)
    * [`sudo_set_coldkey_swap_reannouncement_delay_extrinsic()`](<#bittensor.core.extrinsics.asyncex.sudo.sudo_set_coldkey_swap_reannouncement_delay_extrinsic>)
    * [`sudo_set_mechanism_count_extrinsic()`](<#bittensor.core.extrinsics.asyncex.sudo.sudo_set_mechanism_count_extrinsic>)
    * [`sudo_set_mechanism_emission_split_extrinsic()`](<#bittensor.core.extrinsics.asyncex.sudo.sudo_set_mechanism_emission_split_extrinsic>)
    * [`swap_coldkey_extrinsic()`](<#bittensor.core.extrinsics.asyncex.sudo.swap_coldkey_extrinsic>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.   

  *[*]: Keyword-only parameters separator (PEP 3102)