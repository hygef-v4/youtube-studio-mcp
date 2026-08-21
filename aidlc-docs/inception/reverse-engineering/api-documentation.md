# API Documentation

## MCP Tools Interface (JSON-RPC 2.0)

The server implements the Model Context Protocol (protocol version `2024-11-05`) exposing 11 distinct tools:

### 1. `youtube_auth_status`
- **Purpose**: Verify if client secret and token files are present in the filesystem.
- **Input Schema**:
  ```json
  {
    "type": "object",
    "properties": {},
    "additionalProperties": false
  }
  ```
- **Response Format**:
  ```json
  {
    "client_secrets_exists": true,
    "token_exists": true,
    "client_secrets_path": "/path/to/secrets/client_secret.json",
    "token_path": "/path/to/secrets/token.json"
  }
  ```

---

### 2. `youtube_start_auth`
- **Purpose**: Generate the OAuth authorization URL and return the local helper command.
- **Input Schema**:
  ```json
  {
    "type": "object",
    "properties": {},
    "additionalProperties": false
  }
  ```
- **Response Format**:
  ```json
  {
    "authorization_url": "https://accounts.google.com/o/oauth2/v2/auth?...",
    "token_path": "/path/to/secrets/token.json",
    "client_secrets_path": "/path/to/secrets/client_secret.json",
    "helper_command": "python3 /path/to/scripts/auth.py auth",
    "redirect_uri": "http://127.0.0.1:8765/oauth2callback"
  }
  ```

---

### 3. `youtube_channel_overview`
- **Purpose**: Fetch the authenticated channel's profile, statistics, branding, and uploads playlist ID.
- **Input Schema**:
  ```json
  {
    "type": "object",
    "properties": {},
    "additionalProperties": false
  }
  ```
- **Response Format**:
  ```json
  {
    "kind": "youtube#channelListResponse",
    "items": [
      {
        "id": "UCxxxxxxxxxxxxxxxxxxxx",
        "snippet": { "title": "My Channel", "description": "...", "customUrl": "@mychannel" },
        "statistics": { "viewCount": "1000", "subscriberCount": "500", "videoCount": "20" },
        "contentDetails": { "relatedPlaylists": { "uploads": "UUxxxxxxxxxxxxxxxxxxxx" } }
      }
    ]
  }
  ```

---

### 4. `youtube_list_videos`
- **Purpose**: List recent channel uploads with merged video details and statistics.
- **Input Schema**:
  ```json
  {
    "type": "object",
    "properties": {
      "max_results": { "type": "integer", "minimum": 1, "maximum": 25, "default": 10 },
      "page_token": { "type": "string" }
    },
    "additionalProperties": false
  }
  ```
- **Response Format**:
  ```json
  {
    "items": [
      {
        "playlistItem": { "snippet": { "title": "...", "resourceId": { "videoId": "..." } } },
        "details": { "snippet": { "tags": [] }, "statistics": { "viewCount": "150" }, "status": { "privacyStatus": "public" } }
      }
    ],
    "nextPageToken": "CDIQAA",
    "pageInfo": { "totalResults": 20, "resultsPerPage": 10 }
  }
  ```

---

### 5. `youtube_get_video`
- **Purpose**: Fetch detailed metadata for a single YouTube video by its video ID.
- **Input Schema**:
  ```json
  {
    "type": "object",
    "properties": {
      "video_id": { "type": "string" }
    },
    "required": ["video_id"],
    "additionalProperties": false
  }
  ```
- **Response Format**: Full YouTube Video resource object (`snippet`, `statistics`, `status`, `contentDetails`).

---

### 6. `youtube_update_video`
- **Purpose**: Update title, description, tags, category, default language, or privacy status.
- **Input Schema**:
  ```json
  {
    "type": "object",
    "properties": {
      "video_id": { "type": "string" },
      "title": { "type": "string" },
      "description": { "type": "string" },
      "tags": { "type": "array", "items": { "type": "string" } },
      "category_id": { "type": "string" },
      "default_language": { "type": "string" },
      "privacy_status": { "type": "string" }
    },
    "required": ["video_id"],
    "additionalProperties": false
  }
  ```
- **Response Format**: Updated YouTube Video resource object (`snippet`, `status`).

---

### 7. `youtube_upload_thumbnail`
- **Purpose**: Upload a custom thumbnail from a local image file path.
- **Input Schema**:
  ```json
  {
    "type": "object",
    "properties": {
      "video_id": { "type": "string" },
      "image_path": { "type": "string" }
    },
    "required": ["video_id", "image_path"],
    "additionalProperties": false
  }
  ```
- **Response Format**:
  ```json
  {
    "kind": "youtube#thumbnailSetResponse",
    "items": [
      {
        "default": { "url": "https://..." },
        "medium": { "url": "https://..." },
        "high": { "url": "https://..." }
      }
    ]
  }
  ```

---

### 8. `youtube_channel_analytics`
- **Purpose**: Fetch aggregated channel performance metrics across a date range.
- **Input Schema**:
  ```json
  {
    "type": "object",
    "properties": {
      "start_date": { "type": "string", "description": "YYYY-MM-DD" },
      "end_date": { "type": "string", "description": "YYYY-MM-DD" }
    },
    "required": ["start_date", "end_date"],
    "additionalProperties": false
  }
  ```
- **Metrics Returned**: `views`, `estimatedMinutesWatched`, `averageViewDuration`, `averageViewPercentage`, `likes`, `comments`, `shares`, `subscribersGained`, `subscribersLost`.

---

### 9. `youtube_video_analytics`
- **Purpose**: Fetch daily performance report for a specific video across a date range.
- **Input Schema**:
  ```json
  {
    "type": "object",
    "properties": {
      "video_id": { "type": "string" },
      "start_date": { "type": "string", "description": "YYYY-MM-DD" },
      "end_date": { "type": "string", "description": "YYYY-MM-DD" }
    },
    "required": ["video_id", "start_date", "end_date"],
    "additionalProperties": false
  }
  ```
- **Dimensions**: `day`
- **Metrics Returned**: `views`, `estimatedMinutesWatched`, `averageViewDuration`, `likes`, `comments`, `shares`, `subscribersGained`.

---

### 10. `youtube_post_comment`
- **Purpose**: Publish a new top-level comment on a video.
- **Input Schema**:
  ```json
  {
    "type": "object",
    "properties": {
      "video_id": { "type": "string" },
      "text": { "type": "string" }
    },
    "required": ["video_id", "text"],
    "additionalProperties": false
  }
  ```
- **Response Format**: Created `commentThread` object.

---

### 11. `youtube_list_comments`
- **Purpose**: Retrieve top-level comment threads for a video.
- **Input Schema**:
  ```json
  {
    "type": "object",
    "properties": {
      "video_id": { "type": "string" },
      "max_results": { "type": "integer", "minimum": 1, "maximum": 100, "default": 20 }
    },
    "required": ["video_id"],
    "additionalProperties": false
  }
  ```
- **Response Format**: List of comment thread items ordered by relevance.

---

## External HTTP REST APIs Consumed

| Endpoint | Method | Purpose |
|---|---|---|
| `https://oauth2.googleapis.com/token` | `POST` | Exchanges authorization code or refresh token for access token. |
| `https://www.googleapis.com/youtube/v3/channels` | `GET` | Retrieves authenticated channel profile (`mine=true`). |
| `https://www.googleapis.com/youtube/v3/playlistItems` | `GET` | Retrieves items from the channel's uploads playlist. |
| `https://www.googleapis.com/youtube/v3/videos` | `GET` / `PUT` | Fetches details and updates video snippet / status. |
| `https://www.googleapis.com/upload/youtube/v3/thumbnails/set` | `POST` | Uploads binary thumbnail media. |
| `https://www.googleapis.com/youtube/v3/commentThreads` | `GET` / `POST` | Lists and creates video comment threads. |
| `https://youtubeanalytics.googleapis.com/v2/reports` | `GET` | Queries channel-level and video-level analytics. |
