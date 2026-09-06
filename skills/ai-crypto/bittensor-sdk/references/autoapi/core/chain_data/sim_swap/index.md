# bittensor.core.chain_data.sim_swap &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/sim_swap/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/sim_swap/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/sim_swap/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.sim_swap

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`SimSwapResult`](<#bittensor.core.chain_data.sim_swap.SimSwapResult>)
      * [`SimSwapResult.alpha_amount`](<#bittensor.core.chain_data.sim_swap.SimSwapResult.alpha_amount>)
      * [`SimSwapResult.alpha_fee`](<#bittensor.core.chain_data.sim_swap.SimSwapResult.alpha_fee>)
      * [`SimSwapResult.from_dict()`](<#bittensor.core.chain_data.sim_swap.SimSwapResult.from_dict>)
      * [`SimSwapResult.tao_amount`](<#bittensor.core.chain_data.sim_swap.SimSwapResult.tao_amount>)
      * [`SimSwapResult.tao_fee`](<#bittensor.core.chain_data.sim_swap.SimSwapResult.tao_fee>)



# bittensor.core.chain_data.sim_swap[#](<#module-bittensor.core.chain_data.sim_swap> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`SimSwapResult`](<#bittensor.core.chain_data.sim_swap.SimSwapResult> "bittensor.core.chain_data.sim_swap.SimSwapResult") | Represents the result of a simulated swap operation.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.sim_swap.SimSwapResult[#](<#bittensor.core.chain_data.sim_swap.SimSwapResult> "Link to this definition")
    

Represents the result of a simulated swap operation.

This class is used to encapsulate the amounts and fees for the simulated swap process, including both tao and alpha token values. It provides a convenient way to manage and interpret the swap results.

Variables:
    

  * **tao_amount** – The amount of tao tokens obtained as the result of the swap.

  * **alpha_amount** – The amount of alpha tokens obtained as the result of the swap.

  * **tao_fee** – The fee associated with the tao token portion of the swap.

  * **alpha_fee** – The fee associated with the alpha token portion of the swap.




alpha_amount: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.sim_swap.SimSwapResult.alpha_amount> "Link to this definition")
    

alpha_fee: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.sim_swap.SimSwapResult.alpha_fee> "Link to this definition")
    

classmethod from_dict(_data_ , _netuid_)[#](<#bittensor.core.chain_data.sim_swap.SimSwapResult.from_dict> "Link to this definition")
    

Converts a dictionary to a SimSwapResult instance.

This method acts as a factory to create a SimSwapResult object using the data from a dictionary. It parses the specified dictionary, converts values into Balance objects, and sets associated units based on parameters and context.

Parameters:
    

  * **data** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")) – A dictionary containing the swap result data. It must include the keys “tao_amount”, “alpha_amount”, “tao_fee”, and “alpha_fee” with their respective values.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – A network-specific unit identifier used to set the unit for alpha-related amounts.



Returns:
    

An instance of SimSwapResult initialized with the parsed and converted data.

Return type:
    

[SimSwapResult](<#bittensor.core.chain_data.sim_swap.SimSwapResult> "bittensor.core.chain_data.sim_swap.SimSwapResult")

tao_amount: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.sim_swap.SimSwapResult.tao_amount> "Link to this definition")
    

tao_fee: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.sim_swap.SimSwapResult.tao_fee> "Link to this definition")
    

[ __ previous bittensor.core.chain_data.scheduled_coldkey_swap_info ](<../scheduled_coldkey_swap_info/index.html> "previous page") [ next bittensor.core.chain_data.stake_info __](<../stake_info/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`SimSwapResult`](<#bittensor.core.chain_data.sim_swap.SimSwapResult>)
      * [`SimSwapResult.alpha_amount`](<#bittensor.core.chain_data.sim_swap.SimSwapResult.alpha_amount>)
      * [`SimSwapResult.alpha_fee`](<#bittensor.core.chain_data.sim_swap.SimSwapResult.alpha_fee>)
      * [`SimSwapResult.from_dict()`](<#bittensor.core.chain_data.sim_swap.SimSwapResult.from_dict>)
      * [`SimSwapResult.tao_amount`](<#bittensor.core.chain_data.sim_swap.SimSwapResult.tao_amount>)
      * [`SimSwapResult.tao_fee`](<#bittensor.core.chain_data.sim_swap.SimSwapResult.tao_fee>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.