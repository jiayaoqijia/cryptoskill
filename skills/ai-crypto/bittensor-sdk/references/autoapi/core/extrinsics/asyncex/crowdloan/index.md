# bittensor.core.extrinsics.asyncex.crowdloan &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/asyncex/crowdloan/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/asyncex/crowdloan/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../../_sources/autoapi/bittensor/core/extrinsics/asyncex/crowdloan/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.asyncex.crowdloan

##  Contents 

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`contribute_crowdloan_extrinsic()`](<#bittensor.core.extrinsics.asyncex.crowdloan.contribute_crowdloan_extrinsic>)
    * [`create_crowdloan_extrinsic()`](<#bittensor.core.extrinsics.asyncex.crowdloan.create_crowdloan_extrinsic>)
    * [`dissolve_crowdloan_extrinsic()`](<#bittensor.core.extrinsics.asyncex.crowdloan.dissolve_crowdloan_extrinsic>)
    * [`finalize_crowdloan_extrinsic()`](<#bittensor.core.extrinsics.asyncex.crowdloan.finalize_crowdloan_extrinsic>)
    * [`refund_crowdloan_extrinsic()`](<#bittensor.core.extrinsics.asyncex.crowdloan.refund_crowdloan_extrinsic>)
    * [`update_cap_crowdloan_extrinsic()`](<#bittensor.core.extrinsics.asyncex.crowdloan.update_cap_crowdloan_extrinsic>)
    * [`update_end_crowdloan_extrinsic()`](<#bittensor.core.extrinsics.asyncex.crowdloan.update_end_crowdloan_extrinsic>)
    * [`update_min_contribution_crowdloan_extrinsic()`](<#bittensor.core.extrinsics.asyncex.crowdloan.update_min_contribution_crowdloan_extrinsic>)
    * [`withdraw_crowdloan_extrinsic()`](<#bittensor.core.extrinsics.asyncex.crowdloan.withdraw_crowdloan_extrinsic>)



# bittensor.core.extrinsics.asyncex.crowdloan[#](<#module-bittensor.core.extrinsics.asyncex.crowdloan> "Link to this heading")

## Functions[#](<#functions> "Link to this heading")

[`contribute_crowdloan_extrinsic`](<#bittensor.core.extrinsics.asyncex.crowdloan.contribute_crowdloan_extrinsic> "bittensor.core.extrinsics.asyncex.crowdloan.contribute_crowdloan_extrinsic")(subtensor, wallet, ...) | Contributes funds to an active crowdloan campaign.  
---|---  
[`create_crowdloan_extrinsic`](<#bittensor.core.extrinsics.asyncex.crowdloan.create_crowdloan_extrinsic> "bittensor.core.extrinsics.asyncex.crowdloan.create_crowdloan_extrinsic")(subtensor, wallet, deposit, ...) | Creates a new crowdloan campaign on-chain.  
[`dissolve_crowdloan_extrinsic`](<#bittensor.core.extrinsics.asyncex.crowdloan.dissolve_crowdloan_extrinsic> "bittensor.core.extrinsics.asyncex.crowdloan.dissolve_crowdloan_extrinsic")(subtensor, wallet, ...[, ...]) | Dissolves a completed or failed crowdloan campaign after all refunds are processed.  
[`finalize_crowdloan_extrinsic`](<#bittensor.core.extrinsics.asyncex.crowdloan.finalize_crowdloan_extrinsic> "bittensor.core.extrinsics.asyncex.crowdloan.finalize_crowdloan_extrinsic")(subtensor, wallet, ...[, ...]) | Finalizes a successful crowdloan campaign once the cap has been reached and the end block has passed.  
[`refund_crowdloan_extrinsic`](<#bittensor.core.extrinsics.asyncex.crowdloan.refund_crowdloan_extrinsic> "bittensor.core.extrinsics.asyncex.crowdloan.refund_crowdloan_extrinsic")(subtensor, wallet, ...[, ...]) | Refunds contributors from a failed or expired crowdloan campaign.  
[`update_cap_crowdloan_extrinsic`](<#bittensor.core.extrinsics.asyncex.crowdloan.update_cap_crowdloan_extrinsic> "bittensor.core.extrinsics.asyncex.crowdloan.update_cap_crowdloan_extrinsic")(subtensor, wallet, ...) | Updates the fundraising cap (maximum total contribution) of a non-finalized crowdloan.  
[`update_end_crowdloan_extrinsic`](<#bittensor.core.extrinsics.asyncex.crowdloan.update_end_crowdloan_extrinsic> "bittensor.core.extrinsics.asyncex.crowdloan.update_end_crowdloan_extrinsic")(subtensor, wallet, ...) | Updates the end block of a non-finalized crowdloan campaign.  
[`update_min_contribution_crowdloan_extrinsic`](<#bittensor.core.extrinsics.asyncex.crowdloan.update_min_contribution_crowdloan_extrinsic> "bittensor.core.extrinsics.asyncex.crowdloan.update_min_contribution_crowdloan_extrinsic")(subtensor, ...) | Updates the minimum contribution amount of a non-finalized crowdloan.  
[`withdraw_crowdloan_extrinsic`](<#bittensor.core.extrinsics.asyncex.crowdloan.withdraw_crowdloan_extrinsic> "bittensor.core.extrinsics.asyncex.crowdloan.withdraw_crowdloan_extrinsic")(subtensor, wallet, ...[, ...]) | Withdraws a contribution from an active (not yet finalized or dissolved) crowdloan.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

async bittensor.core.extrinsics.asyncex.crowdloan.contribute_crowdloan_extrinsic(_subtensor_ , _wallet_ , _crowdloan_id_ , _amount_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.crowdloan.contribute_crowdloan_extrinsic> "Link to this definition")
    

Contributes funds to an active crowdloan campaign.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Active Subtensor connection.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance used to sign the transaction.

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to contribute to.

  * **amount** ([_bittensor.utils.balance.Balance_](<../../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – Amount to contribute.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

async bittensor.core.extrinsics.asyncex.crowdloan.create_crowdloan_extrinsic(_subtensor_ , _wallet_ , _deposit_ , _min_contribution_ , _cap_ , _end_ , _call =None_, _target_address =None_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.crowdloan.create_crowdloan_extrinsic> "Link to this definition")
    

Creates a new crowdloan campaign on-chain.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Active Subtensor connection.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance used to sign the transaction.

  * **deposit** ([_bittensor.utils.balance.Balance_](<../../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – Initial deposit in RAO from the creator.

  * **min_contribution** ([_bittensor.utils.balance.Balance_](<../../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – Minimum contribution amount.

  * **cap** ([_bittensor.utils.balance.Balance_](<../../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – Maximum cap to be raised.

  * **end** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Block number when the campaign ends.

  * **call** (_Optional_ _[__scalecodec.types.GenericCall_ _]_) – Runtime call data (e.g., subtensor::register_leased_network).

  * **target_address** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – SS58 address to transfer funds to on success.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

async bittensor.core.extrinsics.asyncex.crowdloan.dissolve_crowdloan_extrinsic(_subtensor_ , _wallet_ , _crowdloan_id_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.crowdloan.dissolve_crowdloan_extrinsic> "Link to this definition")
    

Dissolves a completed or failed crowdloan campaign after all refunds are processed.

This permanently removes the campaign from on-chain storage and refunds the creator’s remaining deposit, if applicable. Can only be called by the campaign creator.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Active Subtensor connection.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance used to sign the transaction.

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to dissolve.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Only the creator can dissolve their own crowdloan.

  * All contributors (except the creator) must have been refunded first.

  * The creator’s remaining contribution (deposit) is returned during dissolution.

  * After this call, the crowdloan is removed from chain storage.




async bittensor.core.extrinsics.asyncex.crowdloan.finalize_crowdloan_extrinsic(_subtensor_ , _wallet_ , _crowdloan_id_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.crowdloan.finalize_crowdloan_extrinsic> "Link to this definition")
    

Finalizes a successful crowdloan campaign once the cap has been reached and the end block has passed.

This executes the stored call or transfers the raised funds to the target address, completing the campaign.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Active Subtensor connection.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance used to sign the transaction.

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to finalize.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

async bittensor.core.extrinsics.asyncex.crowdloan.refund_crowdloan_extrinsic(_subtensor_ , _wallet_ , _crowdloan_id_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.crowdloan.refund_crowdloan_extrinsic> "Link to this definition")
    

Refunds contributors from a failed or expired crowdloan campaign.

This call attempts to refund up to the limit defined by RefundContributorsLimit in a single dispatch. If there are more contributors than the limit, the call may need to be executed multiple times until all refunds are processed.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Active Subtensor connection.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance used to sign the transaction.

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to refund.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Can be called by only creator signed account.

  * Refunds contributors (excluding the creator) whose funds were locked in a failed campaign.

  * Each call processes a limited number of refunds (RefundContributorsLimit).

  * If the campaign has too many contributors, multiple refund calls are required.




async bittensor.core.extrinsics.asyncex.crowdloan.update_cap_crowdloan_extrinsic(_subtensor_ , _wallet_ , _crowdloan_id_ , _new_cap_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.crowdloan.update_cap_crowdloan_extrinsic> "Link to this definition")
    

Updates the fundraising cap (maximum total contribution) of a non-finalized crowdloan.

Only the creator of the crowdloan can perform this action, and the new cap must be greater than or equal to the current amount already raised.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Active Subtensor connection.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance used to sign the transaction.

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to update.

  * **new_cap** ([_bittensor.utils.balance.Balance_](<../../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – The new fundraising cap (in TAO or Balance).

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Only the creator can update the cap.

  * The crowdloan must not be finalized.

  * The new cap must be greater than or equal to the total funds already raised.




async bittensor.core.extrinsics.asyncex.crowdloan.update_end_crowdloan_extrinsic(_subtensor_ , _wallet_ , _crowdloan_id_ , _new_end_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.crowdloan.update_end_crowdloan_extrinsic> "Link to this definition")
    

Updates the end block of a non-finalized crowdloan campaign.

Only the creator of the crowdloan can perform this action. The new end block must be valid — meaning it cannot be in the past and must respect the minimum and maximum duration limits enforced by the chain.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Active Subtensor connection.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance used to sign the transaction.

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to update.

  * **new_end** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The new block number at which the crowdloan will end.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Only the creator can call this extrinsic.

  * The crowdloan must not be finalized.

  * The new end block must be later than the current block and within valid duration bounds (between
    

MinimumBlockDuration and MaximumBlockDuration).




async bittensor.core.extrinsics.asyncex.crowdloan.update_min_contribution_crowdloan_extrinsic(_subtensor_ , _wallet_ , _crowdloan_id_ , _new_min_contribution_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.crowdloan.update_min_contribution_crowdloan_extrinsic> "Link to this definition")
    

Updates the minimum contribution amount of a non-finalized crowdloan.

Only the creator of the crowdloan can perform this action, and the new value must be greater than or equal to the absolute minimum contribution defined in the chain configuration.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Active Subtensor connection.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance used to sign the transaction.

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to update.

  * **new_min_contribution** ([_bittensor.utils.balance.Balance_](<../../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – The new minimum contribution amount (in TAO or Balance).

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Notes

  * Can only be called by the creator of the crowdloan.

  * The crowdloan must not be finalized.

  * The new minimum contribution must not fall below the absolute minimum defined in the runtime.




async bittensor.core.extrinsics.asyncex.crowdloan.withdraw_crowdloan_extrinsic(_subtensor_ , _wallet_ , _crowdloan_id_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.crowdloan.withdraw_crowdloan_extrinsic> "Link to this definition")
    

Withdraws a contribution from an active (not yet finalized or dissolved) crowdloan.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Active Subtensor connection.

  * **wallet** (_bittensor_wallet.Wallet_) – Wallet instance used to sign the transaction (must be unlocked).

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to withdraw from.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the extrinsic to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for finalization of the extrinsic.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Note

  * Regular contributors can fully withdraw their contribution before finalization.

  * The creator cannot withdraw the initial deposit, but may withdraw any amount exceeding his deposit.




[ __ previous bittensor.core.extrinsics.asyncex.coldkey_swap ](<../coldkey_swap/index.html> "previous page") [ next bittensor.core.extrinsics.asyncex.liquidity __](<../liquidity/index.html> "next page")

__Contents

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`contribute_crowdloan_extrinsic()`](<#bittensor.core.extrinsics.asyncex.crowdloan.contribute_crowdloan_extrinsic>)
    * [`create_crowdloan_extrinsic()`](<#bittensor.core.extrinsics.asyncex.crowdloan.create_crowdloan_extrinsic>)
    * [`dissolve_crowdloan_extrinsic()`](<#bittensor.core.extrinsics.asyncex.crowdloan.dissolve_crowdloan_extrinsic>)
    * [`finalize_crowdloan_extrinsic()`](<#bittensor.core.extrinsics.asyncex.crowdloan.finalize_crowdloan_extrinsic>)
    * [`refund_crowdloan_extrinsic()`](<#bittensor.core.extrinsics.asyncex.crowdloan.refund_crowdloan_extrinsic>)
    * [`update_cap_crowdloan_extrinsic()`](<#bittensor.core.extrinsics.asyncex.crowdloan.update_cap_crowdloan_extrinsic>)
    * [`update_end_crowdloan_extrinsic()`](<#bittensor.core.extrinsics.asyncex.crowdloan.update_end_crowdloan_extrinsic>)
    * [`update_min_contribution_crowdloan_extrinsic()`](<#bittensor.core.extrinsics.asyncex.crowdloan.update_min_contribution_crowdloan_extrinsic>)
    * [`withdraw_crowdloan_extrinsic()`](<#bittensor.core.extrinsics.asyncex.crowdloan.withdraw_crowdloan_extrinsic>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.   

  *[*]: Keyword-only parameters separator (PEP 3102)