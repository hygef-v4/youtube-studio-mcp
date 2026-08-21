# User Stories

## Overview
This document specifies the user stories and acceptance criteria for the **YouTube Studio MCP** system, following the **INVEST** principles (Independent, Negotiable, Valuable, Estimable, Small, Testable).

---

## Epic 1: Authentication & Credential Lifecycle

### `US-AUTH-01`: Local OAuth Setup & Authentication Verification
- **As a**: Solo Content Creator (Alex)
- **I want to**: Verify whether my local OAuth credentials and token exist
- **So that**: I know if I need to run the authorization setup before querying YouTube data
- **Primary Persona**: Alex
- **Traceability**: `FR-AUTH-01`, `FR-TOOL-01`
- **Acceptance Criteria**:
  ```gherkin
  Scenario: Credentials and tokens exist
    Given the file "secrets/client_secret.json" exists
    And the file "secrets/token.json" exists
    When the assistant invokes "youtube_auth_status"
    Then the response returns "client_secrets_exists" as true
    And the response returns "token_exists" as true

  Scenario: Credentials missing
    Given the file "secrets/client_secret.json" does not exist
    When the assistant invokes "youtube_auth_status"
    Then the response returns "client_secrets_exists" as false
  ```

---

### `US-AUTH-02`: Transparent Access Token Auto-Refresh
- **As an**: Autonomous AI Assistant (Claude / Codex)
- **I want to**: Automatically refresh expired access tokens using the stored refresh token
- **So that**: Long-running agent conversations are never interrupted by authentication errors
- **Primary Persona**: Claude / Codex
- **Traceability**: `FR-AUTH-03`
- **Acceptance Criteria**:
  ```gherkin
  Scenario: Access token near expiration
    Given the current access token is within 120 seconds of expiry
    When any YouTube API tool is called
    Then the system automatically sends a refresh grant to "https://oauth2.googleapis.com/token"
    And updates "secrets/token.json" with the new access token and timestamp
    And proceeds with the original API call seamlessly without error
  ```

---

## Epic 2: Channel & Video Catalog Inspection

### `US-DISC-01`: Channel Overview Inspection
- **As a**: Solo Content Creator (Alex)
- **I want to**: Ask the AI assistant to summarize my channel's public metrics and profile
- **So that**: I can get a quick snapshot of my subscriber count, total views, and video catalog
- **Primary Persona**: Alex
- **Traceability**: `FR-TOOL-03`
- **Acceptance Criteria**:
  ```gherkin
  Scenario: Successfully fetch channel overview
    Given valid OAuth credentials with YouTube Data API access
    When the assistant invokes "youtube_channel_overview"
    Then the response returns channel title, customUrl, subscriberCount, viewCount, and videoCount
    And returns the ID of the uploads playlist
  ```

---

### `US-DISC-02`: Paginated Recent Uploads Retrieval
- **As a**: Channel Manager (Sarah)
- **I want to**: List the most recent videos with combined statistics and privacy statuses
- **So that**: I can review recent uploads and decide which ones need optimization
- **Primary Persona**: Sarah
- **Traceability**: `FR-TOOL-04`, `FR-TOOL-05`
- **Acceptance Criteria**:
  ```gherkin
  Scenario: Fetch 5 most recent videos
    Given the channel has published videos
    When the assistant invokes "youtube_list_videos" with "max_results" set to 5
    Then the response contains an array of 5 video items
    And each item includes snippet metadata, viewCount, likeCount, and privacyStatus
  ```

---

## Epic 3: Video Optimization & Metadata Management

### `US-META-01`: Video Metadata & Tag Updates
- **As a**: Solo Content Creator (Alex)
- **I want to**: Update video title, description, tags, category, and privacy status via natural language
- **So that**: I can optimize my video SEO without manually editing fields in YouTube Studio web UI
- **Primary Persona**: Alex
- **Traceability**: `FR-TOOL-06`
- **Acceptance Criteria**:
  ```gherkin
  Scenario: Update video tags and title
    Given a valid "video_id"
    When the assistant invokes "youtube_update_video" with updated "tags" and "title"
    Then the YouTube Data API is called with PUT /videos?part=snippet,status
    And the returned video resource reflects the new title and tags
  ```

---

## Epic 4: Visual Asset Management

### `US-THUMB-01`: Local Thumbnail Image Upload
- **As a**: Solo Content Creator (Alex)
- **I want to**: Specify a local image file path on my machine and set it as my video thumbnail
- **So that**: I can publish custom thumbnail artwork directly through my AI workflow
- **Primary Persona**: Alex
- **Traceability**: `FR-TOOL-07`
- **Acceptance Criteria**:
  ```gherkin
  Scenario: Upload valid PNG/JPEG thumbnail
    Given a valid local image file path "C:/path/to/thumb.png"
    And a valid "video_id"
    When the assistant invokes "youtube_upload_thumbnail"
    Then the image MIME type is resolved
    And the binary file is streamed to "https://www.googleapis.com/upload/youtube/v3/thumbnails/set"
    And the response confirms the thumbnail upload with URL endpoints
  ```

---

## Epic 5: Analytics & Growth Auditing

### `US-ANALYTICS-01`: Channel Date-Range Performance Report
- **As a**: Channel Manager (Sarah)
- **I want to**: Extract aggregated channel analytics between two dates
- **So that**: I can analyze overall channel growth, watch time, and subscriber retention
- **Primary Persona**: Sarah
- **Traceability**: `FR-TOOL-08`
- **Acceptance Criteria**:
  ```gherkin
  Scenario: Query 28-day channel analytics
    Given valid "start_date" (YYYY-MM-DD) and "end_date" (YYYY-MM-DD)
    When the assistant invokes "youtube_channel_analytics"
    Then the response returns views, estimatedMinutesWatched, averageViewDuration, likes, comments, shares, and subscriber deltas
  ```

---

### `US-ANALYTICS-02`: Video Daily Retention & Performance Time-Series
- **As a**: Solo Content Creator (Alex)
- **I want to**: Inspect daily view and watch time metrics for a specific video
- **So that**: I can see how my latest release is trending day by day
- **Primary Persona**: Alex
- **Traceability**: `FR-TOOL-09`
- **Acceptance Criteria**:
  ```gherkin
  Scenario: Query per-day video analytics
    Given a valid "video_id", "start_date", and "end_date"
    When the assistant invokes "youtube_video_analytics"
    Then the response returns day-by-day rows with views, watch time, likes, and subscribers gained
  ```

---

## Epic 6: Audience Engagement & Community

### `US-COMMUNITY-01`: Top-Level Comment Thread Reading & Publishing
- **As a**: Solo Content Creator (Alex)
- **I want to**: Read audience comments and post new comments on my videos
- **So that**: I can engage with my community directly from my AI assistant
- **Primary Persona**: Alex
- **Traceability**: `FR-TOOL-10`, `FR-TOOL-11`
- **Acceptance Criteria**:
  ```gherkin
  Scenario: List video comments
    Given a valid "video_id"
    When the assistant invokes "youtube_list_comments"
    Then the response returns a list of top-level comment threads ordered by relevance

  Scenario: Post a comment
    Given a valid "video_id" and non-empty "text"
    When the assistant invokes "youtube_post_comment"
    Then a new comment thread is created on YouTube
    And the response returns the created comment snippet and ID
  ```
