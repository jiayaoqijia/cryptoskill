# bittensor.core.extrinsics.pallets.base &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/pallets/base/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/pallets/base/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../../_sources/autoapi/bittensor/core/extrinsics/pallets/base/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.pallets.base

##  Contents 

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Call`](<#bittensor.core.extrinsics.pallets.base.Call>)
    * [`CallBuilder`](<#bittensor.core.extrinsics.pallets.base.CallBuilder>)
      * [`CallBuilder.create_composed_call()`](<#bittensor.core.extrinsics.pallets.base.CallBuilder.create_composed_call>)
      * [`CallBuilder.dynamic_function`](<#bittensor.core.extrinsics.pallets.base.CallBuilder.dynamic_function>)
      * [`CallBuilder.subtensor`](<#bittensor.core.extrinsics.pallets.base.CallBuilder.subtensor>)



# bittensor.core.extrinsics.pallets.base[#](<#module-bittensor.core.extrinsics.pallets.base> "Link to this heading")

## Attributes[#](<#attributes> "Link to this heading")

[`Call`](<#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call") |   
---|---  
  
## Classes[#](<#classes> "Link to this heading")

[`CallBuilder`](<#bittensor.core.extrinsics.pallets.base.CallBuilder> "bittensor.core.extrinsics.pallets.base.CallBuilder") | Base class for creating GenericCall objects for all Subtensor pallet functions.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

bittensor.core.extrinsics.pallets.base.Call[#](<#bittensor.core.extrinsics.pallets.base.Call> "Link to this definition")
    

class bittensor.core.extrinsics.pallets.base.CallBuilder[#](<#bittensor.core.extrinsics.pallets.base.CallBuilder> "Link to this definition")
    

Base class for creating GenericCall objects for all Subtensor pallet functions.

This class implements an interface for creating GenericCall objects that can be used with any Subtensor pallet function. For async operations, pass an AsyncSubtensor instance and await the result.

Variables:
    

  * **subtensor** – The Subtensor or AsyncSubtensor instance used for call composition.

  * **dynamic_function** – If True, allows dynamic calls to functions not explicitly defined in the pallet class. When a

  * **pallet** (_method is called that doesn't exist in the class_ _,__it will be dynamically created as a call to the_)

  * **name.** (_function with the same_)




create_composed_call(_call_module =None_, _call_function =None_, _** kwargs_)[#](<#bittensor.core.extrinsics.pallets.base.CallBuilder.create_composed_call> "Link to this definition")
    

Create a call to the pallet function.

Parameters:
    

  * **call_module** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – If not provided, will be determined from the calling class name.

  * **call_function** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – If not provided, will be determined from the calling method name.

  * ****kwargs** – Named parameters that will be passed to the function.



Return type:
    

[Call](<#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

Note

The key in kwargs must always match the parameter name in the subtensor’s function.

dynamic_function: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)") = True[#](<#bittensor.core.extrinsics.pallets.base.CallBuilder.dynamic_function> "Link to this definition")
    

subtensor: [bittensor.core.subtensor.Subtensor](<../../../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor") | [bittensor.core.async_subtensor.AsyncSubtensor](<../../../async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor")[#](<#bittensor.core.extrinsics.pallets.base.CallBuilder.subtensor> "Link to this definition")
    

[ __ previous bittensor.core.extrinsics.pallets.balances ](<../balances/index.html> "previous page") [ next bittensor.core.extrinsics.pallets.commitments __](<../commitments/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Call`](<#bittensor.core.extrinsics.pallets.base.Call>)
    * [`CallBuilder`](<#bittensor.core.extrinsics.pallets.base.CallBuilder>)
      * [`CallBuilder.create_composed_call()`](<#bittensor.core.extrinsics.pallets.base.CallBuilder.create_composed_call>)
      * [`CallBuilder.dynamic_function`](<#bittensor.core.extrinsics.pallets.base.CallBuilder.dynamic_function>)
      * [`CallBuilder.subtensor`](<#bittensor.core.extrinsics.pallets.base.CallBuilder.subtensor>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.