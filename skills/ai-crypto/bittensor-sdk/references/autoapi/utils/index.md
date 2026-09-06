# bittensor.utils &#8212; Bittensor SDK Docs  documentation

[Skip to main content](<#main-content>)

__Back to top __ `Ctrl`+`K`

[ ![Bittensor SDK Docs  documentation - Home](../../../_static/logo.svg) ![Bittensor SDK Docs  documentation - Home](../../../_static/logo-dark-mode.svg) ](<../../../index.html>)

__ Search `Ctrl`+`K`

Table of Contents

  * [API Reference](<../../index.html>) __
    * [bittensor](<../index.html>) __
      * [bittensor.core](<../core/index.html>) __
        * [bittensor.core.async_subtensor](<../core/async_subtensor/index.html>)
        * [bittensor.core.axon](<../core/axon/index.html>)
        * [bittensor.core.chain_data](<../core/chain_data/index.html>)
        * [bittensor.core.config](<../core/config/index.html>)
        * [bittensor.core.dendrite](<../core/dendrite/index.html>)
        * [bittensor.core.errors](<../core/errors/index.html>)
        * [bittensor.core.extrinsics](<../core/extrinsics/index.html>)
        * [bittensor.core.metagraph](<../core/metagraph/index.html>)
        * [bittensor.core.settings](<../core/settings/index.html>)
        * [bittensor.core.stream](<../core/stream/index.html>)
        * [bittensor.core.subtensor](<../core/subtensor/index.html>)
        * [bittensor.core.synapse](<../core/synapse/index.html>)
        * [bittensor.core.tensor](<../core/tensor/index.html>)
        * [bittensor.core.threadpool](<../core/threadpool/index.html>)
        * [bittensor.core.types](<../core/types/index.html>)
      * [bittensor.extras](<../extras/index.html>) __
        * [bittensor.extras.dev_framework](<../extras/dev_framework/index.html>)
        * [bittensor.extras.subtensor_api](<../extras/subtensor_api/index.html>)
        * [bittensor.extras.timelock](<../extras/timelock/index.html>)
      * [bittensor.utils](<#>) __
        * [bittensor.utils.axon_utils](<axon_utils/index.html>)
        * [bittensor.utils.balance](<balance/index.html>)
        * [bittensor.utils.btlogging](<btlogging/index.html>)
        * [bittensor.utils.easy_imports](<easy_imports/index.html>)
        * [bittensor.utils.formatting](<formatting/index.html>)
        * [bittensor.utils.liquidity](<liquidity/index.html>)
        * [bittensor.utils.networking](<networking/index.html>)
        * [bittensor.utils.registration](<registration/index.html>)
        * [bittensor.utils.subnets](<subnets/index.html>)
        * [bittensor.utils.version](<version/index.html>)
        * [bittensor.utils.weight_utils](<weight_utils/index.html>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/utils/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/utils/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../_sources/autoapi/bittensor/utils/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.utils

##  Contents 

  * [Submodules](<#submodules>)
  * [Attributes](<#attributes>)
  * [Exceptions](<#exceptions>)
  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Package Contents](<#package-contents>)
    * [`BT_DOCS_LINK`](<#bittensor.utils.BT_DOCS_LINK>)
    * [`Certificate`](<#bittensor.utils.Certificate>)
    * [`ChainFeatureDisabledWarning`](<#bittensor.utils.ChainFeatureDisabledWarning>)
    * [`GLOBAL_MAX_SUBNET_COUNT`](<#bittensor.utils.GLOBAL_MAX_SUBNET_COUNT>)
    * [`RAOPERTAO`](<#bittensor.utils.RAOPERTAO>)
    * [`U16_MAX`](<#bittensor.utils.U16_MAX>)
    * [`U64_MAX`](<#bittensor.utils.U64_MAX>)
    * [`UnlockStatus`](<#bittensor.utils.UnlockStatus>)
      * [`UnlockStatus.message`](<#bittensor.utils.UnlockStatus.message>)
      * [`UnlockStatus.success`](<#bittensor.utils.UnlockStatus.success>)
    * [`VersionCheckError`](<#bittensor.utils.VersionCheckError>)
    * [`check_version`](<#bittensor.utils.check_version>)
    * [`decode_hex_identity_dict()`](<#bittensor.utils.decode_hex_identity_dict>)
    * [`deprecated_message()`](<#bittensor.utils.deprecated_message>)
    * [`determine_chain_endpoint_and_network()`](<#bittensor.utils.determine_chain_endpoint_and_network>)
    * [`float_to_u64()`](<#bittensor.utils.float_to_u64>)
    * [`format_error_message()`](<#bittensor.utils.format_error_message>)
    * [`get_caller_name()`](<#bittensor.utils.get_caller_name>)
    * [`get_explorer_url_for_network()`](<#bittensor.utils.get_explorer_url_for_network>)
    * [`get_function_name()`](<#bittensor.utils.get_function_name>)
    * [`get_hash()`](<#bittensor.utils.get_hash>)
    * [`get_mechid_storage_index()`](<#bittensor.utils.get_mechid_storage_index>)
    * [`get_netuid_and_mechid_by_storage_index()`](<#bittensor.utils.get_netuid_and_mechid_by_storage_index>)
    * [`hex_to_bytes`](<#bittensor.utils.hex_to_bytes>)
    * [`hex_to_ss58`](<#bittensor.utils.hex_to_ss58>)
    * [`is_valid_bittensor_address_or_public_key()`](<#bittensor.utils.is_valid_bittensor_address_or_public_key>)
    * [`is_valid_ss58_address()`](<#bittensor.utils.is_valid_ss58_address>)
    * [`logging`](<#bittensor.utils.logging>)
    * [`ss58_address_to_bytes()`](<#bittensor.utils.ss58_address_to_bytes>)
    * [`ss58_decode`](<#bittensor.utils.ss58_decode>)
    * [`ss58_to_hex`](<#bittensor.utils.ss58_to_hex>)
    * [`ss58_to_vec_u8()`](<#bittensor.utils.ss58_to_vec_u8>)
    * [`strtobool()`](<#bittensor.utils.strtobool>)
    * [`torch`](<#bittensor.utils.torch>)
    * [`u16_normalized_float()`](<#bittensor.utils.u16_normalized_float>)
    * [`u64_normalized_float()`](<#bittensor.utils.u64_normalized_float>)
    * [`unlock_key()`](<#bittensor.utils.unlock_key>)
    * [`use_torch`](<#bittensor.utils.use_torch>)
    * [`validate_chain_endpoint()`](<#bittensor.utils.validate_chain_endpoint>)
    * [`validate_max_attempts()`](<#bittensor.utils.validate_max_attempts>)



# bittensor.utils[#](<#module-bittensor.utils> "Link to this heading")

## Submodules[#](<#submodules> "Link to this heading")

  * [bittensor.utils.axon_utils](<axon_utils/index.html>)
  * [bittensor.utils.balance](<balance/index.html>)
  * [bittensor.utils.btlogging](<btlogging/index.html>)
  * [bittensor.utils.easy_imports](<easy_imports/index.html>)
  * [bittensor.utils.formatting](<formatting/index.html>)
  * [bittensor.utils.liquidity](<liquidity/index.html>)
  * [bittensor.utils.networking](<networking/index.html>)
  * [bittensor.utils.registration](<registration/index.html>)
  * [bittensor.utils.subnets](<subnets/index.html>)
  * [bittensor.utils.version](<version/index.html>)
  * [bittensor.utils.weight_utils](<weight_utils/index.html>)



## Attributes[#](<#attributes> "Link to this heading")

[`BT_DOCS_LINK`](<#bittensor.utils.BT_DOCS_LINK> "bittensor.utils.BT_DOCS_LINK") |   
---|---  
[`GLOBAL_MAX_SUBNET_COUNT`](<#bittensor.utils.GLOBAL_MAX_SUBNET_COUNT> "bittensor.utils.GLOBAL_MAX_SUBNET_COUNT") |   
[`RAOPERTAO`](<#bittensor.utils.RAOPERTAO> "bittensor.utils.RAOPERTAO") |   
[`U16_MAX`](<#bittensor.utils.U16_MAX> "bittensor.utils.U16_MAX") |   
[`U64_MAX`](<#bittensor.utils.U64_MAX> "bittensor.utils.U64_MAX") |   
[`VersionCheckError`](<#bittensor.utils.VersionCheckError> "bittensor.utils.VersionCheckError") |   
[`check_version`](<#bittensor.utils.check_version> "bittensor.utils.check_version") |   
[`hex_to_bytes`](<#bittensor.utils.hex_to_bytes> "bittensor.utils.hex_to_bytes") |   
[`hex_to_ss58`](<#bittensor.utils.hex_to_ss58> "bittensor.utils.hex_to_ss58") |   
[`logging`](<#bittensor.utils.logging> "bittensor.utils.logging") |   
[`ss58_decode`](<#bittensor.utils.ss58_decode> "bittensor.utils.ss58_decode") |   
[`ss58_to_hex`](<#bittensor.utils.ss58_to_hex> "bittensor.utils.ss58_to_hex") |   
[`torch`](<#bittensor.utils.torch> "bittensor.utils.torch") |   
[`use_torch`](<#bittensor.utils.use_torch> "bittensor.utils.use_torch") |   
  
## Exceptions[#](<#exceptions> "Link to this heading")

[`ChainFeatureDisabledWarning`](<#bittensor.utils.ChainFeatureDisabledWarning> "bittensor.utils.ChainFeatureDisabledWarning") | Warning indicating that a feature is currently disabled on the chain side.  
---|---  
  
## Classes[#](<#classes> "Link to this heading")

[`Certificate`](<#bittensor.utils.Certificate> "bittensor.utils.Certificate") | str(object='') -> str  
---|---  
[`UnlockStatus`](<#bittensor.utils.UnlockStatus> "bittensor.utils.UnlockStatus") |   
  
## Functions[#](<#functions> "Link to this heading")

[`decode_hex_identity_dict`](<#bittensor.utils.decode_hex_identity_dict> "bittensor.utils.decode_hex_identity_dict")(info_dictionary) | Decodes a dictionary of hexadecimal identities.  
---|---  
[`deprecated_message`](<#bittensor.utils.deprecated_message> "bittensor.utils.deprecated_message")([message, replacement_message, ...]) | Shows a warning message with the given message.  
[`determine_chain_endpoint_and_network`](<#bittensor.utils.determine_chain_endpoint_and_network> "bittensor.utils.determine_chain_endpoint_and_network")(network) | Determines the chain endpoint and network from the passed network or chain_endpoint.  
[`float_to_u64`](<#bittensor.utils.float_to_u64> "bittensor.utils.float_to_u64")(value) | Converts a float to a u64 int  
[`format_error_message`](<#bittensor.utils.format_error_message> "bittensor.utils.format_error_message")(error_message) | Formats an error message from the Subtensor error information for use in extrinsics.  
[`get_caller_name`](<#bittensor.utils.get_caller_name> "bittensor.utils.get_caller_name")([depth]) | Return the name of the caller function.  
[`get_explorer_url_for_network`](<#bittensor.utils.get_explorer_url_for_network> "bittensor.utils.get_explorer_url_for_network")(network, block_hash, ...) | Returns the explorer url for the given block hash and network.  
[`get_function_name`](<#bittensor.utils.get_function_name> "bittensor.utils.get_function_name")() | Return the current function's name.  
[`get_hash`](<#bittensor.utils.get_hash> "bittensor.utils.get_hash")(content[, encoding]) |   
[`get_mechid_storage_index`](<#bittensor.utils.get_mechid_storage_index> "bittensor.utils.get_mechid_storage_index")(netuid, mechid) | Computes the storage index for a given netuid and mechid pair.  
[`get_netuid_and_mechid_by_storage_index`](<#bittensor.utils.get_netuid_and_mechid_by_storage_index> "bittensor.utils.get_netuid_and_mechid_by_storage_index")(storage_index) | Returns the netuid and mechid from the storage index.  
[`is_valid_bittensor_address_or_public_key`](<#bittensor.utils.is_valid_bittensor_address_or_public_key> "bittensor.utils.is_valid_bittensor_address_or_public_key")(address) | Checks if the given address is a valid destination address.  
[`is_valid_ss58_address`](<#bittensor.utils.is_valid_ss58_address> "bittensor.utils.is_valid_ss58_address")(address) | Checks if the given address is a valid ss58 address.  
[`ss58_address_to_bytes`](<#bittensor.utils.ss58_address_to_bytes> "bittensor.utils.ss58_address_to_bytes")(ss58_address) | Converts a ss58 address to a bytes object.  
[`ss58_to_vec_u8`](<#bittensor.utils.ss58_to_vec_u8> "bittensor.utils.ss58_to_vec_u8")(ss58_address) |   
[`strtobool`](<#bittensor.utils.strtobool> "bittensor.utils.strtobool")(val) | Converts a string to a boolean value.  
[`u16_normalized_float`](<#bittensor.utils.u16_normalized_float> "bittensor.utils.u16_normalized_float")(x) |   
[`u64_normalized_float`](<#bittensor.utils.u64_normalized_float> "bittensor.utils.u64_normalized_float")(x) |   
[`unlock_key`](<#bittensor.utils.unlock_key> "bittensor.utils.unlock_key")(wallet[, unlock_type, raise_error]) | Attempts to decrypt a wallet's coldkey or hotkey  
[`validate_chain_endpoint`](<#bittensor.utils.validate_chain_endpoint> "bittensor.utils.validate_chain_endpoint")(endpoint_url) | Validates if the provided endpoint URL is a valid WebSocket URL.  
[`validate_max_attempts`](<#bittensor.utils.validate_max_attempts> "bittensor.utils.validate_max_attempts")(max_attempts, response) | Common guard for all subtensor methods with max_attempts parameter.  
  
## Package Contents[#](<#package-contents> "Link to this heading")

bittensor.utils.BT_DOCS_LINK = 'https://docs.bittensor.com'[#](<#bittensor.utils.BT_DOCS_LINK> "Link to this definition")
    

class bittensor.utils.Certificate[#](<#bittensor.utils.Certificate> "Link to this definition")
    

Bases: [`str`](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

str(object=’’) -> str str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or errors is specified, then the object must expose a data buffer that will be decoded using the given encoding and error handler. Otherwise, returns the result of object.__str__() (if defined) or repr(object). encoding defaults to ‘utf-8’. errors defaults to ‘strict’.

Initialize self. See help(type(self)) for accurate signature.

exception bittensor.utils.ChainFeatureDisabledWarning[#](<#bittensor.utils.ChainFeatureDisabledWarning> "Link to this definition")
    

Bases: [`UserWarning`](<https://docs.python.org/3/library/exceptions.html#UserWarning> "\(in Python v3.14\)")

Warning indicating that a feature is currently disabled on the chain side.

This warning is issued when SDK functionality depends on chain feats that are temporarily unavailable or disabled.

Initialize self. See help(type(self)) for accurate signature.

bittensor.utils.GLOBAL_MAX_SUBNET_COUNT = 4096[#](<#bittensor.utils.GLOBAL_MAX_SUBNET_COUNT> "Link to this definition")
    

bittensor.utils.RAOPERTAO = 1000000000.0[#](<#bittensor.utils.RAOPERTAO> "Link to this definition")
    

bittensor.utils.U16_MAX = 65535[#](<#bittensor.utils.U16_MAX> "Link to this definition")
    

bittensor.utils.U64_MAX = 18446744073709551615[#](<#bittensor.utils.U64_MAX> "Link to this definition")
    

class bittensor.utils.UnlockStatus[#](<#bittensor.utils.UnlockStatus> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

message[#](<#bittensor.utils.UnlockStatus.message> "Link to this definition")
    

success[#](<#bittensor.utils.UnlockStatus.success> "Link to this definition")
    

bittensor.utils.VersionCheckError[#](<#bittensor.utils.VersionCheckError> "Link to this definition")
    

bittensor.utils.check_version[#](<#bittensor.utils.check_version> "Link to this definition")
    

bittensor.utils.decode_hex_identity_dict(_info_dictionary_)[#](<#bittensor.utils.decode_hex_identity_dict> "Link to this definition")
    

Decodes a dictionary of hexadecimal identities.

Parameters:
    

**info_dictionary** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)") _|_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_)

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [Any](<../core/chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any")]

bittensor.utils.deprecated_message(_message =None_, _replacement_message =None_, _category =DeprecationWarning_, _stacklevel =2_)[#](<#bittensor.utils.deprecated_message> "Link to this definition")
    

Shows a warning message with the given message.

Parameters:
    

  * **message** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The warning message to display. If None, a default deprecation message is generated.

  * **replacement_message** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – An optional additional message suggesting a replacement.

  * **category** (_Type_ _[_[_Warning_](<btlogging/loggingmachine/index.html#bittensor.utils.btlogging.loggingmachine.LoggingMachine.Warning> "bittensor.utils.btlogging.loggingmachine.LoggingMachine.Warning") _]_) – The warning category to use. Defaults to DeprecationWarning.

  * **stacklevel** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The stack level for the warning. Defaults to 2 (points to the caller of deprecated_message). Increase this value if deprecated_message is called from within another wrapper function.



Return type:
    

None

bittensor.utils.determine_chain_endpoint_and_network(_network_)[#](<#bittensor.utils.determine_chain_endpoint_and_network> "Link to this definition")
    

Determines the chain endpoint and network from the passed network or chain_endpoint.

Parameters:
    

**network** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The network flag. The choices are: `finney` (main network), `archive` (archive network +300 blocks), `local` (local running network), `test` (test network).

Returns:
    

The network and chain endpoint flag. If passed, overrides the `network` argument.

Return type:
    

[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[Optional[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")], Optional[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]]

bittensor.utils.float_to_u64(_value_)[#](<#bittensor.utils.float_to_u64> "Link to this definition")
    

Converts a float to a u64 int

Parameters:
    

**value** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

bittensor.utils.format_error_message(_error_message_)[#](<#bittensor.utils.format_error_message> "Link to this definition")
    

Formats an error message from the Subtensor error information for use in extrinsics.

Parameters:
    

**error_message** (_Union_ _[_[_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)") _,_[_Exception_](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)") _]_) – A dictionary containing the error information from Subtensor, or a SubstrateRequestException containing dictionary literal args.

Returns:
    

A formatted error message string.

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

bittensor.utils.get_caller_name(_depth =2_)[#](<#bittensor.utils.get_caller_name> "Link to this definition")
    

Return the name of the caller function.

Parameters:
    

**depth** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

bittensor.utils.get_explorer_url_for_network(_network_ , _block_hash_ , _network_map_)[#](<#bittensor.utils.get_explorer_url_for_network> "Link to this definition")
    

Returns the explorer url for the given block hash and network.

Parameters:
    

  * **network** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The network to get the explorer url for.

  * **block_hash** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The block hash to get the explorer url for.

  * **network_map** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]__]_) – The network maps to get the explorer urls from.



Returns:
    

The explorer url for the given block hash and network. Or None if the network is not known.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]

bittensor.utils.get_function_name()[#](<#bittensor.utils.get_function_name> "Link to this definition")
    

Return the current function’s name.

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

bittensor.utils.get_hash(_content_ , _encoding ='utf-8'_)[#](<#bittensor.utils.get_hash> "Link to this definition")
    

bittensor.utils.get_mechid_storage_index(_netuid_ , _mechid_)[#](<#bittensor.utils.get_mechid_storage_index> "Link to this definition")
    

Computes the storage index for a given netuid and mechid pair.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The netuid of the subnet.

  * **mechid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The mechid of the subnet.



Returns:
    

Storage index number for the subnet and mechanism id.

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

bittensor.utils.get_netuid_and_mechid_by_storage_index(_storage_index_)[#](<#bittensor.utils.get_netuid_and_mechid_by_storage_index> "Link to this definition")
    

Returns the netuid and mechid from the storage index.

Chain APIs (e.g., SubMetagraph response) returns netuid which is storage index that encodes both the netuid and mechid. This function reverses the encoding to extract these components.

Parameters:
    

**storage_index** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The storage index of the subnet.

Returns:
    

  * netuid - subnet identifier.

  * mechid - mechanism identifier.




Return type:
    

[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

bittensor.utils.hex_to_bytes[#](<#bittensor.utils.hex_to_bytes> "Link to this definition")
    

bittensor.utils.hex_to_ss58[#](<#bittensor.utils.hex_to_ss58> "Link to this definition")
    

bittensor.utils.is_valid_bittensor_address_or_public_key(_address_)[#](<#bittensor.utils.is_valid_bittensor_address_or_public_key> "Link to this definition")
    

Checks if the given address is a valid destination address.

Parameters:
    

**address** (_Union_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _,_[_bytes_](<../extras/dev_framework/calls/non_sudo_calls/index.html#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes> "bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes") _]_) – The address to check.

Returns:
    

True if the address is a valid destination address, False otherwise.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

bittensor.utils.is_valid_ss58_address(_address_)[#](<#bittensor.utils.is_valid_ss58_address> "Link to this definition")
    

Checks if the given address is a valid ss58 address.

Parameters:
    

**address** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The address to check.

Returns:
    

True if the address is a valid ss58 address for Bittensor, False otherwise.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

bittensor.utils.logging[#](<#bittensor.utils.logging> "Link to this definition")
    

bittensor.utils.ss58_address_to_bytes(_ss58_address_)[#](<#bittensor.utils.ss58_address_to_bytes> "Link to this definition")
    

Converts a ss58 address to a bytes object.

Parameters:
    

**ss58_address** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

Return type:
    

[bytes](<../extras/dev_framework/calls/non_sudo_calls/index.html#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes> "bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes")

bittensor.utils.ss58_decode[#](<#bittensor.utils.ss58_decode> "Link to this definition")
    

bittensor.utils.ss58_to_hex[#](<#bittensor.utils.ss58_to_hex> "Link to this definition")
    

bittensor.utils.ss58_to_vec_u8(_ss58_address_)[#](<#bittensor.utils.ss58_to_vec_u8> "Link to this definition")
    

Parameters:
    

**ss58_address** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

bittensor.utils.strtobool(_val_)[#](<#bittensor.utils.strtobool> "Link to this definition")
    

Converts a string to a boolean value.

truth-y values are ‘y’, ‘yes’, ‘t’, ‘true’, ‘on’, and ‘1’; false-y values are ‘n’, ‘no’, ‘f’, ‘false’, ‘off’, and ‘0’.

Raises ValueError if ‘val’ is anything else.

Parameters:
    

**val** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

Return type:
    

Union[[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"), Literal[‘==SUPRESS==’]]

bittensor.utils.torch[#](<#bittensor.utils.torch> "Link to this definition")
    

bittensor.utils.u16_normalized_float(_x_)[#](<#bittensor.utils.u16_normalized_float> "Link to this definition")
    

Parameters:
    

**x** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

Return type:
    

[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")

bittensor.utils.u64_normalized_float(_x_)[#](<#bittensor.utils.u64_normalized_float> "Link to this definition")
    

Parameters:
    

**x** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

Return type:
    

[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")

bittensor.utils.unlock_key(_wallet_ , _unlock_type ='coldkey'_, _raise_error =False_)[#](<#bittensor.utils.unlock_key> "Link to this definition")
    

Attempts to decrypt a wallet’s coldkey or hotkey

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance.

  * **unlock_type** – the key type, ‘coldkey’ or ‘hotkey’.

  * **raise_error** – if False, will return (False, error msg), if True will raise the otherwise-caught exception.



Returns:
    

UnlockStatus for success status of unlock, with error message if unsuccessful

Raises:
    

  * **bittensor_wallet.errors.PasswordError** – incorrect password

  * **bittensor_wallet.errors.KeyFileError** – keyfile is corrupt, non-writable, or non-readable, or non-existent



Return type:
    

[UnlockStatus](<#bittensor.utils.UnlockStatus> "bittensor.utils.UnlockStatus")

bittensor.utils.use_torch[#](<#bittensor.utils.use_torch> "Link to this definition")
    

bittensor.utils.validate_chain_endpoint(_endpoint_url_)[#](<#bittensor.utils.validate_chain_endpoint> "Link to this definition")
    

Validates if the provided endpoint URL is a valid WebSocket URL.

Parameters:
    

**endpoint_url** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

Return type:
    

[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"), [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]

bittensor.utils.validate_max_attempts(_max_attempts_ , _response_)[#](<#bittensor.utils.validate_max_attempts> "Link to this definition")
    

Common guard for all subtensor methods with max_attempts parameter.

Parameters:
    

  * **max_attempts** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

  * **response** ([_bittensor.core.types.ExtrinsicResponse_](<../core/types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse"))



Return type:
    

Optional[[bittensor.core.types.ExtrinsicResponse](<../core/types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")]

[ __ previous bittensor.extras.timelock ](<../extras/timelock/index.html> "previous page") [ next bittensor.utils.axon_utils __](<axon_utils/index.html> "next page")

__Contents

  * [Submodules](<#submodules>)
  * [Attributes](<#attributes>)
  * [Exceptions](<#exceptions>)
  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Package Contents](<#package-contents>)
    * [`BT_DOCS_LINK`](<#bittensor.utils.BT_DOCS_LINK>)
    * [`Certificate`](<#bittensor.utils.Certificate>)
    * [`ChainFeatureDisabledWarning`](<#bittensor.utils.ChainFeatureDisabledWarning>)
    * [`GLOBAL_MAX_SUBNET_COUNT`](<#bittensor.utils.GLOBAL_MAX_SUBNET_COUNT>)
    * [`RAOPERTAO`](<#bittensor.utils.RAOPERTAO>)
    * [`U16_MAX`](<#bittensor.utils.U16_MAX>)
    * [`U64_MAX`](<#bittensor.utils.U64_MAX>)
    * [`UnlockStatus`](<#bittensor.utils.UnlockStatus>)
      * [`UnlockStatus.message`](<#bittensor.utils.UnlockStatus.message>)
      * [`UnlockStatus.success`](<#bittensor.utils.UnlockStatus.success>)
    * [`VersionCheckError`](<#bittensor.utils.VersionCheckError>)
    * [`check_version`](<#bittensor.utils.check_version>)
    * [`decode_hex_identity_dict()`](<#bittensor.utils.decode_hex_identity_dict>)
    * [`deprecated_message()`](<#bittensor.utils.deprecated_message>)
    * [`determine_chain_endpoint_and_network()`](<#bittensor.utils.determine_chain_endpoint_and_network>)
    * [`float_to_u64()`](<#bittensor.utils.float_to_u64>)
    * [`format_error_message()`](<#bittensor.utils.format_error_message>)
    * [`get_caller_name()`](<#bittensor.utils.get_caller_name>)
    * [`get_explorer_url_for_network()`](<#bittensor.utils.get_explorer_url_for_network>)
    * [`get_function_name()`](<#bittensor.utils.get_function_name>)
    * [`get_hash()`](<#bittensor.utils.get_hash>)
    * [`get_mechid_storage_index()`](<#bittensor.utils.get_mechid_storage_index>)
    * [`get_netuid_and_mechid_by_storage_index()`](<#bittensor.utils.get_netuid_and_mechid_by_storage_index>)
    * [`hex_to_bytes`](<#bittensor.utils.hex_to_bytes>)
    * [`hex_to_ss58`](<#bittensor.utils.hex_to_ss58>)
    * [`is_valid_bittensor_address_or_public_key()`](<#bittensor.utils.is_valid_bittensor_address_or_public_key>)
    * [`is_valid_ss58_address()`](<#bittensor.utils.is_valid_ss58_address>)
    * [`logging`](<#bittensor.utils.logging>)
    * [`ss58_address_to_bytes()`](<#bittensor.utils.ss58_address_to_bytes>)
    * [`ss58_decode`](<#bittensor.utils.ss58_decode>)
    * [`ss58_to_hex`](<#bittensor.utils.ss58_to_hex>)
    * [`ss58_to_vec_u8()`](<#bittensor.utils.ss58_to_vec_u8>)
    * [`strtobool()`](<#bittensor.utils.strtobool>)
    * [`torch`](<#bittensor.utils.torch>)
    * [`u16_normalized_float()`](<#bittensor.utils.u16_normalized_float>)
    * [`u64_normalized_float()`](<#bittensor.utils.u64_normalized_float>)
    * [`unlock_key()`](<#bittensor.utils.unlock_key>)
    * [`use_torch`](<#bittensor.utils.use_torch>)
    * [`validate_chain_endpoint()`](<#bittensor.utils.validate_chain_endpoint>)
    * [`validate_max_attempts()`](<#bittensor.utils.validate_max_attempts>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.