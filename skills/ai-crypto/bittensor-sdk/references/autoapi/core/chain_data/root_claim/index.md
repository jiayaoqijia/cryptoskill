# bittensor.core.chain_data.root_claim &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/root_claim/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/root_claim/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/root_claim/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.root_claim

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`KeepSubnetsDescriptor`](<#bittensor.core.chain_data.root_claim.KeepSubnetsDescriptor>)
      * [`KeepSubnetsDescriptor.subnets`](<#bittensor.core.chain_data.root_claim.KeepSubnetsDescriptor.subnets>)
      * [`KeepSubnetsDescriptor.to_dict()`](<#bittensor.core.chain_data.root_claim.KeepSubnetsDescriptor.to_dict>)
    * [`RootClaimType`](<#bittensor.core.chain_data.root_claim.RootClaimType>)
      * [`RootClaimType.Keep`](<#bittensor.core.chain_data.root_claim.RootClaimType.Keep>)
      * [`RootClaimType.KeepSubnets`](<#bittensor.core.chain_data.root_claim.RootClaimType.KeepSubnets>)
      * [`RootClaimType.Swap`](<#bittensor.core.chain_data.root_claim.RootClaimType.Swap>)
      * [`RootClaimType.normalize()`](<#bittensor.core.chain_data.root_claim.RootClaimType.normalize>)



# bittensor.core.chain_data.root_claim[#](<#module-bittensor.core.chain_data.root_claim> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`KeepSubnetsDescriptor`](<#bittensor.core.chain_data.root_claim.KeepSubnetsDescriptor> "bittensor.core.chain_data.root_claim.KeepSubnetsDescriptor") | Descriptor that allows callable syntax for KeepSubnets variant.  
---|---  
[`RootClaimType`](<#bittensor.core.chain_data.root_claim.RootClaimType> "bittensor.core.chain_data.root_claim.RootClaimType") | Enumeration of root claim types in the Bittensor network.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.root_claim.KeepSubnetsDescriptor[#](<#bittensor.core.chain_data.root_claim.KeepSubnetsDescriptor> "Link to this definition")
    

Descriptor that allows callable syntax for KeepSubnets variant.

subnets: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.root_claim.KeepSubnetsDescriptor.subnets> "Link to this definition")
    

to_dict()[#](<#bittensor.core.chain_data.root_claim.KeepSubnetsDescriptor.to_dict> "Link to this definition")
    

Converts the descriptor to the required dictionary format.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")

class bittensor.core.chain_data.root_claim.RootClaimType[#](<#bittensor.core.chain_data.root_claim.RootClaimType> "Link to this definition")
    

Bases: [`str`](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [`enum.Enum`](<https://docs.python.org/3/library/enum.html#enum.Enum> "\(in Python v3.14\)")

Enumeration of root claim types in the Bittensor network.

This enum defines how coldkeys manage their root alpha emissions: \- Swap: Swap any alpha emission for TAO \- Keep: Keep all alpha emission \- KeepSubnets: Keep alpha emission for specified subnets, swap everything else

The values match exactly with the RootClaimTypeEnum defined in the Subtensor runtime.

Initialize self. See help(type(self)) for accurate signature.

Keep = 'Keep'[#](<#bittensor.core.chain_data.root_claim.RootClaimType.Keep> "Link to this definition")
    

KeepSubnets[#](<#bittensor.core.chain_data.root_claim.RootClaimType.KeepSubnets> "Link to this definition")
    

Swap = 'Swap'[#](<#bittensor.core.chain_data.root_claim.RootClaimType.Swap> "Link to this definition")
    

classmethod normalize(_value_)[#](<#bittensor.core.chain_data.root_claim.RootClaimType.normalize> "Link to this definition")
    

Normalizes a root claim type to a format suitable for Substrate calls.

This method handles various input formats: \- String values (“Swap”, “Keep”) → returns string \- Enum values (RootClaimType.Swap) → returns string \- Dict values ({“KeepSubnets”: {“subnets”: [1, 2, 3]}}) → returns dict as-is \- Callable KeepSubnets([1, 2, 3]) → returns dict

Parameters:
    

**value** (_Literal_ _[__'Swap'__,__'Keep'__]__|__RootClaimType_ _|__dict_) – The root claim type in any supported format.

Returns:
    

Normalized value - string for Swap/Keep or dict for KeepSubnets.

Raises:
    

  * [**ValueError**](<https://docs.python.org/3/library/exceptions.html#ValueError> "\(in Python v3.14\)") – If the value is not a valid root claim type or KeepSubnets has no subnets.

  * [**TypeError**](<https://docs.python.org/3/library/exceptions.html#TypeError> "\(in Python v3.14\)") – If the value type is not supported.



Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") | [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")

[ __ previous bittensor.core.chain_data.proxy ](<../proxy/index.html> "previous page") [ next bittensor.core.chain_data.scheduled_coldkey_swap_info __](<../scheduled_coldkey_swap_info/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`KeepSubnetsDescriptor`](<#bittensor.core.chain_data.root_claim.KeepSubnetsDescriptor>)
      * [`KeepSubnetsDescriptor.subnets`](<#bittensor.core.chain_data.root_claim.KeepSubnetsDescriptor.subnets>)
      * [`KeepSubnetsDescriptor.to_dict()`](<#bittensor.core.chain_data.root_claim.KeepSubnetsDescriptor.to_dict>)
    * [`RootClaimType`](<#bittensor.core.chain_data.root_claim.RootClaimType>)
      * [`RootClaimType.Keep`](<#bittensor.core.chain_data.root_claim.RootClaimType.Keep>)
      * [`RootClaimType.KeepSubnets`](<#bittensor.core.chain_data.root_claim.RootClaimType.KeepSubnets>)
      * [`RootClaimType.Swap`](<#bittensor.core.chain_data.root_claim.RootClaimType.Swap>)
      * [`RootClaimType.normalize()`](<#bittensor.core.chain_data.root_claim.RootClaimType.normalize>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.