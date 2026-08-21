"""Unit tests for YouTube Studio MCP Server."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Ensure src/ is on sys.path
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from youtube_studio_mcp.auth import AuthConfig
from youtube_studio_mcp.client import YouTubeClient
from youtube_studio_mcp.server import McpServer


class TestAuthConfig(unittest.TestCase):
    def test_auth_status_paths(self) -> None:
        auth = AuthConfig(
            client_secrets_path=Path("secrets/client_secret.json"),
            token_path=Path("secrets/token.json"),
        )
        status = auth.auth_status()
        self.assertIn("client_secrets_exists", status)
        self.assertIn("token_exists", status)
        self.assertIn("client_secrets_path", status)
        self.assertIn("token_path", status)


class TestMcpServerRegistry(unittest.TestCase):
    def setUp(self) -> None:
        self.server = McpServer()

    def test_total_registered_tools(self) -> None:
        self.assertEqual(len(self.server.tools), 32)

    def test_tool_names_exist(self) -> None:
        expected_tools = {
            "youtube_auth_status",
            "youtube_start_auth",
            "youtube_channel_overview",
            "youtube_list_videos",
            "youtube_get_video",
            "youtube_update_video",
            "youtube_delete_video",
            "youtube_upload_thumbnail",
            "youtube_upload_video",
            "youtube_list_playlists",
            "youtube_get_playlist",
            "youtube_create_playlist",
            "youtube_update_playlist",
            "youtube_delete_playlist",
            "youtube_add_to_playlist",
            "youtube_remove_from_playlist",
            "youtube_list_comments",
            "youtube_post_comment",
            "youtube_reply_comment",
            "youtube_delete_comment",
            "youtube_channel_analytics",
            "youtube_video_analytics",
            "youtube_analytics_traffic_sources",
            "youtube_analytics_demographics",
            "youtube_analytics_top_videos",
            "youtube_search_videos",
            "youtube_search_channels",
            "youtube_list_captions",
            "youtube_get_transcript",
            "youtube_bulk_get_transcripts",
            "youtube_download_caption",
            "youtube_delete_caption",
        }
        actual_tools = {tool["name"] for tool in self.server.tools}
        self.assertEqual(expected_tools, actual_tools)

    def test_all_tools_have_input_schema(self) -> None:
        for tool in self.server.tools:
            self.assertIn("inputSchema", tool)
            self.assertEqual(tool["inputSchema"]["type"], "object")
            self.assertIn("description", tool)


class TestYouTubeClientMocked(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_auth = MagicMock(spec=AuthConfig)
        self.client = YouTubeClient(self.mock_auth)

    @patch("youtube_studio_mcp.client.http_json")
    def test_channel_overview_request(self, mock_http_json: MagicMock) -> None:
        mock_http_json.return_value = {"items": [{"id": "UC123"}]}
        with patch.object(self.client, "_access_token", return_value="test_token"):
            result = self.client.channel_overview()
            self.assertEqual(result["items"][0]["id"], "UC123")
            mock_http_json.assert_called_once()


if __name__ == "__main__":
    unittest.main()
