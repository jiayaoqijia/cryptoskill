# bittensor.core.extrinsics.asyncex.mev_shield &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/asyncex/mev_shield/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/asyncex/mev_shield/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../../_sources/autoapi/bittensor/core/extrinsics/asyncex/mev_shield/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.asyncex.mev_shield

##  Contents 

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`submit_encrypted_extrinsic()`](<#bittensor.core.extrinsics.asyncex.mev_shield.submit_encrypted_extrinsic>)
    * [`wait_for_extrinsic_by_hash()`](<#bittensor.core.extrinsics.asyncex.mev_shield.wait_for_extrinsic_by_hash>)



# bittensor.core.extrinsics.asyncex.mev_shield[#](<#module-bittensor.core.extrinsics.asyncex.mev_shield> "Link to this heading")

Module provides async MEV Shield extrinsics.

## Functions[#](<#functions> "Link to this heading")

[`submit_encrypted_extrinsic`](<#bittensor.core.extrinsics.asyncex.mev_shield.submit_encrypted_extrinsic> "bittensor.core.extrinsics.asyncex.mev_shield.submit_encrypted_extrinsic")(subtensor, wallet, call[, ...]) | Submits an encrypted extrinsic to the MEV Shield pallet.  
---|---  
[`wait_for_extrinsic_by_hash`](<#bittensor.core.extrinsics.asyncex.mev_shield.wait_for_extrinsic_by_hash> "bittensor.core.extrinsics.asyncex.mev_shield.wait_for_extrinsic_by_hash")(subtensor, extrinsic_hash, ...) | Wait for the result of a MeV Shield encrypted extrinsic.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

async bittensor.core.extrinsics.asyncex.mev_shield.submit_encrypted_extrinsic(_subtensor_ , _wallet_ , _call_ , _sign_with ='coldkey'_, _*_ , _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =False_, _wait_for_revealed_execution =True_, _blocks_for_revealed_execution =3_)[#](<#bittensor.core.extrinsics.asyncex.mev_shield.submit_encrypted_extrinsic> "Link to this definition")
    

Submits an encrypted extrinsic to the MEV Shield pallet.

This function encrypts a call using ML-KEM-768 + XChaCha20Poly1305 and submits it to the MevShield pallet. The extrinsic remains encrypted in the transaction pool until it is included in a block and decrypted by validators.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – The Subtensor client instance used for blockchain interaction.

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet used to sign the extrinsic (must be unlocked, coldkey will be used for signing).

  * **call** (_scalecodec.types.GenericCall_) – The GenericCall object to encrypt and submit.

  * **sign_with** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The keypair to use for signing the inner call/extrinsic. Can be either “coldkey” or “hotkey”.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **wait_for_revealed_execution** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the executed event, indicating that validators have successfully decrypted and executed the inner call. If True, the function will poll subsequent blocks for the extrinsic matching this submission.

  * **blocks_for_revealed_execution** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Maximum number of blocks to poll for the executed event after inclusion. The function checks blocks from start_block to start_block + blocks_for_revealed_execution. Returns immediately if the event is found before the block limit is reached.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Raises:
    

  * [**ValueError**](<https://docs.python.org/3/library/exceptions.html#ValueError> "\(in Python v3.14\)") – If NextKey is not available in storage or encryption fails.

  * **SubstrateRequestException** – If the extrinsic fails to be submitted or included.




Note

The encryption uses the public key from NextKey storage, which rotates every block. The ciphertext wire format is: [key_hash(16)][u16 kem_len LE][kem_ct][nonce24][aead_ct], where key_hash = twox_128(NextKey).

async bittensor.core.extrinsics.asyncex.mev_shield.wait_for_extrinsic_by_hash(_subtensor_ , _extrinsic_hash_ , _submit_block_hash_ , _timeout_blocks =3_)[#](<#bittensor.core.extrinsics.asyncex.mev_shield.wait_for_extrinsic_by_hash> "Link to this definition")
    

Wait for the result of a MeV Shield encrypted extrinsic.

After submit_encrypted succeeds, the block author will decrypt and submit the inner extrinsic directly. This function polls subsequent blocks looking for an extrinsic matching the provided hash.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – SubtensorInterface instance.

  * **extrinsic_hash** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hash of the inner extrinsic to find.

  * **submit_block_hash** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – Block hash where submit_encrypted was included.

  * **timeout_blocks** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Max blocks to wait.



Returns:
    

Optional ExtrinsicReceipt.

Return type:
    

Optional[async_substrate_interface.AsyncExtrinsicReceipt]

[ __ previous bittensor.core.extrinsics.asyncex.liquidity ](<../liquidity/index.html> "previous page") [ next bittensor.core.extrinsics.asyncex.move_stake __](<../move_stake/index.html> "next page")

__Contents

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`submit_encrypted_extrinsic()`](<#bittensor.core.extrinsics.asyncex.mev_shield.submit_encrypted_extrinsic>)
    * [`wait_for_extrinsic_by_hash()`](<#bittensor.core.extrinsics.asyncex.mev_shield.wait_for_extrinsic_by_hash>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.   

  *[*]: Keyword-only parameters separator (PEP 3102)