# bittensor.core.extrinsics.pallets.balances &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/pallets/balances/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/pallets/balances/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../../_sources/autoapi/bittensor/core/extrinsics/pallets/balances/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.pallets.balances

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Balances`](<#bittensor.core.extrinsics.pallets.balances.Balances>)
      * [`Balances.transfer_all()`](<#bittensor.core.extrinsics.pallets.balances.Balances.transfer_all>)
      * [`Balances.transfer_allow_death()`](<#bittensor.core.extrinsics.pallets.balances.Balances.transfer_allow_death>)
      * [`Balances.transfer_keep_alive()`](<#bittensor.core.extrinsics.pallets.balances.Balances.transfer_keep_alive>)



# bittensor.core.extrinsics.pallets.balances[#](<#module-bittensor.core.extrinsics.pallets.balances> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`Balances`](<#bittensor.core.extrinsics.pallets.balances.Balances> "bittensor.core.extrinsics.pallets.balances.Balances") | Factory class for creating GenericCall objects for Balances pallet functions.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.extrinsics.pallets.balances.Balances[#](<#bittensor.core.extrinsics.pallets.balances.Balances> "Link to this definition")
    

Bases: [`bittensor.core.extrinsics.pallets.base.CallBuilder`](<../base/index.html#bittensor.core.extrinsics.pallets.base.CallBuilder> "bittensor.core.extrinsics.pallets.base.CallBuilder")

Factory class for creating GenericCall objects for Balances pallet functions.

This class provides methods to create GenericCall instances for all Balances pallet extrinsics.

Works with both sync (Subtensor) and async (AsyncSubtensor) instances. For async operations, pass an AsyncSubtensor instance and await the result.

Example

# Sync usage call = Balances(subtensor).transfer_all(dest=”5DE..”, keep_alive=True) response = subtensor.sign_and_send_extrinsic(call=call, …)

# Async usage call = await Balances(subtensor).transfer_all(dest=”5DE..”, keep_alive=True) response = await async_subtensor.sign_and_send_extrinsic(call=call, …)

transfer_all(_dest_ , _keep_alive_)[#](<#bittensor.core.extrinsics.pallets.balances.Balances.transfer_all> "Link to this definition")
    

Returns GenericCall instance for Subtensor function Balances.transfer_all.

Parameters:
    

  * **dest** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The destination ss58 address.

  * **keep_alive** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – A boolean to determine if the transfer_all operation should send all of the funds the account has, causing the sender account to be killed (false), or transfer everything except at least the existential deposit, which will guarantee to keep the sender account alive (true).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

transfer_allow_death(_dest_ , _value_)[#](<#bittensor.core.extrinsics.pallets.balances.Balances.transfer_allow_death> "Link to this definition")
    

Returns GenericCall instance for Subtensor function Balances.transfer_allow_death.

Parameters:
    

  * **dest** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The destination ss58 address.

  * **value** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The Balance amount in RAO to transfer.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

transfer_keep_alive(_dest_ , _value_)[#](<#bittensor.core.extrinsics.pallets.balances.Balances.transfer_keep_alive> "Link to this definition")
    

Returns GenericCall instance for Subtensor function Balances.transfer_keep_alive.

Parameters:
    

  * **dest** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The destination ss58 address.

  * **value** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The Balance amount in RAO to transfer.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

[ __ previous bittensor.core.extrinsics.pallets.admin_utils ](<../admin_utils/index.html> "previous page") [ next bittensor.core.extrinsics.pallets.base __](<../base/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Balances`](<#bittensor.core.extrinsics.pallets.balances.Balances>)
      * [`Balances.transfer_all()`](<#bittensor.core.extrinsics.pallets.balances.Balances.transfer_all>)
      * [`Balances.transfer_allow_death()`](<#bittensor.core.extrinsics.pallets.balances.Balances.transfer_allow_death>)
      * [`Balances.transfer_keep_alive()`](<#bittensor.core.extrinsics.pallets.balances.Balances.transfer_keep_alive>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.