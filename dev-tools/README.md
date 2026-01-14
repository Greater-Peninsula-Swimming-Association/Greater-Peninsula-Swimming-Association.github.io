# GPSA Dev Tools

Developer tools for generating and managing GPSA website content.

## Overview

This directory contains Python scripts that automate the generation of GPSA website content, including season archives and directory index pages.

## Tools

### 1. build_archive.py - Season Archive Generator

**Intelligent archive builder** that automatically generates season archives from individual meet result files.

#### Features

- ✅ **Automatic year detection** from meet filenames
- ✅ **Automatic division detection** by analyzing opponent relationships
- ✅ **CSV-based division assignment** for automated workflows
- ✅ **Interactive fallback** when CSV not available
- ✅ **GitHub Actions integration** for automatic archive generation
- ✅ **No hardcoded configuration** - adapts year-to-year
- ✅ **Self-contained HTML** - embedded styling for portability
- ✅ **Fully responsive design** - optimized for all screen sizes
- ✅ **Standardized GPSA branding** - matches tool aesthetic
- ✅ **Comprehensive logging** with verbose mode

#### Responsive Design

Generated archives are fully responsive with mobile-first design:

**Mobile (< 640px):**

- Compact padding (4px-8px)
- Abbreviated dates: "MON JUN 16"
- Smaller fonts (12px-14px)
- Division links wrap if needed
- Horizontal scroll for wide tables

**Tablet (640px - 767px):**

- Medium padding (8px)
- Full dates: "MONDAY JUNE 16"
- Standard fonts (14px-16px)

**Desktop (768px+):**

- Spacious padding (12px+)
- Large fonts (16px-18px)
- Optimal readability

#### Requirements

- Python 3.x
- BeautifulSoup4

```bash
pip install beautifulsoup4
```

#### Usage

**Basic usage:**

```bash
python dev-tools/build_archive.py -i results/2025
```

**Specify output directory:**

```bash
python dev-tools/build_archive.py -i results/2025 -o results/2025
```

**Enable verbose logging:**

```bash
python dev-tools/build_archive.py -i results/2025 -o results/2025 --verbose
```

**View help:**

```bash
python dev-tools/build_archive.py --help
```

#### Command-Line Arguments

| Argument | Short | Description | Required |
| ---------- | ------- | ------------- | ---------- |
| `--input` | `-i` | Directory containing meet result HTML files | Yes |
| `--output` | `-o` | Output directory for archive (default: current directory) | No |
| `--verbose` | `-v` | Enable detailed debug logging | No |
| `--non-interactive` | | Run without prompts (requires `divisions.csv`) | No |

#### Input Requirements

- All meet files must be in a single directory
- Filename format: `YYYY-MM-DD_TEAM1_v_TEAM2.html`
- Example: `2025-06-16_GG_v_WW.html`

#### Interactive Workflow

1. **Year Detection** - Automatically extracts year from filenames
2. **Team Clustering** - Analyzes which teams competed together
3. **Division Assignment** - Prompts you to assign team clusters to divisions:
   - Group 1: Select Red (1), White (2), or Blue (3)
   - Group 2: Select from remaining two divisions
   - Group 3: Automatically assigned to final division
4. **HTML Generation** - Creates `index.html` archive

#### Automated Mode (GitHub Actions)

For CI/CD pipelines and automated builds, use the `--non-interactive` flag with a `divisions.csv` file.

**Command:**
```bash
python dev-tools/build_archive.py -i results/2025 -o results/2025 --non-interactive
```

**Requirements:**
- `divisions.csv` must exist in the input directory
- All teams in result files must have division assignments in CSV

**divisions.csv Format:**
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

**Team Codes:**
- Use filename abbreviations (WPPI, MBKM, BLMA, etc.)
- Script automatically translates to official codes (WPPIR, MBKMT, BLMAR)
- Division names are lowercase: `red`, `white`, `blue`

**GitHub Actions Integration:**
When results are pushed to `results/YYYY/` directories:
1. GitHub Action detects changed years
2. Runs `build_archive.py --non-interactive` for each year with `divisions.csv`
3. Auto-commits generated `index.html` files

See `.github/workflows/build-season-archive.yml` for workflow configuration.

**Error Handling:**
- Missing `divisions.csv`: Exits with error (non-interactive) or falls back to prompts (interactive)
- Team in results but not in CSV: Exits with error in non-interactive mode
- Team in CSV but not in results: Warning only (appears in standings with 0-0 record)

#### Example Session

```
================================================================================
GPSA Season Archive Generator
================================================================================

Step 1: Detecting season year from filenames...
INFO: Detected season year: 2025

Step 2: Analyzing meet results to detect team groupings...
INFO: Found 42 HTML files to analyze
INFO: Detected 17 unique teams
INFO: Detected division cluster with 5 teams
INFO: Detected division cluster with 6 teams
INFO: Detected division cluster with 6 teams

Step 3: Assigning team clusters to divisions...

================================================================================
DIVISION ASSIGNMENT
================================================================================

GROUP 1 - Teams that competed together:
────────────────────────────────────────────────────────────────────────────────
  • BLMAR    - Beaconsdale Blue Marlins
  • EL       - Elizabeth Lake Tideriders
  • JRCC     - James River Country Club
  • KCD      - Kiln Creek Dolphins
  • RRST     - Riverdale Rays

Available divisions:
  1. Red
  2. White
  3. Blue

Select division for Group 1 (1-3): 3
✓ Assigned to Blue Division

[... continues for Groups 2 and 3 ...]

Step 4: Processing meet result files...
Step 5: Organizing meets by division...
Step 6: Generating HTML archive...
Step 7: Save output file

================================================================================
✓ Successfully generated gpsa_2025_season_archive.html
================================================================================
```

#### Generated HTML Structure

The archive includes:
- **Responsive GPSA header** with logo and subtitle
- **Division navigation links** (Red, White, Blue)
- **Three division sections**, each containing:
  - Meet schedule table (date, home, score, visitor, score, results link)
  - Standings table (team, wins, losses)
  - Back to top link

#### Division Assignment Tips

- **Blue Division** typically has fewer/smaller teams (5-6 teams)
- **Red & White Divisions** typically have similar sizes (5-7 teams each)
- Review team names carefully before assigning
- Check previous season's divisions for continuity if uncertain

#### Configuration Updates

When teams change names or new teams join, update these maps in `build_archive.py`:

```python
TEAM_NAME_MAP = {
    "Full Team Name": "ABBR",
    # ... existing teams ...
}

TEAM_SCHEDULE_NAME_MAP = {
    "Full Team Name": "Short Name",
    # ... existing teams ...
}

FILENAME_ABBR_MAP = {
    "FILE": "ABBR",  # If filenames use different abbreviation
    # ... existing mappings ...
}
```

#### Troubleshooting

**Error: "Expected 3 divisions but detected X"**
- Cause: Incomplete meet data or unusual division structure
- Solution: Verify all meets are included, or proceed anyway if intentional

**Error: "Could not detect year from any files"**
- Cause: Files don't match naming pattern
- Solution: Ensure files follow `YYYY-MM-DD_TEAM1_v_TEAM2.html` format

**Warning: "Multiple years detected"**
- Cause: Mix of seasons in directory
- Solution: Move prior season files to separate directory

**Warning: "Team not found in any division"**
- Cause: Team only competed in non-division meets
- Solution: Check if team should be in standings

---

### 2. bulk_process_results.py - Bulk SDIF Processor

**Bulk SDIF file processor** that converts swim meet result files to formatted HTML.

#### Features

- ✅ **Automatic ZIP extraction** - Extracts `.sd3` files from `.zip` archives and cleans up
- ✅ **Year-based organization** - Automatically organizes results into `YYYY/` subdirectories
- ✅ **Dual meet detection** - Auto-generates filenames in format `YYYY-MM-DD_TEAM1_v_TEAM2.html`
- ✅ **Production logging** - Comprehensive logging to console and `bulk_process_results.log`
- ✅ **Robust error handling** - Detailed failure reporting without stopping processing
- ✅ **Flexible I/O** - CLI arguments for custom input/output directories

#### Requirements

- Python 3.6+
- Standard library only (no external dependencies)

#### Usage

**Basic usage:**
```bash
python3 dev-tools/bulk_process_results.py -i /path/to/input -o results
```

**Process files from downloads:**
```bash
python3 dev-tools/bulk_process_results.py -i ~/Downloads/meet_results -o results
```

**Process directly into repository:**
```bash
python3 dev-tools/bulk_process_results.py -i ./incoming -o ./results
```

#### Command-Line Arguments

| Argument | Short | Description | Required |
|----------|-------|-------------|----------|
| `--input` | `-i` | Input directory containing `.sd3` and/or `.zip` files | Yes |
| `--output` | `-o` | Output directory for generated HTML files | Yes |

#### Output Structure

Files are automatically organized by year:

```
results/
├── 2023/
│   ├── 2023-06-19_KCD_v_WW.html
│   └── 2023-06-20_WO_v_GWRA.html
├── 2024/
│   ├── 2024-06-17_WO_v_WYCC.html
│   └── 2024-06-20_COL_v_POQ.html
└── 2025/
    ├── 2025-06-16_GG_v_WW.html
    └── 2025-06-23_EL_v_BLMA.html
```

#### Filename Generation

**Dual Meets (2 teams):**
- Format: `YYYY-MM-DD_TEAM1_v_TEAM2.html`
- Example: `2025-06-16_GG_v_WW.html`

**Multi-Team Meets:**
- Format: `YYYY-MM-DD_MeetName.html`
- Example: `2025-07-15_City_Meet.html`

#### Logging

The tool generates comprehensive logs:

**Console Output:**
- Real-time progress updates
- Processing summary

**Log File:** `bulk_process_results.log`
- Detailed operation logs
- Error stack traces
- Timestamp for each operation

**Sample Log Output:**
```
2025-01-14 09:15:32 - INFO - Starting bulk processing...
2025-01-14 09:15:32 - INFO - Input directory: /Users/dan/Downloads/meets
2025-01-14 09:15:32 - INFO - Output directory: /Users/dan/Code/GPSA/results
2025-01-14 09:15:32 - INFO - Extracting meet_results.zip...
2025-01-14 09:15:32 - INFO -   Extracted: 2025-06-16_meet.sd3
2025-01-14 09:15:32 - INFO - Deleted meet_results.zip
2025-01-14 09:15:32 - INFO - Found 3 .sd3 file(s) to process
2025-01-14 09:15:32 - INFO - Processing 2025-06-16_meet.sd3...
2025-01-14 09:15:32 - INFO -   Generated: 2025/2025-06-16_GG_v_WW.html
2025-01-14 09:15:33 - INFO - ============================================================
2025-01-14 09:15:33 - INFO - PROCESSING SUMMARY
2025-01-14 09:15:33 - INFO - ============================================================
2025-01-14 09:15:33 - INFO - Zip files extracted: 1
2025-01-14 09:15:33 - INFO - SDIF files processed: 3
2025-01-14 09:15:33 - INFO - HTML files generated: 3
2025-01-14 09:15:33 - INFO - Failed: 0
2025-01-14 09:15:33 - INFO - ============================================================
```

#### SDIF Format Support

Standard SDIF (Swimming Data Interchange Format) records:

- **B1**: Meet information (name, date in MMDDYYYY format)
- **B2**: Host team information
- **C1**: Team records
- **D0**: Individual swimmer results
- **E0**: Relay team results
- **F0**: Individual relay swimmer names

**Supported Features:**
- Individual and relay events
- Age groups: "8 & Under", "9-10", "11-12", "13-14", "15-18", "Open"
- Gender categories: Boys, Girls, Mixed
- Stroke types: Freestyle, Backstroke, Breaststroke, Butterfly, IM
- Relay types: Freestyle Relay, Medley Relay
- Team score calculation
- VA team code prefix stripping

#### Generated HTML Features

Each output file includes:

- **GPSA Header**: Logo and responsive meet title
- **Team Scores**: Sorted by score (highest first)
- **Event Winners**: All event winners with times
- **Responsive Design**: Mobile-friendly layout
- **Print Support**: Optimized for printing
- **GPSA Branding**: Navy blue (#002366) and red (#d9242b) colors

#### Error Handling

**Common Issues:**

**"Input directory does not exist"**
- Solution: Verify the path to your input directory

**"No .sd3 files found in input directory"**
- Solution: Check directory contains `.sd3` or `.zip` files

**"Invalid zip file"**
- Solution: Zip file may be corrupted; try re-downloading

**"Could not generate filename"**
- Solution: SDIF file may be missing date information; check log for details

**Recovery:**
- Failed files are logged but don't stop processing
- Check `bulk_process_results.log` for details
- Stack traces included for debugging

#### Code Architecture

- **SDIFParser**: Parses SDIF format files
- **HTMLGenerator**: Generates formatted HTML output
- **BulkProcessor**: Orchestrates bulk processing workflow

---

### 3. generate_index.py - Directory Index Generator

**Automated index page generator** that creates branded directory listings for website folders.

#### Features

- ✅ **Recursive directory crawling** - Processes entire directory trees
- ✅ **GPSA standardized branding** - Consistent header and styling
- ✅ **Breadcrumb navigation** - Smart linking to parent directories
- ✅ **Automatic repository root detection** - Finds CSS regardless of starting location
- ✅ **Smart path calculation** - Correct relative paths at any depth
- ✅ **Excludes development files** - Filters out `.git`, `dev-tools`, etc.

#### Requirements

- Python 3.x
- No additional dependencies

#### Usage

**Generate index pages for entire site:**
```bash
python dev-tools/generate_index.py .
```

**Generate for specific directory:**
```bash
python dev-tools/generate_index.py results/2025
python dev-tools/generate_index.py invitationals/CityMeet
```

#### Generated Page Features

- **GPSA Header**: Logo, title with breadcrumb navigation, subtitle
- **Directory Listing**: Icons for folders (📁) and files (📄)
- **Hover Effects**: Subtle animations on directory items
- **Responsive Design**: Works on all screen sizes
- **Breadcrumb Navigation**: Clickable path from Home → current location

#### Breadcrumb Examples

- `results/2023/index.html` → **Home** / **results** / 2023
- `invitationals/CityMeet/2025/index.html` → **Home** / **invitationals** / **CityMeet** / 2025
- Bold items are clickable links to their `index.html` files

#### Excluded Directories

By default, these directories are excluded from indexing:
- `.git`
- `dev-tools`
- `assets`
- `resources`
- `css`
- `tools`

To exclude additional directories, modify the `EXCLUDE_DIRS` list in the script.

#### How It Works

1. **Repository Detection**: Searches upward for `css/gpsa-tools-common.css` to find repository root
2. **Path Calculation**: Computes correct relative paths based on directory depth
3. **Recursive Processing**: Crawls all subdirectories (except excluded ones)
4. **HTML Generation**: Creates `index.html` with standardized GPSA structure
5. **Breadcrumb Building**: Generates clickable path from root to current location

---

## Best Practices

### Complete Workflow: From SDIF to Archive

**Scenario: New 2025 Season**

```bash
# Step 1: Collect all SDIF files
# Place .sd3 or .zip files in incoming/ directory

# Step 2: Bulk process SDIF files to HTML results
python3 dev-tools/bulk_process_results.py -i incoming/ -o results/

# Step 3: Generate season archive from results
python3 dev-tools/build_archive.py -i results/2025 -o results/2025

# Step 4: Generate directory index pages
python3 dev-tools/generate_index.py results/2025

# Step 5: Commit to repository
git add results/2025/
git commit -m "Add 2025 season meet results and archive"
git push origin main
```

### Before Running bulk_process_results.py

1. ✅ Collect all SDIF files (`.sd3` or `.zip`) in input directory
2. ✅ Verify output directory exists or can be created
3. ✅ Check for disk space (HTML files are larger than SDIF)
4. ✅ Review `bulk_process_results.log` from previous runs if debugging

### Before Running build_archive.py

1. ✅ Ensure all dual meet results are in the input directory
2. ✅ Verify filenames follow `YYYY-MM-DD_TEAM1_v_TEAM2.html` format
3. ✅ Check for any stray files from previous seasons
4. ✅ Review team abbreviations match `FILENAME_ABBR_MAP`

### After Generating Archive

1. ✅ Open HTML in browser to verify formatting
2. ✅ Check all teams appear in correct divisions
3. ✅ Verify meet schedules are complete and chronological
4. ✅ Confirm win/loss records are accurate
5. ✅ Test responsive behavior on mobile device
6. ✅ Update year directory `index.html` to link to new archive

### Before Running generate_index.py

1. ✅ Run from repository root for best results
2. ✅ Verify `css/gpsa-tools-common.css` exists
3. ✅ Check that target directories contain content to list
4. ✅ Review excluded directories if needed

---

## Development Notes

### build_archive.py Implementation

**Key Design Decisions:**
- **Embedded CSS**: All styles inline for portability (archives can live anywhere)
- **Responsive Classes**: Custom CSS classes (`.table-header`, `.table-cell`, `.table-text`, `.table-date`)
- **Mobile-First**: Base styles for mobile, enhanced with media queries
- **Date Toggle**: Both full and abbreviated dates in HTML, shown/hidden via CSS

**Responsive Breakpoints:**
- `< 640px` - Mobile (compact)
- `640px - 767px` - Tablet (medium)
- `768px+` - Desktop (spacious)

**Color Preservation:**
- Table headers: GPSA Red (`#d9242b`)
- Table borders: Black
- Links: GPSA Blue (`#0033a0`)
- Matches CMS-hosted league schedule styling

### generate_index.py Implementation

**Path Detection Algorithm:**
1. Start from target directory
2. Walk up directory tree
3. Look for `css/gpsa-tools-common.css`
4. Use that location as repository root
5. Calculate relative path from current directory to root

**Breadcrumb Generation:**
- Splits directory path into segments
- Creates clickable links for all segments except current
- Calculates correct `../` prefixes for each link
- Final segment shown in bold, not clickable

---

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'bs4'"**
- Solution: Install BeautifulSoup4: `pip install beautifulsoup4`

**"Input directory does not exist"**
- Solution: Verify path is correct relative to where you're running the command

**"Could not find repository root"** (generate_index.py)
- Solution: Ensure `css/gpsa-tools-common.css` exists in repository

**Archive tables not responsive**
- Solution: Regenerate archive with latest `build_archive.py` version

**Directory index pages missing CSS**
- Solution: Run `generate_index.py` from repository root, or verify relative paths

---

## Support

For questions or issues with these tools:
1. Check the troubleshooting section above
2. Review the CLAUDE.md file in repository root
3. Examine the source code comments
4. Test with verbose logging enabled (`-v` flag)

---

## Version History

**build_archive.py v2.1 (January 2025)**
- Added `--non-interactive` flag for CI/CD automation
- CSV-based division assignment (`divisions.csv`)
- GitHub Actions workflow integration
- Validation of CSV divisions against detected teams
- Fallback to interactive mode when CSV unavailable

**build_archive.py v2.0 (2025)**
- Added fully responsive design
- Embedded CSS for portability
- Standardized GPSA header
- Mobile date abbreviation
- Responsive text sizing and padding

**build_archive.py v1.0 (2024)**
- Initial release
- Automatic year and division detection
- Interactive division assignment
- BeautifulSoup HTML parsing

**bulk_process_results.py v1.0 (2025)**
- Initial release
- ZIP extraction and cleanup
- Automatic year-based organization
- Production logging
- Comprehensive error handling
- CLI argument support

**generate_index.py v1.0 (2024)**
- Initial release
- Automatic repository root detection
- Breadcrumb navigation
- GPSA standardized branding
