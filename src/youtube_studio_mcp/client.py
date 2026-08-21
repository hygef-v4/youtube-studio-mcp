"""High-performance YouTube Data API v3 and Analytics API v2 client."""

from __future__ import annotations

import json
import mimetypes
import re
import time
import urllib.parse
from typing import Any

from youtube_studio_mcp.auth import AuthConfig
from youtube_studio_mcp.constants import (
    TOKEN_URL,
    YOUTUBE_API_BASE,
    YOUTUBE_ANALYTICS_BASE,
    YOUTUBE_UPLOAD_BASE,
)
from youtube_studio_mcp.http import abs_path, http_json, http_raw


class YouTubeClient:
    def __init__(self, auth: AuthConfig):
        self.auth = auth

    def _refresh_token(self, token: dict[str, Any]) -> dict[str, Any]:
        client = self.auth.load_client_config()
        refresh_token = token.get("refresh_token")
        if not refresh_token:
            raise RuntimeError("Token file does not contain a refresh_token.")
        payload = urllib.parse.urlencode(
            {
                "client_id": client["client_id"],
                "client_secret": client.get("client_secret", ""),
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
            }
        ).encode("utf-8")
        refreshed = http_json(
            TOKEN_URL,
            method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=payload,
        )
        refreshed["refresh_token"] = refresh_token
        refreshed["created_at"] = int(time.time())
        self.auth.save_token(refreshed)
        return refreshed

    def _access_token(self) -> str:
        token = self.auth.load_token()
        expires_in = int(token.get("expires_in", 0))
        created_at = int(token.get("created_at", 0))
        if not token.get("access_token"):
            raise RuntimeError("Token file is missing access_token.")
        if created_at + max(expires_in - 120, 0) <= int(time.time()):
            token = self._refresh_token(token)
        return token["access_token"]

    def _request(
        self,
        base_url: str,
        path: str,
        *,
        method: str = "GET",
        query: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        raw_data: bytes | None = None,
        timeout: int = 60,
    ) -> dict[str, Any]:
        query_string = ""
        if query:
            cleaned = {key: value for key, value in query.items() if value is not None}
            query_string = "?" + urllib.parse.urlencode(cleaned, doseq=True)
        url = f"{base_url}{path}{query_string}"
        request_headers = {
            "Authorization": f"Bearer {self._access_token()}",
        }
        if headers:
            request_headers.update(headers)
        data = raw_data
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            request_headers["Content-Type"] = "application/json"
        return http_json(url, method=method, headers=request_headers, data=data, timeout=timeout)

    # -------------------------------------------------------------------------
    # Channel & Videos
    # -------------------------------------------------------------------------

    def channel_overview(self) -> dict[str, Any]:
        return self._request(
            YOUTUBE_API_BASE,
            "/channels",
            query={"part": "snippet,statistics,brandingSettings,contentDetails", "mine": "true"},
        )

    def list_videos(self, max_results: int = 10, page_token: str | None = None) -> dict[str, Any]:
        channel = self.channel_overview()
        channels = channel.get("items", [])
        if not channels:
            raise RuntimeError("No authenticated YouTube channel was returned.")
        uploads_playlist = (
            channels[0].get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
        )
        if not uploads_playlist:
            raise RuntimeError("Could not find the uploads playlist for the authenticated channel.")
        playlist = self._request(
            YOUTUBE_API_BASE,
            "/playlistItems",
            query={
                "part": "snippet,contentDetails,status",
                "playlistId": uploads_playlist,
                "maxResults": max(1, min(max_results, 50)),
                "pageToken": page_token,
            },
        )
        video_ids = [
            item.get("contentDetails", {}).get("videoId")
            for item in playlist.get("items", [])
            if item.get("contentDetails", {}).get("videoId")
        ]
        details = {}
        if video_ids:
            details_response = self._request(
                YOUTUBE_API_BASE,
                "/videos",
                query={
                    "part": "snippet,statistics,status,contentDetails",
                    "id": ",".join(video_ids),
                },
            )
            details = {item["id"]: item for item in details_response.get("items", [])}
        merged = []
        for item in playlist.get("items", []):
            video_id = item.get("contentDetails", {}).get("videoId")
            merged.append(
                {
                    "playlistItem": item,
                    "details": details.get(video_id),
                }
            )
        return {
            "items": merged,
            "nextPageToken": playlist.get("nextPageToken"),
            "pageInfo": playlist.get("pageInfo", {}),
        }

    def get_video(self, video_id: str) -> dict[str, Any]:
        result = self._request(
            YOUTUBE_API_BASE,
            "/videos",
            query={"part": "snippet,statistics,status,contentDetails", "id": video_id},
        )
        items = result.get("items", [])
        if not items:
            raise RuntimeError(f"Video {video_id} not found.")
        return items[0]

    def update_video(
        self,
        video_id: str,
        *,
        title: str | None = None,
        description: str | None = None,
        tags: list[str] | None = None,
        category_id: str | None = None,
        default_language: str | None = None,
        privacy_status: str | None = None,
    ) -> dict[str, Any]:
        existing = self.get_video(video_id)
        snippet = existing["snippet"]
        status = existing["status"]
        if title is not None:
            snippet["title"] = title
        if description is not None:
            snippet["description"] = description
        if tags is not None:
            snippet["tags"] = tags
        if category_id is not None:
            snippet["categoryId"] = category_id
        if default_language is not None:
            snippet["defaultLanguage"] = default_language
        if privacy_status is not None:
            status["privacyStatus"] = privacy_status
        body = {
            "id": video_id,
            "snippet": snippet,
            "status": status,
        }
        return self._request(
            YOUTUBE_API_BASE,
            "/videos",
            method="PUT",
            query={"part": "snippet,status"},
            body=body,
        )

    def delete_video(self, video_id: str) -> dict[str, Any]:
        return self._request(
            YOUTUBE_API_BASE,
            "/videos",
            method="DELETE",
            query={"id": video_id},
        )

    def upload_thumbnail(self, video_id: str, image_path: str) -> dict[str, Any]:
        path = abs_path(image_path)
        if not path.exists():
            raise RuntimeError(f"Thumbnail file not found: {path}")
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        body = path.read_bytes()
        return self._request(
            YOUTUBE_UPLOAD_BASE,
            "/thumbnails/set",
            method="POST",
            query={"videoId": video_id, "uploadType": "media"},
            headers={"Content-Type": mime},
            raw_data=body,
            timeout=120,
        )

    def upload_video(
        self,
        video_path: str,
        title: str,
        *,
        description: str = "",
        tags: list[str] | None = None,
        category_id: str = "20",
        privacy_status: str = "private",
        made_for_kids: bool = False,
    ) -> dict[str, Any]:
        path = abs_path(video_path)
        if not path.exists():
            raise RuntimeError(f"Video file not found: {path}")
        file_size = path.stat().st_size
        mime = mimetypes.guess_type(path.name)[0] or "video/mp4"

        metadata = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags or [],
                "categoryId": category_id,
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": made_for_kids,
            },
        }
        init_headers = {
            "Authorization": f"Bearer {self._access_token()}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Type": mime,
            "X-Upload-Content-Length": str(file_size),
        }
        status, resp_headers, _ = http_raw(
            f"{YOUTUBE_UPLOAD_BASE}/videos?uploadType=resumable&part=snippet,status",
            method="POST",
            headers=init_headers,
            data=json.dumps(metadata).encode("utf-8"),
        )
        upload_url = resp_headers.get("location")
        if not upload_url:
            raise RuntimeError("Failed to initiate resumable video upload session.")

        video_bytes = path.read_bytes()
        upload_headers = {
            "Authorization": f"Bearer {self._access_token()}",
            "Content-Type": mime,
            "Content-Length": str(file_size),
        }
        status, _, resp_body = http_raw(
            upload_url,
            method="PUT",
            headers=upload_headers,
            data=video_bytes,
            timeout=600,
        )
        return json.loads(resp_body.decode("utf-8"))

    # -------------------------------------------------------------------------
    # Playlists
    # -------------------------------------------------------------------------

    def list_playlists(self, max_results: int = 25, page_token: str | None = None) -> dict[str, Any]:
        return self._request(
            YOUTUBE_API_BASE,
            "/playlists",
            query={
                "part": "snippet,status,contentDetails",
                "mine": "true",
                "maxResults": max(1, min(max_results, 50)),
                "pageToken": page_token,
            },
        )

    def get_playlist(self, playlist_id: str, max_results: int = 25, page_token: str | None = None) -> dict[str, Any]:
        return self._request(
            YOUTUBE_API_BASE,
            "/playlistItems",
            query={
                "part": "snippet,status,contentDetails",
                "playlistId": playlist_id,
                "maxResults": max(1, min(max_results, 50)),
                "pageToken": page_token,
            },
        )

    def create_playlist(
        self,
        title: str,
        description: str = "",
        privacy_status: str = "public",
    ) -> dict[str, Any]:
        body = {
            "snippet": {"title": title, "description": description},
            "status": {"privacyStatus": privacy_status},
        }
        return self._request(
            YOUTUBE_API_BASE,
            "/playlists",
            method="POST",
            query={"part": "snippet,status"},
            body=body,
        )

    def update_playlist(
        self,
        playlist_id: str,
        *,
        title: str | None = None,
        description: str | None = None,
        privacy_status: str | None = None,
    ) -> dict[str, Any]:
        existing = self._request(
            YOUTUBE_API_BASE,
            "/playlists",
            query={"part": "snippet,status", "id": playlist_id},
        )
        items = existing.get("items", [])
        if not items:
            raise RuntimeError(f"Playlist {playlist_id} not found.")
        snippet = items[0]["snippet"]
        status = items[0]["status"]
        if title is not None:
            snippet["title"] = title
        if description is not None:
            snippet["description"] = description
        if privacy_status is not None:
            status["privacyStatus"] = privacy_status
        body = {
            "id": playlist_id,
            "snippet": snippet,
            "status": status,
        }
        return self._request(
            YOUTUBE_API_BASE,
            "/playlists",
            method="PUT",
            query={"part": "snippet,status"},
            body=body,
        )

    def delete_playlist(self, playlist_id: str) -> dict[str, Any]:
        return self._request(
            YOUTUBE_API_BASE,
            "/playlists",
            method="DELETE",
            query={"id": playlist_id},
        )

    def add_to_playlist(
        self,
        playlist_id: str,
        video_id: str,
        position: int | None = None,
    ) -> dict[str, Any]:
        snippet: dict[str, Any] = {
            "playlistId": playlist_id,
            "resourceId": {"kind": "youtube#video", "videoId": video_id},
        }
        if position is not None:
            snippet["position"] = position
        return self._request(
            YOUTUBE_API_BASE,
            "/playlistItems",
            method="POST",
            query={"part": "snippet"},
            body={"snippet": snippet},
        )

    def remove_from_playlist(self, playlist_item_id: str) -> dict[str, Any]:
        return self._request(
            YOUTUBE_API_BASE,
            "/playlistItems",
            method="DELETE",
            query={"id": playlist_item_id},
        )

    # -------------------------------------------------------------------------
    # Comments & Community
    # -------------------------------------------------------------------------

    def list_comments(self, video_id: str, max_results: int = 20) -> dict[str, Any]:
        return self._request(
            YOUTUBE_API_BASE,
            "/commentThreads",
            query={
                "part": "snippet",
                "videoId": video_id,
                "maxResults": max(1, min(max_results, 100)),
                "order": "relevance",
                "textFormat": "plainText",
            },
        )

    def post_comment(self, video_id: str, text: str) -> dict[str, Any]:
        body = {
            "snippet": {
                "videoId": video_id,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": text,
                    }
                },
            }
        }
        return self._request(
            YOUTUBE_API_BASE,
            "/commentThreads",
            method="POST",
            query={"part": "snippet"},
            body=body,
        )

    def reply_comment(self, parent_id: str, text: str) -> dict[str, Any]:
        body = {
            "snippet": {
                "parentId": parent_id,
                "textOriginal": text,
            }
        }
        return self._request(
            YOUTUBE_API_BASE,
            "/comments",
            method="POST",
            query={"part": "snippet"},
            body=body,
        )

    def delete_comment(self, comment_id: str) -> dict[str, Any]:
        return self._request(
            YOUTUBE_API_BASE,
            "/comments",
            method="DELETE",
            query={"id": comment_id},
        )

    # -------------------------------------------------------------------------
    # Analytics
    # -------------------------------------------------------------------------

    def channel_analytics(self, start_date: str, end_date: str) -> dict[str, Any]:
        return self._request(
            YOUTUBE_ANALYTICS_BASE,
            "/reports",
            query={
                "ids": "channel==MINE",
                "startDate": start_date,
                "endDate": end_date,
                "metrics": ",".join(
                    [
                        "views",
                        "estimatedMinutesWatched",
                        "averageViewDuration",
                        "averageViewPercentage",
                        "likes",
                        "comments",
                        "shares",
                        "subscribersGained",
                        "subscribersLost",
                    ]
                ),
            },
        )

    def video_analytics(self, video_id: str, start_date: str, end_date: str) -> dict[str, Any]:
        return self._request(
            YOUTUBE_ANALYTICS_BASE,
            "/reports",
            query={
                "ids": "channel==MINE",
                "startDate": start_date,
                "endDate": end_date,
                "dimensions": "day",
                "filters": f"video=={video_id}",
                "metrics": ",".join(
                    [
                        "views",
                        "estimatedMinutesWatched",
                        "averageViewDuration",
                        "likes",
                        "comments",
                        "shares",
                        "subscribersGained",
                    ]
                ),
            },
        )

    def analytics_traffic_sources(self, start_date: str, end_date: str) -> dict[str, Any]:
        return self._request(
            YOUTUBE_ANALYTICS_BASE,
            "/reports",
            query={
                "ids": "channel==MINE",
                "startDate": start_date,
                "endDate": end_date,
                "dimensions": "insightTrafficSourceType",
                "metrics": "views,estimatedMinutesWatched",
                "sort": "-views",
            },
        )

    def analytics_demographics(self, start_date: str, end_date: str, dimension: str = "ageGroup,gender") -> dict[str, Any]:
        return self._request(
            YOUTUBE_ANALYTICS_BASE,
            "/reports",
            query={
                "ids": "channel==MINE",
                "startDate": start_date,
                "endDate": end_date,
                "dimensions": dimension,
                "metrics": "viewerPercentage",
                "sort": "-viewerPercentage",
            },
        )

    def analytics_top_videos(self, start_date: str, end_date: str, max_results: int = 10) -> dict[str, Any]:
        return self._request(
            YOUTUBE_ANALYTICS_BASE,
            "/reports",
            query={
                "ids": "channel==MINE",
                "startDate": start_date,
                "endDate": end_date,
                "dimensions": "video",
                "metrics": "views,estimatedMinutesWatched,averageViewDuration,likes,subscribersGained",
                "sort": "-views",
                "maxResults": max(1, min(max_results, 50)),
            },
        )

    # -------------------------------------------------------------------------
    # Search & Discovery
    # -------------------------------------------------------------------------

    def search_videos(self, query: str, max_results: int = 10, order: str = "relevance") -> dict[str, Any]:
        return self._request(
            YOUTUBE_API_BASE,
            "/search",
            query={
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": max(1, min(max_results, 50)),
                "order": order,
            },
        )

    def search_channels(self, query: str, max_results: int = 10) -> dict[str, Any]:
        return self._request(
            YOUTUBE_API_BASE,
            "/search",
            query={
                "part": "snippet",
                "q": query,
                "type": "channel",
                "maxResults": max(1, min(max_results, 50)),
            },
        )

    # -------------------------------------------------------------------------
    # Captions & Transcripts
    # -------------------------------------------------------------------------

    def list_captions(self, video_id: str) -> dict[str, Any]:
        return self._request(
            YOUTUBE_API_BASE,
            "/captions",
            query={"part": "snippet", "videoId": video_id},
        )

    def download_caption(self, caption_id: str, fmt: str = "srt") -> dict[str, Any]:
        url = f"{YOUTUBE_API_BASE}/captions/{caption_id}?tfmt={fmt}"
        headers = {"Authorization": f"Bearer {self._access_token()}"}
        status, _, body = http_raw(url, method="GET", headers=headers)
        raw_text = body.decode("utf-8", errors="replace")
        return {
            "caption_id": caption_id,
            "format": fmt,
            "content": raw_text,
        }

    def get_transcript(
        self,
        video_id: str,
        *,
        language: str | None = None,
        output_format: str = "text",
    ) -> dict[str, Any]:
        captions_resp = self.list_captions(video_id)
        items = captions_resp.get("items", [])
        if not items:
            return {
                "video_id": video_id,
                "has_transcript": False,
                "message": f"No caption tracks or transcripts found for video {video_id}.",
            }

        selected = None
        if language:
            for item in items:
                if item.get("snippet", {}).get("language") == language:
                    selected = item
                    break
        if not selected:
            selected = items[0]

        caption_id = selected["id"]
        lang = selected.get("snippet", {}).get("language", "und")
        download_result = self.download_caption(caption_id, fmt="srt")
        raw_srt = download_result.get("content", "")

        blocks = re.split(r"\n\s*\n", raw_srt.strip())
        segments = []
        text_lines = []
        for block in blocks:
            lines = [line.strip() for line in block.splitlines() if line.strip()]
            if len(lines) >= 2:
                time_line = lines[1] if lines[0].isdigit() and len(lines) > 2 else lines[0]
                text_part = " ".join(lines[2:]) if lines[0].isdigit() and len(lines) > 2 else " ".join(lines[1:])
                text_clean = re.sub(r"<[^>]+>", "", text_part).strip()
                if text_clean:
                    segments.append({"timestamp": time_line, "text": text_clean})
                    text_lines.append(text_clean)

        full_text = " ".join(text_lines)
        return {
            "video_id": video_id,
            "has_transcript": True,
            "caption_id": caption_id,
            "language": lang,
            "track_kind": selected.get("snippet", {}).get("trackKind"),
            "format": output_format,
            "raw_srt": raw_srt if output_format == "srt" else None,
            "full_text": full_text,
            "total_segments": len(segments),
            "segments": segments if output_format == "segments" else segments[:50],
        }

    def bulk_get_transcripts(
        self,
        *,
        video_ids: list[str] | None = None,
        playlist_id: str | None = None,
        max_videos: int = 10,
        language: str | None = None,
        output_format: str = "text",
        output_dir: str | None = None,
    ) -> dict[str, Any]:
        targets = []
        if video_ids:
            targets = [{"video_id": vid, "title": f"Video_{vid}"} for vid in video_ids[:max_videos]]
        elif playlist_id:
            pl_items = self.get_playlist(playlist_id, max_results=max_videos)
            for item in pl_items.get("items", []):
                vid = item.get("snippet", {}).get("resourceId", {}).get("videoId")
                title = item.get("snippet", {}).get("title", f"Video_{vid}")
                if vid:
                    targets.append({"video_id": vid, "title": title})
        else:
            recent = self.list_videos(max_results=max_videos)
            for item in recent.get("items", []):
                vid = item.get("playlistItem", {}).get("contentDetails", {}).get("videoId")
                title = item.get("playlistItem", {}).get("snippet", {}).get("title", f"Video_{vid}")
                if vid:
                    targets.append({"video_id": vid, "title": title})

        out_path = abs_path(output_dir) if output_dir else None
        if out_path:
            out_path.mkdir(parents=True, exist_ok=True)

        results = []
        for target in targets:
            vid = target["video_id"]
            title = target["title"]
            try:
                transcript_res = self.get_transcript(
                    vid, language=language, output_format=output_format
                )
                item_data = {
                    "video_id": vid,
                    "title": title,
                    "has_transcript": transcript_res.get("has_transcript", False),
                    "language": transcript_res.get("language"),
                    "total_segments": transcript_res.get("total_segments", 0),
                    "full_text": transcript_res.get("full_text", ""),
                }
                if output_format == "srt":
                    item_data["raw_srt"] = transcript_res.get("raw_srt")

                if out_path and transcript_res.get("has_transcript"):
                    safe_title = re.sub(r'[\\/*?:"<>|]', "_", title)[:50]
                    ext = "srt" if output_format == "srt" else "txt"
                    content = (
                        transcript_res.get("raw_srt")
                        if output_format == "srt"
                        else transcript_res.get("full_text", "")
                    )
                    file_name = f"{vid}_{safe_title}.{ext}"
                    (out_path / file_name).write_text(content or "", encoding="utf-8")
                    item_data["saved_file"] = str(out_path / file_name)

                results.append(item_data)
            except Exception as exc:
                results.append({
                    "video_id": vid,
                    "title": title,
                    "has_transcript": False,
                    "error": str(exc),
                })

        success_count = sum(1 for r in results if r.get("has_transcript"))
        return {
            "total_requested": len(targets),
            "successful_transcripts": success_count,
            "saved_to_directory": str(out_path) if out_path else None,
            "transcripts": results,
        }

    def delete_caption(self, caption_id: str) -> dict[str, Any]:
        return self._request(
            YOUTUBE_API_BASE,
            "/captions",
            method="DELETE",
            query={"id": caption_id},
        )
