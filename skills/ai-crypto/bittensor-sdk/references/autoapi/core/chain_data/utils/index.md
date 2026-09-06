# bittensor.core.chain_data.utils &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/utils/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/utils/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/utils/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.utils

##  Contents 

  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`ChainDataType`](<#bittensor.core.chain_data.utils.ChainDataType>)
      * [`ChainDataType.AccountId`](<#bittensor.core.chain_data.utils.ChainDataType.AccountId>)
      * [`ChainDataType.AxonInfo`](<#bittensor.core.chain_data.utils.ChainDataType.AxonInfo>)
      * [`ChainDataType.ChainIdentity`](<#bittensor.core.chain_data.utils.ChainDataType.ChainIdentity>)
      * [`ChainDataType.DelegateInfo`](<#bittensor.core.chain_data.utils.ChainDataType.DelegateInfo>)
      * [`ChainDataType.DelegatedInfo`](<#bittensor.core.chain_data.utils.ChainDataType.DelegatedInfo>)
      * [`ChainDataType.DynamicInfo`](<#bittensor.core.chain_data.utils.ChainDataType.DynamicInfo>)
      * [`ChainDataType.IPInfo`](<#bittensor.core.chain_data.utils.ChainDataType.IPInfo>)
      * [`ChainDataType.MetagraphInfo`](<#bittensor.core.chain_data.utils.ChainDataType.MetagraphInfo>)
      * [`ChainDataType.NeuronInfo`](<#bittensor.core.chain_data.utils.ChainDataType.NeuronInfo>)
      * [`ChainDataType.NeuronInfoLite`](<#bittensor.core.chain_data.utils.ChainDataType.NeuronInfoLite>)
      * [`ChainDataType.ScheduledColdkeySwapInfo`](<#bittensor.core.chain_data.utils.ChainDataType.ScheduledColdkeySwapInfo>)
      * [`ChainDataType.StakeInfo`](<#bittensor.core.chain_data.utils.ChainDataType.StakeInfo>)
      * [`ChainDataType.SubnetHyperparameters`](<#bittensor.core.chain_data.utils.ChainDataType.SubnetHyperparameters>)
      * [`ChainDataType.SubnetIdentity`](<#bittensor.core.chain_data.utils.ChainDataType.SubnetIdentity>)
      * [`ChainDataType.SubnetInfo`](<#bittensor.core.chain_data.utils.ChainDataType.SubnetInfo>)
      * [`ChainDataType.SubnetState`](<#bittensor.core.chain_data.utils.ChainDataType.SubnetState>)
    * [`decode_block()`](<#bittensor.core.chain_data.utils.decode_block>)
    * [`decode_metadata()`](<#bittensor.core.chain_data.utils.decode_metadata>)
    * [`decode_revealed_commitment()`](<#bittensor.core.chain_data.utils.decode_revealed_commitment>)
    * [`decode_revealed_commitment_with_hotkey()`](<#bittensor.core.chain_data.utils.decode_revealed_commitment_with_hotkey>)
    * [`from_scale_encoding()`](<#bittensor.core.chain_data.utils.from_scale_encoding>)
    * [`from_scale_encoding_using_type_string()`](<#bittensor.core.chain_data.utils.from_scale_encoding_using_type_string>)
    * [`process_stake_data()`](<#bittensor.core.chain_data.utils.process_stake_data>)



# bittensor.core.chain_data.utils[#](<#module-bittensor.core.chain_data.utils> "Link to this heading")

Chain data helper functions and data.

## Classes[#](<#classes> "Link to this heading")

[`ChainDataType`](<#bittensor.core.chain_data.utils.ChainDataType> "bittensor.core.chain_data.utils.ChainDataType") | Create a collection of name/value pairs.  
---|---  
  
## Functions[#](<#functions> "Link to this heading")

[`decode_block`](<#bittensor.core.chain_data.utils.decode_block> "bittensor.core.chain_data.utils.decode_block")(data) | Decode the block data from the given input if it is not None.  
---|---  
[`decode_metadata`](<#bittensor.core.chain_data.utils.decode_metadata> "bittensor.core.chain_data.utils.decode_metadata")(metadata) |   
[`decode_revealed_commitment`](<#bittensor.core.chain_data.utils.decode_revealed_commitment> "bittensor.core.chain_data.utils.decode_revealed_commitment")(encoded_data) | Decode the revealed commitment data from the given input if it is not None.  
[`decode_revealed_commitment_with_hotkey`](<#bittensor.core.chain_data.utils.decode_revealed_commitment_with_hotkey> "bittensor.core.chain_data.utils.decode_revealed_commitment_with_hotkey")(encoded_data) | Decode revealed commitment using a hotkey.  
[`from_scale_encoding`](<#bittensor.core.chain_data.utils.from_scale_encoding> "bittensor.core.chain_data.utils.from_scale_encoding")(input_, type_name[, is_vec, is_option]) | Decodes [input_](<#id1>) data from SCALE encoding based on the specified type name and modifiers.  
[`from_scale_encoding_using_type_string`](<#bittensor.core.chain_data.utils.from_scale_encoding_using_type_string> "bittensor.core.chain_data.utils.from_scale_encoding_using_type_string")(input_, type_string) | Decodes SCALE encoded data to a dictionary based on the provided type string.  
[`process_stake_data`](<#bittensor.core.chain_data.utils.process_stake_data> "bittensor.core.chain_data.utils.process_stake_data")(stake_data) | Processes stake data to decode account IDs and convert stakes from rao to Balance objects.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.utils.ChainDataType[#](<#bittensor.core.chain_data.utils.ChainDataType> "Link to this definition")
    

Bases: [`enum.Enum`](<https://docs.python.org/3/library/enum.html#enum.Enum> "\(in Python v3.14\)")

Create a collection of name/value pairs.

Example enumeration:
[code] 
    >>> class Color(Enum):
    ...     RED = 1
    ...     BLUE = 2
    ...     GREEN = 3
    
[/code]

Access them by:

  * attribute access:
[code] >>> Color.RED
        <Color.RED: 1>
        
[/code]

  * value lookup:
[code] >>> Color(1)
        <Color.RED: 1>
        
[/code]

  * name lookup:
[code] >>> Color['RED']
        <Color.RED: 1>
        
[/code]




Enumerations can be iterated over, and know how many members they have:
[code] 
    >>> len(Color)
    3
    
[/code]
[code] 
    >>> list(Color)
    [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]
    
[/code]

Methods can be added to enumerations, and members can have their own attributes – see the documentation for details.

AccountId = 10[#](<#bittensor.core.chain_data.utils.ChainDataType.AccountId> "Link to this definition")
    

AxonInfo = 16[#](<#bittensor.core.chain_data.utils.ChainDataType.AxonInfo> "Link to this definition")
    

ChainIdentity = 15[#](<#bittensor.core.chain_data.utils.ChainDataType.ChainIdentity> "Link to this definition")
    

DelegateInfo = 3[#](<#bittensor.core.chain_data.utils.ChainDataType.DelegateInfo> "Link to this definition")
    

DelegatedInfo = 5[#](<#bittensor.core.chain_data.utils.ChainDataType.DelegatedInfo> "Link to this definition")
    

DynamicInfo = 12[#](<#bittensor.core.chain_data.utils.ChainDataType.DynamicInfo> "Link to this definition")
    

IPInfo = 7[#](<#bittensor.core.chain_data.utils.ChainDataType.IPInfo> "Link to this definition")
    

MetagraphInfo = 14[#](<#bittensor.core.chain_data.utils.ChainDataType.MetagraphInfo> "Link to this definition")
    

NeuronInfo = 1[#](<#bittensor.core.chain_data.utils.ChainDataType.NeuronInfo> "Link to this definition")
    

NeuronInfoLite = 4[#](<#bittensor.core.chain_data.utils.ChainDataType.NeuronInfoLite> "Link to this definition")
    

ScheduledColdkeySwapInfo = 9[#](<#bittensor.core.chain_data.utils.ChainDataType.ScheduledColdkeySwapInfo> "Link to this definition")
    

StakeInfo = 6[#](<#bittensor.core.chain_data.utils.ChainDataType.StakeInfo> "Link to this definition")
    

SubnetHyperparameters = 8[#](<#bittensor.core.chain_data.utils.ChainDataType.SubnetHyperparameters> "Link to this definition")
    

SubnetIdentity = 13[#](<#bittensor.core.chain_data.utils.ChainDataType.SubnetIdentity> "Link to this definition")
    

SubnetInfo = 2[#](<#bittensor.core.chain_data.utils.ChainDataType.SubnetInfo> "Link to this definition")
    

SubnetState = 11[#](<#bittensor.core.chain_data.utils.ChainDataType.SubnetState> "Link to this definition")
    

bittensor.core.chain_data.utils.decode_block(_data_)[#](<#bittensor.core.chain_data.utils.decode_block> "Link to this definition")
    

Decode the block data from the given input if it is not None.

Parameters:
    

**data** ([_bytes_](<../../../extras/dev_framework/calls/non_sudo_calls/index.html#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes> "bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes")) – The block data to decode.

Returns:
    

The decoded block.

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

bittensor.core.chain_data.utils.decode_metadata(_metadata_)[#](<#bittensor.core.chain_data.utils.decode_metadata> "Link to this definition")
    

Parameters:
    

**metadata** ([_bittensor.core.types.CommitmentOfResponse_](<../../types/index.html#bittensor.core.types.CommitmentOfResponse> "bittensor.core.types.CommitmentOfResponse"))

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

bittensor.core.chain_data.utils.decode_revealed_commitment(_encoded_data_)[#](<#bittensor.core.chain_data.utils.decode_revealed_commitment> "Link to this definition")
    

Decode the revealed commitment data from the given input if it is not None.

Parameters:
    

**encoded_data** – A tuple containing the revealed message and the block number.

Returns:
    

A tuple containing the revealed block number and decoded commitment message.

Return type:
    

[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]

bittensor.core.chain_data.utils.decode_revealed_commitment_with_hotkey(_encoded_data_)[#](<#bittensor.core.chain_data.utils.decode_revealed_commitment_with_hotkey> "Link to this definition")
    

Decode revealed commitment using a hotkey.

Returns:
    

A tuple containing the hotkey (ss58 address) and a tuple of block
    

numbers and their corresponding revealed commitments.

Return type:
    

[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")], …]]

Parameters:
    

**encoded_data** (_async_substrate_interface.sync_substrate.QueryMapResult_)

bittensor.core.chain_data.utils.from_scale_encoding(_input__ , _type_name_ , _is_vec =False_, _is_option =False_)[#](<#bittensor.core.chain_data.utils.from_scale_encoding> "Link to this definition")
    

Decodes [input_](<#id3>) data from SCALE encoding based on the specified type name and modifiers.

Parameters:
    

  * **input** – The [input_](<#id5>) data to decode.

  * **type_name** ([_ChainDataType_](<#bittensor.core.chain_data.utils.ChainDataType> "bittensor.core.chain_data.utils.ChainDataType")) – The type of data being decoded.

  * **is_vec** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether the data is a vector of the specified type.

  * **is_option** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether the data is an optional value of the specified type.

  * **input_** (_Union_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]__,_[_bytes_](<../../../extras/dev_framework/calls/non_sudo_calls/index.html#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes> "bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes") _,__scalecodec.ScaleBytes_ _]_)



Returns:
    

The decoded data as a dictionary, or `None` if the decoding fails.

Return type:
    

Optional[[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")]

bittensor.core.chain_data.utils.from_scale_encoding_using_type_string(_input__ , _type_string_)[#](<#bittensor.core.chain_data.utils.from_scale_encoding_using_type_string> "Link to this definition")
    

Decodes SCALE encoded data to a dictionary based on the provided type string.

Parameters:
    

  * **input** – The SCALE encoded input data.

  * **type_string** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The type string defining the structure of the data.

  * **input_** (_Union_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]__,_[_bytes_](<../../../extras/dev_framework/calls/non_sudo_calls/index.html#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes> "bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes") _,__scalecodec.ScaleBytes_ _]_)



Returns:
    

The decoded data as a dictionary, or `None` if the decoding fails.

Raises:
    

[**TypeError**](<https://docs.python.org/3/library/exceptions.html#TypeError> "\(in Python v3.14\)") – If the [input_](<#id7>) is not a list[int], bytes, or ScaleBytes.

Return type:
    

Optional[[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")]

bittensor.core.chain_data.utils.process_stake_data(_stake_data_)[#](<#bittensor.core.chain_data.utils.process_stake_data> "Link to this definition")
    

Processes stake data to decode account IDs and convert stakes from rao to Balance objects.

Parameters:
    

**stake_data** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")) – A list of tuples where each tuple contains an account ID in bytes and a stake in rao.

Returns:
    

A dictionary with account IDs as keys and their corresponding Balance objects as values.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")

[ __ previous bittensor.core.chain_data.subnet_state ](<../subnet_state/index.html> "previous page") [ next bittensor.core.chain_data.weight_commit_info __](<../weight_commit_info/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`ChainDataType`](<#bittensor.core.chain_data.utils.ChainDataType>)
      * [`ChainDataType.AccountId`](<#bittensor.core.chain_data.utils.ChainDataType.AccountId>)
      * [`ChainDataType.AxonInfo`](<#bittensor.core.chain_data.utils.ChainDataType.AxonInfo>)
      * [`ChainDataType.ChainIdentity`](<#bittensor.core.chain_data.utils.ChainDataType.ChainIdentity>)
      * [`ChainDataType.DelegateInfo`](<#bittensor.core.chain_data.utils.ChainDataType.DelegateInfo>)
      * [`ChainDataType.DelegatedInfo`](<#bittensor.core.chain_data.utils.ChainDataType.DelegatedInfo>)
      * [`ChainDataType.DynamicInfo`](<#bittensor.core.chain_data.utils.ChainDataType.DynamicInfo>)
      * [`ChainDataType.IPInfo`](<#bittensor.core.chain_data.utils.ChainDataType.IPInfo>)
      * [`ChainDataType.MetagraphInfo`](<#bittensor.core.chain_data.utils.ChainDataType.MetagraphInfo>)
      * [`ChainDataType.NeuronInfo`](<#bittensor.core.chain_data.utils.ChainDataType.NeuronInfo>)
      * [`ChainDataType.NeuronInfoLite`](<#bittensor.core.chain_data.utils.ChainDataType.NeuronInfoLite>)
      * [`ChainDataType.ScheduledColdkeySwapInfo`](<#bittensor.core.chain_data.utils.ChainDataType.ScheduledColdkeySwapInfo>)
      * [`ChainDataType.StakeInfo`](<#bittensor.core.chain_data.utils.ChainDataType.StakeInfo>)
      * [`ChainDataType.SubnetHyperparameters`](<#bittensor.core.chain_data.utils.ChainDataType.SubnetHyperparameters>)
      * [`ChainDataType.SubnetIdentity`](<#bittensor.core.chain_data.utils.ChainDataType.SubnetIdentity>)
      * [`ChainDataType.SubnetInfo`](<#bittensor.core.chain_data.utils.ChainDataType.SubnetInfo>)
      * [`ChainDataType.SubnetState`](<#bittensor.core.chain_data.utils.ChainDataType.SubnetState>)
    * [`decode_block()`](<#bittensor.core.chain_data.utils.decode_block>)
    * [`decode_metadata()`](<#bittensor.core.chain_data.utils.decode_metadata>)
    * [`decode_revealed_commitment()`](<#bittensor.core.chain_data.utils.decode_revealed_commitment>)
    * [`decode_revealed_commitment_with_hotkey()`](<#bittensor.core.chain_data.utils.decode_revealed_commitment_with_hotkey>)
    * [`from_scale_encoding()`](<#bittensor.core.chain_data.utils.from_scale_encoding>)
    * [`from_scale_encoding_using_type_string()`](<#bittensor.core.chain_data.utils.from_scale_encoding_using_type_string>)
    * [`process_stake_data()`](<#bittensor.core.chain_data.utils.process_stake_data>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.