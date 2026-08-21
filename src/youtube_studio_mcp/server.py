"""Stdio JSON-RPC 2.0 Model Context Protocol (MCP) server for YouTube Studio."""

from __future__ import annotations

import json
import os
import secrets
import sys
import urllib.parse
from pathlib import Path
from typing import Any

from youtube_studio_mcp.auth import AuthConfig
from youtube_studio_mcp.client import YouTubeClient
from youtube_studio_mcp.constants import (
    AUTH_URL,
    PROTOCOL_VERSION,
    REDIRECT_URI,
    SCOPES,
    SERVER_NAME,
    SERVER_VERSION,
)
from youtube_studio_mcp.http import abs_path
from youtube_studio_mcp.tools import ALL_TOOLS


def text_content(text: str) -> dict[str, Any]:
    return {"type": "text", "text": text}


class McpServer:
    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = base_dir or Path.cwd()
        client_secrets = os.environ.get("YOUTUBE_CLIENT_SECRETS", "secrets/client_secret.json")
        token_file = os.environ.get("YOUTUBE_TOKEN_FILE", "secrets/token.json")
        self.auth = AuthConfig(
            client_secrets_path=abs_path(client_secrets, self.base_dir),
            token_path=abs_path(token_file, self.base_dir),
        )
        self.youtube = YouTubeClient(self.auth)
        self.tools = ALL_TOOLS

    def _start_auth_payload(self) -> dict[str, Any]:
        status = self.auth.auth_status()
        if not status["client_secrets_exists"]:
            raise RuntimeError(
                "client_secret.json is missing. Add your Google OAuth desktop client JSON first."
            )
        client = self.auth.load_client_config()
        state = secrets.token_urlsafe(24)
        params = urllib.parse.urlencode(
            {
                "client_id": client["client_id"],
                "redirect_uri": REDIRECT_URI,
                "response_type": "code",
                "scope": " ".join(SCOPES),
                "access_type": "offline",
                "prompt": "consent",
                "state": state,
            }
        )
        helper_cmd = "python scripts/auth.py auth"
        return {
            "authorization_url": f"{AUTH_URL}?{params}",
            "token_path": status["token_path"],
            "client_secrets_path": status["client_secrets_path"],
            "helper_command": helper_cmd,
            "redirect_uri": REDIRECT_URI,
        }

    def _call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        # 1. Auth
        if name == "youtube_auth_status":
            return self.auth.auth_status()
        if name == "youtube_start_auth":
            return self._start_auth_payload()

        # 2. Channel & Video CRUD
        if name == "youtube_channel_overview":
            return self.youtube.channel_overview()
        if name == "youtube_list_videos":
            return self.youtube.list_videos(
                int(arguments.get("max_results", 10)), arguments.get("page_token")
            )
        if name == "youtube_get_video":
            return self.youtube.get_video(arguments["video_id"])
        if name == "youtube_update_video":
            return self.youtube.update_video(
                arguments["video_id"],
                title=arguments.get("title"),
                description=arguments.get("description"),
                tags=arguments.get("tags"),
                category_id=arguments.get("category_id"),
                default_language=arguments.get("default_language"),
                privacy_status=arguments.get("privacy_status"),
            )
        if name == "youtube_delete_video":
            return self.youtube.delete_video(arguments["video_id"])
        if name == "youtube_upload_thumbnail":
            return self.youtube.upload_thumbnail(arguments["video_id"], arguments["image_path"])
        if name == "youtube_upload_video":
            return self.youtube.upload_video(
                arguments["video_path"],
                arguments["title"],
                description=arguments.get("description", ""),
                tags=arguments.get("tags"),
                category_id=arguments.get("category_id", "20"),
                privacy_status=arguments.get("privacy_status", "private"),
                made_for_kids=arguments.get("made_for_kids", False),
            )

        # 3. Playlists
        if name == "youtube_list_playlists":
            return self.youtube.list_playlists(
                int(arguments.get("max_results", 25)), arguments.get("page_token")
            )
        if name == "youtube_get_playlist":
            return self.youtube.get_playlist(
                arguments["playlist_id"],
                int(arguments.get("max_results", 25)),
                arguments.get("page_token"),
            )
        if name == "youtube_create_playlist":
            return self.youtube.create_playlist(
                arguments["title"],
                description=arguments.get("description", ""),
                privacy_status=arguments.get("privacy_status", "public"),
            )
        if name == "youtube_update_playlist":
            return self.youtube.update_playlist(
                arguments["playlist_id"],
                title=arguments.get("title"),
                description=arguments.get("description"),
                privacy_status=arguments.get("privacy_status"),
            )
        if name == "youtube_delete_playlist":
            return self.youtube.delete_playlist(arguments["playlist_id"])
        if name == "youtube_add_to_playlist":
            return self.youtube.add_to_playlist(
                arguments["playlist_id"],
                arguments["video_id"],
                arguments.get("position"),
            )
        if name == "youtube_remove_from_playlist":
            return self.youtube.remove_from_playlist(arguments["playlist_item_id"])

        # 4. Comments
        if name == "youtube_list_comments":
            return self.youtube.list_comments(
                arguments["video_id"], int(arguments.get("max_results", 20))
            )
        if name == "youtube_post_comment":
            return self.youtube.post_comment(arguments["video_id"], arguments["text"])
        if name == "youtube_reply_comment":
            return self.youtube.reply_comment(arguments["parent_id"], arguments["text"])
        if name == "youtube_delete_comment":
            return self.youtube.delete_comment(arguments["comment_id"])

        # 5. Analytics
        if name == "youtube_channel_analytics":
            return self.youtube.channel_analytics(arguments["start_date"], arguments["end_date"])
        if name == "youtube_video_analytics":
            return self.youtube.video_analytics(
                arguments["video_id"], arguments["start_date"], arguments["end_date"]
            )
        if name == "youtube_analytics_traffic_sources":
            return self.youtube.analytics_traffic_sources(
                arguments["start_date"], arguments["end_date"]
            )
        if name == "youtube_analytics_demographics":
            return self.youtube.analytics_demographics(
                arguments["start_date"],
                arguments["end_date"],
                arguments.get("dimension", "ageGroup,gender"),
            )
        if name == "youtube_analytics_top_videos":
            return self.youtube.analytics_top_videos(
                arguments["start_date"],
                arguments["end_date"],
                int(arguments.get("max_results", 10)),
            )

        # 6. Search
        if name == "youtube_search_videos":
            return self.youtube.search_videos(
                arguments["query"],
                int(arguments.get("max_results", 10)),
                arguments.get("order", "relevance"),
            )
        if name == "youtube_search_channels":
            return self.youtube.search_channels(
                arguments["query"], int(arguments.get("max_results", 10))
            )

        # 7. Captions & Transcripts
        if name == "youtube_list_captions":
            return self.youtube.list_captions(arguments["video_id"])
        if name == "youtube_get_transcript":
            return self.youtube.get_transcript(
                arguments["video_id"],
                language=arguments.get("language"),
                output_format=arguments.get("output_format", "text"),
            )
        if name == "youtube_bulk_get_transcripts":
            return self.youtube.bulk_get_transcripts(
                video_ids=arguments.get("video_ids"),
                playlist_id=arguments.get("playlist_id"),
                max_videos=int(arguments.get("max_videos", 10)),
                language=arguments.get("language"),
                output_format=arguments.get("output_format", "text"),
                output_dir=arguments.get("output_dir"),
            )
        if name == "youtube_download_caption":
            return self.youtube.download_caption(
                arguments["caption_id"],
                fmt=arguments.get("fmt", "srt"),
            )
        if name == "youtube_delete_caption":
            return self.youtube.delete_caption(arguments["caption_id"])

        raise RuntimeError(f"Unknown tool: {name}")

    @staticmethod
    def _read_message() -> dict[str, Any] | None:
        headers: dict[str, str] = {}
        while True:
            line = sys.stdin.buffer.readline()
            if not line:
                return None
            if line == b"\r\n":
                break
            key, _, value = line.decode("utf-8").partition(":")
            headers[key.strip().lower()] = value.strip()
        length = int(headers.get("content-length", "0"))
        if length <= 0:
            return None
        body = sys.stdin.buffer.read(length)
        return json.loads(body.decode("utf-8"))

    @staticmethod
    def _write_message(payload: dict[str, Any]) -> None:
        encoded = json.dumps(payload).encode("utf-8")
        sys.stdout.buffer.write(f"Content-Length: {len(encoded)}\r\n\r\n".encode("utf-8"))
        sys.stdout.buffer.write(encoded)
        sys.stdout.buffer.flush()

    def _success(self, message_id: Any, result: dict[str, Any]) -> None:
        self._write_message({"jsonrpc": "2.0", "id": message_id, "result": result})

    def _error(self, message_id: Any, code: int, message: str) -> None:
        self._write_message(
            {
                "jsonrpc": "2.0",
                "id": message_id,
                "error": {"code": code, "message": message},
            }
        )

    def serve(self) -> None:
        while True:
            message = self._read_message()
            if message is None:
                return
            message_id = message.get("id")
            method = message.get("method")
            try:
                if method == "initialize":
                    self._success(
                        message_id,
                        {
                            "protocolVersion": PROTOCOL_VERSION,
                            "capabilities": {"tools": {}},
                            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                        },
                    )
                elif method == "notifications/initialized":
                    continue
                elif method == "ping":
                    self._success(message_id, {})
                elif method == "tools/list":
                    self._success(message_id, {"tools": self.tools})
                elif method == "tools/call":
                    params = message.get("params", {})
                    result = self._call_tool(params["name"], params.get("arguments", {}))
                    self._success(message_id, {"content": [text_content(json.dumps(result, indent=2))]})
                else:
                    self._error(message_id, -32601, f"Method not found: {method}")
            except Exception as exc:  # noqa: BLE001
                self._error(message_id, -32000, str(exc))


def main() -> None:
    McpServer().serve()


if __name__ == "__main__":
    main()
