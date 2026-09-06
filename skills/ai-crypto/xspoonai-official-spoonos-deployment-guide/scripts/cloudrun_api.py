#!/usr/bin/env python3
"""GCP Cloud Run API for SpoonOS Agent."""

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


# Run: uvicorn cloudrun_api:app --host 0.0.0.0 --port $PORT
