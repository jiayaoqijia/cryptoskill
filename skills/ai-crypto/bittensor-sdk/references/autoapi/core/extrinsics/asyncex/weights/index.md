# bittensor.core.extrinsics.asyncex.weights &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/asyncex/weights/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/asyncex/weights/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../../_sources/autoapi/bittensor/core/extrinsics/asyncex/weights/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.asyncex.weights

##  Contents 

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`commit_timelocked_weights_extrinsic()`](<#bittensor.core.extrinsics.asyncex.weights.commit_timelocked_weights_extrinsic>)
    * [`commit_weights_extrinsic()`](<#bittensor.core.extrinsics.asyncex.weights.commit_weights_extrinsic>)
    * [`reveal_weights_extrinsic()`](<#bittensor.core.extrinsics.asyncex.weights.reveal_weights_extrinsic>)
    * [`set_weights_extrinsic()`](<#bittensor.core.extrinsics.asyncex.weights.set_weights_extrinsic>)



# bittensor.core.extrinsics.asyncex.weights[#](<#module-bittensor.core.extrinsics.asyncex.weights> "Link to this heading")

Module provides async commit and reveal weights extrinsic.

## Functions[#](<#functions> "Link to this heading")

[`commit_timelocked_weights_extrinsic`](<#bittensor.core.extrinsics.asyncex.weights.commit_timelocked_weights_extrinsic> "bittensor.core.extrinsics.asyncex.weights.commit_timelocked_weights_extrinsic")(subtensor, wallet, ...) | Commits the weights for a specific sub subnet mechanism on the Bittensor blockchain using the provided wallet.  
---|---  
[`commit_weights_extrinsic`](<#bittensor.core.extrinsics.asyncex.weights.commit_weights_extrinsic> "bittensor.core.extrinsics.asyncex.weights.commit_weights_extrinsic")(subtensor, wallet, netuid, ...) | Commits the weights for a specific sub subnet on the Bittensor blockchain using the provided wallet.  
[`reveal_weights_extrinsic`](<#bittensor.core.extrinsics.asyncex.weights.reveal_weights_extrinsic> "bittensor.core.extrinsics.asyncex.weights.reveal_weights_extrinsic")(subtensor, wallet, netuid, ...) | Reveals the weights for a specific sub subnet on the Bittensor blockchain using the provided wallet.  
[`set_weights_extrinsic`](<#bittensor.core.extrinsics.asyncex.weights.set_weights_extrinsic> "bittensor.core.extrinsics.asyncex.weights.set_weights_extrinsic")(subtensor, wallet, netuid, ...) | Sets the passed weights in the chain for hotkeys in the sub-subnet of the passed subnet.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

async bittensor.core.extrinsics.asyncex.weights.commit_timelocked_weights_extrinsic(_subtensor_ , _wallet_ , _netuid_ , _mechid_ , _uids_ , _weights_ , _block_time_ , _commit_reveal_version =4_, _version_key =version_as_int_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.weights.commit_timelocked_weights_extrinsic> "Link to this definition")
    

Commits the weights for a specific sub subnet mechanism on the Bittensor blockchain using the provided wallet.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – AsyncSubtensor instance.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet unique identifier.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet mechanism unique identifier

  * **uids** ([_bittensor.core.types.UIDs_](<../../../types/index.html#bittensor.core.types.UIDs> "bittensor.core.types.UIDs")) – The list of neuron UIDs that the weights are being set for.

  * **weights** ([_bittensor.core.types.Weights_](<../../../types/index.html#bittensor.core.types.Weights> "bittensor.core.types.Weights")) – The corresponding weights to be set for each UID.

  * **block_time** (_Union_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _,_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _]_) – The number of seconds for block duration.

  * **commit_reveal_version** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The version of the commit-reveal in the chain.

  * **version_key** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Version key for compatibility with the network.

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

async bittensor.core.extrinsics.asyncex.weights.commit_weights_extrinsic(_subtensor_ , _wallet_ , _netuid_ , _mechid_ , _uids_ , _weights_ , _salt_ , _version_key =version_as_int_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.weights.commit_weights_extrinsic> "Link to this definition")
    

Commits the weights for a specific sub subnet on the Bittensor blockchain using the provided wallet.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – AsyncSubtensor instance.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet unique identifier.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet mechanism unique identifier.

  * **uids** ([_bittensor.core.types.UIDs_](<../../../types/index.html#bittensor.core.types.UIDs> "bittensor.core.types.UIDs")) – NumPy array of neuron UIDs for which weights are being committed.

  * **weights** ([_bittensor.core.types.Weights_](<../../../types/index.html#bittensor.core.types.Weights> "bittensor.core.types.Weights")) – NumPy array of weight values corresponding to each UID.

  * **salt** ([_bittensor.core.types.Salt_](<../../../types/index.html#bittensor.core.types.Salt> "bittensor.core.types.Salt")) – list of randomly generated integers as salt to generated weighted hash.

  * **version_key** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Version key for compatibility with the network.

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

async bittensor.core.extrinsics.asyncex.weights.reveal_weights_extrinsic(_subtensor_ , _wallet_ , _netuid_ , _mechid_ , _uids_ , _weights_ , _salt_ , _version_key_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.weights.reveal_weights_extrinsic> "Link to this definition")
    

Reveals the weights for a specific sub subnet on the Bittensor blockchain using the provided wallet.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – AsyncSubtensor instance.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet mechanism unique identifier.

  * **uids** ([_bittensor.core.types.UIDs_](<../../../types/index.html#bittensor.core.types.UIDs> "bittensor.core.types.UIDs")) – List of neuron UIDs for which weights are being revealed.

  * **weights** ([_bittensor.core.types.Weights_](<../../../types/index.html#bittensor.core.types.Weights> "bittensor.core.types.Weights")) – List of weight values corresponding to each UID.

  * **salt** ([_bittensor.core.types.Salt_](<../../../types/index.html#bittensor.core.types.Salt> "bittensor.core.types.Salt")) – List of salt values corresponding to the hash function.

  * **version_key** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Version key for compatibility with the network.

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

async bittensor.core.extrinsics.asyncex.weights.set_weights_extrinsic(_subtensor_ , _wallet_ , _netuid_ , _mechid_ , _uids_ , _weights_ , _version_key_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.weights.set_weights_extrinsic> "Link to this definition")
    

Sets the passed weights in the chain for hotkeys in the sub-subnet of the passed subnet.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – AsyncSubtensor instance.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet mechanism unique identifier.

  * **uids** ([_bittensor.core.types.UIDs_](<../../../types/index.html#bittensor.core.types.UIDs> "bittensor.core.types.UIDs")) – List of neuron UIDs for which weights are being revealed.

  * **weights** ([_bittensor.core.types.Weights_](<../../../types/index.html#bittensor.core.types.Weights> "bittensor.core.types.Weights")) – List of weight values corresponding to each UID.

  * **version_key** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Version key for compatibility with the network.

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

[ __ previous bittensor.core.extrinsics.asyncex.utils ](<../utils/index.html> "previous page") [ next bittensor.core.extrinsics.children __](<../../children/index.html> "next page")

__Contents

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`commit_timelocked_weights_extrinsic()`](<#bittensor.core.extrinsics.asyncex.weights.commit_timelocked_weights_extrinsic>)
    * [`commit_weights_extrinsic()`](<#bittensor.core.extrinsics.asyncex.weights.commit_weights_extrinsic>)
    * [`reveal_weights_extrinsic()`](<#bittensor.core.extrinsics.asyncex.weights.reveal_weights_extrinsic>)
    * [`set_weights_extrinsic()`](<#bittensor.core.extrinsics.asyncex.weights.set_weights_extrinsic>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.   

  *[*]: Keyword-only parameters separator (PEP 3102)