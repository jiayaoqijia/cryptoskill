# bittensor.core.synapse &#8212; Bittensor SDK Docs  documentation

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
        * [bittensor.core.synapse](<#>)
        * [bittensor.core.tensor](<../tensor/index.html>)
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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/synapse/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/synapse/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/core/synapse/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.synapse

##  Contents 

  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`Synapse`](<#bittensor.core.synapse.Synapse>)
      * [`Synapse.deserialize()`](<#bittensor.core.synapse.Synapse.deserialize>)
      * [`Synapse.__setattr__()`](<#bittensor.core.synapse.Synapse.__setattr__>)
      * [`Synapse.get_total_size()`](<#bittensor.core.synapse.Synapse.get_total_size>)
      * [`Synapse.to_headers()`](<#bittensor.core.synapse.Synapse.to_headers>)
      * [`Synapse.body_hash()`](<#bittensor.core.synapse.Synapse.body_hash>)
      * [`Synapse.parse_headers_to_inputs()`](<#bittensor.core.synapse.Synapse.parse_headers_to_inputs>)
      * [`Synapse.from_headers()`](<#bittensor.core.synapse.Synapse.from_headers>)
      * [`Synapse.axon`](<#bittensor.core.synapse.Synapse.axon>)
      * [`Synapse.body_hash`](<#id0>)
      * [`Synapse.computed_body_hash`](<#bittensor.core.synapse.Synapse.computed_body_hash>)
      * [`Synapse.dendrite`](<#bittensor.core.synapse.Synapse.dendrite>)
      * [`Synapse.deserialize()`](<#id1>)
      * [`Synapse.failed_verification`](<#bittensor.core.synapse.Synapse.failed_verification>)
      * [`Synapse.from_headers()`](<#id2>)
      * [`Synapse.get_required_fields()`](<#bittensor.core.synapse.Synapse.get_required_fields>)
      * [`Synapse.get_total_size()`](<#id3>)
      * [`Synapse.header_size`](<#bittensor.core.synapse.Synapse.header_size>)
      * [`Synapse.is_blacklist`](<#bittensor.core.synapse.Synapse.is_blacklist>)
      * [`Synapse.is_failure`](<#bittensor.core.synapse.Synapse.is_failure>)
      * [`Synapse.is_success`](<#bittensor.core.synapse.Synapse.is_success>)
      * [`Synapse.is_timeout`](<#bittensor.core.synapse.Synapse.is_timeout>)
      * [`Synapse.model_config`](<#bittensor.core.synapse.Synapse.model_config>)
      * [`Synapse.name`](<#bittensor.core.synapse.Synapse.name>)
      * [`Synapse.parse_headers_to_inputs()`](<#id4>)
      * [`Synapse.required_hash_fields`](<#bittensor.core.synapse.Synapse.required_hash_fields>)
      * [`Synapse.set_name_type()`](<#bittensor.core.synapse.Synapse.set_name_type>)
      * [`Synapse.timeout`](<#bittensor.core.synapse.Synapse.timeout>)
      * [`Synapse.to_headers()`](<#id5>)
      * [`Synapse.total_size`](<#bittensor.core.synapse.Synapse.total_size>)
    * [`TerminalInfo`](<#bittensor.core.synapse.TerminalInfo>)
      * [`TerminalInfo.hotkey`](<#bittensor.core.synapse.TerminalInfo.hotkey>)
      * [`TerminalInfo.ip`](<#bittensor.core.synapse.TerminalInfo.ip>)
      * [`TerminalInfo.model_config`](<#bittensor.core.synapse.TerminalInfo.model_config>)
      * [`TerminalInfo.nonce`](<#bittensor.core.synapse.TerminalInfo.nonce>)
      * [`TerminalInfo.port`](<#bittensor.core.synapse.TerminalInfo.port>)
      * [`TerminalInfo.process_time`](<#bittensor.core.synapse.TerminalInfo.process_time>)
      * [`TerminalInfo.signature`](<#bittensor.core.synapse.TerminalInfo.signature>)
      * [`TerminalInfo.status_code`](<#bittensor.core.synapse.TerminalInfo.status_code>)
      * [`TerminalInfo.status_message`](<#bittensor.core.synapse.TerminalInfo.status_message>)
      * [`TerminalInfo.uuid`](<#bittensor.core.synapse.TerminalInfo.uuid>)
      * [`TerminalInfo.version`](<#bittensor.core.synapse.TerminalInfo.version>)
    * [`cast_float()`](<#bittensor.core.synapse.cast_float>)
    * [`cast_int()`](<#bittensor.core.synapse.cast_int>)
    * [`get_size()`](<#bittensor.core.synapse.get_size>)



# bittensor.core.synapse[#](<#module-bittensor.core.synapse> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`Synapse`](<#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse") | Represents a Synapse in the Bittensor network, serving as a communication schema between neurons (nodes).  
---|---  
[`TerminalInfo`](<#bittensor.core.synapse.TerminalInfo> "bittensor.core.synapse.TerminalInfo") | TerminalInfo encapsulates detailed information about a network synapse (node) involved in a communication process.  
  
## Functions[#](<#functions> "Link to this heading")

[`cast_float`](<#bittensor.core.synapse.cast_float> "bittensor.core.synapse.cast_float")(raw) | Converts a string to a float, if the string is not `None`.  
---|---  
[`cast_int`](<#bittensor.core.synapse.cast_int> "bittensor.core.synapse.cast_int")(raw) | Converts a string to an integer, if the string is not `None`.  
[`get_size`](<#bittensor.core.synapse.get_size> "bittensor.core.synapse.get_size")(obj[, seen]) | Recursively finds size of objects.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.synapse.Synapse[#](<#bittensor.core.synapse.Synapse> "Link to this definition")
    

Bases: [`pydantic.BaseModel`](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel> "\(in Pydantic v0.0.0\)")

Represents a Synapse in the Bittensor network, serving as a communication schema between neurons (nodes).

Synapses ensure the format and correctness of transmission tensors according to the Bittensor protocol. Each Synapse type is tailored for a specific machine learning (ML) task, following unique compression and communication processes. This helps maintain sanitized, correct, and useful information flow across the network.

The Synapse class encompasses essential network properties such as HTTP route names, timeouts, request sizes, and terminal information. It also includes methods for serialization, deserialization, attribute setting, and hash computation, ensuring secure and efficient data exchange in the network.

The class includes Pydantic validators and root validators to enforce data integrity and format. Additionally, properties like `is_success`, `is_failure`, `is_timeout`, etc., provide convenient status checks based on dendrite responses.

Think of Bittensor Synapses as glorified pydantic wrappers that have been designed to be used in a distributed network. They provide a standardized way to communicate between neurons, and are the primary mechanism for communication between neurons in Bittensor.

Key Features:

  1. HTTP Route Name (`name` attribute):
    

Enables the identification and proper routing of requests within the network. Essential for users defining custom routes for specific machine learning tasks.

  2. Query Timeout (`timeout` attribute):
    

Determines the maximum duration allowed for a query, ensuring timely responses and network efficiency. Crucial for users to manage network latency and response times, particularly in time-sensitive applications.

  3. Request Sizes (`total_size`, `header_size` attributes):
    

Keeps track of the size of request bodies and headers, ensuring efficient data transmission without overloading the network. Important for users to monitor and optimize the data payload, especially in bandwidth-constrained environments.

  4. Terminal Information (`dendrite`, `axon` attributes):
    

Stores information about the dendrite (receiving end) and axon (sending end), facilitating communication between nodes. Users can access detailed information about the communication endpoints, aiding in debugging and network analysis.

  5. Body Hash Computation (`computed_body_hash`, `required_hash_fields`):
    

Ensures data integrity and security by computing hashes of transmitted data. Provides users with a mechanism to verify data integrity and detect any tampering during transmission. It is recommended that names of fields in required_hash_fields are listed in the order they are defined in the class.

  6. Serialization and Deserialization Methods:
    

Facilitates the conversion of Synapse objects to and from a format suitable for network transmission. Essential for users who need to customize data formats for specific machine learning models or tasks.

  7. Status Check Properties (`is_success`, `is_failure`, `is_timeout`, etc.):
    

Provides quick and easy methods to check the status of a request, improving error handling and response management. Users can efficiently handle different outcomes of network requests, enhancing the robustness of their applications.




Example usage:
[code] 
    # Creating a Synapse instance with default values
    from bittensor.core.synapse import Synapse
    
    synapse = Synapse()
    
    # Setting properties and input
    synapse.timeout = 15.0
    synapse.name = "MySynapse"
    
    # Not setting fields that are not defined in your synapse class will result in an error, e.g.:
    synapse.dummy_input = 1 # This will raise an error because dummy_input is not defined in the Synapse class
    
    # Get a dictionary of headers and body from the synapse instance
    synapse_dict = synapse.model_dump_json()
    
    # Get a dictionary of headers from the synapse instance
    headers = synapse.to_headers()
    
    # Reconstruct the synapse from headers using the classmethod 'from_headers'
    synapse = Synapse.from_headers(headers)
    
    # Deserialize synapse after receiving it over the network, controlled by `deserialize` method
    deserialized_synapse = synapse.deserialize()
    
    # Checking the status of the request
    if synapse.is_success:
        print("Request succeeded")
    
    # Checking and setting the status of the request
    print(synapse.axon.status_code)
    synapse.axon.status_code = 408 # Timeout
    
[/code]

Parameters:
    

  * **name** – HTTP route name, set on `axon.attach()`.

  * **timeout** – Total query length, set by the dendrite terminal.

  * **total_size** – Total size of request body in bytes.

  * **header_size** – Size of request header in bytes.

  * **dendrite** – Information about the dendrite terminal.

  * **axon** – Information about the axon terminal.

  * **computed_body_hash** – Computed hash of the request body.

  * **required_hash_fields** – Fields required to compute the body hash.




deserialize()[#](<#bittensor.core.synapse.Synapse.deserialize> "Link to this definition")
    

Custom deserialization logic for subclasses.

Return type:
    

[Synapse](<#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")

__setattr__()[#](<#bittensor.core.synapse.Synapse.__setattr__> "Link to this definition")
    

Override method to make `required_hash_fields` read-only.

Parameters:
    

  * **name** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

  * **value** ([_Any_](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any"))




get_total_size()[#](<#bittensor.core.synapse.Synapse.get_total_size> "Link to this definition")
    

Calculates and returns the total size of the object.

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

to_headers()[#](<#bittensor.core.synapse.Synapse.to_headers> "Link to this definition")
    

Constructs a dictionary of headers from instance properties.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")

body_hash()[#](<#bittensor.core.synapse.Synapse.body_hash> "Link to this definition")
    

Computes a SHA3-256 hash of the serialized body.

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

parse_headers_to_inputs()[#](<#bittensor.core.synapse.Synapse.parse_headers_to_inputs> "Link to this definition")
    

Parses headers to construct an inputs dictionary.

Parameters:
    

**headers** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)"))

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")

from_headers()[#](<#bittensor.core.synapse.Synapse.from_headers> "Link to this definition")
    

Creates an instance from a headers dictionary.

Parameters:
    

**headers** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)"))

Return type:
    

[Synapse](<#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")

This class is a cornerstone in the Bittensor framework, providing the necessary tools for secure, efficient, and standardized communication in a decentralized environment.

axon: [TerminalInfo](<#bittensor.core.synapse.TerminalInfo> "bittensor.core.synapse.TerminalInfo") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.Synapse.axon> "Link to this definition")
    

property body_hash: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#id0> "Link to this definition")
    

Computes a SHA3-256 hash of the serialized body of the Synapse instance.

This hash is used to ensure the data integrity and security of the Synapse instance when it’s transmitted across the network. It is a crucial feature for verifying that the data received is the same as the data sent.

Process:

  1. Iterates over each required field as specified in `required_hash_fields`.

  2. Concatenates the string representation of these fields.

  3. Applies SHA3-256 hashing to the concatenated string to produce a unique fingerprint of the data.




Example

synapse = Synapse(name=”ExampleRoute”, timeout=10) hash_value = synapse.body_hash # hash_value is the SHA3-256 hash of the serialized body of the Synapse instance

Returns:
    

The SHA3-256 hash as a hexadecimal string, providing a fingerprint of the Synapse instance’s data for
    

integrity checks.

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

computed_body_hash: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.Synapse.computed_body_hash> "Link to this definition")
    

dendrite: [TerminalInfo](<#bittensor.core.synapse.TerminalInfo> "bittensor.core.synapse.TerminalInfo") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.Synapse.dendrite> "Link to this definition")
    

deserialize()[#](<#id1> "Link to this definition")
    

Deserializes the Synapse object.

This method is intended to be overridden by subclasses for custom deserialization logic. In the context of the Synapse superclass, this method simply returns the instance itself. When inheriting from this class, subclasses should provide their own implementation for deserialization if specific deserialization behavior is desired.

By default, if a subclass does not provide its own implementation of this method, the Synapse’s deserialize method will be used, returning the object instance as-is.

In its default form, this method simply returns the instance of the Synapse itself without any modifications. Subclasses of Synapse can override this method to add specific deserialization behaviors, such as converting serialized data back into complex object types or performing additional data integrity checks.

Example

class CustomSynapse(Synapse):
    

additional_data: str

def deserialize(self) -> “CustomSynapse”:
    

# Custom deserialization logic # For example, decoding a base64 encoded string in ‘additional_data’ if self.additional_data:

> self.additional_data = base64.b64decode(self.additional_data).decode(‘utf-8’)

return self

serialized_data = ‘{“additional_data”: “SGVsbG8gV29ybGQ=”}’ # Base64 for ‘Hello World’ custom_synapse = CustomSynapse.model_validate_json(serialized_data) deserialized_synapse = custom_synapse.deserialize()

# deserialized_synapse.additional_data would now be ‘Hello World’

Returns:
    

The deserialized Synapse object. In this default implementation, it returns the object itself.

Return type:
    

[Synapse](<#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")

property failed_verification: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.Synapse.failed_verification> "Link to this definition")
    

Checks if the dendrite’s status code indicates failed verification.

This method returns `True` if the status code of the dendrite is `401`, which is the HTTP status code for unauthorized access.

Returns:
    

`True` if dendrite’s status code is `401`, `False` otherwise.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

classmethod from_headers(_headers_)[#](<#id2> "Link to this definition")
    

Constructs a new Synapse instance from a given headers dictionary, enabling the re-creation of the Synapse’s state as it was prior to network transmission.

This method is a key part of the deserialization process in the Bittensor network, allowing nodes to accurately reconstruct Synapse objects from received data.

Parameters:
    

**headers** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")) – The dictionary of headers containing serialized Synapse information.

Returns:
    

A new instance of Synapse, reconstructed from the parsed header information, replicating the original
    

instance’s state.

Return type:
    

[Synapse](<#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")

Example

received_headers = {
    

‘bt_header_axon_address’: ‘127.0.0.1’, ‘bt_header_dendrite_port’: ‘8080’, # Other headers…

} synapse = Synapse.from_headers(received_headers) # synapse is a new Synapse instance reconstructed from the received headers

get_required_fields()[#](<#bittensor.core.synapse.Synapse.get_required_fields> "Link to this definition")
    

Get the required fields from the model’s JSON schema.

get_total_size()[#](<#id3> "Link to this definition")
    

Get the total size of the current object.

This method first calculates the size of the current object, then assigns it to the instance variable `self.total_size()` and finally returns this value.

Returns:
    

The total size of the current object.

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

header_size: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.Synapse.header_size> "Link to this definition")
    

property is_blacklist: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.Synapse.is_blacklist> "Link to this definition")
    

Checks if the dendrite’s status code indicates a blacklisted request.

This method returns `True` if the status code of the dendrite is `403`, which is the HTTP status code for a forbidden request.

Returns:
    

`True` if dendrite’s status code is `403`, `False` otherwise.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

property is_failure: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.Synapse.is_failure> "Link to this definition")
    

Checks if the dendrite’s status code indicates failure.

This method returns `True` if the status code of the dendrite is not `200`, which would mean the HTTP request was not successful.

Returns:
    

`True` if dendrite’s status code is not `200`, `False` otherwise.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

property is_success: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.Synapse.is_success> "Link to this definition")
    

Checks if the dendrite’s status code indicates success.

This method returns `True` if the status code of the dendrite is `200`, which typically represents a successful HTTP request.

Returns:
    

`True` if dendrite’s status code is `200`, `False` otherwise.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

property is_timeout: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.Synapse.is_timeout> "Link to this definition")
    

Checks if the dendrite’s status code indicates a timeout.

This method returns `True` if the status code of the dendrite is `408`, which is the HTTP status code for a request timeout.

Returns:
    

`True` if dendrite’s status code is `408`, `False` otherwise.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

model_config[#](<#bittensor.core.synapse.Synapse.model_config> "Link to this definition")
    

name: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.Synapse.name> "Link to this definition")
    

classmethod parse_headers_to_inputs(_headers_)[#](<#id4> "Link to this definition")
    

Interprets and transforms a given dictionary of headers into a structured dictionary, facilitating the reconstruction of Synapse objects.

This method is essential for parsing network-transmitted data back into a Synapse instance, ensuring data consistency and integrity.

Parameters:
    

**headers** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")) – The headers dictionary to parse.

Returns:
    

A structured dictionary representing the inputs for constructing a Synapse instance.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")

Process:
    

  1. Separates headers into categories based on prefixes (`axon`, `dendrite`, etc.).

  2. Decodes and deserializes `input_obj` headers into their original objects.

  3. Assigns simple fields directly from the headers to the input dictionary.




Example

received_headers = {
    

‘bt_header_axon_address’: ‘127.0.0.1’, ‘bt_header_dendrite_port’: ‘8080’, # Other headers…

} inputs = Synapse.parse_headers_to_inputs(received_headers) # inputs now contains a structured representation of Synapse properties based on the headers

Note

This is handled automatically when calling `Synapse.from_headers(headers)()` and does not need to be called directly.

required_hash_fields: ClassVar[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), Ellipsis]] = ()[#](<#bittensor.core.synapse.Synapse.required_hash_fields> "Link to this definition")
    

set_name_type(_values_)[#](<#bittensor.core.synapse.Synapse.set_name_type> "Link to this definition")
    

Parameters:
    

**values** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)"))

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")

timeout: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.Synapse.timeout> "Link to this definition")
    

to_headers()[#](<#id5> "Link to this definition")
    

Converts the state of a Synapse instance into a dictionary of HTTP headers.

This method is essential for packaging Synapse data for network transmission in the Bittensor framework, ensuring that each key aspect of the Synapse is represented in a format suitable for HTTP communication.

Process:

1\. Basic Information: It starts by including the `name` and `timeout` of the Synapse, which are fundamental for identifying the query and managing its lifespan on the network. 2\. Complex Objects: The method serializes the `axon` and `dendrite` objects, if present, into strings. This serialization is crucial for preserving the state and structure of these objects over the network. 3\. Encoding: Non-optional complex objects are serialized and encoded in base64, making them safe for HTTP transport. 4\. Size Metrics: The method calculates and adds the size of headers and the total object size, providing valuable information for network bandwidth management.

Example Usage:
[code] 
    synapse = Synapse(name="ExampleSynapse", timeout=30)
    headers = synapse.to_headers()
    # headers now contains a dictionary representing the Synapse instance
    
[/code]

Returns:
    

A dictionary containing key-value pairs representing the Synapse’s properties, suitable for HTTP communication.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")

total_size: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.Synapse.total_size> "Link to this definition")
    

class bittensor.core.synapse.TerminalInfo[#](<#bittensor.core.synapse.TerminalInfo> "Link to this definition")
    

Bases: [`pydantic.BaseModel`](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel> "\(in Pydantic v0.0.0\)")

TerminalInfo encapsulates detailed information about a network synapse (node) involved in a communication process.

This class serves as a metadata carrier, providing essential details about the state and configuration of a terminal during network interactions. This is a

> crucial class in the Bittensor framework.

The TerminalInfo class contains information such as HTTP status codes and messages, processing times, IP addresses, ports, Bittensor version numbers, and unique identifiers. These details are vital for maintaining network reliability, security, and efficient data flow within the Bittensor network.

This class includes Pydantic validators and root validators to enforce data integrity and format. It is designed to be used natively within Synapses, so that you will not need to call this directly, but rather is used as a helper class for Synapses.

Parameters:
    

  * **status_code** – HTTP status code indicating the result of a network request. Essential for identifying the outcome of network interactions.

  * **status_message** – Descriptive message associated with the status code, providing additional context about the request’s result.

  * **process_time** – Time taken by the terminal to process the call, important for performance monitoring and optimization.

  * **ip** – IP address of the terminal, crucial for network routing and data transmission.

  * **port** – Network port used by the terminal, key for establishing network connections.

  * **version** – Bittensor version running on the terminal, ensuring compatibility between different nodes in the network.

  * **nonce** – Unique, monotonically increasing number for each terminal, aiding in identifying and ordering network interactions.

  * **uuid** – Unique identifier for the terminal, fundamental for network security and identification.

  * **hotkey** – Encoded hotkey string of the terminal wallet, important for transaction and identity verification in the network.

  * **signature** – Digital signature verifying the tuple of nonce, axon_hotkey, dendrite_hotkey, and uuid, critical for ensuring data authenticity and security.




Usage:
[code] 
    # Creating a TerminalInfo instance
    from bittensor.core.synapse import TerminalInfo
    
    terminal_info = TerminalInfo(
        status_code=200,
        status_message="Success",
        process_time=0.1,
        ip="198.123.23.1",
        port=9282,
        version=111,
        nonce=111111,
        uuid="5ecbd69c-1cec-11ee-b0dc-e29ce36fec1a",
        hotkey="5EnjDGNqqWnuL2HCAdxeEtN2oqtXZw6BMBe936Kfy2PFz1J1",
        signature="0x0813029319030129u4120u10841824y0182u091u230912u"
    )
    
    # Accessing TerminalInfo attributes
    ip_address = terminal_info.ip
    processing_duration = terminal_info.process_time
    
    # TerminalInfo can be used to monitor and verify network interactions, ensuring proper communication and
    security within the Bittensor network.
    
[/code]

TerminalInfo plays a pivotal role in providing transparency and control over network operations, making it an indispensable tool for developers and users interacting with the Bittensor ecosystem.

hotkey: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.TerminalInfo.hotkey> "Link to this definition")
    

ip: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.TerminalInfo.ip> "Link to this definition")
    

model_config[#](<#bittensor.core.synapse.TerminalInfo.model_config> "Link to this definition")
    

nonce: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.TerminalInfo.nonce> "Link to this definition")
    

port: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.TerminalInfo.port> "Link to this definition")
    

process_time: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.TerminalInfo.process_time> "Link to this definition")
    

signature: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.TerminalInfo.signature> "Link to this definition")
    

status_code: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.TerminalInfo.status_code> "Link to this definition")
    

status_message: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.TerminalInfo.status_message> "Link to this definition")
    

uuid: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.TerminalInfo.uuid> "Link to this definition")
    

version: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.synapse.TerminalInfo.version> "Link to this definition")
    

bittensor.core.synapse.cast_float(_raw_)[#](<#bittensor.core.synapse.cast_float> "Link to this definition")
    

Converts a string to a float, if the string is not `None`.

This function attempts to convert a string to a float. If the string is `None`, it simply returns `None`.

Parameters:
    

**raw** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The string to convert.

Returns:
    

The converted float, or `None` if the input was `None`.

Return type:
    

Optional[[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")]

bittensor.core.synapse.cast_int(_raw_)[#](<#bittensor.core.synapse.cast_int> "Link to this definition")
    

Converts a string to an integer, if the string is not `None`.

This function attempts to convert a string to an integer. If the string is `None`, it simply returns `None`.

Parameters:
    

**raw** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The string to convert.

Returns:
    

The converted integer, or `None` if the input was `None`.

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

bittensor.core.synapse.get_size(_obj_ , _seen =None_)[#](<#bittensor.core.synapse.get_size> "Link to this definition")
    

Recursively finds size of objects.

This function traverses every item of a given object and sums their sizes to compute the total size.

Parameters:
    

  * **obj** ([_Any_](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any")) – The object to get the size of.

  * **seen** (_Optional_ _[_[_set_](<https://docs.python.org/3/library/stdtypes.html#set> "\(in Python v3.14\)") _]_) – Set of object ids that have been calculated.



Returns:
    

The total size of the object.

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

[ __ previous bittensor.core.subtensor ](<../subtensor/index.html> "previous page") [ next bittensor.core.tensor __](<../tensor/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`Synapse`](<#bittensor.core.synapse.Synapse>)
      * [`Synapse.deserialize()`](<#bittensor.core.synapse.Synapse.deserialize>)
      * [`Synapse.__setattr__()`](<#bittensor.core.synapse.Synapse.__setattr__>)
      * [`Synapse.get_total_size()`](<#bittensor.core.synapse.Synapse.get_total_size>)
      * [`Synapse.to_headers()`](<#bittensor.core.synapse.Synapse.to_headers>)
      * [`Synapse.body_hash()`](<#bittensor.core.synapse.Synapse.body_hash>)
      * [`Synapse.parse_headers_to_inputs()`](<#bittensor.core.synapse.Synapse.parse_headers_to_inputs>)
      * [`Synapse.from_headers()`](<#bittensor.core.synapse.Synapse.from_headers>)
      * [`Synapse.axon`](<#bittensor.core.synapse.Synapse.axon>)
      * [`Synapse.body_hash`](<#id0>)
      * [`Synapse.computed_body_hash`](<#bittensor.core.synapse.Synapse.computed_body_hash>)
      * [`Synapse.dendrite`](<#bittensor.core.synapse.Synapse.dendrite>)
      * [`Synapse.deserialize()`](<#id1>)
      * [`Synapse.failed_verification`](<#bittensor.core.synapse.Synapse.failed_verification>)
      * [`Synapse.from_headers()`](<#id2>)
      * [`Synapse.get_required_fields()`](<#bittensor.core.synapse.Synapse.get_required_fields>)
      * [`Synapse.get_total_size()`](<#id3>)
      * [`Synapse.header_size`](<#bittensor.core.synapse.Synapse.header_size>)
      * [`Synapse.is_blacklist`](<#bittensor.core.synapse.Synapse.is_blacklist>)
      * [`Synapse.is_failure`](<#bittensor.core.synapse.Synapse.is_failure>)
      * [`Synapse.is_success`](<#bittensor.core.synapse.Synapse.is_success>)
      * [`Synapse.is_timeout`](<#bittensor.core.synapse.Synapse.is_timeout>)
      * [`Synapse.model_config`](<#bittensor.core.synapse.Synapse.model_config>)
      * [`Synapse.name`](<#bittensor.core.synapse.Synapse.name>)
      * [`Synapse.parse_headers_to_inputs()`](<#id4>)
      * [`Synapse.required_hash_fields`](<#bittensor.core.synapse.Synapse.required_hash_fields>)
      * [`Synapse.set_name_type()`](<#bittensor.core.synapse.Synapse.set_name_type>)
      * [`Synapse.timeout`](<#bittensor.core.synapse.Synapse.timeout>)
      * [`Synapse.to_headers()`](<#id5>)
      * [`Synapse.total_size`](<#bittensor.core.synapse.Synapse.total_size>)
    * [`TerminalInfo`](<#bittensor.core.synapse.TerminalInfo>)
      * [`TerminalInfo.hotkey`](<#bittensor.core.synapse.TerminalInfo.hotkey>)
      * [`TerminalInfo.ip`](<#bittensor.core.synapse.TerminalInfo.ip>)
      * [`TerminalInfo.model_config`](<#bittensor.core.synapse.TerminalInfo.model_config>)
      * [`TerminalInfo.nonce`](<#bittensor.core.synapse.TerminalInfo.nonce>)
      * [`TerminalInfo.port`](<#bittensor.core.synapse.TerminalInfo.port>)
      * [`TerminalInfo.process_time`](<#bittensor.core.synapse.TerminalInfo.process_time>)
      * [`TerminalInfo.signature`](<#bittensor.core.synapse.TerminalInfo.signature>)
      * [`TerminalInfo.status_code`](<#bittensor.core.synapse.TerminalInfo.status_code>)
      * [`TerminalInfo.status_message`](<#bittensor.core.synapse.TerminalInfo.status_message>)
      * [`TerminalInfo.uuid`](<#bittensor.core.synapse.TerminalInfo.uuid>)
      * [`TerminalInfo.version`](<#bittensor.core.synapse.TerminalInfo.version>)
    * [`cast_float()`](<#bittensor.core.synapse.cast_float>)
    * [`cast_int()`](<#bittensor.core.synapse.cast_int>)
    * [`get_size()`](<#bittensor.core.synapse.get_size>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.