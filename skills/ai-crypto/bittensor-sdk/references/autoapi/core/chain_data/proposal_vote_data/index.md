# bittensor.core.chain_data.proposal_vote_data &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/proposal_vote_data/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/proposal_vote_data/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/proposal_vote_data/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.proposal_vote_data

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`ProposalVoteData`](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData>)
      * [`ProposalVoteData.ayes`](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData.ayes>)
      * [`ProposalVoteData.end`](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData.end>)
      * [`ProposalVoteData.from_dict()`](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData.from_dict>)
      * [`ProposalVoteData.index`](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData.index>)
      * [`ProposalVoteData.nays`](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData.nays>)
      * [`ProposalVoteData.threshold`](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData.threshold>)



# bittensor.core.chain_data.proposal_vote_data[#](<#module-bittensor.core.chain_data.proposal_vote_data> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`ProposalVoteData`](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData> "bittensor.core.chain_data.proposal_vote_data.ProposalVoteData") | Senate / Proposal data  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.proposal_vote_data.ProposalVoteData[#](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData> "Link to this definition")
    

Bases: [`bittensor.core.chain_data.info_base.InfoBase`](<../info_base/index.html#bittensor.core.chain_data.info_base.InfoBase> "bittensor.core.chain_data.info_base.InfoBase")

Senate / Proposal data

ayes: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData.ayes> "Link to this definition")
    

end: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData.end> "Link to this definition")
    

classmethod from_dict(_proposal_dict_)[#](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData.from_dict> "Link to this definition")
    

Parameters:
    

**proposal_dict** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)"))

Return type:
    

[ProposalVoteData](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData> "bittensor.core.chain_data.proposal_vote_data.ProposalVoteData")

index: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData.index> "Link to this definition")
    

nays: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")][#](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData.nays> "Link to this definition")
    

threshold: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData.threshold> "Link to this definition")
    

[ __ previous bittensor.core.chain_data.prometheus_info ](<../prometheus_info/index.html> "previous page") [ next bittensor.core.chain_data.proxy __](<../proxy/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`ProposalVoteData`](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData>)
      * [`ProposalVoteData.ayes`](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData.ayes>)
      * [`ProposalVoteData.end`](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData.end>)
      * [`ProposalVoteData.from_dict()`](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData.from_dict>)
      * [`ProposalVoteData.index`](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData.index>)
      * [`ProposalVoteData.nays`](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData.nays>)
      * [`ProposalVoteData.threshold`](<#bittensor.core.chain_data.proposal_vote_data.ProposalVoteData.threshold>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.