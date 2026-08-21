"""Tool schema registry for YouTube Studio MCP."""

from typing import Any

from youtube_studio_mcp.tools.analytics_tools import ANALYTICS_TOOLS
from youtube_studio_mcp.tools.auth_tools import AUTH_TOOLS
from youtube_studio_mcp.tools.caption_tools import CAPTION_TOOLS
from youtube_studio_mcp.tools.comment_tools import COMMENT_TOOLS
from youtube_studio_mcp.tools.playlist_tools import PLAYLIST_TOOLS
from youtube_studio_mcp.tools.search_tools import SEARCH_TOOLS
from youtube_studio_mcp.tools.video_tools import VIDEO_TOOLS

ALL_TOOLS: list[dict[str, Any]] = (
    AUTH_TOOLS
    + VIDEO_TOOLS
    + PLAYLIST_TOOLS
    + COMMENT_TOOLS
    + ANALYTICS_TOOLS
    + SEARCH_TOOLS
    + CAPTION_TOOLS
)

__all__ = [
    "ALL_TOOLS",
    "AUTH_TOOLS",
    "VIDEO_TOOLS",
    "PLAYLIST_TOOLS",
    "COMMENT_TOOLS",
    "ANALYTICS_TOOLS",
    "SEARCH_TOOLS",
    "CAPTION_TOOLS",
]
