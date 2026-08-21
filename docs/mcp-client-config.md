# MCP Client Configuration

YouTube Studio MCP operates over standard I/O (`stdio`) JSON-RPC 2.0 and is compatible with any MCP client.

---

## 1. Claude Desktop Configuration
Add the server entry to your Claude Desktop configuration file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Option A: Direct from GitHub (`uvx` - Zero Manual Install)
```json
{
  "mcpServers": {
    "youtube-studio": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/hygef-v4/youtube-studio-mcp.git",
        "youtube-studio-mcp"
      ],
      "env": {
        "YOUTUBE_CLIENT_SECRETS": "/path/to/client_secret.json",
        "YOUTUBE_TOKEN_FILE": "/path/to/token.json"
      }
    }
  }
}
```

### Option B: Local Script (`python`)
```json
{
  "mcpServers": {
    "youtube-studio": {
      "command": "python",
      "args": ["/path/to/youtube-studio-mcp/scripts/server.py"],
      "cwd": "/path/to/youtube-studio-mcp",
      "env": {
        "YOUTUBE_CLIENT_SECRETS": "/path/to/youtube-studio-mcp/secrets/client_secret.json",
        "YOUTUBE_TOKEN_FILE": "/path/to/youtube-studio-mcp/secrets/token.json"
      }
    }
  }
}
```

---

## 2. Cursor IDE Configuration
In Cursor Settings > Features > MCP:
- **Name**: `youtube-studio`
- **Type**: `command`
- **Command**: `python /path/to/youtube-studio-mcp/scripts/server.py`

Or add `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "youtube-studio": {
      "command": "python",
      "args": ["./scripts/server.py"],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

---

## 3. Generic `.mcp.json` / OpenAI Codex
The repository includes a ready-to-use [`.mcp.json`](../.mcp.json) at project root:
```json
{
  "mcpServers": {
    "youtube-studio": {
      "command": "python",
      "args": ["./scripts/server.py"],
      "cwd": ".",
      "env": {
        "YOUTUBE_CLIENT_SECRETS": "./secrets/client_secret.json",
        "YOUTUBE_TOKEN_FILE": "./secrets/token.json"
      }
    }
  }
}
```
