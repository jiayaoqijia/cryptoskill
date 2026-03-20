# Gate Exchange Staking Skill

A comprehensive skill for querying and managing staking operations on Gate's earn platform.

## Overview

This skill provides users with complete visibility into their staking activities on Gate, including positions, rewards, available products, and transaction history. It supports multiple staking types including flexible staking, locked staking, DeFi staking, and treasury products.

### Core Capabilities

| Capability | Description | MCP Tools |
|------------|-------------|-----------|
| Query staking positions | View positions, available vs locked amounts, values | `cex_earn_asset_list` |
| Check staking rewards | Daily/cumulative rewards, trends, APY | `cex_earn_award_list` |
| Browse staking products | Discover products, compare APY, filter by coin/lock | `cex_earn_find_coin` |
| View transaction history | Staking/redemption history, filters, order status | `cex_earn_order_list` |

### 1. Query Staking Positions
- View all staking positions across different cryptocurrencies
- Check available vs locked amounts
- Monitor real-time position values
- Track individual product performance

### 2. Check Staking Rewards
- View daily, weekly, and monthly earnings
- Track cumulative rewards by coin
- Analyze reward trends and patterns
- Calculate actual vs advertised APY

### 3. Browse Staking Products
- Discover available staking opportunities
- Compare APY rates across products
- Filter by coin type or lock period
- Check minimum staking requirements

### 4. View Transaction History
- Track all staking and redemption operations
- Filter by date range or operation type
- Monitor order status and completion
- Export transaction records

## Architecture

```
┌─────────────────────┐
│   User Request      │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Intent Detection   │
│  - Position Query   │
│  - Reward Check     │
│  - Product Browse   │
│  - History View     │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│   MCP Tool Call     │
│  - asset_list       │
│  - award_list       │
│  - find_coin        │
│  - order_list       │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Response Format    │
│  - Tables           │
│  - Summaries        │
│  - Calculations     │
└─────────────────────┘
```

## Key Features

### Smart Query Recognition
- Multilingual support (English)
- Natural language processing
- Context-aware responses
- Intelligent parameter extraction

### Comprehensive Data Display
- Real-time position tracking
- Historical reward analysis
- Product comparison tables
- Transaction timelines

### Advanced Calculations
- Total portfolio value
- Weighted average APY
- Daily/monthly earnings
- ROI calculations

### Number Formatting Standards
- **General amounts**: 8 decimal places precision with trailing zeros removed
- **Rate fields** (APY, APR): 2 decimal places precision with trailing zeros retained
- Consistent formatting across all displays for better readability

## Usage Examples

### Basic Queries
```
"Show my staking positions"
"What are my staking rewards?"
"Find BTC staking products"
"Show staking history"
```

### Advanced Queries
```
"Calculate my total staking earnings this month"
"Compare APY rates for USDT staking"
"Show locked vs flexible positions"
"What's my actual vs advertised APY?"
```

### Multilingual Support
```
"Check my staking assets"
"Show yesterday's earnings"
"What coins can I stake?"
"View staking records"
```

## Product Types Supported

| Type | Description | Lock Period | Liquidity |
|------|-------------|-------------|-----------|
| **Flexible** | Instant redemption | None | High |
| **Locked** | Fixed-term staking | 7-90 days | Low |
| **DeFi** | Protocol staking | Variable | Medium |
| **Treasury** | Stable returns | None | High |

## MCP Tools Used

- `cex_earn_asset_list`: Query current staking positions
- `cex_earn_award_list`: Retrieve reward history
- `cex_earn_find_coin`: Discover available products
- `cex_earn_order_list`: View transaction history

## Error Handling

The skill gracefully handles various error scenarios:
- Empty positions: Suggests available products
- No rewards: Explains reward accrual timing
- API failures: Provides retry guidance
- Invalid queries: Offers query suggestions

## Security Considerations

- **Read-only access**: No execution of staking operations
- **Authentication required**: All queries need user authentication
- **Data privacy**: Sensitive information displayed only to account owner
- **Rate limiting**: Respects API rate limits

## Best Practices

1. **Regular Monitoring**: Check positions and rewards daily
2. **Diversification**: Spread stakes across multiple products
3. **APY Comparison**: Always compare rates before staking
4. **Lock Period Awareness**: Understand redemption restrictions
5. **Reward Tracking**: Monitor actual vs expected returns

## Limitations

- Cannot execute staking or redemption operations
- Historical data limited by API constraints
- Real-time prices may have slight delays
- Some DeFi products may have additional restrictions

## Future Enhancements

- Staking operation execution
- Automated reward reinvestment
- Price alerts and notifications
- Portfolio optimization suggestions
- Tax reporting features

## Support

For issues or questions:
- Check Gate API documentation
- Review error messages for guidance
- Contact Gate support for account-specific issues