# bittensor.core.extrinsics.asyncex.serving &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/asyncex/serving/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/asyncex/serving/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../../_sources/autoapi/bittensor/core/extrinsics/asyncex/serving/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.asyncex.serving

##  Contents 

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`publish_metadata_extrinsic()`](<#bittensor.core.extrinsics.asyncex.serving.publish_metadata_extrinsic>)
    * [`serve_axon_extrinsic()`](<#bittensor.core.extrinsics.asyncex.serving.serve_axon_extrinsic>)
    * [`serve_extrinsic()`](<#bittensor.core.extrinsics.asyncex.serving.serve_extrinsic>)



# bittensor.core.extrinsics.asyncex.serving[#](<#module-bittensor.core.extrinsics.asyncex.serving> "Link to this heading")

## Functions[#](<#functions> "Link to this heading")

[`publish_metadata_extrinsic`](<#bittensor.core.extrinsics.asyncex.serving.publish_metadata_extrinsic> "bittensor.core.extrinsics.asyncex.serving.publish_metadata_extrinsic")(subtensor, wallet, netuid, ...) | Publishes metadata on the Bittensor network using the specified wallet and network identifier.  
---|---  
[`serve_axon_extrinsic`](<#bittensor.core.extrinsics.asyncex.serving.serve_axon_extrinsic> "bittensor.core.extrinsics.asyncex.serving.serve_axon_extrinsic")(subtensor, netuid, axon[, ...]) | Serves the axon to the network.  
[`serve_extrinsic`](<#bittensor.core.extrinsics.asyncex.serving.serve_extrinsic> "bittensor.core.extrinsics.asyncex.serving.serve_extrinsic")(subtensor, wallet, ip, port, protocol, ...) | Subscribes a Bittensor endpoint to the subtensor chain.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

async bittensor.core.extrinsics.asyncex.serving.publish_metadata_extrinsic(_subtensor_ , _wallet_ , _netuid_ , _data_type_ , _data_ , _reset_bonds =False_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.serving.publish_metadata_extrinsic> "Link to this definition")
    

Publishes metadata on the Bittensor network using the specified wallet and network identifier.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – The subtensor instance representing the Bittensor blockchain connection.

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet object used for authentication in the transaction.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Network UID on which the metadata is to be published.

  * **data_type** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The data type of the information being submitted. It should be one of the following: `'Sha256'`, `'Blake256'`, `'Keccak256'`, or `'Raw0-128'`. This specifies the format or hashing algorithm used for the data.

  * **data** (_Union_ _[_[_bytes_](<../../../../extras/dev_framework/calls/non_sudo_calls/index.html#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes> "bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes") _,_[_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)") _]_) – The actual metadata content to be published. This should be formatted or hashed according to the `type` specified. (Note: max `str` length is 128 bytes for `'Raw0-128'`.)

  * **reset_bonds** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, the function will reset the bonds for the neuron.

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

Raises:
    

  * [**MetadataError**](<../../../errors/index.html#bittensor.core.errors.MetadataError> "bittensor.core.errors.MetadataError") – If there is an error in submitting the extrinsic, or if the response from the blockchain indicates

  * **failure.** – 




async bittensor.core.extrinsics.asyncex.serving.serve_axon_extrinsic(_subtensor_ , _netuid_ , _axon_ , _certificate =None_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.serving.serve_axon_extrinsic> "Link to this definition")
    

Serves the axon to the network.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – AsyncSubtensor instance object.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The `netuid` being served on.

  * **axon** ([_bittensor.core.axon.Axon_](<../../../axon/index.html#bittensor.core.axon.Axon> "bittensor.core.axon.Axon")) – Axon to serve.

  * **certificate** (_Optional_ _[_[_bittensor.utils.Certificate_](<../../../../utils/index.html#bittensor.utils.Certificate> "bittensor.utils.Certificate") _]_) – Certificate to use for TLS. If `None`, no TLS will be used.

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

async bittensor.core.extrinsics.asyncex.serving.serve_extrinsic(_subtensor_ , _wallet_ , _ip_ , _port_ , _protocol_ , _netuid_ , _placeholder1 =0_, _placeholder2 =0_, _certificate =None_, _*_ , _mev_protection =DEFAULT_MEV_PROTECTION_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _wait_for_revealed_execution =True_)[#](<#bittensor.core.extrinsics.asyncex.serving.serve_extrinsic> "Link to this definition")
    

Subscribes a Bittensor endpoint to the subtensor chain.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – Subtensor instance object.

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor wallet object.

  * **ip** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – Endpoint host port i.e., `192.122.31.4`.

  * **port** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Endpoint port number i.e., `9221`.

  * **protocol** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – An `int` representation of the protocol.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network uid to serve on.

  * **placeholder1** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – A placeholder for future use.

  * **placeholder2** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – A placeholder for future use.

  * **certificate** (_Optional_ _[_[_bittensor.utils.Certificate_](<../../../../utils/index.html#bittensor.utils.Certificate> "bittensor.utils.Certificate") _]_) – Certificate to use for TLS. If `None`, no TLS will be used.

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

[ __ previous bittensor.core.extrinsics.asyncex.root ](<../root/index.html> "previous page") [ next bittensor.core.extrinsics.asyncex.staking __](<../staking/index.html> "next page")

__Contents

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`publish_metadata_extrinsic()`](<#bittensor.core.extrinsics.asyncex.serving.publish_metadata_extrinsic>)
    * [`serve_axon_extrinsic()`](<#bittensor.core.extrinsics.asyncex.serving.serve_axon_extrinsic>)
    * [`serve_extrinsic()`](<#bittensor.core.extrinsics.asyncex.serving.serve_extrinsic>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.   

  *[*]: Keyword-only parameters separator (PEP 3102)