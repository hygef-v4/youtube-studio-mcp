"""Authentication tool schemas for YouTube Studio MCP."""

from typing import Any

AUTH_TOOLS: list[dict[str, Any]] = [
    {
        "name": "youtube_auth_status",
        "description": "Show whether YouTube OAuth credentials and tokens are configured.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "youtube_start_auth",
        "description": "Generate the OAuth authorization URL and local auth command.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
]
