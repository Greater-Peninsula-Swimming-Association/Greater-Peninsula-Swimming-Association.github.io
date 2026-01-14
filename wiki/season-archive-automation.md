---
layout: wiki
title: Season Archive Automation
category: Automation
toc: true
last_updated: January 2025
---

GPSA season archives are automatically generated when new meet results are pushed to the repository. This page explains how the automation works and how to set up division assignments for each season.

## Overview

The automation system consists of three components:

1. **Division CSV files** - Define which teams are in each division
2. **Build Archive script** - Generates season summary HTML from results
3. **GitHub Action** - Triggers automatic rebuilds when results change

When you push new meet result files to the repository, the GitHub Action automatically regenerates the season archive (`index.html`) for affected years.

## How It Works

```
Push meet results → GitHub Action triggers → Archive rebuilds → Auto-commit
```

**Detailed flow:**

1. Push HTML result files to `results/YYYY/` directory
2. GitHub Action detects which years changed
3. For each affected year with a `divisions.csv`:
   - Runs `build_archive.py --non-interactive`
   - Generates updated `index.html` with schedules and standings
4. Auto-commits the generated `index.html` files

## Setting Up a New Season

### Step 1: Create Division Assignments

Before results can be processed, you need to define division assignments in a CSV file.

**Create** `results/YYYY/divisions.csv` with this format:

```csv
season,team_code,division
2025,WPPI,red
2025,WO,red
2025,MBKM,red
2025,COL,red
2025,RMMR,red
2025,POQ,red
2025,CV,white
2025,WYCC,white
2025,GG,white
2025,HW,white
2025,WW,white
2025,GWRA,white
2025,KCD,blue
2025,JRCC,blue
2025,RRST,blue
2025,BLMA,blue
2025,EL,blue
```

### CSV Format

| Column | Description | Example Values |
|--------|-------------|----------------|
| `season` | Four-digit year | `2025` |
| `team_code` | Team abbreviation (from filenames) | `WPPI`, `GG`, `KCD` |
| `division` | Division name (lowercase) | `red`, `white`, `blue` |

### Step 2: Upload Meet Results

Save meet result HTML files in the year directory:

```
results/2025/
├── divisions.csv
├── 2025-06-16_GG_v_WW.html
├── 2025-06-16_WPPI_v_WO.html
├── 2025-06-23_COL_v_POQ.html
└── ...
```

**Filename format:** `YYYY-MM-DD_TEAM1_v_TEAM2.html`

### Step 3: Push to Repository

```bash
git add results/2025/
git commit -m "Add week 1 meet results"
git push origin main
```

The GitHub Action will automatically:
1. Detect changes in `results/2025/`
2. Load `divisions.csv` for team assignments
3. Generate `results/2025/index.html`
4. Commit the generated file

## Team Codes Reference

Use these codes in `divisions.csv`:

| Code | Team Name |
|------|-----------|
| `BLMA` | Beaconsdale Blue Marlins |
| `COL` | Colony Cudas |
| `CV` | Coventry Sailfish Swim Team |
| `EL` | Elizabeth Lake Tideriders |
| `GG` | Glendale Gators |
| `GWRA` | George Wythe Wahoos |
| `HW` | Hidenwood Tarpons |
| `JRCC` | James River Country Club |
| `KCD` | Kiln Creek Dolphins |
| `MBKM` | Marlbank Mudtoads |
| `NHM` | Northampton Marlins |
| `POQ` | Poquoson Barracudas |
| `RMMR` | Running Man Manta Rays |
| `RRST` | Riverdale Rays |
| `WO` | Willow Oaks Stingrays |
| `WPPI` | Windy Point Piranhas |
| `WW` | Wendwood Wahoos |
| `WYCC` | WYCC Sea Turtles |

**Note:** Team codes should match the abbreviations used in result filenames. The script automatically translates some codes internally (e.g., `WPPI` → `WPPIR`).

## Manual Regeneration

If you need to manually rebuild an archive:

### Using GitHub Actions

1. Go to **Actions** tab on GitHub
2. Select **"Build Season Archive"** workflow
3. Click **"Run workflow"**
4. Optionally enter a specific year (e.g., `2025`)
5. Click **"Run workflow"**

### Using Command Line

```bash
# Install dependencies (if not already)
pip install beautifulsoup4

# Run for specific year
python dev-tools/build_archive.py \
  -i results/2025 \
  -o results/2025 \
  --non-interactive \
  --verbose
```

## Generated Archive Features

The generated `index.html` includes:

- **Division navigation** - Jump links to Red, White, Blue sections
- **Meet schedules** - Chronological list of all meets per division
- **Standings tables** - Win/loss records sorted by wins
- **Result links** - Direct links to individual meet results
- **Responsive design** - Works on desktop, tablet, and mobile
- **GPSA branding** - Consistent styling with other GPSA tools

## Troubleshooting

### Archive not generated after push

**Symptoms:** Push succeeds but no new `index.html` commit appears.

**Check:**
1. `divisions.csv` exists in the year directory
2. CSV format is correct (verify column headers)
3. All teams in results have entries in CSV
4. Review GitHub Actions logs for errors

### Team missing from standings

**Symptoms:** A team doesn't appear in the division standings.

**Fix:**
1. Add the team's code to `divisions.csv`
2. Ensure team code matches filename abbreviation
3. Push updated CSV to trigger rebuild

### Wrong division assignment

**Symptoms:** Team appears in wrong division's schedule/standings.

**Fix:**
1. Edit `divisions.csv` with correct division
2. Push the change to trigger rebuild

### GitHub Action fails

**Symptoms:** Red X on Actions tab, archive not updated.

**Debug steps:**
1. Go to **Actions** tab
2. Click the failed workflow run
3. Expand failed step to see error messages
4. Common issues:
   - Missing `divisions.csv`
   - Team in results but not in CSV
   - Malformed CSV file

### Error: "Teams in results but not in divisions.csv"

**Cause:** Meet result file references a team not defined in CSV.

**Fix:** Add the missing team code to `divisions.csv` with appropriate division.

## Workflow Configuration

The GitHub Action is defined in `.github/workflows/build-season-archive.yml`.

### Triggers

```yaml
on:
  push:
    paths:
      - 'results/**/*.html'
      - 'results/**/divisions.csv'
    branches:
      - main
  workflow_dispatch:
    inputs:
      year:
        description: 'Specific year to rebuild'
        required: false
```

- **Automatic:** Triggers on push when result files or CSV changes
- **Manual:** Can be run via "Run workflow" button

### Year Detection

The workflow automatically detects which years changed by comparing file paths:
- `results/2025/2025-06-16_GG_v_WW.html` → processes year `2025`
- `results/2024/divisions.csv` → processes year `2024`

### Commit Behavior

- Generated files are committed by `github-actions[bot]`
- Commit message: `"Build season archives [skip ci]"`
- `[skip ci]` flag prevents infinite workflow loops

## Related Documentation

- [Publicity Processor](/wiki/publicity-processor) - Create individual meet result HTML files
- [Dev Tools README](/dev-tools/README.md) - Detailed script documentation
- [Season Archive Builder](/dev-tools/README.md#1-build_archivepy---season-archive-generator) - Manual usage guide

## FAQ

### Can I run the archive builder locally?

Yes! Use the command:
```bash
python dev-tools/build_archive.py -i results/2025 -o results/2025 --non-interactive
```

Requires Python 3 and `beautifulsoup4` package.

### What if a team changes divisions mid-season?

Update the `divisions.csv` file with the new division assignment. The archive will be regenerated with the updated assignment on next push.

Note: Historical results won't change - the team will appear in whichever division they're currently assigned to.

### Can I use this for previous seasons?

Yes! Create a `divisions.csv` file in the appropriate year directory (e.g., `results/2024/divisions.csv`) with that season's division assignments, then trigger a manual workflow run.

### What happens if divisions.csv is missing?

- **Automatic mode:** Year is skipped with a warning
- **Interactive mode:** Script prompts for manual division assignment

### How do I add a new team?

1. Add the team to `TEAM_NAME_MAP` in `build_archive.py`
2. Add the team to `TEAM_SCHEDULE_NAME_MAP`
3. If filename uses different abbreviation, add to `FILENAME_ABBR_MAP`
4. Add team to `divisions.csv` with appropriate division
