#!/usr/bin/env python3
"""Telegram Bot Integration for SpoonOS Agents."""

import os
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
    """Run the bot in polling mode."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
