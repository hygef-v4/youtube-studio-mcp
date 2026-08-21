# Security

This project can update YouTube video metadata, upload thumbnails, post comments, and read analytics through OAuth permissions granted by the user.

## Protect your credentials

- Never commit `secrets/client_secret.json` or `secrets/token.json`.
- Keep your Google OAuth client private.
- Revoke tokens from your Google Account if a machine is lost or compromised.
- Use a dedicated Google Cloud project for this MCP server when possible.

## Reporting issues

If you find a vulnerability, please open a private security advisory on GitHub if available, or contact the repository owner directly. Do not publish working exploits or leaked credentials in a public issue.
