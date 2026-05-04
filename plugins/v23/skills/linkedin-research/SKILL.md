---
name: linkedin-research
description: >
  AI-powered LinkedIn bulk research agent. Uses vision-based browser automation
  to navigate LinkedIn like a human — takes screenshots of real browser pages,
  then uses Claude's vision to extract whatever fields you ask for in plain
  English. No DOM parsing, no fragile selectors. Always use this skill when
  the user asks to research LinkedIn profiles, pull contact info from LinkedIn,
  enrich a contact list, find someone's job history, or anything involving
  "scrape LinkedIn", "research contacts", "LinkedIn profiles", or "who is X on LinkedIn".
---

# LinkedIn Research Agent

A vision-based research agent. Browser automation takes screenshots of your live, logged-in Chrome browser. Claude reads those screenshots like a human would — no DOM scraping, no fragile selectors. Whatever LinkedIn looks like today is what Claude reads.

## How to invoke

You need two things:
1. **Contacts list**: `research/scrape_input.json` with LinkedIn URLs (in the user's Documents\Claude folder)
2. **Fields request**: plain English — *"get their current title, firm, years in CRE, and any Ivy League education"*

If the user doesn't specify a fields request, ask: *"What information do you want extracted from each profile?"*

---

## LinkedIn page map

Use this map to decide which pages to visit — visit only what's needed for the requested fields.

| Page | Key | What it contains |
|------|-----|-----------------|
| Main profile | `main` | Name, headline, location, about summary, featured section, top 2-3 experience/education entries, follower count |
| Full experience | `experience` | Complete job history — all roles, companies, date ranges, descriptions |
| Full education | `education` | All schools, degrees, fields of study, graduation years |
| Skills | `skills` | Skills list with endorsement counts |
| Recent activity | `activity` | Recent posts, articles, comments, shares |
| Recommendations | `recommendations` | Received and given recommendations with full text |

**Mapping rules:**
- Current title / firm / headline / about / location → `main` only
- Full career history / all previous jobs / tenure → `experience`
- Schools / degrees / MBA / undergrad → `education`
- What they post about / recent deals mentioned → `activity`
- Skills / expertise → `skills`
- Reputation / testimonials → `recommendations`

---

## Phase 1: Parse the request

Read the user's fields request and decide which pages to visit:

```json
{
  "fields_requested": "the user's original text",
  "fields": ["current_title", "current_firm", ...],
  "pages_to_visit": ["main", "experience"]
}
```

Be minimal — only include pages actually needed.

---

## Phase 2: Environment setup (Claude handles all of this)

Claude takes care of every setup step using the Windows MCP PowerShell tool. The only thing that ever requires a human is logging into LinkedIn the very first time.

### Check for Windows MCP access

Before doing anything, verify the `mcp__Windows-MCP__PowerShell` tool is available in your tool list.

If it is **not** available, call `mcp__mcp-registry__suggest_connectors` with:
- `uuids: ["Windows-MCP"]`
- `keywords: ["automation"]`

This renders an inline Connect button — do not describe it in text, just call the tool. Then stop and wait for the user to connect it before proceeding.

Do not proceed without Windows MCP. All of Phase 2 depends on it.

### Step 1 — Find the skill's scripts directory

The skill is installed somewhere on the user's machine. Find the `scrape_screenshots.js` script path — it lives in the `scripts/` subfolder of wherever this skill was installed (e.g., `%USERPROFILE%\Documents\Claude\.claude\plugins\v23-plugins\skills\linkedin-research\scripts`). Use PowerShell to locate it:

```powershell
$skillScript = Get-ChildItem -Path "$env:USERPROFILE" -Recurse -Filter "scrape_screenshots.js" -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
Write-Host $skillScript
```

### Step 2 — Install Node dependencies if missing

```powershell
$scriptDir = Split-Path $skillScript
if (-not (Test-Path "$scriptDir\node_modules\puppeteer-core")) {
    Write-Host "Installing dependencies (first time only)..."
    Push-Location $scriptDir
    npm install
    Pop-Location
}
```

### Step 3 — Ensure Chrome is running with debug port

Check if the CDP endpoint is live. If not, launch Chrome automatically:

```powershell
$cdpLive = $false
try {
    $wc = New-Object System.Net.WebClient
    $wc.DownloadString("http://127.0.0.1:9222/json/version") | Out-Null
    $cdpLive = $true
} catch {}

if (-not $cdpLive) {
    Write-Host "Launching Chrome with debug port..."
    Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" `
        -ArgumentList "--remote-debugging-port=9222","--user-data-dir=$env:USERPROFILE\remote-debug","--no-first-run","--no-default-browser-check","https://www.linkedin.com"
    Start-Sleep 4  # give Chrome time to start
    
    # Verify it came up
    try {
        $wc = New-Object System.Net.WebClient
        $wc.DownloadString("http://127.0.0.1:9222/json/version") | Out-Null
        Write-Host "Chrome ready."
    } catch {
        Write-Host "ERROR: Chrome didn't start with debug port. Is the user logged into LinkedIn in their remote-debug profile?"
        # Stop and ask the user to open Chrome manually and log in, then retry
    }
}
```

> **If Chrome starts but shows the LinkedIn login page:** the session expired. Tell the user to log back into LinkedIn in that Chrome window, then rerun. This is the only step Claude cannot do on the user's behalf.

### Step 4 — Ensure research output directory exists

```powershell
$research = "$env:USERPROFILE\Documents\Claude\research"
if (-not (Test-Path $research)) { New-Item -ItemType Directory -Path $research | Out-Null }
```

---

## Phase 3: Run the screenshot agent

Launch the script in the background (it can take a few minutes for large batches):

```powershell
$pages = "main,experience"  # from Phase 1 output — comma-separated page keys

# Remove stale manifest from any previous run
$manifest = "$research\screenshots\manifest.json"
if (Test-Path $manifest) { Remove-Item $manifest -Force }

Start-Process -FilePath "cmd.exe" `
  -ArgumentList "/c node `"$skillScript`" `"$research\scrape_input.json`" `"$research\screenshots`" `"$pages`" > `"$research\screenshot_log.txt`" 2>&1" `
  -WindowStyle Hidden

Write-Host "Screenshot agent running..."
```

Poll until the manifest appears:

```powershell
$timeout = 300  # seconds
$elapsed = 0
while (-not (Test-Path $manifest) -and $elapsed -lt $timeout) {
    Start-Sleep 5
    $elapsed += 5
    Write-Host "Waiting... ($elapsed s)"
}
if (Test-Path $manifest) { Write-Host "Done." } else { Write-Host "Timed out — check screenshot_log.txt" }
```

### What the script produces

```
research/screenshots/
  manifest.json
  John_Smith/
    main_001.png  main_002.png  main_003.png
    experience_001.png  experience_002.png
  Jane_Doe/
    main_001.png  ...
```

---

## Phase 4: Extract fields from screenshots

Read `research/screenshots/manifest.json` to get each contact's screenshot file paths.

For each contact, use the Read tool on every screenshot image. Read ALL screenshots for a contact before extracting — profiles span multiple screenshots. If a field isn't visible in any screenshot, record it as `null`.

**What to look for:**
- **Main profile**: header = name/headline/location, middle = about, bottom = experience/education previews
- **Experience page**: each role is a card — company, title, date range, description
- **Education page**: each school is a card — institution, degree, years
- **Activity page**: stacked posts — note recurring topics and themes

Build a result per contact:
```json
{
  "name": "John Smith",
  "linkedin_url": "https://linkedin.com/in/johnsmith",
  "status": "success",
  "data": {
    "current_title": "Managing Director",
    "current_firm": "Blackstone",
    "years_in_cre": 14
  }
}
```

Use field names from the user's request (snake_case). Contacts flagged with errors in the manifest get `"status": "not_found"` or `"status": "auth_required"`.

---

## Phase 5: Output

Write `research/scrape_output.json`:
```json
{
  "extracted_at": "ISO timestamp",
  "fields_requested": "user's original request",
  "stats": { "total": 10, "success": 9, "failed": 1 },
  "contacts": [ ...per-contact results... ]
}
```

If the user wants Excel, use the xlsx skill to produce `research/scrape_output.xlsx` with one row per contact.

Tell the user where their files are and briefly summarize results (e.g., *"9/10 contacts extracted — 1 profile not found"*).

---

## Troubleshooting

**"CDP connection refused" after Chrome launch** → Chrome may have opened without the debug port. Close all Chrome windows and rerun — Phase 2 will relaunch it correctly.

**Chrome opens to LinkedIn login** → Session expired. User needs to log back in manually (one time), then rerun.

**Manifest missing contacts** → Check `research/screenshot_log.txt` for per-contact errors.

**Profile data is sparse** → Some users keep minimal LinkedIn profiles. Extract what's visible, mark missing fields `null`.
