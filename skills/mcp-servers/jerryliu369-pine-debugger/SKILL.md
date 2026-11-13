<!--
  Imported from: https://github.com/TradersPost/pinescript-agents
  Source Path: skills/pine-debugger/SKILL.md
  Curated for awesome-quant-skills
-->

---
name: pine-debugger
description: Troubleshoots Pine Script issues and adds debugging capabilities. Use when scripts have errors or unexpected behavior.
allowed-tools: Read, Edit, Grep, Glob
---

# Pine Script Debugger

Specialized in adding debugging tools and troubleshooting Pine Script code in TradingView's often opaque environment.

## ⚠️ Pine Script v6 2025 Common Pitfalls

### CRITICAL: March 2025 Breaking Change - For Loop Boundaries

`for` loops now re-evaluate boundaries **every iteration**.

**PREFERRED FIX: Use `for...in` loops:**
```pinescript
// ✅ BEST: Use for...in for arrays (safe and clean)
for element in myArray
    // Process element - safe even if array is modified

// ✅ BEST: Use for...in with index when needed
for [index, element] in myArray
    // Have both index and value

// ✅ for...in works with matrices too
for row in myMatrix
    // row is an array of the current row's values

// ✅ for...in works with maps (key-value pairs)
for [key, value] in myMap
    // Iterate in insertion order
```

**FALLBACK: Cache boundary if traditional `for` is required:**
```pinescript
// ❌ BUG: Infinite loop or unexpected behavior
var arr = array.new<int>()
for i = 0 to array.size(arr)  // Re-evaluated each iteration!
    array.push(arr, i)        // Array grows, loop never ends

// ✅ FALLBACK: Cache the boundary before the loop
arrSize = array.size(arr)
for i = 0 to arrSize
    array.push(arr, i)
```

**Debug check:** If a loop seems to hang, either switch to `for...in` or verify boundaries are cached.

### Line Continuation Errors

The most common syntax error. Updated rules as of December 2025:

```pinescript
// ❌ ERROR: "end of line without line continuation"
text = condition ?
    "value1" :
    "value2"

// ✅ FIX: Keep ternary on one line
text = condition ? "value1" : "value2"

// ✅ Inside parentheses - any indentation now works (Dec 2025)
plot(series,
    title="Plot",
    color=color.blue)

// ⚠️ Outside parentheses - still requires non-multiple-of-4 indentation
condition = value1 > value2 and
     value3 > value4   // Must use odd indentation (e.g., 5 spaces)
```

### Bid/Ask Variables Return NA

```pinescript
// ❌ UNEXPECTED: Always na on most charts
bidValue = bid  // Only works on 1T (tick) timeframe!

// ✅ DEBUG: Check timeframe
if barstate.islast
    label.new(bar_index, high,
        "Bid: " + (na(bid) ? "N/A (not 1T)" : str.tostring(bid)))
```

### Plot in Local Scope

```pinescript
// ❌ ERROR: "Cannot use 'plot' in local scope"
if condition
    plot(value)

for i = 0 to 10
    plot(close[i])

// ✅ FIX: Use conditional plotting at global scope
plot(condition ? value : na)
```

## Core Debugging Toolkit

### 1. Label-Based Value Inspector

```pinescript
// Debug label showing multiple values
if barstate.islast
    debugText = "RSI: " + str.tostring(rsiValue, "#.##") + "\n"
    debugText += "MA: " + str.tostring(maValue, "#.##") + "\n"
    debugText += "Signal: " + (buySignal ? "BUY" : "NEUTRAL")
    label.new(bar_index, high * 1.05, debugText,
        style=label.style_label_down,
        color=color.yellow,
        textcolor=color.black)
```

### 2. Table-Based Variable Monitor

```pinescript
// Real-time variable monitor table
var table debugTable = table.new(position.top_right, 2, 10,
    bgcolor=color.new(color.black, 80), border_width=1)

if barstate.islast
    table.cell(debugTable, 0, 0, "Variable",
        bgcolor=color.gray, text_color=color.white)
    table.cell(debugTable, 1, 0, "Value",
        bgcolor=color.gray, text_color=color.white)

    table.cell(debugTable, 0, 1, "Bar Index", text_color=color.white)
    table.cell(debugTable, 1, 1, str.tostring(bar_index), text_color=color.yellow)

    table.cell(debugTable, 0, 2, "Close", text_color=color.white)
    table.cell(debugTable, 1, 2, str.tostring(close, "#.####"), text_color=color.yellow)

    table.cell(debugTable, 0, 3, "Signal Active", text_color=color.white)
    sigColor = signalActive ? color.green : color.red
    table.cell(debugTable, 1, 3, signalActive ? "YES" : "NO", text_color=sigColor)
```

### 3. Loop Iteration Debugger

```pinescript
// Debug loop iteration (use for...in for safety)
var array<float> values = array.new<float>()
var int loopIterations = 0

loopIterations := 0

// ✅ PREFERRED: Use for...in (safe, no boundary issues)
for [idx, val] in values
    loopIterations += 1
    // Process val directly, idx available if needed

// Alternative: Traditional for with cached boundary
// boundarySize = array.size(values)
// for i = 0 to boundarySize - 1
//     loopIterations += 1

if barstate.islast
    label.new(bar_index, high,
        "Loop ran " + str.tostring(loopIterations) + " times\n" +
        "Array size: " + str.tostring(array.size(values)))
```

### 4. Repainting Detector

```pinescript
// Detect potential repainting
var bool repaintDetected = false
var float previousValue = na

if not barstate.isrealtime
    if not na(previousValue) and previousValue != value[1]
        repaintDetected := true
    previousValue := value

if barstate.islast and repaintDetected
    label.new(bar_index, high * 1.1, "⚠️ REPAINTING DETECTED",
        style=label.style_label_down,
        color=color.red,
        textcolor=color.white)
```

### 5. NA Value Tracker

```pinescript
// Debug na propagation
debugNa() =>
    result = "NA Debug:\n"
    result += "value1: " + (na(value1) ? "NA ❌" : "OK ✓") + "\n"
    result += "value2: " + (na(value2) ? "NA ❌" : "OK ✓") + "\n"
    result += "result: " + (na(result) ? "NA ❌" : "OK ✓")
    result

if barstate.islast
    label.new(bar_index, low, debugNa(),
        style=label.style_label_up,
        color=color.orange)
```

### 6. Security Function Debugger

```pinescript
// Debug request.security() calls
[htfClose, htfTime] = request.security(syminfo.tickerid, "D",
    [close, time],
    lookahead=barmerge.lookahead_off)

if barstate.islast
    secDebug = "HTF Debug:\n"
    secDebug += "Close: " + str.tostring(htfClose, "#.##") + "\n"
    secDebug += "Time: " + str.format_time(htfTime, "yyyy-MM-dd") + "\n"
    secDebug += "Current TF: " + timeframe.period
    label.new(bar_index, high, secDebug)
```

### 7. Input Active State Debugger (July 2025)

```pinescript
// Debug conditional inputs
showAdvanced = input.bool(false, "Show Advanced")
advValue = input.int(10, "Advanced Value",
    active=showAdvanced,  // July 2025 feature
    tooltip="This input is conditional")

if barstate.islast
    label.new(bar_index, high,
        "showAdvanced: " + str.tostring(showAdvanced) + "\n" +
        "advValue: " + str.tostring(advValue) + "\n" +
        "(advValue active: " + str.tostring(showAdvanced) + ")")
```

## UDT Debugging Techniques

### 1. UDT State Inspector

```pinescript
// Debug UDT field values with a method
type Regression
    int startTime
    int endTime
    int startBarIndex
    int endBarIndex
    float slope
    float intercept
    line centerLine = na

// Add debug method to UDT
method debug(Regression this, int yPos) =>
    if barstate.islast and not na(this.startTime)
        debugText = "Regression Debug:\n"
        debugText += "startTime: " + str.format_time(this.startTime, "MM-dd HH:mm") + "\n"
        debugText += "endTime: " + str.format_time(this.endTime, "MM-dd HH:mm") + "\n"
        debugText += "startBar: " + str.tostring(this.startBarIndex) + "\n"
        debugText += "endBar: " + str.tostring(this.endBarIndex) + "\n"
        debugText += "slope: " + str.tostring(this.slope, "#.######") + "\n"
        debugText += "intercept: " + str.tostring(this.intercept, "#.##") + "\n"
        debugText += "hasLine: " + (na(this.centerLine) ? "NO ❌" : "YES ✓")
        label.new(bar_index, yPos, debugText,
            style=label.style_label_left,
            color=color.blue,
            textcolor=color.white)

// Use it
if debugMode
    myRegression.debug(high)
```

### 2. UDT Array Inspector Table

```pinescript
// Debug all items in a UDT array
var table udtTable = table.new(position.bottom_left, 6, 12,
    bgcolor=color.new(color.black, 80))

if debugMode and barstate.islast
    // Header row
    table.cell(udtTable, 0, 0, "#", text_color=color.gray)
    table.cell(udtTable, 1, 0, "StartTime", text_color=color.gray)
    table.cell(udtTable, 2, 0, "EndTime", text_color=color.gray)
    table.cell(udtTable, 3, 0, "Slope", text_color=color.gray)
    table.cell(udtTable, 4, 0, "HasLine", text_color=color.gray)

    // Use for...in to iterate UDT array
    row = 1
    for [idx, reg] in regressions
        if row < 11  // Limit rows
            table.cell(udtTable, 0, row, str.tostring(idx), text_color=color.white)
            table.cell(udtTable, 1, row, str.format_time(reg.startTime, "MM-dd"), text_color=color.yellow)
            table.cell(udtTable, 2, row, str.format_time(reg.endTime, "MM-dd"), text_color=color.yellow)
            slopeColor = reg.slope >= 0 ? color.green : color.red
            table.cell(udtTable, 3, row, str.tostring(reg.slope, "#.####"), text_color=slopeColor)
            lineStatus = na(reg.centerLine) ? "❌" : "✓"
            table.cell(udtTable, 4, row, lineStatus, text_color=color.white)
            row += 1
```

### 3. Time vs Bar_Index Comparison Debugger

```pinescript
// Debug time-based coordinates vs bar_index
if debugMode and barstate.islast
    currentTimeFormatted = str.format_time(time, "yyyy-MM-dd HH:mm")
    barsAgo = bar_index - startBarIndex

    debugText = "Coordinate Debug:\n"
    debugText += "Current bar_index: " + str.tostring(bar_index) + "\n"
    debugText += "Current time: " + currentTimeFormatted + "\n"
    debugText += "─────────────────\n"
    debugText += "Start bar_index: " + str.tostring(startBarIndex) + "\n"
    debugText += "Start time: " + str.format_time(startTime, "yyyy-MM-dd HH:mm") + "\n"
    debugText += "Bars ago: " + str.tostring(barsAgo) + "\n"
    debugText += "─────────────────\n"

    // Check if bar_index would hit 5000 limit
    if barsAgo > 5000
        debugText += "⚠️ WOULD EXCEED 5000 BAR LIMIT!\n"
        debugText += "Use xloc.bar_time instead\n"
    else
        debugText += "✓ Within bar_index limit\n"

    label.new(bar_index, high * 1.02, debugText,
        style=label.style_label_down,
        color=barsAgo > 5000 ? color.red : color.green)
```

### 4. Drawing Object Status Debugger

```pinescript
// Debug whether UDT drawing objects exist
method debugDrawings(Regression this) =>
    status = "Drawing Status:\n"
    status += "centerLine: " + (na(this.centerLine) ? "NULL ❌" : "EXISTS ✓") + "\n"
    status += "upperLine: " + (na(this.upperLine) ? "NULL ❌" : "EXISTS ✓") + "\n"
    status += "lowerLine: " + (na(this.lowerLine) ? "NULL ❌" : "EXISTS ✓") + "\n"
    status += "fill: " + (na(this.fill) ? "NULL ❌" : "EXISTS ✓")
    status

if debugMode and barstate.islast
    for [i, reg] in regressions
        if i == 0  // Just debug first one
            label.new(bar_index, low, reg.debugDrawings(),
                style=label.style_label_up,
                color=color.purple)
```

### 5. UDT Creation Flow Debugger

```pinescript
// Track when UDTs are created
var int udtCreationCount = 0
var array<string> creationLog = array.new<string>()

// When creating new UDT
if shouldCreateNew
    udtCreationCount += 1
    logEntry = "Created #" + str.tostring(udtCreationCount) + " at bar " + str.tostring(bar_index)
    array.push(creationLog, logEntry)

    newReg = Regression.new(
        startTime = time,
        startBarIndex = bar_index,
        // ...
    )
    array.push(regressions, newReg)

// Display creation log
if debugMode and barstate.islast
    logText = "UDT Creation Log:\n"
    logText += "Total created: " + str.tostring(udtCreationCount) + "\n"
    logText += "─────────────────\n"

    // Show last 5 entries using for...in
    startIdx = math.max(0, array.size(creationLog) - 5)
    for [i, entry] in creationLog
        if i >= startIdx
            logText += entry + "\n"

    label.new(bar_index - 10, high, logText,
        style=label.style_label_right,
        color=color.teal)
```

### 6. xloc.bar_time vs xloc.bar_index Validator

```pinescript
// Verify time coordinates work correctly
if debugMode
    // Draw test lines with both methods
    if barstate.islast
        testStartBar = bar_index - 100
        testStartTime = time[100]

        // bar_index method (may fail if >5000 bars back)
        testLine1 = line.new(testStartBar, close[100], bar_index, close,
            xloc=xloc.bar_index,
            color=color.red,
            width=2)

        // bar_time method (unlimited lookback)
        testLine2 = line.new(testStartTime, close[100] * 0.99, time, close * 0.99,
            xloc=xloc.bar_time,
            color=color.green,
            width=2)

        label.new(bar_index, low * 0.98,
            "Red: xloc.bar_index\nGreen: xloc.bar_time\n(Should overlap if working)",
            style=label.style_label_up,
            color=color.yellow)
```

## Common Issues and Solutions

### 1. Infinite Loop (March 2025)

**Symptom:** Script hangs or times out

```pinescript
// ❌ CAUSE: Dynamic boundary grows during loop
for i = 0 to array.size(arr)
    array.push(arr, i)

// ✅ FIX: Cache boundary
size = array.size(arr)
for i = 0 to size
    array.push(arr, i)
```

### 2. Unexpected NA Values

**Symptom:** Calculations return na unexpectedly

```pinescript
// Debug NA chain
if na(finalResult)
    // Check each component
    if na(input1)
        label.new(bar_index, high, "input1 is NA")
    else if na(intermediate)
        label.new(bar_index, high, "intermediate is NA")
    else
        label.new(bar_index, high, "Unknown NA source")
```

### 3. Security Function Issues

**Symptom:** Wrong values from higher timeframe

```pinescript
// ✅ Correct security() usage
htfValue = request.security(syminfo.tickerid, "D", close,
    gaps=barmerge.gaps_off,
    lookahead=barmerge.lookahead_off)  // Prevent future leak
```

### 4. Historical vs Real-time Mismatch

**Symptom:** Strategy works in backtest, fails live

```pinescript
// Debug historical vs realtime
if barstate.islast
    label.new(bar_index, high,
        "ishistorical: " + str.tostring(barstate.ishistory) + "\n" +
        "isrealtime: " + str.tostring(barstate.isrealtime) + "\n" +
        "isconfirmed: " + str.tostring(barstate.isconfirmed))
```

### 5. String Too Long (Pre-August 2025)

**Symptom:** String truncation errors

```pinescript
// August 2025: Limit increased to 40,960 characters
// If still hitting limits, chunk the string
longString = ""
for i = 0 to 100
    if str.length(longString) < 40000  // Leave buffer
        longString += "data" + str.tostring(i) + "\n"
```

## Debug Mode Implementation

```pinescript
// Master debug toggle
debugMode = input.bool(false, "🔧 Debug Mode", group="Debug")

// Conditional debug elements
var table debugTable = na
if debugMode
    debugTable := table.new(position.top_right, 2, 5,
        bgcolor=color.new(color.black, 80))

if debugMode and barstate.islast
    table.cell(debugTable, 0, 0, "Debug Info", text_color=color.white)
    // ... add debug info

// Debug plots (only when debug mode on)
plot(debugMode ? debugValue : na, "Debug Value", color.yellow)
```

## Debugging Workflow

1. **Identify Symptom**
   - Compilation error?
   - Runtime error?
   - Wrong values?
   - Performance issue?

2. **Check 2025 Breaking Changes**
   - For loop boundaries (March 2025)
   - Line continuation rules
   - Bid/ask availability

3. **Add Debug Points**
   - Labels at key calculations
   - Table for variable monitoring
   - Plot intermediate values

4. **Trace Execution**
   - Follow calculation flow
   - Check condition evaluations
   - Monitor state changes

5. **Test Edge Cases**
   - First bars (bar_index == 0)
   - NA values
   - Real-time vs historical
   - Different timeframes

6. **Clean Up**
   - Wrap debug code in `if debugMode`
   - Or remove before publishing

## Quick Reference: Error Messages

| Error | Likely Cause | Fix |
|-------|--------------|-----|
| "end of line without line continuation" | Split ternary or wrong indentation | Keep ternary on one line, use 5-space indent |
| "Cannot use 'plot' in local scope" | plot() inside if/for/function | Use `plot(condition ? value : na)` |
| "Loop too long" | Dynamic boundary in for loop | Cache boundary or use `for...in` |
| "String is too long" | String > 40,960 chars | Chunk string or reduce content |
| "na" everywhere | NA propagation | Add NA checks at each step |
| Drawing doesn't appear | bar_index > 5000 bars back | Use `xloc.bar_time` instead |
| UDT line is na | Forgot to assign after line.new() | Use `:=` to assign drawing to UDT field |

## UDT-Specific Debugging Checklist

- [ ] Are time values being captured when events occur (not later)?
- [ ] Are both `time` AND `bar_index` stored (for drawing + calculation)?
- [ ] Are drawing objects using `xloc.bar_time`?
- [ ] Is `delete()` being called before `draw()`?
- [ ] Are UDT methods using `this.field :=` for assignments?
- [ ] Is the UDT array being iterated with `for...in`?

TradingView's environment is opaque. Always test thoroughly and provide multiple debugging approaches.
