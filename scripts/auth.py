#!/usr/bin/env python
"""Local OAuth 2.0 PKCE helper launcher for YouTube Studio MCP."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Ensure src/ is on Python search path
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from youtube_studio_mcp.auth import run_auth
from youtube_studio_mcp.http import abs_path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    parser = argparse.ArgumentParser(description="Authenticate with Google OAuth 2.0 PKCE")
    parser.add_argument("command", choices=["auth"])
    parser.add_argument(
        "--client-secrets",
        default=os.environ.get("YOUTUBE_CLIENT_SECRETS", "secrets/client_secret.json"),
    )
    parser.add_argument(
        "--token-file",
        default=os.environ.get("YOUTUBE_TOKEN_FILE", "secrets/token.json"),
    )
    args = parser.parse_args()
    client_secrets = abs_path(args.client_secrets, PLUGIN_ROOT)
    token_path = abs_path(args.token_file, PLUGIN_ROOT)
    return run_auth(client_secrets, token_path)


if __name__ == "__main__":
    raise SystemExit(main())
