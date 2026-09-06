# bittensor.extras.dev_framework.subnet &#8212; Bittensor SDK Docs  documentation

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
      * [bittensor.extras](<../../index.html>) __
        * [bittensor.extras.dev_framework](<../index.html>)
        * [bittensor.extras.subtensor_api](<../../subtensor_api/index.html>)
        * [bittensor.extras.timelock](<../../timelock/index.html>)
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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/extras/dev_framework/subnet/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/extras/dev_framework/subnet/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/extras/dev_framework/subnet/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.extras.dev_framework.subnet

##  Contents 

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`CALL_RECORD`](<#bittensor.extras.dev_framework.subnet.CALL_RECORD>)
      * [`CALL_RECORD.idx`](<#bittensor.extras.dev_framework.subnet.CALL_RECORD.idx>)
      * [`CALL_RECORD.operation`](<#bittensor.extras.dev_framework.subnet.CALL_RECORD.operation>)
      * [`CALL_RECORD.response`](<#bittensor.extras.dev_framework.subnet.CALL_RECORD.response>)
    * [`NETUID`](<#bittensor.extras.dev_framework.subnet.NETUID>)
    * [`TestSubnet`](<#bittensor.extras.dev_framework.subnet.TestSubnet>)
      * [`TestSubnet.async_execute_one()`](<#bittensor.extras.dev_framework.subnet.TestSubnet.async_execute_one>)
      * [`TestSubnet.async_execute_steps()`](<#bittensor.extras.dev_framework.subnet.TestSubnet.async_execute_steps>)
      * [`TestSubnet.async_set_hyperparameter()`](<#bittensor.extras.dev_framework.subnet.TestSubnet.async_set_hyperparameter>)
      * [`TestSubnet.async_wait_next_epoch()`](<#bittensor.extras.dev_framework.subnet.TestSubnet.async_wait_next_epoch>)
      * [`TestSubnet.calls`](<#bittensor.extras.dev_framework.subnet.TestSubnet.calls>)
      * [`TestSubnet.execute_one()`](<#bittensor.extras.dev_framework.subnet.TestSubnet.execute_one>)
      * [`TestSubnet.execute_steps()`](<#bittensor.extras.dev_framework.subnet.TestSubnet.execute_steps>)
      * [`TestSubnet.netuid`](<#bittensor.extras.dev_framework.subnet.TestSubnet.netuid>)
      * [`TestSubnet.owner`](<#bittensor.extras.dev_framework.subnet.TestSubnet.owner>)
      * [`TestSubnet.period`](<#bittensor.extras.dev_framework.subnet.TestSubnet.period>)
      * [`TestSubnet.raise_error`](<#bittensor.extras.dev_framework.subnet.TestSubnet.raise_error>)
      * [`TestSubnet.s`](<#bittensor.extras.dev_framework.subnet.TestSubnet.s>)
      * [`TestSubnet.set_hyperparameter()`](<#bittensor.extras.dev_framework.subnet.TestSubnet.set_hyperparameter>)
      * [`TestSubnet.wait_for_finalization`](<#bittensor.extras.dev_framework.subnet.TestSubnet.wait_for_finalization>)
      * [`TestSubnet.wait_for_inclusion`](<#bittensor.extras.dev_framework.subnet.TestSubnet.wait_for_inclusion>)
      * [`TestSubnet.wait_next_epoch()`](<#bittensor.extras.dev_framework.subnet.TestSubnet.wait_next_epoch>)



# bittensor.extras.dev_framework.subnet[#](<#module-bittensor.extras.dev_framework.subnet> "Link to this heading")

## Attributes[#](<#attributes> "Link to this heading")

[`NETUID`](<#bittensor.extras.dev_framework.subnet.NETUID> "bittensor.extras.dev_framework.subnet.NETUID") |   
---|---  
  
## Classes[#](<#classes> "Link to this heading")

[`CALL_RECORD`](<#bittensor.extras.dev_framework.subnet.CALL_RECORD> "bittensor.extras.dev_framework.subnet.CALL_RECORD") |   
---|---  
[`TestSubnet`](<#bittensor.extras.dev_framework.subnet.TestSubnet> "bittensor.extras.dev_framework.subnet.TestSubnet") | Class for managing test subnet operations.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.extras.dev_framework.subnet.CALL_RECORD[#](<#bittensor.extras.dev_framework.subnet.CALL_RECORD> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

idx[#](<#bittensor.extras.dev_framework.subnet.CALL_RECORD.idx> "Link to this definition")
    

operation[#](<#bittensor.extras.dev_framework.subnet.CALL_RECORD.operation> "Link to this definition")
    

response[#](<#bittensor.extras.dev_framework.subnet.CALL_RECORD.response> "Link to this definition")
    

bittensor.extras.dev_framework.subnet.NETUID = 'SN_NETUID'[#](<#bittensor.extras.dev_framework.subnet.NETUID> "Link to this definition")
    

class bittensor.extras.dev_framework.subnet.TestSubnet(_subtensor_ , _netuid =None_, _period =DEFAULT_PERIOD_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_)[#](<#bittensor.extras.dev_framework.subnet.TestSubnet> "Link to this definition")
    

Class for managing test subnet operations.

Parameters:
    

  * **subtensor** (_bittensor.extras.SubtensorApi_)

  * **netuid** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_)

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_)

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))




async async_execute_one(_step_)[#](<#bittensor.extras.dev_framework.subnet.TestSubnet.async_execute_one> "Link to this definition")
    

Executes one step asynchronously.

Parameters:
    

**step** (_Union_ _[_[_bittensor.extras.dev_framework.utils.STEPS_](<../utils/index.html#bittensor.extras.dev_framework.utils.STEPS> "bittensor.extras.dev_framework.utils.STEPS") _,_[_tuple_](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)") _]_)

Return type:
    

[bittensor.core.types.ExtrinsicResponse](<../../../core/types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

async async_execute_steps(_steps_)[#](<#bittensor.extras.dev_framework.subnet.TestSubnet.async_execute_steps> "Link to this definition")
    

Executes a multiple steps asynchronously.

Parameters:
    

**steps** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[__Union_ _[_[_bittensor.extras.dev_framework.utils.STEPS_](<../utils/index.html#bittensor.extras.dev_framework.utils.STEPS> "bittensor.extras.dev_framework.utils.STEPS") _,_[_tuple_](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)") _]__]_)

async async_set_hyperparameter(_sudo_or_owner_wallet_ , _call_function_ , _call_module_ , _call_params_ , _sudo_call =False_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_)[#](<#bittensor.extras.dev_framework.subnet.TestSubnet.async_set_hyperparameter> "Link to this definition")
    

Set hyperparameter for the chain or subnet.

Parameters:
    

  * **sudo_or_owner_wallet** (_bittensor_wallet.Wallet_)

  * **call_function** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

  * **call_module** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

  * **call_params** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)"))

  * **sudo_call** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_)

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))



Return type:
    

[bittensor.core.types.ExtrinsicResponse](<../../../core/types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

async async_wait_next_epoch(_netuid =None_)[#](<#bittensor.extras.dev_framework.subnet.TestSubnet.async_wait_next_epoch> "Link to this definition")
    

Async wait until the next epoch first block is reached.

Parameters:
    

**netuid** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_)

property calls: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[CALL_RECORD](<#bittensor.extras.dev_framework.subnet.CALL_RECORD> "bittensor.extras.dev_framework.subnet.CALL_RECORD")][#](<#bittensor.extras.dev_framework.subnet.TestSubnet.calls> "Link to this definition")
    

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[CALL_RECORD](<#bittensor.extras.dev_framework.subnet.CALL_RECORD> "bittensor.extras.dev_framework.subnet.CALL_RECORD")]

execute_one(_step_)[#](<#bittensor.extras.dev_framework.subnet.TestSubnet.execute_one> "Link to this definition")
    

Executes one step synchronously.

Parameters:
    

**step** (_Union_ _[_[_bittensor.extras.dev_framework.utils.STEPS_](<../utils/index.html#bittensor.extras.dev_framework.utils.STEPS> "bittensor.extras.dev_framework.utils.STEPS") _,_[_tuple_](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)") _]_)

Return type:
    

[bittensor.core.types.ExtrinsicResponse](<../../../core/types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

execute_steps(_steps_)[#](<#bittensor.extras.dev_framework.subnet.TestSubnet.execute_steps> "Link to this definition")
    

Executes a multiple steps synchronously.

Parameters:
    

**steps** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[__Union_ _[_[_bittensor.extras.dev_framework.utils.STEPS_](<../utils/index.html#bittensor.extras.dev_framework.utils.STEPS> "bittensor.extras.dev_framework.utils.STEPS") _,_[_tuple_](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)") _]__]_)

property netuid: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.extras.dev_framework.subnet.TestSubnet.netuid> "Link to this definition")
    

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

property owner: bittensor_wallet.Wallet[#](<#bittensor.extras.dev_framework.subnet.TestSubnet.owner> "Link to this definition")
    

Return type:
    

bittensor_wallet.Wallet

period = 128[#](<#bittensor.extras.dev_framework.subnet.TestSubnet.period> "Link to this definition")
    

raise_error = False[#](<#bittensor.extras.dev_framework.subnet.TestSubnet.raise_error> "Link to this definition")
    

s: bittensor.extras.SubtensorApi[#](<#bittensor.extras.dev_framework.subnet.TestSubnet.s> "Link to this definition")
    

set_hyperparameter(_sudo_or_owner_wallet_ , _call_function_ , _call_module_ , _call_params_ , _sudo_call =False_, _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_)[#](<#bittensor.extras.dev_framework.subnet.TestSubnet.set_hyperparameter> "Link to this definition")
    

Set hyperparameter for the chain or subnet.

Parameters:
    

  * **sudo_or_owner_wallet** (_bittensor_wallet.Wallet_)

  * **call_function** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

  * **call_module** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

  * **call_params** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)"))

  * **sudo_call** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_)

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))



Return type:
    

[bittensor.core.types.ExtrinsicResponse](<../../../core/types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

wait_for_finalization = True[#](<#bittensor.extras.dev_framework.subnet.TestSubnet.wait_for_finalization> "Link to this definition")
    

wait_for_inclusion = True[#](<#bittensor.extras.dev_framework.subnet.TestSubnet.wait_for_inclusion> "Link to this definition")
    

wait_next_epoch(_netuid =None_)[#](<#bittensor.extras.dev_framework.subnet.TestSubnet.wait_next_epoch> "Link to this definition")
    

Sync wait until the next epoch first block is reached.

Parameters:
    

**netuid** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_)

[ __ previous bittensor.extras.dev_framework.calls.sudo_calls ](<../calls/sudo_calls/index.html> "previous page") [ next bittensor.extras.dev_framework.utils __](<../utils/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`CALL_RECORD`](<#bittensor.extras.dev_framework.subnet.CALL_RECORD>)
      * [`CALL_RECORD.idx`](<#bittensor.extras.dev_framework.subnet.CALL_RECORD.idx>)
      * [`CALL_RECORD.operation`](<#bittensor.extras.dev_framework.subnet.CALL_RECORD.operation>)
      * [`CALL_RECORD.response`](<#bittensor.extras.dev_framework.subnet.CALL_RECORD.response>)
    * [`NETUID`](<#bittensor.extras.dev_framework.subnet.NETUID>)
    * [`TestSubnet`](<#bittensor.extras.dev_framework.subnet.TestSubnet>)
      * [`TestSubnet.async_execute_one()`](<#bittensor.extras.dev_framework.subnet.TestSubnet.async_execute_one>)
      * [`TestSubnet.async_execute_steps()`](<#bittensor.extras.dev_framework.subnet.TestSubnet.async_execute_steps>)
      * [`TestSubnet.async_set_hyperparameter()`](<#bittensor.extras.dev_framework.subnet.TestSubnet.async_set_hyperparameter>)
      * [`TestSubnet.async_wait_next_epoch()`](<#bittensor.extras.dev_framework.subnet.TestSubnet.async_wait_next_epoch>)
      * [`TestSubnet.calls`](<#bittensor.extras.dev_framework.subnet.TestSubnet.calls>)
      * [`TestSubnet.execute_one()`](<#bittensor.extras.dev_framework.subnet.TestSubnet.execute_one>)
      * [`TestSubnet.execute_steps()`](<#bittensor.extras.dev_framework.subnet.TestSubnet.execute_steps>)
      * [`TestSubnet.netuid`](<#bittensor.extras.dev_framework.subnet.TestSubnet.netuid>)
      * [`TestSubnet.owner`](<#bittensor.extras.dev_framework.subnet.TestSubnet.owner>)
      * [`TestSubnet.period`](<#bittensor.extras.dev_framework.subnet.TestSubnet.period>)
      * [`TestSubnet.raise_error`](<#bittensor.extras.dev_framework.subnet.TestSubnet.raise_error>)
      * [`TestSubnet.s`](<#bittensor.extras.dev_framework.subnet.TestSubnet.s>)
      * [`TestSubnet.set_hyperparameter()`](<#bittensor.extras.dev_framework.subnet.TestSubnet.set_hyperparameter>)
      * [`TestSubnet.wait_for_finalization`](<#bittensor.extras.dev_framework.subnet.TestSubnet.wait_for_finalization>)
      * [`TestSubnet.wait_for_inclusion`](<#bittensor.extras.dev_framework.subnet.TestSubnet.wait_for_inclusion>)
      * [`TestSubnet.wait_next_epoch()`](<#bittensor.extras.dev_framework.subnet.TestSubnet.wait_next_epoch>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.