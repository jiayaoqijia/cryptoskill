# bittensor.core.extrinsics.children &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/children/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/children/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/extrinsics/children/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.children

##  Contents 

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`root_set_pending_childkey_cooldown_extrinsic()`](<#bittensor.core.extrinsics.children.root_set_pending_childkey_cooldown_extrinsic>)
    * [`set_children_extrinsic()`](<#bittensor.core.extrinsics.children.set_children_extrinsic>)



# bittensor.core.extrinsics.children[#](<#module-bittensor.core.extrinsics.children> "Link to this heading")

## Functions[#](<#functions> "Link to this heading")

[`root_set_pending_childkey_cooldown_extrinsic`](<#bittensor.core.extrinsics.children.root_set_pending_childkey_cooldown_extrinsic> "bittensor.core.extrinsics.children.root_set_pending_childkey_cooldown_extrinsic")(...[, ...]) | Allows a root coldkey to set children-keys.  
---|---  
[`set_children_extrinsic`](<#bittensor.core.extrinsics.children.set_children_extrinsic> "bittensor.core.extrinsics.children.set_children_extrinsic")(subtensor, wallet, hotkey_ss58, ...) | Allows a coldkey to set children-keys.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

bittensor.core.extrinsics.children.root_set_pending_childkey_cooldown_extrinsic(_subtensor_ , _wallet_ , _cooldown_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.children.root_set_pending_childkey_cooldown_extrinsic> "Link to this definition")
    

Allows a root coldkey to set children-keys.

Parameters:
    

  * **subtensor** ([_bittensor.core.subtensor.Subtensor_](<../../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor")) – The Subtensor client instance used for blockchain interaction.

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet used to sign the extrinsic (must be unlocked).

  * **cooldown** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The cooldown period in blocks.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be finalized on the blockchain.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

bittensor.core.extrinsics.children.set_children_extrinsic(_subtensor_ , _wallet_ , _hotkey_ss58_ , _netuid_ , _children_ , _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.children.set_children_extrinsic> "Link to this definition")
    

Allows a coldkey to set children-keys.

Parameters:
    

  * **subtensor** ([_bittensor.core.subtensor.Subtensor_](<../../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor")) – The Subtensor client instance used for blockchain interaction.

  * **wallet** (_bittensor_wallet.Wallet_) – bittensor wallet instance.

  * **hotkey_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The `SS58` address of the neuron’s hotkey.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid value.

  * **children** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_tuple_](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)") _[_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _,_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]__]_) – A list of children with their proportions.

  * **mev_protection** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, encrypts and submits the transaction through the MEV Shield pallet to protect against front-running and MEV attacks. The transaction remains encrypted in the mempool until validators decrypt and execute it. If False, submits the transaction directly without encryption.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be included in a block.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Waits for the transaction to be finalized on the blockchain.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the revealed execution of transaction if mev_protection used.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Raises:
    

  * [**DuplicateChild**](<../../errors/index.html#bittensor.core.errors.DuplicateChild> "bittensor.core.errors.DuplicateChild") – There are duplicates in the list of children.

  * [**InvalidChild**](<../../errors/index.html#bittensor.core.errors.InvalidChild> "bittensor.core.errors.InvalidChild") – Child is the hotkey.

  * [**NonAssociatedColdKey**](<../../errors/index.html#bittensor.core.errors.NonAssociatedColdKey> "bittensor.core.errors.NonAssociatedColdKey") – The coldkey does not own the hotkey or the child is the same as the hotkey.

  * [**NotEnoughStakeToSetChildkeys**](<../../errors/index.html#bittensor.core.errors.NotEnoughStakeToSetChildkeys> "bittensor.core.errors.NotEnoughStakeToSetChildkeys") – Parent key doesn’t have minimum own stake.

  * [**ProportionOverflow**](<../../errors/index.html#bittensor.core.errors.ProportionOverflow> "bittensor.core.errors.ProportionOverflow") – The sum of the proportions does exceed uint64.

  * [**RegistrationNotPermittedOnRootSubnet**](<../../errors/index.html#bittensor.core.errors.RegistrationNotPermittedOnRootSubnet> "bittensor.core.errors.RegistrationNotPermittedOnRootSubnet") – Attempting to register a child on the root network.

  * [**SubnetNotExists**](<../../errors/index.html#bittensor.core.errors.SubnetNotExists> "bittensor.core.errors.SubnetNotExists") – Attempting to register to a non-existent network.

  * [**TooManyChildren**](<../../errors/index.html#bittensor.core.errors.TooManyChildren> "bittensor.core.errors.TooManyChildren") – Too many children in request.

  * [**TxRateLimitExceeded**](<../../errors/index.html#bittensor.core.errors.TxRateLimitExceeded> "bittensor.core.errors.TxRateLimitExceeded") – Hotkey hit the rate limit.

  * **bittensor_wallet.errors.KeyFileError** – Failed to decode keyfile data.

  * **bittensor_wallet.errors.PasswordError** – Decryption failed or wrong password for decryption provided.




[ __ previous bittensor.core.extrinsics.asyncex.weights ](<../asyncex/weights/index.html> "previous page") [ next bittensor.core.extrinsics.coldkey_swap __](<../coldkey_swap/index.html> "next page")

__Contents

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`root_set_pending_childkey_cooldown_extrinsic()`](<#bittensor.core.extrinsics.children.root_set_pending_childkey_cooldown_extrinsic>)
    * [`set_children_extrinsic()`](<#bittensor.core.extrinsics.children.set_children_extrinsic>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.   

  *[*]: Keyword-only parameters separator (PEP 3102)