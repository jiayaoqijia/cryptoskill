# bittensor.utils.version &#8212; Bittensor SDK Docs  documentation

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
        * [bittensor.utils.axon_utils](<../axon_utils/index.html>)
        * [bittensor.utils.balance](<../balance/index.html>)
        * [bittensor.utils.btlogging](<../btlogging/index.html>)
        * [bittensor.utils.easy_imports](<../easy_imports/index.html>)
        * [bittensor.utils.formatting](<../formatting/index.html>)
        * [bittensor.utils.liquidity](<../liquidity/index.html>)
        * [bittensor.utils.networking](<../networking/index.html>)
        * [bittensor.utils.registration](<../registration/index.html>)
        * [bittensor.utils.subnets](<../subnets/index.html>)
        * [bittensor.utils.version](<#>)
        * [bittensor.utils.weight_utils](<../weight_utils/index.html>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/utils/version/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/utils/version/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/utils/version/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.utils.version

##  Contents 

  * [Attributes](<#attributes>)
  * [Exceptions](<#exceptions>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`VERSION_CHECK_THRESHOLD`](<#bittensor.utils.version.VERSION_CHECK_THRESHOLD>)
    * [`VersionCheckError`](<#bittensor.utils.version.VersionCheckError>)
    * [`check_latest_version_in_pypi()`](<#bittensor.utils.version.check_latest_version_in_pypi>)
    * [`check_version()`](<#bittensor.utils.version.check_version>)
    * [`get_and_save_latest_version()`](<#bittensor.utils.version.get_and_save_latest_version>)



# bittensor.utils.version[#](<#module-bittensor.utils.version> "Link to this heading")

## Attributes[#](<#attributes> "Link to this heading")

[`VERSION_CHECK_THRESHOLD`](<#bittensor.utils.version.VERSION_CHECK_THRESHOLD> "bittensor.utils.version.VERSION_CHECK_THRESHOLD") |   
---|---  
  
## Exceptions[#](<#exceptions> "Link to this heading")

[`VersionCheckError`](<#bittensor.utils.version.VersionCheckError> "bittensor.utils.version.VersionCheckError") | Exception raised for errors in the version check process.  
---|---  
  
## Functions[#](<#functions> "Link to this heading")

[`check_latest_version_in_pypi`](<#bittensor.utils.version.check_latest_version_in_pypi> "bittensor.utils.version.check_latest_version_in_pypi")() | Check for the latest version of the package on PyPI.  
---|---  
[`check_version`](<#bittensor.utils.version.check_version> "bittensor.utils.version.check_version")([timeout]) | Check if the current version of Bittensor is up-to-date with the latest version on PyPi.  
[`get_and_save_latest_version`](<#bittensor.utils.version.get_and_save_latest_version> "bittensor.utils.version.get_and_save_latest_version")([timeout]) | Retrieves and saves the latest version of Bittensor.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

bittensor.utils.version.VERSION_CHECK_THRESHOLD = 86400[#](<#bittensor.utils.version.VERSION_CHECK_THRESHOLD> "Link to this definition")
    

exception bittensor.utils.version.VersionCheckError[#](<#bittensor.utils.version.VersionCheckError> "Link to this definition")
    

Bases: [`Exception`](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)")

Exception raised for errors in the version check process.

Initialize self. See help(type(self)) for accurate signature.

bittensor.utils.version.check_latest_version_in_pypi()[#](<#bittensor.utils.version.check_latest_version_in_pypi> "Link to this definition")
    

Check for the latest version of the package on PyPI.

bittensor.utils.version.check_version(_timeout =15_)[#](<#bittensor.utils.version.check_version> "Link to this definition")
    

Check if the current version of Bittensor is up-to-date with the latest version on PyPi. Raises a VersionCheckError if the version check fails.

Parameters:
    

**timeout** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The timeout for the request to PyPI in seconds.

bittensor.utils.version.get_and_save_latest_version(_timeout =15_)[#](<#bittensor.utils.version.get_and_save_latest_version> "Link to this definition")
    

Retrieves and saves the latest version of Bittensor.

Parameters:
    

**timeout** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The timeout for the request to PyPI in seconds.

Returns:
    

The latest version of Bittensor.

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

[ __ previous bittensor.utils.subnets ](<../subnets/index.html> "previous page") [ next bittensor.utils.weight_utils __](<../weight_utils/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Exceptions](<#exceptions>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`VERSION_CHECK_THRESHOLD`](<#bittensor.utils.version.VERSION_CHECK_THRESHOLD>)
    * [`VersionCheckError`](<#bittensor.utils.version.VersionCheckError>)
    * [`check_latest_version_in_pypi()`](<#bittensor.utils.version.check_latest_version_in_pypi>)
    * [`check_version()`](<#bittensor.utils.version.check_version>)
    * [`get_and_save_latest_version()`](<#bittensor.utils.version.get_and_save_latest_version>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.