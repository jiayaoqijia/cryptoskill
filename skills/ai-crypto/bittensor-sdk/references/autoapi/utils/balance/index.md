# bittensor.utils.balance &#8212; Bittensor SDK Docs  documentation

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
        * [bittensor.utils.balance](<#>)
        * [bittensor.utils.btlogging](<../btlogging/index.html>)
        * [bittensor.utils.easy_imports](<../easy_imports/index.html>)
        * [bittensor.utils.formatting](<../formatting/index.html>)
        * [bittensor.utils.liquidity](<../liquidity/index.html>)
        * [bittensor.utils.networking](<../networking/index.html>)
        * [bittensor.utils.registration](<../registration/index.html>)
        * [bittensor.utils.subnets](<../subnets/index.html>)
        * [bittensor.utils.version](<../version/index.html>)
        * [bittensor.utils.weight_utils](<../weight_utils/index.html>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/utils/balance/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/utils/balance/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/utils/balance/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.utils.balance

##  Contents 

  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`Balance`](<#bittensor.utils.balance.Balance>)
      * [`Balance.from_float()`](<#bittensor.utils.balance.Balance.from_float>)
      * [`Balance.from_rao()`](<#bittensor.utils.balance.Balance.from_rao>)
      * [`Balance.from_tao()`](<#bittensor.utils.balance.Balance.from_tao>)
      * [`Balance.get_unit()`](<#bittensor.utils.balance.Balance.get_unit>)
      * [`Balance.netuid`](<#bittensor.utils.balance.Balance.netuid>)
      * [`Balance.rao`](<#bittensor.utils.balance.Balance.rao>)
      * [`Balance.rao_unit`](<#bittensor.utils.balance.Balance.rao_unit>)
      * [`Balance.set_unit()`](<#bittensor.utils.balance.Balance.set_unit>)
      * [`Balance.tao`](<#bittensor.utils.balance.Balance.tao>)
      * [`Balance.unit`](<#bittensor.utils.balance.Balance.unit>)
    * [`check_balance_amount()`](<#bittensor.utils.balance.check_balance_amount>)
    * [`rao()`](<#bittensor.utils.balance.rao>)
    * [`tao()`](<#bittensor.utils.balance.tao>)



# bittensor.utils.balance[#](<#module-bittensor.utils.balance> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`Balance`](<#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") | Represents the bittensor balance of the wallet, stored as rao (int).  
---|---  
  
## Functions[#](<#functions> "Link to this heading")

[`check_balance_amount`](<#bittensor.utils.balance.check_balance_amount> "bittensor.utils.balance.check_balance_amount")(amount[, allow_none]) | Validate that the provided value is a Balance instance.  
---|---  
[`rao`](<#bittensor.utils.balance.rao> "bittensor.utils.balance.rao")(amount[, netuid]) | Helper function to create a Balance object from an int (Rao)  
[`tao`](<#bittensor.utils.balance.tao> "bittensor.utils.balance.tao")(amount[, netuid]) | Helper function to create a Balance object from a float (Tao)  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.utils.balance.Balance(_balance_)[#](<#bittensor.utils.balance.Balance> "Link to this definition")
    

Represents the bittensor balance of the wallet, stored as rao (int).

This class provides a way to interact with balances in two different units: rao and tao. It provides methods to convert between these units, as well as to perform arithmetic and comparison operations.

Variables:
    

  * **unit** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – A string representing the symbol for the tao unit.

  * **rao_unit** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – A string representing the symbol for the rao unit.

  * **rao** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – An integer that stores the balance in rao units.

  * **tao** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")) – A float property that gives the balance in tao units.



Parameters:
    

**balance** (_Union_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _,_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _]_)

Note

To ensure arithmetic operations between Balance instances work correctly, they must set the same unit for each using the netuid.

Examples

balance_wallet_default = Balance.from_tao(10, netuid=14) balance_wallet_secret = Balance.from_tao(2, netuid=14) total_balance = balance_wallet_default + balance_wallet_secret

# or

balance_wallet_default = Balance.from_tao(10).set_unit(netuid=14) balance_wallet_secret = Balance.from_tao(2).set_unit(netuid=14) total_balance = balance_wallet_default + balance_wallet_secret

The from_tao() and from_rao() methods accept the netuid parameter to set the appropriate unit symbol.

Note

When performing arithmetic or comparison operations where the first operand is a Balance instance and the second operand is not, the second operand is implicitly interpreted as a raw amount in rao, using the same unit (netuid) as the first operand. This allows interoperability with integer or float values, but may result in unexpected behavior if the caller assumes the second operand is in tao.

Example

balance = Balance.from_tao(10, netuid=14) result = balance + 5000 # 5 will be treated as 5000 rao, not 5 tao print(result) output: τ10.000005000

Initialize a Balance object. If balance is an int, it’s assumed to be in rao. If balance is a float, it’s assumed to be in tao.

Parameters:
    

  * **balance** (_Union_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _,_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _]_)

  * **rao** (_in either_)

  * **balance**




static from_float(_amount_ , _netuid =0_)[#](<#bittensor.utils.balance.Balance.from_float> "Link to this definition")
    

Given tao, return [`Balance()`](<#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") object with rao(`int`) and tao(`float`), where rao = int(tao*pow(10,9))

Parameters:
    

  * **amount** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")) – The amount in tao.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet uid for set currency unit.



Returns:
    

A Balance object representing the given amount.

Return type:
    

[Balance](<#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

static from_rao(_amount_ , _netuid =0_)[#](<#bittensor.utils.balance.Balance.from_rao> "Link to this definition")
    

Given rao, return Balance object with rao(`int`) and tao(`float`), where rao = int(tao*pow(10,9))

Parameters:
    

  * **amount** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The amount in rao.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet uid for set currency unit.



Returns:
    

A Balance object representing the given amount.

Return type:
    

[Balance](<#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

static from_tao(_amount_ , _netuid =0_)[#](<#bittensor.utils.balance.Balance.from_tao> "Link to this definition")
    

Given tao, return Balance object with rao(`int`) and tao(`float`), where rao = int(tao*pow(10,9))

Parameters:
    

  * **amount** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")) – The amount in tao.

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The subnet uid for set currency unit.



Returns:
    

A Balance object representing the given amount.

Return type:
    

[Balance](<#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

static get_unit(_netuid_)[#](<#bittensor.utils.balance.Balance.get_unit> "Link to this definition")
    

Parameters:
    

**netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

netuid: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") = 0[#](<#bittensor.utils.balance.Balance.netuid> "Link to this definition")
    

rao: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.utils.balance.Balance.rao> "Link to this definition")
    

rao_unit: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.utils.balance.Balance.rao_unit> "Link to this definition")
    

set_unit(_netuid_)[#](<#bittensor.utils.balance.Balance.set_unit> "Link to this definition")
    

Parameters:
    

**netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

property tao[#](<#bittensor.utils.balance.Balance.tao> "Link to this definition")
    

unit: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.utils.balance.Balance.unit> "Link to this definition")
    

bittensor.utils.balance.check_balance_amount(_amount_ , _allow_none =True_)[#](<#bittensor.utils.balance.check_balance_amount> "Link to this definition")
    

Validate that the provided value is a Balance instance.

This function ensures that the amount argument is a Balance object. If a non-Balance type is passed, it raises a BalanceTypeError to enforce consistent usage of Balance objects across arithmetic operations.

Parameters:
    

  * **amount** (_Optional_ _[_[_Balance_](<#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") _]_) – The value to validate.

  * **allow_none** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – if False then a BalanceTypeError is raised if the value is None.



Returns:
    

Always returns None if validation passes.

Return type:
    

None

Raises:
    

[**BalanceTypeError**](<../../core/errors/index.html#bittensor.core.errors.BalanceTypeError> "bittensor.core.errors.BalanceTypeError") – If amount is not a Balance instance and not None.

bittensor.utils.balance.rao(_amount_ , _netuid =0_)[#](<#bittensor.utils.balance.rao> "Link to this definition")
    

Helper function to create a Balance object from an int (Rao)

Parameters:
    

  * **amount** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))



Return type:
    

[Balance](<#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

bittensor.utils.balance.tao(_amount_ , _netuid =0_)[#](<#bittensor.utils.balance.tao> "Link to this definition")
    

Helper function to create a Balance object from a float (Tao)

Parameters:
    

  * **amount** ([_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)"))

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))



Return type:
    

[Balance](<#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")

[ __ previous bittensor.utils.axon_utils ](<../axon_utils/index.html> "previous page") [ next bittensor.utils.btlogging __](<../btlogging/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`Balance`](<#bittensor.utils.balance.Balance>)
      * [`Balance.from_float()`](<#bittensor.utils.balance.Balance.from_float>)
      * [`Balance.from_rao()`](<#bittensor.utils.balance.Balance.from_rao>)
      * [`Balance.from_tao()`](<#bittensor.utils.balance.Balance.from_tao>)
      * [`Balance.get_unit()`](<#bittensor.utils.balance.Balance.get_unit>)
      * [`Balance.netuid`](<#bittensor.utils.balance.Balance.netuid>)
      * [`Balance.rao`](<#bittensor.utils.balance.Balance.rao>)
      * [`Balance.rao_unit`](<#bittensor.utils.balance.Balance.rao_unit>)
      * [`Balance.set_unit()`](<#bittensor.utils.balance.Balance.set_unit>)
      * [`Balance.tao`](<#bittensor.utils.balance.Balance.tao>)
      * [`Balance.unit`](<#bittensor.utils.balance.Balance.unit>)
    * [`check_balance_amount()`](<#bittensor.utils.balance.check_balance_amount>)
    * [`rao()`](<#bittensor.utils.balance.rao>)
    * [`tao()`](<#bittensor.utils.balance.tao>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.