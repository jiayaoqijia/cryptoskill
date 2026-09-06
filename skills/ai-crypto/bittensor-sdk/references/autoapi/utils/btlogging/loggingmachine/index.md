# bittensor.utils.btlogging.loggingmachine &#8212; Bittensor SDK Docs  documentation

[Skip to main content](<#main-content>)

__Back to top __ `Ctrl`+`K`

[ ![Bittensor SDK Docs  documentation - Home](../../../../../_static/logo.svg) ![Bittensor SDK Docs  documentation - Home](../../../../../_static/logo-dark-mode.svg) ](<../../../../../index.html>)

__ Search `Ctrl`+`K`

Table of Contents

  * [API Reference](<../../../../index.html>) __
    * [bittensor](<../../../index.html>) __
      * [bittensor.core](<../../../core/index.html>) __
        * [bittensor.core.async_subtensor](<../../../core/async_subtensor/index.html>)
        * [bittensor.core.axon](<../../../core/axon/index.html>)
        * [bittensor.core.chain_data](<../../../core/chain_data/index.html>)
        * [bittensor.core.config](<../../../core/config/index.html>)
        * [bittensor.core.dendrite](<../../../core/dendrite/index.html>)
        * [bittensor.core.errors](<../../../core/errors/index.html>)
        * [bittensor.core.extrinsics](<../../../core/extrinsics/index.html>)
        * [bittensor.core.metagraph](<../../../core/metagraph/index.html>)
        * [bittensor.core.settings](<../../../core/settings/index.html>)
        * [bittensor.core.stream](<../../../core/stream/index.html>)
        * [bittensor.core.subtensor](<../../../core/subtensor/index.html>)
        * [bittensor.core.synapse](<../../../core/synapse/index.html>)
        * [bittensor.core.tensor](<../../../core/tensor/index.html>)
        * [bittensor.core.threadpool](<../../../core/threadpool/index.html>)
        * [bittensor.core.types](<../../../core/types/index.html>)
      * [bittensor.extras](<../../../extras/index.html>) __
        * [bittensor.extras.dev_framework](<../../../extras/dev_framework/index.html>)
        * [bittensor.extras.subtensor_api](<../../../extras/subtensor_api/index.html>)
        * [bittensor.extras.timelock](<../../../extras/timelock/index.html>)
      * [bittensor.utils](<../../index.html>) __
        * [bittensor.utils.axon_utils](<../../axon_utils/index.html>)
        * [bittensor.utils.balance](<../../balance/index.html>)
        * [bittensor.utils.btlogging](<../index.html>)
        * [bittensor.utils.easy_imports](<../../easy_imports/index.html>)
        * [bittensor.utils.formatting](<../../formatting/index.html>)
        * [bittensor.utils.liquidity](<../../liquidity/index.html>)
        * [bittensor.utils.networking](<../../networking/index.html>)
        * [bittensor.utils.registration](<../../registration/index.html>)
        * [bittensor.utils.subnets](<../../subnets/index.html>)
        * [bittensor.utils.version](<../../version/index.html>)
        * [bittensor.utils.weight_utils](<../../weight_utils/index.html>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/utils/btlogging/loggingmachine/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/utils/btlogging/loggingmachine/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/utils/btlogging/loggingmachine/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.utils.btlogging.loggingmachine

##  Contents 

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`CUSTOM_LOGGER_METHOD_STACK_LEVEL`](<#bittensor.utils.btlogging.loggingmachine.CUSTOM_LOGGER_METHOD_STACK_LEVEL>)
    * [`LoggingConfig`](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig>)
      * [`LoggingConfig.debug`](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig.debug>)
      * [`LoggingConfig.enable_third_party_loggers`](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig.enable_third_party_loggers>)
      * [`LoggingConfig.info`](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig.info>)
      * [`LoggingConfig.logging_dir`](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig.logging_dir>)
      * [`LoggingConfig.record_log`](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig.record_log>)
      * [`LoggingConfig.trace`](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig.trace>)
    * [`LoggingMachine`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine>)
      * [`LoggingMachine.Debug`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.Debug>)
      * [`LoggingMachine.Default`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.Default>)
      * [`LoggingMachine.Disabled`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.Disabled>)
      * [`LoggingMachine.Info`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.Info>)
      * [`LoggingMachine.Trace`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.Trace>)
      * [`LoggingMachine.Warning`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.Warning>)
      * [`LoggingMachine.add_args()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.add_args>)
      * [`LoggingMachine.after_disable_debug()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_disable_debug>)
      * [`LoggingMachine.after_disable_trace()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_disable_trace>)
      * [`LoggingMachine.after_enable_debug()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_enable_debug>)
      * [`LoggingMachine.after_enable_default()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_enable_default>)
      * [`LoggingMachine.after_enable_info()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_enable_info>)
      * [`LoggingMachine.after_enable_trace()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_enable_trace>)
      * [`LoggingMachine.after_enable_warning()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_enable_warning>)
      * [`LoggingMachine.after_transition()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_transition>)
      * [`LoggingMachine.before_disable_debug()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_disable_debug>)
      * [`LoggingMachine.before_disable_logging()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_disable_logging>)
      * [`LoggingMachine.before_disable_trace()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_disable_trace>)
      * [`LoggingMachine.before_enable_console()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_enable_console>)
      * [`LoggingMachine.before_enable_debug()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_enable_debug>)
      * [`LoggingMachine.before_enable_default()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_enable_default>)
      * [`LoggingMachine.before_enable_info()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_enable_info>)
      * [`LoggingMachine.before_enable_trace()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_enable_trace>)
      * [`LoggingMachine.before_enable_warning()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_enable_warning>)
      * [`LoggingMachine.before_transition()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_transition>)
      * [`LoggingMachine.check_config()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.check_config>)
      * [`LoggingMachine.config()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.config>)
      * [`LoggingMachine.console`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.console>)
      * [`LoggingMachine.critical()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.critical>)
      * [`LoggingMachine.debug()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.debug>)
      * [`LoggingMachine.deregister_primary_logger()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.deregister_primary_logger>)
      * [`LoggingMachine.disable_debug`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.disable_debug>)
      * [`LoggingMachine.disable_info`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.disable_info>)
      * [`LoggingMachine.disable_logging`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.disable_logging>)
      * [`LoggingMachine.disable_third_party_loggers()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.disable_third_party_loggers>)
      * [`LoggingMachine.disable_trace`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.disable_trace>)
      * [`LoggingMachine.disable_warning`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.disable_warning>)
      * [`LoggingMachine.enable_console`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_console>)
      * [`LoggingMachine.enable_debug`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_debug>)
      * [`LoggingMachine.enable_default`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_default>)
      * [`LoggingMachine.enable_info`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_info>)
      * [`LoggingMachine.enable_third_party_loggers()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_third_party_loggers>)
      * [`LoggingMachine.enable_trace`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_trace>)
      * [`LoggingMachine.enable_warning`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_warning>)
      * [`LoggingMachine.error()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.error>)
      * [`LoggingMachine.exception()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.exception>)
      * [`LoggingMachine.get_config()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.get_config>)
      * [`LoggingMachine.get_level()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.get_level>)
      * [`LoggingMachine.get_queue()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.get_queue>)
      * [`LoggingMachine.help()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.help>)
      * [`LoggingMachine.info()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.info>)
      * [`LoggingMachine.off()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.off>)
      * [`LoggingMachine.on()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.on>)
      * [`LoggingMachine.register_primary_logger()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.register_primary_logger>)
      * [`LoggingMachine.setLevel()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.setLevel>)
      * [`LoggingMachine.set_config()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_config>)
      * [`LoggingMachine.set_console()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_console>)
      * [`LoggingMachine.set_debug()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_debug>)
      * [`LoggingMachine.set_default()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_default>)
      * [`LoggingMachine.set_info()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_info>)
      * [`LoggingMachine.set_trace()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_trace>)
      * [`LoggingMachine.set_warning()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_warning>)
      * [`LoggingMachine.success()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.success>)
      * [`LoggingMachine.trace()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.trace>)
      * [`LoggingMachine.warning()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.warning>)



# bittensor.utils.btlogging.loggingmachine[#](<#module-bittensor.utils.btlogging.loggingmachine> "Link to this heading")

Module provides a logging framework for Bittensor, managing both Bittensor-specific and third-party logging states. It leverages the StateMachine from the statemachine package to transition between different logging states such as Default, Debug, Trace, and Disabled.

## Attributes[#](<#attributes> "Link to this heading")

[`CUSTOM_LOGGER_METHOD_STACK_LEVEL`](<#bittensor.utils.btlogging.loggingmachine.CUSTOM_LOGGER_METHOD_STACK_LEVEL> "bittensor.utils.btlogging.loggingmachine.CUSTOM_LOGGER_METHOD_STACK_LEVEL") |   
---|---  
  
## Classes[#](<#classes> "Link to this heading")

[`LoggingConfig`](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig> "bittensor.utils.btlogging.loggingmachine.LoggingConfig") | Named tuple to hold the logging configuration.  
---|---  
[`LoggingMachine`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine> "bittensor.utils.btlogging.loggingmachine.LoggingMachine") | Handles logger states for bittensor and 3rd party libraries.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

bittensor.utils.btlogging.loggingmachine.CUSTOM_LOGGER_METHOD_STACK_LEVEL = 2[#](<#bittensor.utils.btlogging.loggingmachine.CUSTOM_LOGGER_METHOD_STACK_LEVEL> "Link to this definition")
    

class bittensor.utils.btlogging.loggingmachine.LoggingConfig[#](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig> "Link to this definition")
    

Bases: `NamedTuple`

Named tuple to hold the logging configuration.

debug: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig.debug> "Link to this definition")
    

enable_third_party_loggers: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig.enable_third_party_loggers> "Link to this definition")
    

info: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig.info> "Link to this definition")
    

logging_dir: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig.logging_dir> "Link to this definition")
    

record_log: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig.record_log> "Link to this definition")
    

trace: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig.trace> "Link to this definition")
    

class bittensor.utils.btlogging.loggingmachine.LoggingMachine(_config_ , _name =BITTENSOR_LOGGER_NAME_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine> "Link to this definition")
    

Bases: `statemachine.StateMachine`, [`logging.Logger`](<https://docs.python.org/3/library/logging.html#logging.Logger> "\(in Python v3.14\)")

Handles logger states for bittensor and 3rd party libraries.

Initialize the logger with a name and an optional level.

Parameters:
    

  * **config** ([_bittensor.core.config.Config_](<../../../core/config/index.html#bittensor.core.config.Config> "bittensor.core.config.Config"))

  * **name** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))




Debug[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.Debug> "Link to this definition")
    

Default[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.Default> "Link to this definition")
    

Disabled[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.Disabled> "Link to this definition")
    

Info[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.Info> "Link to this definition")
    

Trace[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.Trace> "Link to this definition")
    

Warning[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.Warning> "Link to this definition")
    

classmethod add_args(_parser_ , _prefix =None_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.add_args> "Link to this definition")
    

Accept specific arguments fro parser

Parameters:
    

  * **parser** ([_argparse.ArgumentParser_](<https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser> "\(in Python v3.14\)"))

  * **prefix** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))




after_disable_debug()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_disable_debug> "Link to this definition")
    

Logs status after disable Debug.

after_disable_trace()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_disable_trace> "Link to this definition")
    

Logs status after disable Trace.

after_enable_debug()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_enable_debug> "Link to this definition")
    

Logs status after enable Debug.

after_enable_default()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_enable_default> "Link to this definition")
    

after_enable_info()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_enable_info> "Link to this definition")
    

Logs status after enable info.

after_enable_trace()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_enable_trace> "Link to this definition")
    

Logs status after enable Trace.

after_enable_warning()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_enable_warning> "Link to this definition")
    

Logs status after enable Warning.

after_transition(_event_ , _state_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_transition> "Link to this definition")
    

Starts listener after transition.

before_disable_debug()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_disable_debug> "Link to this definition")
    

Logs status before disable Debug.

before_disable_logging()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_disable_logging> "Link to this definition")
    

Prepares the logging system for disabling.

This method performs the following actions: 1\. Logs an informational message indicating that logging is being disabled. 2\. Disables trace mode in the stream formatter. 3\. Sets the logging level to CRITICAL for all loggers.

This ensures that only critical messages will be logged after this method is called.

before_disable_trace()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_disable_trace> "Link to this definition")
    

Logs status before disable Trace.

before_enable_console()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_enable_console> "Link to this definition")
    

Logs status before enable Console.

before_enable_debug()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_enable_debug> "Link to this definition")
    

Logs status before enable Debug.

before_enable_default()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_enable_default> "Link to this definition")
    

before_enable_info()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_enable_info> "Link to this definition")
    

Logs status before enable info.

before_enable_trace()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_enable_trace> "Link to this definition")
    

Logs status before enable Trace.

before_enable_warning()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_enable_warning> "Link to this definition")
    

Logs status before enable Warning.

before_transition(_event_ , _state_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_transition> "Link to this definition")
    

Stops listener after transition.

check_config(_config_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.check_config> "Link to this definition")
    

Parameters:
    

**config** ([_bittensor.core.config.Config_](<../../../core/config/index.html#bittensor.core.config.Config> "bittensor.core.config.Config"))

classmethod config()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.config> "Link to this definition")
    

Get config from the argument parser.

Returns:
    

Configuration object with settings from command-line arguments.

Return type:
    

[bittensor.core.config.Config](<../../../core/config/index.html#bittensor.core.config.Config> "bittensor.core.config.Config")

console[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.console> "Link to this definition")
    

critical(_msg =''_, _prefix =''_, _suffix =''_, _* args_, _stacklevel =1_, _** kwargs_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.critical> "Link to this definition")
    

Wraps critical message with prefix and suffix.

debug(_msg =''_, _prefix =''_, _suffix =''_, _* args_, _stacklevel =1_, _** kwargs_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.debug> "Link to this definition")
    

Wraps debug message with prefix and suffix.

deregister_primary_logger(_name_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.deregister_primary_logger> "Link to this definition")
    

De-registers a primary logger.

This function removes the logger from the _primary_loggers set and deinitializes its queue handler

Parameters:
    

**name** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – the name of primary logger.

disable_debug[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.disable_debug> "Link to this definition")
    

disable_info[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.disable_info> "Link to this definition")
    

disable_logging[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.disable_logging> "Link to this definition")
    

disable_third_party_loggers()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.disable_third_party_loggers> "Link to this definition")
    

Disables logging for third-party loggers by removing all their handlers.

disable_trace[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.disable_trace> "Link to this definition")
    

disable_warning[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.disable_warning> "Link to this definition")
    

enable_console[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_console> "Link to this definition")
    

enable_debug[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_debug> "Link to this definition")
    

enable_default[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_default> "Link to this definition")
    

enable_info[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_info> "Link to this definition")
    

enable_third_party_loggers()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_third_party_loggers> "Link to this definition")
    

Enables logging for third-party loggers by adding a queue handler to each.

enable_trace[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_trace> "Link to this definition")
    

enable_warning[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_warning> "Link to this definition")
    

error(_msg =''_, _prefix =''_, _suffix =''_, _* args_, _stacklevel =1_, _** kwargs_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.error> "Link to this definition")
    

Wraps error message with prefix and suffix.

exception(_msg =''_, _prefix =''_, _suffix =''_, _* args_, _stacklevel =1_, _** kwargs_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.exception> "Link to this definition")
    

Wraps exception message with prefix and suffix.

get_config()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.get_config> "Link to this definition")
    

get_level()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.get_level> "Link to this definition")
    

Returns Logging level.

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

get_queue()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.get_queue> "Link to this definition")
    

Get the queue the QueueListener is publishing from.

To set up logging in a separate process, a QueueHandler must be added to all the desired loggers.

help()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.help> "Link to this definition")
    

info(_msg =''_, _prefix =''_, _suffix =''_, _* args_, _stacklevel =1_, _** kwargs_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.info> "Link to this definition")
    

Wraps info message with prefix and suffix.

off()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.off> "Link to this definition")
    

Disables all states.

on()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.on> "Link to this definition")
    

Enable default state.

register_primary_logger(_name_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.register_primary_logger> "Link to this definition")
    

Register a logger as primary logger.

This adds a logger to the _primary_loggers set to ensure it doesn’t get disabled when disabling third-party loggers. A queue handler is also associated with it.

Parameters:
    

**name** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – the name for primary logger.

setLevel(_level_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.setLevel> "Link to this definition")
    

Set the specified level on the underlying logger.

set_config(_config_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_config> "Link to this definition")
    

Set config after initialization, if desired.

Parameters:
    

**config** ([_bittensor.core.config.Config_](<../../../core/config/index.html#bittensor.core.config.Config> "bittensor.core.config.Config")) – Bittensor config instance.

set_console()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_console> "Link to this definition")
    

Sets Console state.

set_debug(_on =True_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_debug> "Link to this definition")
    

Sets Debug state.

Parameters:
    

**on** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

set_default()[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_default> "Link to this definition")
    

Sets Default state.

set_info(_on =True_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_info> "Link to this definition")
    

Sets Info state.

Parameters:
    

**on** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

set_trace(_on =True_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_trace> "Link to this definition")
    

Sets Trace state.

Parameters:
    

**on** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

set_warning(_on =True_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_warning> "Link to this definition")
    

Sets Warning state.

Parameters:
    

**on** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

success(_msg =''_, _prefix =''_, _suffix =''_, _* args_, _stacklevel =1_, _** kwargs_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.success> "Link to this definition")
    

Wraps success message with prefix and suffix.

trace(_msg =''_, _prefix =''_, _suffix =''_, _* args_, _stacklevel =1_, _** kwargs_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.trace> "Link to this definition")
    

Wraps trace message with prefix and suffix.

warning(_msg =''_, _prefix =''_, _suffix =''_, _* args_, _stacklevel =1_, _** kwargs_)[#](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.warning> "Link to this definition")
    

Wraps warning message with prefix and suffix.

[ __ previous bittensor.utils.btlogging.levels ](<../levels/index.html> "previous page") [ next bittensor.utils.easy_imports __](<../../easy_imports/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`CUSTOM_LOGGER_METHOD_STACK_LEVEL`](<#bittensor.utils.btlogging.loggingmachine.CUSTOM_LOGGER_METHOD_STACK_LEVEL>)
    * [`LoggingConfig`](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig>)
      * [`LoggingConfig.debug`](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig.debug>)
      * [`LoggingConfig.enable_third_party_loggers`](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig.enable_third_party_loggers>)
      * [`LoggingConfig.info`](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig.info>)
      * [`LoggingConfig.logging_dir`](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig.logging_dir>)
      * [`LoggingConfig.record_log`](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig.record_log>)
      * [`LoggingConfig.trace`](<#bittensor.utils.btlogging.loggingmachine.LoggingConfig.trace>)
    * [`LoggingMachine`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine>)
      * [`LoggingMachine.Debug`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.Debug>)
      * [`LoggingMachine.Default`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.Default>)
      * [`LoggingMachine.Disabled`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.Disabled>)
      * [`LoggingMachine.Info`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.Info>)
      * [`LoggingMachine.Trace`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.Trace>)
      * [`LoggingMachine.Warning`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.Warning>)
      * [`LoggingMachine.add_args()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.add_args>)
      * [`LoggingMachine.after_disable_debug()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_disable_debug>)
      * [`LoggingMachine.after_disable_trace()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_disable_trace>)
      * [`LoggingMachine.after_enable_debug()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_enable_debug>)
      * [`LoggingMachine.after_enable_default()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_enable_default>)
      * [`LoggingMachine.after_enable_info()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_enable_info>)
      * [`LoggingMachine.after_enable_trace()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_enable_trace>)
      * [`LoggingMachine.after_enable_warning()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_enable_warning>)
      * [`LoggingMachine.after_transition()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.after_transition>)
      * [`LoggingMachine.before_disable_debug()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_disable_debug>)
      * [`LoggingMachine.before_disable_logging()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_disable_logging>)
      * [`LoggingMachine.before_disable_trace()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_disable_trace>)
      * [`LoggingMachine.before_enable_console()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_enable_console>)
      * [`LoggingMachine.before_enable_debug()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_enable_debug>)
      * [`LoggingMachine.before_enable_default()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_enable_default>)
      * [`LoggingMachine.before_enable_info()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_enable_info>)
      * [`LoggingMachine.before_enable_trace()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_enable_trace>)
      * [`LoggingMachine.before_enable_warning()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_enable_warning>)
      * [`LoggingMachine.before_transition()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.before_transition>)
      * [`LoggingMachine.check_config()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.check_config>)
      * [`LoggingMachine.config()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.config>)
      * [`LoggingMachine.console`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.console>)
      * [`LoggingMachine.critical()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.critical>)
      * [`LoggingMachine.debug()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.debug>)
      * [`LoggingMachine.deregister_primary_logger()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.deregister_primary_logger>)
      * [`LoggingMachine.disable_debug`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.disable_debug>)
      * [`LoggingMachine.disable_info`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.disable_info>)
      * [`LoggingMachine.disable_logging`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.disable_logging>)
      * [`LoggingMachine.disable_third_party_loggers()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.disable_third_party_loggers>)
      * [`LoggingMachine.disable_trace`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.disable_trace>)
      * [`LoggingMachine.disable_warning`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.disable_warning>)
      * [`LoggingMachine.enable_console`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_console>)
      * [`LoggingMachine.enable_debug`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_debug>)
      * [`LoggingMachine.enable_default`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_default>)
      * [`LoggingMachine.enable_info`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_info>)
      * [`LoggingMachine.enable_third_party_loggers()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_third_party_loggers>)
      * [`LoggingMachine.enable_trace`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_trace>)
      * [`LoggingMachine.enable_warning`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.enable_warning>)
      * [`LoggingMachine.error()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.error>)
      * [`LoggingMachine.exception()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.exception>)
      * [`LoggingMachine.get_config()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.get_config>)
      * [`LoggingMachine.get_level()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.get_level>)
      * [`LoggingMachine.get_queue()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.get_queue>)
      * [`LoggingMachine.help()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.help>)
      * [`LoggingMachine.info()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.info>)
      * [`LoggingMachine.off()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.off>)
      * [`LoggingMachine.on()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.on>)
      * [`LoggingMachine.register_primary_logger()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.register_primary_logger>)
      * [`LoggingMachine.setLevel()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.setLevel>)
      * [`LoggingMachine.set_config()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_config>)
      * [`LoggingMachine.set_console()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_console>)
      * [`LoggingMachine.set_debug()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_debug>)
      * [`LoggingMachine.set_default()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_default>)
      * [`LoggingMachine.set_info()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_info>)
      * [`LoggingMachine.set_trace()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_trace>)
      * [`LoggingMachine.set_warning()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.set_warning>)
      * [`LoggingMachine.success()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.success>)
      * [`LoggingMachine.trace()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.trace>)
      * [`LoggingMachine.warning()`](<#bittensor.utils.btlogging.loggingmachine.LoggingMachine.warning>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.