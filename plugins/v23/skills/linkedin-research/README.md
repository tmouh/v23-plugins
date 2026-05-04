# LinkedIn Research Agent

AI-powered LinkedIn bulk research skill for V23. Navigates LinkedIn like a human using screenshot-based vision — no DOM scraping, no fragile selectors.

## Install

In Claude Cowork or Claude Code, install this plugin directly from GitHub:

```
tmouh/v23-plugins
```

Claude handles everything else automatically — finding the script, installing Node dependencies, launching Chrome, and running the agent.

## One-time requirement

The first time you run a research request, Claude will launch Chrome and open LinkedIn. **You just need to log in once.** After that, the session persists and Claude handles everything on its own.

If you don't have the **Windows MCP** plugin installed, Claude will ask you to install it from the marketplace — it's what lets Claude control your browser and run scripts.

---

## Usage

### 1. Prepare your contacts list

Create `Documents\Claude\research\scrape_input.json`:

```json
{
  "contacts": [
    { "name": "John Smith", "linkedin_url": "https://www.linkedin.com/in/johnsmith/" },
    { "name": "Jane Doe",   "linkedin_url": "https://www.linkedin.com/in/janedoe/" }
  ]
}
```

### 2. Ask Claude in plain English

> *"Research my contacts — get their current title, firm, and years in CRE"*

> *"Pull LinkedIn profiles for my list — full job history and whether they have a top-10 MBA"*

> *"Enrich my contacts with: current role, company, city, and recent post topics"*

Claude figures out which pages to visit, runs the screenshot agent, reads the results, and hands you a clean JSON or Excel file.

### 3. Get your results

Results land in `Documents\Claude\research\`:
- `scrape_output.json` — structured data per contact
- `scrape_output.xlsx` — Excel version (ask for it if you want it)

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Claude says "Windows MCP not found" | Install the Windows MCP plugin from the Cowork marketplace, then retry. |
| Chrome opens to LinkedIn login | Log into LinkedIn in that Chrome window — Claude will continue from there. |
| Contact returns `not_found` | LinkedIn URL is wrong or the profile was deleted. |
