"""
Pika MCP Plugin — MCP Server

Exposes Pika video generation capabilities as MCP tools.
Can run standalone or connect to the Pika MCP at mcp.pika.me.

Run: python -m plugins.pika-mcp.server
"""

import json
import sys
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field, asdict

try:
    from .pika_client import (
        PikaClient,
        PikaClientError,
        PikaAuthenticationError,
        PikaGenerationError,
        PikaVideoResult,
        VideoModel,
        VideoAspectRatio,
    )
except ImportError:
    # Allow direct execution when not in a package
    from pika_client import (  # type: ignore
        PikaClient,
        PikaClientError,
        PikaAuthenticationError,
        PikaGenerationError,
        PikaVideoResult,
        VideoModel,
        VideoAspectRatio,
    )

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger("pika-mcp-server")


# ── Tool definitions (MCP-compatible) ──────────────────────────────────────

MCP_TOOLS = [
    {
        "name": "pika_text_to_video",
        "description": "Generate a video from a text description using Pika AI. "
                       "Supports 5s or 10s videos in 16:9, 9:16, or 1:1 aspect ratios. "
                       "Uses Pika 2.5 model by default.",
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Detailed text description of the video to generate"
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["16:9", "9:16", "1:1"],
                    "description": "Video aspect ratio (default: 16:9)"
                },
                "duration_seconds": {
                    "type": "integer",
                    "enum": [5, 10],
                    "description": "Video length in seconds (default: 5)"
                },
                "model": {
                    "type": "string",
                    "enum": ["pika-2.5", "pika-2.1"],
                    "description": "Pika model version (default: pika-2.5)"
                },
                "negative_prompt": {
                    "type": "string",
                    "description": "What to avoid in the generated video"
                }
            },
            "required": ["prompt"]
        }
    },
    {
        "name": "pika_image_to_video",
        "description": "Generate a video from a starting image with text guidance using Pika AI.",
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Text description of motion/animation to apply"
                },
                "image_url": {
                    "type": "string",
                    "description": "URL of the source image to animate"
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["16:9", "9:16", "1:1"],
                    "description": "Video aspect ratio (default: 16:9)"
                },
                "duration_seconds": {
                    "type": "integer",
                    "enum": [5, 10],
                    "description": "Video length in seconds (default: 5)"
                }
            },
            "required": ["prompt", "image_url"]
        }
    },
    {
        "name": "pika_health",
        "description": "Check if the Pika API is configured and accessible. "
                       "Returns configuration status and available models.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
]

# ── MCP Server ─────────────────────────────────────────────────────────────

class PikaMCPServer:
    """Minimal MCP server implementing the protocol over stdio."""

    def __init__(self, client: Optional[PikaClient] = None):
        self.client = client
        self.tools = MCP_TOOLS

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single JSON-RPC request."""
        method = request.get("method", "")
        req_id = request.get("id")

        if method == "tools/list":
            return {"jsonrpc": "2.0", "id": req_id, "result": self.tools}

        elif method == "tools/call":
            return self._handle_tool_call(request)

        elif method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": "gentech-pika-mcp",
                        "version": "0.1.0"
                    }
                }
            }

        elif method == "ping":
            return {"jsonrpc": "2.0", "id": req_id, "result": {}}

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }

    def _handle_tool_call(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool call and return the result."""
        params = request.get("params", {})
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        req_id = request.get("id")

        try:
            if tool_name == "pika_text_to_video":
                result = self._text_to_video(arguments)
            elif tool_name == "pika_image_to_video":
                result = self._image_to_video(arguments)
            elif tool_name == "pika_health":
                result = self._health_check()
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32602, "message": f"Unknown tool: {tool_name}"}
                }

            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            }

        except PikaAuthenticationError as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32000, "message": f"Authentication error: {e}"}
            }
        except PikaGenerationError as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32001, "message": f"Generation error: {e}"}
            }
        except Exception as e:
            logger.exception(f"Unhandled error in {tool_name}")
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32603, "message": f"Internal error: {e}"}
            }

    def _text_to_video(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute pika_text_to_video tool."""
        if not self.client:
            raise PikaClientError("Pika client not configured. Set FAL_KEY or use Pika MCP at mcp.pika.me.")
        model_map = {"pika-2.5": VideoModel.PIKA_2_5, "pika-2.1": VideoModel.PIKA_2_1}
        model_key = args.get("model", "pika-2.5")
        model = model_map.get(model_key, VideoModel.PIKA_2_5)

        result = self.client.text_to_video(
            prompt=args["prompt"],
            model=model,
            aspect_ratio=VideoAspectRatio(args.get("aspect_ratio", "16:9")),
            duration_seconds=args.get("duration_seconds", 5),
            negative_prompt=args.get("negative_prompt"),
        )
        return self._format_result(result)

    def _image_to_video(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute pika_image_to_video tool."""
        if not self.client:
            raise PikaClientError("Pika client not configured. Set FAL_KEY or use Pika MCP at mcp.pika.me.")
        result = self.client.image_to_video(
            prompt=args["prompt"],
            image_url=args["image_url"],
            aspect_ratio=VideoAspectRatio(args.get("aspect_ratio", "16:9")),
            duration_seconds=args.get("duration_seconds", 5),
        )
        return self._format_result(result)

    def _health_check(self) -> Dict[str, Any]:
        """Execute pika_health tool."""
        if not self.client:
            return {
                "configured": False,
                "error": "No Pika API key configured. Set FAL_KEY or add Pika MCP server.",
                "alternative": "Use Pika MCP server at mcp.pika.me/api/mcp instead."
            }
        return self.client.health_check()

    @staticmethod
    def _format_result(result: PikaVideoResult) -> Dict[str, Any]:
        return {
            "video_url": result.video_url,
            "duration_seconds": result.duration_seconds,
            "request_id": result.request_id,
            "credits_used": result.credits_used,
            "model_used": result.model_used,
            "status": "completed" if result.video_url else "pending",
        }


# ── Stdio server loop ─────────────────────────────────────────────────────

def main():
    """Run the MCP server over stdio (MCP protocol transport)."""
    import argparse
    parser = argparse.ArgumentParser(description="GenTech Pika MCP Server")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Try to initialize Pika client
    client = None
    try:
        client = PikaClient()
        logger.info("Pika Fal.ai client initialized")
    except PikaAuthenticationError:
        logger.warning("No FAL_KEY set — Pika Fal.ai client disabled")
        logger.info("Alternative: use Pika MCP at mcp.pika.me/api/mcp")

    server = PikaMCPServer(client)

    logger.info("Pika MCP server ready (stdio transport)")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = server.handle_request(request)
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
        except json.JSONDecodeError:
            err = {"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
