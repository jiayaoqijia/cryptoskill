# bittensor.core.chain_data.weight_commit_info &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/weight_commit_info/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/weight_commit_info/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/weight_commit_info/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.weight_commit_info

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`WeightCommitInfo`](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo>)
      * [`WeightCommitInfo.commit_block`](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo.commit_block>)
      * [`WeightCommitInfo.commit_hex`](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo.commit_hex>)
      * [`WeightCommitInfo.from_vec_u8()`](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo.from_vec_u8>)
      * [`WeightCommitInfo.from_vec_u8_v2()`](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo.from_vec_u8_v2>)
      * [`WeightCommitInfo.reveal_round`](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo.reveal_round>)
      * [`WeightCommitInfo.ss58`](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo.ss58>)



# bittensor.core.chain_data.weight_commit_info[#](<#module-bittensor.core.chain_data.weight_commit_info> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`WeightCommitInfo`](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo> "bittensor.core.chain_data.weight_commit_info.WeightCommitInfo") | Data class representing weight commit information.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.weight_commit_info.WeightCommitInfo[#](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo> "Link to this definition")
    

Data class representing weight commit information.

Variables:
    

  * **ss58** – The SS58 address of the committer

  * **commit_block** – The block number of the commitment.

  * **commit_hex** – The serialized weight commit data as hex string

  * **reveal_round** – The round number for reveal




commit_block: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo.commit_block> "Link to this definition")
    

commit_hex: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo.commit_hex> "Link to this definition")
    

classmethod from_vec_u8(_data_)[#](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo.from_vec_u8> "Link to this definition")
    

Creates a WeightCommitInfo instance

Parameters:
    

**data** ([_tuple_](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")) – Tuple containing ((AccountId,), (commit_data,), round_number)

Returns:
    

A new instance with the decoded data

Return type:
    

[WeightCommitInfo](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo> "bittensor.core.chain_data.weight_commit_info.WeightCommitInfo")

Note

This method is used when querying a block or block hash where storage functions CRV3WeightCommitsV2 does not exist in Subtensor module.

classmethod from_vec_u8_v2(_data_)[#](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo.from_vec_u8_v2> "Link to this definition")
    

# TODO no it does not Creates a WeightCommitInfo instance

Parameters:
    

**data** ([_tuple_](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")) – Tuple containing ((AccountId,), (commit_block, ) (commit_data,), round_number)

Returns:
    

A new instance with the decoded data

Return type:
    

[WeightCommitInfo](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo> "bittensor.core.chain_data.weight_commit_info.WeightCommitInfo")

reveal_round: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo.reveal_round> "Link to this definition")
    

ss58: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo.ss58> "Link to this definition")
    

[ __ previous bittensor.core.chain_data.utils ](<../utils/index.html> "previous page") [ next bittensor.core.config __](<../../config/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`WeightCommitInfo`](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo>)
      * [`WeightCommitInfo.commit_block`](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo.commit_block>)
      * [`WeightCommitInfo.commit_hex`](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo.commit_hex>)
      * [`WeightCommitInfo.from_vec_u8()`](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo.from_vec_u8>)
      * [`WeightCommitInfo.from_vec_u8_v2()`](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo.from_vec_u8_v2>)
      * [`WeightCommitInfo.reveal_round`](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo.reveal_round>)
      * [`WeightCommitInfo.ss58`](<#bittensor.core.chain_data.weight_commit_info.WeightCommitInfo.ss58>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.