# bittensor.core.chain_data.dynamic_info &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/dynamic_info/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/dynamic_info/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/dynamic_info/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.dynamic_info

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`DynamicInfo`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo>)
      * [`DynamicInfo.alpha_in`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_in>)
      * [`DynamicInfo.alpha_in_emission`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_in_emission>)
      * [`DynamicInfo.alpha_out`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_out>)
      * [`DynamicInfo.alpha_out_emission`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_out_emission>)
      * [`DynamicInfo.alpha_slippage`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_slippage>)
      * [`DynamicInfo.alpha_to_tao()`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_to_tao>)
      * [`DynamicInfo.alpha_to_tao_with_slippage()`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_to_tao_with_slippage>)
      * [`DynamicInfo.blocks_since_last_step`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.blocks_since_last_step>)
      * [`DynamicInfo.emission`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.emission>)
      * [`DynamicInfo.is_dynamic`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.is_dynamic>)
      * [`DynamicInfo.k`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.k>)
      * [`DynamicInfo.last_step`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.last_step>)
      * [`DynamicInfo.moving_price`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.moving_price>)
      * [`DynamicInfo.netuid`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.netuid>)
      * [`DynamicInfo.network_registered_at`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.network_registered_at>)
      * [`DynamicInfo.owner_coldkey`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.owner_coldkey>)
      * [`DynamicInfo.owner_hotkey`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.owner_hotkey>)
      * [`DynamicInfo.pending_alpha_emission`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.pending_alpha_emission>)
      * [`DynamicInfo.pending_root_emission`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.pending_root_emission>)
      * [`DynamicInfo.price`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.price>)
      * [`DynamicInfo.slippage`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.slippage>)
      * [`DynamicInfo.subnet_identity`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.subnet_identity>)
      * [`DynamicInfo.subnet_name`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.subnet_name>)
      * [`DynamicInfo.subnet_volume`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.subnet_volume>)
      * [`DynamicInfo.symbol`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.symbol>)
      * [`DynamicInfo.tao_in`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.tao_in>)
      * [`DynamicInfo.tao_in_emission`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.tao_in_emission>)
      * [`DynamicInfo.tao_slippage`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.tao_slippage>)
      * [`DynamicInfo.tao_to_alpha()`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.tao_to_alpha>)
      * [`DynamicInfo.tao_to_alpha_with_slippage()`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.tao_to_alpha_with_slippage>)
      * [`DynamicInfo.tempo`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.tempo>)



# bittensor.core.chain_data.dynamic_info[#](<#module-bittensor.core.chain_data.dynamic_info> "Link to this heading")

This module defines the DynamicInfo data class and associated methods for handling and decoding dynamic information in the Bittensor network.

## Classes[#](<#classes> "Link to this heading")

[`DynamicInfo`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo> "bittensor.core.chain_data.dynamic_info.DynamicInfo") |   
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.dynamic_info.DynamicInfo[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo> "Link to this definition")
    

Bases: [`bittensor.core.chain_data.info_base.InfoBase`](<../info_base/index.html#bittensor.core.chain_data.info_base.InfoBase> "bittensor.core.chain_data.info_base.InfoBase")

alpha_in: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_in> "Link to this definition")
    

alpha_in_emission: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_in_emission> "Link to this definition")
    

alpha_out: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_out> "Link to this definition")
    

alpha_out_emission: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_out_emission> "Link to this definition")
    

alpha_slippage[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_slippage> "Link to this definition")
    

alpha_to_tao(_alpha_)[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_to_tao> "Link to this definition")
    

Parameters:
    

**alpha** (_Union_ _[_[_bittensor.utils.balance.Balance_](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") _,_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _,_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_)

Return type:
    

[bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

alpha_to_tao_with_slippage(_alpha_ , _percentage =False_)[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_to_tao_with_slippage> "Link to this definition")
    

Returns an estimate of how much TAO would a staker receive if they unstake their alpha using the current pool state.

Parameters:
    

  * **alpha** (_Union_ _[_[_bittensor.utils.balance.Balance_](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") _,_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _,_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Amount of Alpha to stake.

  * **percentage** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – percentage



Returns:
    

If percentage is False, a tuple of balances where the first part is the amount of TAO received, and the second part (slippage) is the difference between the estimated amount and ideal amount as if there was no slippage. If percentage is True, a float representing the slippage percentage.

Return type:
    

Union[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance"), [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")], [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")]

blocks_since_last_step: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.blocks_since_last_step> "Link to this definition")
    

emission: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.emission> "Link to this definition")
    

is_dynamic: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.is_dynamic> "Link to this definition")
    

k: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.k> "Link to this definition")
    

last_step: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.last_step> "Link to this definition")
    

moving_price: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.moving_price> "Link to this definition")
    

netuid: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.netuid> "Link to this definition")
    

network_registered_at: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.network_registered_at> "Link to this definition")
    

owner_coldkey: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.owner_coldkey> "Link to this definition")
    

owner_hotkey: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.owner_hotkey> "Link to this definition")
    

pending_alpha_emission: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.pending_alpha_emission> "Link to this definition")
    

pending_root_emission: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.pending_root_emission> "Link to this definition")
    

price: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.price> "Link to this definition")
    

slippage[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.slippage> "Link to this definition")
    

subnet_identity: [bittensor.core.chain_data.subnet_identity.SubnetIdentity](<../subnet_identity/index.html#bittensor.core.chain_data.subnet_identity.SubnetIdentity> "bittensor.core.chain_data.subnet_identity.SubnetIdentity") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.subnet_identity> "Link to this definition")
    

subnet_name: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.subnet_name> "Link to this definition")
    

subnet_volume: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.subnet_volume> "Link to this definition")
    

symbol: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.symbol> "Link to this definition")
    

tao_in: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.tao_in> "Link to this definition")
    

tao_in_emission: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.tao_in_emission> "Link to this definition")
    

tao_slippage[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.tao_slippage> "Link to this definition")
    

tao_to_alpha(_tao_)[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.tao_to_alpha> "Link to this definition")
    

Parameters:
    

**tao** (_Union_ _[_[_bittensor.utils.balance.Balance_](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") _,_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _,_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_)

Return type:
    

[bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

tao_to_alpha_with_slippage(_tao_ , _percentage =False_)[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.tao_to_alpha_with_slippage> "Link to this definition")
    

Returns an estimate of how much Alpha would a staker receive if they stake their tao using the current pool state.

Parameters:
    

  * **tao** (_Union_ _[_[_bittensor.utils.balance.Balance_](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") _,_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _,_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Amount of TAO to stake.

  * **percentage** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – percentage



Returns:
    

If percentage is False, a tuple of balances where the first part is the amount of Alpha received, and the second part (slippage) is the difference between the estimated amount and ideal amount as if there was no slippage. If percentage is True, a float representing the slippage percentage.

Return type:
    

Union[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance"), [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")], [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")]

tempo: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.tempo> "Link to this definition")
    

[ __ previous bittensor.core.chain_data.delegate_info_lite ](<../delegate_info_lite/index.html> "previous page") [ next bittensor.core.chain_data.info_base __](<../info_base/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`DynamicInfo`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo>)
      * [`DynamicInfo.alpha_in`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_in>)
      * [`DynamicInfo.alpha_in_emission`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_in_emission>)
      * [`DynamicInfo.alpha_out`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_out>)
      * [`DynamicInfo.alpha_out_emission`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_out_emission>)
      * [`DynamicInfo.alpha_slippage`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_slippage>)
      * [`DynamicInfo.alpha_to_tao()`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_to_tao>)
      * [`DynamicInfo.alpha_to_tao_with_slippage()`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.alpha_to_tao_with_slippage>)
      * [`DynamicInfo.blocks_since_last_step`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.blocks_since_last_step>)
      * [`DynamicInfo.emission`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.emission>)
      * [`DynamicInfo.is_dynamic`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.is_dynamic>)
      * [`DynamicInfo.k`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.k>)
      * [`DynamicInfo.last_step`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.last_step>)
      * [`DynamicInfo.moving_price`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.moving_price>)
      * [`DynamicInfo.netuid`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.netuid>)
      * [`DynamicInfo.network_registered_at`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.network_registered_at>)
      * [`DynamicInfo.owner_coldkey`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.owner_coldkey>)
      * [`DynamicInfo.owner_hotkey`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.owner_hotkey>)
      * [`DynamicInfo.pending_alpha_emission`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.pending_alpha_emission>)
      * [`DynamicInfo.pending_root_emission`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.pending_root_emission>)
      * [`DynamicInfo.price`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.price>)
      * [`DynamicInfo.slippage`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.slippage>)
      * [`DynamicInfo.subnet_identity`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.subnet_identity>)
      * [`DynamicInfo.subnet_name`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.subnet_name>)
      * [`DynamicInfo.subnet_volume`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.subnet_volume>)
      * [`DynamicInfo.symbol`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.symbol>)
      * [`DynamicInfo.tao_in`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.tao_in>)
      * [`DynamicInfo.tao_in_emission`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.tao_in_emission>)
      * [`DynamicInfo.tao_slippage`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.tao_slippage>)
      * [`DynamicInfo.tao_to_alpha()`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.tao_to_alpha>)
      * [`DynamicInfo.tao_to_alpha_with_slippage()`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.tao_to_alpha_with_slippage>)
      * [`DynamicInfo.tempo`](<#bittensor.core.chain_data.dynamic_info.DynamicInfo.tempo>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.