# bittensor.utils.liquidity &#8212; Bittensor SDK Docs  documentation

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
        * [bittensor.utils.liquidity](<#>)
        * [bittensor.utils.networking](<../networking/index.html>)
        * [bittensor.utils.registration](<../registration/index.html>)
        * [bittensor.utils.subnets](<../subnets/index.html>)
        * [bittensor.utils.version](<../version/index.html>)
        * [bittensor.utils.weight_utils](<../weight_utils/index.html>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/utils/liquidity/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/utils/liquidity/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/utils/liquidity/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.utils.liquidity

##  Contents 

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`LiquidityPosition`](<#bittensor.utils.liquidity.LiquidityPosition>)
      * [`LiquidityPosition.fees_alpha`](<#bittensor.utils.liquidity.LiquidityPosition.fees_alpha>)
      * [`LiquidityPosition.fees_tao`](<#bittensor.utils.liquidity.LiquidityPosition.fees_tao>)
      * [`LiquidityPosition.id`](<#bittensor.utils.liquidity.LiquidityPosition.id>)
      * [`LiquidityPosition.liquidity`](<#bittensor.utils.liquidity.LiquidityPosition.liquidity>)
      * [`LiquidityPosition.netuid`](<#bittensor.utils.liquidity.LiquidityPosition.netuid>)
      * [`LiquidityPosition.price_high`](<#bittensor.utils.liquidity.LiquidityPosition.price_high>)
      * [`LiquidityPosition.price_low`](<#bittensor.utils.liquidity.LiquidityPosition.price_low>)
      * [`LiquidityPosition.to_token_amounts()`](<#bittensor.utils.liquidity.LiquidityPosition.to_token_amounts>)
    * [`MAX_TICK`](<#bittensor.utils.liquidity.MAX_TICK>)
    * [`MIN_TICK`](<#bittensor.utils.liquidity.MIN_TICK>)
    * [`PRICE_STEP`](<#bittensor.utils.liquidity.PRICE_STEP>)
    * [`calculate_fees()`](<#bittensor.utils.liquidity.calculate_fees>)
    * [`get_fees()`](<#bittensor.utils.liquidity.get_fees>)
    * [`get_fees_in_range()`](<#bittensor.utils.liquidity.get_fees_in_range>)
    * [`price_to_tick()`](<#bittensor.utils.liquidity.price_to_tick>)
    * [`tick_to_price()`](<#bittensor.utils.liquidity.tick_to_price>)



# bittensor.utils.liquidity[#](<#module-bittensor.utils.liquidity> "Link to this heading")

This module provides utilities for managing liquidity positions and price conversions in the Bittensor network. The module handles conversions between TAO and Alpha tokens while maintaining precise calculations for liquidity provisioning and fee distribution.

## Attributes[#](<#attributes> "Link to this heading")

[`MAX_TICK`](<#bittensor.utils.liquidity.MAX_TICK> "bittensor.utils.liquidity.MAX_TICK") |   
---|---  
[`MIN_TICK`](<#bittensor.utils.liquidity.MIN_TICK> "bittensor.utils.liquidity.MIN_TICK") |   
[`PRICE_STEP`](<#bittensor.utils.liquidity.PRICE_STEP> "bittensor.utils.liquidity.PRICE_STEP") |   
  
## Classes[#](<#classes> "Link to this heading")

[`LiquidityPosition`](<#bittensor.utils.liquidity.LiquidityPosition> "bittensor.utils.liquidity.LiquidityPosition") |   
---|---  
  
## Functions[#](<#functions> "Link to this heading")

[`calculate_fees`](<#bittensor.utils.liquidity.calculate_fees> "bittensor.utils.liquidity.calculate_fees")(position, global_fees_tao, ...) | Calculate fees for a position.  
---|---  
[`get_fees`](<#bittensor.utils.liquidity.get_fees> "bittensor.utils.liquidity.get_fees")(current_tick, tick, tick_index, quote, ...) | Returns the liquidity fee.  
[`get_fees_in_range`](<#bittensor.utils.liquidity.get_fees_in_range> "bittensor.utils.liquidity.get_fees_in_range")(quote, global_fees_tao, ...) | Returns the liquidity fee value in a range.  
[`price_to_tick`](<#bittensor.utils.liquidity.price_to_tick> "bittensor.utils.liquidity.price_to_tick")(price) | Converts a float price to the nearest Uniswap V3 tick index.  
[`tick_to_price`](<#bittensor.utils.liquidity.tick_to_price> "bittensor.utils.liquidity.tick_to_price")(tick) | Convert an integer Uniswap V3 tick index to float price.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.utils.liquidity.LiquidityPosition[#](<#bittensor.utils.liquidity.LiquidityPosition> "Link to this definition")
    

fees_alpha: [bittensor.utils.balance.Balance](<../balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.utils.liquidity.LiquidityPosition.fees_alpha> "Link to this definition")
    

fees_tao: [bittensor.utils.balance.Balance](<../balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.utils.liquidity.LiquidityPosition.fees_tao> "Link to this definition")
    

id: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.utils.liquidity.LiquidityPosition.id> "Link to this definition")
    

liquidity: [bittensor.utils.balance.Balance](<../balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.utils.liquidity.LiquidityPosition.liquidity> "Link to this definition")
    

netuid: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.utils.liquidity.LiquidityPosition.netuid> "Link to this definition")
    

price_high: [bittensor.utils.balance.Balance](<../balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.utils.liquidity.LiquidityPosition.price_high> "Link to this definition")
    

price_low: [bittensor.utils.balance.Balance](<../balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.utils.liquidity.LiquidityPosition.price_low> "Link to this definition")
    

to_token_amounts(_current_subnet_price_)[#](<#bittensor.utils.liquidity.LiquidityPosition.to_token_amounts> "Link to this definition")
    

Convert a position to token amounts.

Parameters:
    

**current_subnet_price** ([_bittensor.utils.balance.Balance_](<../balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")) – current subnet price in Alpha.

Returns:
    

Amount of Alpha in liquidity Amount of TAO in liquidity

Return type:
    

[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]

Liquidity is a combination of TAO and Alpha depending on the price of the subnet at the moment.

bittensor.utils.liquidity.MAX_TICK = 887272[#](<#bittensor.utils.liquidity.MAX_TICK> "Link to this definition")
    

bittensor.utils.liquidity.MIN_TICK = -887272[#](<#bittensor.utils.liquidity.MIN_TICK> "Link to this definition")
    

bittensor.utils.liquidity.PRICE_STEP = 1.0001[#](<#bittensor.utils.liquidity.PRICE_STEP> "Link to this definition")
    

bittensor.utils.liquidity.calculate_fees(_position_ , _global_fees_tao_ , _global_fees_alpha_ , _tao_fees_below_low_ , _tao_fees_above_high_ , _alpha_fees_below_low_ , _alpha_fees_above_high_ , _netuid_)[#](<#bittensor.utils.liquidity.calculate_fees> "Link to this definition")
    

Calculate fees for a position.

Parameters:
    

  * **position** ([_bittensor.core.types.PositionResponse_](<../../core/types/index.html#bittensor.core.types.PositionResponse> "bittensor.core.types.PositionResponse"))

  * **global_fees_tao** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

  * **global_fees_alpha** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

  * **tao_fees_below_low** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

  * **tao_fees_above_high** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

  * **alpha_fees_below_low** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

  * **alpha_fees_above_high** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))



Return type:
    

[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[bittensor.utils.balance.Balance](<../balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance"), [bittensor.utils.balance.Balance](<../balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")]

bittensor.utils.liquidity.get_fees(_current_tick_ , _tick_ , _tick_index_ , _quote_ , _global_fees_tao_ , _global_fees_alpha_ , _above_)[#](<#bittensor.utils.liquidity.get_fees> "Link to this definition")
    

Returns the liquidity fee.

Parameters:
    

  * **current_tick** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

  * **tick** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)"))

  * **tick_index** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

  * **quote** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **global_fees_tao** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

  * **global_fees_alpha** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

  * **above** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))



Return type:
    

[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")

bittensor.utils.liquidity.get_fees_in_range(_quote_ , _global_fees_tao_ , _global_fees_alpha_ , _fees_below_low_ , _fees_above_high_)[#](<#bittensor.utils.liquidity.get_fees_in_range> "Link to this definition")
    

Returns the liquidity fee value in a range.

Parameters:
    

  * **quote** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **global_fees_tao** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

  * **global_fees_alpha** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

  * **fees_below_low** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

  * **fees_above_high** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))



Return type:
    

[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")

bittensor.utils.liquidity.price_to_tick(_price_)[#](<#bittensor.utils.liquidity.price_to_tick> "Link to this definition")
    

Converts a float price to the nearest Uniswap V3 tick index.

Parameters:
    

**price** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

bittensor.utils.liquidity.tick_to_price(_tick_)[#](<#bittensor.utils.liquidity.tick_to_price> "Link to this definition")
    

Convert an integer Uniswap V3 tick index to float price.

Parameters:
    

**tick** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

Return type:
    

[float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")

[ __ previous bittensor.utils.formatting ](<../formatting/index.html> "previous page") [ next bittensor.utils.networking __](<../networking/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`LiquidityPosition`](<#bittensor.utils.liquidity.LiquidityPosition>)
      * [`LiquidityPosition.fees_alpha`](<#bittensor.utils.liquidity.LiquidityPosition.fees_alpha>)
      * [`LiquidityPosition.fees_tao`](<#bittensor.utils.liquidity.LiquidityPosition.fees_tao>)
      * [`LiquidityPosition.id`](<#bittensor.utils.liquidity.LiquidityPosition.id>)
      * [`LiquidityPosition.liquidity`](<#bittensor.utils.liquidity.LiquidityPosition.liquidity>)
      * [`LiquidityPosition.netuid`](<#bittensor.utils.liquidity.LiquidityPosition.netuid>)
      * [`LiquidityPosition.price_high`](<#bittensor.utils.liquidity.LiquidityPosition.price_high>)
      * [`LiquidityPosition.price_low`](<#bittensor.utils.liquidity.LiquidityPosition.price_low>)
      * [`LiquidityPosition.to_token_amounts()`](<#bittensor.utils.liquidity.LiquidityPosition.to_token_amounts>)
    * [`MAX_TICK`](<#bittensor.utils.liquidity.MAX_TICK>)
    * [`MIN_TICK`](<#bittensor.utils.liquidity.MIN_TICK>)
    * [`PRICE_STEP`](<#bittensor.utils.liquidity.PRICE_STEP>)
    * [`calculate_fees()`](<#bittensor.utils.liquidity.calculate_fees>)
    * [`get_fees()`](<#bittensor.utils.liquidity.get_fees>)
    * [`get_fees_in_range()`](<#bittensor.utils.liquidity.get_fees_in_range>)
    * [`price_to_tick()`](<#bittensor.utils.liquidity.price_to_tick>)
    * [`tick_to_price()`](<#bittensor.utils.liquidity.tick_to_price>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.