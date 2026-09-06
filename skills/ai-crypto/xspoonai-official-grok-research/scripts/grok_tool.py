#!/usr/bin/env python3
"""
Grok Research Tool - Aggressive web research via Grok-compatible API.

Author: Anonymous (Adapted from Frankieli123/grok-skill)
Version: 1.0.0
"""

import json
import os
import re
import urllib.request
import urllib.error
from typing import Any, List, Dict, Optional
from pydantic import Field
from spoon_ai.tools.base import BaseTool

class GrokResearchTool(BaseTool):
    name: str = "grok_research"
    description: str = (
        "Perform aggressive web research and information synthesis. "
        "Returns a synthesized answer with source citations. "
        "Use for time-sensitive, technical, or factual verification tasks."
    )
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "query": {
                "type": "string", 
                "description": "The search query or research task."
            },
            "model": {
                "type": "string",
                "description": "Optional model override (e.g., grok-2-latest).",
                "default": "grok-2-latest"
            }
        },
        "required": ["query"]
    })

    async def execute(self, query: str, model: str = "grok-2-latest") -> str:
        api_key = os.environ.get("GROK_API_KEY")
        base_url = os.environ.get("GROK_BASE_URL")
        
        if not api_key or not base_url:
            return json.dumps({
                "ok": False,
                "error": "Configuration missing",
                "detail": "Please set GROK_API_KEY and GROK_BASE_URL environment variables."
            })

        # Normalize base_url
        base_url = base_url.strip().rstrip("/")
        if not base_url.endswith("/v1"):
            url = f"{base_url}/v1/chat/completions"
        else:
            url = f"{base_url}/chat/completions"

        system_prompt = (
            "You are a web research assistant. Use live web search/browsing when answering. "
            "Return ONLY a single JSON object with keys: "
            "content (string), sources (array of objects with url/title/snippet when possible). "
            "Keep content concise and evidence-backed."
        )

        body = {
            "model": os.environ.get("GROK_MODEL", model),
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
            "temperature": 0.2,
            "stream": False,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }

        try:
            data_bytes = json.dumps(body).encode("utf-8")
            req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
            
            with urllib.request.urlopen(req, timeout=60.0) as response:
                resp_data = response.read().decode("utf-8")
                
                # Try parsing as a single JSON object first
                try:
                    data = json.loads(resp_data)
                    message_content = data["choices"][0]["message"]["content"]
                except (json.JSONDecodeError, KeyError, IndexError):
                    # Fallback: Handle SSE stream format (data: {...})
                    lines = resp_data.strip().split("\n")
                    combined_content = ""
                    for line in lines:
                        if line.startswith("data: "):
                            content_str = line[6:].strip()
                            if content_str == "[DONE]":
                                break
                            try:
                                chunk = json.loads(content_str)
                                # Handle errors inside the chunk
                                if "error" in chunk:
                                    return json.dumps({
                                        "ok": False,
                                        "error": "API Error in Stream",
                                        "detail": str(chunk["error"])
                                    })
                                    
                                # Handle both message (standard) and delta (stream) formats
                                if "choices" in chunk and len(chunk["choices"]) > 0:
                                    choice = chunk["choices"][0]
                                    if "message" in choice and "content" in choice["message"]:
                                        combined_content += choice["message"]["content"] or ""
                                    elif "delta" in choice and "content" in choice["delta"]:
                                        combined_content += choice["delta"]["content"] or ""
                            except json.JSONDecodeError:
                                continue
                    
                    if combined_content:
                        message_content = combined_content
                    else:
                        return json.dumps({
                            "ok": False,
                            "error": "Invalid response format",
                            "detail": f"Could not parse response as JSON or SSE stream. Raw: {resp_data[:100]}..."
                        })
        except urllib.error.HTTPError as e:
            return json.dumps({
                "ok": False,
                "error": f"HTTP {e.code}",
                "detail": e.read().decode("utf-8") if hasattr(e, 'read') else str(e)
            })
        except Exception as e:
            return json.dumps({
                "ok": False,
                "error": "Request failed",
                "detail": str(e)
            })

        # Process the result
        parsed_result = self._parse_message(message_content)
        
        output = {
            "ok": True,
            "query": query,
            "content": parsed_result.get("content", ""),
            "sources": parsed_result.get("sources", []),
            "raw": message_content if not parsed_result.get("content") else ""
        }
        
        return json.dumps(output, ensure_ascii=False)

    def _parse_message(self, text: str) -> Dict[str, Any]:
        text = text.strip()
        # Try direct JSON parsing
        if text.startswith("{") and text.endswith("}"):
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                pass
        
        # Try extracting JSON from code blocks
        match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
                
        # Fallback: extract URLs
        urls = re.findall(r"https?://[^\s)\]}>\"]+", text)
        sources = [{"url": url} for url in list(dict.fromkeys(urls))]
        return {"content": text, "sources": sources}
