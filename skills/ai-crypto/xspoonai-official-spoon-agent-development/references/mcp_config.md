# MCP Configuration Reference

## Transport Types

### NPX (Node.js)

```python
mcp_config={
    "command": "npx",
    "args": ["-y", "package-name"],
    "env": {"API_KEY": "..."},
    "timeout": 30,
    "max_retries": 3
}
```

### Python

```python
mcp_config={
    "command": "python",
    "args": ["path/to/server.py"],
    "env": {"DATA_PATH": "/data"}
}
```

### UVX

```python
mcp_config={
    "command": "uvx",
    "args": ["package-name", "--flag"],
    "env": {}
}
```

### SSE (Server-Sent Events)

```python
mcp_config={
    "url": "https://mcp.example.com/sse",
    "transport": "sse"
}
```

### WebSocket

```python
mcp_config={
    "url": "wss://mcp.example.com/ws"
}
```

### HTTP Streamable

```python
mcp_config={
    "url": "https://mcp.example.com/api",
    "transport": "http",
    "headers": {"Authorization": "Bearer token"}
}
```

## Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `command` | str | - | Command to execute |
| `args` | list | [] | Command arguments |
| `env` | dict | {} | Environment variables |
| `url` | str | - | Server URL (SSE/WS/HTTP) |
| `transport` | str | "sse" | Transport type |
| `timeout` | int | 30 | Connection timeout (seconds) |
| `max_retries` | int | 3 | Max retry attempts |
| `health_check_interval` | int | 300 | Health check interval (seconds) |
