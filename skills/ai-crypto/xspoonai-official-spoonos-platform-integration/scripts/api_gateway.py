#!/usr/bin/env python3
"""REST API Gateway for SpoonOS Agents."""

import os
import uuid
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional

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


@app.get("/health")
async def health():
    return {"status": "healthy", "active_sessions": len(agent_pool)}


# Run: uvicorn api_gateway:app --host 0.0.0.0 --port 8000
