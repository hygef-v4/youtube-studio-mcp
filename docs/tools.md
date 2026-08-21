# YouTube Studio MCP — Tool Reference

The YouTube Studio MCP server exposes **29 specialized tools** covering the full spectrum of channel administration, content publishing, playlist curation, audience engagement, deep analytics, and SEO research.

---

## Tool Overview by Category

### 1. 🔐 Authentication & Session (`2 tools`)
| Tool Name | Description | Key Parameters |
|---|---|---|
| `youtube_auth_status` | Check whether local OAuth credentials and session tokens exist. | *None* |
| `youtube_start_auth` | Generate the OAuth authorization URL and terminal command. | *None* |

---

### 2. 🎬 Videos & Content Publishing (`7 tools`)
| Tool Name | Description | Key Parameters |
|---|---|---|
| `youtube_channel_overview` | Fetch channel branding, stats, and uploads playlist ID. | *None* |
| `youtube_list_videos` | List recent uploads with combined metadata and public stats. | `max_results` (1–50), `page_token` |
| `youtube_get_video` | Fetch detailed snippet, status, and statistics for one video. | `video_id` *(required)* |
| `youtube_update_video` | Update title, description, tags, category, language, or privacy. | `video_id` *(req)*, `title`, `description`, `tags`, `privacy_status` |
| `youtube_delete_video` | Permanently delete a video from your channel. | `video_id` *(required)* |
| `youtube_upload_thumbnail` | Stream upload a local image file as a custom video thumbnail. | `video_id` *(req)*, `image_path` *(req)* |
| `youtube_upload_video` | Resumable upload of a local video file (`.mp4`, `.mov`, `.mkv`). | `video_path` *(req)*, `title` *(req)*, `description`, `tags`, `privacy_status` |

---

### 3. 📂 Playlists & Series Management (`7 tools`)
| Tool Name | Description | Key Parameters |
|---|---|---|
| `youtube_list_playlists` | List all playlists created on your channel. | `max_results` (1–50), `page_token` |
| `youtube_get_playlist` | Get all videos contained inside a specific playlist. | `playlist_id` *(required)*, `max_results` |
| `youtube_create_playlist` | Create a brand new playlist on your channel. | `title` *(required)*, `description`, `privacy_status` |
| `youtube_update_playlist` | Update title, description, or privacy of an existing playlist. | `playlist_id` *(required)*, `title`, `description`, `privacy_status` |
| `youtube_delete_playlist` | Delete a playlist from your channel. | `playlist_id` *(required)* |
| `youtube_add_to_playlist` | Add a video to a specific playlist at a target position. | `playlist_id` *(req)*, `video_id` *(req)*, `position` |
| `youtube_remove_from_playlist` | Remove a video item from a playlist. | `playlist_item_id` *(required)* |

---

### 4. 💬 Comments & Community Moderation (`4 tools`)
| Tool Name | Description | Key Parameters |
|---|---|---|
| `youtube_list_comments` | List top-level comment threads on a video. | `video_id` *(req)*, `max_results` (1–100) |
| `youtube_post_comment` | Post a top-level comment on one of your videos. | `video_id` *(req)*, `text` *(req)* |
| `youtube_reply_comment` | Reply directly to an existing audience comment. | `parent_id` *(req)*, `text` *(req)* |
| `youtube_delete_comment` | Delete a specific comment by ID. | `comment_id` *(required)* |

---

### 5. 📊 Deep Analytics & Audience Insights (`5 tools`)
| Tool Name | Description | Key Parameters |
|---|---|---|
| `youtube_channel_analytics` | Query channel-level aggregate performance across date range. | `start_date` *(req)*, `end_date` *(req)* |
| `youtube_video_analytics` | Query per-day metrics time-series for a specific video. | `video_id` *(req)*, `start_date` *(req)*, `end_date` *(req)* |
| `youtube_analytics_traffic_sources` | Breakdown of views by traffic source (Search, Suggested, etc.). | `start_date` *(req)*, `end_date` *(req)* |
| `youtube_analytics_demographics` | Breakdown of audience by age group, gender, or country. | `start_date` *(req)*, `end_date` *(req)*, `dimension` |
| `youtube_analytics_top_videos` | Top performing videos ranked by views and watch time. | `start_date` *(req)*, `end_date` *(req)*, `max_results` |

---

### 6. 🔎 SEO & Competitor Discovery (`2 tools`)
| Tool Name | Description | Key Parameters |
|---|---|---|
| `youtube_search_videos` | Search videos by keywords to analyze competitor titles and tags. | `query` *(req)*, `max_results`, `order` |
| `youtube_search_channels` | Search YouTube channels by topic or keyword. | `query` *(required)*, `max_results` |

---

### 7. 🌐 Subtitles & Transcripts (`5 tools`)
| Tool Name | Description | Key Parameters |
|---|---|---|
| `youtube_list_captions` | List existing subtitle tracks for a video. | `video_id` *(required)* |
| `youtube_get_transcript` | Extract clean full spoken transcript, summary text, or timestamps. | `video_id` *(req)*, `language`, `output_format` (`text`/`srt`/`segments`) |
| `youtube_bulk_get_transcripts` | Bulk extract transcripts from video IDs, playlist, or recent uploads. | `video_ids`, `playlist_id`, `max_videos`, `output_dir` |
| `youtube_download_caption` | Download raw caption file (SRT, VTT, SBV) by caption ID. | `caption_id` *(req)*, `fmt` (`srt`/`vtt`/`sbv`) |
| `youtube_delete_caption` | Delete a caption track by ID. | `caption_id` *(required)* |

---

## 💡 Example Prompt Invocations

### Transcript Extraction & Summarization
```text
Extract the full transcript of video VIDEO_ID, summarize the key points, and generate 5 SEO chapters with timestamps.
```

### Channel Inspection & SEO
```text
Show my channel overview and summarize the performance of my last 5 uploaded videos.
```

### Video Optimization
```text
Review video VIDEO_ID, optimize its title for higher CTR, write an SEO-rich description with timestamps, and update its tags.
```

### Thumbnail Publishing
```text
Upload the image file at "C:/thumbnails/valorant_ep1.png" as the custom thumbnail for video VIDEO_ID.
```

### Playlist Curation
```text
Create a new public playlist titled "Valorant Highlights" and add video VIDEO_ID to it.
```

### Audience Engagement
```text
Read the top 10 comments on video VIDEO_ID and draft thoughtful replies to viewers asking questions.
```

### Growth & Analytics
```text
Analyze my traffic sources and viewer demographics over the last 28 days. Where are most of my viewers discovering my content?
```
