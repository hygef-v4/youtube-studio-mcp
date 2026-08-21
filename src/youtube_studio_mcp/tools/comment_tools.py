"""Comment and community moderation tool schemas."""

from typing import Any

COMMENT_TOOLS: list[dict[str, Any]] = [
    {
        "name": "youtube_list_comments",
        "description": "List top-level comment threads on a YouTube video.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "video_id": {"type": "string"},
                "max_results": {"type": "integer", "minimum": 1, "maximum": 100, "default": 20},
            },
            "required": ["video_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_post_comment",
        "description": "Post a top-level comment on one of your YouTube videos.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "video_id": {"type": "string"},
                "text": {"type": "string"},
            },
            "required": ["video_id", "text"],
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_reply_comment",
        "description": "Reply directly to an existing comment on a video.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "parent_id": {"type": "string", "description": "ID of the parent comment being replied to"},
                "text": {"type": "string", "description": "Reply text"},
            },
            "required": ["parent_id", "text"],
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_delete_comment",
        "description": "Delete a comment by its ID.",
        "inputSchema": {
            "type": "object",
            "properties": {"comment_id": {"type": "string"}},
            "required": ["comment_id"],
            "additionalProperties": False,
        },
    },
]
