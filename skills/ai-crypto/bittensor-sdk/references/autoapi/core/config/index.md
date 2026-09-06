# bittensor.core.config &#8212; Bittensor SDK Docs  documentation

[Skip to main content](<#main-content>)

__Back to top __ `Ctrl`+`K`

[ ![Bittensor SDK Docs  documentation - Home](../../../../_static/logo.svg) ![Bittensor SDK Docs  documentation - Home](../../../../_static/logo-dark-mode.svg) ](<../../../../index.html>)

__ Search `Ctrl`+`K`

Table of Contents

  * [API Reference](<../../../index.html>) __
    * [bittensor](<../../index.html>) __
      * [bittensor.core](<../index.html>) __
        * [bittensor.core.async_subtensor](<../async_subtensor/index.html>)
        * [bittensor.core.axon](<../axon/index.html>)
        * [bittensor.core.chain_data](<../chain_data/index.html>)
        * [bittensor.core.config](<#>)
        * [bittensor.core.dendrite](<../dendrite/index.html>)
        * [bittensor.core.errors](<../errors/index.html>)
        * [bittensor.core.extrinsics](<../extrinsics/index.html>)
        * [bittensor.core.metagraph](<../metagraph/index.html>)
        * [bittensor.core.settings](<../settings/index.html>)
        * [bittensor.core.stream](<../stream/index.html>)
        * [bittensor.core.subtensor](<../subtensor/index.html>)
        * [bittensor.core.synapse](<../synapse/index.html>)
        * [bittensor.core.tensor](<../tensor/index.html>)
        * [bittensor.core.threadpool](<../threadpool/index.html>)
        * [bittensor.core.types](<../types/index.html>)
      * [bittensor.extras](<../../extras/index.html>) __
        * [bittensor.extras.dev_framework](<../../extras/dev_framework/index.html>)
        * [bittensor.extras.subtensor_api](<../../extras/subtensor_api/index.html>)
        * [bittensor.extras.timelock](<../../extras/timelock/index.html>)
      * [bittensor.utils](<../../utils/index.html>) __
        * [bittensor.utils.axon_utils](<../../utils/axon_utils/index.html>)
        * [bittensor.utils.balance](<../../utils/balance/index.html>)
        * [bittensor.utils.btlogging](<../../utils/btlogging/index.html>)
        * [bittensor.utils.easy_imports](<../../utils/easy_imports/index.html>)
        * [bittensor.utils.formatting](<../../utils/formatting/index.html>)
        * [bittensor.utils.liquidity](<../../utils/liquidity/index.html>)
        * [bittensor.utils.networking](<../../utils/networking/index.html>)
        * [bittensor.utils.registration](<../../utils/registration/index.html>)
        * [bittensor.utils.subnets](<../../utils/subnets/index.html>)
        * [bittensor.utils.version](<../../utils/version/index.html>)
        * [bittensor.utils.weight_utils](<../../utils/weight_utils/index.html>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/config/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/config/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/core/config/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.config

##  Contents 

  * [Exceptions](<#exceptions>)
  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Config`](<#bittensor.core.config.Config>)
      * [`Config.is_set()`](<#bittensor.core.config.Config.is_set>)
      * [`Config.merge()`](<#bittensor.core.config.Config.merge>)
      * [`Config.to_dict()`](<#bittensor.core.config.Config.to_dict>)
    * [`DefaultMunch`](<#bittensor.core.config.DefaultMunch>)
      * [`DefaultMunch.fromDict()`](<#bittensor.core.config.DefaultMunch.fromDict>)
      * [`DefaultMunch.toDict()`](<#bittensor.core.config.DefaultMunch.toDict>)
    * [`InvalidConfigFile`](<#bittensor.core.config.InvalidConfigFile>)



# bittensor.core.config[#](<#module-bittensor.core.config> "Link to this heading")

Implementation of the config class, which manages the configuration of different Bittensor modules.

Example

import argparse import bittensor as bt

parser = argparse.ArgumentParser(‘Miner’) bt.Axon.add_args(parser) bt.Subtensor.add_args(parser) bt.Async_subtensor.add_args(parser) bt.Wallet.add_args(parser) bt.logging.add_args(parser) bt.PriorityThreadPoolExecutor.add_args(parser) config = bt.config(parser)

print(config)

## Exceptions[#](<#exceptions> "Link to this heading")

[`InvalidConfigFile`](<#bittensor.core.config.InvalidConfigFile> "bittensor.core.config.InvalidConfigFile") | Raised when there's an error loading the config file.  
---|---  
  
## Classes[#](<#classes> "Link to this heading")

[`Config`](<#bittensor.core.config.Config> "bittensor.core.config.Config") | Manages configuration for Bittensor modules with nested namespace support.  
---|---  
[`DefaultMunch`](<#bittensor.core.config.DefaultMunch> "bittensor.core.config.DefaultMunch") | Dict with attribute-style access and a configurable default value.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.config.Config(_parser =None_, _args =None_, _strict =False_, _default =DEFAULTS_)[#](<#bittensor.core.config.Config> "Link to this definition")
    

Bases: [`DefaultMunch`](<#bittensor.core.config.DefaultMunch> "bittensor.core.config.DefaultMunch")

Manages configuration for Bittensor modules with nested namespace support.

Initialize self. See help(type(self)) for accurate signature.

Parameters:
    

  * **parser** ([_argparse.ArgumentParser_](<https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser> "\(in Python v3.14\)"))

  * **args** (_Optional_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]__]_)

  * **strict** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **default** ([_Any_](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any"))




is_set(_param_name_)[#](<#bittensor.core.config.Config.is_set> "Link to this definition")
    

Checks if a parameter was explicitly set.

Parameters:
    

**param_name** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

merge(_other_)[#](<#bittensor.core.config.Config.merge> "Link to this definition")
    

Merges another Config into this one.

Parameters:
    

**other** ([_Config_](<#bittensor.core.config.Config> "bittensor.core.config.Config"))

Return type:
    

None

to_dict()[#](<#bittensor.core.config.Config.to_dict> "Link to this definition")
    

Returns the configuration as a dictionary.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")

class bittensor.core.config.DefaultMunch(_default =None_, _* args_, _** kwargs_)[#](<#bittensor.core.config.DefaultMunch> "Link to this definition")
    

Bases: [`dict`](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")

Dict with attribute-style access and a configurable default value.

Drop-in replacement for munch.DefaultMunch using only the stdlib. The default value (returned for missing keys) is stored on the instance via `object.__setattr__` so it never collides with dict entries.

Initialize self. See help(type(self)) for accurate signature.

classmethod fromDict(_d_ , __default =None_)[#](<#bittensor.core.config.DefaultMunch.fromDict> "Link to this definition")
    

Recursively creates a DefaultMunch from a plain dict.

toDict()[#](<#bittensor.core.config.DefaultMunch.toDict> "Link to this definition")
    

Recursively converts this object to a plain dict.

exception bittensor.core.config.InvalidConfigFile[#](<#bittensor.core.config.InvalidConfigFile> "Link to this definition")
    

Bases: [`Exception`](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)")

Raised when there’s an error loading the config file.

Initialize self. See help(type(self)) for accurate signature.

[ __ previous bittensor.core.chain_data.weight_commit_info ](<../chain_data/weight_commit_info/index.html> "previous page") [ next bittensor.core.dendrite __](<../dendrite/index.html> "next page")

__Contents

  * [Exceptions](<#exceptions>)
  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Config`](<#bittensor.core.config.Config>)
      * [`Config.is_set()`](<#bittensor.core.config.Config.is_set>)
      * [`Config.merge()`](<#bittensor.core.config.Config.merge>)
      * [`Config.to_dict()`](<#bittensor.core.config.Config.to_dict>)
    * [`DefaultMunch`](<#bittensor.core.config.DefaultMunch>)
      * [`DefaultMunch.fromDict()`](<#bittensor.core.config.DefaultMunch.fromDict>)
      * [`DefaultMunch.toDict()`](<#bittensor.core.config.DefaultMunch.toDict>)
    * [`InvalidConfigFile`](<#bittensor.core.config.InvalidConfigFile>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.