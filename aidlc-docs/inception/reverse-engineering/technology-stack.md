# Technology Stack

## Programming Languages
- **Python**: 3.10+ (Primary runtime language using standard library features like `dataclasses`, type annotations, `urllib`, `http.server`, `secrets`)
- **Bash / Shell**: Bash scripts for GitHub repository publishing (`publish_github.sh`)
- **JSON**: Protocol payload formatting, configuration manifests (`.mcp.json`, `plugin.json`), and credential token stores

## Frameworks & Protocols
- **Model Context Protocol (MCP)**: Specification `2024-11-05` (stdio transport with JSON-RPC 2.0 and `Content-Length` header framing)
- **OAuth 2.0 with PKCE**: RFC 7636 (Proof Key for Code Exchange) using SHA-256 challenge

## External APIs & Cloud Services
- **Google Cloud Platform (GCP)**:
  - **YouTube Data API v3**: Channels, Videos, PlaylistItems, CommentThreads, Thumbnails
  - **YouTube Analytics API v2**: Aggregated channel reports, daily video reports
  - **Google OAuth 2.0 Identity Platform**: Consent screen, code exchange, refresh token grant

## Build & Quality Tools
- **Build System**: PEP 621 Standard Python packaging via `pyproject.toml`
- **Linter & Formatter**: Ruff (`line-length = 100`)
- **Version Control**: Git & GitHub CLI (`gh`)

## Testing Tools
- **Current State**: Manual end-to-end testing via MCP client integration; candidate for `pytest` / `unittest` test suite integration.
