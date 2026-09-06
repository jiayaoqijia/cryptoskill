# bittensor.utils.networking &#8212; Bittensor SDK Docs  documentation

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
        * [bittensor.utils.networking](<#>)
        * [bittensor.utils.registration](<../registration/index.html>)
        * [bittensor.utils.subnets](<../subnets/index.html>)
        * [bittensor.utils.version](<../version/index.html>)
        * [bittensor.utils.weight_utils](<../weight_utils/index.html>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/utils/networking/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/utils/networking/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/utils/networking/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.utils.networking

##  Contents 

  * [Exceptions](<#exceptions>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`ExternalIPNotFound`](<#bittensor.utils.networking.ExternalIPNotFound>)
    * [`get_external_ip()`](<#bittensor.utils.networking.get_external_ip>)
    * [`get_formatted_ws_endpoint_url()`](<#bittensor.utils.networking.get_formatted_ws_endpoint_url>)
    * [`int_to_ip()`](<#bittensor.utils.networking.int_to_ip>)
    * [`ip__str__()`](<#bittensor.utils.networking.ip__str__>)
    * [`ip_to_int()`](<#bittensor.utils.networking.ip_to_int>)
    * [`ip_version()`](<#bittensor.utils.networking.ip_version>)



# bittensor.utils.networking[#](<#module-bittensor.utils.networking> "Link to this heading")

Utils for handling local network with ip and ports.

## Exceptions[#](<#exceptions> "Link to this heading")

[`ExternalIPNotFound`](<#bittensor.utils.networking.ExternalIPNotFound> "bittensor.utils.networking.ExternalIPNotFound") | Raised if we cannot attain your external ip from CURL/URLLIB/IPIFY/AWS  
---|---  
  
## Functions[#](<#functions> "Link to this heading")

[`get_external_ip`](<#bittensor.utils.networking.get_external_ip> "bittensor.utils.networking.get_external_ip")() | Checks CURL/URLLIB/IPIFY/AWS for your external ip.  
---|---  
[`get_formatted_ws_endpoint_url`](<#bittensor.utils.networking.get_formatted_ws_endpoint_url> "bittensor.utils.networking.get_formatted_ws_endpoint_url")(endpoint_url) | Returns a formatted websocket endpoint url.  
[`int_to_ip`](<#bittensor.utils.networking.int_to_ip> "bittensor.utils.networking.int_to_ip")(int_val) | Maps an integer to a unique ip-string  
[`ip__str__`](<#bittensor.utils.networking.ip__str__> "bittensor.utils.networking.ip__str__")(ip_type, ip_str, port) | Return a formatted ip string  
[`ip_to_int`](<#bittensor.utils.networking.ip_to_int> "bittensor.utils.networking.ip_to_int")(str_val) | Maps an ip-string to a unique integer.  
[`ip_version`](<#bittensor.utils.networking.ip_version> "bittensor.utils.networking.ip_version")(str_val) | Returns the ip version (IPV4 or IPV6).  
  
## Module Contents[#](<#module-contents> "Link to this heading")

exception bittensor.utils.networking.ExternalIPNotFound[#](<#bittensor.utils.networking.ExternalIPNotFound> "Link to this definition")
    

Bases: [`Exception`](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)")

Raised if we cannot attain your external ip from CURL/URLLIB/IPIFY/AWS

Initialize self. See help(type(self)) for accurate signature.

bittensor.utils.networking.get_external_ip()[#](<#bittensor.utils.networking.get_external_ip> "Link to this definition")
    

Checks CURL/URLLIB/IPIFY/AWS for your external ip.

Returns:
    

Your routers external facing ip as a string.

Return type:
    

[external_ip](<../../core/axon/index.html#bittensor.core.axon.Axon.external_ip> "bittensor.core.axon.Axon.external_ip") ([str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

Raises:
    

[**ExternalIPNotFound**](<#bittensor.utils.networking.ExternalIPNotFound> "bittensor.utils.networking.ExternalIPNotFound")**(**[**Exception**](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)")**)** – Raised if all external ip attempts fail.

bittensor.utils.networking.get_formatted_ws_endpoint_url(_endpoint_url_)[#](<#bittensor.utils.networking.get_formatted_ws_endpoint_url> "Link to this definition")
    

Returns a formatted websocket endpoint url.

Parameters:
    

**endpoint_url** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The endpoint url to format.

Returns:
    

The formatted endpoint url. In the form of ws://<endpoint_url> or wss://<endpoint_url>

Return type:
    

formatted_endpoint_url

Note: The port (or lack thereof) is left unchanged.

bittensor.utils.networking.int_to_ip(_int_val_)[#](<#bittensor.utils.networking.int_to_ip> "Link to this definition")
    

Maps an integer to a unique ip-string

Parameters:
    

**int_val** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The integer representation of an ip. Must be in the range (0, 3.4028237e+38).

Returns:
    

The string representation of an ip. Of form _._.*.* for ipv4 or _::_ :_:_ :* for ipv6

Return type:
    

str_val

bittensor.utils.networking.ip__str__(_ip_type_ , _ip_str_ , _port_)[#](<#bittensor.utils.networking.ip__str__> "Link to this definition")
    

Return a formatted ip string

Parameters:
    

  * **ip_type** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

  * **ip_str** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

  * **port** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))




bittensor.utils.networking.ip_to_int(_str_val_)[#](<#bittensor.utils.networking.ip_to_int> "Link to this definition")
    

Maps an ip-string to a unique integer.

Parameters:
    

**str_val** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The string representation of an ip. Of form _._.*.* for ipv4 or _::_ :_:_ :* for ipv6

Returns:
    

The integer representation of an ip. Must be in the range (0, 3.4028237e+38).

Return type:
    

int_val

bittensor.utils.networking.ip_version(_str_val_)[#](<#bittensor.utils.networking.ip_version> "Link to this definition")
    

Returns the ip version (IPV4 or IPV6).

Parameters:
    

**str_val** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The string representation of an ip. Of form _._.*.* for ipv4 or _::_ :_:_ :* for ipv6

Returns:
    

The ip version (Either 4 or 6 for IPv4/IPv6)

Return type:
    

int_val

[ __ previous bittensor.utils.liquidity ](<../liquidity/index.html> "previous page") [ next bittensor.utils.registration __](<../registration/index.html> "next page")

__Contents

  * [Exceptions](<#exceptions>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`ExternalIPNotFound`](<#bittensor.utils.networking.ExternalIPNotFound>)
    * [`get_external_ip()`](<#bittensor.utils.networking.get_external_ip>)
    * [`get_formatted_ws_endpoint_url()`](<#bittensor.utils.networking.get_formatted_ws_endpoint_url>)
    * [`int_to_ip()`](<#bittensor.utils.networking.int_to_ip>)
    * [`ip__str__()`](<#bittensor.utils.networking.ip__str__>)
    * [`ip_to_int()`](<#bittensor.utils.networking.ip_to_int>)
    * [`ip_version()`](<#bittensor.utils.networking.ip_version>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.