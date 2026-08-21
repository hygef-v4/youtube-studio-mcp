"""Playlist management tool schemas."""

from typing import Any

PLAYLIST_TOOLS: list[dict[str, Any]] = [
    {
        "name": "youtube_list_playlists",
        "description": "List all playlists on the authenticated YouTube channel.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "max_results": {"type": "integer", "minimum": 1, "maximum": 50, "default": 25},
                "page_token": {"type": "string"},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_get_playlist",
        "description": "Get all videos contained inside a specific playlist.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "playlist_id": {"type": "string"},
                "max_results": {"type": "integer", "minimum": 1, "maximum": 50, "default": 25},
                "page_token": {"type": "string"},
            },
            "required": ["playlist_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_create_playlist",
        "description": "Create a new playlist on your channel.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "privacy_status": {"type": "string", "enum": ["public", "private", "unlisted"], "default": "public"},
            },
            "required": ["title"],
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_update_playlist",
        "description": "Update title, description, or privacy of an existing playlist.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "playlist_id": {"type": "string"},
                "title": {"type": "string"},
                "description": {"type": "string"},
                "privacy_status": {"type": "string", "enum": ["public", "private", "unlisted"]},
            },
            "required": ["playlist_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_delete_playlist",
        "description": "Delete a playlist from your YouTube channel.",
        "inputSchema": {
            "type": "object",
            "properties": {"playlist_id": {"type": "string"}},
            "required": ["playlist_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_add_to_playlist",
        "description": "Add a video to a specific playlist.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "playlist_id": {"type": "string"},
                "video_id": {"type": "string"},
                "position": {"type": "integer", "description": "0-based position index in playlist"},
            },
            "required": ["playlist_id", "video_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_remove_from_playlist",
        "description": "Remove an item from a playlist using its playlist item ID.",
        "inputSchema": {
            "type": "object",
            "properties": {"playlist_item_id": {"type": "string"}},
            "required": ["playlist_item_id"],
            "additionalProperties": False,
        },
    },
]
