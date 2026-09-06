# bittensor.core.chain_data.prometheus_info &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/prometheus_info/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/prometheus_info/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/prometheus_info/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.prometheus_info

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`PrometheusInfo`](<#bittensor.core.chain_data.prometheus_info.PrometheusInfo>)
      * [`PrometheusInfo.block`](<#bittensor.core.chain_data.prometheus_info.PrometheusInfo.block>)
      * [`PrometheusInfo.ip`](<#bittensor.core.chain_data.prometheus_info.PrometheusInfo.ip>)
      * [`PrometheusInfo.ip_type`](<#bittensor.core.chain_data.prometheus_info.PrometheusInfo.ip_type>)
      * [`PrometheusInfo.port`](<#bittensor.core.chain_data.prometheus_info.PrometheusInfo.port>)
      * [`PrometheusInfo.version`](<#bittensor.core.chain_data.prometheus_info.PrometheusInfo.version>)



# bittensor.core.chain_data.prometheus_info[#](<#module-bittensor.core.chain_data.prometheus_info> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`PrometheusInfo`](<#bittensor.core.chain_data.prometheus_info.PrometheusInfo> "bittensor.core.chain_data.prometheus_info.PrometheusInfo") | Dataclass representing information related to Prometheus.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.prometheus_info.PrometheusInfo[#](<#bittensor.core.chain_data.prometheus_info.PrometheusInfo> "Link to this definition")
    

Bases: [`bittensor.core.chain_data.info_base.InfoBase`](<../info_base/index.html#bittensor.core.chain_data.info_base.InfoBase> "bittensor.core.chain_data.info_base.InfoBase")

Dataclass representing information related to Prometheus.

Variables:
    

  * **block** – The block number associated with the Prometheus data.

  * **version** – The version of the Prometheus data.

  * **ip** – The IP address associated with Prometheus.

  * **port** – The port number for Prometheus.

  * **ip_type** – The type of IP address (e.g., IPv4, IPv6).




block: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.prometheus_info.PrometheusInfo.block> "Link to this definition")
    

ip: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.prometheus_info.PrometheusInfo.ip> "Link to this definition")
    

ip_type: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.prometheus_info.PrometheusInfo.ip_type> "Link to this definition")
    

port: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.prometheus_info.PrometheusInfo.port> "Link to this definition")
    

version: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.prometheus_info.PrometheusInfo.version> "Link to this definition")
    

[ __ previous bittensor.core.chain_data.neuron_info_lite ](<../neuron_info_lite/index.html> "previous page") [ next bittensor.core.chain_data.proposal_vote_data __](<../proposal_vote_data/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`PrometheusInfo`](<#bittensor.core.chain_data.prometheus_info.PrometheusInfo>)
      * [`PrometheusInfo.block`](<#bittensor.core.chain_data.prometheus_info.PrometheusInfo.block>)
      * [`PrometheusInfo.ip`](<#bittensor.core.chain_data.prometheus_info.PrometheusInfo.ip>)
      * [`PrometheusInfo.ip_type`](<#bittensor.core.chain_data.prometheus_info.PrometheusInfo.ip_type>)
      * [`PrometheusInfo.port`](<#bittensor.core.chain_data.prometheus_info.PrometheusInfo.port>)
      * [`PrometheusInfo.version`](<#bittensor.core.chain_data.prometheus_info.PrometheusInfo.version>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.