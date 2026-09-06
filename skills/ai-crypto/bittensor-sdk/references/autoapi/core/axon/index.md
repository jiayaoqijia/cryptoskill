# bittensor.core.axon &#8212; Bittensor SDK Docs  documentation

[Skip to main content](<#main-content>)

__Back to top __ `Ctrl`+`K`

[ ![Bittensor SDK Docs  documentation - Home](../../../../_static/logo.svg) ![Bittensor SDK Docs  documentation - Home](../../../../_static/logo-dark-mode.svg) ](<../../../../index.html>)

__ Search `Ctrl`+`K`

Table of Contents

  * [API Reference](<../../../index.html>) __
    * [bittensor](<../../index.html>) __
      * [bittensor.core](<../index.html>) __
        * [bittensor.core.async_subtensor](<../async_subtensor/index.html>)
        * [bittensor.core.axon](<#>)
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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/axon/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/axon/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/core/axon/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.axon

##  Contents 

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`Axon`](<#bittensor.core.axon.Axon>)
      * [`Axon.add_args()`](<#bittensor.core.axon.Axon.add_args>)
      * [`Axon.app`](<#bittensor.core.axon.Axon.app>)
      * [`Axon.attach()`](<#bittensor.core.axon.Axon.attach>)
      * [`Axon.blacklist_fns`](<#bittensor.core.axon.Axon.blacklist_fns>)
      * [`Axon.check_config()`](<#bittensor.core.axon.Axon.check_config>)
      * [`Axon.config()`](<#bittensor.core.axon.Axon.config>)
      * [`Axon.default_verify()`](<#bittensor.core.axon.Axon.default_verify>)
      * [`Axon.external_ip`](<#bittensor.core.axon.Axon.external_ip>)
      * [`Axon.external_port`](<#bittensor.core.axon.Axon.external_port>)
      * [`Axon.fast_config`](<#bittensor.core.axon.Axon.fast_config>)
      * [`Axon.fast_server`](<#bittensor.core.axon.Axon.fast_server>)
      * [`Axon.forward_class_types`](<#bittensor.core.axon.Axon.forward_class_types>)
      * [`Axon.forward_fns`](<#bittensor.core.axon.Axon.forward_fns>)
      * [`Axon.full_address`](<#bittensor.core.axon.Axon.full_address>)
      * [`Axon.help()`](<#bittensor.core.axon.Axon.help>)
      * [`Axon.info()`](<#bittensor.core.axon.Axon.info>)
      * [`Axon.ip`](<#bittensor.core.axon.Axon.ip>)
      * [`Axon.middleware_cls`](<#bittensor.core.axon.Axon.middleware_cls>)
      * [`Axon.nonces`](<#bittensor.core.axon.Axon.nonces>)
      * [`Axon.port`](<#bittensor.core.axon.Axon.port>)
      * [`Axon.priority_fns`](<#bittensor.core.axon.Axon.priority_fns>)
      * [`Axon.router`](<#bittensor.core.axon.Axon.router>)
      * [`Axon.serve()`](<#bittensor.core.axon.Axon.serve>)
      * [`Axon.start()`](<#bittensor.core.axon.Axon.start>)
      * [`Axon.started`](<#bittensor.core.axon.Axon.started>)
      * [`Axon.stop()`](<#bittensor.core.axon.Axon.stop>)
      * [`Axon.thread_pool`](<#bittensor.core.axon.Axon.thread_pool>)
      * [`Axon.to_string()`](<#bittensor.core.axon.Axon.to_string>)
      * [`Axon.uuid`](<#bittensor.core.axon.Axon.uuid>)
      * [`Axon.verify_body_integrity()`](<#bittensor.core.axon.Axon.verify_body_integrity>)
      * [`Axon.verify_fns`](<#bittensor.core.axon.Axon.verify_fns>)
      * [`Axon.wallet`](<#bittensor.core.axon.Axon.wallet>)
    * [`AxonMiddleware`](<#bittensor.core.axon.AxonMiddleware>)
      * [`AxonMiddleware.axon`](<#bittensor.core.axon.AxonMiddleware.axon>)
      * [`AxonMiddleware.blacklist()`](<#bittensor.core.axon.AxonMiddleware.blacklist>)
      * [`AxonMiddleware.dispatch()`](<#bittensor.core.axon.AxonMiddleware.dispatch>)
      * [`AxonMiddleware.preprocess()`](<#bittensor.core.axon.AxonMiddleware.preprocess>)
      * [`AxonMiddleware.priority()`](<#bittensor.core.axon.AxonMiddleware.priority>)
      * [`AxonMiddleware.run()`](<#bittensor.core.axon.AxonMiddleware.run>)
      * [`AxonMiddleware.synapse_to_response()`](<#bittensor.core.axon.AxonMiddleware.synapse_to_response>)
      * [`AxonMiddleware.verify()`](<#bittensor.core.axon.AxonMiddleware.verify>)
    * [`FastAPIThreadedServer`](<#bittensor.core.axon.FastAPIThreadedServer>)
      * [`FastAPIThreadedServer.install_signal_handlers()`](<#bittensor.core.axon.FastAPIThreadedServer.install_signal_handlers>)
      * [`FastAPIThreadedServer.is_running`](<#bittensor.core.axon.FastAPIThreadedServer.is_running>)
      * [`FastAPIThreadedServer.run_in_thread()`](<#bittensor.core.axon.FastAPIThreadedServer.run_in_thread>)
      * [`FastAPIThreadedServer.should_exit`](<#bittensor.core.axon.FastAPIThreadedServer.should_exit>)
      * [`FastAPIThreadedServer.start()`](<#bittensor.core.axon.FastAPIThreadedServer.start>)
      * [`FastAPIThreadedServer.stop()`](<#bittensor.core.axon.FastAPIThreadedServer.stop>)
    * [`V_7_2_0`](<#bittensor.core.axon.V_7_2_0>)
    * [`create_error_response()`](<#bittensor.core.axon.create_error_response>)
    * [`log_and_handle_error()`](<#bittensor.core.axon.log_and_handle_error>)



# bittensor.core.axon[#](<#module-bittensor.core.axon> "Link to this heading")

Create and initialize Axon, which services the forward and backward requests from other neurons.

## Attributes[#](<#attributes> "Link to this heading")

[`V_7_2_0`](<#bittensor.core.axon.V_7_2_0> "bittensor.core.axon.V_7_2_0") |   
---|---  
  
## Classes[#](<#classes> "Link to this heading")

[`Axon`](<#bittensor.core.axon.Axon> "bittensor.core.axon.Axon") | The `Axon` class in Bittensor is a fundamental component that serves as the server-side interface for a neuron  
---|---  
[`AxonMiddleware`](<#bittensor.core.axon.AxonMiddleware> "bittensor.core.axon.AxonMiddleware") | The AxonMiddleware class is a key component in the Axon server, responsible for processing all incoming requests.  
[`FastAPIThreadedServer`](<#bittensor.core.axon.FastAPIThreadedServer> "bittensor.core.axon.FastAPIThreadedServer") | The `FastAPIThreadedServer` class is a specialized server implementation for the Axon server in the Bittensor  
  
## Functions[#](<#functions> "Link to this heading")

[`create_error_response`](<#bittensor.core.axon.create_error_response> "bittensor.core.axon.create_error_response")(synapse) | Creates an error response based on the provided synapse object.  
---|---  
[`log_and_handle_error`](<#bittensor.core.axon.log_and_handle_error> "bittensor.core.axon.log_and_handle_error")(synapse, exception[, ...]) | Logs the error and updates the synapse object with the appropriate error details.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.axon.Axon(_wallet =None_, _config =None_, _port =None_, _ip =None_, _external_ip =None_, _external_port =None_, _max_workers =None_)[#](<#bittensor.core.axon.Axon> "Link to this definition")
    

The `Axon` class in Bittensor is a fundamental component that serves as the server-side interface for a neuron within the Bittensor network.

This class is responsible for managing incoming requests from other neurons and implements various mechanisms to ensure efficient and secure network interactions.

An axon relies on a FastAPI router to create endpoints for different message types. These endpoints are crucial for handling various request types that a neuron might receive. The class is designed to be flexible and customizable, allowing users to specify custom rules for forwarding, blacklisting, prioritizing, and verifying incoming requests. The class also includes internal mechanisms to manage a thread pool, supporting concurrent handling of requests with defined priority levels.

Methods in this class are equipped to deal with incoming requests from various scenarios in the network and serve as the server face for a neuron. It accepts multiple arguments, like wallet, configuration parameters, ip address, server binding port, external ip, external port and max workers. Key methods involve managing and operating the FastAPI application router, including the attachment and operation of endpoints.

Key Features:

  * FastAPI router integration for endpoint creation and management.

  * Customizable request handling including forwarding, blacklisting, and prioritization.

  * Verification of incoming requests against custom-defined functions.

  * Thread pool management for concurrent request handling.

  * Command-line argument support for user-friendly program interaction.




Example Usage:
[code] 
    import bittensor
    # Define your custom synapse class
    class MySynapse( bittensor.Synapse ):
        input: int = 1
        output: int = None
    
    # Define a custom request forwarding function using your synapse class
    def forward( synapse: MySynapse ) -> MySynapse:
        # Apply custom logic to synapse and return it
        synapse.output = 2
        return synapse
    
    # Define a custom request verification function
    def verify_my_synapse( synapse: MySynapse ):
        # Apply custom verification logic to synapse
        # Optionally raise Exception
        assert synapse.input == 1
        ...
    
    # Define a custom request blacklist function
    def blacklist_my_synapse( synapse: MySynapse ) -> bool:
        # Apply custom blacklist
        return False ( if non blacklisted ) or True ( if blacklisted )
    
    # Define a custom request priority function
    def prioritize_my_synapse( synapse: MySynapse ) -> float:
        # Apply custom priority
        return 1.0
    
    # Initialize Axon object with a custom configuration
    my_axon = bittensor.Axon(
        config=my_config,
        wallet=my_wallet,
        port=9090,
        ip="192.0.2.0",
        external_ip="203.0.113.0",
        external_port=7070
    )
    
    # Attach the endpoint with the specified verification and forward functions.
    my_axon.attach(
        forward_fn = forward_my_synapse,
        verify_fn = verify_my_synapse,
        blacklist_fn = blacklist_my_synapse,
        priority_fn = prioritize_my_synapse
    )
    
    # Serve and start your axon.
    my_axon.serve(
        netuid = ...
        subtensor = ...
    ).start()
    
    # If you have multiple forwarding functions, you can chain attach them.
    my_axon.attach(
        forward_fn = forward_my_synapse,
        verify_fn = verify_my_synapse,
        blacklist_fn = blacklist_my_synapse,
        priority_fn = prioritize_my_synapse
    ).attach(
        forward_fn = forward_my_synapse_2,
        verify_fn = verify_my_synapse_2,
        blacklist_fn = blacklist_my_synapse_2,
        priority_fn = prioritize_my_synapse_2
    ).serve(
        netuid = ...
        subtensor = ...
    ).start()
    
[/code]

Parameters:
    

  * **wallet** (_Optional_ _[__bittensor_wallet.Wallet_ _]_) – Wallet with hotkey and coldkeypub.

  * **config** (_Optional_ _[_[_bittensor.core.config.Config_](<../config/index.html#bittensor.core.config.Config> "bittensor.core.config.Config") _]_) – Configuration parameters for the axon.

  * **port** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Port for server binding.

  * **ip** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – Binding IP address.

  * **external_ip** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – External IP address to broadcast.

  * **external_port** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – External port to broadcast.

  * **max_workers** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Number of active threads for request handling.



Returns:
    

An instance of the axon class configured as per the provided arguments.

Note

This class is a core part of Bittensor’s decentralized network for machine intelligence, allowing neurons to communicate effectively and securely.

Importance and Functionality
    

Endpoint Registration
    

This method dynamically registers API endpoints based on the Synapse used, allowing the Axon to respond to specific types of requests and synapses.

Customization of Request Handling
    

By attaching different functions, the Axon can customize how it handles, verifies, prioritizes, and potentially blocks incoming requests, making it adaptable to various network scenarios.

Security and Efficiency
    

The method contributes to both the security (via verification and blacklisting) and efficiency (via prioritization) of request handling, which are crucial in a decentralized network environment.

Flexibility
    

The ability to define custom functions for different aspects of request handling provides great flexibility, allowing the Axon to be tailored to specific needs and use cases within the Bittensor network.

Error Handling and Validation
    

The method ensures that the attached functions meet the required signatures, providing error handling to prevent runtime issues.

Creates a new bittensor.Axon object from passed arguments.

Parameters:
    

  * **config** (_Optional_ _[_[_bittensor.core.config.Config_](<../config/index.html#bittensor.core.config.Config> "bittensor.core.config.Config") _]_) – Bittensor.Axon.config()

  * **wallet** (_Optional_ _[__bittensor_wallet.Wallet_ _]_) – Bittensor Wallet with hotkey and coldkeypub.

  * **port** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Binding port.

  * **ip** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – Binding ip.

  * **external_ip** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The external ip of the server to broadcast to the network.

  * **external_port** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The external port of the server to broadcast to the network.

  * **max_workers** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Used to create the threadpool if not passed, specifies the number of active threads servicing requests.




classmethod add_args(_parser_ , _prefix =None_)[#](<#bittensor.core.axon.Axon.add_args> "Link to this definition")
    

Adds AxonServer-specific command-line arguments to the argument parser.

Parameters:
    

  * **parser** ([_argparse.ArgumentParser_](<https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser> "\(in Python v3.14\)")) – Argument parser to which the arguments will be added.

  * **prefix** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – Prefix to add to the argument names.




Note

Environment variables are used to define default values for the arguments.

app[#](<#bittensor.core.axon.Axon.app> "Link to this definition")
    

attach(_forward_fn_ , _blacklist_fn =None_, _priority_fn =None_, _verify_fn =None_)[#](<#bittensor.core.axon.Axon.attach> "Link to this definition")
    

Attaches custom functions to the Axon server for handling incoming requests. This method enables the `Axon` to define specific behaviors for request forwarding, verification, blacklisting, and prioritization, thereby customizing its interaction within the Bittensor network.

Registers an API endpoint to the FastAPI application router. It uses the name of the first argument of the `forward_fn()` function as the endpoint name.

The [`attach()`](<#bittensor.core.axon.Axon.attach> "bittensor.core.axon.Axon.attach") method in the Bittensor framework’s axon class is a crucial function for registering API endpoints to the Axon’s FastAPI application router. This method allows the Axon server to define how it handles incoming requests by attaching functions for forwarding, verifying, blacklisting, and prioritizing requests. It’s a key part of customizing the server’s behavior and ensuring efficient and secure handling of requests within the Bittensor network.

Parameters:
    

  * **forward_fn** (_Callable_) – Function to be called when the API endpoint is accessed. It should have at least one argument.

  * **blacklist_fn** (_Optional_ _[__Callable_ _]_) – Function to filter out undesired requests. It should take the same arguments as `forward_fn()` and return a boolean value.

  * **priority_fn** (_Optional_ _[__Callable_ _]_) – Function to rank requests based on their priority. It should take the same arguments as `forward_fn()` and return a numerical value representing the request’s priority.

  * **verify_fn** (_Optional_ _[__Callable_ _]_) – Function to verify requests. It should take the same arguments as `forward_fn()` and return a boolean value. If `None`, `self.default_verify()` function will be used.



Return type:
    

[Axon](<#bittensor.core.axon.Axon> "bittensor.core.axon.Axon")

Note

The methods `forward_fn()`, `blacklist_fn()`, `priority_fn()`, and `verify_fn()` should be designed to receive the same parameters.

Raises:
    

  * [**AssertionError**](<https://docs.python.org/3/library/exceptions.html#AssertionError> "\(in Python v3.14\)") – If `forward_fn()` does not have the signature: `forward( synapse: YourSynapse ) -> synapse`.

  * [**AssertionError**](<https://docs.python.org/3/library/exceptions.html#AssertionError> "\(in Python v3.14\)") – If `blacklist_fn()` does not have the signature: `blacklist( synapse: YourSynapse ) -> bool`.

  * [**AssertionError**](<https://docs.python.org/3/library/exceptions.html#AssertionError> "\(in Python v3.14\)") – If `priority_fn()` does not have the signature: `priority( synapse: YourSynapse ) -> float`.

  * [**AssertionError**](<https://docs.python.org/3/library/exceptions.html#AssertionError> "\(in Python v3.14\)") – If `verify_fn()` does not have the signature: `verify( synapse: YourSynapse ) -> None`.



Returns:
    

Returns the instance of the AxonServer class for potential method chaining.

Parameters:
    

  * **forward_fn** (_Callable_)

  * **blacklist_fn** (_Optional_ _[__Callable_ _]_)

  * **priority_fn** (_Optional_ _[__Callable_ _]_)

  * **verify_fn** (_Optional_ _[__Callable_ _]_)



Return type:
    

[Axon](<#bittensor.core.axon.Axon> "bittensor.core.axon.Axon")

Example Usage:
[code] 
    def forward_custom(synapse: MyCustomSynapse) -> MyCustomSynapse:
        # Custom logic for processing the request
        return synapse
    
    def blacklist_custom(synapse: MyCustomSynapse) -> tuple[bool, str]:
        return True, "Allowed!"
    
    def priority_custom(synapse: MyCustomSynapse) -> float:
        return 1.0
    
    def verify_custom(synapse: MyCustomSynapse):
        # Custom logic for verifying the request
        pass
    
    my_axon = bittensor.Axon(...)
    my_axon.attach(forward_fn=forward_custom, verify_fn=verify_custom)
    
[/code]

Note

The [`attach()`](<#bittensor.core.axon.Axon.attach> "bittensor.core.axon.Axon.attach") method is fundamental in setting up the Axon server’s request handling capabilities, enabling it to participate effectively and securely in the Bittensor network. The flexibility offered by this method allows developers to tailor the Axon’s behavior to specific requirements and use cases.

blacklist_fns: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), Callable | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")][#](<#bittensor.core.axon.Axon.blacklist_fns> "Link to this definition")
    

classmethod check_config(_config_)[#](<#bittensor.core.axon.Axon.check_config> "Link to this definition")
    

This method checks the configuration for the axon’s port and wallet.

Parameters:
    

**config** ([_bittensor.core.config.Config_](<../config/index.html#bittensor.core.config.Config> "bittensor.core.config.Config")) – The config object holding axon settings.

Raises:
    

[**AssertionError**](<https://docs.python.org/3/library/exceptions.html#AssertionError> "\(in Python v3.14\)") – If the axon or external ports are not in range [1024, 65535]

classmethod config()[#](<#bittensor.core.axon.Axon.config> "Link to this definition")
    

Parses the command-line arguments to form a Bittensor configuration object.

Returns:
    

Configuration object with settings from command-line arguments.

Return type:
    

[bittensor.core.config.Config](<../config/index.html#bittensor.core.config.Config> "bittensor.core.config.Config")

async default_verify(_synapse_)[#](<#bittensor.core.axon.Axon.default_verify> "Link to this definition")
    

This method is used to verify the authenticity of a received message using a digital signature.

It ensures that the message was not tampered with and was sent by the expected sender.

The [`default_verify()`](<#bittensor.core.axon.Axon.default_verify> "bittensor.core.axon.Axon.default_verify") method in the Bittensor framework is a critical security function within the Axon server. It is designed to authenticate incoming messages by verifying their digital signatures. This verification ensures the integrity of the message and confirms that it was indeed sent by the claimed sender. The method plays a pivotal role in maintaining the trustworthiness and reliability of the communication within the Bittensor network.

Key Features
    

Security Assurance
    

The default_verify method is crucial for ensuring the security of the Bittensor network. By verifying digital signatures, it guards against unauthorized access and data manipulation.

Preventing Replay Attacks
    

The method checks for increasing nonce values, which is a vital step in preventing replay attacks. A replay attack involves an adversary reusing or delaying the transmission of a valid data transmission to deceive the receiver. The first time a nonce is seen, it is checked for freshness by ensuring it is within an acceptable delta time range.

Authenticity and Integrity Checks
    

By verifying that the message’s digital signature matches its content, the method ensures the message’s authenticity (it comes from the claimed sender) and integrity (it hasn’t been altered during transmission).

Trust in Communication
    

This method fosters trust in the network communication. Neurons (nodes in the Bittensor network) can confidently interact, knowing that the messages they receive are genuine and have not been tampered with.

Cryptographic Techniques
    

The method’s reliance on asymmetric encryption techniques is a cornerstone of modern cryptographic security, ensuring that only entities with the correct cryptographic keys can participate in secure communication.

Parameters:
    

**synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")) – bittensor request synapse.

Raises:
    

  * [**Exception**](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)") – If the `receiver_hotkey` doesn’t match with `self.receiver_hotkey`.

  * [**Exception**](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)") – If the nonce is not larger than the previous nonce for the same endpoint key.

  * [**Exception**](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)") – If the signature verification fails.




After successful verification, the nonce for the given endpoint key is updated.

Note

The verification process assumes the use of an asymmetric encryption algorithm, where the sender signs the message with their private key and the receiver verifies the signature using the sender’s public key.

external_ip: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.axon.Axon.external_ip> "Link to this definition")
    

external_port: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.axon.Axon.external_port> "Link to this definition")
    

fast_config[#](<#bittensor.core.axon.Axon.fast_config> "Link to this definition")
    

fast_server[#](<#bittensor.core.axon.Axon.fast_server> "Link to this definition")
    

forward_class_types: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[inspect.Signature](<https://docs.python.org/3/library/inspect.html#inspect.Signature> "\(in Python v3.14\)")]][#](<#bittensor.core.axon.Axon.forward_class_types> "Link to this definition")
    

forward_fns: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), Callable | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")][#](<#bittensor.core.axon.Axon.forward_fns> "Link to this definition")
    

full_address = ':'[#](<#bittensor.core.axon.Axon.full_address> "Link to this definition")
    

classmethod help()[#](<#bittensor.core.axon.Axon.help> "Link to this definition")
    

Prints the help text (list of command-line arguments and their descriptions) to stdout.

info()[#](<#bittensor.core.axon.Axon.info> "Link to this definition")
    

Returns the axon info object associated with this axon.

Return type:
    

bittensor.core.chain_data.AxonInfo

ip: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.axon.Axon.ip> "Link to this definition")
    

middleware_cls[#](<#bittensor.core.axon.Axon.middleware_cls> "Link to this definition")
    

nonces: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")][#](<#bittensor.core.axon.Axon.nonces> "Link to this definition")
    

port: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.axon.Axon.port> "Link to this definition")
    

priority_fns: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), Callable | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")][#](<#bittensor.core.axon.Axon.priority_fns> "Link to this definition")
    

router[#](<#bittensor.core.axon.Axon.router> "Link to this definition")
    

serve(_netuid_ , _subtensor =None_, _certificate =None_)[#](<#bittensor.core.axon.Axon.serve> "Link to this definition")
    

Serves the Axon on the specified subtensor connection using the configured wallet. This method registers the Axon with a specific subnet within the Bittensor network, identified by the `netuid`. It links the Axon to the broader network, allowing it to participate in the decentralized exchange of information.

Parameters:
    

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The unique identifier of the subnet to register on. This ID is essential for the Axon to correctly position itself within the Bittensor network topology.

  * **subtensor** (_Optional_ _[_[_bittensor.core.subtensor.Subtensor_](<../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor") _]_) – The subtensor connection to use for serving. If not provided, a new connection is established based on default configurations.

  * **certificate** (_Optional_ _[_[_bittensor.utils.Certificate_](<../../utils/index.html#bittensor.utils.Certificate> "bittensor.utils.Certificate") _]_) – Neuron certificate.



Returns:
    

The Axon instance that is now actively serving on the specified subtensor.

Return type:
    

[Axon](<#bittensor.core.axon.Axon> "bittensor.core.axon.Axon")

Example

my_axon = bittensor.Axon(…) subtensor = bt.subtensor(network=”local”) # Local by default my_axon.serve(netuid=1, subtensor=subtensor) # Serves the axon on subnet with netuid 1

Note

The `serve` method is crucial for integrating the Axon into the Bittensor network, allowing it to start receiving and processing requests from other neurons.

start()[#](<#bittensor.core.axon.Axon.start> "Link to this definition")
    

Starts the Axon server and its underlying FastAPI server thread, transitioning the state of the Axon instance to `started`. This method initiates the server’s ability to accept and process incoming network requests, making it an active participant in the Bittensor network.

The start method triggers the FastAPI server associated with the Axon to begin listening for incoming requests. It is a crucial step in making the neuron represented by this Axon operational within the Bittensor network.

Returns:
    

The Axon instance in the ‘started’ state.

Return type:
    

[bittensor.core.axon.Axon](<#bittensor.core.axon.Axon> "bittensor.core.axon.Axon")

Example

my_axon = bittensor.Axon(…) … # setup axon, attach functions, etc. my_axon.start() # Starts the axon server

Note

After invoking this method, the Axon is ready to handle requests as per its configured endpoints and custom
    

logic.

started = False[#](<#bittensor.core.axon.Axon.started> "Link to this definition")
    

stop()[#](<#bittensor.core.axon.Axon.stop> "Link to this definition")
    

Stops the Axon server and its underlying GRPC server thread, transitioning the state of the Axon instance to `stopped`. This method ceases the server’s ability to accept new network requests, effectively removing the neuron’s server-side presence in the Bittensor network.

By stopping the FastAPI server, the Axon ceases to listen for incoming requests, and any existing connections are gracefully terminated. This function is typically used when the neuron is being shut down or needs to temporarily go offline.

Returns:
    

The Axon instance in the ‘stopped’ state.

Return type:
    

[bittensor.core.axon.Axon](<#bittensor.core.axon.Axon> "bittensor.core.axon.Axon")

Example

my_axon = bittensor.Axon(…) my_axon.start() … my_axon.stop() # Stops the axon server

Note

It is advisable to ensure that all ongoing processes or requests are completed or properly handled before invoking this method.

thread_pool[#](<#bittensor.core.axon.Axon.thread_pool> "Link to this definition")
    

to_string()[#](<#bittensor.core.axon.Axon.to_string> "Link to this definition")
    

Provides a human-readable representation of the AxonInfo for this Axon.

uuid = ''[#](<#bittensor.core.axon.Axon.uuid> "Link to this definition")
    

async verify_body_integrity(_request_)[#](<#bittensor.core.axon.Axon.verify_body_integrity> "Link to this definition")
    

The `verify_body_integrity` method in the Bittensor framework is a key security function within the Axon server’s middleware. It is responsible for ensuring the integrity of the body of incoming HTTP requests.

It asynchronously verifies the integrity of the body of a request by comparing the hash of required fields with the corresponding hashes provided in the request headers. This method is critical for ensuring that the incoming request payload has not been altered or tampered with during transmission, establishing a level of trust and security between the sender and receiver in the network.

Parameters:
    

**request** (_starlette.requests.Request_) – The incoming FastAPI request object containing both headers and the request body.

Returns:
    

Returns the parsed body of the request as a dictionary if all the hash comparisons match, indicating that
    

the body is intact and has not been tampered with.

Raises:
    

**JSONResponse** – Raises a JSONResponse with a 400 status code if any of the hash comparisons fail, indicating a potential integrity issue with the incoming request payload. The response includes the detailed error message specifying which field has a hash mismatch.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")

This method performs several key functions:

  1. Decoding and loading the request body for inspection.

  2. Gathering required field names for hash comparison from the Axon configuration.

  3. Loading and parsing the request body into a dictionary.

  4. Reconstructing the Synapse object and recomputing the hash for verification and logging.

  5. Comparing the recomputed hash with the hash provided in the request headers for verification.




Note

The integrity verification is an essential step in ensuring the security of the data exchange within the Bittensor network. It helps prevent tampering and manipulation of data during transit, thereby maintaining the reliability and trust in the network communication.

verify_fns: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), Callable | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")][#](<#bittensor.core.axon.Axon.verify_fns> "Link to this definition")
    

wallet: bittensor_wallet.Wallet[#](<#bittensor.core.axon.Axon.wallet> "Link to this definition")
    

class bittensor.core.axon.AxonMiddleware(_app_ , _axon_)[#](<#bittensor.core.axon.AxonMiddleware> "Link to this definition")
    

Bases: `starlette.middleware.base.BaseHTTPMiddleware`

The AxonMiddleware class is a key component in the Axon server, responsible for processing all incoming requests.

It handles the essential tasks of verifying requests, executing blacklist checks, running priority functions, and managing the logging of messages and errors. Additionally, the class is responsible for updating the headers of the response and executing the requested functions.

This middleware acts as an intermediary layer in request handling, ensuring that each request is processed according to the defined rules and protocols of the Bittensor network. It plays a pivotal role in maintaining the integrity and security of the network communication.

Parameters:
    

  * **app** (_starlette.types.ASGIApp_) – An instance of the FastAPI application to which this middleware is attached.

  * **axon** ([_Axon_](<#bittensor.core.axon.Axon> "bittensor.core.axon.Axon")) – The Axon instance that will process the requests.




The middleware operates by intercepting incoming requests, performing necessary preprocessing (like verification and priority assessment), executing the request through the Axon’s endpoints, and then handling any postprocessing steps such as response header updating and logging.

Initialize the AxonMiddleware class.

Parameters:
    

  * **app** (_starlette.types.ASGIApp_) – An instance of the application where the middleware processor is used.

  * **axon** ([_Axon_](<#bittensor.core.axon.Axon> "bittensor.core.axon.Axon")) – The axon instance used to process the requests.




axon[#](<#bittensor.core.axon.AxonMiddleware.axon> "Link to this definition")
    

async blacklist(_synapse_)[#](<#bittensor.core.axon.AxonMiddleware.blacklist> "Link to this definition")
    

Checks if the request should be blacklisted. This method ensures that requests from disallowed sources or with malicious intent are blocked from processing. This can be extremely useful for preventing spam or other forms of abuse. The blacklist is a list of keys or identifiers that are prohibited from accessing certain resources.

Parameters:
    

**synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")) – The Synapse object representing the request.

Raises:
    

[**Exception**](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)") – If the request is found in the blacklist.

The blacklist check involves:

  1. Retrieving the blacklist checking function for the request’s Synapse type.

  2. Executing the check and handling the case where the request is blacklisted.




If a request is blacklisted, it is blocked, and an exception is raised to halt further processing.

async dispatch(_request_ , _call_next_)[#](<#bittensor.core.axon.AxonMiddleware.dispatch> "Link to this definition")
    

Asynchronously processes incoming HTTP requests and returns the corresponding responses. This method acts as the central processing unit of the AxonMiddleware, handling each step in the request lifecycle.

Parameters:
    

  * **request** (_starlette.requests.Request_) – The incoming HTTP request to be processed.

  * **call_next** (_starlette.middleware.base.RequestResponseEndpoint_) – A callable that processes the request and returns a response.



Returns:
    

The HTTP response generated after processing the request.

Return type:
    

Response

This method performs several key functions:

  1. Request Preprocessing: Sets up Synapse object from request headers and fills necessary information.

  2. Logging: Logs the start of request processing.

  3. Blacklist Checking: Verifies if the request is blacklisted.

  4. Request Verification: Ensures the authenticity and integrity of the request.

  5. Priority Assessment: Evaluates and assigns priority to the request.

  6. Request Execution: Calls the next function in the middleware chain to process the request.

  7. Response Postprocessing: Updates response headers and logs the end of the request processing.




The method also handles exceptions and errors that might occur during each stage, ensuring that appropriate responses are returned to the client.

async preprocess(_request_)[#](<#bittensor.core.axon.AxonMiddleware.preprocess> "Link to this definition")
    

Performs the initial processing of the incoming request. This method is responsible for extracting relevant information from the request and setting up the Synapse object, which represents the state and context of the request within the Axon server.

Parameters:
    

**request** (_starlette.requests.Request_) – The incoming request to be preprocessed.

Returns:
    

The Synapse object representing the preprocessed state of the request.

Return type:
    

[bittensor.core.synapse.Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")

The preprocessing involves:

  1. Extracting the request name from the URL path.

  2. Creating a Synapse instance from the request headers using the appropriate class type.

  3. Filling in the Axon and Dendrite information into the Synapse object.

  4. Signing the Synapse from the Axon side using the wallet hotkey.




This method sets the foundation for the subsequent steps in the request handling process, ensuring that all necessary information is encapsulated within the Synapse object.

async priority(_synapse_)[#](<#bittensor.core.axon.AxonMiddleware.priority> "Link to this definition")
    

Executes the priority function for the request. This method assesses and assigns a priority level to the request, determining its urgency and importance in the processing queue.

Parameters:
    

**synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")) – The Synapse object representing the request.

Raises:
    

[**Exception**](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)") – If the priority assessment process encounters issues, such as timeouts.

The priority function plays a crucial role in managing the processing load and ensuring that critical requests are handled promptly.

async run(_synapse_ , _call_next_ , _request_)[#](<#bittensor.core.axon.AxonMiddleware.run> "Link to this definition")
    

Executes the requested function as part of the request processing pipeline. This method calls the next function in the middleware chain to process the request and generate a response.

Parameters:
    

  * **synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")) – The Synapse object representing the request.

  * **call_next** (_starlette.middleware.base.RequestResponseEndpoint_) – The next function in the middleware chain to process requests.

  * **request** (_starlette.requests.Request_) – The original HTTP request.



Returns:
    

The HTTP response generated by processing the request.

Return type:
    

Response

This method is a critical part of the request lifecycle, where the actual processing of the request takes place, leading to the generation of a response.

classmethod synapse_to_response(_synapse_ , _start_time_ , _*_ , _response_override =None_)[#](<#bittensor.core.axon.AxonMiddleware.synapse_to_response> "Link to this definition")
    

Async:
    

Parameters:
    

  * **synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse"))

  * **start_time** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

  * **response_override** (_Optional_ _[__starlette.responses.Response_ _]_)



Return type:
    

starlette.responses.Response

Converts the Synapse object into a JSON response with HTTP headers.

Parameters:
    

  * **synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")) – The Synapse object representing the request.

  * **start_time** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")) – The timestamp when the request processing started.

  * **response_override** (_Optional_ _[__starlette.responses.Response_ _]_) – Instead of serializing the synapse, mutate the provided response object. This is only really useful for StreamingSynapse responses.



Returns:
    

The final HTTP response, with updated headers, ready to be sent back to the client.

Return type:
    

Response

Postprocessing is the last step in the request handling process, ensuring that the response is properly formatted and contains all necessary information.

async verify(_synapse_)[#](<#bittensor.core.axon.AxonMiddleware.verify> "Link to this definition")
    

Verifies the authenticity and integrity of the request. This method ensures that the incoming request meets the predefined security and validation criteria.

Parameters:
    

**synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")) – The Synapse object representing the request.

Raises:
    

[**Exception**](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)") – If the verification process fails due to unmet criteria or security concerns.

The verification process involves:

  1. Retrieving the specific verification function for the request’s Synapse type.

  2. Executing the verification function and handling any exceptions that arise.




Successful verification allows the request to proceed further in the processing pipeline, while failure results in an appropriate exception being raised.

class bittensor.core.axon.FastAPIThreadedServer[#](<#bittensor.core.axon.FastAPIThreadedServer> "Link to this definition")
    

Bases: `uvicorn.Server`

The `FastAPIThreadedServer` class is a specialized server implementation for the Axon server in the Bittensor network. It extends the functionality of `uvicorn.Server()` to run the FastAPI application in a separate thread, allowing the Axon server to handle HTTP requests concurrently and non-blocking.

This class is designed to facilitate the integration of FastAPI with the Axon’s asynchronous architecture, ensuring efficient and scalable handling of network requests.

Importance and Functionality
    

Threaded Execution
    

The class allows the FastAPI application to run in a separate thread, enabling concurrent handling of HTTP requests which is crucial for the performance and scalability of the Axon server.

Seamless Integration
    

By running FastAPI in a threaded manner, this class ensures seamless integration of FastAPI’s capabilities with the Axon server’s asynchronous and multi-threaded architecture.

Controlled Server Management
    

The methods start and stop provide controlled management of the server’s lifecycle, ensuring that the server can be started and stopped as needed, which is vital for maintaining the Axon server’s reliability and availability.

Signal Handling
    

Overriding the default signal handlers prevents potential conflicts with the Axon server’s main application flow, ensuring stable operation in various network conditions.

Use Cases
    

Starting the Server
    

When the Axon server is initialized, it can use this class to start the FastAPI application in a separate thread, enabling it to begin handling HTTP requests immediately.

Stopping the Server
    

During shutdown or maintenance of the Axon server, this class can be used to stop the FastAPI application gracefully, ensuring that all resources are properly released.

Example Usage:
[code] 
    self.app = FastAPI()
    log_level = "trace"
    self.fast_config = uvicorn.Config(self.app, host="0.0.0.0", port=self.config.axon.port, log_level=log_level)
    self.fast_server = FastAPIThreadedServer(config=self.fast_config)
    self.fast_server.start()
    # do something
    self.fast_server.stop()
    
[/code]

Parameters:
    

  * **should_exit** – Flag to indicate whether the server should stop running.

  * **is_running** – Flag to indicate whether the server is currently running.




The server overrides the default signal handlers to prevent interference with the main application flow and provides methods to start and stop the server in a controlled manner.

install_signal_handlers()[#](<#bittensor.core.axon.FastAPIThreadedServer.install_signal_handlers> "Link to this definition")
    

Overrides the default signal handlers provided by `uvicorn.Server`. This method is essential to ensure that the signal handling in the threaded server does not interfere with the main application’s flow, especially in a complex asynchronous environment like the Axon server.

is_running: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)") = False[#](<#bittensor.core.axon.FastAPIThreadedServer.is_running> "Link to this definition")
    

run_in_thread()[#](<#bittensor.core.axon.FastAPIThreadedServer.run_in_thread> "Link to this definition")
    

Manages the execution of the server in a separate thread, allowing the FastAPI application to run asynchronously without blocking the main thread of the Axon server. This method is a key component in enabling concurrent request handling in the Axon server.

Yields:
    

_None_ – This method yields control back to the caller while the server is running in the background thread.

should_exit: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)") = False[#](<#bittensor.core.axon.FastAPIThreadedServer.should_exit> "Link to this definition")
    

start()[#](<#bittensor.core.axon.FastAPIThreadedServer.start> "Link to this definition")
    

Starts the FastAPI server in a separate thread if it is not already running. This method sets up the server to handle HTTP requests concurrently, enabling the Axon server to efficiently manage incoming network requests.

The method ensures that the server starts running in a non-blocking manner, allowing the Axon server to continue its other operations seamlessly.

stop()[#](<#bittensor.core.axon.FastAPIThreadedServer.stop> "Link to this definition")
    

Signals the FastAPI server to stop running. This method sets the [`should_exit()`](<#bittensor.core.axon.FastAPIThreadedServer.should_exit> "bittensor.core.axon.FastAPIThreadedServer.should_exit") flag to `True`, indicating that the server should cease its operations and exit the running thread.

Stopping the server is essential for controlled shutdowns and resource management in the Axon server, especially during maintenance or when redeploying with updated configurations.

bittensor.core.axon.V_7_2_0 = 7002000[#](<#bittensor.core.axon.V_7_2_0> "Link to this definition")
    

bittensor.core.axon.create_error_response(_synapse_)[#](<#bittensor.core.axon.create_error_response> "Link to this definition")
    

Creates an error response based on the provided synapse object.

Parameters:
    

**synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")) – The synapse object containing details about the request and the associated axon.

Returns:
    

A JSON response with a status code and content indicating the error message.

Return type:
    

JSONResponse

bittensor.core.axon.log_and_handle_error(_synapse_ , _exception_ , _status_code =None_, _start_time =None_)[#](<#bittensor.core.axon.log_and_handle_error> "Link to this definition")
    

Logs the error and updates the synapse object with the appropriate error details.

Parameters:
    

  * **synapse** ([_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")) – The synapse object to be updated with error information.

  * **exception** ([_Exception_](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)")) – The exception that was raised and needs to be logged and handled.

  * **status_code** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The HTTP status code to be set on the synapse object.

  * **start_time** (_Optional_ _[_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _]_) – The timestamp marking the start of the processing, used to calculate process time.



Returns:
    

The updated synapse object with error details.

Return type:
    

[bittensor.core.synapse.Synapse](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse")

[ __ previous bittensor.core.async_subtensor ](<../async_subtensor/index.html> "previous page") [ next bittensor.core.chain_data __](<../chain_data/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`Axon`](<#bittensor.core.axon.Axon>)
      * [`Axon.add_args()`](<#bittensor.core.axon.Axon.add_args>)
      * [`Axon.app`](<#bittensor.core.axon.Axon.app>)
      * [`Axon.attach()`](<#bittensor.core.axon.Axon.attach>)
      * [`Axon.blacklist_fns`](<#bittensor.core.axon.Axon.blacklist_fns>)
      * [`Axon.check_config()`](<#bittensor.core.axon.Axon.check_config>)
      * [`Axon.config()`](<#bittensor.core.axon.Axon.config>)
      * [`Axon.default_verify()`](<#bittensor.core.axon.Axon.default_verify>)
      * [`Axon.external_ip`](<#bittensor.core.axon.Axon.external_ip>)
      * [`Axon.external_port`](<#bittensor.core.axon.Axon.external_port>)
      * [`Axon.fast_config`](<#bittensor.core.axon.Axon.fast_config>)
      * [`Axon.fast_server`](<#bittensor.core.axon.Axon.fast_server>)
      * [`Axon.forward_class_types`](<#bittensor.core.axon.Axon.forward_class_types>)
      * [`Axon.forward_fns`](<#bittensor.core.axon.Axon.forward_fns>)
      * [`Axon.full_address`](<#bittensor.core.axon.Axon.full_address>)
      * [`Axon.help()`](<#bittensor.core.axon.Axon.help>)
      * [`Axon.info()`](<#bittensor.core.axon.Axon.info>)
      * [`Axon.ip`](<#bittensor.core.axon.Axon.ip>)
      * [`Axon.middleware_cls`](<#bittensor.core.axon.Axon.middleware_cls>)
      * [`Axon.nonces`](<#bittensor.core.axon.Axon.nonces>)
      * [`Axon.port`](<#bittensor.core.axon.Axon.port>)
      * [`Axon.priority_fns`](<#bittensor.core.axon.Axon.priority_fns>)
      * [`Axon.router`](<#bittensor.core.axon.Axon.router>)
      * [`Axon.serve()`](<#bittensor.core.axon.Axon.serve>)
      * [`Axon.start()`](<#bittensor.core.axon.Axon.start>)
      * [`Axon.started`](<#bittensor.core.axon.Axon.started>)
      * [`Axon.stop()`](<#bittensor.core.axon.Axon.stop>)
      * [`Axon.thread_pool`](<#bittensor.core.axon.Axon.thread_pool>)
      * [`Axon.to_string()`](<#bittensor.core.axon.Axon.to_string>)
      * [`Axon.uuid`](<#bittensor.core.axon.Axon.uuid>)
      * [`Axon.verify_body_integrity()`](<#bittensor.core.axon.Axon.verify_body_integrity>)
      * [`Axon.verify_fns`](<#bittensor.core.axon.Axon.verify_fns>)
      * [`Axon.wallet`](<#bittensor.core.axon.Axon.wallet>)
    * [`AxonMiddleware`](<#bittensor.core.axon.AxonMiddleware>)
      * [`AxonMiddleware.axon`](<#bittensor.core.axon.AxonMiddleware.axon>)
      * [`AxonMiddleware.blacklist()`](<#bittensor.core.axon.AxonMiddleware.blacklist>)
      * [`AxonMiddleware.dispatch()`](<#bittensor.core.axon.AxonMiddleware.dispatch>)
      * [`AxonMiddleware.preprocess()`](<#bittensor.core.axon.AxonMiddleware.preprocess>)
      * [`AxonMiddleware.priority()`](<#bittensor.core.axon.AxonMiddleware.priority>)
      * [`AxonMiddleware.run()`](<#bittensor.core.axon.AxonMiddleware.run>)
      * [`AxonMiddleware.synapse_to_response()`](<#bittensor.core.axon.AxonMiddleware.synapse_to_response>)
      * [`AxonMiddleware.verify()`](<#bittensor.core.axon.AxonMiddleware.verify>)
    * [`FastAPIThreadedServer`](<#bittensor.core.axon.FastAPIThreadedServer>)
      * [`FastAPIThreadedServer.install_signal_handlers()`](<#bittensor.core.axon.FastAPIThreadedServer.install_signal_handlers>)
      * [`FastAPIThreadedServer.is_running`](<#bittensor.core.axon.FastAPIThreadedServer.is_running>)
      * [`FastAPIThreadedServer.run_in_thread()`](<#bittensor.core.axon.FastAPIThreadedServer.run_in_thread>)
      * [`FastAPIThreadedServer.should_exit`](<#bittensor.core.axon.FastAPIThreadedServer.should_exit>)
      * [`FastAPIThreadedServer.start()`](<#bittensor.core.axon.FastAPIThreadedServer.start>)
      * [`FastAPIThreadedServer.stop()`](<#bittensor.core.axon.FastAPIThreadedServer.stop>)
    * [`V_7_2_0`](<#bittensor.core.axon.V_7_2_0>)
    * [`create_error_response()`](<#bittensor.core.axon.create_error_response>)
    * [`log_and_handle_error()`](<#bittensor.core.axon.log_and_handle_error>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.   

  *[*]: Keyword-only parameters separator (PEP 3102)