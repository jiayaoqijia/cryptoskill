# Binance Futures API 参考

## 基础信息

- **Base URL**: 
  - 生产环境: `https://fapi.binance.com`
  - 测试网: `https://demo-fapi.binance.com`
- **频率限制**: 1200 请求/分钟
- **K线限制**: 最大 1500 根

## 常用公共接口

### 1. K线数据

**Endpoint**: `/fapi/v1/klines`

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| symbol | string | 是 | 交易对 (如 ETHUSDT) |
| interval | string | 是 | 间隔 (1m, 5m, 15m, 1h, 4h, 1d) |
| startTime | long | 否 | 开始时间 (ms) |
| endTime | long | 否 | 结束时间 (ms) |
| limit | int | 否 | 数量 (最大1500) |

**示例**:
```bash
curl "https://fapi.binance.com/fapi/v1/klines?symbol=ETHUSDT&interval=1h&limit=100"
```

### 2. 当前价格

**Endpoint**: `/fapi/v1/ticker/price`

**示例**:
```bash
curl "https://fapi.binance.com/fapi/v1/ticker/price?symbol=ETHUSDT"
```

### 3. 24小时行情

**Endpoint**: `/fapi/v1/ticker/24hr`

**示例**:
```bash
curl "https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=ETHUSDT"
```

### 4. 资金费率

**Endpoint**: `/fapi/v1/premiumIndex`

**示例**:
```bash
curl "https://fapi.binance.com/fapi/v1/premiumIndex?symbol=ETHUSDT"
```

### 5. 资金费率历史

**Endpoint**: `/fapi/v1/fundingRate`

**示例**:
```bash
curl "https://fapi.binance.com/fapi/v1/fundingRate?symbol=ETHUSDT&limit=10"
```

## 认证接口（需要 API Key）

### 签名机制

1. 构建 query string（包含 timestamp）
2. HMAC SHA256 签名
3. 附加签名到请求

**示例代码 (Python)**:
```python
import hmac
import hashlib
import requests
import time

def sign(query_string, secret_key):
    return hmac.new(
        secret_key.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

api_key = "YOUR_API_KEY"
secret_key = "YOUR_SECRET_KEY"
timestamp = int(time.time() * 1000)

query = f"symbol=ETHUSDT&timestamp={timestamp}"
signature = sign(query, secret_key)

url = f"https://fapi.binance.com/fapi/v1/order?{query}&signature={signature}"
headers = {"X-MBX-APIKEY": api_key}

response = requests.post(url, headers=headers)
```

## 错误码

| 代码 | 说明 |
|------|------|
| -1000 | 未知错误 |
| -1001 | 断开连接 |
| -1002 | 未授权 |
| -1003 | 太多请求 |
| -1015 | 请求过多 |
| -1021 | 时间戳错误 |
| -1022 | 签名错误 |

## 测试网

Binance 提供测试网用于开发测试：
- **URL**: https://demo-fapi.binance.com
- **API Key**: 需在测试网申请（与生产环境独立）

获取测试网 API Key：https://testnet.binancefuture.com
