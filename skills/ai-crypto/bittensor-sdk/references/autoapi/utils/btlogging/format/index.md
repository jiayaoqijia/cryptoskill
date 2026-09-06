# bittensor.utils.btlogging.format &#8212; Bittensor SDK Docs  documentation

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
      * [bittensor.extras](<../../../extras/index.html>) __
        * [bittensor.extras.dev_framework](<../../../extras/dev_framework/index.html>)
        * [bittensor.extras.subtensor_api](<../../../extras/subtensor_api/index.html>)
        * [bittensor.extras.timelock](<../../../extras/timelock/index.html>)
      * [bittensor.utils](<../../index.html>) __
        * [bittensor.utils.axon_utils](<../../axon_utils/index.html>)
        * [bittensor.utils.balance](<../../balance/index.html>)
        * [bittensor.utils.btlogging](<../index.html>)
        * [bittensor.utils.easy_imports](<../../easy_imports/index.html>)
        * [bittensor.utils.formatting](<../../formatting/index.html>)
        * [bittensor.utils.liquidity](<../../liquidity/index.html>)
        * [bittensor.utils.networking](<../../networking/index.html>)
        * [bittensor.utils.registration](<../../registration/index.html>)
        * [bittensor.utils.subnets](<../../subnets/index.html>)
        * [bittensor.utils.version](<../../version/index.html>)
        * [bittensor.utils.weight_utils](<../../weight_utils/index.html>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/utils/btlogging/format/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/utils/btlogging/format/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/utils/btlogging/format/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.utils.btlogging.format

##  Contents 

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`BtFileFormatter`](<#bittensor.utils.btlogging.format.BtFileFormatter>)
      * [`BtFileFormatter.format()`](<#bittensor.utils.btlogging.format.BtFileFormatter.format>)
      * [`BtFileFormatter.formatTime()`](<#bittensor.utils.btlogging.format.BtFileFormatter.formatTime>)
    * [`BtStreamFormatter`](<#bittensor.utils.btlogging.format.BtStreamFormatter>)
      * [`BtStreamFormatter.format()`](<#bittensor.utils.btlogging.format.BtStreamFormatter.format>)
      * [`BtStreamFormatter.formatTime()`](<#bittensor.utils.btlogging.format.BtStreamFormatter.formatTime>)
      * [`BtStreamFormatter.set_trace()`](<#bittensor.utils.btlogging.format.BtStreamFormatter.set_trace>)
      * [`BtStreamFormatter.trace`](<#bittensor.utils.btlogging.format.BtStreamFormatter.trace>)
    * [`DEFAULT_LOG_FORMAT`](<#bittensor.utils.btlogging.format.DEFAULT_LOG_FORMAT>)
    * [`DEFAULT_TRACE_FORMAT`](<#bittensor.utils.btlogging.format.DEFAULT_TRACE_FORMAT>)
    * [`LOG_FORMATS`](<#bittensor.utils.btlogging.format.LOG_FORMATS>)
    * [`LOG_TRACE_FORMATS`](<#bittensor.utils.btlogging.format.LOG_TRACE_FORMATS>)
    * [`SUCCESS_LEVEL_NUM`](<#bittensor.utils.btlogging.format.SUCCESS_LEVEL_NUM>)
    * [`TRACE_LEVEL_NUM`](<#bittensor.utils.btlogging.format.TRACE_LEVEL_NUM>)
    * [`color_map`](<#bittensor.utils.btlogging.format.color_map>)
    * [`emoji_map`](<#bittensor.utils.btlogging.format.emoji_map>)
    * [`log_level_color_prefix`](<#bittensor.utils.btlogging.format.log_level_color_prefix>)



# bittensor.utils.btlogging.format[#](<#module-bittensor.utils.btlogging.format> "Link to this heading")

btlogging.format module

This module defines custom logging formatters for the Bittensor project.

## Attributes[#](<#attributes> "Link to this heading")

[`DEFAULT_LOG_FORMAT`](<#bittensor.utils.btlogging.format.DEFAULT_LOG_FORMAT> "bittensor.utils.btlogging.format.DEFAULT_LOG_FORMAT") |   
---|---  
[`DEFAULT_TRACE_FORMAT`](<#bittensor.utils.btlogging.format.DEFAULT_TRACE_FORMAT> "bittensor.utils.btlogging.format.DEFAULT_TRACE_FORMAT") |   
[`LOG_FORMATS`](<#bittensor.utils.btlogging.format.LOG_FORMATS> "bittensor.utils.btlogging.format.LOG_FORMATS") |   
[`LOG_TRACE_FORMATS`](<#bittensor.utils.btlogging.format.LOG_TRACE_FORMATS> "bittensor.utils.btlogging.format.LOG_TRACE_FORMATS") |   
[`SUCCESS_LEVEL_NUM`](<#bittensor.utils.btlogging.format.SUCCESS_LEVEL_NUM> "bittensor.utils.btlogging.format.SUCCESS_LEVEL_NUM") |   
[`TRACE_LEVEL_NUM`](<#bittensor.utils.btlogging.format.TRACE_LEVEL_NUM> "bittensor.utils.btlogging.format.TRACE_LEVEL_NUM") |   
[`color_map`](<#bittensor.utils.btlogging.format.color_map> "bittensor.utils.btlogging.format.color_map") |   
[`emoji_map`](<#bittensor.utils.btlogging.format.emoji_map> "bittensor.utils.btlogging.format.emoji_map") |   
[`log_level_color_prefix`](<#bittensor.utils.btlogging.format.log_level_color_prefix> "bittensor.utils.btlogging.format.log_level_color_prefix") |   
  
## Classes[#](<#classes> "Link to this heading")

[`BtFileFormatter`](<#bittensor.utils.btlogging.format.BtFileFormatter> "bittensor.utils.btlogging.format.BtFileFormatter") | BtFileFormatter  
---|---  
[`BtStreamFormatter`](<#bittensor.utils.btlogging.format.BtStreamFormatter> "bittensor.utils.btlogging.format.BtStreamFormatter") | A custom logging formatter for the Bittensor project that overrides the time formatting to include milliseconds,  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.utils.btlogging.format.BtFileFormatter(_fmt =None_, _datefmt =None_, _style ='%'_, _validate =True_, _*_ , _defaults =None_)[#](<#bittensor.utils.btlogging.format.BtFileFormatter> "Link to this definition")
    

Bases: [`logging.Formatter`](<https://docs.python.org/3/library/logging.html#logging.Formatter> "\(in Python v3.14\)")

BtFileFormatter

A custom logging formatter for the Bittensor project that overrides the time formatting to include milliseconds and centers the level name.

Initialize the formatter with specified format strings.

Initialize the formatter either with the specified format string, or a default as described above. Allow for specialized date formatting with the optional datefmt argument. If datefmt is omitted, you get an ISO8601-like (or RFC 3339-like) format.

Use a style parameter of ‘%’, ‘{’ or ‘$’ to specify that you want to use one of %-formatting, [`str.format()`](<https://docs.python.org/3/library/stdtypes.html#str.format> "\(in Python v3.14\)") (`{}`) formatting or [`string.Template`](<https://docs.python.org/3/library/string.html#string.Template> "\(in Python v3.14\)") formatting in your format string.

Changed in version 3.2: Added the `style` parameter.

format(_record_)[#](<#bittensor.utils.btlogging.format.BtFileFormatter.format> "Link to this definition")
    

Override format to center the level name.

Parameters:
    

**record** ([_logging.LogRecord_](<https://docs.python.org/3/library/logging.html#logging.LogRecord> "\(in Python v3.14\)")) – The log record.

Returns:
    

The formatted log record.

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

formatTime(_record_ , _datefmt =None_)[#](<#bittensor.utils.btlogging.format.BtFileFormatter.formatTime> "Link to this definition")
    

Override formatTime to add milliseconds.

Parameters:
    

  * **record** ([_logging.LogRecord_](<https://docs.python.org/3/library/logging.html#logging.LogRecord> "\(in Python v3.14\)")) – The log record.

  * **datefmt** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The date format string.



Returns:
    

The formatted time string with milliseconds.

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

class bittensor.utils.btlogging.format.BtStreamFormatter(_* args_, _** kwargs_)[#](<#bittensor.utils.btlogging.format.BtStreamFormatter> "Link to this definition")
    

Bases: [`logging.Formatter`](<https://docs.python.org/3/library/logging.html#logging.Formatter> "\(in Python v3.14\)")

A custom logging formatter for the Bittensor project that overrides the time formatting to include milliseconds, centers the level name, and applies custom log formats, emojis, and colors.

Initialize the formatter with specified format strings.

Initialize the formatter either with the specified format string, or a default as described above. Allow for specialized date formatting with the optional datefmt argument. If datefmt is omitted, you get an ISO8601-like (or RFC 3339-like) format.

Use a style parameter of ‘%’, ‘{’ or ‘$’ to specify that you want to use one of %-formatting, [`str.format()`](<https://docs.python.org/3/library/stdtypes.html#str.format> "\(in Python v3.14\)") (`{}`) formatting or [`string.Template`](<https://docs.python.org/3/library/string.html#string.Template> "\(in Python v3.14\)") formatting in your format string.

Changed in version 3.2: Added the `style` parameter.

format(_record_)[#](<#bittensor.utils.btlogging.format.BtStreamFormatter.format> "Link to this definition")
    

Override format to apply custom formatting including emojis and colors.

This method saves the original format, applies custom formatting based on the log level and trace flag, replaces text with emojis and colors, and then returns the formatted log record.

Parameters:
    

**record** ([_logging.LogRecord_](<https://docs.python.org/3/library/logging.html#logging.LogRecord> "\(in Python v3.14\)")) – The log record.

Returns:
    

The formatted log record.

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

formatTime(_record_ , _datefmt =None_)[#](<#bittensor.utils.btlogging.format.BtStreamFormatter.formatTime> "Link to this definition")
    

Override formatTime to add milliseconds.

Parameters:
    

  * **record** – The log record.

  * **datefmt** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The date format string.



Returns:
    

The formatted time string with milliseconds.

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

set_trace(_state =True_)[#](<#bittensor.utils.btlogging.format.BtStreamFormatter.set_trace> "Link to this definition")
    

Change formatter state.

Parameters:
    

**state** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

trace = False[#](<#bittensor.utils.btlogging.format.BtStreamFormatter.trace> "Link to this definition")
    

bittensor.utils.btlogging.format.DEFAULT_LOG_FORMAT: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.utils.btlogging.format.DEFAULT_LOG_FORMAT> "Link to this definition")
    

bittensor.utils.btlogging.format.DEFAULT_TRACE_FORMAT: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.utils.btlogging.format.DEFAULT_TRACE_FORMAT> "Link to this definition")
    

bittensor.utils.btlogging.format.LOG_FORMATS: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")][#](<#bittensor.utils.btlogging.format.LOG_FORMATS> "Link to this definition")
    

bittensor.utils.btlogging.format.LOG_TRACE_FORMATS: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")][#](<#bittensor.utils.btlogging.format.LOG_TRACE_FORMATS> "Link to this definition")
    

bittensor.utils.btlogging.format.SUCCESS_LEVEL_NUM: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") = 21[#](<#bittensor.utils.btlogging.format.SUCCESS_LEVEL_NUM> "Link to this definition")
    

bittensor.utils.btlogging.format.TRACE_LEVEL_NUM: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") = 5[#](<#bittensor.utils.btlogging.format.TRACE_LEVEL_NUM> "Link to this definition")
    

bittensor.utils.btlogging.format.color_map: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")][#](<#bittensor.utils.btlogging.format.color_map> "Link to this definition")
    

bittensor.utils.btlogging.format.emoji_map: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")][#](<#bittensor.utils.btlogging.format.emoji_map> "Link to this definition")
    

bittensor.utils.btlogging.format.log_level_color_prefix: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")][#](<#bittensor.utils.btlogging.format.log_level_color_prefix> "Link to this definition")
    

[ __ previous bittensor.utils.btlogging.defines ](<../defines/index.html> "previous page") [ next bittensor.utils.btlogging.helpers __](<../helpers/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`BtFileFormatter`](<#bittensor.utils.btlogging.format.BtFileFormatter>)
      * [`BtFileFormatter.format()`](<#bittensor.utils.btlogging.format.BtFileFormatter.format>)
      * [`BtFileFormatter.formatTime()`](<#bittensor.utils.btlogging.format.BtFileFormatter.formatTime>)
    * [`BtStreamFormatter`](<#bittensor.utils.btlogging.format.BtStreamFormatter>)
      * [`BtStreamFormatter.format()`](<#bittensor.utils.btlogging.format.BtStreamFormatter.format>)
      * [`BtStreamFormatter.formatTime()`](<#bittensor.utils.btlogging.format.BtStreamFormatter.formatTime>)
      * [`BtStreamFormatter.set_trace()`](<#bittensor.utils.btlogging.format.BtStreamFormatter.set_trace>)
      * [`BtStreamFormatter.trace`](<#bittensor.utils.btlogging.format.BtStreamFormatter.trace>)
    * [`DEFAULT_LOG_FORMAT`](<#bittensor.utils.btlogging.format.DEFAULT_LOG_FORMAT>)
    * [`DEFAULT_TRACE_FORMAT`](<#bittensor.utils.btlogging.format.DEFAULT_TRACE_FORMAT>)
    * [`LOG_FORMATS`](<#bittensor.utils.btlogging.format.LOG_FORMATS>)
    * [`LOG_TRACE_FORMATS`](<#bittensor.utils.btlogging.format.LOG_TRACE_FORMATS>)
    * [`SUCCESS_LEVEL_NUM`](<#bittensor.utils.btlogging.format.SUCCESS_LEVEL_NUM>)
    * [`TRACE_LEVEL_NUM`](<#bittensor.utils.btlogging.format.TRACE_LEVEL_NUM>)
    * [`color_map`](<#bittensor.utils.btlogging.format.color_map>)
    * [`emoji_map`](<#bittensor.utils.btlogging.format.emoji_map>)
    * [`log_level_color_prefix`](<#bittensor.utils.btlogging.format.log_level_color_prefix>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.   

  *[*]: Keyword-only parameters separator (PEP 3102)