# bittensor.extras.dev_framework.calls &#8212; Bittensor SDK Docs  documentation

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
      * [bittensor.extras](<../../index.html>) __
        * [bittensor.extras.dev_framework](<../index.html>)
        * [bittensor.extras.subtensor_api](<../../subtensor_api/index.html>)
        * [bittensor.extras.timelock](<../../timelock/index.html>)
      * [bittensor.utils](<../../../utils/index.html>) __
        * [bittensor.utils.axon_utils](<../../../utils/axon_utils/index.html>)
        * [bittensor.utils.balance](<../../../utils/balance/index.html>)
        * [bittensor.utils.btlogging](<../../../utils/btlogging/index.html>)
        * [bittensor.utils.easy_imports](<../../../utils/easy_imports/index.html>)
        * [bittensor.utils.formatting](<../../../utils/formatting/index.html>)
        * [bittensor.utils.liquidity](<../../../utils/liquidity/index.html>)
        * [bittensor.utils.networking](<../../../utils/networking/index.html>)
        * [bittensor.utils.registration](<../../../utils/registration/index.html>)
        * [bittensor.utils.subnets](<../../../utils/subnets/index.html>)
        * [bittensor.utils.version](<../../../utils/version/index.html>)
        * [bittensor.utils.weight_utils](<../../../utils/weight_utils/index.html>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/extras/dev_framework/calls/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/extras/dev_framework/calls/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/extras/dev_framework/calls/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.extras.dev_framework.calls

##  Contents 

  * [Submodules](<#submodules>)
  * [Attributes](<#attributes>)
  * [Functions](<#functions>)
  * [Package Contents](<#package-contents>)
    * [`HEADER`](<#bittensor.extras.dev_framework.calls.HEADER>)
    * [`IMPORT_TEXT`](<#bittensor.extras.dev_framework.calls.IMPORT_TEXT>)
    * [`recreate_calls_subpackage()`](<#bittensor.extras.dev_framework.calls.recreate_calls_subpackage>)



# bittensor.extras.dev_framework.calls[#](<#module-bittensor.extras.dev_framework.calls> "Link to this heading")

This module serves primarily as a reference and auxiliary resource for developers.

Although any command can be constructed directly within a test without relying on the pre-generated call definitions, the provided command lists (divided into sudo and non-sudo categories), together with the pallet reference, significantly streamline the creation of accurate, maintainable, and well-structured end-to-end tests.

In practice, these definitions act as convenient blueprints for composing extrinsic calls and understanding the structure of available Subtensor operations.

## Submodules[#](<#submodules> "Link to this heading")

  * [bittensor.extras.dev_framework.calls.non_sudo_calls](<non_sudo_calls/index.html>)
  * [bittensor.extras.dev_framework.calls.pallets](<pallets/index.html>)
  * [bittensor.extras.dev_framework.calls.sudo_calls](<sudo_calls/index.html>)



## Attributes[#](<#attributes> "Link to this heading")

[`HEADER`](<#bittensor.extras.dev_framework.calls.HEADER> "bittensor.extras.dev_framework.calls.HEADER") |   
---|---  
[`IMPORT_TEXT`](<#bittensor.extras.dev_framework.calls.IMPORT_TEXT> "bittensor.extras.dev_framework.calls.IMPORT_TEXT") |   
  
## Functions[#](<#functions> "Link to this heading")

[`recreate_calls_subpackage`](<#bittensor.extras.dev_framework.calls.recreate_calls_subpackage> "bittensor.extras.dev_framework.calls.recreate_calls_subpackage")([network]) | Fetch the list of pallets and their call and save them to the corresponding modules.  
---|---  
  
## Package Contents[#](<#package-contents> "Link to this heading")

bittensor.extras.dev_framework.calls.HEADER = Multiline-String[#](<#bittensor.extras.dev_framework.calls.HEADER> "Link to this definition")
    Show Value
[code]
    """"""
    This file is auto-generated. Do not edit manually.
    
    For developers:
    - Use the function `recreate_calls_subpackage()` to regenerate this file.
    - The command lists are built dynamically from the current Subtensor metadata (`Subtensor.substrate.metadata`).
    - Each command is represented as a `namedtuple` with fields:
        * System arguments: wallet, pallet (and `sudo` for sudo calls).
        * Additional arguments: taken from the extrinsic definition (with type hints for reference).
    - These namedtuples are intended as convenient templates for building commands in tests and end-to-end scenarios.
    
    Note:
        Any manual changes will be overwritten the next time the generator is run.
    """
    
[/code]

bittensor.extras.dev_framework.calls.IMPORT_TEXT = Multiline-String[#](<#bittensor.extras.dev_framework.calls.IMPORT_TEXT> "Link to this definition")
    Show Value
[code]
    """
    """
    
    from collections import namedtuple
    
    
    """
    
[/code]

bittensor.extras.dev_framework.calls.recreate_calls_subpackage(_network ='local'_)[#](<#bittensor.extras.dev_framework.calls.recreate_calls_subpackage> "Link to this definition")
    

Fetch the list of pallets and their call and save them to the corresponding modules.

[ __ previous bittensor.extras.dev_framework ](<../index.html> "previous page") [ next bittensor.extras.dev_framework.calls.non_sudo_calls __](<non_sudo_calls/index.html> "next page")

__Contents

  * [Submodules](<#submodules>)
  * [Attributes](<#attributes>)
  * [Functions](<#functions>)
  * [Package Contents](<#package-contents>)
    * [`HEADER`](<#bittensor.extras.dev_framework.calls.HEADER>)
    * [`IMPORT_TEXT`](<#bittensor.extras.dev_framework.calls.IMPORT_TEXT>)
    * [`recreate_calls_subpackage()`](<#bittensor.extras.dev_framework.calls.recreate_calls_subpackage>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.