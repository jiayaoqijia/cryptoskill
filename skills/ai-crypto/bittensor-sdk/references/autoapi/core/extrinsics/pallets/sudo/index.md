# bittensor.core.extrinsics.pallets.sudo &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/pallets/sudo/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/pallets/sudo/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../../_sources/autoapi/bittensor/core/extrinsics/pallets/sudo/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.pallets.sudo

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Sudo`](<#bittensor.core.extrinsics.pallets.sudo.Sudo>)
      * [`Sudo.sudo()`](<#bittensor.core.extrinsics.pallets.sudo.Sudo.sudo>)



# bittensor.core.extrinsics.pallets.sudo[#](<#module-bittensor.core.extrinsics.pallets.sudo> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`Sudo`](<#bittensor.core.extrinsics.pallets.sudo.Sudo> "bittensor.core.extrinsics.pallets.sudo.Sudo") | Factory class for creating GenericCall objects for Sudo pallet functions.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.extrinsics.pallets.sudo.Sudo[#](<#bittensor.core.extrinsics.pallets.sudo.Sudo> "Link to this definition")
    

Bases: [`bittensor.core.extrinsics.pallets.base.CallBuilder`](<../base/index.html#bittensor.core.extrinsics.pallets.base.CallBuilder> "bittensor.core.extrinsics.pallets.base.CallBuilder")

Factory class for creating GenericCall objects for Sudo pallet functions.

This class provides methods to create GenericCall instances for all Sudo pallet extrinsics.

Works with both sync (Subtensor) and async (AsyncSubtensor) instances. For async operations, pass an AsyncSubtensor instance and await the result.

Example

# Nested sync calls (e.g., with Sudo) inner_call = SubtensorModule(subtensor).set_pending_childkey_cooldown(cooldown=100) sudo_call = Sudo(subtensor).sudo(call=inner_call) response = subtensor.sign_and_send_extrinsic(call=sudo_call, …)

# Nested async calls (e.g., with Sudo) inner_call = await SubtensorModule(subtensor).set_pending_childkey_cooldown(cooldown=100) sudo_call = await Sudo(subtensor).sudo(call=inner_call) response = subtensor.sign_and_send_extrinsic(call=sudo_call, …)

sudo(_call_)[#](<#bittensor.core.extrinsics.pallets.sudo.Sudo.sudo> "Link to this definition")
    

Returns GenericCall instance for Subtensor function Sudo.sudo.

Parameters:
    

**call** (_scalecodec.GenericCall_) – The call to be executed as sudo.

Returns:
    

GenericCall instance.

Return type:
    

[bittensor.core.extrinsics.pallets.base.Call](<../base/index.html#bittensor.core.extrinsics.pallets.base.Call> "bittensor.core.extrinsics.pallets.base.Call")

[ __ previous bittensor.core.extrinsics.pallets.subtensor_module ](<../subtensor_module/index.html> "previous page") [ next bittensor.core.extrinsics.pallets.swap __](<../swap/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Sudo`](<#bittensor.core.extrinsics.pallets.sudo.Sudo>)
      * [`Sudo.sudo()`](<#bittensor.core.extrinsics.pallets.sudo.Sudo.sudo>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.