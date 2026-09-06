# bittensor.extras.subtensor_api.proxy &#8212; Bittensor SDK Docs  documentation

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
        * [bittensor.extras.dev_framework](<../../dev_framework/index.html>)
        * [bittensor.extras.subtensor_api](<../index.html>)
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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/extras/subtensor_api/proxy/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/extras/subtensor_api/proxy/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/extras/subtensor_api/proxy/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.extras.subtensor_api.proxy

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Proxy`](<#bittensor.extras.subtensor_api.proxy.Proxy>)
      * [`Proxy.add_proxy`](<#bittensor.extras.subtensor_api.proxy.Proxy.add_proxy>)
      * [`Proxy.announce_proxy`](<#bittensor.extras.subtensor_api.proxy.Proxy.announce_proxy>)
      * [`Proxy.create_pure_proxy`](<#bittensor.extras.subtensor_api.proxy.Proxy.create_pure_proxy>)
      * [`Proxy.get_proxies`](<#bittensor.extras.subtensor_api.proxy.Proxy.get_proxies>)
      * [`Proxy.get_proxies_for_real_account`](<#bittensor.extras.subtensor_api.proxy.Proxy.get_proxies_for_real_account>)
      * [`Proxy.get_proxy_announcement`](<#bittensor.extras.subtensor_api.proxy.Proxy.get_proxy_announcement>)
      * [`Proxy.get_proxy_announcements`](<#bittensor.extras.subtensor_api.proxy.Proxy.get_proxy_announcements>)
      * [`Proxy.get_proxy_constants`](<#bittensor.extras.subtensor_api.proxy.Proxy.get_proxy_constants>)
      * [`Proxy.kill_pure_proxy`](<#bittensor.extras.subtensor_api.proxy.Proxy.kill_pure_proxy>)
      * [`Proxy.poke_deposit`](<#bittensor.extras.subtensor_api.proxy.Proxy.poke_deposit>)
      * [`Proxy.proxy`](<#bittensor.extras.subtensor_api.proxy.Proxy.proxy>)
      * [`Proxy.proxy_announced`](<#bittensor.extras.subtensor_api.proxy.Proxy.proxy_announced>)
      * [`Proxy.reject_proxy_announcement`](<#bittensor.extras.subtensor_api.proxy.Proxy.reject_proxy_announcement>)
      * [`Proxy.remove_proxies`](<#bittensor.extras.subtensor_api.proxy.Proxy.remove_proxies>)
      * [`Proxy.remove_proxy`](<#bittensor.extras.subtensor_api.proxy.Proxy.remove_proxy>)
      * [`Proxy.remove_proxy_announcement`](<#bittensor.extras.subtensor_api.proxy.Proxy.remove_proxy_announcement>)



# bittensor.extras.subtensor_api.proxy[#](<#module-bittensor.extras.subtensor_api.proxy> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`Proxy`](<#bittensor.extras.subtensor_api.proxy.Proxy> "bittensor.extras.subtensor_api.proxy.Proxy") | Class for managing proxy operations on the Bittensor network.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.extras.subtensor_api.proxy.Proxy(_subtensor_)[#](<#bittensor.extras.subtensor_api.proxy.Proxy> "Link to this definition")
    

Class for managing proxy operations on the Bittensor network.

This class provides access to all proxy-related operations, including creating and managing both standard and pure proxy relationships, handling proxy announcements, and querying proxy data. It works with both synchronous Subtensor and asynchronous AsyncSubtensor instances.

Proxies enable secure delegation of account permissions by allowing a delegate account to perform certain operations on behalf of a real account, with restrictions defined by the proxy type and optional time-lock delays.

Notes

  * For comprehensive documentation on proxies, see: <<https://docs.learnbittensor.org/keys/proxies>>

  * For creating and managing proxies, see: <<https://docs.learnbittensor.org/keys/proxies/create-proxy>>

  * For pure proxy documentation, see: <<https://docs.learnbittensor.org/keys/proxies/pure-proxies>>

  * For available proxy types and their permissions, see: <<https://docs.learnbittensor.org/keys/proxies#types-of-proxies>>




Parameters:
    

**subtensor** (_Union_ _[_[_bittensor.core.subtensor.Subtensor_](<../../../core/subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor") _,_[_bittensor.core.async_subtensor.AsyncSubtensor_](<../../../core/async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor> "bittensor.core.async_subtensor.AsyncSubtensor") _]_)

add_proxy[#](<#bittensor.extras.subtensor_api.proxy.Proxy.add_proxy> "Link to this definition")
    

announce_proxy[#](<#bittensor.extras.subtensor_api.proxy.Proxy.announce_proxy> "Link to this definition")
    

create_pure_proxy[#](<#bittensor.extras.subtensor_api.proxy.Proxy.create_pure_proxy> "Link to this definition")
    

get_proxies[#](<#bittensor.extras.subtensor_api.proxy.Proxy.get_proxies> "Link to this definition")
    

get_proxies_for_real_account[#](<#bittensor.extras.subtensor_api.proxy.Proxy.get_proxies_for_real_account> "Link to this definition")
    

get_proxy_announcement[#](<#bittensor.extras.subtensor_api.proxy.Proxy.get_proxy_announcement> "Link to this definition")
    

get_proxy_announcements[#](<#bittensor.extras.subtensor_api.proxy.Proxy.get_proxy_announcements> "Link to this definition")
    

get_proxy_constants[#](<#bittensor.extras.subtensor_api.proxy.Proxy.get_proxy_constants> "Link to this definition")
    

kill_pure_proxy[#](<#bittensor.extras.subtensor_api.proxy.Proxy.kill_pure_proxy> "Link to this definition")
    

poke_deposit[#](<#bittensor.extras.subtensor_api.proxy.Proxy.poke_deposit> "Link to this definition")
    

proxy[#](<#bittensor.extras.subtensor_api.proxy.Proxy.proxy> "Link to this definition")
    

proxy_announced[#](<#bittensor.extras.subtensor_api.proxy.Proxy.proxy_announced> "Link to this definition")
    

reject_proxy_announcement[#](<#bittensor.extras.subtensor_api.proxy.Proxy.reject_proxy_announcement> "Link to this definition")
    

remove_proxies[#](<#bittensor.extras.subtensor_api.proxy.Proxy.remove_proxies> "Link to this definition")
    

remove_proxy[#](<#bittensor.extras.subtensor_api.proxy.Proxy.remove_proxy> "Link to this definition")
    

remove_proxy_announcement[#](<#bittensor.extras.subtensor_api.proxy.Proxy.remove_proxy_announcement> "Link to this definition")
    

[ __ previous bittensor.extras.subtensor_api.neurons ](<../neurons/index.html> "previous page") [ next bittensor.extras.subtensor_api.queries __](<../queries/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`Proxy`](<#bittensor.extras.subtensor_api.proxy.Proxy>)
      * [`Proxy.add_proxy`](<#bittensor.extras.subtensor_api.proxy.Proxy.add_proxy>)
      * [`Proxy.announce_proxy`](<#bittensor.extras.subtensor_api.proxy.Proxy.announce_proxy>)
      * [`Proxy.create_pure_proxy`](<#bittensor.extras.subtensor_api.proxy.Proxy.create_pure_proxy>)
      * [`Proxy.get_proxies`](<#bittensor.extras.subtensor_api.proxy.Proxy.get_proxies>)
      * [`Proxy.get_proxies_for_real_account`](<#bittensor.extras.subtensor_api.proxy.Proxy.get_proxies_for_real_account>)
      * [`Proxy.get_proxy_announcement`](<#bittensor.extras.subtensor_api.proxy.Proxy.get_proxy_announcement>)
      * [`Proxy.get_proxy_announcements`](<#bittensor.extras.subtensor_api.proxy.Proxy.get_proxy_announcements>)
      * [`Proxy.get_proxy_constants`](<#bittensor.extras.subtensor_api.proxy.Proxy.get_proxy_constants>)
      * [`Proxy.kill_pure_proxy`](<#bittensor.extras.subtensor_api.proxy.Proxy.kill_pure_proxy>)
      * [`Proxy.poke_deposit`](<#bittensor.extras.subtensor_api.proxy.Proxy.poke_deposit>)
      * [`Proxy.proxy`](<#bittensor.extras.subtensor_api.proxy.Proxy.proxy>)
      * [`Proxy.proxy_announced`](<#bittensor.extras.subtensor_api.proxy.Proxy.proxy_announced>)
      * [`Proxy.reject_proxy_announcement`](<#bittensor.extras.subtensor_api.proxy.Proxy.reject_proxy_announcement>)
      * [`Proxy.remove_proxies`](<#bittensor.extras.subtensor_api.proxy.Proxy.remove_proxies>)
      * [`Proxy.remove_proxy`](<#bittensor.extras.subtensor_api.proxy.Proxy.remove_proxy>)
      * [`Proxy.remove_proxy_announcement`](<#bittensor.extras.subtensor_api.proxy.Proxy.remove_proxy_announcement>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.