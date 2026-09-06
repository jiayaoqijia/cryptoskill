# bittensor.utils.registration.torch_utils &#8212; Bittensor SDK Docs  documentation

[Skip to main content](<#main-content>)

__Back to top __ `Ctrl`+`K`

[ ![Bittensor SDK Docs  documentation - Home](../../../../../_static/logo.svg) ![Bittensor SDK Docs  documentation - Home](../../../../../_static/logo-dark-mode.svg) ](<../../../../../index.html>)

__ Search `Ctrl`+`K`

Table of Contents

  * [API Reference](<../../../../index.html>) __
    * [bittensor](<../../../index.html>) __
      * [bittensor.core](<../../../core/index.html>) __
        * [bittensor.core.async_subtensor](<../../../core/async_subtensor/index.html>)
        * [bittensor.core.axon](<../../../core/axon/index.html>)
        * [bittensor.core.chain_data](<../../../core/chain_data/index.html>)
        * [bittensor.core.config](<../../../core/config/index.html>)
        * [bittensor.core.dendrite](<../../../core/dendrite/index.html>)
        * [bittensor.core.errors](<../../../core/errors/index.html>)
        * [bittensor.core.extrinsics](<../../../core/extrinsics/index.html>)
        * [bittensor.core.metagraph](<../../../core/metagraph/index.html>)
        * [bittensor.core.settings](<../../../core/settings/index.html>)
        * [bittensor.core.stream](<../../../core/stream/index.html>)
        * [bittensor.core.subtensor](<../../../core/subtensor/index.html>)
        * [bittensor.core.synapse](<../../../core/synapse/index.html>)
        * [bittensor.core.tensor](<../../../core/tensor/index.html>)
        * [bittensor.core.threadpool](<../../../core/threadpool/index.html>)
        * [bittensor.core.types](<../../../core/types/index.html>)
      * [bittensor.extras](<../../../extras/index.html>) __
        * [bittensor.extras.dev_framework](<../../../extras/dev_framework/index.html>)
        * [bittensor.extras.subtensor_api](<../../../extras/subtensor_api/index.html>)
        * [bittensor.extras.timelock](<../../../extras/timelock/index.html>)
      * [bittensor.utils](<../../index.html>) __
        * [bittensor.utils.axon_utils](<../../axon_utils/index.html>)
        * [bittensor.utils.balance](<../../balance/index.html>)
        * [bittensor.utils.btlogging](<../../btlogging/index.html>)
        * [bittensor.utils.easy_imports](<../../easy_imports/index.html>)
        * [bittensor.utils.formatting](<../../formatting/index.html>)
        * [bittensor.utils.liquidity](<../../liquidity/index.html>)
        * [bittensor.utils.networking](<../../networking/index.html>)
        * [bittensor.utils.registration](<../index.html>)
        * [bittensor.utils.subnets](<../../subnets/index.html>)
        * [bittensor.utils.version](<../../version/index.html>)
        * [bittensor.utils.weight_utils](<../../weight_utils/index.html>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/utils/registration/torch_utils/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/utils/registration/torch_utils/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/utils/registration/torch_utils/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.utils.registration.torch_utils

##  Contents 

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`LazyLoadedTorch`](<#bittensor.utils.registration.torch_utils.LazyLoadedTorch>)
    * [`legacy_torch_api_compat()`](<#bittensor.utils.registration.torch_utils.legacy_torch_api_compat>)
    * [`log_no_torch_error()`](<#bittensor.utils.registration.torch_utils.log_no_torch_error>)
    * [`torch`](<#bittensor.utils.registration.torch_utils.torch>)
    * [`use_torch()`](<#bittensor.utils.registration.torch_utils.use_torch>)



# bittensor.utils.registration.torch_utils[#](<#module-bittensor.utils.registration.torch_utils> "Link to this heading")

Torch compatibility utilities for Bittensor.

## Attributes[#](<#attributes> "Link to this heading")

[`torch`](<#bittensor.utils.registration.torch_utils.torch> "bittensor.utils.registration.torch_utils.torch") |   
---|---  
  
## Classes[#](<#classes> "Link to this heading")

[`LazyLoadedTorch`](<#bittensor.utils.registration.torch_utils.LazyLoadedTorch> "bittensor.utils.registration.torch_utils.LazyLoadedTorch") | A lazy-loading proxy for the torch module.  
---|---  
  
## Functions[#](<#functions> "Link to this heading")

[`legacy_torch_api_compat`](<#bittensor.utils.registration.torch_utils.legacy_torch_api_compat> "bittensor.utils.registration.torch_utils.legacy_torch_api_compat")(func) | Convert function operating on numpy Input&Output to legacy torch Input&Output API if use_torch() is True.  
---|---  
[`log_no_torch_error`](<#bittensor.utils.registration.torch_utils.log_no_torch_error> "bittensor.utils.registration.torch_utils.log_no_torch_error")() |   
[`use_torch`](<#bittensor.utils.registration.torch_utils.use_torch> "bittensor.utils.registration.torch_utils.use_torch")() | Force the use of torch over numpy for certain operations.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.utils.registration.torch_utils.LazyLoadedTorch[#](<#bittensor.utils.registration.torch_utils.LazyLoadedTorch> "Link to this definition")
    

A lazy-loading proxy for the torch module.

bittensor.utils.registration.torch_utils.legacy_torch_api_compat(_func_)[#](<#bittensor.utils.registration.torch_utils.legacy_torch_api_compat> "Link to this definition")
    

Convert function operating on numpy Input&Output to legacy torch Input&Output API if use_torch() is True.

Parameters:
    

**func** – Function with numpy Input/Output to be decorated.

Returns:
    

Decorated function.

Return type:
    

decorated

bittensor.utils.registration.torch_utils.log_no_torch_error()[#](<#bittensor.utils.registration.torch_utils.log_no_torch_error> "Link to this definition")
    

bittensor.utils.registration.torch_utils.torch[#](<#bittensor.utils.registration.torch_utils.torch> "Link to this definition")
    

bittensor.utils.registration.torch_utils.use_torch()[#](<#bittensor.utils.registration.torch_utils.use_torch> "Link to this definition")
    

Force the use of torch over numpy for certain operations.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

[ __ previous bittensor.utils.registration ](<../index.html> "previous page") [ next bittensor.utils.subnets __](<../../subnets/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`LazyLoadedTorch`](<#bittensor.utils.registration.torch_utils.LazyLoadedTorch>)
    * [`legacy_torch_api_compat()`](<#bittensor.utils.registration.torch_utils.legacy_torch_api_compat>)
    * [`log_no_torch_error()`](<#bittensor.utils.registration.torch_utils.log_no_torch_error>)
    * [`torch`](<#bittensor.utils.registration.torch_utils.torch>)
    * [`use_torch()`](<#bittensor.utils.registration.torch_utils.use_torch>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.