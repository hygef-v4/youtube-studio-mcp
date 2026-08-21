# Contributing

Thanks for helping improve YouTube Studio MCP.

## Development setup

1. Clone the repo.
2. Create your own Google Cloud OAuth desktop client.
3. Put the OAuth JSON at `secrets/client_secret.json`.
4. Run `python scripts/auth.py auth`.
5. Configure your MCP client to run `python scripts/server.py`.

## Pull requests

- Keep secrets, tokens, and channel-specific data out of commits.
- Prefer small, focused changes.
- Include clear manual test notes for YouTube API behavior.
- Update `README.md` when changing setup steps, scopes, or available tools.

## Code style

This project intentionally has no third-party Python runtime dependencies. Keep new functionality standard-library only unless there is a strong reason to add a dependency.
