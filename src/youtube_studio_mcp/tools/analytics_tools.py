"""YouTube Analytics reporting tool schemas."""

from typing import Any

ANALYTICS_TOOLS: list[dict[str, Any]] = [
    {
        "name": "youtube_channel_analytics",
        "description": "Return channel-level analytics (views, watch time, retention, subs) for a date range.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "start_date": {"type": "string", "description": "YYYY-MM-DD"},
                "end_date": {"type": "string", "description": "YYYY-MM-DD"},
            },
            "required": ["start_date", "end_date"],
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_video_analytics",
        "description": "Return per-day analytics for one video across a date range.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "video_id": {"type": "string"},
                "start_date": {"type": "string", "description": "YYYY-MM-DD"},
                "end_date": {"type": "string", "description": "YYYY-MM-DD"},
            },
            "required": ["video_id", "start_date", "end_date"],
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_analytics_traffic_sources",
        "description": "Return traffic source breakdown (Search, Suggested, Browse, External) for a date range.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "start_date": {"type": "string", "description": "YYYY-MM-DD"},
                "end_date": {"type": "string", "description": "YYYY-MM-DD"},
            },
            "required": ["start_date", "end_date"],
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_analytics_demographics",
        "description": "Return viewer age group, gender, or country distribution percentages.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "start_date": {"type": "string", "description": "YYYY-MM-DD"},
                "end_date": {"type": "string", "description": "YYYY-MM-DD"},
                "dimension": {"type": "string", "enum": ["ageGroup,gender", "country"], "default": "ageGroup,gender"},
            },
            "required": ["start_date", "end_date"],
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_analytics_top_videos",
        "description": "Return top performing videos by view count and watch time for a date range.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "start_date": {"type": "string", "description": "YYYY-MM-DD"},
                "end_date": {"type": "string", "description": "YYYY-MM-DD"},
                "max_results": {"type": "integer", "minimum": 1, "maximum": 50, "default": 10},
            },
            "required": ["start_date", "end_date"],
            "additionalProperties": False,
        },
    },
]
