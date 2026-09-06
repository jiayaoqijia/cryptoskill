# bittensor.core.extrinsics.pallets.crowdloan &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/pallets/crowdloan/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/pallets/crowdloan/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../../_sources/autoapi/bittensor/core/extrinsics/pallets/crowdloan/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.pallets.crowdloan

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Crowdloan`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan>)
      * [`Crowdloan.contribute()`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.contribute>)
      * [`Crowdloan.create()`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.create>)
      * [`Crowdloan.dissolve()`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.dissolve>)
      * [`Crowdloan.finalize()`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.finalize>)
      * [`Crowdloan.refund()`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.refund>)
      * [`Crowdloan.update_cap()`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.update_cap>)
      * [`Crowdloan.update_end()`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.update_end>)
      * [`Crowdloan.update_min_contribution()`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.update_min_contribution>)
      * [`Crowdloan.withdraw()`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.withdraw>)



# bittensor.core.extrinsics.pallets.crowdloan[#](<#module-bittensor.core.extrinsics.pallets.crowdloan> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`Crowdloan`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan> "bittensor.core.extrinsics.pallets.crowdloan.Crowdloan") | Factory class for creating GenericCall objects for Crowdloan pallet functions.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.extrinsics.pallets.crowdloan.Crowdloan[#](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan> "Link to this definition")
    

Bases: [`bittensor.core.extrinsics.pallets.base.CallBuilder`](<../base/index.html#bittensor.core.extrinsics.pallets.base.CallBuilder> "bittensor.core.extrinsics.pallets.base.CallBuilder")

Factory class for creating GenericCall objects for Crowdloan pallet functions.

This class provides methods to create GenericCall instances for all Crowdloan pallet extrinsics.

Works with both sync (Subtensor) and async (AsyncSubtensor) instances. For async operations, pass an AsyncSubtensor instance and await the result.

Example

# Sync usage call = Crowdloan(subtensor).finalize(crowdloan_id=123) response = subtensor.sign_and_send_extrinsic(call=call, …)

# Async usage call = await Crowdloan(subtensor).finalize(crowdloan_id=123) response = await async_subtensor.sign_and_send_extrinsic(call=call, …)

contribute(_crowdloan_id_ , _amount_)[#](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.contribute> "Link to this definition")
    

Returns GenericCall instance for Subtensor function Crowdloan.contribute.

Parameters:
    

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to contribute to.

  * **amount** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Amount in RAO to contribute.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

create(_deposit_ , _min_contribution_ , _cap_ , _end_ , _call =None_, _target_address =None_)[#](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.create> "Link to this definition")
    

Returns GenericCall instance for Subtensor function Crowdloan.create.

Parameters:
    

  * **deposit** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Initial deposit in RAO from the creator.

  * **min_contribution** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Minimum contribution amount in RAO.

  * **cap** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Maximum cap to be raised in RAO.

  * **end** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Block number when the campaign ends.

  * **call** (_Optional_ _[__scalecodec.GenericCall_ _]_) – Runtime call data (e.g., subtensor::register_leased_network).

  * **target_address** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – SS58 address to transfer funds to on success.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

dissolve(_crowdloan_id_)[#](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.dissolve> "Link to this definition")
    

Returns GenericCall instance for Subtensor function Crowdloan.dissolve.

Parameters:
    

**crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to dissolve.

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

finalize(_crowdloan_id_)[#](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.finalize> "Link to this definition")
    

Returns GenericCall instance for Subtensor function Crowdloan.finalize.

Parameters:
    

**crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to finalize.

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

refund(_crowdloan_id_)[#](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.refund> "Link to this definition")
    

Returns GenericCall instance for Subtensor function Crowdloan.refund.

Parameters:
    

**crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to refund.

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

update_cap(_crowdloan_id_ , _new_cap_)[#](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.update_cap> "Link to this definition")
    

Returns GenericCall instance for Subtensor function Crowdloan.update_cap.

Parameters:
    

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to update the cap for.

  * **new_cap** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – New cap to be raised in RAO.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

update_end(_crowdloan_id_ , _new_end_)[#](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.update_end> "Link to this definition")
    

Returns GenericCall instance for Subtensor function Crowdloan.update_end.

Parameters:
    

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to update the end block number for.

  * **new_end** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – New end block number.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

update_min_contribution(_crowdloan_id_ , _new_min_contribution_)[#](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.update_min_contribution> "Link to this definition")
    

Returns GenericCall instance for Subtensor function Crowdloan.update_min_contribution.

Parameters:
    

  * **crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to update the minimum contribution amount for.

  * **new_min_contribution** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – New minimum contribution amount in RAO.



Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

withdraw(_crowdloan_id_)[#](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.withdraw> "Link to this definition")
    

Returns GenericCall instance for Subtensor function Crowdloan.withdraw.

Parameters:
    

**crowdloan_id** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the crowdloan to withdraw from.

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

[ __ previous bittensor.core.extrinsics.pallets.commitments ](<../commitments/index.html> "previous page") [ next bittensor.core.extrinsics.pallets.mev_shield __](<../mev_shield/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Crowdloan`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan>)
      * [`Crowdloan.contribute()`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.contribute>)
      * [`Crowdloan.create()`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.create>)
      * [`Crowdloan.dissolve()`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.dissolve>)
      * [`Crowdloan.finalize()`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.finalize>)
      * [`Crowdloan.refund()`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.refund>)
      * [`Crowdloan.update_cap()`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.update_cap>)
      * [`Crowdloan.update_end()`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.update_end>)
      * [`Crowdloan.update_min_contribution()`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.update_min_contribution>)
      * [`Crowdloan.withdraw()`](<#bittensor.core.extrinsics.pallets.crowdloan.Crowdloan.withdraw>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.