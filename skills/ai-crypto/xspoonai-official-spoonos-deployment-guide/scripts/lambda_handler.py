#!/usr/bin/env python3
"""AWS Lambda Handler for SpoonOS Agent."""

import json
import asyncio
from spoon_ai.agents import SpoonReactMCP
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager

# Initialize outside handler for warm starts
agent = None


def get_agent():
    """Get or create agent instance."""
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

        # Run synchronously
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
