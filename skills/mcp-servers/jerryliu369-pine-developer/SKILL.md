<!--
  Imported from: https://github.com/TradersPost/pinescript-agents
  Source Path: skills/pine-developer/SKILL.md
  Curated for awesome-quant-skills
-->

---
name: pine-developer
description: Writes production-quality Pine Script v6 code following TradingView guidelines. Use when implementing indicators, strategies, or any Pine Script code.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Pine Script Developer

Specialized in writing production-quality Pine Script v6 code for TradingView.

## ⚠️ CRITICAL: Pine Script v6 2025 Updates

**These updates are essential for writing correct, modern Pine Script code:**

### December 2025: Updated Line Wrapping Rules
Expressions in parentheses now support flexible indentation:
```pinescript
// ✅ NOW VALID - Any indentation inside parentheses
plot(series,
    title="My Plot",    // Can use any indentation
    color=color.blue)

// ✅ Also valid
longCondition = (ta.crossover(ema50, ema200) and
    rsi < 30 and
    volume > ta.sma(volume, 20))

// ⚠️ STILL REQUIRED outside parentheses - non-multiple-of-4 indentation
longCondition = ta.crossover(ema50, ema200) and
     rsi < 30   // Must NOT be multiple of 4 spaces
```

### March 2025: BREAKING CHANGE - For Loop Dynamic Boundaries
`for` loops now evaluate `to_num` **before every iteration**, not just once.

**PREFERRED: Use `for...in` loops for collections:**
```pinescript
// ✅ BEST: Use for...in for arrays (safe, clean, preferred)
for element in myArray
    // Process element directly

// ✅ BEST: Use for...in with index when needed
for [index, element] in myArray
    // Have both index and value

// ✅ for...in works with arrays, matrices, and maps
for [key, value] in myMap
    // Iterate key-value pairs
```

**If you must use traditional `for` loop:**
```pinescript
// ⚠️ BREAKING: This creates infinite loop!
var arr = array.new<int>()
for i = 0 to array.size(arr)  // Re-evaluated each iteration
    array.push(arr, i)  // Array grows, loop never ends!

// ✅ FALLBACK: Cache the boundary if using traditional for
size = array.size(arr)
for i = 0 to size
    array.push(arr, i)
```

**Note:** `for...in` allows modifying array/matrix sizes during iteration. Maps cannot be resized during `for...in` - use `map.keys()` array instead.

### February 2025: Scope Limit Removed
- Previously limited to 550 total scopes
- Now **unlimited** scopes across functions, methods, loops, conditionals, types, and enums

### February 2025: Bid/Ask Variables
```pinescript
// Only available on 1T (tick) timeframe
bidPrice = bid  // Highest buyer price (na on other timeframes)
askPrice = ask  // Lowest seller price (na on other timeframes)
```

## Pine Script v6 2025 New Features

### July 2025: Input `active` Parameter
All input functions now support conditional activation:
```pinescript
useCustomMA = input.bool(false, "Use Custom MA")
customMALength = input.int(20, "Custom MA Length",
    active=useCustomMA,  // Grayed out when useCustomMA is false
    tooltip="Only available when 'Use Custom MA' is enabled")
```

### July 2025: `syminfo.current_contract`
```pinescript
// For continuous futures - returns underlying contract ticker
currentContract = syminfo.current_contract  // Returns na for non-continuous
```

### November 2025: `syminfo.isin`
```pinescript
// International Securities Identification Number (12 chars)
isinCode = syminfo.isin  // Empty string if unavailable
```

### September 2025: Plot Line Styles
```pinescript
plot(series, linestyle=plot.linestyle_solid)   // Default
plot(series, linestyle=plot.linestyle_dashed)  // Dashed line
plot(series, linestyle=plot.linestyle_dotted)  // Dotted line
```

### October 2025: Enhanced `time()` and `time_close()`
New `timeframe_bars_back` parameter:
```pinescript
// Get time from 5 bars back on the DAILY timeframe (not current chart)
dailyTimeBack = time("D", timeframe_bars_back=5)

// Positive = past bars, Negative = future (expected) timestamps
futureTime = time("D", timeframe_bars_back=-1)  // Expected next bar
```

### August 2025: Increased String Length
- Maximum string length: **40,960 characters** (was 4,096)

### June 2025: Library Constant Exports
```pinescript
// In library:
//@version=6
library("MyLib")
export const float PI = 3.14159265359
export const int MAX_BARS = 500
export const string VERSION = "1.0.0"
```

### May 2025: `time_close` on Non-Time-Based Charts
For Renko, Line Break, Kagi, Point & Figure, Range charts:
- `time_close` of open realtime bar now returns `na`
- `time_close[1]` now works immediately after bar closes

### April 2025: Percentage-Based Ticker Styles
```pinescript
// New "PercentageLTP" style for percentage box sizing
renkoTicker = ticker.renko(syminfo.tickerid, "PercentageLTP", 1.0)
kagiTicker = ticker.kagi(syminfo.tickerid, "PercentageLTP", 0.5)
pnfTicker = ticker.pointfigure(syminfo.tickerid, "PercentageLTP", 1.0)
```

### March 2025: `box.set_xloc()`
```pinescript
// Modify box x-coordinates after creation
box.set_xloc(myBox, left, right, xloc.bar_index)
box.set_xloc(myBox, leftTime, rightTime, xloc.bar_time)
```

## CRITICAL: Line Wrapping Rules (Updated December 2025)

### Inside Parentheses (FLEXIBLE)
```pinescript
// ✅ Any indentation works inside ()
plot(series,
    title="Plot",
        color=color.blue,  // Different indentation OK
    linewidth=2)

indicator("Title",
    overlay=true,
    max_bars_back=500)
```

### Outside Parentheses (STRICT)
```pinescript
// ✅ CORRECT - Non-multiple-of-4 indentation
longCondition = ta.crossover(ema50, ema200) and
     rsi < 30 and
     volume > ta.sma(volume, 20)

// ❌ WRONG - Multiple of 4 (or same level)
longCondition = ta.crossover(ema50, ema200) and
    rsi < 30  // Error: 4 spaces

longCondition = ta.crossover(ema50, ema200) and
rsi < 30  // Error: same indentation
```

### CRITICAL: Ternary Operators - Keep on ONE Line
```pinescript
// ❌ NEVER split ternary across lines
text = condition ?
    "value1" :
    "value2"  // ERROR!

// ✅ ALWAYS keep on one line
text = condition ? "value1" : "value2"

// ✅ For long ternaries, use intermediate variables
trueText = str.format("Long value {0}", param1)
falseText = str.format("Other value {0}", param2)
result = condition ? trueText : falseText
```

## CRITICAL: Plot Scope Restriction

**NEVER use plot() inside local scopes:**
```pinescript
// ❌ WRONG - All of these fail:
if condition
    plot(value)  // ERROR: Cannot use 'plot' in local scope

for i = 0 to 10
    plot(close[i])  // ERROR!

myFunc() =>
    plot(close)  // ERROR!

// ✅ CORRECT patterns:
plot(condition ? value : na)  // Conditional plotting
plot(value, color=condition ? color.blue : na)  // Conditional color

// For dynamic drawing in local scopes, use:
if condition
    line.new(...)   // OK
    label.new(...)  // OK
    box.new(...)    // OK
```

## ⚠️ CRITICAL: UDT-First Architecture

**For any complex data structure, ALWAYS define User Defined Types (UDTs) FIRST before writing any other code.**

### Why UDT-First?
1. **Encapsulation**: Bundle related data and drawing objects together
2. **Methods**: Add behavior directly to types with `method` syntax
3. **Unlimited Lookback**: Use `xloc.bar_time` instead of `xloc.bar_index` (5000 bar limit!)
4. **Clean Arrays**: One `array<MyType>` instead of 6+ parallel arrays
5. **Self-Managing Drawings**: Types can create/delete their own visual objects

### UDT Definition Pattern
```pinescript
// ALWAYS define UDTs early in script (after inputs, before calculations)
type Regression
    // Time coordinates (for xloc.bar_time - NO lookback limit!)
    int startTime
    int endTime

    // Bar indices (for Y calculations: y = slope * barIndex + intercept)
    int startBarIndex
    int endBarIndex

    // Data parameters
    float slope
    float intercept
    float stdDev
    float pearsonR

    // State flags
    bool isLive = false
    bool isOriginal = false

    // Drawing objects (managed internally)
    line centerLine = na
    line upperLine = na
    line lowerLine = na
    linefill fill = na
```

### UDT Methods Pattern
```pinescript
// Delete method - clean up drawing objects
method delete(Regression this) =>
    if not na(this.centerLine)
        line.delete(this.centerLine)
    if not na(this.upperLine)
        line.delete(this.upperLine)
    if not na(this.lowerLine)
        line.delete(this.lowerLine)
    if not na(this.fill)
        linefill.delete(this.fill)
    this.centerLine := na
    this.upperLine := na
    this.lowerLine := na
    this.fill := na

// Calculation method
method calculateY(Regression this, int barIdx) =>
    this.slope * barIdx + this.intercept

// Draw method - use xloc.bar_time for unlimited lookback!
method draw(Regression this, color baseColor, int width) =>
    this.delete()  // Clean up old drawings first
    startY = this.calculateY(this.startBarIndex)
    endY = this.calculateY(this.endBarIndex)

    // ✅ CRITICAL: Use xloc.bar_time - NO 5000 bar limit!
    this.centerLine := line.new(
         this.startTime, startY,
         this.endTime, endY,
         xloc=xloc.bar_time,  // ← UNLIMITED LOOKBACK
         color=baseColor,
         width=width)
```

### ⚠️ CRITICAL: xloc.bar_time vs xloc.bar_index

**ALWAYS use `xloc.bar_time` for drawing objects that may need historical display:**

```pinescript
// ❌ WRONG - Limited to 5000 bars back
line.new(bar_index - 100, y1, bar_index, y2, xloc=xloc.bar_index)

// ✅ CORRECT - Unlimited historical lookback
line.new(time[100], y1, time, y2, xloc=xloc.bar_time)

// Store TIME when events occur, not just bar_index
var int eventTime = na
var int eventBarIndex = na
if eventOccurred
    eventTime := time           // For drawing
    eventBarIndex := bar_index  // For Y calculation
```

### UDT Storage Pattern
```pinescript
// Single array of UDTs instead of parallel arrays
var array<Regression> regressions = array.new<Regression>()
var Regression liveRegression = na
var Regression originalRegression = na

// ❌ WRONG - Parallel arrays (hard to maintain)
var array<float> slopes = array.new<float>()
var array<float> intercepts = array.new<float>()
var array<int> startBars = array.new<int>()
var array<int> endBars = array.new<int>()
// ... 6+ arrays to keep in sync!

// ✅ CORRECT - Single UDT array
var array<Regression> regressions = array.new<Regression>()
```

### Creating and Storing UDTs
```pinescript
// Create new instance with all data
newRegression = Regression.new(
    startTime = capturedStartTime,
    endTime = capturedEndTime,
    startBarIndex = capturedStartBar,
    endBarIndex = capturedEndBar,
    slope = calculatedSlope,
    intercept = calculatedIntercept,
    stdDev = calculatedStdDev,
    pearsonR = calculatedR
)

// Add to collection
array.push(regressions, newRegression)
```

### Iterating UDT Arrays with for...in
```pinescript
// ✅ BEST: Use for...in for UDT arrays
for reg in regressions
    baseColor = reg.slope >= 0 ? uptrendColor : downtrendColor
    reg.draw(baseColor, lineWidth)

// ✅ With index when needed
for [i, reg] in regressions
    if i == array.size(regressions) - 1
        // Special handling for last item
```

### Time Capture Pattern
```pinescript
// Capture BOTH time and bar_index when events occur
var int startTime = na
var int startBarIndex = na
var int endTime = na
var int endBarIndex = na

if eventStart
    startTime := time        // For xloc.bar_time drawing
    startBarIndex := bar_index  // For Y calculations

if eventEnd
    endTime := time
    endBarIndex := bar_index

    // Create UDT with both coordinate systems
    newItem = MyType.new(
        startTime = startTime,
        endTime = endTime,
        startBarIndex = startBarIndex,
        endBarIndex = endBarIndex
    )
```

### UDT Architecture Checklist
- [ ] Define UDT type BEFORE any calculations
- [ ] Store `time` values for drawing coordinates
- [ ] Store `bar_index` values for Y calculations
- [ ] Include drawing objects (`line`, `box`, `label`) as UDT fields
- [ ] Add `delete()` method to clean up drawings
- [ ] Add `draw()` method using `xloc.bar_time`
- [ ] Use single `array<MyType>` instead of parallel arrays
- [ ] Use `for...in` to iterate UDT arrays

## Documentation Access

Primary documentation references:
- `/docs/pinescript-v6/quick-reference/syntax-basics.md` - Core syntax
- `/docs/pinescript-v6/reference-tables/function-index.md` - Function reference
- `/docs/pinescript-v6/core-concepts/execution-model.md` - Execution model
- `/docs/pinescript-v6/core-concepts/repainting.md` - Repainting issues
- `/docs/pinescript-v6/quick-reference/limitations.md` - Platform limits

## Project File Management

- Save work to `/projects/[project-name].pine`
- Update file header with accurate project information
- Never create unnecessary files

## Script Structure Templates

### Indicator Template
```pinescript
// built with PineScript Agents by TradersPost
//@version=6
indicator(title="", shorttitle="", overlay=true)
```

### Strategy Template (IMPORTANT: Include alert annotation)
```pinescript
// built with PineScript Agents by TradersPost
//@version=6
strategy(title="", shorttitle="", overlay=true)
//@strategy_alert_message {{strategy.order.alert_message}}

// ============================================================================
// INPUTS
// ============================================================================

// Group 1: Main Settings
setting1 = input.int(14, "Setting", group="Main Settings",
    tooltip="Description of what this does")

// Group 2: Visual Settings
showPlots = input.bool(true, "Show Plots", group="Visual Settings")
plotColor = input.color(color.blue, "Plot Color", group="Visual Settings",
    active=showPlots)  // Grayed out when showPlots is false

// ============================================================================
// CALCULATIONS
// ============================================================================

// Cache boundaries for loops (March 2025 breaking change)
arraySize = array.size(myArray)
for i = 0 to arraySize - 1
    // Process...

// ============================================================================
// CONDITIONS
// ============================================================================

// ============================================================================
// PLOTS
// ============================================================================

// Use new linestyle parameter (September 2025)
plot(ma, "MA", color.blue, linewidth=2, linestyle=plot.linestyle_solid)

// ============================================================================
// ALERTS
// ============================================================================
```

## TradingView Constraints (2025 Updated)

### Limits
- Maximum 500 bars historical reference
- Maximum 500 plot/hline/fill outputs
- Maximum 64 drawing objects (label/line/box/table)
- Maximum 40 security() calls
- Maximum 100KB compiled script size
- Tables: max 100 cells
- Arrays: max 100,000 elements
- Strings: max **40,960 characters** (increased August 2025)
- Scopes: **Unlimited** (removed February 2025)

### Platform Quirks
- bar_index starts at 0
- na propagation in calculations
- Historical vs real-time calculation differences
- Strategy calculations on bar close (unless calc_on_every_tick)
- `bid`/`ask` only available on 1T timeframe

## Best Practices

### Avoid Repainting
```pinescript
// Use barstate.isconfirmed for signals
if barstate.isconfirmed and buyCondition
    strategy.entry("Long", strategy.long)

// Proper request.security() usage
htfClose = request.security(syminfo.tickerid, "D", close,
    lookahead=barmerge.lookahead_off)
```

### Performance Optimization
```pinescript
// Cache repeated calculations
sma20 = ta.sma(close, 20)
sma50 = ta.sma(close, 50)
crossUp = ta.crossover(sma20, sma50)

// Combine security() calls
[htfClose, htfHigh, htfLow] = request.security(syminfo.tickerid, "D",
    [close, high, low])
```

### User Experience (Use 2025 Features)
```pinescript
// Input groups with active parameter
advancedMode = input.bool(false, "Advanced Mode", group="Settings")
advSetting = input.int(10, "Advanced Setting",
    group="Settings",
    active=advancedMode,  // July 2025 feature
    tooltip="Only visible in advanced mode")
```

### Error Handling
```pinescript
// Check for na values
safeValue = na(value) ? 0 : value

// Handle division by zero
safeDiv = denominator != 0 ? numerator / denominator : 0

// Cache loop boundaries (March 2025 breaking change)
arrSize = array.size(arr)
for i = 0 to arrSize - 1
    // ...
```

## Code Review Checklist

### Architecture (Check First!)
- [ ] Complex data uses UDT-first pattern
- [ ] Drawing objects use `xloc.bar_time` (not bar_index)
- [ ] Time values captured for historical drawing
- [ ] Single UDT array instead of parallel arrays

### Script Basics
- [ ] `//@version=6` declaration
- [ ] `//@strategy_alert_message {{strategy.order.alert_message}}` for strategies (placed **after** the `strategy()` call)
- [ ] Proper title and overlay setting

### Inputs & UX
- [ ] Inputs have tooltips and groups
- [ ] Inputs use `active` parameter where appropriate
- [ ] Using new plot linestyles where appropriate
- [ ] Proper plot styling

### Code Quality
- [ ] No repainting issues
- [ ] na values handled
- [ ] Loop boundaries cached (March 2025 fix)
- [ ] Efficient calculations
- [ ] Clear variable names
- [ ] Alert conditions if needed

Write code that is production-ready, efficient, and uses UDT-first architecture with the latest Pine Script v6 features.
