---
name: workflow-automation
description: Automate complex workflows and repetitive tasks using AI agents and tool integration. Use when user wants to create automated pipelines, integrate multiple services, or build task-specific agents.
version: 1.1.0
author: with-philia
license: MIT
tags: [AI, Automation, Workflow, Productivity, Agent, Integration, Python]
dependencies: [spoonos-sdk, langgraph, pydantic]
allowed-tools: Python(spoon_ai:*), Python(langgraph:*)
---

# AI Workflow Automation

Create intelligent, automated workflows that combine AI reasoning with external tool execution. This skill enables the construction of robust pipelines for data processing, content generation, and system integration, moving beyond simple scripts to adaptive, state-aware agents.

## When to Use

- **Complex Pipelines**: User wants to connect multiple APIs (e.g., "fetch data from X, process with Y, send to Z").
- **Intelligent Automation**: User wants to "automate a daily report", "build a news digest bot", or "triage customer emails".
- **Background Tasks**: User asks for a "background worker" or "cron job" with AI capabilities.
- **Decision Support**: User wants to streamline a repetitive manual process involving decision making (e.g., "approve if score > 80, else review").

## Decision Flow

**Determine the complexity and requirements of the automation.**

```
User Request for Automation
        │
  Analyze Complexity
        │
   ┌────┴─────────────────┐
 Simple                 Complex
 (Linear Sequence)      (Branching/Looping/State)
    │                      │
  Script                 Agent / Graph
  Based                  Based
    │                      │
    │                  Need Human Approval?
    │                  ┌───┴───┐
    │                 Yes     No
    │                  │       │
    │             Human-in-  Fully
    │             the-loop   Autonomous
    │                  │       │
    └──────┬───────────┴───────┘
           │
     Select Tools & APIs
           │
     Define State Schema
           │
     Implement Logic
           │
     Test & Deploy
```

## Core Concepts

1.  **Triggers**: Events that initiate the workflow (e.g., Schedule/Cron, Webhook, Manual Input, File Upload).
2.  **Steps (Nodes)**: Discrete units of work.
    - _Action_: Executing a tool or API call (deterministic).
    - _Reasoning_: LLM processing (summarization, decision making, extraction).
3.  **State**: The shared context passed between steps (e.g., `messages`, `current_data`, `errors`).
4.  **Routing (Edges)**: Logic to determine the next step based on current state (e.g., "if error, go to retry; else go to finish").
5.  **Human-in-the-loop**: Pausing execution for human review before proceeding with critical actions.

## Implementation Guide

### Step 1: Define the Workflow

Clearly outline the inputs, processing steps, decision points, and desired outputs.

_Example: Daily Tech News Digest_

- **Input**: RSS feeds or NewsAPI query.
- **Process**:
  1. Fetch latest articles.
  2. Filter for relevance (e.g., "AI", "LLM").
  3. Summarize each article into 3 bullet points.
  4. Generate an HTML email template.
- **Output**: Send email via SMTP or SendGrid.

### Step 2: Select Tools & Manage Secrets

Identify necessary integrations and ensure API keys are managed securely (e.g., `.env` file).

- **Data Source**: `requests` (Python), `NewsAPI`, `Tavily`.
- **Processing**: `OpenAI` or `Anthropic` (via SpoonOS).
- **Output**: `smtplib`, `SendGrid`, `Slack Webhook`.

**Security Note**: Never hardcode API keys. Use `os.getenv("API_KEY")`.

### Step 3: Build the Agent (SpoonReactSkill)

For simpler, tool-using agents, use `SpoonReactSkill`.

```python
import os
from spoon_ai.agents import SpoonReactSkill
from spoon_ai.tools import Tool
from spoon_ai.llm import ChatBot

class NewsDigestAgent(SpoonReactSkill):
    def __init__(self):
        super().__init__(
            name="news_digest_bot",
            description="Fetches and summarizes tech news.",
            llm=ChatBot(model="gpt-4o"),
            tools=[self.fetch_news, self.send_email]
        )

    @Tool
    def fetch_news(self, topic: str) -> str:
        """Fetches latest news about a topic. Returns JSON string of articles."""
        # Mock implementation
        return f"Found 5 articles about {topic}..."

    @Tool
    def send_email(self, recipient: str, subject: str, content: str) -> str:
        """Sends the summarized content via email."""
        print(f"Sending email to {recipient}: {subject}")
        return "Email sent successfully."

# Usage
async def run_agent():
    agent = NewsDigestAgent()
    await agent.initialize()
    result = await agent.run("Send me a digest of today's AI news to user@example.com")
    print(result)
```

### Step 4: Orchestration (StateGraph)

For complex workflows with strict control flow, loops, or state management, use `StateGraph`.

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    topic: str
    articles: list
    summary: str

def fetch_node(state: AgentState):
    # Fetch logic
    return {"articles": ["Article 1", "Article 2"]}

def summarize_node(state: AgentState):
    # LLM summarization logic
    summary = f"Summary of {len(state['articles'])} articles..."
    return {"summary": summary}

def notify_node(state: AgentState):
    # Send notification
    print(f"Sending: {state['summary']}")
    return {}

# Define Graph
workflow = StateGraph(AgentState)
workflow.add_node("fetch", fetch_node)
workflow.add_node("summarize", summarize_node)
workflow.add_node("notify", notify_node)

workflow.set_entry_point("fetch")
workflow.add_edge("fetch", "summarize")
workflow.add_edge("summarize", "notify")
workflow.add_edge("notify", END)

app = workflow.compile()
```

## Example Workflows

### 1. Automated Code Reviewer

**Goal**: Automatically review new Pull Requests and post comments.

1.  **Trigger**: GitHub Webhook (PR Created).
2.  **Step 1 (Fetch)**: Get PR diff using GitHub API.
3.  **Step 2 (Analyze)**: Send diff to LLM with prompt "Identify bugs and security risks".
4.  **Step 3 (Filter)**: Ignore minor style issues if configured.
5.  **Step 4 (Post)**: Post review comments to GitHub PR.

### 2. Customer Support Triage

**Goal**: Categorize and draft responses for support tickets.

1.  **Trigger**: New ticket in Zendesk/Jira.
2.  **Step 1 (Read)**: Extract ticket subject and body.
3.  **Step 2 (Classify)**: LLM classifies intent (Billing, Technical, Feature Request).
4.  **Step 3 (RAG)**: Retrieve relevant documentation based on classification.
5.  **Step 4 (Draft)**: Generate response using retrieved docs.
6.  **Step 5 (Human Review)**: Save as "Draft" status for human agent approval.

### 3. Social Media Content Calendar

**Goal**: Generate and schedule posts from a blog RSS feed.

1.  **Trigger**: New item in RSS feed.
2.  **Step 1 (Extract)**: Get title, content, and URL.
3.  **Step 2 (Generate)**: Create variations for Twitter (short), LinkedIn (professional), and Facebook.
4.  **Step 3 (Image)**: Generate a thumbnail using DALL-E / Midjourney API.
5.  **Step 4 (Schedule)**: Post to Buffer/Hootsuite API.

## Tools & Integrations

| Category          | Common Tools                                | Use Case                             |
| :---------------- | :------------------------------------------ | :----------------------------------- |
| **Communication** | Slack, Discord, Telegram, Email (SMTP/IMAP) | Notifications, Chatbots, Alerts      |
| **Development**   | GitHub, GitLab, Jira, Linear                | Code review, Issue tracking          |
| **Data/Docs**     | Notion, Google Sheets, Airtable, Vector DBs | Knowledge base, CRM, structured data |
| **Social**        | Twitter (X), LinkedIn, Reddit               | Content publishing, monitoring       |
| **Search**        | Tavily, Google Search, Bing                 | Real-time information retrieval      |

## Debugging & Monitoring

- **Traceability**: Use tools like LangSmith or Arize Phoenix to trace LLM calls and agent steps.
- **Verbose Mode**: Enable verbose logging in your agent framework to see intermediate thoughts and tool outputs.
- **Dry Run**: Implement a "dry run" flag that mocks side-effect actions (like sending emails or deleting files).

## Security & Privacy

- **Least Privilege**: Give the agent only the permissions it needs (e.g., read-only access to production DBs).
- **PII Redaction**: Detect and redact Personally Identifiable Information before sending data to LLM providers.
- **Human Approval**: Always require human confirmation for high-stakes actions (e.g., transferring funds, deploying code).

## Best Practices

- **Idempotency**: Ensure steps can be retried without side effects.
- **Graceful Degradation**: If a non-critical tool fails (e.g., image generation), the workflow should continue or notify the user rather than crashing.
- **Modular Design**: Create reusable tools (e.g., a generic `send_slack_message` tool) that can be used across multiple agents.
