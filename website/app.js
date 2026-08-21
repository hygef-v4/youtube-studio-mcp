/**
 * YouTube Studio MCP - Interactive Web Showcase Application
 * Author: hygef-v4
 */

// ============================================================================
// 1. 32 Tools Dataset
// ============================================================================
const TOOLS_DATA = [
  // Auth (2)
  {
    name: "youtube_auth_status",
    category: "auth",
    categoryLabel: "Auth",
    description: "Check if Google OAuth client secret and access tokens exist locally.",
    params: []
  },
  {
    name: "youtube_start_auth",
    category: "auth",
    categoryLabel: "Auth",
    description: "Generate OAuth authorization URL with PKCE and local helper command.",
    params: []
  },

  // Videos (7)
  {
    name: "youtube_channel_overview",
    category: "videos",
    categoryLabel: "Videos",
    description: "Retrieve channel branding, subscriber count, total views, and uploads playlist ID.",
    params: []
  },
  {
    name: "youtube_list_videos",
    category: "videos",
    categoryLabel: "Videos",
    description: "List recent uploaded videos with combined metadata and public view/like metrics.",
    params: [
      { name: "max_results", type: "int", required: false, default: "10" },
      { name: "page_token", type: "string", required: false }
    ]
  },
  {
    name: "youtube_get_video",
    category: "videos",
    categoryLabel: "Videos",
    description: "Inspect full snippet, statistics, category, and privacy status for one video.",
    params: [
      { name: "video_id", type: "string", required: true }
    ]
  },
  {
    name: "youtube_update_video",
    category: "videos",
    categoryLabel: "Videos",
    description: "Update title, description, tags list, category, language, or privacy status.",
    params: [
      { name: "video_id", type: "string", required: true },
      { name: "title", type: "string", required: false },
      { name: "tags", type: "array", required: false }
    ]
  },
  {
    name: "youtube_delete_video",
    category: "videos",
    categoryLabel: "Videos",
    description: "Permanently delete a video from your YouTube channel.",
    params: [
      { name: "video_id", type: "string", required: true }
    ]
  },
  {
    name: "youtube_upload_thumbnail",
    category: "videos",
    categoryLabel: "Videos",
    description: "Upload a local image file as a custom high-resolution video thumbnail.",
    params: [
      { name: "video_id", type: "string", required: true },
      { name: "image_path", type: "string", required: true }
    ]
  },
  {
    name: "youtube_upload_video",
    category: "videos",
    categoryLabel: "Videos",
    description: "Resumable upload of a local video (.mp4, .mov, .mkv) with metadata & tags.",
    params: [
      { name: "video_path", type: "string", required: true },
      { name: "title", type: "string", required: true },
      { name: "privacy_status", type: "enum", required: false, default: "private" }
    ]
  },

  // Playlists (7)
  {
    name: "youtube_list_playlists",
    category: "playlists",
    categoryLabel: "Playlists",
    description: "List all playlists on the authenticated channel.",
    params: [
      { name: "max_results", type: "int", required: false, default: "25" }
    ]
  },
  {
    name: "youtube_get_playlist",
    category: "playlists",
    categoryLabel: "Playlists",
    description: "List all video items contained inside a specific playlist.",
    params: [
      { name: "playlist_id", type: "string", required: true }
    ]
  },
  {
    name: "youtube_create_playlist",
    category: "playlists",
    categoryLabel: "Playlists",
    description: "Create a brand new playlist (public, unlisted, or private).",
    params: [
      { name: "title", type: "string", required: true },
      { name: "privacy_status", type: "enum", required: false, default: "public" }
    ]
  },
  {
    name: "youtube_update_playlist",
    category: "playlists",
    categoryLabel: "Playlists",
    description: "Modify playlist title, description, or visibility status.",
    params: [
      { name: "playlist_id", type: "string", required: true }
    ]
  },
  {
    name: "youtube_delete_playlist",
    category: "playlists",
    categoryLabel: "Playlists",
    description: "Delete an entire playlist from your channel.",
    params: [
      { name: "playlist_id", type: "string", required: true }
    ]
  },
  {
    name: "youtube_add_to_playlist",
    category: "playlists",
    categoryLabel: "Playlists",
    description: "Add a video to a specific playlist at a defined position index.",
    params: [
      { name: "playlist_id", type: "string", required: true },
      { name: "video_id", type: "string", required: true }
    ]
  },
  {
    name: "youtube_remove_from_playlist",
    category: "playlists",
    categoryLabel: "Playlists",
    description: "Remove a video entry from a playlist by playlist item ID.",
    params: [
      { name: "playlist_item_id", type: "string", required: true }
    ]
  },

  // Captions & Transcripts (5)
  {
    name: "youtube_list_captions",
    category: "captions",
    categoryLabel: "Captions",
    description: "Inspect available caption and subtitle tracks for a video.",
    params: [
      { name: "video_id", type: "string", required: true }
    ]
  },
  {
    name: "youtube_get_transcript",
    category: "captions",
    categoryLabel: "Captions",
    description: "Extract clean full spoken transcript, summary text, or timestamped segments.",
    params: [
      { name: "video_id", type: "string", required: true },
      { name: "language", type: "string", required: false },
      { name: "output_format", type: "enum", required: false, default: "text" }
    ]
  },
  {
    name: "youtube_bulk_get_transcripts",
    category: "captions",
    categoryLabel: "Captions",
    description: "Bulk extract transcripts from a list of video IDs, a playlist, or recent uploads.",
    params: [
      { name: "video_ids", type: "array", required: false },
      { name: "playlist_id", type: "string", required: false },
      { name: "output_dir", type: "string", required: false }
    ]
  },
  {
    name: "youtube_download_caption",
    category: "captions",
    categoryLabel: "Captions",
    description: "Download raw caption file (SRT, VTT, SBV) by caption ID.",
    params: [
      { name: "caption_id", type: "string", required: true },
      { name: "fmt", type: "enum", required: false, default: "srt" }
    ]
  },
  {
    name: "youtube_delete_caption",
    category: "captions",
    categoryLabel: "Captions",
    description: "Delete a caption track by ID.",
    params: [
      { name: "caption_id", type: "string", required: true }
    ]
  },

  // Analytics (5)
  {
    name: "youtube_channel_analytics",
    category: "analytics",
    categoryLabel: "Analytics",
    description: "Aggregate channel metrics (views, watch time, retention, subs) over custom date ranges.",
    params: [
      { name: "start_date", type: "string", required: true },
      { name: "end_date", type: "string", required: true }
    ]
  },
  {
    name: "youtube_video_analytics",
    category: "analytics",
    categoryLabel: "Analytics",
    description: "Daily time-series retention and watch time metrics for a specific video.",
    params: [
      { name: "video_id", type: "string", required: true },
      { name: "start_date", type: "string", required: true },
      { name: "end_date", type: "string", required: true }
    ]
  },
  {
    name: "youtube_analytics_traffic_sources",
    category: "analytics",
    categoryLabel: "Analytics",
    description: "Breakdown of views by traffic origin (Search, Suggested, Browse, External).",
    params: [
      { name: "start_date", type: "string", required: true },
      { name: "end_date", type: "string", required: true }
    ]
  },
  {
    name: "youtube_analytics_demographics",
    category: "analytics",
    categoryLabel: "Analytics",
    description: "Audience demographics breakdown by age group, gender, or geographic country.",
    params: [
      { name: "start_date", type: "string", required: true },
      { name: "end_date", type: "string", required: true }
    ]
  },
  {
    name: "youtube_analytics_top_videos",
    category: "analytics",
    categoryLabel: "Analytics",
    description: "Rank top performing videos by views and watch time for a date range.",
    params: [
      { name: "start_date", type: "string", required: true },
      { name: "end_date", type: "string", required: true },
      { name: "max_results", type: "int", required: false, default: "10" }
    ]
  },

  // Comments (4)
  {
    name: "youtube_list_comments",
    category: "comments",
    categoryLabel: "Comments",
    description: "List top-level comment threads ordered by relevance.",
    params: [
      { name: "video_id", type: "string", required: true },
      { name: "max_results", type: "int", required: false, default: "20" }
    ]
  },
  {
    name: "youtube_post_comment",
    category: "comments",
    categoryLabel: "Comments",
    description: "Post a top-level comment on one of your YouTube videos.",
    params: [
      { name: "video_id", type: "string", required: true },
      { name: "text", type: "string", required: true }
    ]
  },
  {
    name: "youtube_reply_comment",
    category: "comments",
    categoryLabel: "Comments",
    description: "Reply directly to an audience comment by parent comment ID.",
    params: [
      { name: "parent_id", type: "string", required: true },
      { name: "text", type: "string", required: true }
    ]
  },
  {
    name: "youtube_delete_comment",
    category: "comments",
    categoryLabel: "Comments",
    description: "Delete a comment by its unique comment ID.",
    params: [
      { name: "comment_id", type: "string", required: true }
    ]
  },

  // Search (2)
  {
    name: "youtube_search_videos",
    category: "search",
    categoryLabel: "Search",
    description: "Search videos across YouTube to analyze competitor titles, tags, and views.",
    params: [
      { name: "query", type: "string", required: true },
      { name: "order", type: "enum", required: false, default: "relevance" }
    ]
  },
  {
    name: "youtube_search_channels",
    category: "search",
    categoryLabel: "Search",
    description: "Search YouTube channels by topic or niche keyword.",
    params: [
      { name: "query", type: "string", required: true }
    ]
  }
];

// ============================================================================
// 2. Interactive Terminal Scenarios
// ============================================================================
const TERMINAL_SCENARIOS = {
  transcript: `
<div class="term-line"><span class="term-prompt">User ></span> Extract the spoken transcript of video <span class="term-cmd">cUP8vrApOlc</span> and summarize it.</div>
<div class="term-line"><span class="term-prompt">AI ></span> Calling <span class="term-tool">youtube_get_transcript(video_id="cUP8vrApOlc", output_format="text")</span>...</div>
<div class="term-output">
  <span class="term-success">✓ Transcript extracted (19 segments, Language: English ASR):</span><br><br>
  <em>"I'm gonna guess like I think Bakersfield is like a really Farm area, yes ah okay it was California but it was like closer to here. Am I zooming in on Watsonville? Oh my God, okay we're not zooming anymore! Oh my God, my location! Because when you get to the end screen... it'll take you to Google Maps which automatically shows your location..."</em>
</div>
<div class="term-line"><span class="term-prompt">AI ></span> <strong>Summary:</strong> The streamer was playing GeoGuessr in California and accidentally zoomed near her hometown (Watsonville), quickly stopping to avoid revealing her home location on livestream.</div>
`,
  overview: `
<div class="term-line"><span class="term-prompt">User ></span> How is my YouTube channel performing today?</div>
<div class="term-line"><span class="term-prompt">AI ></span> Calling <span class="term-tool">youtube_channel_overview()</span>...</div>
<div class="term-output">
  <span class="term-success">✓ Channel Data Retrieved:</span><br>
  • <strong>Channel:</strong> Chal7z (@chal7z)<br>
  • <strong>Subscribers:</strong> 938<br>
  • <strong>Total Uploads:</strong> 228 Videos (35 Public, 192 Unlisted, 1 Private)<br>
  • <strong>Public Views:</strong> 11,612<br>
  • <strong>Uploads Playlist:</strong> UUH0opG5MAF2Y5tleh3lSZ4Q
</div>
<div class="term-line"><span class="term-prompt">AI ></span> Your top public video is <em>SATURN - FREE PF</em> (7,708 views, 620 likes).</div>
`,
  analytics: `
<div class="term-line"><span class="term-prompt">User ></span> Where are most of my viewers finding my videos this month?</div>
<div class="term-line"><span class="term-prompt">AI ></span> Calling <span class="term-tool">youtube_analytics_traffic_sources(start_date="2026-08-01", end_date="2026-08-21")</span>...</div>
<div class="term-output">
  <span class="term-success">✓ Traffic Source Breakdown:</span><br>
  1. <strong>YouTube Search:</strong> 48.2% (Top search: <em>"valorant tips silver"</em>)<br>
  2. <strong>Suggested Videos:</strong> 31.5%<br>
  3. <strong>Browse Features:</strong> 14.1%<br>
  4. <strong>External Links:</strong> 6.2% (Discord, Reddit)
</div>
<div class="term-line"><span class="term-prompt">AI ></span> Search traffic is your strongest discovery driver. Adding structured timestamps in descriptions will further boost CTR.</div>
`,
  search: `
<div class="term-line"><span class="term-prompt">User ></span> Search top 3 competitor videos about 'Valorant rank up tips'.</div>
<div class="term-line"><span class="term-prompt">AI ></span> Calling <span class="term-tool">youtube_search_videos(query="Valorant rank up tips", order="viewCount", max_results=3)</span>...</div>
<div class="term-output">
  <span class="term-success">✓ Search Results (YouTube Global):</span><br>
  1. [td9kDW3iUqI] <em>How Raze Main REALLY warm up</em> — 2.1M views (supRAZE)<br>
  2. [IQNyOQ4fLEg] <em>These Silver VALORANT Lobbies are UNREAL</em> — 1.8M views (curry)<br>
  3. [X0_R1e-HSvA] <em>Iron to Radiant Speedrun</em> — 1.4M views (root)
</div>
<div class="term-line"><span class="term-prompt">AI ></span> Would you like me to extract their titles and tags to generate viral keyword recommendations for your next video?</div>
`
};

// ============================================================================
// 3. Config Generator Snippets
// ============================================================================
const CONFIG_SNIPPETS = {
  uvx: {
    filepath: "%APPDATA%\\Claude\\claude_desktop_config.json (Zero manual clone)",
    code: `{
  "mcpServers": {
    "youtube-studio": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/hygef-v4/youtube-studio-mcp.git",
        "youtube-studio-mcp"
      ],
      "env": {
        "YOUTUBE_CLIENT_SECRETS": "C:/path/to/secrets/client_secret.json",
        "YOUTUBE_TOKEN_FILE": "C:/path/to/secrets/token.json"
      }
    }
  }
}`
  },
  claude: {
    filepath: "%APPDATA%\\Claude\\claude_desktop_config.json",
    code: `{
  "mcpServers": {
    "youtube-studio": {
      "command": "python",
      "args": ["F:/code/git/youtube-studio-mcp/scripts/server.py"],
      "cwd": "F:/code/git/youtube-studio-mcp",
      "env": {
        "YOUTUBE_CLIENT_SECRETS": "F:/code/git/youtube-studio-mcp/secrets/client_secret.json",
        "YOUTUBE_TOKEN_FILE": "F:/code/git/youtube-studio-mcp/secrets/token.json"
      }
    }
  }
}`
  },
  cursor: {
    filepath: ".cursor/mcp.json or Cursor Settings > Features > MCP",
    code: `{
  "mcpServers": {
    "youtube-studio": {
      "command": "python",
      "args": ["./scripts/server.py"],
      "cwd": "\${workspaceFolder}",
      "env": {
        "YOUTUBE_CLIENT_SECRETS": "./secrets/client_secret.json",
        "YOUTUBE_TOKEN_FILE": "./secrets/token.json"
      }
    }
  }
}`
  },
  local: {
    filepath: "Terminal / PowerShell CLI",
    code: `# 1. Clone repository
git clone https://github.com/hygef-v4/youtube-studio-mcp.git
cd youtube-studio-mcp

# 2. Run OAuth 2.0 PKCE browser login
python scripts/auth.py auth

# 3. Test MCP server stdio directly
python scripts/server.py`
  }
};

// ============================================================================
// 4. DOM Initialization & Event Handlers
// ============================================================================
document.addEventListener("DOMContentLoaded", () => {
  initThemeToggle();
  initTerminal();
  initToolsDirectory();
  initConfigGenerator();
});

// 4.1 Theme Toggle
function initThemeToggle() {
  const themeToggleBtn = document.getElementById("themeToggle");
  const currentTheme = localStorage.getItem("yt_mcp_theme") || "light";
  document.documentElement.setAttribute("data-theme", currentTheme);

  themeToggleBtn.addEventListener("click", () => {
    const isDark = document.documentElement.getAttribute("data-theme") === "dark";
    const nextTheme = isDark ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", nextTheme);
    localStorage.setItem("yt_mcp_theme", nextTheme);
  });
}

// 4.2 Terminal Scenarios
function initTerminal() {
  const terminalOutput = document.getElementById("terminalOutput");
  const promptTabs = document.querySelectorAll(".prompt-tab");

  function renderScenario(scenarioKey) {
    terminalOutput.innerHTML = TERMINAL_SCENARIOS[scenarioKey] || TERMINAL_SCENARIOS.transcript;
  }

  renderScenario("transcript");

  promptTabs.forEach(tab => {
    tab.addEventListener("click", () => {
      promptTabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      const scenario = tab.getAttribute("data-scenario");
      renderScenario(scenario);
    });
  });
}

// 4.3 Tools Directory Filtering & Search
function initToolsDirectory() {
  const toolsGrid = document.getElementById("toolsGrid");
  const searchInput = document.getElementById("toolSearchInput");
  const pillBtns = document.querySelectorAll(".pill-btn");

  let activeCategory = "all";
  let searchQuery = "";

  function renderTools() {
    const filtered = TOOLS_DATA.filter(tool => {
      const matchCat = activeCategory === "all" || tool.category === activeCategory;
      const matchQuery = !searchQuery || 
        tool.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
        tool.description.toLowerCase().includes(searchQuery.toLowerCase());
      return matchCat && matchQuery;
    });

    if (filtered.length === 0) {
      toolsGrid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 3rem; color: var(--text-muted);">
          <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">No tools found matching "${searchQuery}"</p>
          <span style="font-size: 0.9rem;">Try searching for <code>transcript</code>, <code>analytics</code>, <code>upload</code>, or <code>playlist</code>.</span>
        </div>
      `;
      return;
    }

    toolsGrid.innerHTML = filtered.map(tool => `
      <div class="tool-card">
        <div class="tool-header">
          <span class="tool-name">${tool.name}</span>
          <span class="tool-badge">${tool.categoryLabel}</span>
        </div>
        <p class="tool-desc">${tool.description}</p>
        <div class="tool-params">
          ${tool.params.length > 0 ? tool.params.map(p => `
            <span class="param-tag ${p.required ? 'required' : ''}">
              ${p.name}${p.required ? '*' : ''}: ${p.type}
            </span>
          `).join('') : '<span class="param-tag">No parameters</span>'}
        </div>
      </div>
    `).join('');
  }

  renderTools();

  searchInput.addEventListener("input", (e) => {
    searchQuery = e.target.value.trim();
    renderTools();
  });

  pillBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      pillBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeCategory = btn.getAttribute("data-category");
      renderTools();
    });
  });
}

// 4.4 Config Generator & Copy Button
function initConfigGenerator() {
  const configTabs = document.querySelectorAll(".config-tab-btn");
  const configFilePath = document.getElementById("configFilePath");
  const configCodeDisplay = document.getElementById("configCodeDisplay");
  const copyBtn = document.getElementById("copyConfigBtn");

  let currentTarget = "uvx";

  function renderConfig(targetKey) {
    const config = CONFIG_SNIPPETS[targetKey] || CONFIG_SNIPPETS.uvx;
    configFilePath.textContent = config.filepath;
    configCodeDisplay.textContent = config.code;
    currentTarget = targetKey;
  }

  renderConfig("uvx");

  configTabs.forEach(tab => {
    tab.addEventListener("click", () => {
      configTabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      const target = tab.getAttribute("data-target");
      renderConfig(target);
    });
  });

  copyBtn.addEventListener("click", () => {
    const config = CONFIG_SNIPPETS[currentTarget] || CONFIG_SNIPPETS.uvx;
    navigator.clipboard.writeText(config.code).then(() => {
      const originalText = copyBtn.innerHTML;
      copyBtn.innerHTML = `
        <svg viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2" class="copy-icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
        </svg>
        <span style="color: #22c55e;">Copied to Clipboard!</span>
      `;
      setTimeout(() => {
        copyBtn.innerHTML = originalText;
      }, 2000);
    });
  });
}
