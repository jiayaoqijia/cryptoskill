# bittensor.extras.dev_framework.utils &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/extras/dev_framework/utils/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/extras/dev_framework/utils/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/extras/dev_framework/utils/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.extras.dev_framework.utils

##  Contents 

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`ACTIVATE_SUBNET`](<#bittensor.extras.dev_framework.utils.ACTIVATE_SUBNET>)
    * [`ActivateSubnet`](<#bittensor.extras.dev_framework.utils.ActivateSubnet>)
      * [`ActivateSubnet.netuid`](<#bittensor.extras.dev_framework.utils.ActivateSubnet.netuid>)
      * [`ActivateSubnet.wallet`](<#bittensor.extras.dev_framework.utils.ActivateSubnet.wallet>)
    * [`REGISTER_NEURON`](<#bittensor.extras.dev_framework.utils.REGISTER_NEURON>)
    * [`REGISTER_SUBNET`](<#bittensor.extras.dev_framework.utils.REGISTER_SUBNET>)
    * [`RegisterNeuron`](<#bittensor.extras.dev_framework.utils.RegisterNeuron>)
      * [`RegisterNeuron.netuid`](<#bittensor.extras.dev_framework.utils.RegisterNeuron.netuid>)
      * [`RegisterNeuron.wallet`](<#bittensor.extras.dev_framework.utils.RegisterNeuron.wallet>)
    * [`RegisterSubnet`](<#bittensor.extras.dev_framework.utils.RegisterSubnet>)
      * [`RegisterSubnet.wallet`](<#bittensor.extras.dev_framework.utils.RegisterSubnet.wallet>)
    * [`STEPS`](<#bittensor.extras.dev_framework.utils.STEPS>)
    * [`is_instance_namedtuple()`](<#bittensor.extras.dev_framework.utils.is_instance_namedtuple>)
    * [`split_command()`](<#bittensor.extras.dev_framework.utils.split_command>)



# bittensor.extras.dev_framework.utils[#](<#module-bittensor.extras.dev_framework.utils> "Link to this heading")

## Attributes[#](<#attributes> "Link to this heading")

[`ACTIVATE_SUBNET`](<#bittensor.extras.dev_framework.utils.ACTIVATE_SUBNET> "bittensor.extras.dev_framework.utils.ACTIVATE_SUBNET") |   
---|---  
[`REGISTER_NEURON`](<#bittensor.extras.dev_framework.utils.REGISTER_NEURON> "bittensor.extras.dev_framework.utils.REGISTER_NEURON") |   
[`REGISTER_SUBNET`](<#bittensor.extras.dev_framework.utils.REGISTER_SUBNET> "bittensor.extras.dev_framework.utils.REGISTER_SUBNET") |   
[`STEPS`](<#bittensor.extras.dev_framework.utils.STEPS> "bittensor.extras.dev_framework.utils.STEPS") |   
  
## Classes[#](<#classes> "Link to this heading")

[`ActivateSubnet`](<#bittensor.extras.dev_framework.utils.ActivateSubnet> "bittensor.extras.dev_framework.utils.ActivateSubnet") |   
---|---  
[`RegisterNeuron`](<#bittensor.extras.dev_framework.utils.RegisterNeuron> "bittensor.extras.dev_framework.utils.RegisterNeuron") |   
[`RegisterSubnet`](<#bittensor.extras.dev_framework.utils.RegisterSubnet> "bittensor.extras.dev_framework.utils.RegisterSubnet") |   
  
## Functions[#](<#functions> "Link to this heading")

[`is_instance_namedtuple`](<#bittensor.extras.dev_framework.utils.is_instance_namedtuple> "bittensor.extras.dev_framework.utils.is_instance_namedtuple")(obj) | Check if the object is an instance of a namedtuple.  
---|---  
[`split_command`](<#bittensor.extras.dev_framework.utils.split_command> "bittensor.extras.dev_framework.utils.split_command")(command) | Parse command and return four objects (wallet, pallet, sudo, kwargs).  
  
## Module Contents[#](<#module-contents> "Link to this heading")

bittensor.extras.dev_framework.utils.ACTIVATE_SUBNET[#](<#bittensor.extras.dev_framework.utils.ACTIVATE_SUBNET> "Link to this definition")
    

class bittensor.extras.dev_framework.utils.ActivateSubnet[#](<#bittensor.extras.dev_framework.utils.ActivateSubnet> "Link to this definition")
    

netuid: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)") = None[#](<#bittensor.extras.dev_framework.utils.ActivateSubnet.netuid> "Link to this definition")
    

wallet: bittensor_wallet.Wallet[#](<#bittensor.extras.dev_framework.utils.ActivateSubnet.wallet> "Link to this definition")
    

bittensor.extras.dev_framework.utils.REGISTER_NEURON[#](<#bittensor.extras.dev_framework.utils.REGISTER_NEURON> "Link to this definition")
    

bittensor.extras.dev_framework.utils.REGISTER_SUBNET[#](<#bittensor.extras.dev_framework.utils.REGISTER_SUBNET> "Link to this definition")
    

class bittensor.extras.dev_framework.utils.RegisterNeuron[#](<#bittensor.extras.dev_framework.utils.RegisterNeuron> "Link to this definition")
    

netuid: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)") = None[#](<#bittensor.extras.dev_framework.utils.RegisterNeuron.netuid> "Link to this definition")
    

wallet: bittensor_wallet.Wallet[#](<#bittensor.extras.dev_framework.utils.RegisterNeuron.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.utils.RegisterSubnet[#](<#bittensor.extras.dev_framework.utils.RegisterSubnet> "Link to this definition")
    

wallet: bittensor_wallet.Wallet[#](<#bittensor.extras.dev_framework.utils.RegisterSubnet.wallet> "Link to this definition")
    

bittensor.extras.dev_framework.utils.STEPS[#](<#bittensor.extras.dev_framework.utils.STEPS> "Link to this definition")
    

bittensor.extras.dev_framework.utils.is_instance_namedtuple(_obj_)[#](<#bittensor.extras.dev_framework.utils.is_instance_namedtuple> "Link to this definition")
    

Check if the object is an instance of a namedtuple.

bittensor.extras.dev_framework.utils.split_command(_command_)[#](<#bittensor.extras.dev_framework.utils.split_command> "Link to this definition")
    

Parse command and return four objects (wallet, pallet, sudo, kwargs).

[ __ previous bittensor.extras.dev_framework.subnet ](<../subnet/index.html> "previous page") [ next bittensor.extras.subtensor_api __](<../../subtensor_api/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`ACTIVATE_SUBNET`](<#bittensor.extras.dev_framework.utils.ACTIVATE_SUBNET>)
    * [`ActivateSubnet`](<#bittensor.extras.dev_framework.utils.ActivateSubnet>)
      * [`ActivateSubnet.netuid`](<#bittensor.extras.dev_framework.utils.ActivateSubnet.netuid>)
      * [`ActivateSubnet.wallet`](<#bittensor.extras.dev_framework.utils.ActivateSubnet.wallet>)
    * [`REGISTER_NEURON`](<#bittensor.extras.dev_framework.utils.REGISTER_NEURON>)
    * [`REGISTER_SUBNET`](<#bittensor.extras.dev_framework.utils.REGISTER_SUBNET>)
    * [`RegisterNeuron`](<#bittensor.extras.dev_framework.utils.RegisterNeuron>)
      * [`RegisterNeuron.netuid`](<#bittensor.extras.dev_framework.utils.RegisterNeuron.netuid>)
      * [`RegisterNeuron.wallet`](<#bittensor.extras.dev_framework.utils.RegisterNeuron.wallet>)
    * [`RegisterSubnet`](<#bittensor.extras.dev_framework.utils.RegisterSubnet>)
      * [`RegisterSubnet.wallet`](<#bittensor.extras.dev_framework.utils.RegisterSubnet.wallet>)
    * [`STEPS`](<#bittensor.extras.dev_framework.utils.STEPS>)
    * [`is_instance_namedtuple()`](<#bittensor.extras.dev_framework.utils.is_instance_namedtuple>)
    * [`split_command()`](<#bittensor.extras.dev_framework.utils.split_command>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.