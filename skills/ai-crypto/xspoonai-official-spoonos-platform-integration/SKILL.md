---
name: spoonos-platform-integration
description: Deploy SpoonOS agents to messaging platforms and APIs. Use when integrating agents with Telegram, Discord, Slack, REST APIs, webhooks, or scheduled tasks.
---

# Platform Integration

Connect SpoonOS agents to external platforms.

## Integration Options

| Platform | Use Case | Transport |
|----------|----------|-----------|
| Telegram | Chat bot | Polling/Webhook |
| Discord | Server bot | Gateway/Webhook |
| Slack | Workspace bot | Events API |
| REST API | HTTP interface | FastAPI/Flask |
| Webhooks | Event triggers | HTTP POST |
| Scheduler | Cron tasks | APScheduler |

## Telegram Bot

### Setup

```bash
pip install python-telegram-bot
```

### Implementation

```python
# telegram_bot.py
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from spoon_ai.agents import SpoonReactMCP
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager

# Initialize agent
agent = SpoonReactMCP(
    name="telegram_agent",
    llm=ChatBot(model_name="gpt-4o"),
    tools=ToolManager([]),
    max_steps=10
)

async def start(update: Update, context):
    """Handle /start command."""
    await update.message.reply_text(
        "Hello! I'm your SpoonOS agent. Send me a message!"
    )

async def handle_message(update: Update, context):
    """Process user messages through agent."""
    user_message = update.message.text
    user_id = update.effective_user.id

    # Show typing indicator
    await update.message.chat.send_action("typing")

    try:
        # Run agent
        response = await agent.run(user_message)

        # Split long messages (Telegram limit: 4096 chars)
        if len(response) > 4000:
            for i in range(0, len(response), 4000):
                await update.message.reply_text(response[i:i+4000])
        else:
            await update.message.reply_text(response)

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def main():
    """Run the bot."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
```

### Webhook Mode (Production)

```python
# telegram_webhook.py
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application

app = FastAPI()
telegram_app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}

# Set webhook:
# curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://your-domain.com/webhook"
```

## Discord Bot

### Setup

```bash
pip install discord.py
```

### Implementation

```python
# discord_bot.py
import os
import discord
from discord.ext import commands
from spoon_ai.agents import SpoonReactMCP
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize agent
agent = SpoonReactMCP(
    name="discord_agent",
    llm=ChatBot(model_name="gpt-4o"),
    tools=ToolManager([]),
    max_steps=10
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name="ask")
async def ask(ctx, *, question: str):
    """Ask the agent a question."""
    async with ctx.typing():
        try:
            response = await agent.run(question)

            # Split long messages (Discord limit: 2000 chars)
            if len(response) > 1900:
                for i in range(0, len(response), 1900):
                    await ctx.send(response[i:i+1900])
            else:
                await ctx.send(response)

        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

@bot.event
async def on_message(message):
    """Handle mentions."""
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        content = message.content.replace(f"<@{bot.user.id}>", "").strip()
        if content:
            async with message.channel.typing():
                response = await agent.run(content)
                await message.reply(response[:2000])

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
```

### Slash Commands

```python
@bot.tree.command(name="analyze", description="Analyze a token")
async def analyze(interaction: discord.Interaction, token: str):
    await interaction.response.defer()

    response = await agent.run(f"Analyze token: {token}")
    await interaction.followup.send(response[:2000])

# Sync commands on ready
@bot.event
async def on_ready():
    await bot.tree.sync()
```

## REST API Gateway

### FastAPI Implementation

```python
# api_gateway.py
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import asyncio
import uuid

from spoon_ai.agents import SpoonReactMCP
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager

app = FastAPI(title="SpoonOS Agent API")
security = HTTPBearer()

# Agent pool for concurrent requests
agent_pool = {}

class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    max_steps: Optional[int] = 10

class QueryResponse(BaseModel):
    response: str
    session_id: str
    steps_taken: int

def get_or_create_agent(session_id: str) -> SpoonReactMCP:
    """Get existing agent or create new one."""
    if session_id not in agent_pool:
        agent_pool[session_id] = SpoonReactMCP(
            name=f"api_agent_{session_id}",
            llm=ChatBot(model_name="gpt-4o"),
            tools=ToolManager([]),
            max_steps=15
        )
    return agent_pool[session_id]

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API token."""
    if credentials.credentials != os.getenv("API_TOKEN"):
        raise HTTPException(status_code=401, detail="Invalid token")
    return credentials.credentials

@app.post("/v1/query", response_model=QueryResponse)
async def query_agent(
    request: QueryRequest,
    token: str = Depends(verify_token)
):
    """Execute agent query."""
    session_id = request.session_id or str(uuid.uuid4())
    agent = get_or_create_agent(session_id)

    try:
        response = await agent.run(request.query)
        return QueryResponse(
            response=response,
            session_id=session_id,
            steps_taken=agent.current_step
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/query/stream")
async def query_agent_stream(request: QueryRequest):
    """Stream agent response."""
    from fastapi.responses import StreamingResponse

    session_id = request.session_id or str(uuid.uuid4())
    agent = get_or_create_agent(session_id)

    async def generate():
        async for chunk in agent.stream(request.query):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

@app.delete("/v1/session/{session_id}")
async def delete_session(session_id: str):
    """Clean up session."""
    if session_id in agent_pool:
        del agent_pool[session_id]
    return {"status": "deleted"}

# Run: uvicorn api_gateway:app --host 0.0.0.0 --port 8000
```

## Webhook Handler

### Generic Webhook Receiver

```python
# webhook_handler.py
from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
import hmac
import hashlib

app = FastAPI()

class WebhookConfig(BaseModel):
    source: str
    secret: str
    agent_prompt_template: str

WEBHOOK_CONFIGS = {
    "github": WebhookConfig(
        source="github",
        secret=os.getenv("GITHUB_WEBHOOK_SECRET"),
        agent_prompt_template="Analyze this GitHub event: {event}"
    ),
    "stripe": WebhookConfig(
        source="stripe",
        secret=os.getenv("STRIPE_WEBHOOK_SECRET"),
        agent_prompt_template="Process this payment event: {event}"
    )
}

def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify webhook signature."""
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)

async def process_webhook(source: str, payload: dict):
    """Background task to process webhook."""
    config = WEBHOOK_CONFIGS[source]
    prompt = config.agent_prompt_template.format(event=payload)

    agent = SpoonReactMCP(
        name=f"webhook_{source}",
        llm=ChatBot(model_name="gpt-4o"),
        tools=ToolManager([])
    )

    result = await agent.run(prompt)
    # Store result, send notification, etc.
    print(f"Webhook processed: {result}")

@app.post("/webhook/{source}")
async def receive_webhook(
    source: str,
    request: Request,
    background_tasks: BackgroundTasks
):
    """Receive and process webhooks."""
    if source not in WEBHOOK_CONFIGS:
        return {"error": "Unknown source"}, 400

    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256", "")

    if not verify_signature(body, signature, WEBHOOK_CONFIGS[source].secret):
        return {"error": "Invalid signature"}, 401

    payload = await request.json()
    background_tasks.add_task(process_webhook, source, payload)

    return {"status": "accepted"}
```

## Scheduled Tasks

### APScheduler Integration

```python
# scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio

from spoon_ai.agents import SpoonReactMCP
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager

scheduler = AsyncIOScheduler()

# Initialize agent
agent = SpoonReactMCP(
    name="scheduled_agent",
    llm=ChatBot(model_name="gpt-4o"),
    tools=ToolManager([])
)

async def daily_market_report():
    """Generate daily market report."""
    result = await agent.run(
        "Generate a daily market report for top 10 cryptocurrencies"
    )
    # Send to Telegram, Discord, email, etc.
    print(f"Daily report: {result}")

async def hourly_price_check():
    """Check prices hourly."""
    result = await agent.run(
        "Check current BTC and ETH prices, alert if >5% change"
    )
    print(f"Price check: {result}")

async def weekly_portfolio_review():
    """Weekly portfolio analysis."""
    result = await agent.run(
        "Review portfolio performance for the past week"
    )
    print(f"Weekly review: {result}")

# Schedule tasks
scheduler.add_job(
    daily_market_report,
    CronTrigger(hour=9, minute=0),  # 9:00 AM daily
    id="daily_report"
)

scheduler.add_job(
    hourly_price_check,
    CronTrigger(minute=0),  # Every hour
    id="hourly_check"
)

scheduler.add_job(
    weekly_portfolio_review,
    CronTrigger(day_of_week="mon", hour=10),  # Monday 10 AM
    id="weekly_review"
)

async def main():
    scheduler.start()
    print("Scheduler started...")

    # Keep running
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
```

## Environment Configuration

```bash
# Platform tokens
TELEGRAM_BOT_TOKEN=...
DISCORD_BOT_TOKEN=...
SLACK_BOT_TOKEN=...

# API security
API_TOKEN=...

# Webhook secrets
GITHUB_WEBHOOK_SECRET=...
STRIPE_WEBHOOK_SECRET=...

# LLM
OPENAI_API_KEY=...
```

## Best Practices

1. **Rate Limiting** - Implement per-user limits
2. **Error Handling** - Graceful degradation
3. **Logging** - Structured logs for debugging
4. **Timeouts** - Set appropriate timeouts
5. **Session Management** - Clean up idle sessions
