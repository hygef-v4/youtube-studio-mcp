"""Video and media management tool schemas."""

from typing import Any

VIDEO_TOOLS: list[dict[str, Any]] = [
    {
        "name": "youtube_channel_overview",
        "description": "Fetch the authenticated YouTube channel profile, branding, and public statistics.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "youtube_list_videos",
        "description": "List recent channel videos with merged metadata, details, and statistics.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "max_results": {"type": "integer", "minimum": 1, "maximum": 50, "default": 10},
                "page_token": {"type": "string"},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_get_video",
        "description": "Fetch detailed metadata, statistics, and status for a single YouTube video.",
        "inputSchema": {
            "type": "object",
            "properties": {"video_id": {"type": "string"}},
            "required": ["video_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_update_video",
        "description": "Update video title, description, tags list, category, language, or privacy status.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "video_id": {"type": "string"},
                "title": {"type": "string"},
                "description": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}},
                "category_id": {"type": "string"},
                "default_language": {"type": "string"},
                "privacy_status": {"type": "string", "enum": ["public", "private", "unlisted"]},
            },
            "required": ["video_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_delete_video",
        "description": "Permanently delete a YouTube video from your channel.",
        "inputSchema": {
            "type": "object",
            "properties": {"video_id": {"type": "string"}},
            "required": ["video_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_upload_thumbnail",
        "description": "Upload a new custom thumbnail for a video from a local image file path.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "video_id": {"type": "string"},
                "image_path": {"type": "string"},
            },
            "required": ["video_id", "image_path"],
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_upload_video",
        "description": "Upload a local video file (.mp4, .mov, .mkv) to YouTube via resumable upload.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "video_path": {"type": "string", "description": "Absolute or relative path to local video file"},
                "title": {"type": "string", "description": "Video title"},
                "description": {"type": "string", "description": "Video description"},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "List of SEO tags"},
                "category_id": {"type": "string", "default": "20", "description": "YouTube Category ID (e.g. 20=Gaming, 22=People & Blogs, 27=Education, 28=Sci & Tech)"},
                "privacy_status": {"type": "string", "enum": ["private", "unlisted", "public"], "default": "private"},
                "made_for_kids": {"type": "boolean", "default": False},
            },
            "required": ["video_path", "title"],
            "additionalProperties": False,
        },
    },
]
