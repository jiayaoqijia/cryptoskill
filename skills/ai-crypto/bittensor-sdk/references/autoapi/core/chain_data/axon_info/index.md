# bittensor.core.chain_data.axon_info &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/axon_info/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/axon_info/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/axon_info/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.axon_info

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`AxonInfo`](<#bittensor.core.chain_data.axon_info.AxonInfo>)
      * [`AxonInfo.coldkey`](<#bittensor.core.chain_data.axon_info.AxonInfo.coldkey>)
      * [`AxonInfo.from_neuron_info()`](<#bittensor.core.chain_data.axon_info.AxonInfo.from_neuron_info>)
      * [`AxonInfo.from_parameter_dict()`](<#bittensor.core.chain_data.axon_info.AxonInfo.from_parameter_dict>)
      * [`AxonInfo.from_string()`](<#bittensor.core.chain_data.axon_info.AxonInfo.from_string>)
      * [`AxonInfo.hotkey`](<#bittensor.core.chain_data.axon_info.AxonInfo.hotkey>)
      * [`AxonInfo.ip`](<#bittensor.core.chain_data.axon_info.AxonInfo.ip>)
      * [`AxonInfo.ip_str()`](<#bittensor.core.chain_data.axon_info.AxonInfo.ip_str>)
      * [`AxonInfo.ip_type`](<#bittensor.core.chain_data.axon_info.AxonInfo.ip_type>)
      * [`AxonInfo.is_serving`](<#bittensor.core.chain_data.axon_info.AxonInfo.is_serving>)
      * [`AxonInfo.placeholder1`](<#bittensor.core.chain_data.axon_info.AxonInfo.placeholder1>)
      * [`AxonInfo.placeholder2`](<#bittensor.core.chain_data.axon_info.AxonInfo.placeholder2>)
      * [`AxonInfo.port`](<#bittensor.core.chain_data.axon_info.AxonInfo.port>)
      * [`AxonInfo.protocol`](<#bittensor.core.chain_data.axon_info.AxonInfo.protocol>)
      * [`AxonInfo.to_parameter_dict()`](<#bittensor.core.chain_data.axon_info.AxonInfo.to_parameter_dict>)
      * [`AxonInfo.to_string()`](<#bittensor.core.chain_data.axon_info.AxonInfo.to_string>)
      * [`AxonInfo.version`](<#bittensor.core.chain_data.axon_info.AxonInfo.version>)



# bittensor.core.chain_data.axon_info[#](<#module-bittensor.core.chain_data.axon_info> "Link to this heading")

This module defines the AxonInfo class, a data structure used to represent information about an axon endpoint in the bittensor network.

## Classes[#](<#classes> "Link to this heading")

[`AxonInfo`](<#bittensor.core.chain_data.axon_info.AxonInfo> "bittensor.core.chain_data.axon_info.AxonInfo") | The AxonInfo class represents information about an axon endpoint in the bittensor network. This includes  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.axon_info.AxonInfo[#](<#bittensor.core.chain_data.axon_info.AxonInfo> "Link to this definition")
    

Bases: [`bittensor.core.chain_data.info_base.InfoBase`](<../info_base/index.html#bittensor.core.chain_data.info_base.InfoBase> "bittensor.core.chain_data.info_base.InfoBase")

The AxonInfo class represents information about an axon endpoint in the bittensor network. This includes properties such as IP address, ports, and relevant keys.

Variables:
    

  * **version** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The version of the axon endpoint.

  * **ip** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The IP address of the axon endpoint.

  * **port** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The port number the axon endpoint uses.

  * **ip_type** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The type of IP protocol (e.g., IPv4 or IPv6).

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The hotkey associated with the axon endpoint.

  * **coldkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The coldkey associated with the axon endpoint.

  * **protocol** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The protocol version (default is 4).

  * **placeholder1** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Reserved field (default is 0).

  * **placeholder2** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Reserved field (default is 0).




coldkey: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.axon_info.AxonInfo.coldkey> "Link to this definition")
    

classmethod from_neuron_info(_neuron_info_)[#](<#bittensor.core.chain_data.axon_info.AxonInfo.from_neuron_info> "Link to this definition")
    

Converts a dictionary to an AxonInfo object.

Parameters:
    

**neuron_info** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")) – A dictionary containing the neuron information.

Returns:
    

An instance of AxonInfo created from the dictionary.

Return type:
    

[AxonInfo](<#bittensor.core.chain_data.axon_info.AxonInfo> "bittensor.core.chain_data.axon_info.AxonInfo")

classmethod from_parameter_dict(_parameter_dict_)[#](<#bittensor.core.chain_data.axon_info.AxonInfo.from_parameter_dict> "Link to this definition")
    

Returns an axon_info object from a torch parameter_dict or a parameter dict.

Parameters:
    

**parameter_dict** (_Union_ _[_[_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_Any_](<../proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any") _]__,__bittensor.utils.registration.torch.nn.ParameterDict_ _]_)

Return type:
    

[AxonInfo](<#bittensor.core.chain_data.axon_info.AxonInfo> "bittensor.core.chain_data.axon_info.AxonInfo")

classmethod from_string(_json_string_)[#](<#bittensor.core.chain_data.axon_info.AxonInfo.from_string> "Link to this definition")
    

Creates an AxonInfo object from its string representation using JSON.

Parameters:
    

**json_string** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The JSON string representation of the AxonInfo object.

Returns:
    

An instance of AxonInfo created from the JSON string. If decoding fails, returns a default AxonInfo` object
    

with default values.

Raises:
    

  * [**json.JSONDecodeError**](<https://docs.python.org/3/library/json.html#json.JSONDecodeError> "\(in Python v3.14\)") – If there is an error in decoding the JSON string.

  * [**TypeError**](<https://docs.python.org/3/library/exceptions.html#TypeError> "\(in Python v3.14\)") – If there is a type error when creating the AxonInfo object.

  * [**ValueError**](<https://docs.python.org/3/library/exceptions.html#ValueError> "\(in Python v3.14\)") – If there is a value error when creating the AxonInfo object.



Return type:
    

[AxonInfo](<#bittensor.core.chain_data.axon_info.AxonInfo> "bittensor.core.chain_data.axon_info.AxonInfo")

hotkey: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.axon_info.AxonInfo.hotkey> "Link to this definition")
    

ip: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.axon_info.AxonInfo.ip> "Link to this definition")
    

ip_str()[#](<#bittensor.core.chain_data.axon_info.AxonInfo.ip_str> "Link to this definition")
    

Return the whole IP as string

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

ip_type: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.axon_info.AxonInfo.ip_type> "Link to this definition")
    

property is_serving: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.axon_info.AxonInfo.is_serving> "Link to this definition")
    

True if the endpoint is serving.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

placeholder1: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") = 0[#](<#bittensor.core.chain_data.axon_info.AxonInfo.placeholder1> "Link to this definition")
    

placeholder2: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") = 0[#](<#bittensor.core.chain_data.axon_info.AxonInfo.placeholder2> "Link to this definition")
    

port: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.axon_info.AxonInfo.port> "Link to this definition")
    

protocol: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") = 4[#](<#bittensor.core.chain_data.axon_info.AxonInfo.protocol> "Link to this definition")
    

to_parameter_dict()[#](<#bittensor.core.chain_data.axon_info.AxonInfo.to_parameter_dict> "Link to this definition")
    

Returns a torch tensor or dict of the subnet info, depending on the USE_TORCH flag set.

Return type:
    

Union[[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), Union[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]], bittensor.utils.registration.torch.nn.ParameterDict]

to_string()[#](<#bittensor.core.chain_data.axon_info.AxonInfo.to_string> "Link to this definition")
    

Converts the AxonInfo object to a string representation using JSON.

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

version: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.axon_info.AxonInfo.version> "Link to this definition")
    

[ __ previous bittensor.core.chain_data ](<../index.html> "previous page") [ next bittensor.core.chain_data.chain_identity __](<../chain_identity/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`AxonInfo`](<#bittensor.core.chain_data.axon_info.AxonInfo>)
      * [`AxonInfo.coldkey`](<#bittensor.core.chain_data.axon_info.AxonInfo.coldkey>)
      * [`AxonInfo.from_neuron_info()`](<#bittensor.core.chain_data.axon_info.AxonInfo.from_neuron_info>)
      * [`AxonInfo.from_parameter_dict()`](<#bittensor.core.chain_data.axon_info.AxonInfo.from_parameter_dict>)
      * [`AxonInfo.from_string()`](<#bittensor.core.chain_data.axon_info.AxonInfo.from_string>)
      * [`AxonInfo.hotkey`](<#bittensor.core.chain_data.axon_info.AxonInfo.hotkey>)
      * [`AxonInfo.ip`](<#bittensor.core.chain_data.axon_info.AxonInfo.ip>)
      * [`AxonInfo.ip_str()`](<#bittensor.core.chain_data.axon_info.AxonInfo.ip_str>)
      * [`AxonInfo.ip_type`](<#bittensor.core.chain_data.axon_info.AxonInfo.ip_type>)
      * [`AxonInfo.is_serving`](<#bittensor.core.chain_data.axon_info.AxonInfo.is_serving>)
      * [`AxonInfo.placeholder1`](<#bittensor.core.chain_data.axon_info.AxonInfo.placeholder1>)
      * [`AxonInfo.placeholder2`](<#bittensor.core.chain_data.axon_info.AxonInfo.placeholder2>)
      * [`AxonInfo.port`](<#bittensor.core.chain_data.axon_info.AxonInfo.port>)
      * [`AxonInfo.protocol`](<#bittensor.core.chain_data.axon_info.AxonInfo.protocol>)
      * [`AxonInfo.to_parameter_dict()`](<#bittensor.core.chain_data.axon_info.AxonInfo.to_parameter_dict>)
      * [`AxonInfo.to_string()`](<#bittensor.core.chain_data.axon_info.AxonInfo.to_string>)
      * [`AxonInfo.version`](<#bittensor.core.chain_data.axon_info.AxonInfo.version>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.