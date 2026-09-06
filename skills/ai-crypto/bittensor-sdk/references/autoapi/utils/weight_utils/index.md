# bittensor.utils.weight_utils &#8212; Bittensor SDK Docs  documentation

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
        * [bittensor.utils.networking](<../networking/index.html>)
        * [bittensor.utils.registration](<../registration/index.html>)
        * [bittensor.utils.subnets](<../subnets/index.html>)
        * [bittensor.utils.version](<../version/index.html>)
        * [bittensor.utils.weight_utils](<#>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/utils/weight_utils/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/utils/weight_utils/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/utils/weight_utils/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.utils.weight_utils

##  Contents 

  * [Attributes](<#attributes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`U16_MAX`](<#bittensor.utils.weight_utils.U16_MAX>)
    * [`U32_MAX`](<#bittensor.utils.weight_utils.U32_MAX>)
    * [`convert_and_normalize_weights_and_uids()`](<#bittensor.utils.weight_utils.convert_and_normalize_weights_and_uids>)
    * [`convert_bond_uids_and_vals_to_tensor()`](<#bittensor.utils.weight_utils.convert_bond_uids_and_vals_to_tensor>)
    * [`convert_maybe_split_to_u16()`](<#bittensor.utils.weight_utils.convert_maybe_split_to_u16>)
    * [`convert_root_weight_uids_and_vals_to_tensor()`](<#bittensor.utils.weight_utils.convert_root_weight_uids_and_vals_to_tensor>)
    * [`convert_uids_and_weights()`](<#bittensor.utils.weight_utils.convert_uids_and_weights>)
    * [`convert_weight_uids_and_vals_to_tensor()`](<#bittensor.utils.weight_utils.convert_weight_uids_and_vals_to_tensor>)
    * [`convert_weights_and_uids_for_emit()`](<#bittensor.utils.weight_utils.convert_weights_and_uids_for_emit>)
    * [`generate_weight_hash()`](<#bittensor.utils.weight_utils.generate_weight_hash>)
    * [`normalize_max_weight()`](<#bittensor.utils.weight_utils.normalize_max_weight>)
    * [`process_weights()`](<#bittensor.utils.weight_utils.process_weights>)
    * [`process_weights_for_netuid()`](<#bittensor.utils.weight_utils.process_weights_for_netuid>)



# bittensor.utils.weight_utils[#](<#module-bittensor.utils.weight_utils> "Link to this heading")

Conversion for weight between chain representation and np.array or torch.Tensor

## Attributes[#](<#attributes> "Link to this heading")

[`U16_MAX`](<#bittensor.utils.weight_utils.U16_MAX> "bittensor.utils.weight_utils.U16_MAX") |   
---|---  
[`U32_MAX`](<#bittensor.utils.weight_utils.U32_MAX> "bittensor.utils.weight_utils.U32_MAX") |   
  
## Functions[#](<#functions> "Link to this heading")

[`convert_and_normalize_weights_and_uids`](<#bittensor.utils.weight_utils.convert_and_normalize_weights_and_uids> "bittensor.utils.weight_utils.convert_and_normalize_weights_and_uids")(uids, weights) | Converts weights and uids to numpy arrays if they are not already.  
---|---  
[`convert_bond_uids_and_vals_to_tensor`](<#bittensor.utils.weight_utils.convert_bond_uids_and_vals_to_tensor> "bittensor.utils.weight_utils.convert_bond_uids_and_vals_to_tensor")(n, uids, bonds) | Converts bond and uids from chain representation into a np.array.  
[`convert_maybe_split_to_u16`](<#bittensor.utils.weight_utils.convert_maybe_split_to_u16> "bittensor.utils.weight_utils.convert_maybe_split_to_u16")(maybe_split) |   
[`convert_root_weight_uids_and_vals_to_tensor`](<#bittensor.utils.weight_utils.convert_root_weight_uids_and_vals_to_tensor> "bittensor.utils.weight_utils.convert_root_weight_uids_and_vals_to_tensor")(n, uids, ...) | Converts root weights and uids from chain representation into a np.array or torch FloatTensor  
[`convert_uids_and_weights`](<#bittensor.utils.weight_utils.convert_uids_and_weights> "bittensor.utils.weight_utils.convert_uids_and_weights")(uids, weights) | Converts netuids and weights to numpy arrays if they are not already.  
[`convert_weight_uids_and_vals_to_tensor`](<#bittensor.utils.weight_utils.convert_weight_uids_and_vals_to_tensor> "bittensor.utils.weight_utils.convert_weight_uids_and_vals_to_tensor")(n, uids, weights) | Converts weights and uids from chain representation into a np.array (inverse operation from  
[`convert_weights_and_uids_for_emit`](<#bittensor.utils.weight_utils.convert_weights_and_uids_for_emit> "bittensor.utils.weight_utils.convert_weights_and_uids_for_emit")(uids, weights) | Converts weights into integer u32 representation that sum to MAX_INT_WEIGHT.  
[`generate_weight_hash`](<#bittensor.utils.weight_utils.generate_weight_hash> "bittensor.utils.weight_utils.generate_weight_hash")(address, netuid, uids, values, ...) | Generate a valid commit hash from the provided weights.  
[`normalize_max_weight`](<#bittensor.utils.weight_utils.normalize_max_weight> "bittensor.utils.weight_utils.normalize_max_weight")(x[, limit]) | Normalizes the tensor x so that sum(x) = 1 and the max value is not greater than the limit.  
[`process_weights`](<#bittensor.utils.weight_utils.process_weights> "bittensor.utils.weight_utils.process_weights")(uids, weights, num_neurons, ...[, ...]) | Processes weight tensors for a given weights and UID arrays and hyperparams, applying constraints and normalization  
[`process_weights_for_netuid`](<#bittensor.utils.weight_utils.process_weights_for_netuid> "bittensor.utils.weight_utils.process_weights_for_netuid")(uids, weights, netuid, ...) | Processes weight tensors for a given subnet id using the provided weight and UID arrays, applying constraints and  
  
## Module Contents[#](<#module-contents> "Link to this heading")

bittensor.utils.weight_utils.U16_MAX = 65535[#](<#bittensor.utils.weight_utils.U16_MAX> "Link to this definition")
    

bittensor.utils.weight_utils.U32_MAX = 4294967295[#](<#bittensor.utils.weight_utils.U32_MAX> "Link to this definition")
    

bittensor.utils.weight_utils.convert_and_normalize_weights_and_uids(_uids_ , _weights_)[#](<#bittensor.utils.weight_utils.convert_and_normalize_weights_and_uids> "Link to this definition")
    

Converts weights and uids to numpy arrays if they are not already.

Parameters:
    

  * **uids** (_Union_ _[__numpy.typing.NDArray_ _[__numpy.int64_ _]__,__bittensor.utils.registration.torch.LongTensor_ _,_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _]_) – The `uint64` uids of destination neurons.

  * **weights** (_Union_ _[__numpy.typing.NDArray_ _[__numpy.float32_ _]__,__bittensor.utils.registration.torch.FloatTensor_ _,_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _]_) – The weights to set. These must be `float` s and correspond to the passed `uid` s.



Returns:
    

Bytes converted weights and uids

Return type:
    

weight_uids, weight_vals

bittensor.utils.weight_utils.convert_bond_uids_and_vals_to_tensor(_n_ , _uids_ , _bonds_)[#](<#bittensor.utils.weight_utils.convert_bond_uids_and_vals_to_tensor> "Link to this definition")
    

Converts bond and uids from chain representation into a np.array.

Parameters:
    

  * **n** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – number of neurons on network.

  * **uids** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Tensor of uids as destinations for passed bonds.

  * **bonds** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Tensor of bonds.



Returns:
    

Converted row bonds.

Return type:
    

Union[numpy.typing.NDArray[numpy.int64], bittensor.utils.registration.torch.LongTensor]

bittensor.utils.weight_utils.convert_maybe_split_to_u16(_maybe_split_)[#](<#bittensor.utils.weight_utils.convert_maybe_split_to_u16> "Link to this definition")
    

Parameters:
    

**maybe_split** ([_bittensor.core.types.Weights_](<../../core/types/index.html#bittensor.core.types.Weights> "bittensor.core.types.Weights"))

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

bittensor.utils.weight_utils.convert_root_weight_uids_and_vals_to_tensor(_n_ , _uids_ , _weights_ , _subnets_)[#](<#bittensor.utils.weight_utils.convert_root_weight_uids_and_vals_to_tensor> "Link to this definition")
    

Converts root weights and uids from chain representation into a np.array or torch FloatTensor (inverse operation from convert_weights_and_uids_for_emit)

Parameters:
    

  * **n** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – number of neurons on network.

  * **uids** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Tensor of uids as destinations for passed weights.

  * **weights** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Tensor of weights.

  * **subnets** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – list of subnets on the network.



Returns:
    

Converted row weights.

Return type:
    

Union[numpy.typing.NDArray[numpy.float32], bittensor.utils.registration.torch.FloatTensor]

bittensor.utils.weight_utils.convert_uids_and_weights(_uids_ , _weights_)[#](<#bittensor.utils.weight_utils.convert_uids_and_weights> "Link to this definition")
    

Converts netuids and weights to numpy arrays if they are not already.

Parameters:
    

  * **uids** (_Union_ _[__numpy.typing.NDArray_ _[__numpy.int64_ _]__,_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _]_) – The uint64 uids of destination neurons.

  * **weights** (_Union_ _[__numpy.typing.NDArray_ _[__numpy.float32_ _]__,_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _]_) – The weights to set. These must be floated.



Returns:
    

Bytes converted netuids and weights.

Return type:
    

[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[ndarray, ndarray]

bittensor.utils.weight_utils.convert_weight_uids_and_vals_to_tensor(_n_ , _uids_ , _weights_)[#](<#bittensor.utils.weight_utils.convert_weight_uids_and_vals_to_tensor> "Link to this definition")
    

Converts weights and uids from chain representation into a np.array (inverse operation from convert_weights_and_uids_for_emit).

Parameters:
    

  * **n** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – number of neurons on network.

  * **uids** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Tensor of uids as destinations for passed weights.

  * **weights** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Tensor of weights.



Returns:
    

Converted row weights.

Return type:
    

Union[numpy.typing.NDArray[numpy.float32], bittensor.utils.registration.torch.FloatTensor]

bittensor.utils.weight_utils.convert_weights_and_uids_for_emit(_uids_ , _weights_)[#](<#bittensor.utils.weight_utils.convert_weights_and_uids_for_emit> "Link to this definition")
    

Converts weights into integer u32 representation that sum to MAX_INT_WEIGHT.

Parameters:
    

  * **uids** (_Union_ _[__numpy.typing.NDArray_ _[__numpy.int64_ _]__,__bittensor.utils.registration.torch.LongTensor_ _]_) – Tensor of uids as destinations for passed weights.

  * **weights** (_Union_ _[__numpy.typing.NDArray_ _[__numpy.float32_ _]__,__bittensor.utils.registration.torch.FloatTensor_ _]_) – Tensor of weights.



Returns:
    

Uids as a list. weight_vals: Weights as a list.

Return type:
    

weight_uids

bittensor.utils.weight_utils.generate_weight_hash(_address_ , _netuid_ , _uids_ , _values_ , _version_key_ , _salt_)[#](<#bittensor.utils.weight_utils.generate_weight_hash> "Link to this definition")
    

Generate a valid commit hash from the provided weights.

Parameters:
    

  * **address** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The account identifier. Wallet ss58_address.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet unique identifier.

  * **uids** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The list of UIDs.

  * **salt** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The salt to add to hash.

  * **values** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The list of weight values.

  * **version_key** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The version key.



Returns:
    

The generated commit hash.

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

bittensor.utils.weight_utils.normalize_max_weight(_x_ , _limit =0.1_)[#](<#bittensor.utils.weight_utils.normalize_max_weight> "Link to this definition")
    

Normalizes the tensor x so that sum(x) = 1 and the max value is not greater than the limit.

Parameters:
    

  * **x** (_Union_ _[__numpy.typing.NDArray_ _[__numpy.float32_ _]__,__bittensor.utils.registration.torch.FloatTensor_ _]_) – Tensor to be max_value normalized.

  * **limit** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")) – float: Max value after normalization.



Returns:
    

Normalized x tensor.

Return type:
    

y

bittensor.utils.weight_utils.process_weights(_uids_ , _weights_ , _num_neurons_ , _min_allowed_weights_ , _max_weight_limit_ , _exclude_quantile =0_)[#](<#bittensor.utils.weight_utils.process_weights> "Link to this definition")
    

Processes weight tensors for a given weights and UID arrays and hyperparams, applying constraints and normalization based on the subtensor and metagraph data. This function can handle both NumPy arrays and PyTorch tensors.

Parameters:
    

  * **uids** (_Union_ _[__numpy.typing.NDArray_ _[__numpy.int64_ _]__,__bittensor.utils.registration.torch.Tensor_ _]_) – Array of unique identifiers of the neurons.

  * **weights** (_Union_ _[__numpy.typing.NDArray_ _[__numpy.float32_ _]__,__bittensor.utils.registration.torch.Tensor_ _]_) – Array of weights associated with the user IDs.

  * **num_neurons** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The number of neurons in the network.

  * **min_allowed_weights** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Subnet hyperparam Minimum number of allowed weights.

  * **max_weight_limit** (_Optional_ _[_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _]_) – Subnet hyperparam Maximum weight limit.

  * **exclude_quantile** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Quantile threshold for excluding lower weights.



Returns:
    

Tuple containing the array of user IDs and the corresponding normalized weights. The data type of the return matches the type of the input weights (NumPy or PyTorch).

Return type:
    

Union[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[bittensor.utils.registration.torch.Tensor, bittensor.utils.registration.torch.FloatTensor], [tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[numpy.typing.NDArray[numpy.int64], numpy.typing.NDArray[numpy.float32]]]

bittensor.utils.weight_utils.process_weights_for_netuid(_uids_ , _weights_ , _netuid_ , _subtensor_ , _metagraph =None_, _exclude_quantile =0_)[#](<#bittensor.utils.weight_utils.process_weights_for_netuid> "Link to this definition")
    

Processes weight tensors for a given subnet id using the provided weight and UID arrays, applying constraints and normalization based on the subtensor and metagraph data. This function can handle both NumPy arrays and PyTorch tensors.

Parameters:
    

  * **uids** (_Union_ _[__numpy.typing.NDArray_ _[__numpy.int64_ _]__,__bittensor.utils.registration.torch.Tensor_ _]_) – Array of unique identifiers of the neurons.

  * **weights** (_Union_ _[__numpy.typing.NDArray_ _[__numpy.float32_ _]__,__bittensor.utils.registration.torch.Tensor_ _]_) – Array of weights associated with the user IDs.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The network uid to process weights for.

  * **subtensor** ([_bittensor.core.subtensor.Subtensor_](<../../core/subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor")) – Subtensor instance to access blockchain data.

  * **metagraph** (_Optional_ _[_[_bittensor.core.metagraph.Metagraph_](<../../core/metagraph/index.html#bittensor.core.metagraph.Metagraph> "bittensor.core.metagraph.Metagraph") _]_) – Metagraph instance for additional network data. If None, it is fetched from the subtensor using the netuid.

  * **exclude_quantile** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Quantile threshold for excluding lower weights.



Returns:
    

Tuple containing the array of user IDs and the corresponding normalized weights. The data type of the return matches the type of the input weights (NumPy or PyTorch).

Return type:
    

Union[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[bittensor.utils.registration.torch.Tensor, bittensor.utils.registration.torch.FloatTensor], [tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[numpy.typing.NDArray[numpy.int64], numpy.typing.NDArray[numpy.float32]]]

[ __ previous bittensor.utils.version ](<../version/index.html> "previous page")

__Contents

  * [Attributes](<#attributes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`U16_MAX`](<#bittensor.utils.weight_utils.U16_MAX>)
    * [`U32_MAX`](<#bittensor.utils.weight_utils.U32_MAX>)
    * [`convert_and_normalize_weights_and_uids()`](<#bittensor.utils.weight_utils.convert_and_normalize_weights_and_uids>)
    * [`convert_bond_uids_and_vals_to_tensor()`](<#bittensor.utils.weight_utils.convert_bond_uids_and_vals_to_tensor>)
    * [`convert_maybe_split_to_u16()`](<#bittensor.utils.weight_utils.convert_maybe_split_to_u16>)
    * [`convert_root_weight_uids_and_vals_to_tensor()`](<#bittensor.utils.weight_utils.convert_root_weight_uids_and_vals_to_tensor>)
    * [`convert_uids_and_weights()`](<#bittensor.utils.weight_utils.convert_uids_and_weights>)
    * [`convert_weight_uids_and_vals_to_tensor()`](<#bittensor.utils.weight_utils.convert_weight_uids_and_vals_to_tensor>)
    * [`convert_weights_and_uids_for_emit()`](<#bittensor.utils.weight_utils.convert_weights_and_uids_for_emit>)
    * [`generate_weight_hash()`](<#bittensor.utils.weight_utils.generate_weight_hash>)
    * [`normalize_max_weight()`](<#bittensor.utils.weight_utils.normalize_max_weight>)
    * [`process_weights()`](<#bittensor.utils.weight_utils.process_weights>)
    * [`process_weights_for_netuid()`](<#bittensor.utils.weight_utils.process_weights_for_netuid>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.