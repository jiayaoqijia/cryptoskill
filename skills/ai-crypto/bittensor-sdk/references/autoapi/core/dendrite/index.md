# bittensor.core.dendrite &#8212; Bittensor SDK Docs  documentation

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
        * [bittensor.core.dendrite](<#>)
        * [bittensor.core.errors](<../errors/index.html>)
        * [bittensor.core.extrinsics](<../extrinsics/index.html>)
        * [bittensor.core.metagraph](<../metagraph/index.html>)
        * [bittensor.core.settings](<../settings/index.html>)
        * [bittensor.core.stream](<../stream/index.html>)
        * [bittensor.core.subtensor](<../subtensor/index.html>)
        * [bittensor.core.synapse](<../synapse/index.html>)
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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/dendrite/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/dendrite/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/core/dendrite/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.dendrite

##  Contents 

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`BaseModel`](<#bittensor.core.dendrite.BaseModel>)
    * [`DENDRITE_DEFAULT_ERROR`](<#bittensor.core.dendrite.DENDRITE_DEFAULT_ERROR>)
    * [`DENDRITE_ERROR_MAPPING`](<#bittensor.core.dendrite.DENDRITE_ERROR_MAPPING>)
    * [`Dendrite`](<#bittensor.core.dendrite.Dendrite>)
      * [`Dendrite.__str__()`](<#bittensor.core.dendrite.Dendrite.__str__>)
      * [`Dendrite.__repr__()`](<#bittensor.core.dendrite.Dendrite.__repr__>)
      * [`Dendrite.query()`](<#bittensor.core.dendrite.Dendrite.query>)
      * [`Dendrite.forward()`](<#bittensor.core.dendrite.Dendrite.forward>)
      * [`Dendrite.call()`](<#bittensor.core.dendrite.Dendrite.call>)
      * [`Dendrite.call_stream()`](<#bittensor.core.dendrite.Dendrite.call_stream>)
      * [`Dendrite.preprocess_synapse_for_request()`](<#bittensor.core.dendrite.Dendrite.preprocess_synapse_for_request>)
      * [`Dendrite.process_server_response()`](<#bittensor.core.dendrite.Dendrite.process_server_response>)
      * [`Dendrite.close_session()`](<#bittensor.core.dendrite.Dendrite.close_session>)
      * [`Dendrite.aclose_session()`](<#bittensor.core.dendrite.Dendrite.aclose_session>)
    * [`DendriteMixin`](<#bittensor.core.dendrite.DendriteMixin>)
      * [`DendriteMixin.__str__()`](<#bittensor.core.dendrite.DendriteMixin.__str__>)
      * [`DendriteMixin.__repr__()`](<#bittensor.core.dendrite.DendriteMixin.__repr__>)
      * [`DendriteMixin.query()`](<#bittensor.core.dendrite.DendriteMixin.query>)
      * [`DendriteMixin.forward()`](<#bittensor.core.dendrite.DendriteMixin.forward>)
      * [`DendriteMixin.call()`](<#bittensor.core.dendrite.DendriteMixin.call>)
      * [`DendriteMixin.call_stream()`](<#bittensor.core.dendrite.DendriteMixin.call_stream>)
      * [`DendriteMixin.preprocess_synapse_for_request()`](<#bittensor.core.dendrite.DendriteMixin.preprocess_synapse_for_request>)
      * [`DendriteMixin.process_server_response()`](<#bittensor.core.dendrite.DendriteMixin.process_server_response>)
      * [`DendriteMixin.close_session()`](<#bittensor.core.dendrite.DendriteMixin.close_session>)
      * [`DendriteMixin.aclose_session()`](<#bittensor.core.dendrite.DendriteMixin.aclose_session>)
      * [`DendriteMixin.aclose_session()`](<#id0>)
      * [`DendriteMixin.aquery()`](<#bittensor.core.dendrite.DendriteMixin.aquery>)
      * [`DendriteMixin.call()`](<#id3>)
      * [`DendriteMixin.call_stream()`](<#id4>)
      * [`DendriteMixin.close_session()`](<#id5>)
      * [`DendriteMixin.external_ip`](<#bittensor.core.dendrite.DendriteMixin.external_ip>)
      * [`DendriteMixin.forward()`](<#id7>)
      * [`DendriteMixin.keypair`](<#bittensor.core.dendrite.DendriteMixin.keypair>)
      * [`DendriteMixin.log_exception()`](<#bittensor.core.dendrite.DendriteMixin.log_exception>)
      * [`DendriteMixin.preprocess_synapse_for_request()`](<#id8>)
      * [`DendriteMixin.process_error_message()`](<#bittensor.core.dendrite.DendriteMixin.process_error_message>)
      * [`DendriteMixin.process_server_response()`](<#id9>)
      * [`DendriteMixin.query()`](<#id11>)
      * [`DendriteMixin.session`](<#bittensor.core.dendrite.DendriteMixin.session>)
      * [`DendriteMixin.synapse_history`](<#bittensor.core.dendrite.DendriteMixin.synapse_history>)
      * [`DendriteMixin.uuid`](<#bittensor.core.dendrite.DendriteMixin.uuid>)
    * [`call()`](<#bittensor.core.dendrite.call>)
    * [`event_loop_is_running()`](<#bittensor.core.dendrite.event_loop_is_running>)



# bittensor.core.dendrite[#](<#module-bittensor.core.dendrite> "Link to this heading")

## Attributes[#](<#attributes> "Link to this heading")

[`BaseModel`](<#bittensor.core.dendrite.BaseModel> "bittensor.core.dendrite.BaseModel") |   
---|---  
[`DENDRITE_DEFAULT_ERROR`](<#bittensor.core.dendrite.DENDRITE_DEFAULT_ERROR> "bittensor.core.dendrite.DENDRITE_DEFAULT_ERROR") |   
[`DENDRITE_ERROR_MAPPING`](<#bittensor.core.dendrite.DENDRITE_ERROR_MAPPING> "bittensor.core.dendrite.DENDRITE_ERROR_MAPPING") |   
  
## Classes[#](<#classes> "Link to this heading")

[`Dendrite`](<#bittensor.core.dendrite.Dendrite> "bittensor.core.dendrite.Dendrite") | The Dendrite class represents the abstracted implementation of a network client module.  
---|---  
[`DendriteMixin`](<#bittensor.core.dendrite.DendriteMixin> "bittensor.core.dendrite.DendriteMixin") | The Dendrite class represents the abstracted implementation of a network client module.  
  
## Functions[#](<#functions> "Link to this heading")

[`call`](<#bittensor.core.dendrite.call> "bittensor.core.dendrite.call")(self, *args, **kwargs) |   
---|---  
[`event_loop_is_running`](<#bittensor.core.dendrite.event_loop_is_running> "bittensor.core.dendrite.event_loop_is_running")() |   
  
## Module Contents[#](<#module-contents> "Link to this heading")

bittensor.core.dendrite.BaseModel: bittensor.utils.registration.torch.nn.Module | [object](<https://docs.python.org/3/library/functions.html#object> "\(in Python v3.14\)")[#](<#bittensor.core.dendrite.BaseModel> "Link to this definition")
    

bittensor.core.dendrite.DENDRITE_DEFAULT_ERROR = ('422', 'Failed to parse response')[#](<#bittensor.core.dendrite.DENDRITE_DEFAULT_ERROR> "Link to this definition")
    

bittensor.core.dendrite.DENDRITE_ERROR_MAPPING: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[Type[[Exception](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)")], [tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")][#](<#bittensor.core.dendrite.DENDRITE_ERROR_MAPPING> "Link to this definition")
    

class bittensor.core.dendrite.Dendrite(_wallet =None_)[#](<#bittensor.core.dendrite.Dendrite> "Link to this definition")
    

Bases: [`DendriteMixin`](<#bittensor.core.dendrite.DendriteMixin> "bittensor.core.dendrite.DendriteMixin"), [`BaseModel`](<#bittensor.core.dendrite.BaseModel> "bittensor.core.dendrite.BaseModel")

The Dendrite class represents the abstracted implementation of a network client module.

In the brain analogy, dendrites receive signals from other neurons (in this case, network servers or axons), and the Dendrite class here is designed to send requests to those endpoint to receive inputs.

This class includes a wallet or keypair used for signing messages, and methods for making HTTP requests to the network servers. It also provides functionalities such as logging network requests and processing server responses.

Parameters:
    

  * **keypair** – The wallet or keypair used for signing messages.

  * **external_ip** – The external IP address of the local system.

  * **synapse_history** – A list of Synapse objects representing the historical responses.

  * **wallet** (_Optional_ _[__Union_ _[__bittensor_wallet.Wallet_ _,__bittensor_wallet.Keypair_ _]__]_)




__str__()[#](<#bittensor.core.dendrite.Dendrite.__str__> "Link to this definition")
    

Returns a string representation of the Dendrite object.

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

__repr__()[#](<#bittensor.core.dendrite.Dendrite.__repr__> "Link to this definition")
    

Returns a string representation of the Dendrite object, acting as a fallback for __str__().

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

query(_self_ , _* args_, _** kwargs_) → [Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse") | [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")][#](<#bittensor.core.dendrite.Dendrite.query> "Link to this definition")
    

Makes synchronous requests to one or multiple target Axons and returns responses.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[Union[AsyncGenerator[[Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any"), [Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any")], [bittensor.core.synapse.Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse"), [bittensor.core.stream.StreamingSynapse](<../stream/index.html#bittensor.core.stream.StreamingSynapse> "bittensor.core.stream.StreamingSynapse")]]

forward(_self_ , _axons_ , _synapse =Synapse()_, _timeout =12_, _deserialize =True_, _run_async =True_, _streaming =False_)[#](<#bittensor.core.dendrite.Dendrite.forward> "Link to this definition")
    

Synapse: Asynchronously sends requests to one or multiple Axons and collates their responses.

Parameters:
    

  * **axons** (_Union_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[__Union_ _[__bittensor.core.chain_data.AxonInfo_ _,_[_bittensor.core.axon.Axon_](<../axon/index.html#bittensor.core.axon.Axon> "bittensor.core.axon.Axon") _]__]__,__Union_ _[__bittensor.core.chain_data.AxonInfo_ _,_[_bittensor.core.axon.Axon_](<../axon/index.html#bittensor.core.axon.Axon> "bittensor.core.axon.Axon") _]__]_)

  * **synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse"))

  * **timeout** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

  * **deserialize** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **run_async** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **streaming** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))



Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[Union[AsyncGenerator[[Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any"), [Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any")], [bittensor.core.synapse.Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse"), [bittensor.core.stream.StreamingSynapse](<../stream/index.html#bittensor.core.stream.StreamingSynapse> "bittensor.core.stream.StreamingSynapse")]]

call(_self_ , _target_axon_ , _synapse =Synapse()_, _timeout =12.0_, _deserialize =True_) → [Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")[#](<#bittensor.core.dendrite.Dendrite.call> "Link to this definition")
    

Asynchronously sends a request to a specified Axon and processes the response.

Parameters:
    

  * **target_axon** (_Union_ _[__bittensor.core.chain_data.AxonInfo_ _,_[_bittensor.core.axon.Axon_](<../axon/index.html#bittensor.core.axon.Axon> "bittensor.core.axon.Axon") _]_)

  * **synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse"))

  * **timeout** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

  * **deserialize** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))



Return type:
    

[bittensor.core.synapse.Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")

call_stream(_self_ , _target_axon_ , _synapse =Synapse()_, _timeout =12.0_, _deserialize =True_)[#](<#bittensor.core.dendrite.Dendrite.call_stream> "Link to this definition")
    

AsyncGenerator[Synapse, None]: Sends a request to a specified Axon and yields an AsyncGenerator that contains streaming response chunks before finally yielding the filled Synapse as the final element.

Parameters:
    

  * **target_axon** (_Union_ _[__bittensor.core.chain_data.AxonInfo_ _,_[_bittensor.core.axon.Axon_](<../axon/index.html#bittensor.core.axon.Axon> "bittensor.core.axon.Axon") _]_)

  * **synapse** ([_bittensor.core.stream.StreamingSynapse_](<../stream/index.html#bittensor.core.stream.StreamingSynapse> "bittensor.core.stream.StreamingSynapse"))

  * **timeout** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

  * **deserialize** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))



Return type:
    

AsyncGenerator[[Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any"), [Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any")]

preprocess_synapse_for_request(_self_ , _target_axon_info_ , _synapse_ , _timeout =12.0_) → [Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")[#](<#bittensor.core.dendrite.Dendrite.preprocess_synapse_for_request> "Link to this definition")
    

Preprocesses the synapse for making a request, including building headers and signing.

Parameters:
    

  * **target_axon_info** (_bittensor.core.chain_data.AxonInfo_)

  * **synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse"))

  * **timeout** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))



Return type:
    

[bittensor.core.synapse.Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")

process_server_response(_self_ , _server_response_ , _json_response_ , _local_synapse_)[#](<#bittensor.core.dendrite.Dendrite.process_server_response> "Link to this definition")
    

Processes the server response, updates the local synapse state, and merges headers.

Parameters:
    

  * **server_response** (_aiohttp.ClientResponse_)

  * **json_response** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)"))

  * **local_synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse"))




close_session(_self_)[#](<#bittensor.core.dendrite.Dendrite.close_session> "Link to this definition")
    

Synchronously closes the internal aiohttp client session.

Parameters:
    

**using_new_loop** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

aclose_session(_self_)[#](<#bittensor.core.dendrite.Dendrite.aclose_session> "Link to this definition")
    

Asynchronously closes the internal aiohttp client session.

Note

When working with async [aiohttp](<https://github.com/aio-libs/aiohttp>) client sessions, it is recommended to use a context manager.

Example with a context manager:
[code] 
    async with dendrite(wallet = bittensor_wallet.Wallet()) as d:
        print(d)
        d( <axon> ) # ping axon
        d( [<axons>] ) # ping multiple
        d( Axon(), Synapse )
    
[/code]

However, you are able to safely call `dendrite.query()` without a context manager in a synchronous setting.

Example without a context manager:
[code] 
    d = dendrite(wallet = bittensor_wallet.Wallet() )
    print(d)
    d( <axon> ) # ping axon
    d( [<axons>] ) # ping multiple
    d( bittensor.core.axon.Axon, bittensor.core.synapse.Synapse )
    
[/code]

Initializes the Dendrite object, setting up essential properties.

Parameters:
    

**wallet** (_Optional_ _[__Union_ _[__bittensor_wallet.Wallet_ _,__bittensor_wallet.Keypair_ _]__]_) – The user’s wallet or keypair used for signing messages.

class bittensor.core.dendrite.DendriteMixin(_wallet =None_)[#](<#bittensor.core.dendrite.DendriteMixin> "Link to this definition")
    

The Dendrite class represents the abstracted implementation of a network client module.

In the brain analogy, dendrites receive signals from other neurons (in this case, network servers or axons), and the Dendrite class here is designed to send requests to those endpoint to receive inputs.

This class includes a wallet or keypair used for signing messages, and methods for making HTTP requests to the network servers. It also provides functionalities such as logging network requests and processing server responses.

Parameters:
    

  * **keypair** – The wallet or keypair used for signing messages.

  * **external_ip** – The external IP address of the local system.

  * **synapse_history** – A list of Synapse objects representing the historical responses.

  * **wallet** (_Optional_ _[__Union_ _[__bittensor_wallet.Wallet_ _,__bittensor_wallet.Keypair_ _]__]_)




__str__()[#](<#bittensor.core.dendrite.DendriteMixin.__str__> "Link to this definition")
    

Returns a string representation of the Dendrite object.

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

__repr__()[#](<#bittensor.core.dendrite.DendriteMixin.__repr__> "Link to this definition")
    

Returns a string representation of the Dendrite object, acting as a fallback for __str__().

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

query(_self_ , _* args_, _** kwargs_) → [Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse") | [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")][#](<#bittensor.core.dendrite.DendriteMixin.query> "Link to this definition")
    

Makes synchronous requests to one or multiple target Axons and returns responses.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[Union[AsyncGenerator[[Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any"), [Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any")], [bittensor.core.synapse.Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse"), [bittensor.core.stream.StreamingSynapse](<../stream/index.html#bittensor.core.stream.StreamingSynapse> "bittensor.core.stream.StreamingSynapse")]]

forward(_self_ , _axons_ , _synapse =Synapse()_, _timeout =12_, _deserialize =True_, _run_async =True_, _streaming =False_)[#](<#bittensor.core.dendrite.DendriteMixin.forward> "Link to this definition")
    

Synapse: Asynchronously sends requests to one or multiple Axons and collates their responses.

Parameters:
    

  * **axons** (_Union_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[__Union_ _[__bittensor.core.chain_data.AxonInfo_ _,_[_bittensor.core.axon.Axon_](<../axon/index.html#bittensor.core.axon.Axon> "bittensor.core.axon.Axon") _]__]__,__Union_ _[__bittensor.core.chain_data.AxonInfo_ _,_[_bittensor.core.axon.Axon_](<../axon/index.html#bittensor.core.axon.Axon> "bittensor.core.axon.Axon") _]__]_)

  * **synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse"))

  * **timeout** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

  * **deserialize** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **run_async** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **streaming** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))



Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[Union[AsyncGenerator[[Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any"), [Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any")], [bittensor.core.synapse.Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse"), [bittensor.core.stream.StreamingSynapse](<../stream/index.html#bittensor.core.stream.StreamingSynapse> "bittensor.core.stream.StreamingSynapse")]]

call(_self_ , _target_axon_ , _synapse =Synapse()_, _timeout =12.0_, _deserialize =True_) → [Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")[#](<#bittensor.core.dendrite.DendriteMixin.call> "Link to this definition")
    

Asynchronously sends a request to a specified Axon and processes the response.

Parameters:
    

  * **target_axon** (_Union_ _[__bittensor.core.chain_data.AxonInfo_ _,_[_bittensor.core.axon.Axon_](<../axon/index.html#bittensor.core.axon.Axon> "bittensor.core.axon.Axon") _]_)

  * **synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse"))

  * **timeout** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

  * **deserialize** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))



Return type:
    

[bittensor.core.synapse.Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")

call_stream(_self_ , _target_axon_ , _synapse =Synapse()_, _timeout =12.0_, _deserialize =True_)[#](<#bittensor.core.dendrite.DendriteMixin.call_stream> "Link to this definition")
    

AsyncGenerator[Synapse, None]: Sends a request to a specified Axon and yields an AsyncGenerator that contains streaming response chunks before finally yielding the filled Synapse as the final element.

Parameters:
    

  * **target_axon** (_Union_ _[__bittensor.core.chain_data.AxonInfo_ _,_[_bittensor.core.axon.Axon_](<../axon/index.html#bittensor.core.axon.Axon> "bittensor.core.axon.Axon") _]_)

  * **synapse** ([_bittensor.core.stream.StreamingSynapse_](<../stream/index.html#bittensor.core.stream.StreamingSynapse> "bittensor.core.stream.StreamingSynapse"))

  * **timeout** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

  * **deserialize** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))



Return type:
    

AsyncGenerator[[Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any"), [Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any")]

preprocess_synapse_for_request(_self_ , _target_axon_info_ , _synapse_ , _timeout =12.0_) → [Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")[#](<#bittensor.core.dendrite.DendriteMixin.preprocess_synapse_for_request> "Link to this definition")
    

Preprocesses the synapse for making a request, including building headers and signing.

Parameters:
    

  * **target_axon_info** (_bittensor.core.chain_data.AxonInfo_)

  * **synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse"))

  * **timeout** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))



Return type:
    

[bittensor.core.synapse.Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")

process_server_response(_self_ , _server_response_ , _json_response_ , _local_synapse_)[#](<#bittensor.core.dendrite.DendriteMixin.process_server_response> "Link to this definition")
    

Processes the server response, updates the local synapse state, and merges headers.

Parameters:
    

  * **server_response** (_aiohttp.ClientResponse_)

  * **json_response** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)"))

  * **local_synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse"))




close_session(_self_)[#](<#bittensor.core.dendrite.DendriteMixin.close_session> "Link to this definition")
    

Synchronously closes the internal aiohttp client session.

Parameters:
    

**using_new_loop** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

aclose_session(_self_)[#](<#bittensor.core.dendrite.DendriteMixin.aclose_session> "Link to this definition")
    

Asynchronously closes the internal aiohttp client session.

Note

When working with async [aiohttp](<https://github.com/aio-libs/aiohttp>) client sessions, it is recommended to use a context manager.

Example with a context manager:
[code] 
    async with dendrite(wallet = bittensor_wallet.Wallet()) as d:
        print(d)
        d( <axon> ) # ping axon
        d( [<axons>] ) # ping multiple
        d( Axon(), Synapse )
    
[/code]

However, you are able to safely call `dendrite.query()` without a context manager in a synchronous setting.

Example without a context manager:
[code] 
    d = dendrite(wallet = bittensor_wallet.Wallet() )
    print(d)
    d( <axon> ) # ping axon
    d( [<axons>] ) # ping multiple
    d( bittensor.core.axon.Axon, bittensor.core.synapse.Synapse )
    
[/code]

Initializes the Dendrite object, setting up essential properties.

Parameters:
    

**wallet** (_Optional_ _[__Union_ _[__bittensor_wallet.Wallet_ _,__bittensor_wallet.Keypair_ _]__]_) – The user’s wallet or keypair used for signing messages.

async aclose_session()[#](<#id0> "Link to this definition")
    

Asynchronously closes the internal [aiohttp](<https://github.com/aio-libs/aiohttp>) client session.

This method is the asynchronous counterpart to the [`close_session()`](<#id5> "bittensor.core.dendrite.DendriteMixin.close_session") method. It should be used in asynchronous contexts to ensure that the aiohttp client session is closed properly. The method releases resources associated with the session, such as open connections and internal buffers, which is essential for resource management in asynchronous applications.

Example

Usage::
    

When finished with dendrite in an asynchronous context await `dendrite_instance.aclose_session()`.

Example

Usage::
    

async with dendrite_instance:
    

# Operations using dendrite pass

# The session will be closed automatically after the above block

async aquery(_* args_, _** kwargs_)[#](<#bittensor.core.dendrite.DendriteMixin.aquery> "Link to this definition")
    

async call(_target_axon_ , _synapse =Synapse()_, _timeout =12.0_, _deserialize =True_)[#](<#id3> "Link to this definition")
    

Asynchronously sends a request to a specified Axon and processes the response.

This function establishes a connection with a specified Axon, sends the encapsulated data through the Synapse object, waits for a response, processes it, and then returns the updated Synapse object.

Parameters:
    

  * **target_axon** (_Union_ _[__bittensor.core.chain_data.AxonInfo_ _,_[_bittensor.core.axon.Axon_](<../axon/index.html#bittensor.core.axon.Axon> "bittensor.core.axon.Axon") _]_) – The target Axon to send the request to.

  * **synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")) – The Synapse object encapsulating the data.

  * **timeout** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")) – Maximum duration to wait for a response from the Axon in seconds.

  * **deserialize** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Determines if the received response should be deserialized.



Returns:
    

The Synapse object, updated with the response data from the Axon.

Return type:
    

[bittensor.core.synapse.Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")

async call_stream(_target_axon_ , _synapse =Synapse()_, _timeout =12.0_, _deserialize =True_)[#](<#id4> "Link to this definition")
    

Sends a request to a specified Axon and yields streaming responses.

Similar to `call`, but designed for scenarios where the Axon sends back data in multiple chunks or streams. The function yields each chunk as it is received. This is useful for processing large responses piece by piece without waiting for the entire data to be transmitted.

Parameters:
    

  * **target_axon** (_Union_ _[__bittensor.core.chain_data.AxonInfo_ _,_[_bittensor.core.axon.Axon_](<../axon/index.html#bittensor.core.axon.Axon> "bittensor.core.axon.Axon") _]_) – The target Axon to send the request to.

  * **synapse** ([_bittensor.core.stream.StreamingSynapse_](<../stream/index.html#bittensor.core.stream.StreamingSynapse> "bittensor.core.stream.StreamingSynapse")) – The Synapse object encapsulating the data.

  * **timeout** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")) – Maximum duration to wait for a response (or a chunk of the response) from the Axon in seconds.

  * **deserialize** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Determines if each received chunk should be deserialized.



Yields:
    

_object_ – Each yielded object contains a chunk of the arbitrary response data from the Axon. bittensor.core.synapse.Synapse: After the AsyncGenerator has been exhausted, yields the final filled Synapse.

Return type:
    

AsyncGenerator[[Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any"), [Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any")]

close_session(_using_new_loop =False_)[#](<#id5> "Link to this definition")
    

Closes the internal [aiohttp](<https://github.com/aio-libs/aiohttp>) client session synchronously.

This method ensures the proper closure and cleanup of the aiohttp client session, releasing any resources like open connections and internal buffers. It is crucial for preventing resource leakage and should be called when the dendrite instance is no longer in use, especially in synchronous contexts.

Parameters:
    

**using_new_loop** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – A flag to determine whether this has been called with a new event loop rather than the default. This will indicate whether to close this event loop at the end of this call.

Note

This method utilizes asyncio’s event loop to close the session asynchronously from a synchronous context. It is advisable to use this method only when asynchronous context management is not feasible.

Usage:
    

When finished with dendrite in a synchronous context `dendrite_instance.close_session()`.

external_ip[#](<#bittensor.core.dendrite.DendriteMixin.external_ip> "Link to this definition")
    

async forward(_axons_ , _synapse =Synapse()_, _timeout =12_, _deserialize =True_, _run_async =True_, _streaming =False_)[#](<#id7> "Link to this definition")
    

Asynchronously sends requests to one or multiple Axons and collates their responses.

This function acts as a bridge for sending multiple requests concurrently or sequentially based on the provided parameters. It checks the type of the target Axons, preprocesses the requests, and then sends them off. After getting the responses, it processes and collates them into a unified format.

When querying an Axon that sends a single response, this function returns a Synapse object containing the response data. If multiple Axons are queried, a list of Synapse objects is returned, each containing the response from the corresponding Axon.

Example

… import bittensor wallet = bittensor.Wallet() # Initialize a wallet synapse = bittensor.Synapse(…) # Create a synapse object that contains query data dendrite = bittensor.Dendrite(wallet = wallet) # Initialize a dendrite instance netuid = … # Provide subnet ID metagraph = bittensor.Metagraph(netuid) # Initialize a metagraph instance axons = metagraph.axons # Create a list of axons to query responses = await dendrite(axons, synapse) # Send the query to all axons and await the responses

When querying an Axon that sends back data in chunks using the Dendrite, this function returns an AsyncGenerator that yields each chunk as it is received. The generator can be iterated over to process each chunk individually.

Example

… dendrite = bittensor.Dendrite(wallet = wallet) async for chunk in dendrite.forward(axons, synapse, timeout, deserialize, run_async, streaming):

> # Process each chunk here print(chunk)

Parameters:
    

  * **axons** (_Union_ _[_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[__Union_ _[__bittensor.core.chain_data.AxonInfo_ _,_[_bittensor.core.axon.Axon_](<../axon/index.html#bittensor.core.axon.Axon> "bittensor.core.axon.Axon") _]__]__,__Union_ _[__bittensor.core.chain_data.AxonInfo_ _,_[_bittensor.core.axon.Axon_](<../axon/index.html#bittensor.core.axon.Axon> "bittensor.core.axon.Axon") _]__]_) – The target Axons to send requests to. Can be a single Axon or a list of Axons.

  * **synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")) – The Synapse object encapsulating the data.

  * **timeout** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")) – Maximum duration to wait for a response from an Axon in seconds.

  * **deserialize** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Determines if the received response should be deserialized.

  * **run_async** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If `True`, sends requests concurrently. Otherwise, sends requests sequentially.

  * **streaming** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Indicates if the response is expected to be in streaming format.



Returns:
    

If a single Axon is targeted, returns its response. If multiple Axons are targeted, returns a list of their responses.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[Union[AsyncGenerator[[Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any"), [Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any")], [bittensor.core.synapse.Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse"), [bittensor.core.stream.StreamingSynapse](<../stream/index.html#bittensor.core.stream.StreamingSynapse> "bittensor.core.stream.StreamingSynapse")]]

keypair[#](<#bittensor.core.dendrite.DendriteMixin.keypair> "Link to this definition")
    

log_exception(_exception_)[#](<#bittensor.core.dendrite.DendriteMixin.log_exception> "Link to this definition")
    

Logs an exception with a unique identifier.

This method generates a unique UUID for the error, extracts the error type, and logs the error message using Bittensor’s logging system.

Parameters:
    

**exception** ([_Exception_](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)")) – The exception object to be logged.

Returns:
    

None

preprocess_synapse_for_request(_target_axon_info_ , _synapse_ , _timeout =12.0_)[#](<#id8> "Link to this definition")
    

Preprocesses the synapse for making a request. This includes building headers for Dendrite and Axon and signing the request.

Parameters:
    

  * **target_axon_info** (_bittensor.core.chain_data.AxonInfo_) – The target axon information.

  * **synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")) – The synapse object to be preprocessed.

  * **timeout** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")) – The request timeout duration in seconds.



Returns:
    

The preprocessed synapse.

Return type:
    

[bittensor.core.synapse.Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")

process_error_message(_synapse_ , _request_name_ , _exception_)[#](<#bittensor.core.dendrite.DendriteMixin.process_error_message> "Link to this definition")
    

Handles exceptions that occur during network requests, updating the synapse with appropriate status codes and messages.

This method interprets different types of exceptions and sets the corresponding status code and message in the synapse object. It covers common network errors such as connection issues and timeouts.

Parameters:
    

  * **synapse** (_Union_ _[_[_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse") _,_[_bittensor.core.stream.StreamingSynapse_](<../stream/index.html#bittensor.core.stream.StreamingSynapse> "bittensor.core.stream.StreamingSynapse") _]_) – The synapse object associated with the request.

  * **request_name** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The name of the request during which the exception occurred.

  * **exception** ([_Exception_](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)")) – The exception object caught during the request.



Returns:
    

The updated synapse object with the error status code and message.

Return type:
    

[Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")

Note

This method updates the synapse object in-place.

process_server_response(_server_response_ , _json_response_ , _local_synapse_)[#](<#id9> "Link to this definition")
    

Processes the server response, updates the local synapse state with the server’s state and merges headers set by the server.

Parameters:
    

  * **server_response** (_aiohttp.ClientResponse_) – 

The [aiohttp](<https://github.com/aio-libs/aiohttp>) response object from the server.

  * **json_response** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")) – The parsed JSON response from the server.

  * **local_synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")) – The local synapse object to be updated.



Raises:
    

**None** – But errors in attribute setting are silently ignored.

query(_* args_, _** kwargs_)[#](<#id11> "Link to this definition")
    

Makes a synchronous request to multiple target Axons and returns the server responses.

Cleanup is automatically handled and sessions are closed upon completed requests.

Parameters:
    

  * **axons** – The list of target Axon information.

  * **synapse** – The Synapse object.

  * **timeout** – The request timeout duration in seconds.



Returns:
    

If a single target axon is provided, returns the response from that axon. If multiple target axons are provided, returns a list of responses from all target axons.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[Union[AsyncGenerator[[Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any"), [Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any")], [bittensor.core.synapse.Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse"), [bittensor.core.stream.StreamingSynapse](<../stream/index.html#bittensor.core.stream.StreamingSynapse> "bittensor.core.stream.StreamingSynapse")]]

property session: aiohttp.ClientSession[#](<#bittensor.core.dendrite.DendriteMixin.session> "Link to this definition")
    

An asynchronous property that provides access to the internal [aiohttp](<https://github.com/aio-libs/aiohttp>) client session.

This property ensures the management of HTTP connections in an efficient way. It lazily initializes the [aiohttp.ClientSession](<https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession>) on its first use. The session is then reused for subsequent HTTP requests, offering performance benefits by reusing underlying connections.

This is used internally by the dendrite when querying axons, and should not be used directly unless absolutely necessary for your application.

Returns:
    

The active [aiohttp](<https://github.com/aio-libs/aiohttp>) client session instance. If no session exists, a new one is created and returned. This session is used for asynchronous HTTP requests within the dendrite, adhering to the async nature of the network interactions in the Bittensor framework.

Return type:
    

aiohttp.ClientSession

Example usage:
[code] 
    import bittensor                                # Import bittensor
    wallet = bittensor.Wallet( ... )                # Initialize a wallet
    dendrite = bittensor.Dendrite(wallet=wallet)   # Initialize a dendrite instance with the wallet
    
    async with (await dendrite.session).post(       # Use the session to make an HTTP POST request
        url,                                        # URL to send the request to
        headers={...},                              # Headers dict to be sent with the request
        json={...},                                 # JSON body data to be sent with the request
        timeout=10,                                 # Timeout duration in seconds
    ) as response:
        json_response = await response.json()       # Extract the JSON response from the server
    
[/code]

synapse_history: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") = [][#](<#bittensor.core.dendrite.DendriteMixin.synapse_history> "Link to this definition")
    

uuid = ''[#](<#bittensor.core.dendrite.DendriteMixin.uuid> "Link to this definition")
    

async bittensor.core.dendrite.call(_self_ , _* args_, _** kwargs_)[#](<#bittensor.core.dendrite.call> "Link to this definition")
    

bittensor.core.dendrite.event_loop_is_running()[#](<#bittensor.core.dendrite.event_loop_is_running> "Link to this definition")
    

[ __ previous bittensor.core.config ](<../config/index.html> "previous page") [ next bittensor.core.errors __](<../errors/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`BaseModel`](<#bittensor.core.dendrite.BaseModel>)
    * [`DENDRITE_DEFAULT_ERROR`](<#bittensor.core.dendrite.DENDRITE_DEFAULT_ERROR>)
    * [`DENDRITE_ERROR_MAPPING`](<#bittensor.core.dendrite.DENDRITE_ERROR_MAPPING>)
    * [`Dendrite`](<#bittensor.core.dendrite.Dendrite>)
      * [`Dendrite.__str__()`](<#bittensor.core.dendrite.Dendrite.__str__>)
      * [`Dendrite.__repr__()`](<#bittensor.core.dendrite.Dendrite.__repr__>)
      * [`Dendrite.query()`](<#bittensor.core.dendrite.Dendrite.query>)
      * [`Dendrite.forward()`](<#bittensor.core.dendrite.Dendrite.forward>)
      * [`Dendrite.call()`](<#bittensor.core.dendrite.Dendrite.call>)
      * [`Dendrite.call_stream()`](<#bittensor.core.dendrite.Dendrite.call_stream>)
      * [`Dendrite.preprocess_synapse_for_request()`](<#bittensor.core.dendrite.Dendrite.preprocess_synapse_for_request>)
      * [`Dendrite.process_server_response()`](<#bittensor.core.dendrite.Dendrite.process_server_response>)
      * [`Dendrite.close_session()`](<#bittensor.core.dendrite.Dendrite.close_session>)
      * [`Dendrite.aclose_session()`](<#bittensor.core.dendrite.Dendrite.aclose_session>)
    * [`DendriteMixin`](<#bittensor.core.dendrite.DendriteMixin>)
      * [`DendriteMixin.__str__()`](<#bittensor.core.dendrite.DendriteMixin.__str__>)
      * [`DendriteMixin.__repr__()`](<#bittensor.core.dendrite.DendriteMixin.__repr__>)
      * [`DendriteMixin.query()`](<#bittensor.core.dendrite.DendriteMixin.query>)
      * [`DendriteMixin.forward()`](<#bittensor.core.dendrite.DendriteMixin.forward>)
      * [`DendriteMixin.call()`](<#bittensor.core.dendrite.DendriteMixin.call>)
      * [`DendriteMixin.call_stream()`](<#bittensor.core.dendrite.DendriteMixin.call_stream>)
      * [`DendriteMixin.preprocess_synapse_for_request()`](<#bittensor.core.dendrite.DendriteMixin.preprocess_synapse_for_request>)
      * [`DendriteMixin.process_server_response()`](<#bittensor.core.dendrite.DendriteMixin.process_server_response>)
      * [`DendriteMixin.close_session()`](<#bittensor.core.dendrite.DendriteMixin.close_session>)
      * [`DendriteMixin.aclose_session()`](<#bittensor.core.dendrite.DendriteMixin.aclose_session>)
      * [`DendriteMixin.aclose_session()`](<#id0>)
      * [`DendriteMixin.aquery()`](<#bittensor.core.dendrite.DendriteMixin.aquery>)
      * [`DendriteMixin.call()`](<#id3>)
      * [`DendriteMixin.call_stream()`](<#id4>)
      * [`DendriteMixin.close_session()`](<#id5>)
      * [`DendriteMixin.external_ip`](<#bittensor.core.dendrite.DendriteMixin.external_ip>)
      * [`DendriteMixin.forward()`](<#id7>)
      * [`DendriteMixin.keypair`](<#bittensor.core.dendrite.DendriteMixin.keypair>)
      * [`DendriteMixin.log_exception()`](<#bittensor.core.dendrite.DendriteMixin.log_exception>)
      * [`DendriteMixin.preprocess_synapse_for_request()`](<#id8>)
      * [`DendriteMixin.process_error_message()`](<#bittensor.core.dendrite.DendriteMixin.process_error_message>)
      * [`DendriteMixin.process_server_response()`](<#id9>)
      * [`DendriteMixin.query()`](<#id11>)
      * [`DendriteMixin.session`](<#bittensor.core.dendrite.DendriteMixin.session>)
      * [`DendriteMixin.synapse_history`](<#bittensor.core.dendrite.DendriteMixin.synapse_history>)
      * [`DendriteMixin.uuid`](<#bittensor.core.dendrite.DendriteMixin.uuid>)
    * [`call()`](<#bittensor.core.dendrite.call>)
    * [`event_loop_is_running()`](<#bittensor.core.dendrite.event_loop_is_running>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.