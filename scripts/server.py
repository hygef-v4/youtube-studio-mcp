#!/usr/bin/env python
"""Launcher script for YouTube Studio MCP server.

Imports the modular implementation from src/youtube_studio_mcp.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure src/ is on Python search path
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from youtube_studio_mcp.auth import AuthConfig
from youtube_studio_mcp.client import YouTubeClient
from youtube_studio_mcp.constants import (
    AUTH_URL,
    PROTOCOL_VERSION,
    REDIRECT_URI,
    SCOPES,
    SERVER_NAME,
    SERVER_VERSION,
    TOKEN_URL,
    YOUTUBE_ANALYTICS_BASE,
    YOUTUBE_API_BASE,
    YOUTUBE_UPLOAD_BASE,
)
from youtube_studio_mcp.http import abs_path, http_json, http_raw
from youtube_studio_mcp.server import McpServer, main
from youtube_studio_mcp.tools import ALL_TOOLS

if __name__ == "__main__":
    main()
