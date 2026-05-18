---
name: om-builder-help
description: Use when the user asks for help with the om-builder workflow — phrases like 'om-builder help', 'omcreator help', 'om creator help', 'how does the OM builder work', 'what does the OM builder need', 'om-builder prereqs', 'om-builder setup', 'what do I need to build an OM', 'om-builder docs', or any meta question about prerequisites, caveats, troubleshooting, or extending the OM-creation pipeline. Returns a comprehensive guide covering what the skill does, prerequisites, step-by-step flow, what the pasteable prompt does in Claude in PowerPoint, known caveats and limitations, troubleshooting, and how to update or extend.
---

# v23-om-builder-help

When the user invokes help on the om-builder workflow, present the guide below. Keep it intact — the user wants the full reference, not a summary.

---

# Vanadium OM Builder — Help & Reference

## What is the OM Builder?

`v23:om-builder` is a skill that generates a copy-paste prompt for **Claude in PowerPoint** to build a Vanadium-style commercial real estate Offering Memorandum from a SharePoint-synced deal folder.

The skill itself runs in **Claude Code**, not in PowerPoint. It produces one block of text you paste into Claude in PowerPoint's chat panel, which then drives the live deck build.

It encodes the lessons from prior Vanadium OM productions — canonical reference is the **105 N 13th Street OM (April 2026)** — including the house design system, layout repertoire, voice principles, and anti-AI guardrails.

## How to invoke

In Claude Code, say one of these (or natural variants):
- "Build the OM for [deal name or folder]"
- "Create an OM for [deal]"
- "Generate offering memorandum for [deal folder]"
- "Make an OM for [deal]"

For help (this guide):
- "om-builder help"
- "omcreator help"
- "how does the OM builder work"
- "what does the OM builder need"

## Prerequisites

### Required

1. **V23 plugin version ≥ 3.4.0** in Claude Code. Run your plugin-update flow if you're on an older version. The skill won't appear until updated.

2. **Deal folder must be SharePoint-synced locally.** Path typically:
   `C:\Users\<you>\Vanadium Group LLC\V23 - Database\1- Realty\1- Deals\<Deal Folder>`
   Online-only folders won't work — the skill needs to enumerate files locally.

3. **Source files in the deal folder.** At minimum:
   - Underwriting dashboard PDF (returns, cap stack, NOI trajectory)
   - Underwriting model xlsx
   - Investment summary PDF (narrative voice)
   
   Quality improves with:
   - Asset photos
   - Floor plans / renderings
   - Comp lease/sale documents
   - Sponsor track record materials
   - Market articles for context

4. **Microsoft 365 MCP connector** enabled in your Claude Code session. The skill uses `sharepoint_search` and `sharepoint_folder_search` to look up Graph driveItem URIs. If MCP isn't available, the skill surfaces unresolved files for manual lookup rather than fabricating URIs.

5. **Claude in PowerPoint** open in the PowerPoint app where you'll build the deck.

### Optional

6. **`/adobe-for-creativity/adobe-design-from-template`** skill installed in Claude in PowerPoint — only needed if you upload a custom template. If you take the default Vanadium route, this isn't required.

7. **A template .pptx file** — only if you choose the upload path.

## How it works (step-by-step)

### In Claude Code (the om-builder skill)

1. **Resolve deal folder.** Identifies the folder you mean; asks if ambiguous.
2. **List source files.** Filters to PDF, xlsx, docx, pptx, html, images.
3. **Look up Graph URIs.** Queries Microsoft Graph via 365 MCP per file. Composes URIs as `file:///<driveId>/<itemId>`. Known V23 driveIds (Realty + Teams Chat Files) are baked in.
4. **Pull asset brief.** Reads the dashboard or investment summary for a 1-2 sentence asset description (SF, location, sponsor, ask).
5. **Assemble pasteable prompt.** Fills `prompt-template.md` placeholders, inserts `layout-repertoire.md` at `{{LAYOUT_REPERTOIRE}}`, prints with copy markers.

### In Claude in PowerPoint (after you paste)

6. **Step 0 — File access verification.** Opens every file via Graph URIs and reports one concrete detail per file proving it actually read it.
7. **Step 2 — Template decision (BLOCKING).** Asks: "Upload a template or default to Vanadium style?" Waits for your answer.
8. **Step 4 — Design system setup** (if default chosen). Applies Vanadium master: Garamond + Aptos fonts, navy + pale-blue palette with exact hex codes, 60pt margin grid, footer bar.
9. **Cover + Executive Summary.** Drafts, pauses for sign-off.
10. **Section depth plan.** Proposes layout (from the 12-layout repertoire) per section with flex slide counts. Pauses for sign-off.
11. **Section-by-section build.** Builds each section, pauses for review.
12. **QA pass.** Runs 30-item checklist before declaring done.

## What the pasteable prompt contains

10 steps, ~4,900 words total:

| Step | Purpose |
|---|---|
| 0 | File access and verification |
| 1 | Mission + three governing rules (slide count not a target, layout not fixed, no fabrication) |
| 2 | Template decision (blocking question) |
| 3 | Source priority (dashboard wins on numbers) |
| 4 | Vanadium house design system |
| 5 | Layout repertoire (12 layouts with when/structure/why/DO/DON'T) |
| 6 | OM section spine (29 canonical sections, content-driven count) |
| 7 | Voice and copy principles |
| 8 | Anti-AI guardrails |
| 9 | Process (build sequence with checkpoints) |
| 10 | QA checklist (30 items) |

## Known caveats and limitations

### MCP and file access

- **MCP availability is per-session.** If the 365 MCP isn't loaded in your Claude Code session, Graph URI lookup fails. The skill surfaces unresolved files rather than fabricating URIs. Workaround: look them up manually in SharePoint or re-run from a session with MCP enabled.
- **SharePoint sync must be current.** Files added but not yet synced down won't appear.
- **Two known V23 drives** are baked in (main Realty + Teams Chat Files). If a deal uses a third drive (e.g., a sponsor's own SharePoint), the skill needs to be updated to know it.
- **Refusal preamble doesn't always defeat Claude in PowerPoint refusals.** The pasteable prompt's Step 0 includes language telling Claude in PowerPoint not to refuse on "can't access local files" before checking 365 MCP. If it still refuses, the MCP isn't loaded in PowerPoint either — you can either enable it or ask Claude in PowerPoint to open files one at a time as you reference them.

### Source files

- **Excel parsing is limited in Claude in PowerPoint.** Office.js can't fully parse complex xlsx OOXML. For dense rent rolls and line-item models, Claude in PowerPoint may need to default to "TBD — confirm with sponsor" rather than extract everything. This is by design — better to flag than fabricate.
- **Image-only PDFs have no extractable text.** Renderings and floor plans get inserted as visuals; Claude in PowerPoint can't read text inside them.
- **Stale source files = stale OM.** The skill doesn't validate file recency. If the dashboard is 2 months old and the deal has moved, the OM reflects the old numbers. Refresh the dashboard before running.

### Style and content

- **Canonical style is locked to 105 N 13th OM (April 2026).** Future Vanadium OMs may evolve the house style. To update, edit `prompt-template.md` and `layout-repertoire.md` in `<plugin>/skills/om-builder/` and bump the plugin version.
- **Vanadium hex codes are inferred from 105 N 13th, not from an official brand style guide.** They match the production reference. If Vanadium has an official palette with different exact values, edit `prompt-template.md`.
- **Font fallback risk.** Garamond and Aptos are specified. Aptos is the Microsoft 365 default (replaced Calibri in 2024) so it should be present. Garamond may not be installed on every system; PowerPoint will substitute (often with Times New Roman or a similar serif). If you need a specific Garamond variant (EB Garamond, Adobe Garamond Pro, etc.), edit the template.
- **Footer attribution is hardcoded to "Vanadium Realty | [Deal Name]".** If V23's role on a deal is different (acquisition principal, advisor, co-broker) or the OM is co-branded, edit `prompt-template.md`.
- **Section spine includes sections that don't apply to every deal.** Specifically:
  - Section 11 (Submarket Residential Overview) — only relevant if the deal has a multifamily rezoning/conversion angle
  - Section 24 (Mixed-Use / Land comps) — only relevant for upside-thesis-supporting comps
  - Section 16 (Submarket Residential Overview) and Section 24 (Mixed-Use comps) should be skipped for pure office/industrial deals with no optionality
- **Photo-grid layout assumes you have photos.** If the deal folder has no usable photos, the Asset Overview — Photos slide should be skipped (Claude in PowerPoint should propose this in the section depth plan).

### Process

- **Pasteable prompt is ~4,900 words.** Most Claude in PowerPoint contexts handle this, but if context compresses mid-build, you may need to re-paste in chunks (one section at a time).
- **First-run feedback expected.** The skill encodes 105 N 13th lessons; every deal differs. Flag anomalies on your first real run and refine the prompt template.
- **No deal-specific numerics in the prompt itself** (intentional). Numbers come from source files at deck-build time so they stay in sync. Don't paste extracted financials into the prompt — Claude in PowerPoint will extract them itself.
- **The skill doesn't run TDD compliance tests on its own output.** A first-run anomaly is your signal to refine, not evidence the skill is broken.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Skill doesn't appear in Claude Code's available skills | Plugin not updated to 3.4.0 | Run plugin update; restart Claude Code |
| "Could not resolve Graph URI" warning | 365 MCP not loaded in session, or file not yet synced | Look up URIs manually in SharePoint; or re-run in a session with MCP enabled; or trigger sync |
| Claude in PowerPoint says "I can't access local files" | The refusal preamble didn't override the default refusal | Tell Claude in PowerPoint explicitly: "Use the 365 MCP connector and try again." If it still refuses, MCP isn't loaded in PowerPoint either |
| Claude in PowerPoint reads PDFs fine but can't fully parse the xlsx | Office.js OOXML parsing limit on complex sheets | Accept "TBD — confirm with sponsor" placeholders; supplement manually after the deck is built |
| Deck comes out with rounded cards, icons, or gradients (AI tells) | Anti-AI guardrails not applied | Re-paste the prompt emphasizing Step 8; or post-process with the dedicated rework prompt (separate output, not this skill) |
| Footer shows wrong attribution | Hardcoded to "Vanadium Realty | ..." | Edit `prompt-template.md` line in the master slide spec; bump plugin version |
| Garamond didn't render — body looks like Times New Roman | Garamond not installed on the system | Install Garamond, or edit `prompt-template.md` to specify a substitute (EB Garamond, etc.) |
| Section count exploded — Claude in PowerPoint made 50+ slides | Section depth plan wasn't reviewed/approved before building | After the cover + exec summary, force a pause; demand the depth plan with one-sentence rationale per section; sign off explicitly before building further |
| Numbers don't match across slides | Cross-slide consistency check not run in QA | Ask Claude in PowerPoint to cross-check 5-10 key figures (PP, equity, debt, IRR, EM, NOI Yr1/Yr5, exit, cap rate) and fix any mismatches |

## Updating or extending the skill

Files live at:
`C:\Users\TheodoreMouhlas\.claude\plugins\marketplaces\v23-plugins\plugins\v23\skills\om-builder\`
(and `om-builder-help/` for this guide)

To change behavior:

1. **Design system** (fonts, colors, margins, section spine, voice) → edit `prompt-template.md`
2. **Layouts** (new layouts, refined existing) → edit `layout-repertoire.md`
3. **Skill orchestration** (file lookup logic, runbook steps) → edit `SKILL.md`
4. **Help content** (this document) → edit `om-builder-help/SKILL.md`
5. **Bump version** in both `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`:
   - Patch (3.4.0 → 3.4.1) for refinements, fixes, language tweaks
   - Minor (3.4.0 → 3.5.0) for new layouts, new sections, new behavior
   - Major (3.x → 4.0.0) for breaking changes (renames, removed sections)
6. **Commit and push** to the plugin git repo so clients pick up the change.

## Related skills

- **`v23:deal-pack`** — ingest raw DD materials into a clean canonical pack. Run before om-builder if the deal folder isn't already normalized (rent roll abstracted, photos captioned, T-12 mapped).
- **`v23:deal-screener`** — screen an OM, model, or pitch deck with a senior CRE eye. Use after a draft is built to pressure-test.
- **`v23:comp-search`** — pull sale/lease comps for the OM's comp slides. Useful alongside om-builder to populate Section 21-24.
- **`v23:placement-engine`** — generate ranked investor placement lists. Use after the OM is finished.
- **`/adobe-for-creativity/adobe-design-from-template`** — used by Claude in PowerPoint when you upload a template (not directly invocable from Claude Code).

## When NOT to use the om-builder

- **Re-styling an existing deck** → different prompt (separate skill or one-off prompt, not this one)
- **One-pagers or teasers** → different artifact; `v23:deal-screener` is closer
- **Direct deck construction in Claude Code** → Claude in PowerPoint does the live work; om-builder builds the prompt that drives it
- **Non-OM artifacts** (IC memos, broker pitches, LP updates) → different document type; ask for a different prompt

## The bottom line

The om-builder is the **prompt-generation layer** between V23's source files and Claude in PowerPoint's live deck build. It encodes the Vanadium house style + the layout repertoire + the anti-AI guardrails + the process discipline that was hard-won over multiple OM productions.

It does not build the deck. Claude in PowerPoint does.

If something feels off on the first real run, the answer is to refine `prompt-template.md` or `layout-repertoire.md` and bump the plugin version — not to abandon the skill. The skill exists to compound lessons across deals.
