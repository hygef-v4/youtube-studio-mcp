<div align="center">

# 🎬 YouTube Studio MCP

**A high-performance, zero-dependency Model Context Protocol (MCP) server for full YouTube Studio management, video publishing, playlists, community interaction, and deep analytics directly from AI agents.**

[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](pyproject.toml)
[![MCP Protocol: 2024-11-05](https://img.shields.io/badge/MCP-stdio%202024--11--05-orange.svg)](docs/tools.md)
[![Google APIs: Data v3 + Analytics v2](https://img.shields.io/badge/YouTube-Data%20v3%20%2B%20Analytics%20v2-red.svg)](https://developers.google.com/youtube/v3)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(100%25%20Stdlib)-success.svg)](scripts/server.py)
[![Open Source](https://img.shields.io/badge/Open%20Source-Ready-purple.svg)](https://github.com/hygef-v4/youtube-studio-mcp)

```bash
# 1. Clone & Setup
git clone https://github.com/hygef-v4/youtube-studio-mcp.git
cd youtube-studio-mcp && python scripts/auth.py auth

# 2. Ask your AI Assistant (Claude Desktop / Cursor / Antigravity):
> "Audit my last 5 videos, optimize SEO tags, and summarize 28-day traffic sources."
```

</div>

---

## 🌟 Why YouTube Studio MCP?

Most YouTube automation tools either require heavy external dependencies or force you to route channel tokens through third-party cloud proxies. **YouTube Studio MCP** is designed from the ground up to be:

- 🛡️ **100% Local & Private**: Direct Google OAuth 2.0 PKCE authentication. All access tokens stay strictly on your local machine (`secrets/`).
- ⚡ **Zero Runtime Dependencies**: Built entirely on Python 3.10+ standard libraries (`urllib`, `http.server`, `json`, `dataclasses`, `secrets`). No pip dependencies, no version drift, instant startup.
- 🔄 **Autonomous Token Renewal**: Transparent background OAuth token refresh ensures long-running agent conversations are never interrupted.
- 🧰 **Comprehensive Toolset (31 MCP Tools)**: Complete coverage of YouTube channel operations from video uploads and full spoken transcript extraction to viewer demographics.

---

## 🗺️ System Architecture

```
 ┌────────────────────────────────────────────────────────┐
 │                      AI MCP CLIENT                     │
 │          (Claude Desktop / Cursor / Antigravity)       │
 └───────────────────────────┬────────────────────────────┘
                             │ stdio (JSON-RPC 2.0)
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │              YOUTUBE STUDIO MCP SERVER                 │
 │                                                        │
 │   ┌───────────────────────┐  ┌──────────────────────┐  │
 │   │      McpServer        │  │     AuthConfig       │  │
 │   │  (29 Tools Dispatcher)│  │ (OAuth Token Manager)│  │
 │   └───────────┬───────────┘  └──────────┬───────────┘  │
 │               │                         │              │
 │               ▼                         ▼              │
 │   ┌─────────────────────────────────────────────────┐  │
 │   │                 YouTubeClient                   │  │
 │   │ (Zero-dependency HTTPS REST Engine via urllib)  │  │
 │   └───────────────────┬─────────────────────────────┘  │
 └───────────────────────┼────────────────────────────────┘
                         │ HTTPS / TLS 1.3
                         ▼
 ┌────────────────────────────────────────────────────────┐
 │                 GOOGLE CLOUD PLATFORM                  │
 │  • Google OAuth 2.0 Token Server                       │
 │  • YouTube Data API v3                                 │
 │  • YouTube Analytics API v2                            │
 └────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start (5 Minutes)

### 1. Clone the repository
```bash
git clone https://github.com/hygef-v4/youtube-studio-mcp.git
cd youtube-studio-mcp
mkdir -p secrets
```

### 2. Configure Google Cloud OAuth Client
1. Create a project in [Google Cloud Console](https://console.cloud.google.com/).
2. Enable **YouTube Data API v3** and **YouTube Analytics API**.
3. Create an OAuth 2.0 Client ID with application type **Desktop app**.
4. Download the JSON credential file and save it locally as:
   ```text
   secrets/client_secret.json
   ```
*(See the step-by-step [Google OAuth Setup Guide](docs/setup-google-oauth.md) for screenshots and troubleshooting)*.

### 3. Authenticate Locally
Run the interactive loopback authentication helper:
```bash
python scripts/auth.py auth
```
Approve the permissions in your browser. Upon success, your credentials are encrypted locally in `secrets/token.json`.

---

## ⚙️ MCP Client Configuration

### Claude Desktop
Add to your `claude_desktop_config.json`:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "youtube-studio": {
      "command": "python",
      "args": ["F:/code/git/youtube-studio-mcp/scripts/server.py"],
      "cwd": "F:/code/git/youtube-studio-mcp",
      "env": {
        "YOUTUBE_CLIENT_SECRETS": "F:/code/git/youtube-studio-mcp/secrets/client_secret.json",
        "YOUTUBE_TOKEN_FILE": "F:/code/git/youtube-studio-mcp/secrets/token.json"
      }
    }
  }
}
```

### Cursor IDE
In Cursor **Settings > Features > MCP**, click **Add New MCP Server**:
- **Name**: `youtube-studio`
- **Type**: `command`
- **Command**: `python F:/code/git/youtube-studio-mcp/scripts/server.py`

*(See [MCP Client Configuration Guide](docs/mcp-client-config.md) for VS Code, Codex, and other clients)*.

---

## 🧰 Complete Directory of 32 MCP Tools

| Category | Tool Name | Description |
|---|---|---|
| **Auth & Setup** | `youtube_auth_status` | Check local OAuth secret and token existence. |
| | `youtube_start_auth` | Generate browser authorization URL and local command. |
| **Channel & Videos** | `youtube_channel_overview` | Fetch channel subscriber count, views, branding, and uploads playlist ID. |
| | `youtube_list_videos` | Retrieve recent uploads with combined metadata and public metrics. |
| | `youtube_get_video` | Inspect full snippet, statistics, and status for one video. |
| | `youtube_update_video` | Update title, description, tags list, category, language, or privacy status. |
| | `youtube_delete_video` | Permanently delete a video from your channel. |
| | `youtube_upload_thumbnail` | Upload a local image file as a custom high-res video thumbnail. |
| | `youtube_upload_video` | Resumable upload of a local video file (`.mp4`, `.mov`, `.mkv`) directly to YouTube. |
| **Playlists** | `youtube_list_playlists` | List all playlists on the authenticated channel. |
| | `youtube_get_playlist` | List all video items inside a specific playlist. |
| | `youtube_create_playlist` | Create a brand new playlist (public, unlisted, or private). |
| | `youtube_update_playlist` | Modify playlist title, description, or visibility status. |
| | `youtube_delete_playlist` | Delete a playlist from your channel. |
| | `youtube_add_to_playlist` | Add a video to a specific playlist at a defined position. |
| | `youtube_remove_from_playlist` | Remove a video entry from a playlist. |
| **Community & Comments** | `youtube_list_comments` | List top-level comment threads ordered by relevance. |
| | `youtube_post_comment` | Post a top-level comment on one of your videos. |
| | `youtube_reply_comment` | Reply directly to an audience comment. |
| | `youtube_delete_comment` | Delete a comment by its unique ID. |
| **Deep Analytics** | `youtube_channel_analytics` | Aggregate channel performance (views, watch time, subs) over custom date ranges. |
| | `youtube_video_analytics` | Daily time-series retention and watch time metrics for a specific video. |
| | `youtube_analytics_traffic_sources` | Breakdown of views by traffic origin (Search, Suggested, Browse, External). |
| | `youtube_analytics_demographics` | Audience demographics breakdown by age group, gender, or geographic country. |
| | `youtube_analytics_top_videos` | Rank top performing videos by views and watch time. |
| **Search & Research** | `youtube_search_videos` | Search videos by keywords to analyze competitor titles, tags, and views. |
| | `youtube_search_channels` | Search YouTube channels by topic or niche keyword. |
| **Captions & Transcripts** | `youtube_list_captions` | Inspect available caption and subtitle tracks for a video. |
| | `youtube_get_transcript` | Extract full spoken transcript, summary-ready text, or timestamped segments. |
| | `youtube_bulk_get_transcripts` | Bulk extract transcripts from a list of video IDs, a playlist, or recent uploads. |
| | `youtube_download_caption` | Download raw caption file (SRT, VTT, SBV) by caption ID. |
| | `youtube_delete_caption` | Delete a caption track by ID. |

*(For full input schemas, type definitions, and parameters, see [docs/tools.md](docs/tools.md))*.

---

## 💡 Example Conversational Prompts

```text
"Show my channel overview and summarize the public statistics of my last 5 videos."
```

```text
"Inspect video VIDEO_ID, generate 15 high-converting SEO tags, and update its description with chapter timestamps."
```

```text
"Upload the image at 'C:/thumbnails/hero.png' as the thumbnail for video VIDEO_ID."
```

```text
"Analyze where my channel views came from over the last 28 days and break down the traffic sources by percentage."
```

```text
"Create a new public playlist titled 'Valorant Highlights' and add my latest video to it."
```

---

## 🧪 Testing

Run the built-in test suite (no third-party test runners required):

```bash
python -m unittest discover tests
```

---

## 🔒 Security Policy

- Credentials (`secrets/client_secret.json` and `secrets/token.json`) are strictly git-ignored.
- No network requests are sent to any domain other than `googleapis.com` and `accounts.google.com`.
- See [SECURITY.md](SECURITY.md) for reporting guidelines.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/hygef-v4/youtube-studio-mcp/issues).

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.
