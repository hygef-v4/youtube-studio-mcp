"""Authentication and OAuth 2.0 PKCE token management for YouTube Studio MCP."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import secrets
import sys
import threading
import time
import urllib.parse
import urllib.request
import webbrowser
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

from youtube_studio_mcp.constants import (
    AUTH_URL,
    REDIRECT_URI,
    SCOPES,
    TOKEN_URL,
)
from youtube_studio_mcp.http import abs_path, http_json, read_json, write_json


@dataclass
class AuthConfig:
    client_secrets_path: Path
    token_path: Path

    def load_client_config(self) -> dict[str, Any]:
        payload = read_json(self.client_secrets_path)
        client = payload.get("installed") or payload.get("web")
        if not client:
            raise RuntimeError(
                "client_secret.json must contain an 'installed' or 'web' client definition."
            )
        return client

    def load_token(self) -> dict[str, Any]:
        if not self.token_path.exists():
            raise RuntimeError(
                f"Token file not found at {self.token_path}. Run 'python scripts/auth.py auth' first."
            )
        return read_json(self.token_path)

    def save_token(self, payload: dict[str, Any]) -> None:
        write_json(self.token_path, payload)

    def auth_status(self) -> dict[str, Any]:
        return {
            "client_secrets_exists": self.client_secrets_path.exists(),
            "token_exists": self.token_path.exists(),
            "client_secrets_path": str(self.client_secrets_path),
            "token_path": str(self.token_path),
        }


def post_form(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    encoded = urllib.parse.urlencode(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=encoded,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


class OAuthHandler(BaseHTTPRequestHandler):
    server_version = "YouTubeStudioOAuth/1.0"

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        self.server.auth_code = query.get("code", [None])[0]  # type: ignore[attr-defined]
        self.server.auth_error = query.get("error", [None])[0]  # type: ignore[attr-defined]
        self.server.auth_state = query.get("state", [None])[0]  # type: ignore[attr-defined]
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        if getattr(self.server, "auth_code", None):
            body = (
                "<html><body style='font-family:sans-serif;text-align:center;padding:50px;'>"
                "<h1 style='color:#2E7D32;'>YouTube Connection Successful!</h1>"
                "<p>OAuth credentials have been saved. You can close this window and return to your AI Assistant / IDE.</p>"
                "</body></html>"
            )
        else:
            body = (
                "<html><body style='font-family:sans-serif;text-align:center;padding:50px;'>"
                "<h1 style='color:#D32F2F;'>YouTube Connection Failed</h1>"
                "<p>Please check your terminal for error details.</p>"
                "</body></html>"
            )
        self.wfile.write(body.encode("utf-8"))

    def log_message(self, fmt: str, *args: Any) -> None:  # noqa: A003
        return


def run_auth(client_secrets: Path, token_path: Path) -> int:
    auth_config = AuthConfig(client_secrets, token_path)
    client = auth_config.load_client_config()
    state = secrets.token_urlsafe(24)
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(48)).decode("utf-8").rstrip("=")
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .decode("utf-8")
        .rstrip("=")
    )
    params = urllib.parse.urlencode(
        {
            "client_id": client["client_id"],
            "redirect_uri": REDIRECT_URI,
            "response_type": "code",
            "scope": " ".join(SCOPES),
            "access_type": "offline",
            "prompt": "consent",
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
    )
    url = f"{AUTH_URL}?{params}"

    server = HTTPServer(("127.0.0.1", 8765), OAuthHandler)
    thread = threading.Thread(target=server.handle_request, daemon=True)
    thread.start()

    print("Open this URL if your browser does not launch automatically:")
    print(url)
    print("")
    sys.stdout.flush()
    webbrowser.open(url)

    deadline = time.time() + 300
    while time.time() < deadline and not getattr(server, "auth_code", None) and not getattr(
        server, "auth_error", None
    ):
        time.sleep(0.25)

    if getattr(server, "auth_error", None):
        print(f"OAuth failed: {server.auth_error}", file=sys.stderr)  # type: ignore[attr-defined]
        return 1
    if getattr(server, "auth_state", None) != state:  # type: ignore[attr-defined]
        print("OAuth failed: state mismatch.", file=sys.stderr)
        return 1
    if not getattr(server, "auth_code", None):
        print("OAuth failed: timed out waiting for Google callback.", file=sys.stderr)
        return 1

    token = post_form(
        TOKEN_URL,
        {
            "code": server.auth_code,  # type: ignore[attr-defined]
            "client_id": client["client_id"],
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
            "code_verifier": code_verifier,
            **({"client_secret": client["client_secret"]} if client.get("client_secret") else {}),
        },
    )
    token["created_at"] = int(time.time())
    auth_config.save_token(token)
    print(f"Saved OAuth token to {token_path}")
    return 0
