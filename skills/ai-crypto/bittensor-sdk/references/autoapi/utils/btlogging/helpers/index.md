# bittensor.utils.btlogging.helpers &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/utils/btlogging/helpers/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/utils/btlogging/helpers/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/utils/btlogging/helpers/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.utils.btlogging.helpers

##  Contents 

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`all_logger_names()`](<#bittensor.utils.btlogging.helpers.all_logger_names>)
    * [`all_loggers()`](<#bittensor.utils.btlogging.helpers.all_loggers>)
    * [`get_max_logger_name_length()`](<#bittensor.utils.btlogging.helpers.get_max_logger_name_length>)



# bittensor.utils.btlogging.helpers[#](<#module-bittensor.utils.btlogging.helpers> "Link to this heading")

btlogging.helpers module provides helper functions for the Bittensor logging system.

## Functions[#](<#functions> "Link to this heading")

[`all_logger_names`](<#bittensor.utils.btlogging.helpers.all_logger_names> "bittensor.utils.btlogging.helpers.all_logger_names")() | Generate the names of all active loggers.  
---|---  
[`all_loggers`](<#bittensor.utils.btlogging.helpers.all_loggers> "bittensor.utils.btlogging.helpers.all_loggers")() | Generator that yields all logger instances in the application.  
[`get_max_logger_name_length`](<#bittensor.utils.btlogging.helpers.get_max_logger_name_length> "bittensor.utils.btlogging.helpers.get_max_logger_name_length")() | Calculate and return the length of the longest logger name.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

bittensor.utils.btlogging.helpers.all_logger_names()[#](<#bittensor.utils.btlogging.helpers.all_logger_names> "Link to this definition")
    

Generate the names of all active loggers.

This function iterates through the logging root manager’s logger dictionary and yields the names of all active Logger instances. It skips placeholders and other types that are not instances of Logger.

Yields:
    

The name of an active logger.

Return type:
    

Generator[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), None, None]

bittensor.utils.btlogging.helpers.all_loggers()[#](<#bittensor.utils.btlogging.helpers.all_loggers> "Link to this definition")
    

Generator that yields all logger instances in the application.

Iterates through the logging root manager’s logger dictionary and yields all active Logger instances. It skips placeholders and other types that are not instances of Logger.

Yields:
    

_logger_ – An active logger instance.

Return type:
    

Generator[[logging.Logger](<https://docs.python.org/3/library/logging.html#logging.Logger> "\(in Python v3.14\)"), None, None]

bittensor.utils.btlogging.helpers.get_max_logger_name_length()[#](<#bittensor.utils.btlogging.helpers.get_max_logger_name_length> "Link to this definition")
    

Calculate and return the length of the longest logger name.

This function iterates through all active logger names and determines the length of the longest name.

Returns:
    

The length of the longest logger name.

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

[ __ previous bittensor.utils.btlogging.format ](<../format/index.html> "previous page") [ next bittensor.utils.btlogging.levels __](<../levels/index.html> "next page")

__Contents

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`all_logger_names()`](<#bittensor.utils.btlogging.helpers.all_logger_names>)
    * [`all_loggers()`](<#bittensor.utils.btlogging.helpers.all_loggers>)
    * [`get_max_logger_name_length()`](<#bittensor.utils.btlogging.helpers.get_max_logger_name_length>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.