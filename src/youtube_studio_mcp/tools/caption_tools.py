"""Caption, subtitle, and transcript tool schemas."""

from typing import Any

CAPTION_TOOLS: list[dict[str, Any]] = [
    {
        "name": "youtube_list_captions",
        "description": "List existing caption/subtitle tracks for a video.",
        "inputSchema": {
            "type": "object",
            "properties": {"video_id": {"type": "string"}},
            "required": ["video_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_get_transcript",
        "description": "Extract the full spoken transcript, summary-ready text, or timestamped segments from a video.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "video_id": {"type": "string", "description": "YouTube video ID"},
                "language": {"type": "string", "description": "Language code (e.g. 'vi', 'en'). Defaults to first available track."},
                "output_format": {"type": "string", "enum": ["text", "srt", "segments"], "default": "text", "description": "Format of output: 'text' (continuous plain text), 'srt' (raw SRT), or 'segments' (list of timestamps and text)"},
            },
            "required": ["video_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_bulk_get_transcripts",
        "description": "Bulk extract transcripts from a list of video IDs, an entire playlist, or recent uploads. Can optionally save directly to local files.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "video_ids": {"type": "array", "items": {"type": "string"}, "description": "List of YouTube video IDs"},
                "playlist_id": {"type": "string", "description": "Playlist ID to extract transcripts from all videos inside"},
                "max_videos": {"type": "integer", "minimum": 1, "maximum": 50, "default": 10},
                "language": {"type": "string", "description": "Preferred language code (e.g. 'vi', 'en')"},
                "output_format": {"type": "string", "enum": ["text", "srt"], "default": "text"},
                "output_dir": {"type": "string", "description": "Optional local folder path to save transcript files (.txt or .srt)"},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_download_caption",
        "description": "Download raw caption file (SRT, VTT, SBV) by caption ID.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "caption_id": {"type": "string", "description": "Unique caption track ID"},
                "fmt": {"type": "string", "enum": ["srt", "vtt", "sbv"], "default": "srt"},
            },
            "required": ["caption_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "youtube_delete_caption",
        "description": "Delete a caption track by its caption ID.",
        "inputSchema": {
            "type": "object",
            "properties": {"caption_id": {"type": "string"}},
            "required": ["caption_id"],
            "additionalProperties": False,
        },
    },
]
