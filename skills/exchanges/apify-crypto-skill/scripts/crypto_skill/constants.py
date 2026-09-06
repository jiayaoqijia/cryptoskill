APIFY_BASE_URL = "https://api.apify.com/v2"
KUCOIN_ACTOR_ID = "moving_beacon-owner1~my-actor-14"
COINGECKO_ACTOR_ID = "benthepythondev~crypto-intelligence"
DEFAULT_TIMEOUT = 300  # seconds, matches Apify sync endpoint limit
DEFAULT_DATA_LIMIT = 100
DEFAULT_VS_CURRENCY = "usd"
DEFAULT_SORT_ORDER = "market_cap_desc"
REALTIME_TIMEFRAME = "1m"
REALTIME_DATA_LIMIT = 1
DEFAULT_HISTORICAL_DAYS = 30

# HTTP status codes for Apify API error mapping
AUTH_ERROR_CODES = frozenset({401, 403})
TIMEOUT_ERROR_CODE = 408
RATE_LIMIT_ERROR_CODE = 429

# CoinGecko scrape modes
SCRAPE_MODE_SIMPLE_PRICES = "simple_prices"
SCRAPE_MODE_MARKET_DATA = "market_data"
SCRAPE_MODE_COIN_DETAIL = "coin_detail"
SCRAPE_MODE_HISTORICAL = "historical_data"
SCRAPE_MODE_TRENDING = "trending"
SCRAPE_MODE_CATEGORIES = "categories"
