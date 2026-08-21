# Google Cloud OAuth 2.0 Setup Guide

YouTube Studio MCP uses your own Google Cloud OAuth 2.0 Desktop client. This ensures that all API credentials, tokens, and data remain strictly on your local machine under your direct ownership.

---

## Step 1: Create or Select a Google Cloud Project
1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (e.g., `youtube-studio-automation`) or select an existing project.

---

## Step 2: Enable Required Google APIs
Navigate to **APIs & Services > Library** and enable both:
1. **YouTube Data API v3**
2. **YouTube Analytics API**

---

## Step 3: Configure OAuth Consent Screen & Audience
1. Navigate to **APIs & Services > OAuth consent screen** (or **Google Auth Platform**).
2. Choose **External** user type and fill in basic app details (App name, support email).
3. Under the **Audience / Test users** section:
   > ⚠️ **Important**: If your app is in *Testing* status (default for personal projects), click **+ Add users** and add the Google email address associated with your YouTube channel. This prevents `Error 403: access_denied`.

---

## Step 4: Create Desktop OAuth Client Credentials
1. Navigate to **APIs & Services > Credentials**.
2. Click **+ Create Credentials > OAuth client ID**.
3. Select Application type: **Desktop app**.
4. Set name (e.g., `YouTube Studio MCP Desktop`).
5. Click **Create**, then click **Download JSON**.
6. Save the downloaded JSON file into your local project repository as:
   ```text
   secrets/client_secret.json
   ```

---

## Step 5: Authenticate Locally
Run the built-in authentication script:

```bash
python scripts/auth.py auth
```

1. Your default web browser will open with the Google OAuth consent page.
2. Sign in with your YouTube channel account.
3. If Google displays *"Google hasn't verified this app"*:
   - Click **Advanced (Nâng cao)**.
   - Click **Go to [App Name] (unsafe)**.
4. Check all permission checkboxes and click **Continue**.
5. Once your browser displays **"YouTube Connection Successful!"**, the token is stored locally at:
   ```text
   secrets/token.json
   ```

> 🔒 **Security Notice**: Both `secrets/client_secret.json` and `secrets/token.json` are excluded from git via `.gitignore`. Never commit or share these files.
