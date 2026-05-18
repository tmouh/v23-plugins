---
name: om-builder
description: "Generate a copy-paste prompt for Claude in PowerPoint to build a Vanadium-style commercial real estate Offering Memorandum (OM). Use when the user says 'build the OM', 'create an OM', 'generate offering memorandum', 'make an OM for a deal', or points at a SharePoint-synced deal folder under the 1- Realty / 1- Deals path and is ready to produce a deck. Output is a single pasteable prompt that handles file access via Microsoft 365 MCP, applies the Vanadium house style with a full layout repertoire, and offers a template-upload vs. default-style branch."
---

# v23-om-builder

## Overview

When V23 is ready to produce an Offering Memorandum, this skill generates a single copy-paste prompt for Claude in PowerPoint. The prompt:

- Includes a refusal-prevention preamble (Claude in PowerPoint must not refuse on "cannot access local files" before checking 365 MCP tools)
- Embeds Microsoft Graph driveItem URIs for every source file in the deal folder
- Applies the **Vanadium house style** (Garamond + Aptos, navy + pale-blue palette, hairline rules, source lines) — derived from the most recent Vanadium OM in production (105 N 13th Street, April 2026)
- Includes a full **layout repertoire** (single-narrative, KPI strip, half-and-half, photo grid, map-dominant, table, chart, two-column comparison, investment-highlights pattern, full-bleed visual, section divider, hybrid) with rules on when each layout is optimal
- Branches on template: asks the user whether to upload a template (which routes to `/adobe-for-creativity/adobe-design-from-template`) OR use the default Vanadium style baked in

This skill does NOT build the deck. It builds the **prompt** that Claude in PowerPoint uses to build the deck live.

## When to use

- User asks to build, create, or generate an OM
- User points at a SharePoint-synced deal folder
- User has completed the underwriting and is ready for deck production

Do NOT use for:
- Re-styling an existing deck (use a different prompt)
- Building one-pagers or teasers (different artifact)
- Direct deck construction in Claude Code (Claude in PowerPoint does the live work)

## Runbook

### Step 1 — Resolve the deal folder

Ask the user for the deal folder path if not given. Path typically looks like:
`C:\Users\<user>\Vanadium Group LLC\V23 - Database\1- Realty\1- Deals\<Deal Folder>`

Validate:
- Folder exists
- Contains source files (PDF, xlsx, docx, html, png/jpg)
- Lives under a SharePoint sync root (so Graph URIs can be resolved)

If validation fails, stop and tell the user what's wrong. Do not proceed.

### Step 2 — List folder contents

Enumerate files in the deal folder. Filter to relevant source file types:
- `.pdf` (investment summaries, comps, articles, dashboards, renderings)
- `.xlsx` / `.xls` (underwriting model, rent roll)
- `.docx` / `.doc` (sponsor notes)
- `.pptx` (templates, prior decks — may be present but not used as source)
- `.html` (dashboards)
- `.png` / `.jpg` (photos)

Group files by likely role for the output: dashboard/numbers, narrative summaries, model, photos, articles/context.

### Step 3 — Resolve Microsoft Graph URIs for each file

For each file, look up its Microsoft Graph driveItem URI using the 365 MCP connector. The two SharePoint MCP tools to use:
- `sharepoint_search` — search by name and location
- `sharepoint_folder_search` — search within a folder

The Graph URI format is:
`file:///<driveId>/<itemId>`

Where:
- `<driveId>` looks like `b!Uou3HdWer0eCUXRGrrncSRgdwoH5N7tAhDE1U97uucCBdYSc3MbQSbzJvy0Hi16f`
- `<itemId>` looks like `01RMD2GBZAVZ5JVO2QXJB2JRRMUYMQO2KO`

Known V23 driveIds:
- **Main Realty drive** (most deal files): `b!Uou3HdWer0eCUXRGrrncSRgdwoH5N7tAhDE1U97uucCBdYSc3MbQSbzJvy0Hi16f`
- **Teams Chat Files drive** (files shared in Teams chats): `b!9nw1VCgBm0yQN0OLVey8mmJy_K7tqPtMgn2m8KBKbMR1QnXIybjzTruGy_FJwZlD`

Group files by drive in the output for clarity.

If the MCP tool is unavailable in the current session OR a lookup fails for a specific file, DO NOT fabricate a URI. Tell the user which file(s) couldn't be resolved and offer:
- Manual URI lookup and paste-in
- Re-running the skill in a session where MCP is available

### Step 4 — Pull a brief asset description

Open the deal folder's underwriting dashboard PDF or investment summary PDF (whichever is most recent). Extract a 1-2 sentence asset description containing:
- Total SF
- Address / city
- Sponsor name
- Anticipated offer / purchase price
- Equity ask

This single brief is for context only — Claude in PowerPoint will read the source files for the full deal. Do not paste extracted financials into the prompt beyond this.

### Step 5 — Assemble the pasteable prompt

Read `prompt-template.md` and `layout-repertoire.md` from this skill's folder. Substitute these placeholders in `prompt-template.md`:

| Placeholder | What to substitute |
|---|---|
| `{{DEAL_CODENAME}}` | Short codename for the footer (e.g., "Project Exchange", "Project N13") |
| `{{DEAL_FULL_NAME}}` | Full property/deal name as it should appear in the footer attribution (e.g., "TheExchange — 77 Center Drive") |
| `{{DEAL_FOLDER_DISPLAY}}` | Folder name as it appears under `\1- Realty\1- Deals\` |
| `{{ASSET_BRIEF}}` | The 1-2 sentence asset description from Step 4 |
| `{{FILE_LIST_BLOCK}}` | Formatted list of files with their Graph URIs, grouped by drive (format below) |
| `{{LAYOUT_REPERTOIRE}}` | Full contents of `layout-repertoire.md` inserted verbatim |

`{{FILE_LIST_BLOCK}}` format:

```
The first N files live on the main Realty drive `b!Uou3HdWer0eCUXRGrrncSRgdwoH5N7tAhDE1U97uucCBdYSc3MbQSbzJvy0Hi16f`. [If applicable: Other files live on the Teams Chat Files drive `b!9nw1VCgBm0yQN0OLVey8mmJy_K7tqPtMgn2m8KBKbMR1QnXIybjzTruGy_FJwZlD`.] These are Graph resource URIs:

- <File name 1> → file:///<driveId>/<itemId>
- <File name 2> → file:///<driveId>/<itemId>
[...]
```

Do NOT substitute deal numerics (NOI, IRR, returns, rent roll) into the prompt. Claude in PowerPoint must extract these from the source files at build time so the numbers stay in sync with whatever the sources actually say.

### Step 6 — Print to user

Output structure:

```
═══ READY: paste this into Claude in PowerPoint ═══

How to use:
1. Open PowerPoint with the deal materials nearby
2. Open Claude in PowerPoint (right-hand pane)
3. Copy everything between the COPY markers below
4. Paste into Claude in PowerPoint
5. Claude in PowerPoint will FIRST verify file access, THEN ask if you want to upload a template — answer accordingly
6. Review the section depth plan it proposes before letting it build past the executive summary

━━━━ COPY FROM HERE ━━━━

<the filled prompt — prompt-template.md with all placeholders substituted, with layout-repertoire.md inserted at {{LAYOUT_REPERTOIRE}}>

━━━━ END COPY ━━━━
```

If any files couldn't be resolved to Graph URIs, list them above the COPY block:

```
⚠ Could not resolve Graph URIs for these files. Look them up manually before pasting:
  - <filename>
```

## Safety rules

- Never fabricate a Graph URI. If lookup fails, surface the failure to the user.
- Never substitute deal numerics into the prompt itself. Numerics come from sources at deck-build time.
- Always preserve the refusal-prevention preamble at the top of the prompt.
- Always preserve the template-decision branch (Step 2 in the prompt) — the user must be given the upload-template vs. default-Vanadium choice.
- Do not edit `prompt-template.md` or `layout-repertoire.md` as part of running the skill. Those are versioned reference; edit them as a separate task and bump the plugin version when you do.

## Updating the Vanadium style or layout repertoire

If the user wants to refine the Vanadium house style (new fonts, new colors, new section spine) or extend the layout repertoire:

1. Edit `prompt-template.md` (for design system, section spine, voice principles)
2. Edit `layout-repertoire.md` (for layout-specific guidance, new layouts)
3. Bump the plugin version in `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`
4. Commit so clients pick up the change on the next plugin update

The canonical Vanadium house style is derived from the 105 N 13th Street OM (April 2026 production version). If a future OM diverges and becomes the new reference, update the comment at the top of `prompt-template.md` accordingly.
