---
name: spoonos-deployment-guide
description: Deploy SpoonOS agents to production environments. Use when containerizing agents with Docker, deploying to cloud platforms (AWS, GCP, Vercel), or setting up self-hosted infrastructure.
---

# Deployment Guide

Production deployment patterns for SpoonOS agents.

## Deployment Options

| Method | Best For | Complexity |
|--------|----------|------------|
| Docker | Portability, consistency | Low |
| AWS Lambda | Serverless, event-driven | Medium |
| GCP Cloud Run | Auto-scaling containers | Medium |
| Vercel | API endpoints | Low |
| VPS | Full control, cost-effective | Medium |

## Docker Deployment

### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s \
    CMD python -c "import spoon_ai; print('ok')" || exit 1

# Run
CMD ["python", "main.py"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  agent:
    build: .
    restart: unless-stopped
    env_file:
      - .env
    environment:
      - LOG_LEVEL=INFO
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

### Build and Run

```bash
# Build
docker build -t spoonos-agent .

# Run
docker run -d \
  --name my-agent \
  --env-file .env \
  -p 8000:8000 \
  spoonos-agent

# With compose
docker-compose up -d
```

## AWS Lambda

### Handler

```python
# lambda_handler.py
import json
import os
from spoon_ai.agents import SpoonReactMCP
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager

# Initialize outside handler for warm starts
agent = None

def get_agent():
    global agent
    if agent is None:
        agent = SpoonReactMCP(
            name="lambda_agent",
            llm=ChatBot(model_name="gpt-4o"),
            tools=ToolManager([]),
            max_steps=10
        )
    return agent

def handler(event, context):
    """Lambda handler."""
    try:
        body = json.loads(event.get('body', '{}'))
        query = body.get('query', '')

        if not query:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing query'})
            }

        agent = get_agent()

        # Run synchronously (Lambda doesn't support async directly)
        import asyncio
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(agent.run(query))

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'response': response})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

### SAM Template

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Timeout: 300
    MemorySize: 1024
    Runtime: python3.12

Resources:
  AgentFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: .
      Handler: lambda_handler.handler
      Environment:
        Variables:
          OPENAI_API_KEY: !Ref OpenAIKey
      Events:
        Api:
          Type: Api
          Properties:
            Path: /query
            Method: post

Parameters:
  OpenAIKey:
    Type: String
    NoEcho: true

Outputs:
  ApiEndpoint:
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/query"
```

### Deploy

```bash
# Install SAM CLI
pip install aws-sam-cli

# Build and deploy
sam build
sam deploy --guided
```

## GCP Cloud Run

### Dockerfile for Cloud Run

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run uses PORT env var
ENV PORT=8080

CMD exec uvicorn api:app --host 0.0.0.0 --port $PORT
```

### API for Cloud Run

```python
# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from spoon_ai.agents import SpoonReactMCP
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager

app = FastAPI()

agent = SpoonReactMCP(
    name="cloudrun_agent",
    llm=ChatBot(model_name="gpt-4o"),
    tools=ToolManager([])
)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query(request: QueryRequest):
    response = await agent.run(request.query)
    return {"response": response}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### Deploy to Cloud Run

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/spoonos-agent

# Deploy
gcloud run deploy spoonos-agent \
  --image gcr.io/PROJECT_ID/spoonos-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "OPENAI_API_KEY=sk-..."
```

## Vercel Deployment

### API Route

```python
# api/query.py
from http.server import BaseHTTPRequestHandler
import json
import asyncio
from spoon_ai.agents import SpoonReactMCP
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager

agent = SpoonReactMCP(
    name="vercel_agent",
    llm=ChatBot(model_name="gpt-4o"),
    tools=ToolManager([])
)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(content_length))

        query = body.get('query', '')

        loop = asyncio.new_event_loop()
        response = loop.run_until_complete(agent.run(query))
        loop.close()

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'response': response}).encode())
```

### vercel.json

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/*.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    }
  ]
}
```

### Deploy

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

## Self-Hosted VPS

### Setup Script

```bash
#!/bin/bash
# setup.sh

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.12
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install python3.12 python3.12-venv -y

# Create app directory
sudo mkdir -p /opt/spoonos
sudo chown $USER:$USER /opt/spoonos

# Clone and setup
cd /opt/spoonos
git clone https://github.com/your-org/your-agent.git app
cd app

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your keys
```

### Systemd Service

```ini
# /etc/systemd/system/spoonos-agent.service
[Unit]
Description=SpoonOS Agent
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/spoonos/app
Environment=PATH=/opt/spoonos/app/venv/bin
ExecStart=/opt/spoonos/app/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Enable and Start

```bash
sudo systemctl daemon-reload
sudo systemctl enable spoonos-agent
sudo systemctl start spoonos-agent

# Check status
sudo systemctl status spoonos-agent

# View logs
sudo journalctl -u spoonos-agent -f
```

### Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/spoonos
server {
    listen 80;
    server_name agent.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### SSL with Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d agent.yourdomain.com
```

## Environment Management

### Production .env

```bash
# .env.production
NODE_ENV=production
LOG_LEVEL=INFO

# LLM (use secrets manager in production)
OPENAI_API_KEY=${OPENAI_API_KEY}

# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Redis
REDIS_URL=redis://localhost:6379

# Monitoring
SENTRY_DSN=https://...
```

### Secrets Management

```python
# config.py
import os
from functools import lru_cache

# AWS Secrets Manager
def get_secret_aws(secret_name: str) -> str:
    import boto3
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

# GCP Secret Manager
def get_secret_gcp(secret_name: str) -> str:
    from google.cloud import secretmanager
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/PROJECT_ID/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode()

@lru_cache
def get_config():
    env = os.getenv("ENV", "development")

    if env == "production":
        return {
            "openai_key": get_secret_aws("openai-api-key"),
            "database_url": get_secret_aws("database-url"),
        }
    else:
        return {
            "openai_key": os.getenv("OPENAI_API_KEY"),
            "database_url": os.getenv("DATABASE_URL"),
        }
```

## Monitoring

### Health Check Endpoint

```python
@app.get("/health")
async def health():
    checks = {
        "agent": "healthy",
        "llm": "unknown",
        "tools": "unknown"
    }

    # Check LLM connection
    try:
        # Quick test
        checks["llm"] = "healthy"
    except:
        checks["llm"] = "unhealthy"

    status = "healthy" if all(v == "healthy" for v in checks.values()) else "degraded"

    return {"status": status, "checks": checks}
```

### Logging Configuration

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        })

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
```

## Deployment Checklist

- [ ] Environment variables configured
- [ ] Secrets in secure storage
- [ ] Health check endpoint working
- [ ] Logging configured
- [ ] Error tracking (Sentry) enabled
- [ ] SSL/TLS configured
- [ ] Rate limiting implemented
- [ ] Backup strategy in place
- [ ] Monitoring alerts configured
- [ ] Rollback procedure documented
