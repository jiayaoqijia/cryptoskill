# bittensor.core.extrinsics.asyncex.utils &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/asyncex/utils/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/asyncex/utils/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../../_sources/autoapi/bittensor/core/extrinsics/asyncex/utils/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.asyncex.utils

##  Contents 

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`sudo_call_extrinsic()`](<#bittensor.core.extrinsics.asyncex.utils.sudo_call_extrinsic>)



# bittensor.core.extrinsics.asyncex.utils[#](<#module-bittensor.core.extrinsics.asyncex.utils> "Link to this heading")

## Functions[#](<#functions> "Link to this heading")

[`sudo_call_extrinsic`](<#bittensor.core.extrinsics.asyncex.utils.sudo_call_extrinsic> "bittensor.core.extrinsics.asyncex.utils.sudo_call_extrinsic")(subtensor, wallet, call_function, ...) | Execute a sudo call extrinsic.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

async bittensor.core.extrinsics.asyncex.utils.sudo_call_extrinsic(_subtensor_ , _wallet_ , _call_function_ , _call_params_ , _call_module ='AdminUtils'_, _sign_with ='coldkey'_, _use_nonce =False_, _nonce_key ='hotkey'_, _*_ , _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _root_call =False_)[#](<#bittensor.core.extrinsics.asyncex.utils.sudo_call_extrinsic> "Link to this definition")
    

Execute a sudo call extrinsic.

Parameters:
    

  * **subtensor** ([_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")) – AsyncSubtensor instance.

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet instance.

  * **call_function** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The call function to execute.

  * **call_params** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")) – The call parameters.

  * **call_module** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The call module.

  * **sign_with** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The keypair to sign the extrinsic with.

  * **use_nonce** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to use a nonce.

  * **nonce_key** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The key to use for the nonce.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **root_call** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – False, if the subnet owner makes a call.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

[ __ previous bittensor.core.extrinsics.asyncex.unstaking ](<../unstaking/index.html> "previous page") [ next bittensor.core.extrinsics.asyncex.weights __](<../weights/index.html> "next page")

__Contents

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`sudo_call_extrinsic()`](<#bittensor.core.extrinsics.asyncex.utils.sudo_call_extrinsic>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.   

  *[*]: Keyword-only parameters separator (PEP 3102)