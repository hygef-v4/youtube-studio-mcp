"""YouTube Search and discovery tool schemas."""

from typing import Any

SEARCH_TOOLS: list[dict[str, Any]] = [
    {
        "name": "youtube_search_videos",
        "description": "Search YouTube videos by keywords to analyze competitor titles, tags, and views.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search terms"},
                "max_results": {"type": "integer", "minimum": 1, "maximum": 50, "default": 10},
                "order": {"type": "string", "enum": ["relevance", "date", "viewCount", "rating"], "default": "relevance"},
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_search_channels",
        "description": "Search YouTube channels by topic or keyword.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "max_results": {"type": "integer", "minimum": 1, "maximum": 50, "default": 10},
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
]
