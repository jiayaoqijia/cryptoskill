# bittensor.core.extrinsics.pallets.swap &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/pallets/swap/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/pallets/swap/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../../_sources/autoapi/bittensor/core/extrinsics/pallets/swap/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.pallets.swap

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Swap`](<#bittensor.core.extrinsics.pallets.swap.Swap>)
      * [`Swap.add_liquidity()`](<#bittensor.core.extrinsics.pallets.swap.Swap.add_liquidity>)
      * [`Swap.modify_position()`](<#bittensor.core.extrinsics.pallets.swap.Swap.modify_position>)
      * [`Swap.remove_liquidity()`](<#bittensor.core.extrinsics.pallets.swap.Swap.remove_liquidity>)
      * [`Swap.toggle_user_liquidity()`](<#bittensor.core.extrinsics.pallets.swap.Swap.toggle_user_liquidity>)



# bittensor.core.extrinsics.pallets.swap[#](<#module-bittensor.core.extrinsics.pallets.swap> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`Swap`](<#bittensor.core.extrinsics.pallets.swap.Swap> "bittensor.core.extrinsics.pallets.swap.Swap") | Factory class for creating GenericCall objects for Swap pallet functions.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.extrinsics.pallets.swap.Swap[#](<#bittensor.core.extrinsics.pallets.swap.Swap> "Link to this definition")
    

Bases: [`bittensor.core.extrinsics.pallets.base.CallBuilder`](<../base/index.html#bittensor.core.extrinsics.pallets.base.CallBuilder> "bittensor.core.extrinsics.pallets.base.CallBuilder")

Factory class for creating GenericCall objects for Swap pallet functions.

This class provides methods to create GenericCall instances for all Swap pallet extrinsics.

Works with both sync (Subtensor) and async (AsyncSubtensor) instances. For async operations, pass an AsyncSubtensor instance and await the result.

Example

# Sync usage call = Swap(subtensor).toggle_user_liquidity(netuid=14, enable=True) response = subtensor.sign_and_send_extrinsic(call=call, …)

# Async usage call = await Swap(subtensor).toggle_user_liquidity(netuid=14, enable=True) response = await async_subtensor.sign_and_send_extrinsic(call=call, …)

add_liquidity(_netuid_ , _liquidity_ , _tick_low_ , _tick_high_ , _hotkey =None_)[#](<#bittensor.core.extrinsics.pallets.swap.Swap.add_liquidity> "Link to this definition")
    

Returns GenericCall instance for Subtensor function Swap.add_liquidity.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The UID of the target subnet for which the call is being initiated.

  * **liquidity** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The amount of liquidity in RAO to be added.

  * **tick_low** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The lower bound of the price tick range.

  * **tick_high** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The upper bound of the price tick range.

  * **hotkey** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The hotkey with staked TAO in Alpha. If not passed then the wallet hotkey is used.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

modify_position(_netuid_ , _hotkey_ , _position_id_ , _liquidity_delta_)[#](<#bittensor.core.extrinsics.pallets.swap.Swap.modify_position> "Link to this definition")
    

Returns GenericCall instance for Subtensor function Swap.modify_position.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The UID of the target subnet for which the call is being initiated.

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey with staked TAO in Alpha. If not passed then the wallet hotkey is used.

  * **position_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The id of the position record in the pool.

  * **liquidity_delta** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The amount of liquidity in RAO to be added or removed (could be positive or negative).



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

remove_liquidity(_netuid_ , _hotkey_ , _position_id_)[#](<#bittensor.core.extrinsics.pallets.swap.Swap.remove_liquidity> "Link to this definition")
    

Returns GenericCall instance for Subtensor function Swap.remove_liquidity.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The UID of the target subnet for which the call is being initiated.

  * **position_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The id of the position record in the pool.

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey with staked TAO in Alpha. If not passed then the wallet hotkey is used.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

toggle_user_liquidity(_netuid_ , _enable_)[#](<#bittensor.core.extrinsics.pallets.swap.Swap.toggle_user_liquidity> "Link to this definition")
    

Returns GenericCall instance for Subtensor function Swap.toggle_user_liquidity.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The UID of the target subnet for which the call is being initiated.

  * **enable** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Boolean indicating whether to enable user liquidity.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

[ __ previous bittensor.core.extrinsics.pallets.sudo ](<../sudo/index.html> "previous page") [ next bittensor.core.extrinsics.proxy __](<../../proxy/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Swap`](<#bittensor.core.extrinsics.pallets.swap.Swap>)
      * [`Swap.add_liquidity()`](<#bittensor.core.extrinsics.pallets.swap.Swap.add_liquidity>)
      * [`Swap.modify_position()`](<#bittensor.core.extrinsics.pallets.swap.Swap.modify_position>)
      * [`Swap.remove_liquidity()`](<#bittensor.core.extrinsics.pallets.swap.Swap.remove_liquidity>)
      * [`Swap.toggle_user_liquidity()`](<#bittensor.core.extrinsics.pallets.swap.Swap.toggle_user_liquidity>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.