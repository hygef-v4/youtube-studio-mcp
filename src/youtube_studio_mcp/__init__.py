"""YouTube Studio MCP - High-performance, dependency-free Model Context Protocol server."""

from youtube_studio_mcp.auth import AuthConfig, run_auth
from youtube_studio_mcp.client import YouTubeClient
from youtube_studio_mcp.constants import PROTOCOL_VERSION, SERVER_NAME, SERVER_VERSION
from youtube_studio_mcp.server import McpServer
from youtube_studio_mcp.tools import ALL_TOOLS

__version__ = SERVER_VERSION
__all__ = [
    "ALL_TOOLS",
    "AuthConfig",
    "McpServer",
    "PROTOCOL_VERSION",
    "SERVER_NAME",
    "SERVER_VERSION",
    "YouTubeClient",
    "run_auth",
]
