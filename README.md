# V23 Plugins

Claude Cowork plugin marketplace for Vanadium Group internal tools.

## Skills

### comp-search
Search, filter, and export CRE sale and lease comparables from the V23 Database. Uses a 5-agent parallel architecture to search across zones simultaneously and export clean results to Excel.

**Trigger phrases:** "find comps", "pull comps", "hotel comps in Texas", "export Dallas multifamily sales", "what sold in [market]", "leasing activity in [area]", etc.

### linkedin-research
Vision-based LinkedIn bulk research agent. Takes screenshots of live browser pages and uses Claude's vision to extract whatever fields you ask for — no DOM scraping, no fragile selectors.

**Trigger phrases:** "research LinkedIn profiles", "scrape LinkedIn", "enrich contact list", "find someone's job history on LinkedIn", "who is X on LinkedIn", etc.

### placement-engine
Generate ranked investor placement lists for commercial real estate capital raises. Maintains a local SQLite "living memory" of investors, deals, and interactions to produce data-driven placement recommendations.

**Trigger phrases:** "generate placement list", "rank investors for this deal", "who should we target for this raise", "update investor database", "import placement history", etc.

## Installation (Cowork)

1. Open the Cowork desktop app
2. Go to **Settings → Marketplaces**
3. Add marketplace: `tmouh/v23-plugins`
4. Install the **v23** plugin

## Adding New Skills

Create a new folder under `skills/`:

```
skills/
├── comp-search/          # CRE comparables search
│   ├── SKILL.md
│   └── scripts/
├── linkedin-research/    # LinkedIn profile research
│   ├── SKILL.md
│   └── scripts/
├── placement-engine/     # Investor placement lists
│   ├── SKILL.md
│   └── scripts/
└── your-new-skill/       # add here
    └── SKILL.md
```

Each skill needs at minimum a `SKILL.md` with `name` and `description` frontmatter fields. Skills are auto-discovered — no registration needed.

## Requirements

- **comp-search**: Read-only access to `C:\Users\TheodoreMouhlas\Vanadium Group LLC\V23 - Database` mounted in Cowork
- **linkedin-research**: Chrome browser open and logged into LinkedIn
- **placement-engine**: Python 3.10+ with openpyxl, thefuzz, python-Levenshtein
