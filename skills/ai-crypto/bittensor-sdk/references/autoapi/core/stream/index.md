# bittensor.core.stream &#8212; Bittensor SDK Docs  documentation

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
        * [bittensor.core.stream](<#>)
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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/stream/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/stream/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/core/stream/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.stream

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`BTStreamingResponseModel`](<#bittensor.core.stream.BTStreamingResponseModel>)
      * [`BTStreamingResponseModel.token_streamer`](<#bittensor.core.stream.BTStreamingResponseModel.token_streamer>)
    * [`StreamingSynapse`](<#bittensor.core.stream.StreamingSynapse>)
      * [`StreamingSynapse.BTStreamingResponse`](<#bittensor.core.stream.StreamingSynapse.BTStreamingResponse>)
        * [`StreamingSynapse.BTStreamingResponse.stream_response()`](<#bittensor.core.stream.StreamingSynapse.BTStreamingResponse.stream_response>)
        * [`StreamingSynapse.BTStreamingResponse.synapse`](<#bittensor.core.stream.StreamingSynapse.BTStreamingResponse.synapse>)
        * [`StreamingSynapse.BTStreamingResponse.token_streamer`](<#bittensor.core.stream.StreamingSynapse.BTStreamingResponse.token_streamer>)
      * [`StreamingSynapse.create_streaming_response()`](<#bittensor.core.stream.StreamingSynapse.create_streaming_response>)
      * [`StreamingSynapse.extract_response_json()`](<#bittensor.core.stream.StreamingSynapse.extract_response_json>)
      * [`StreamingSynapse.model_config`](<#bittensor.core.stream.StreamingSynapse.model_config>)
      * [`StreamingSynapse.process_streaming_response()`](<#bittensor.core.stream.StreamingSynapse.process_streaming_response>)



# bittensor.core.stream[#](<#module-bittensor.core.stream> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`BTStreamingResponseModel`](<#bittensor.core.stream.BTStreamingResponseModel> "bittensor.core.stream.BTStreamingResponseModel") | [`BTStreamingResponseModel()`](<#bittensor.core.stream.BTStreamingResponseModel> "bittensor.core.stream.BTStreamingResponseModel") is a Pydantic model that encapsulates the token streamer callable for Pydantic  
---|---  
[`StreamingSynapse`](<#bittensor.core.stream.StreamingSynapse> "bittensor.core.stream.StreamingSynapse") | The [`StreamingSynapse()`](<#bittensor.core.stream.StreamingSynapse> "bittensor.core.stream.StreamingSynapse") class is designed to be subclassed for handling streaming responses in the Bittensor network.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.stream.BTStreamingResponseModel[#](<#bittensor.core.stream.BTStreamingResponseModel> "Link to this definition")
    

Bases: [`pydantic.BaseModel`](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel> "\(in Pydantic v0.0.0\)")

[`BTStreamingResponseModel()`](<#bittensor.core.stream.BTStreamingResponseModel> "bittensor.core.stream.BTStreamingResponseModel") is a Pydantic model that encapsulates the token streamer callable for Pydantic validation. It is used within the [`StreamingSynapse()`](<#bittensor.core.stream.StreamingSynapse> "bittensor.core.stream.StreamingSynapse") class to create a `BTStreamingResponse()` object, which is responsible for handling the streaming of tokens.

The token streamer is a callable that takes a send function and returns an awaitable. It is responsible for generating the content of the streaming response, typically by processing tokens and sending them to the client.

This model ensures that the token streamer conforms to the expected signature and provides a clear interface for passing the token streamer to the BTStreamingResponse class.

Variables:
    

**token_streamer** – Callable[[Send], Awaitable[None]] The token streamer callable, which takes a send function (provided by the ASGI server) and returns an awaitable. It is responsible for generating the content of the streaming response.

token_streamer: Callable[[starlette.types.Send], Awaitable[[None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")]][#](<#bittensor.core.stream.BTStreamingResponseModel.token_streamer> "Link to this definition")
    

class bittensor.core.stream.StreamingSynapse[#](<#bittensor.core.stream.StreamingSynapse> "Link to this definition")
    

Bases: [`bittensor.core.synapse.Synapse`](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse"), [`abc.ABC`](<https://docs.python.org/3/library/abc.html#abc.ABC> "\(in Python v3.14\)")

The [`StreamingSynapse()`](<#bittensor.core.stream.StreamingSynapse> "bittensor.core.stream.StreamingSynapse") class is designed to be subclassed for handling streaming responses in the Bittensor network. It provides abstract methods that must be implemented by the subclass to deserialize, process streaming responses, and extract JSON data. It also includes a method to create a streaming response object.

class BTStreamingResponse(_model_ , _*_ , _synapse =None_, _** kwargs_)[#](<#bittensor.core.stream.StreamingSynapse.BTStreamingResponse> "Link to this definition")
    

Bases: `starlette.responses.StreamingResponse`

`BTStreamingResponse()` is a specialized subclass of the Starlette StreamingResponse designed to handle the streaming of tokens within the Bittensor network. It is used internally by the StreamingSynapse class to manage the response streaming process, including sending headers and calling the token streamer provided by the subclass.

This class is not intended to be directly instantiated or modified by developers subclassing StreamingSynapse. Instead, it is used by the `create_streaming_response()` method to create a response object based on the token streamer provided by the subclass.

Initializes the BTStreamingResponse with the given token streamer model.

Parameters:
    

  * **model** ([_BTStreamingResponseModel_](<#bittensor.core.stream.BTStreamingResponseModel> "bittensor.core.stream.BTStreamingResponseModel")) – A BTStreamingResponseModel instance containing the token streamer callable, which is responsible for generating the content of the response.

  * **synapse** (_Optional_ _[_[_StreamingSynapse_](<#bittensor.core.stream.StreamingSynapse> "bittensor.core.stream.StreamingSynapse") _]_) – The response Synapse to be used to update the response headers etc.

  * ****kwargs** – Additional keyword arguments passed to the parent StreamingResponse class.




async stream_response(_send_)[#](<#bittensor.core.stream.StreamingSynapse.BTStreamingResponse.stream_response> "Link to this definition")
    

Asynchronously streams the response by sending headers and calling the token streamer.

This method is responsible for initiating the response by sending the appropriate headers, including the content type for event-streaming. It then calls the token streamer to generate the content and sends the response body to the client.

Parameters:
    

**send** (_starlette.types.Send_) – A callable to send the response, provided by the ASGI server.

synapse = None[#](<#bittensor.core.stream.StreamingSynapse.BTStreamingResponse.synapse> "Link to this definition")
    

token_streamer[#](<#bittensor.core.stream.StreamingSynapse.BTStreamingResponse.token_streamer> "Link to this definition")
    

create_streaming_response(_token_streamer_)[#](<#bittensor.core.stream.StreamingSynapse.create_streaming_response> "Link to this definition")
    

Creates a streaming response using the provided token streamer. This method can be used by the subclass to create a response object that can be sent back to the client. The token streamer should be implemented to generate the content of the response according to the specific requirements of the subclass.

Parameters:
    

**token_streamer** (_Callable_ _[__[__starlette.types.Send_ _]__,__Awaitable_ _[__None_ _]__]_) – A callable that takes a send function and returns an awaitable. It’s responsible for generating the content of the response.

Returns:
    

The streaming response object, ready to be sent to the client.

Return type:
    

[BTStreamingResponse](<#bittensor.core.stream.StreamingSynapse.BTStreamingResponse> "bittensor.core.stream.StreamingSynapse.BTStreamingResponse")

abstractmethod extract_response_json(_response_)[#](<#bittensor.core.stream.StreamingSynapse.extract_response_json> "Link to this definition")
    

Abstract method that must be implemented by the subclass. This method should provide logic to extract JSON data from the response, including headers and content. It is called after the response has been processed and is responsible for retrieving structured data that can be used by the application.

Parameters:
    

  * **data.** (_The response object from which to extract JSON_)

  * **response** (_aiohttp.ClientResponse_)



Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")

model_config[#](<#bittensor.core.stream.StreamingSynapse.model_config> "Link to this definition")
    

abstractmethod process_streaming_response(_response_)[#](<#bittensor.core.stream.StreamingSynapse.process_streaming_response> "Link to this definition")
    

Async:
    

Parameters:
    

**response** (_aiohttp.ClientResponse_)

Abstract method that must be implemented by the subclass. This method should provide logic to handle the streaming response, such as parsing and accumulating data. It is called as the response is being streamed from the network, and should be implemented to handle the specific streaming data format and requirements of the subclass.

Parameters:
    

  * **processed** (_The response object to be_)

  * **data.** (_typically containing chunks of_)

  * **response** (_aiohttp.ClientResponse_)




[ __ previous bittensor.core.settings ](<../settings/index.html> "previous page") [ next bittensor.core.subtensor __](<../subtensor/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`BTStreamingResponseModel`](<#bittensor.core.stream.BTStreamingResponseModel>)
      * [`BTStreamingResponseModel.token_streamer`](<#bittensor.core.stream.BTStreamingResponseModel.token_streamer>)
    * [`StreamingSynapse`](<#bittensor.core.stream.StreamingSynapse>)
      * [`StreamingSynapse.BTStreamingResponse`](<#bittensor.core.stream.StreamingSynapse.BTStreamingResponse>)
        * [`StreamingSynapse.BTStreamingResponse.stream_response()`](<#bittensor.core.stream.StreamingSynapse.BTStreamingResponse.stream_response>)
        * [`StreamingSynapse.BTStreamingResponse.synapse`](<#bittensor.core.stream.StreamingSynapse.BTStreamingResponse.synapse>)
        * [`StreamingSynapse.BTStreamingResponse.token_streamer`](<#bittensor.core.stream.StreamingSynapse.BTStreamingResponse.token_streamer>)
      * [`StreamingSynapse.create_streaming_response()`](<#bittensor.core.stream.StreamingSynapse.create_streaming_response>)
      * [`StreamingSynapse.extract_response_json()`](<#bittensor.core.stream.StreamingSynapse.extract_response_json>)
      * [`StreamingSynapse.model_config`](<#bittensor.core.stream.StreamingSynapse.model_config>)
      * [`StreamingSynapse.process_streaming_response()`](<#bittensor.core.stream.StreamingSynapse.process_streaming_response>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.   

  *[*]: Keyword-only parameters separator (PEP 3102)