# Component Methods

## 1. `McpServer` Methods (`scripts/server.py`)

### `serve() -> None`
- **Purpose**: Main event loop listening on `sys.stdin.buffer` for incoming JSON-RPC messages and writing responses to `sys.stdout.buffer`.
- **Input**: None (Reads from standard input pipe).
- **Output**: None.

### `_read_message() -> dict[str, Any] | None`
- **Purpose**: Reads `Content-Length: <n>\r\n\r\n` header from binary stdin stream, reads exact byte payload, and parses JSON.
- **Input**: None.
- **Output**: Parsed JSON message dictionary or `None` if EOF reached.

### `_write_message(payload: dict[str, Any]) -> None`
- **Purpose**: Serializes dictionary to UTF-8 JSON and writes formatted binary framing to stdout.
- **Input**: `payload` (JSON-RPC response or error dictionary).
- **Output**: None.

### `_call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]`
- **Purpose**: Dispatches tool request by tool name to the appropriate `YouTubeClient` or `AuthConfig` method.
- **Input**: `name` (Tool name string), `arguments` (Tool parameters dict).
- **Output**: Tool execution result payload.

---

## 2. `YouTubeClient` Methods (`scripts/server.py`)

### `channel_overview() -> dict[str, Any]`
- **Purpose**: Queries `GET /youtube/v3/channels?part=snippet,statistics,brandingSettings,contentDetails&mine=true`.
- **Output**: Channel list response dictionary containing channel metadata and uploads playlist ID.

### `list_videos(max_results: int = 10, page_token: str | None = None) -> dict[str, Any]`
- **Purpose**: Fetches uploads playlist items from `GET /youtube/v3/playlistItems`, then fetches full video details via `GET /youtube/v3/videos` and merges them.
- **Input**: `max_results` (int: 1–25), `page_token` (Optional pagination string).
- **Output**: Dictionary with merged items (`playlistItem`, `details`), `nextPageToken`, and `pageInfo`.

### `get_video(video_id: str) -> dict[str, Any]`
- **Purpose**: Fetches detailed metadata for a single video via `GET /youtube/v3/videos?part=snippet,statistics,status,contentDetails&id={video_id}`.
- **Input**: `video_id` (str).
- **Output**: Video resource dictionary.

### `update_video(video_id: str, *, title: str | None = None, description: str | None = None, tags: list[str] | None = None, category_id: str | None = None, default_language: str | None = None, privacy_status: str | None = None) -> dict[str, Any]`
- **Purpose**: Retrieves existing video snippet/status, applies partial mutations, and calls `PUT /youtube/v3/videos?part=snippet,status`.
- **Input**: `video_id` (str), optional mutation fields.
- **Output**: Updated video resource dictionary.

### `upload_thumbnail(video_id: str, image_path: str) -> dict[str, Any]`
- **Purpose**: Reads local image file, resolves MIME type, and uploads raw bytes to `POST /upload/youtube/v3/thumbnails/set?videoId={video_id}&uploadType=media`.
- **Input**: `video_id` (str), `image_path` (str).
- **Output**: Thumbnail set response dictionary.

### `channel_analytics(start_date: str, end_date: str) -> dict[str, Any]`
- **Purpose**: Queries `GET /v2/reports?ids=channel==MINE&startDate={start_date}&endDate={end_date}&metrics=...` on YouTube Analytics API.
- **Input**: `start_date` (YYYY-MM-DD), `end_date` (YYYY-MM-DD).
- **Output**: Analytics report payload with column headers and rows.

### `video_analytics(video_id: str, start_date: str, end_date: str) -> dict[str, Any]`
- **Purpose**: Queries `GET /v2/reports?ids=channel==MINE&startDate={start_date}&endDate={end_date}&dimensions=day&filters=video=={video_id}&metrics=...`.
- **Input**: `video_id` (str), `start_date` (str), `end_date` (str).
- **Output**: Per-day analytics rows for the target video.

### `post_comment(video_id: str, text: str) -> dict[str, Any]`
- **Purpose**: Creates a new top-level comment via `POST /youtube/v3/commentThreads?part=snippet`.
- **Input**: `video_id` (str), `text` (str).
- **Output**: Created comment thread object.

### `list_comments(video_id: str, max_results: int = 20) -> dict[str, Any]`
- **Purpose**: Retrieves comment threads via `GET /youtube/v3/commentThreads?part=snippet&videoId={video_id}&maxResults={max_results}&order=relevance`.
- **Input**: `video_id` (str), `max_results` (int: 1–100).
- **Output**: Comment threads list response.

---

## 3. `AuthConfig` Methods (`scripts/server.py`)

### `load_client_config() -> dict[str, Any]`
- **Purpose**: Reads and validates `client_secret.json`, returning the `installed` or `web` client configuration dictionary.

### `load_token() -> dict[str, Any]`
- **Purpose**: Reads saved OAuth token payload from `token.json`.

### `save_token(payload: dict[str, Any]) -> None`
- **Purpose**: Writes updated token payload (with `created_at` timestamp) to `token.json`.

### `auth_status() -> dict[str, Any]`
- **Purpose**: Checks file existence for both client secrets and token files, returning paths and booleans.
