# Component Dependencies & Communication Patterns

## Dependency Matrix

| Component | Depends On | Dependency Type | Communication Pattern |
|---|---|---|---|
| `McpServer` | `AuthConfig` | Direct Instance | In-memory synchronous call |
| `McpServer` | `YouTubeClient` | Direct Instance | In-memory synchronous call |
| `YouTubeClient` | `AuthConfig` | Shared Reference | In-memory token retrieval & disk persistence |
| `YouTubeClient` | Google YouTube API | External Network | HTTPS REST / JSON-over-TLS |
| `YouTubeClient` | Google Analytics API | External Network | HTTPS REST / JSON-over-TLS |
| `AuthConfig` | Google OAuth Token Server | External Network | HTTPS `POST /token` |
| `AuthConfig` | Local File System (`secrets/`) | File I/O | Standard synchronous file reads/writes |
| `OAuthHandler` | Google OAuth Auth Server | External Network | Browser Redirect / Loopback callback |

---

## Communication Patterns

### 1. Client-to-Server (Stdio JSON-RPC 2.0)
- **Protocol**: JSON-RPC 2.0
- **Transport**: Standard Input/Output (`stdio`)
- **Framing**: Binary header: `Content-Length: <n>\r\n\r\n` followed by `<n>` bytes of UTF-8 JSON payload.
- **Handling**: Blocking read loop in main thread; response written immediately upon tool execution.

### 2. Server-to-Google Cloud (HTTPS REST)
- **Protocol**: HTTPS 1.1 with TLS 1.3
- **Authentication**: `Authorization: Bearer <access_token>` header
- **Payload Format**: `application/json` for metadata, `multipart/media` or raw binary for thumbnail image uploads.
- **Timeouts**: 60 seconds default timeout, 120 seconds for media uploads.
