# bittensor.core.chain_data.ip_info &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/ip_info/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/ip_info/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/ip_info/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.ip_info

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`IPInfo`](<#bittensor.core.chain_data.ip_info.IPInfo>)
      * [`IPInfo.encode()`](<#bittensor.core.chain_data.ip_info.IPInfo.encode>)
      * [`IPInfo.from_parameter_dict()`](<#bittensor.core.chain_data.ip_info.IPInfo.from_parameter_dict>)
      * [`IPInfo.ip`](<#bittensor.core.chain_data.ip_info.IPInfo.ip>)
      * [`IPInfo.ip_type`](<#bittensor.core.chain_data.ip_info.IPInfo.ip_type>)
      * [`IPInfo.protocol`](<#bittensor.core.chain_data.ip_info.IPInfo.protocol>)
      * [`IPInfo.to_parameter_dict()`](<#bittensor.core.chain_data.ip_info.IPInfo.to_parameter_dict>)



# bittensor.core.chain_data.ip_info[#](<#module-bittensor.core.chain_data.ip_info> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`IPInfo`](<#bittensor.core.chain_data.ip_info.IPInfo> "bittensor.core.chain_data.ip_info.IPInfo") | Dataclass representing IP information.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.ip_info.IPInfo[#](<#bittensor.core.chain_data.ip_info.IPInfo> "Link to this definition")
    

Dataclass representing IP information.

Variables:
    

  * **ip** – The IP address as a string.

  * **ip_type** – The type of the IP address (e.g., IPv4, IPv6).

  * **protocol** – The protocol associated with the IP (e.g., TCP, UDP).




encode()[#](<#bittensor.core.chain_data.ip_info.IPInfo.encode> "Link to this definition")
    

Returns a dictionary of the IPInfo object that can be encoded.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [Any](<../proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any")]

classmethod from_parameter_dict(_parameter_dict_)[#](<#bittensor.core.chain_data.ip_info.IPInfo.from_parameter_dict> "Link to this definition")
    

Creates a IPInfo instance from a parameter dictionary.

Parameters:
    

**parameter_dict** (_Union_ _[_[_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_Any_](<../proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any") _]__,__bittensor.utils.registration.torch.nn.ParameterDict_ _]_)

Return type:
    

[IPInfo](<#bittensor.core.chain_data.ip_info.IPInfo> "bittensor.core.chain_data.ip_info.IPInfo")

ip: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.ip_info.IPInfo.ip> "Link to this definition")
    

ip_type: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.ip_info.IPInfo.ip_type> "Link to this definition")
    

protocol: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.ip_info.IPInfo.protocol> "Link to this definition")
    

to_parameter_dict()[#](<#bittensor.core.chain_data.ip_info.IPInfo.to_parameter_dict> "Link to this definition")
    

Returns a torch tensor or dict of the subnet IP info.

Return type:
    

Union[[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), Union[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]], bittensor.utils.registration.torch.nn.ParameterDict]

[ __ previous bittensor.core.chain_data.info_base ](<../info_base/index.html> "previous page") [ next bittensor.core.chain_data.metagraph_info __](<../metagraph_info/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`IPInfo`](<#bittensor.core.chain_data.ip_info.IPInfo>)
      * [`IPInfo.encode()`](<#bittensor.core.chain_data.ip_info.IPInfo.encode>)
      * [`IPInfo.from_parameter_dict()`](<#bittensor.core.chain_data.ip_info.IPInfo.from_parameter_dict>)
      * [`IPInfo.ip`](<#bittensor.core.chain_data.ip_info.IPInfo.ip>)
      * [`IPInfo.ip_type`](<#bittensor.core.chain_data.ip_info.IPInfo.ip_type>)
      * [`IPInfo.protocol`](<#bittensor.core.chain_data.ip_info.IPInfo.protocol>)
      * [`IPInfo.to_parameter_dict()`](<#bittensor.core.chain_data.ip_info.IPInfo.to_parameter_dict>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.