---
name: weather-forecast
description: "Get current weather conditions and forecasts for any location"
homepage: https://github.com/chubin/wttr.in
metadata:
  {
    "openclaw":
      {
        "emoji": "🌤️",
        "requires": { "bins": ["curl", "jq"] },
        "credentials": [],
      },
  }
---
# Weather Forecast

Get current weather, forecasts, and alerts for any location worldwide.

## Current Weather

Get current conditions using wttr.in (no API key needed):

```bash
# Simple one-liner
curl -s "wttr.in/San+Francisco?format=%l:+%c+%t+%h+%w"

# Detailed current weather
curl -s "wttr.in/New+York?format=j1" | jq '.current_condition[0] | {
  temp_f: .temp_F,
  temp_c: .temp_C,
  feels_like: .FeelsLikeF,
  humidity: .humidity,
  wind_mph: .windspeedMiles,
  wind_dir: .winddir16Point,
  condition: .weatherDesc[0].value,
  uv_index: .uvIndex
}'

# ASCII art weather (great for terminal)
curl -s "wttr.in/London"

# Compact view
curl -s "wttr.in/Tokyo?0"
```

## Multi-Day Forecast

```bash
# 3-day forecast
curl -s "wttr.in/Chicago?format=j1" | jq '.weather[] | {
  date: .date,
  max_temp: .maxtempF,
  min_temp: .mintempF,
  avg_temp: .avgtempF,
  condition: .hourly[4].weatherDesc[0].value,
  chance_of_rain: .hourly[4].chanceofrain
}'

# Week forecast (text format)
curl -s "wttr.in/Seattle?format=v2"
```

## Weather by Coordinates

```bash
# Use latitude,longitude
curl -s "wttr.in/37.7749,-122.4194?format=j1" | jq '.current_condition[0]'
```

## Weather Alerts

Using National Weather Service API (US only, no key needed):

```bash
# Get alerts for a location
curl -s "https://api.weather.gov/alerts/active?point=40.7128,-74.0060" | jq '.features[] | {
  event: .properties.event,
  headline: .properties.headline,
  severity: .properties.severity,
  expires: .properties.expires
}'

# Get alerts by state
curl -s "https://api.weather.gov/alerts/active?area=CA" | jq '.features | length'
```

## OpenWeatherMap (Free API Key)

For more detailed data, use OpenWeatherMap (free tier: 1000 calls/day):

```bash
# Current weather
curl -s "https://api.openweathermap.org/data/2.5/weather?q=Miami&appid=YOUR_API_KEY&units=imperial" | jq '{
  city: .name,
  temp: .main.temp,
  feels_like: .main.feels_like,
  humidity: .main.humidity,
  description: .weather[0].description,
  wind_speed: .wind.speed
}'

# 5-day forecast
curl -s "https://api.openweathermap.org/data/2.5/forecast?q=Denver&appid=YOUR_API_KEY&units=imperial" | jq '.list[0:8] | .[] | {
  time: .dt_txt,
  temp: .main.temp,
  description: .weather[0].description
}'
```

## Air Quality

```bash
# Using OpenWeatherMap Air Pollution API
curl -s "https://api.openweathermap.org/data/2.5/air_pollution?lat=34.0522&lon=-118.2437&appid=YOUR_API_KEY" | jq '.list[0] | {
  aqi: .main.aqi,
  co: .components.co,
  no2: .components.no2,
  pm2_5: .components.pm2_5,
  pm10: .components.pm10
}'
# AQI: 1=Good, 2=Fair, 3=Moderate, 4=Poor, 5=Very Poor
```

## Sunrise/Sunset

```bash
# Get sun times
curl -s "wttr.in/Boston?format=j1" | jq '.weather[0].astronomy[0] | {
  sunrise: .sunrise,
  sunset: .sunset,
  moonrise: .moonrise,
  moonset: .moonset,
  moon_phase: .moon_phase
}'
```

## Weather Comparison

Compare weather across cities:

```bash
# Compare multiple cities
for city in "New York" "Los Angeles" "Chicago"; do
  echo -n "$city: "
  curl -s "wttr.in/${city// /+}?format=%t+%c"
  echo
done
```

## Moon Phase

```bash
curl -s "wttr.in/Moon"
```

## Tips

- wttr.in is free and requires no API key
- For production apps, use OpenWeatherMap or Weather.gov APIs
- Cache weather data (it doesn't change that fast)
- Use `?format=` parameter for custom output formats

## Format Codes (wttr.in)

| Code | Description |
|------|-------------|
| %c | Weather condition icon |
| %t | Temperature |
| %h | Humidity |
| %w | Wind |
| %l | Location |
| %p | Precipitation |

## Resources

- [wttr.in GitHub](https://github.com/chubin/wttr.in)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [Weather.gov API](https://www.weather.gov/documentation/services-web-api)
