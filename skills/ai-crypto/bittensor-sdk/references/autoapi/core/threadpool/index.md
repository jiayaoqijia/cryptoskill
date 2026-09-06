# bittensor.core.threadpool &#8212; Bittensor SDK Docs  documentation

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
        * [bittensor.core.tensor](<../tensor/index.html>)
        * [bittensor.core.threadpool](<#>)
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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/threadpool/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/threadpool/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/core/threadpool/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.threadpool

##  Contents 

  * [Attributes](<#attributes>)
  * [Exceptions](<#exceptions>)
  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`BrokenThreadPool`](<#bittensor.core.threadpool.BrokenThreadPool>)
    * [`NULL_ENTRY`](<#bittensor.core.threadpool.NULL_ENTRY>)
    * [`PriorityThreadPoolExecutor`](<#bittensor.core.threadpool.PriorityThreadPoolExecutor>)
      * [`PriorityThreadPoolExecutor.add_args()`](<#bittensor.core.threadpool.PriorityThreadPoolExecutor.add_args>)
      * [`PriorityThreadPoolExecutor.config()`](<#bittensor.core.threadpool.PriorityThreadPoolExecutor.config>)
      * [`PriorityThreadPoolExecutor.is_empty`](<#bittensor.core.threadpool.PriorityThreadPoolExecutor.is_empty>)
      * [`PriorityThreadPoolExecutor.shutdown()`](<#bittensor.core.threadpool.PriorityThreadPoolExecutor.shutdown>)
      * [`PriorityThreadPoolExecutor.submit()`](<#bittensor.core.threadpool.PriorityThreadPoolExecutor.submit>)
    * [`logger`](<#bittensor.core.threadpool.logger>)



# bittensor.core.threadpool[#](<#module-bittensor.core.threadpool> "Link to this heading")

Implements [ThreadPoolExecutor](<https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor>).

## Attributes[#](<#attributes> "Link to this heading")

[`NULL_ENTRY`](<#bittensor.core.threadpool.NULL_ENTRY> "bittensor.core.threadpool.NULL_ENTRY") |   
---|---  
[`logger`](<#bittensor.core.threadpool.logger> "bittensor.core.threadpool.logger") |   
  
## Exceptions[#](<#exceptions> "Link to this heading")

[`BrokenThreadPool`](<#bittensor.core.threadpool.BrokenThreadPool> "bittensor.core.threadpool.BrokenThreadPool") | Raised when a worker thread in a [ThreadPoolExecutor](<https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor>) failed initializing.  
---|---  
  
## Classes[#](<#classes> "Link to this heading")

[`PriorityThreadPoolExecutor`](<#bittensor.core.threadpool.PriorityThreadPoolExecutor> "bittensor.core.threadpool.PriorityThreadPoolExecutor") | Base threadpool executor with a priority queue.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

exception bittensor.core.threadpool.BrokenThreadPool[#](<#bittensor.core.threadpool.BrokenThreadPool> "Link to this definition")
    

Bases: `concurrent.futures._base.BrokenExecutor`

Raised when a worker thread in a [ThreadPoolExecutor](<https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor>) failed initializing.

Initialize self. See help(type(self)) for accurate signature.

bittensor.core.threadpool.NULL_ENTRY[#](<#bittensor.core.threadpool.NULL_ENTRY> "Link to this definition")
    

class bittensor.core.threadpool.PriorityThreadPoolExecutor(_maxsize =-1_, _max_workers =None_, _thread_name_prefix =''_, _initializer =None_, _initargs =()_)[#](<#bittensor.core.threadpool.PriorityThreadPoolExecutor> "Link to this definition")
    

Bases: `concurrent.futures._base.Executor`

Base threadpool executor with a priority queue.

Initializes a new [ThreadPoolExecutor](<https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor>) instance.

Parameters:
    

  * **max_workers** – The maximum number of threads that can be used to execute the given calls.

  * **thread_name_prefix** – An optional name prefix to give our threads.

  * **initializer** – An callable used to initialize worker threads.

  * **initargs** – A tuple of arguments to pass to the initializer.




classmethod add_args(_parser_ , _prefix =None_)[#](<#bittensor.core.threadpool.PriorityThreadPoolExecutor.add_args> "Link to this definition")
    

Accept specific arguments from parser

Parameters:
    

  * **parser** ([_argparse.ArgumentParser_](<https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser> "\(in Python v3.14\)"))

  * **prefix** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))




classmethod config()[#](<#bittensor.core.threadpool.PriorityThreadPoolExecutor.config> "Link to this definition")
    

Get config from the argument parser.

Return: `bittensor.Config()` object.

Return type:
    

[bittensor.core.config.Config](<../config/index.html#bittensor.core.config.Config> "bittensor.core.config.Config")

property is_empty[#](<#bittensor.core.threadpool.PriorityThreadPoolExecutor.is_empty> "Link to this definition")
    

shutdown(_wait =True_)[#](<#bittensor.core.threadpool.PriorityThreadPoolExecutor.shutdown> "Link to this definition")
    

Clean-up the resources associated with the Executor.

It is safe to call this method several times. Otherwise, no other methods can be called after this one.

Parameters:
    

  * **wait** – If True then shutdown will not return until all running futures have finished executing and the resources used by the executor have been reclaimed.

  * **cancel_futures** – If True then shutdown will cancel all pending futures. Futures that are completed or running will not be cancelled.




submit(_fn_ , _* args_, _** kwargs_)[#](<#bittensor.core.threadpool.PriorityThreadPoolExecutor.submit> "Link to this definition")
    

Submits a callable to be executed with the given arguments.

Schedules the callable to be executed as fn([*](<#id4>)args, [**](<#id6>)kwargs) and returns a Future instance representing the execution of the callable.

Returns:
    

A Future representing the given call.

Parameters:
    

**fn** (_Callable_)

Return type:
    

concurrent.futures._base.Future

bittensor.core.threadpool.logger[#](<#bittensor.core.threadpool.logger> "Link to this definition")
    

[ __ previous bittensor.core.tensor ](<../tensor/index.html> "previous page") [ next bittensor.core.types __](<../types/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Exceptions](<#exceptions>)
  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`BrokenThreadPool`](<#bittensor.core.threadpool.BrokenThreadPool>)
    * [`NULL_ENTRY`](<#bittensor.core.threadpool.NULL_ENTRY>)
    * [`PriorityThreadPoolExecutor`](<#bittensor.core.threadpool.PriorityThreadPoolExecutor>)
      * [`PriorityThreadPoolExecutor.add_args()`](<#bittensor.core.threadpool.PriorityThreadPoolExecutor.add_args>)
      * [`PriorityThreadPoolExecutor.config()`](<#bittensor.core.threadpool.PriorityThreadPoolExecutor.config>)
      * [`PriorityThreadPoolExecutor.is_empty`](<#bittensor.core.threadpool.PriorityThreadPoolExecutor.is_empty>)
      * [`PriorityThreadPoolExecutor.shutdown()`](<#bittensor.core.threadpool.PriorityThreadPoolExecutor.shutdown>)
      * [`PriorityThreadPoolExecutor.submit()`](<#bittensor.core.threadpool.PriorityThreadPoolExecutor.submit>)
    * [`logger`](<#bittensor.core.threadpool.logger>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.