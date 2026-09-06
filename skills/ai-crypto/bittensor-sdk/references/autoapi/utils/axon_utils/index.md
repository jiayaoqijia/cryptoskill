# bittensor.utils.axon_utils &#8212; Bittensor SDK Docs  documentation

[Skip to main content](<#main-content>)

__Back to top __ `Ctrl`+`K`

[ ![Bittensor SDK Docs  documentation - Home](../../../../_static/logo.svg) ![Bittensor SDK Docs  documentation - Home](../../../../_static/logo-dark-mode.svg) ](<../../../../index.html>)

__ Search `Ctrl`+`K`

Table of Contents

  * [API Reference](<../../../index.html>) __
    * [bittensor](<../../index.html>) __
      * [bittensor.core](<../../core/index.html>) __
        * [bittensor.core.async_subtensor](<../../core/async_subtensor/index.html>)
        * [bittensor.core.axon](<../../core/axon/index.html>)
        * [bittensor.core.chain_data](<../../core/chain_data/index.html>)
        * [bittensor.core.config](<../../core/config/index.html>)
        * [bittensor.core.dendrite](<../../core/dendrite/index.html>)
        * [bittensor.core.errors](<../../core/errors/index.html>)
        * [bittensor.core.extrinsics](<../../core/extrinsics/index.html>)
        * [bittensor.core.metagraph](<../../core/metagraph/index.html>)
        * [bittensor.core.settings](<../../core/settings/index.html>)
        * [bittensor.core.stream](<../../core/stream/index.html>)
        * [bittensor.core.subtensor](<../../core/subtensor/index.html>)
        * [bittensor.core.synapse](<../../core/synapse/index.html>)
        * [bittensor.core.tensor](<../../core/tensor/index.html>)
        * [bittensor.core.threadpool](<../../core/threadpool/index.html>)
        * [bittensor.core.types](<../../core/types/index.html>)
      * [bittensor.extras](<../../extras/index.html>) __
        * [bittensor.extras.dev_framework](<../../extras/dev_framework/index.html>)
        * [bittensor.extras.subtensor_api](<../../extras/subtensor_api/index.html>)
        * [bittensor.extras.timelock](<../../extras/timelock/index.html>)
      * [bittensor.utils](<../index.html>) __
        * [bittensor.utils.axon_utils](<#>)
        * [bittensor.utils.balance](<../balance/index.html>)
        * [bittensor.utils.btlogging](<../btlogging/index.html>)
        * [bittensor.utils.easy_imports](<../easy_imports/index.html>)
        * [bittensor.utils.formatting](<../formatting/index.html>)
        * [bittensor.utils.liquidity](<../liquidity/index.html>)
        * [bittensor.utils.networking](<../networking/index.html>)
        * [bittensor.utils.registration](<../registration/index.html>)
        * [bittensor.utils.subnets](<../subnets/index.html>)
        * [bittensor.utils.version](<../version/index.html>)
        * [bittensor.utils.weight_utils](<../weight_utils/index.html>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/utils/axon_utils/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/utils/axon_utils/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/utils/axon_utils/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.utils.axon_utils

##  Contents 

  * [Attributes](<#attributes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`ALLOWED_DELTA`](<#bittensor.utils.axon_utils.ALLOWED_DELTA>)
    * [`NANOSECONDS_IN_SECOND`](<#bittensor.utils.axon_utils.NANOSECONDS_IN_SECOND>)
    * [`allowed_nonce_window_ns()`](<#bittensor.utils.axon_utils.allowed_nonce_window_ns>)
    * [`calculate_diff_seconds()`](<#bittensor.utils.axon_utils.calculate_diff_seconds>)



# bittensor.utils.axon_utils[#](<#module-bittensor.utils.axon_utils> "Link to this heading")

## Attributes[#](<#attributes> "Link to this heading")

[`ALLOWED_DELTA`](<#bittensor.utils.axon_utils.ALLOWED_DELTA> "bittensor.utils.axon_utils.ALLOWED_DELTA") |   
---|---  
[`NANOSECONDS_IN_SECOND`](<#bittensor.utils.axon_utils.NANOSECONDS_IN_SECOND> "bittensor.utils.axon_utils.NANOSECONDS_IN_SECOND") |   
  
## Functions[#](<#functions> "Link to this heading")

[`allowed_nonce_window_ns`](<#bittensor.utils.axon_utils.allowed_nonce_window_ns> "bittensor.utils.axon_utils.allowed_nonce_window_ns")(current_time_ns[, synapse_timeout]) | Calculates the allowed window for a nonce in nanoseconds.  
---|---  
[`calculate_diff_seconds`](<#bittensor.utils.axon_utils.calculate_diff_seconds> "bittensor.utils.axon_utils.calculate_diff_seconds")(current_time, synapse_timeout, ...) | Calculates the difference in seconds between the current time and the synapse nonce, and also returns the allowed  
  
## Module Contents[#](<#module-contents> "Link to this heading")

bittensor.utils.axon_utils.ALLOWED_DELTA = 4000000000[#](<#bittensor.utils.axon_utils.ALLOWED_DELTA> "Link to this definition")
    

bittensor.utils.axon_utils.NANOSECONDS_IN_SECOND = 1000000000[#](<#bittensor.utils.axon_utils.NANOSECONDS_IN_SECOND> "Link to this definition")
    

bittensor.utils.axon_utils.allowed_nonce_window_ns(_current_time_ns_ , _synapse_timeout =None_)[#](<#bittensor.utils.axon_utils.allowed_nonce_window_ns> "Link to this definition")
    

Calculates the allowed window for a nonce in nanoseconds.

Parameters:
    

  * **current_time_ns** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The current time in nanoseconds.

  * **synapse_timeout** (_Optional_ _[_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _]_) – The optional timeout for the synapse in seconds. If None, it defaults to 0.



Returns:
    

The allowed nonce window in nanoseconds.

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

bittensor.utils.axon_utils.calculate_diff_seconds(_current_time_ , _synapse_timeout_ , _synapse_nonce_)[#](<#bittensor.utils.axon_utils.calculate_diff_seconds> "Link to this definition")
    

Calculates the difference in seconds between the current time and the synapse nonce, and also returns the allowed delta in seconds.

Parameters:
    

  * **current_time** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The current time in nanoseconds.

  * **synapse_timeout** (_Optional_ _[_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _]_) – The optional timeout for the synapse in seconds.

  * **synapse_nonce** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The nonce value for the synapse in nanoseconds.



Returns:
    

A tuple containing the difference in seconds (float) and the allowed delta in seconds (float).

[ __ previous bittensor.utils ](<../index.html> "previous page") [ next bittensor.utils.balance __](<../balance/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`ALLOWED_DELTA`](<#bittensor.utils.axon_utils.ALLOWED_DELTA>)
    * [`NANOSECONDS_IN_SECOND`](<#bittensor.utils.axon_utils.NANOSECONDS_IN_SECOND>)
    * [`allowed_nonce_window_ns()`](<#bittensor.utils.axon_utils.allowed_nonce_window_ns>)
    * [`calculate_diff_seconds()`](<#bittensor.utils.axon_utils.calculate_diff_seconds>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.