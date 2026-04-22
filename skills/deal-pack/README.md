# v23-deal-pack

A Claude Code skill that ingests a folder of commercial real-estate due-diligence
materials and produces a clean, canonical **deal pack** that Claude-in-PowerPoint
consumes to build an Offering Memorandum (OM).

## What it produces

```
deal-packs/<deal-name>/
├── facts.md              # narrative, source-attributed
├── financials.xlsx       # rent_roll, rent_roll_summary, t12, t12_summary, derived
├── leases/               # one markdown abstract per lease
├── images/               # photos + captions.json
├── sources/              # originals, renamed predictably
├── pack-manifest.json    # provenance + confidence flags
└── .v23-deal-pack.sha    # sidecar for re-run protection of facts.md
```

## Architecture

- **LLM (Claude) handles** extraction of messy client materials: file classification,
  rent-roll / T-12 layout detection, lease abstraction, facts narrative, photo captioning.
- **Python (`deal_pack/`) owns** all arithmetic and file writing: WALT, occupancy,
  NOI, derived metrics, `financials.xlsx`, manifest, sidecar.
- The LLM never computes a number. All numbers in the pack come from the Python CLI.

## Install

1. Install Python 3.11+.
2. From this directory:
   ```
   python -m venv .venv
   .venv/Scripts/activate   # Windows
   pip install -e ".[dev]"
   ```
3. Run tests to verify:
   ```
   pytest -v
   ```
4. Install the skill into your Claude Code skill search path.
   - Option A (user-level): copy `SKILL.md` and the `deal_pack/` package into
     `~/.claude/skills/v23-deal-pack/`.
   - Option B (plugin): drop the folder into the existing `v23` plugin alongside
     `v23:linkedin-research`, `v23:placement-engine`, `v23:comp-search`.

## Usage

In Claude Code:
```
/v23:deal-pack <path-to-client-materials> [--out <path>] [--name <deal>] [--force]
```

Defaults:
- `--out`: `C:\Users\TheodoreMouhlas\Documents\Claude\deal-packs\<deal-name>\`
- `--name`: the input folder name
- `--force`: required to overwrite an existing pack

## Development

CLI subcommands (called by `SKILL.md`):

| Subcommand            | Purpose                                              |
| --------------------- | ---------------------------------------------------- |
| `inventory <root>`    | Recursive scan + previews, JSON out                  |
| `rent-roll-summary`   | Canonical rent-roll CSV → summary JSON               |
| `t12-summary`         | Canonical T-12 CSV → summary JSON                    |
| `derived`             | Combine rent-roll + T-12 summaries → derived JSON    |
| `write-financials`    | Assemble multi-tab `financials.xlsx`                 |
| `write-manifest`      | Write `pack-manifest.json`                           |
| `copy-sources`        | Copy originals with predictable renaming             |
| `check-facts-edited`  | Has the user edited `facts.md` since generation?     |
| `write-facts-sidecar` | Record current `facts.md` hash                       |

All commands exchange JSON on stdout/stdin. Errors go to stderr with non-zero exit.

## Testing

Unit tests cover every Python helper with golden fixtures. Integration test
chains inventory → summaries → financials end-to-end on a sample deal.
