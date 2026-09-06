# bittensor.utils.btlogging.console &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/utils/btlogging/console/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/utils/btlogging/console/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/utils/btlogging/console/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.utils.btlogging.console

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`BittensorConsole`](<#bittensor.utils.btlogging.console.BittensorConsole>)
      * [`BittensorConsole.critical()`](<#bittensor.utils.btlogging.console.BittensorConsole.critical>)
      * [`BittensorConsole.debug()`](<#bittensor.utils.btlogging.console.BittensorConsole.debug>)
      * [`BittensorConsole.error()`](<#bittensor.utils.btlogging.console.BittensorConsole.error>)
      * [`BittensorConsole.info()`](<#bittensor.utils.btlogging.console.BittensorConsole.info>)
      * [`BittensorConsole.logger`](<#bittensor.utils.btlogging.console.BittensorConsole.logger>)
      * [`BittensorConsole.success()`](<#bittensor.utils.btlogging.console.BittensorConsole.success>)
      * [`BittensorConsole.warning()`](<#bittensor.utils.btlogging.console.BittensorConsole.warning>)



# bittensor.utils.btlogging.console[#](<#module-bittensor.utils.btlogging.console> "Link to this heading")

BittensorConsole class gives the ability to log messages to the terminal without changing Bittensor logging level.

Example

from bittensor import logging

# will be logged logging.console.info(“info message”) logging.console.error(“error message”) logging.console.success(“success message”) logging.console.warning(“warning message”) logging.console.critical(“critical message”)

# will not be logged logging.info(“test info”)

## Classes[#](<#classes> "Link to this heading")

[`BittensorConsole`](<#bittensor.utils.btlogging.console.BittensorConsole> "bittensor.utils.btlogging.console.BittensorConsole") |   
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.utils.btlogging.console.BittensorConsole(_logger_)[#](<#bittensor.utils.btlogging.console.BittensorConsole> "Link to this definition")
    

Parameters:
    

**logger** ([_bittensor.utils.btlogging.loggingmachine.LoggingMachine_](<../loggingmachine/index.html#bittensor.utils.btlogging.loggingmachine.LoggingMachine> "bittensor.utils.btlogging.loggingmachine.LoggingMachine"))

critical(_message_)[#](<#bittensor.utils.btlogging.console.BittensorConsole.critical> "Link to this definition")
    

Logs a CRITICAL message to the console.

Parameters:
    

**message** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

debug(_message_)[#](<#bittensor.utils.btlogging.console.BittensorConsole.debug> "Link to this definition")
    

Logs a DEBUG message to the console.

Parameters:
    

**message** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

error(_message_)[#](<#bittensor.utils.btlogging.console.BittensorConsole.error> "Link to this definition")
    

Logs a ERROR message to the console.

Parameters:
    

**message** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

info(_message_)[#](<#bittensor.utils.btlogging.console.BittensorConsole.info> "Link to this definition")
    

Logs a INFO message to the console.

Parameters:
    

**message** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

logger[#](<#bittensor.utils.btlogging.console.BittensorConsole.logger> "Link to this definition")
    

success(_message_)[#](<#bittensor.utils.btlogging.console.BittensorConsole.success> "Link to this definition")
    

Logs a SUCCESS message to the console.

Parameters:
    

**message** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

warning(_message_)[#](<#bittensor.utils.btlogging.console.BittensorConsole.warning> "Link to this definition")
    

Logs a WARNING message to the console.

Parameters:
    

**message** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

[ __ previous bittensor.utils.btlogging ](<../index.html> "previous page") [ next bittensor.utils.btlogging.defines __](<../defines/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`BittensorConsole`](<#bittensor.utils.btlogging.console.BittensorConsole>)
      * [`BittensorConsole.critical()`](<#bittensor.utils.btlogging.console.BittensorConsole.critical>)
      * [`BittensorConsole.debug()`](<#bittensor.utils.btlogging.console.BittensorConsole.debug>)
      * [`BittensorConsole.error()`](<#bittensor.utils.btlogging.console.BittensorConsole.error>)
      * [`BittensorConsole.info()`](<#bittensor.utils.btlogging.console.BittensorConsole.info>)
      * [`BittensorConsole.logger`](<#bittensor.utils.btlogging.console.BittensorConsole.logger>)
      * [`BittensorConsole.success()`](<#bittensor.utils.btlogging.console.BittensorConsole.success>)
      * [`BittensorConsole.warning()`](<#bittensor.utils.btlogging.console.BittensorConsole.warning>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.