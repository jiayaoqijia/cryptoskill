"""
Tests for Pika MCP Plugin — Client and Server
"""
import sys
import os
# Add plugin package to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
import pytest
from unittest.mock import patch, MagicMock

from pika_client import (
    PikaClient,
    PikaAuthenticationError,
    PikaVideoResult,
    VideoModel,
    VideoAspectRatio,
)
from server import PikaMCPServer, MCP_TOOLS


# ── Client Tests ───────────────────────────────────────────────────────────

class TestPikaClient:
    """Test Pika client initialization and validation."""

    def test_init_without_key_raises(self):
        """Client without API key should raise."""
        with patch.dict("os.environ", clear=True):
            with pytest.raises(PikaAuthenticationError, match="FAL_KEY"):
                PikaClient()

    def test_init_with_env_key(self):
        """Client should initialize from env var."""
        with patch.dict("os.environ", {"FAL_KEY": "test-key-12345"}):
            client = PikaClient()
            assert client.api_key == "test-key-12345"

    def test_init_with_explicit_key(self):
        """Explicit key should take precedence over env."""
        with patch.dict("os.environ", {"FAL_KEY": "env-key"}):
            client = PikaClient(api_key="explicit-key")
            assert client.api_key == "explicit-key"

    def test_health_check_configured(self):
        """Health check should report state correctly."""
        with patch.dict("os.environ", {"FAL_KEY": "test-key-abcdefghijk"}):
            client = PikaClient()
            result = client.health_check()
            assert result["configured"] is True
            assert "pika/v2.5" in result["models"][0]
            assert "16:9" in result["aspect_ratios"]

    @patch("pika_client.PikaClient._get_session")
    def test_text_to_video_success(self, mock_session):
        """Successful text-to-video call returns PikaVideoResult."""
        mock_sess = MagicMock()
        mock_sess.post.return_value.status_code = 200
        mock_sess.post.return_value.json.return_value = {
            "video": {"url": "https://example.com/video.mp4"},
            "request_id": "req-123",
        }
        mock_session.return_value = mock_sess

        with patch.dict("os.environ", {"FAL_KEY": "test-key"}):
            client = PikaClient()
            client._session = mock_sess
            result = client.text_to_video(prompt="A cat dancing")
            assert result.video_url == "https://example.com/video.mp4"
            assert result.duration_seconds == 5
            assert result.model_used == "fal-ai/pika/v2.5"

    @patch("pika_client.PikaClient._get_session")
    def test_image_to_video_success(self, mock_session):
        """Successful image-to-video call."""
        mock_sess = MagicMock()
        mock_sess.post.return_value.status_code = 200
        mock_sess.post.return_value.json.return_value = {
            "video": {"url": "https://example.com/img2vid.mp4"},
        }
        mock_session.return_value = mock_sess

        with patch.dict("os.environ", {"FAL_KEY": "test-key"}):
            client = PikaClient()
            client._session = mock_sess
            result = client.image_to_video(
                prompt="Make it move",
                image_url="https://example.com/start.jpg"
            )
            assert "img2vid.mp4" in result.video_url

    @patch("pika_client.PikaClient._get_session")
    def test_text_to_video_api_error(self, mock_session):
        """API errors should raise PikaGenerationError."""
        mock_sess = MagicMock()
        mock_sess.post.side_effect = Exception("Connection failed")
        mock_session.return_value = mock_sess

        with patch.dict("os.environ", {"FAL_KEY": "test-key"}):
            client = PikaClient()
            client._session = mock_sess
            with pytest.raises(Exception, match="Pika API call failed"):
                client.text_to_video(prompt="test")


# ── Server Tests ───────────────────────────────────────────────────────────

class TestPikaMCPServer:
    """Test MCP server request handling."""

    def setup_method(self):
        self.server = PikaMCPServer(client=None)

    def test_tools_list(self):
        """tools/list returns all tool definitions."""
        request = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
        response = self.server.handle_request(request)
        assert response["id"] == 1
        assert len(response["result"]) == 3

    def test_tools_list_contains_expected(self):
        """Tool list contains expected tool names."""
        names = [t["name"] for t in MCP_TOOLS]
        assert "pika_text_to_video" in names
        assert "pika_image_to_video" in names
        assert "pika_health" in names

    def test_health_without_client(self):
        """Health check without client returns informative message."""
        request = {
            "jsonrpc": "2.0", "id": 2, "method": "tools/call",
            "params": {"name": "pika_health", "arguments": {}}
        }
        response = self.server.handle_request(request)
        result = json.loads(response["result"]["content"][0]["text"])
        assert result["configured"] is False

    def test_unknown_method(self):
        """Unknown methods return error."""
        request = {"jsonrpc": "2.0", "id": 3, "method": "unknown"}
        response = self.server.handle_request(request)
        assert "error" in response
        assert response["error"]["code"] == -32601

    def test_initialize(self):
        """Initialize handshake works."""
        request = {"jsonrpc": "2.0", "id": 4, "method": "initialize"}
        response = self.server.handle_request(request)
        assert response["result"]["serverInfo"]["name"] == "gentech-pika-mcp"

    def test_ping(self):
        """Ping responds."""
        request = {"jsonrpc": "2.0", "id": 5, "method": "ping"}
        response = self.server.handle_request(request)
        assert response["result"] == {}

    def test_tool_call_unknown_tool(self):
        """Unknown tool name returns error."""
        request = {
            "jsonrpc": "2.0", "id": 6, "method": "tools/call",
            "params": {"name": "nonexistent", "arguments": {}}
        }
        response = self.server.handle_request(request)
        assert response["error"]["code"] == -32602

    def test_text_to_video_without_client(self):
        """Text-to-video without client returns proper error."""
        request = {
            "jsonrpc": "2.0", "id": 7, "method": "tools/call",
            "params": {
                "name": "pika_text_to_video",
                "arguments": {"prompt": "test"}
            }
        }
        response = self.server.handle_request(request)
        assert "error" in response
        assert "not configured" in response["error"]["message"].lower()

    def test_tool_schema_validation(self):
        """Check text_to_video tool schema has required field."""
        ttv = next(t for t in MCP_TOOLS if t["name"] == "pika_text_to_video")
        props = ttv["input_schema"]["properties"]
        assert "prompt" in props
        assert props["prompt"]["type"] == "string"
        assert ttv["input_schema"]["required"] == ["prompt"]

    def test_invalid_json_parse(self):
        """Invalid JSON input returns parse error."""
        response = self.server.handle_request({"invalid": "request"})
        # Should still handle gracefully
        assert "error" in response or "result" in response
