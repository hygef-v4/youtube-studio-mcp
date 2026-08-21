# Interactive Demo & Verification Walkthrough

This demo walks through setting up the local YouTube Studio MCP server and interacting with it using an AI assistant.

---

## 1. Quick Setup
Clone the repository and initialize local credentials:

```bash
git clone https://github.com/your-username/youtube-studio-mcp.git
cd youtube-studio-mcp
mkdir -p secrets
```

Place your Google Cloud OAuth Desktop client JSON at:
```text
secrets/client_secret.json
```

Authenticate with Google:
```bash
python scripts/auth.py auth
```

Your browser will open to Google OAuth consent. Upon approval, tokens are stored at:
```text
secrets/token.json
```

---

## 2. Example Conversational Workflows

### Scenario A: Video SEO Optimization
```text
User:
"Check the latest 5 videos on my channel. Review their titles and tags, and optimize any that are missing SEO keywords."

Assistant Actions:
1. Calls `youtube_list_videos(max_results=5)`
2. Identifies videos with empty descriptions or missing tags
3. Calls `youtube_update_video(video_id=..., tags=[...], description=...)`
4. Summarizes changes made to the user.
```

### Scenario B: Automated Playlist Curation
```text
User:
"Create a new public playlist called 'Valorant Ranked Clutch' and add my latest video to it."

Assistant Actions:
1. Calls `youtube_create_playlist(title='Valorant Ranked Clutch', privacy_status='public')`
2. Obtains new `playlist_id`
3. Calls `youtube_add_to_playlist(playlist_id=..., video_id=...)`
4. Confirms playlist created with direct YouTube link.
```

### Scenario C: Growth & Traffic Source Auditing
```text
User:
"Give me a breakdown of where my viewers are coming from over the last 28 days."

Assistant Actions:
1. Calls `youtube_analytics_traffic_sources(start_date='2026-07-24', end_date='2026-08-21')`
2. Formats views and watch time into percentage breakdown (Search vs Suggested vs External)
3. Recommends content strategies to capitalize on top search terms.
```
