# Application Design (Consolidated)

## Executive Summary
YouTube Studio MCP is an open-source, local Model Context Protocol (MCP) server that empowers LLM agents to manage YouTube channel operations, analyze video metrics, modify video metadata, and upload custom thumbnails. The application is built on a zero-runtime-dependency Python 3.10+ architecture communicating over standard input/output (`stdio`) JSON-RPC 2.0.

---

## 1. Architectural Architecture & Component Topology

```mermaid
flowchart TD
    subgraph ClientHost["Host Environment (Developer / Creator Machine)"]
        subgraph AgentEnv["MCP Client Environment"]
            LLMClient["AI Client<br/>(Claude Desktop / Cursor / Codex)"]
        end

        subgraph MCPServer["YouTube Studio MCP Core (Python 3.10+)"]
            StdioHandler["Stdio Message Handler<br/>(Content-Length / JSON-RPC 2.0)"]
            Router["McpServer Router<br/>(11 Tools Dispatcher)"]
            
            subgraph DomainServices["Domain Service Layer"]
                AuthSvc["Authentication & Token Service<br/>(AuthConfig)"]
                YTSvc["YouTube API Engine<br/>(YouTubeClient)"]
            end
        end

        subgraph LocalVault["Local Credential Vault"]
            SecretsStore[("Local File System<br/>secrets/client_secret.json<br/>secrets/token.json")]
        end
    end

    subgraph GCP["Google Cloud Platform"]
        OAuthEP["Google OAuth 2.0 Token Endpoint"]
        YTDataEP["YouTube Data API v3"]
        YTAnalyticsEP["YouTube Analytics API v2"]
    end

    LLMClient <-->|stdio JSON-RPC 2.0| StdioHandler
    StdioHandler <--> Router
    Router --> AuthSvc
    Router --> YTSvc
    YTSvc <--> AuthSvc
    AuthSvc <--> LocalVault
    AuthSvc <-->|POST /token (Refresh)| OAuthEP
    YTSvc <-->|HTTPS REST| YTDataEP
    YTSvc <-->|HTTPS REST| YTAnalyticsEP
```

### Text Alternative
```
[AI MCP Client] <---> [Stdio Message Handler / Router]
                             |
                   +---------+---------+
                   |                   |
             [AuthConfig]      [YouTubeClient]
                   |                   |
            [Local Secrets]    [Google YouTube & Analytics APIs]
```

---

## 2. Component Design Summary

| Component | Class / Module | Purpose |
|---|---|---|
| **MCP Protocol Coordinator** | `McpServer` (`scripts/server.py`) | Handles stdio binary framing, protocol negotiation, and dispatches 11 MCP tools. |
| **Google YouTube Client** | `YouTubeClient` (`scripts/server.py`) | Encapsulates all REST calls to YouTube Data API v3 and YouTube Analytics API v2. |
| **Credential & Token Vault** | `AuthConfig` (`scripts/server.py`) | Manages local OAuth JSON files and automatically refreshes tokens upon expiry. |
| **OAuth PKCE CLI Assistant** | `OAuthHandler` (`scripts/auth.py`) | Interactive CLI for initial browser consent and code-for-token exchange. |

---

## 3. Tool Interface Summary (11 Tools)

1. `youtube_auth_status`: Checks presence of credentials and tokens on disk.
2. `youtube_start_auth`: Generates authorization URL and local helper commands.
3. `youtube_channel_overview`: Returns channel subscriber counts, view totals, and uploads playlist ID.
4. `youtube_list_videos`: Paginated retrieval of recent uploads enriched with view/like statistics.
5. `youtube_get_video`: Detailed video snippet, status, and statistics inspection.
6. `youtube_update_video`: Modifies titles, descriptions, tags, categories, language, or privacy status.
7. `youtube_upload_thumbnail`: Streams local binary image files as custom video thumbnails.
8. `youtube_channel_analytics`: Aggregated channel metrics across custom date ranges.
9. `youtube_video_analytics`: Daily time-series retention and watch time metrics for specific videos.
10. `youtube_post_comment`: Publishes new top-level comment threads on videos.
11. `youtube_list_comments`: Retrieves top-level comment threads ordered by relevance.

---

## 4. Verification & Operational Health
The system has been verified end-to-end against live Google APIs on channel `Chal7z`:
- OAuth PKCE authorization verified with local token persistence.
- Live API reading verified (Channel Overview: 938 subscribers, 32 videos, 11,612 views).
- Live API mutation verified (Tags updated across 6 published videos).
