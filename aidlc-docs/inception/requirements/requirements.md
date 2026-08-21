# Requirements Document

## Intent Analysis Summary
- **User Request**: "triển khai aidlc và viết hoàn thành bộ doc cho dự án này" (Implement AI-DLC and write complete documentation set for this project)
- **Request Type**: Reverse Engineering, Architecture Documentation, & AI-DLC Inception Lifecycle
- **Scope Estimate**: System-wide (Entire repository documentation, protocol definitions, tool specifications, and lifecycle traceability)
- **Complexity Estimate**: Moderate
- **Requirements Depth**: Standard

---

## 1. Overview & System Objectives
The objective of YouTube Studio MCP is to provide a secure, local, zero-runtime-dependency Model Context Protocol (MCP) server that connects AI assistants (OpenAI Codex, Claude Desktop, Cursor) to Google's YouTube Data API v3 and YouTube Analytics API v2. It enables AI-driven channel administration, metadata optimization, custom thumbnail publishing, analytics reporting, and audience comment interactions while keeping OAuth credentials strictly on the local client machine.

---

## 2. Functional Requirements (FR)

### Authentication & Token Lifecycle
- **FR-AUTH-01 (Credential Discovery)**: The system shall verify the presence of `client_secret.json` and `token.json` in the configured secrets directory.
- **FR-AUTH-02 (PKCE OAuth Flow)**: The system shall generate RFC 7636 PKCE code verifiers and SHA-256 code challenges, spawn a temporary loopback HTTP server on `http://127.0.0.1:8765`, launch the user's browser for Google OAuth consent, and save access/refresh tokens to disk.
- **FR-AUTH-03 (Proactive Token Refresh)**: The server shall verify access token validity before every Google API dispatch and automatically refresh expired tokens (`expires_in - 120s`) using the stored `refresh_token`.

### MCP Protocol & Transport
- **FR-PROTO-01 (Stdio Framing)**: The server shall communicate over standard I/O pipes (`sys.stdin.buffer` / `sys.stdout.buffer`) with binary `Content-Length: <n>\r\n\r\n` header framing per MCP JSON-RPC 2.0 specifications.
- **FR-PROTO-02 (Lifecycle Methods)**: The server shall respond to standard MCP requests: `initialize`, `ping`, `tools/list`, and `tools/call`.

### YouTube Studio Tool Capabilities
- **FR-TOOL-01 (`youtube_auth_status`)**: Return boolean status of local credential and token file existence.
- **FR-TOOL-02 (`youtube_start_auth`)**: Return the Google OAuth authorization URL, local file paths, and helper command for interactive authorization.
- **FR-TOOL-03 (`youtube_channel_overview`)**: Fetch authenticated channel details (snippet, statistics, brandingSettings, contentDetails with uploads playlist ID).
- **FR-TOOL-04 (`youtube_list_videos`)**: Fetch recent uploads playlist items (1–25 items), merge with full video statistics and content details, and provide pagination tokens.
- **FR-TOOL-05 (`youtube_get_video`)**: Retrieve comprehensive metadata (snippet, statistics, status, contentDetails) for a given `video_id`.
- **FR-TOOL-06 (`youtube_update_video`)**: Update video metadata (title, description, tags list, categoryId, defaultLanguage, privacyStatus).
- **FR-TOOL-07 (`youtube_upload_thumbnail`)**: Read local image file (guessing MIME type) and stream binary upload to `/upload/youtube/v3/thumbnails/set`.
- **FR-TOOL-08 (`youtube_channel_analytics`)**: Query YouTube Analytics API for channel-level metrics across a specified `start_date` and `end_date` (YYYY-MM-DD).
- **FR-TOOL-09 (`youtube_video_analytics`)**: Query YouTube Analytics API for daily time-series metrics filtered by `video_id` across a date range.
- **FR-TOOL-10 (`youtube_post_comment`)**: Publish top-level comment threads on a specific video.
- **FR-TOOL-11 (`youtube_list_comments`)**: Retrieve top-level comment threads for a video with relevance ordering and pagination limits (1–100).

---

## 3. Non-Functional Requirements (NFR)

### Portability & Zero-Dependency Runtime
- **NFR-DEP-01**: Runtime execution must rely solely on the standard library of Python 3.10+ without external pip package dependencies.
- **NFR-DEP-02**: Cross-platform compatibility across Windows, macOS, and Linux hosts.

### Security & Privacy
- **NFR-SEC-01**: OAuth client credentials and tokens must remain on the creator's local filesystem and never be transmitted to third-party backends.
- **NFR-SEC-02**: The `secrets/` directory and private tokens must be excluded from version control via `.gitignore`.
- **NFR-SEC-03**: OAuth 2.0 PKCE flow must be used for native desktop client authorization.

### Reliability & Error Handling
- **NFR-REL-01**: HTTP error responses from Google APIs and JSON parsing failures must be caught gracefully and returned as JSON-RPC error frames or meaningful error messages rather than terminating the stdio process.
- **NFR-REL-02**: Network requests to Google APIs must enforce explicit socket timeouts (60s for REST queries, 120s for thumbnail uploads).

### Usability & Tool Discoverability
- **NFR-USE-01**: All MCP tools must define strict JSON Schema properties and descriptions so LLMs can accurately invoke tools and format arguments.

---

## 4. Traceability Matrix

| Requirement ID | Component / Module | External Dependency / API | Verification Method |
|---|---|---|---|
| FR-AUTH-01, 02 | `scripts/auth.py` | Google OAuth 2.0 Auth & Token APIs | Manual Auth Flow & File Check |
| FR-AUTH-03 | `scripts/server.py` (`AuthConfig`) | Google OAuth 2.0 Token API | Token expiry unit simulation |
| FR-PROTO-01, 02 | `scripts/server.py` (`McpServer`) | MCP Client (stdio) | JSON-RPC handshake test |
| FR-TOOL-01..05 | `scripts/server.py` (`YouTubeClient`) | YouTube Data API v3 (`/channels`, `/playlistItems`, `/videos`) | Tool execution verification |
| FR-TOOL-06 | `scripts/server.py` (`YouTubeClient`) | YouTube Data API v3 (`PUT /videos`) | Video metadata update check |
| FR-TOOL-07 | `scripts/server.py` (`YouTubeClient`) | YouTube Upload API (`POST /thumbnails/set`) | Thumbnail upload check |
| FR-TOOL-08, 09 | `scripts/server.py` (`YouTubeClient`) | YouTube Analytics API v2 (`/reports`) | Analytics query check |
| FR-TOOL-10, 11 | `scripts/server.py` (`YouTubeClient`) | YouTube Data API v3 (`/commentThreads`) | Comment read/write test |
| NFR-DEP-01, 02 | Entire Repository | Python Standard Library 3.10+ | Environment audit |
| NFR-SEC-01..03 | `secrets/`, `scripts/auth.py` | Local FS / Google OAuth | Git tracking & security scan |
