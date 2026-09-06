# bittensor.utils.btlogging.levels &#8212; Bittensor SDK Docs  documentation

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
        * [bittensor.utils.btlogging](<../index.html>)
        * [bittensor.utils.easy_imports](<../../easy_imports/index.html>)
        * [bittensor.utils.formatting](<../../formatting/index.html>)
        * [bittensor.utils.liquidity](<../../liquidity/index.html>)
        * [bittensor.utils.networking](<../../networking/index.html>)
        * [bittensor.utils.registration](<../../registration/index.html>)
        * [bittensor.utils.subnets](<../../subnets/index.html>)
        * [bittensor.utils.version](<../../version/index.html>)
        * [bittensor.utils.weight_utils](<../../weight_utils/index.html>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/utils/btlogging/levels/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/utils/btlogging/levels/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/utils/btlogging/levels/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.utils.btlogging.levels

##  Contents 

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`debug()`](<#bittensor.utils.btlogging.levels.debug>)
    * [`info()`](<#bittensor.utils.btlogging.levels.info>)
    * [`trace()`](<#bittensor.utils.btlogging.levels.trace>)
    * [`warning()`](<#bittensor.utils.btlogging.levels.warning>)



# bittensor.utils.btlogging.levels[#](<#module-bittensor.utils.btlogging.levels> "Link to this heading")

## Functions[#](<#functions> "Link to this heading")

[`debug`](<#bittensor.utils.btlogging.levels.debug> "bittensor.utils.btlogging.levels.debug")([on]) | Enables or disables debug logging.  
---|---  
[`info`](<#bittensor.utils.btlogging.levels.info> "bittensor.utils.btlogging.levels.info")([on]) | Enables or disables info logging.  
[`trace`](<#bittensor.utils.btlogging.levels.trace> "bittensor.utils.btlogging.levels.trace")([on]) | Enables or disables trace logging.  
[`warning`](<#bittensor.utils.btlogging.levels.warning> "bittensor.utils.btlogging.levels.warning")([on]) | Enables or disables warning logging.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

bittensor.utils.btlogging.levels.debug(_on =True_)[#](<#bittensor.utils.btlogging.levels.debug> "Link to this definition")
    

Enables or disables debug logging.

Parameters:
    

**on** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, enables debug logging. If False, disables debug logging.

bittensor.utils.btlogging.levels.info(_on =True_)[#](<#bittensor.utils.btlogging.levels.info> "Link to this definition")
    

Enables or disables info logging.

Parameters:
    

**on** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, enables info logging. If False, disables info logging and sets default (WARNING) level.

bittensor.utils.btlogging.levels.trace(_on =True_)[#](<#bittensor.utils.btlogging.levels.trace> "Link to this definition")
    

Enables or disables trace logging.

Parameters:
    

**on** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, enables trace logging. If False, disables trace logging.

bittensor.utils.btlogging.levels.warning(_on =True_)[#](<#bittensor.utils.btlogging.levels.warning> "Link to this definition")
    

Enables or disables warning logging.

Parameters:
    

**on** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, enables warning logging. If False, disables warning logging and sets default (WARNING) level.

[ __ previous bittensor.utils.btlogging.helpers ](<../helpers/index.html> "previous page") [ next bittensor.utils.btlogging.loggingmachine __](<../loggingmachine/index.html> "next page")

__Contents

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`debug()`](<#bittensor.utils.btlogging.levels.debug>)
    * [`info()`](<#bittensor.utils.btlogging.levels.info>)
    * [`trace()`](<#bittensor.utils.btlogging.levels.trace>)
    * [`warning()`](<#bittensor.utils.btlogging.levels.warning>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.