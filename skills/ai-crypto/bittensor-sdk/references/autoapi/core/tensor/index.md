# bittensor.core.tensor &#8212; Bittensor SDK Docs  documentation

[Skip to main content](<#main-content>)

__Back to top __ `Ctrl`+`K`

[ ![Bittensor SDK Docs  documentation - Home](../../../../_static/logo.svg) ![Bittensor SDK Docs  documentation - Home](../../../../_static/logo-dark-mode.svg) ](<../../../../index.html>)

__ Search `Ctrl`+`K`

Table of Contents

  * [API Reference](<../../../index.html>) __
    * [bittensor](<../../index.html>) __
      * [bittensor.core](<../index.html>) __
        * [bittensor.core.async_subtensor](<../async_subtensor/index.html>)
        * [bittensor.core.axon](<../axon/index.html>)
        * [bittensor.core.chain_data](<../chain_data/index.html>)
        * [bittensor.core.config](<../config/index.html>)
        * [bittensor.core.dendrite](<../dendrite/index.html>)
        * [bittensor.core.errors](<../errors/index.html>)
        * [bittensor.core.extrinsics](<../extrinsics/index.html>)
        * [bittensor.core.metagraph](<../metagraph/index.html>)
        * [bittensor.core.settings](<../settings/index.html>)
        * [bittensor.core.stream](<../stream/index.html>)
        * [bittensor.core.subtensor](<../subtensor/index.html>)
        * [bittensor.core.synapse](<../synapse/index.html>)
        * [bittensor.core.tensor](<#>)
        * [bittensor.core.threadpool](<../threadpool/index.html>)
        * [bittensor.core.types](<../types/index.html>)
      * [bittensor.extras](<../../extras/index.html>) __
        * [bittensor.extras.dev_framework](<../../extras/dev_framework/index.html>)
        * [bittensor.extras.subtensor_api](<../../extras/subtensor_api/index.html>)
        * [bittensor.extras.timelock](<../../extras/timelock/index.html>)
      * [bittensor.utils](<../../utils/index.html>) __
        * [bittensor.utils.axon_utils](<../../utils/axon_utils/index.html>)
        * [bittensor.utils.balance](<../../utils/balance/index.html>)
        * [bittensor.utils.btlogging](<../../utils/btlogging/index.html>)
        * [bittensor.utils.easy_imports](<../../utils/easy_imports/index.html>)
        * [bittensor.utils.formatting](<../../utils/formatting/index.html>)
        * [bittensor.utils.liquidity](<../../utils/liquidity/index.html>)
        * [bittensor.utils.networking](<../../utils/networking/index.html>)
        * [bittensor.utils.registration](<../../utils/registration/index.html>)
        * [bittensor.utils.subnets](<../../utils/subnets/index.html>)
        * [bittensor.utils.version](<../../utils/version/index.html>)
        * [bittensor.utils.weight_utils](<../../utils/weight_utils/index.html>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/tensor/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/tensor/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/core/tensor/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.tensor

##  Contents 

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`DTypes`](<#bittensor.core.tensor.DTypes>)
      * [`DTypes.torch`](<#bittensor.core.tensor.DTypes.torch>)
    * [`Tensor`](<#bittensor.core.tensor.Tensor>)
      * [`Tensor.buffer`](<#bittensor.core.tensor.Tensor.buffer>)
      * [`Tensor.deserialize()`](<#bittensor.core.tensor.Tensor.deserialize>)
      * [`Tensor.dtype`](<#bittensor.core.tensor.Tensor.dtype>)
      * [`Tensor.model_config`](<#bittensor.core.tensor.Tensor.model_config>)
      * [`Tensor.numpy()`](<#bittensor.core.tensor.Tensor.numpy>)
      * [`Tensor.serialize()`](<#bittensor.core.tensor.Tensor.serialize>)
      * [`Tensor.shape`](<#bittensor.core.tensor.Tensor.shape>)
      * [`Tensor.tensor()`](<#bittensor.core.tensor.Tensor.tensor>)
      * [`Tensor.tolist()`](<#bittensor.core.tensor.Tensor.tolist>)
    * [`cast_dtype()`](<#bittensor.core.tensor.cast_dtype>)
    * [`cast_shape()`](<#bittensor.core.tensor.cast_shape>)
    * [`dtypes`](<#bittensor.core.tensor.dtypes>)
    * [`tensor`](<#bittensor.core.tensor.tensor>)



# bittensor.core.tensor[#](<#module-bittensor.core.tensor> "Link to this heading")

## Attributes[#](<#attributes> "Link to this heading")

[`dtypes`](<#bittensor.core.tensor.dtypes> "bittensor.core.tensor.dtypes") |   
---|---  
  
## Classes[#](<#classes> "Link to this heading")

[`DTypes`](<#bittensor.core.tensor.DTypes> "bittensor.core.tensor.DTypes") | dict() -> new empty dictionary  
---|---  
[`Tensor`](<#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor") | Represents a Tensor object.  
[`tensor`](<#bittensor.core.tensor.tensor> "bittensor.core.tensor.tensor") |   
  
## Functions[#](<#functions> "Link to this heading")

[`cast_dtype`](<#bittensor.core.tensor.cast_dtype> "bittensor.core.tensor.cast_dtype")(raw) | Casts the raw value to a string representing the [numpy data type](<https://numpy.org/doc/stable/user/basics.types.html>), or the [torch data type](<https://pytorch.org/docs/stable/tensor_attributes.html>) if using torch.  
---|---  
[`cast_shape`](<#bittensor.core.tensor.cast_shape> "bittensor.core.tensor.cast_shape")(raw) | Casts the raw value to a string representing the tensor shape.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.tensor.DTypes(_* args_, _** kwargs_)[#](<#bittensor.core.tensor.DTypes> "Link to this definition")
    

Bases: [`dict`](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")

dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object’s

> (key, value) pairs

dict(iterable) -> new dictionary initialized as if via:
    

d = {} for k, v in iterable:

> d[k] = v

dict([**](<#id1>)kwargs) -> new dictionary initialized with the name=value pairs
    

in the keyword argument list. For example: dict(one=1, two=2)

Initialize self. See help(type(self)) for accurate signature.

torch: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)") = False[#](<#bittensor.core.tensor.DTypes.torch> "Link to this definition")
    

class bittensor.core.tensor.Tensor[#](<#bittensor.core.tensor.Tensor> "Link to this definition")
    

Bases: [`pydantic.BaseModel`](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel> "\(in Pydantic v0.0.0\)")

Represents a Tensor object.

Parameters:
    

  * **buffer** – Tensor buffer data.

  * **dtype** – Tensor data type.

  * **shape** – Tensor shape.




buffer: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.tensor.Tensor.buffer> "Link to this definition")
    

deserialize()[#](<#bittensor.core.tensor.Tensor.deserialize> "Link to this definition")
    

Deserializes the Tensor object.

Returns:
    

The deserialized tensor object.

Return type:
    

np.array or [torch.Tensor](<https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor> "\(in PyTorch v2.12\)")

Raises:
    

[**Exception**](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)") – If the deserialization process encounters an error.

dtype: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.tensor.Tensor.dtype> "Link to this definition")
    

model_config[#](<#bittensor.core.tensor.Tensor.model_config> "Link to this definition")
    

numpy()[#](<#bittensor.core.tensor.Tensor.numpy> "Link to this definition")
    

Return type:
    

[numpy.ndarray](<https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray> "\(in NumPy v2.4\)")

static serialize(_tensor__)[#](<#bittensor.core.tensor.Tensor.serialize> "Link to this definition")
    

Serializes the given tensor.

Parameters:
    

  * **tensor** – The tensor to serialize.

  * **tensor_** (_Union_ _[_[_numpy.ndarray_](<https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray> "\(in NumPy v2.4\)") _,__bittensor.utils.registration.torch.Tensor_ _]_)



Returns:
    

The serialized tensor.

Raises:
    

[**Exception**](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)") – If the serialization process encounters an error.

Return type:
    

[Tensor](<#bittensor.core.tensor.Tensor> "bittensor.core.tensor.Tensor")

shape: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")][#](<#bittensor.core.tensor.Tensor.shape> "Link to this definition")
    

tensor()[#](<#bittensor.core.tensor.Tensor.tensor> "Link to this definition")
    

Return type:
    

Union[[numpy.ndarray](<https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray> "\(in NumPy v2.4\)"), bittensor.utils.registration.torch.Tensor]

tolist()[#](<#bittensor.core.tensor.Tensor.tolist> "Link to this definition")
    

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[object](<https://docs.python.org/3/library/functions.html#object> "\(in Python v3.14\)")]

bittensor.core.tensor.cast_dtype(_raw_)[#](<#bittensor.core.tensor.cast_dtype> "Link to this definition")
    

Casts the raw value to a string representing the [numpy data type](<https://numpy.org/doc/stable/user/basics.types.html>), or the [torch data type](<https://pytorch.org/docs/stable/tensor_attributes.html>) if using torch.

Parameters:
    

**raw** (_Union_ _[__None_ _,_[_numpy.dtype_](<https://numpy.org/doc/stable/reference/generated/numpy.dtype.html#numpy.dtype> "\(in NumPy v2.4\)") _,__bittensor.utils.registration.torch.dtype_ _,_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The raw value to cast.

Returns:
    

The string representing the numpy/torch data type.

Raises:
    

[**Exception**](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)") – If the raw value is of an invalid type.

Return type:
    

Optional[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")]

bittensor.core.tensor.cast_shape(_raw_)[#](<#bittensor.core.tensor.cast_shape> "Link to this definition")
    

Casts the raw value to a string representing the tensor shape.

Parameters:
    

**raw** (_Union_ _[__None_ _,_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]__,_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The raw value to cast.

Returns:
    

The string representing the tensor shape.

Raises:
    

[**Exception**](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)") – If the raw value is of an invalid type or if the list elements are not of type int.

Return type:
    

Optional[Union[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")]]

bittensor.core.tensor.dtypes[#](<#bittensor.core.tensor.dtypes> "Link to this definition")
    

class bittensor.core.tensor.tensor[#](<#bittensor.core.tensor.tensor> "Link to this definition")
    

[ __ previous bittensor.core.synapse ](<../synapse/index.html> "previous page") [ next bittensor.core.threadpool __](<../threadpool/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`DTypes`](<#bittensor.core.tensor.DTypes>)
      * [`DTypes.torch`](<#bittensor.core.tensor.DTypes.torch>)
    * [`Tensor`](<#bittensor.core.tensor.Tensor>)
      * [`Tensor.buffer`](<#bittensor.core.tensor.Tensor.buffer>)
      * [`Tensor.deserialize()`](<#bittensor.core.tensor.Tensor.deserialize>)
      * [`Tensor.dtype`](<#bittensor.core.tensor.Tensor.dtype>)
      * [`Tensor.model_config`](<#bittensor.core.tensor.Tensor.model_config>)
      * [`Tensor.numpy()`](<#bittensor.core.tensor.Tensor.numpy>)
      * [`Tensor.serialize()`](<#bittensor.core.tensor.Tensor.serialize>)
      * [`Tensor.shape`](<#bittensor.core.tensor.Tensor.shape>)
      * [`Tensor.tensor()`](<#bittensor.core.tensor.Tensor.tensor>)
      * [`Tensor.tolist()`](<#bittensor.core.tensor.Tensor.tolist>)
    * [`cast_dtype()`](<#bittensor.core.tensor.cast_dtype>)
    * [`cast_shape()`](<#bittensor.core.tensor.cast_shape>)
    * [`dtypes`](<#bittensor.core.tensor.dtypes>)
    * [`tensor`](<#bittensor.core.tensor.tensor>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.