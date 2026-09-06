# bittensor.utils.btlogging.defines &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/utils/btlogging/defines/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/utils/btlogging/defines/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/utils/btlogging/defines/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.utils.btlogging.defines

##  Contents 

  * [Attributes](<#attributes>)
  * [Module Contents](<#module-contents>)
    * [`BASE_LOG_FORMAT`](<#bittensor.utils.btlogging.defines.BASE_LOG_FORMAT>)
    * [`BITTENSOR_LOGGER_NAME`](<#bittensor.utils.btlogging.defines.BITTENSOR_LOGGER_NAME>)
    * [`DATE_FORMAT`](<#bittensor.utils.btlogging.defines.DATE_FORMAT>)
    * [`DEFAULT_LOG_BACKUP_COUNT`](<#bittensor.utils.btlogging.defines.DEFAULT_LOG_BACKUP_COUNT>)
    * [`DEFAULT_LOG_FILE_NAME`](<#bittensor.utils.btlogging.defines.DEFAULT_LOG_FILE_NAME>)
    * [`DEFAULT_MAX_ROTATING_LOG_FILE_SIZE`](<#bittensor.utils.btlogging.defines.DEFAULT_MAX_ROTATING_LOG_FILE_SIZE>)
    * [`TRACE_LOG_FORMAT`](<#bittensor.utils.btlogging.defines.TRACE_LOG_FORMAT>)



# bittensor.utils.btlogging.defines[#](<#module-bittensor.utils.btlogging.defines> "Link to this heading")

Btlogging constant definition module.

## Attributes[#](<#attributes> "Link to this heading")

[`BASE_LOG_FORMAT`](<#bittensor.utils.btlogging.defines.BASE_LOG_FORMAT> "bittensor.utils.btlogging.defines.BASE_LOG_FORMAT") |   
---|---  
[`BITTENSOR_LOGGER_NAME`](<#bittensor.utils.btlogging.defines.BITTENSOR_LOGGER_NAME> "bittensor.utils.btlogging.defines.BITTENSOR_LOGGER_NAME") |   
[`DATE_FORMAT`](<#bittensor.utils.btlogging.defines.DATE_FORMAT> "bittensor.utils.btlogging.defines.DATE_FORMAT") |   
[`DEFAULT_LOG_BACKUP_COUNT`](<#bittensor.utils.btlogging.defines.DEFAULT_LOG_BACKUP_COUNT> "bittensor.utils.btlogging.defines.DEFAULT_LOG_BACKUP_COUNT") |   
[`DEFAULT_LOG_FILE_NAME`](<#bittensor.utils.btlogging.defines.DEFAULT_LOG_FILE_NAME> "bittensor.utils.btlogging.defines.DEFAULT_LOG_FILE_NAME") |   
[`DEFAULT_MAX_ROTATING_LOG_FILE_SIZE`](<#bittensor.utils.btlogging.defines.DEFAULT_MAX_ROTATING_LOG_FILE_SIZE> "bittensor.utils.btlogging.defines.DEFAULT_MAX_ROTATING_LOG_FILE_SIZE") |   
[`TRACE_LOG_FORMAT`](<#bittensor.utils.btlogging.defines.TRACE_LOG_FORMAT> "bittensor.utils.btlogging.defines.TRACE_LOG_FORMAT") |   
  
## Module Contents[#](<#module-contents> "Link to this heading")

bittensor.utils.btlogging.defines.BASE_LOG_FORMAT = '%(asctime)s | %(levelname)s | %(message)s'[#](<#bittensor.utils.btlogging.defines.BASE_LOG_FORMAT> "Link to this definition")
    

bittensor.utils.btlogging.defines.BITTENSOR_LOGGER_NAME = 'bittensor'[#](<#bittensor.utils.btlogging.defines.BITTENSOR_LOGGER_NAME> "Link to this definition")
    

bittensor.utils.btlogging.defines.DATE_FORMAT = '%Y-%m-%d %H:%M:%S'[#](<#bittensor.utils.btlogging.defines.DATE_FORMAT> "Link to this definition")
    

bittensor.utils.btlogging.defines.DEFAULT_LOG_BACKUP_COUNT = 10[#](<#bittensor.utils.btlogging.defines.DEFAULT_LOG_BACKUP_COUNT> "Link to this definition")
    

bittensor.utils.btlogging.defines.DEFAULT_LOG_FILE_NAME = 'bittensor.log'[#](<#bittensor.utils.btlogging.defines.DEFAULT_LOG_FILE_NAME> "Link to this definition")
    

bittensor.utils.btlogging.defines.DEFAULT_MAX_ROTATING_LOG_FILE_SIZE = 26214400[#](<#bittensor.utils.btlogging.defines.DEFAULT_MAX_ROTATING_LOG_FILE_SIZE> "Link to this definition")
    

bittensor.utils.btlogging.defines.TRACE_LOG_FORMAT = '%(asctime)s | %(levelname)s | %(name)s:%(filename)s:%(lineno)s | %(message)s'[#](<#bittensor.utils.btlogging.defines.TRACE_LOG_FORMAT> "Link to this definition")
    

[ __ previous bittensor.utils.btlogging.console ](<../console/index.html> "previous page") [ next bittensor.utils.btlogging.format __](<../format/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Module Contents](<#module-contents>)
    * [`BASE_LOG_FORMAT`](<#bittensor.utils.btlogging.defines.BASE_LOG_FORMAT>)
    * [`BITTENSOR_LOGGER_NAME`](<#bittensor.utils.btlogging.defines.BITTENSOR_LOGGER_NAME>)
    * [`DATE_FORMAT`](<#bittensor.utils.btlogging.defines.DATE_FORMAT>)
    * [`DEFAULT_LOG_BACKUP_COUNT`](<#bittensor.utils.btlogging.defines.DEFAULT_LOG_BACKUP_COUNT>)
    * [`DEFAULT_LOG_FILE_NAME`](<#bittensor.utils.btlogging.defines.DEFAULT_LOG_FILE_NAME>)
    * [`DEFAULT_MAX_ROTATING_LOG_FILE_SIZE`](<#bittensor.utils.btlogging.defines.DEFAULT_MAX_ROTATING_LOG_FILE_SIZE>)
    * [`TRACE_LOG_FORMAT`](<#bittensor.utils.btlogging.defines.TRACE_LOG_FORMAT>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.