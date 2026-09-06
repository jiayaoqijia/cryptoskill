# bittensor.core.chain_data.chain_identity &#8212; Bittensor SDK Docs  documentation

[Skip to main content](<#main-content>)

__Back to top __ `Ctrl`+`K`

[ ![Bittensor SDK Docs  documentation - Home](../../../../../_static/logo.svg) ![Bittensor SDK Docs  documentation - Home](../../../../../_static/logo-dark-mode.svg) ](<../../../../../index.html>)

__ Search `Ctrl`+`K`

Table of Contents

  * [API Reference](<../../../../index.html>) __
    * [bittensor](<../../../index.html>) __
      * [bittensor.core](<../../index.html>) __
        * [bittensor.core.async_subtensor](<../../async_subtensor/index.html>)
        * [bittensor.core.axon](<../../axon/index.html>)
        * [bittensor.core.chain_data](<../index.html>)
        * [bittensor.core.config](<../../config/index.html>)
        * [bittensor.core.dendrite](<../../dendrite/index.html>)
        * [bittensor.core.errors](<../../errors/index.html>)
        * [bittensor.core.extrinsics](<../../extrinsics/index.html>)
        * [bittensor.core.metagraph](<../../metagraph/index.html>)
        * [bittensor.core.settings](<../../settings/index.html>)
        * [bittensor.core.stream](<../../stream/index.html>)
        * [bittensor.core.subtensor](<../../subtensor/index.html>)
        * [bittensor.core.synapse](<../../synapse/index.html>)
        * [bittensor.core.tensor](<../../tensor/index.html>)
        * [bittensor.core.threadpool](<../../threadpool/index.html>)
        * [bittensor.core.types](<../../types/index.html>)
      * [bittensor.extras](<../../../extras/index.html>) __
        * [bittensor.extras.dev_framework](<../../../extras/dev_framework/index.html>)
        * [bittensor.extras.subtensor_api](<../../../extras/subtensor_api/index.html>)
        * [bittensor.extras.timelock](<../../../extras/timelock/index.html>)
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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/chain_identity/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/chain_identity/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/chain_identity/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.chain_identity

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`ChainIdentity`](<#bittensor.core.chain_data.chain_identity.ChainIdentity>)
      * [`ChainIdentity.additional`](<#bittensor.core.chain_data.chain_identity.ChainIdentity.additional>)
      * [`ChainIdentity.description`](<#bittensor.core.chain_data.chain_identity.ChainIdentity.description>)
      * [`ChainIdentity.discord`](<#bittensor.core.chain_data.chain_identity.ChainIdentity.discord>)
      * [`ChainIdentity.github`](<#bittensor.core.chain_data.chain_identity.ChainIdentity.github>)
      * [`ChainIdentity.image`](<#bittensor.core.chain_data.chain_identity.ChainIdentity.image>)
      * [`ChainIdentity.name`](<#bittensor.core.chain_data.chain_identity.ChainIdentity.name>)
      * [`ChainIdentity.url`](<#bittensor.core.chain_data.chain_identity.ChainIdentity.url>)



# bittensor.core.chain_data.chain_identity[#](<#module-bittensor.core.chain_data.chain_identity> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`ChainIdentity`](<#bittensor.core.chain_data.chain_identity.ChainIdentity> "bittensor.core.chain_data.chain_identity.ChainIdentity") | Dataclass for chain identity information.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.chain_identity.ChainIdentity[#](<#bittensor.core.chain_data.chain_identity.ChainIdentity> "Link to this definition")
    

Bases: [`bittensor.core.chain_data.info_base.InfoBase`](<../info_base/index.html#bittensor.core.chain_data.info_base.InfoBase> "bittensor.core.chain_data.info_base.InfoBase")

Dataclass for chain identity information.

additional: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.chain_identity.ChainIdentity.additional> "Link to this definition")
    

description: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.chain_identity.ChainIdentity.description> "Link to this definition")
    

discord: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.chain_identity.ChainIdentity.discord> "Link to this definition")
    

github: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.chain_identity.ChainIdentity.github> "Link to this definition")
    

image: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.chain_identity.ChainIdentity.image> "Link to this definition")
    

name: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.chain_identity.ChainIdentity.name> "Link to this definition")
    

url: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.chain_identity.ChainIdentity.url> "Link to this definition")
    

[ __ previous bittensor.core.chain_data.axon_info ](<../axon_info/index.html> "previous page") [ next bittensor.core.chain_data.coldkey_swap __](<../coldkey_swap/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`ChainIdentity`](<#bittensor.core.chain_data.chain_identity.ChainIdentity>)
      * [`ChainIdentity.additional`](<#bittensor.core.chain_data.chain_identity.ChainIdentity.additional>)
      * [`ChainIdentity.description`](<#bittensor.core.chain_data.chain_identity.ChainIdentity.description>)
      * [`ChainIdentity.discord`](<#bittensor.core.chain_data.chain_identity.ChainIdentity.discord>)
      * [`ChainIdentity.github`](<#bittensor.core.chain_data.chain_identity.ChainIdentity.github>)
      * [`ChainIdentity.image`](<#bittensor.core.chain_data.chain_identity.ChainIdentity.image>)
      * [`ChainIdentity.name`](<#bittensor.core.chain_data.chain_identity.ChainIdentity.name>)
      * [`ChainIdentity.url`](<#bittensor.core.chain_data.chain_identity.ChainIdentity.url>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.