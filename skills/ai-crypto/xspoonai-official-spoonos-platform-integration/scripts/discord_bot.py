#!/usr/bin/env python3
"""Discord Bot Integration for SpoonOS Agents."""

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


@bot.tree.command(name="analyze", description="Analyze a token")
async def analyze(interaction: discord.Interaction, token: str):
    """Slash command for token analysis."""
    await interaction.response.defer()
    response = await agent.run(f"Analyze token: {token}")
    await interaction.followup.send(response[:2000])


def main():
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))


if __name__ == "__main__":
    main()
