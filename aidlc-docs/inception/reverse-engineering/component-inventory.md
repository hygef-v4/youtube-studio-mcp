# Component Inventory

## Application Packages / Modules
- `scripts/server.py` - Core MCP runtime server providing JSON-RPC 2.0 stdio framing, tool dispatching, token auto-refresh, and YouTube Data & Analytics REST client implementations.
- `scripts/auth.py` - Standalone interactive OAuth 2.0 PKCE utility with local loopback callback HTTP listener.

## Infrastructure & Configuration Packages
- `pyproject.toml` - Python project configuration, metadata, and Ruff linter settings.
- `.mcp.json` - MCP server declaration mapping the Python executable and environment variables.
- `.codex-plugin/plugin.json` - Plugin manifest for OpenAI Codex integration.
- `scripts/publish_github.sh` - Automated GitHub repository creation, topic tagging, and synchronization script.

## Shared Assets & Documentation
- `secrets/` - Secure directory for local credentials (`client_secret.json`, `token.json`).
- `docs/` - Comprehensive guides (`demo.md`, `launch-copy.md`, `mcp-client-config.md`, `setup-google-oauth.md`, `tools.md`).
- `assets/` - SVG diagrams and visual assets (`demo-terminal.svg`).

## Test Packages
- Currently no automated unit test files exist (candidate for test suite creation in Construction phase).

## Total Count
- **Total Source Scripts**: 3 (`server.py`, `auth.py`, `publish_github.sh`)
- **Total Configuration Files**: 3 (`pyproject.toml`, `.mcp.json`, `plugin.json`)
- **Total Documentation Files**: 8 (`README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE`, 5 in `docs/`)
- **Application Modules**: 2
- **Infrastructure / Config**: 4
- **Shared / Docs / Assets**: 9
- **Test Modules**: 0
