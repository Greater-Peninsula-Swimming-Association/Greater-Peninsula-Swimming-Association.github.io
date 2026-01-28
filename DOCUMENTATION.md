# GPSA Website Documentation

Detailed documentation for tools, scripts, and workflows in the GPSA website repository.

## Table of Contents
- [Key Tools](#key-tools)
- [Publicity API Server](#publicity-api-server)
- [Shared Modules](#shared-modules)
- [Dev Tools](#dev-tools)
- [File Formats](#file-formats)
- [Workflows](#workflows)

---

## Key Tools

### tools/publicity.html - GPSA Meet Publicity Tool (v1.2)

**Purpose:** Parses SDIF format swim meet results files and generates formatted HTML output.

**Features:**
- Parses SDIF format files (.sd3, .txt, or .zip)
- Generates formatted HTML with team scores and event winners
- Auto-generates meet titles for dual meets using host team and date
- Exports as standalone HTML: `YYYY-MM-DD_TEAM1_v_TEAM2.html`
- All SDIF parsing logic in `parseSdif()` function
- Uses Tailwind CDN with GPSA brand colors (#002366 navy, #d9242b red)

**Recent Enhancements (2025):**

**Zip File Support:**
- Accepts `.zip` files containing SDIF data (256KB maximum)
- Automatically extracts `.sd3` or `.txt` files from zip archives
- Uses JSZip 3.10.1 library for client-side extraction
- Handles multi-file zips (uses first SDIF file found)
- Toast notifications for extraction status and errors

**Forfeit/Override Functionality:**
- **Special Circumstances UI**: Optional section to mark forfeits, cancellations, or other overrides
- **Winning Team Selection**: Dropdown auto-populated with teams from SDIF file
- **Standard Forfeit Scoring**: Winner receives 1.0, Loser receives 0.0
- **Reason Documentation**: Free-text field for explanation
- **Override Banner**: Yellow warning banner appears in exported HTML
- **Archive Builder Compatible**: Exported HTML works seamlessly with `build_archive.py`
  - Team Scores table shows 1.0 vs 0.0
  - No special processing required
  - Follows standard naming convention
- **Real-time Updates**: Results preview updates as user changes override settings
- **Export Validation**: Ensures override is complete before allowing export

**Implementation Notes:**
- Override data stored in `overrideData` global variable
- `applyForfeitScores()` function modifies team scores when override is active
- `prepareOverrideData()` validates winning team and reason inputs
- Override banner uses inline styles for portability
- All user inputs sanitized with `escapeHtml()` for XSS protection

**Shared Module Architecture (2025):**
- Core parsing logic extracted to `lib/publicity-core.js`
- Browser tool imports from shared module via ES modules
- Same code powers both browser tool and API server
- See [Shared Modules](#shared-modules) section for details

**Forfeit Workflow:**
1. Upload SDIF file (.sd3, .txt, or .zip)
2. Check "This meet has special circumstances"
3. Click "Process Results" (populates team dropdown)
4. Select winning team from dropdown
5. Enter reason for override
6. Review results with override banner
7. Export as standard HTML file

---

### tools/roster.html - Swim Team Roster Formatter (Enhanced 2025)

**Purpose:** Processes SwimTopia CSV exports to create formatted team rosters.

**Features:**
- Multi-tab interface: Roster Input, Contacts, Officials, Formatted Roster
- Uses PapaParse library for CSV parsing
- Generates three export formats: roster HTML, contacts HTML, officials HTML
- Exports are HTML-only (no embedded CSS) - styled via external CSS on SwimTopia CMS
- Age group processing strips gender prefixes and sorts swimmers alphabetically

**Recent Enhancements (2025):**
- **Security**: All user input sanitized with `escapeHtml()` function
- **Data Persistence**: Auto-saves contacts and officials to localStorage
  - Keys: `gpsa_roster_contacts`, `gpsa_roster_officials`
- **Modern APIs**: Uses Clipboard API (navigator.clipboard) instead of deprecated document.execCommand
- **Input Validation**:
  - Real-time email validation with visual feedback (red border = invalid, green = valid)
  - Auto-formats phone numbers to (XXX) XXX-XXXX format
  - Duplicate contact name detection with warning toasts
  - Prevents export if invalid emails detected
- **Toast Notifications**: Professional non-blocking notifications replace alert() dialogs
  - Types: Success (green), Error (red), Warning (orange), Info (blue)
  - Auto-dismiss after 4 seconds, manual close available
- **Accessibility Features**:
  - Modal focus trap (Tab key cycles only within modal)
  - Dynamic aria-labels on remove buttons
  - Keyboard shortcuts (Esc to close modals)
  - Click-outside-to-close for modals
- **Better Error Messages**:
  - CSV errors list specific missing columns
  - Detailed instructions point to SwimTopia export location
- **Reset Functionality**: Clear buttons with localStorage cleanup

**Implementation Notes:**
- Helper functions: `escapeHtml()`, `isValidEmail()`, `formatPhoneNumber()`, `showToast()`
- Contact rows dynamically update aria-labels as names change
- All validation runs on blur events for better UX
- Export validation checks emails before opening modal
- localStorage auto-loads on page initialization

**CSV Requirements:**
SwimTopia CSV exports must contain these headers:
- `AgeGroup`: May include gender prefix (e.g., "Boys 9-10" or "9-10")
- `AthleteCompetitionCategory`: Gender code (M/F)
- `AthleteDisplayName`: Swimmer's name
- `AthleteAge`: Numeric age

**Export Workflow:**
1. **External CSS Dependencies**: Exports reference stylesheets on `publicity.gpsaswimming.org`:
   - `css/gpsa-roster.css` - Roster table styles
   - `css/gpsa-roster-contact.css` - Contact table styles
   - `css/gpsa-roster-officials.css` - Officials list styles

2. **Export Format**: Each export uses semantic class names:
   - Roster: `.roster-container`, `.roster-main-title`, `.roster-table`, `.roster-group`, `.roster-footer`
   - Contacts: `.contacts-main-title`, `.contact-section-wrapper`, `.contact-header`, `.contact-table`
   - Officials: `.officials-main-title`, `.officials-container`, `.officials-column`, `.officials-list`

3. **SwimTopia Integration**: Users paste HTML into SwimTopia's HTML editor, which applies external stylesheets

**Data Persistence:**
- Contacts and officials auto-save to browser localStorage on every input change
- Data persists across browser sessions/restarts
- Clear buttons remove both UI data and localStorage entries

---

### resources/div-crawler.html - Website ID Reference Crawler

**Purpose:** Development utility for finding HTML element ID references across the website.

**Features:**
- Uses CORS proxy (`https://api.allorigins.win/raw?url=`) to fetch pages
- Recursively crawls same-domain links
- Finds all references to a specified div ID
- Intended for development and maintenance purposes

---

## Publicity API Server

### publicity-server/ - REST API for SDIF Processing

**Purpose:** Node.js API server for processing SDIF files programmatically, designed for n8n and automation integration.

**Location:** `publicity-server/`

**Features:**
- Express.js REST API
- Multipart file upload support
- Memory-only processing (no temp files)
- Docker deployment with volume mounts
- Shares parsing logic with browser tool via `lib/publicity-core.js`

**Endpoints:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check with version info |
| `/api` | GET | API information and limits |
| `/api/process` | POST | Process SDIF file |

**POST /api/process:**

Request (multipart/form-data):
- `file`: SDIF file (.sd3, .txt, or .zip) - required
- `override`: JSON string with override config - optional

Response:
```json
{
  "success": true,
  "filename": "2025-06-16_GG_v_WW.html",
  "html": "<!DOCTYPE html>...",
  "metadata": {
    "meetName": "2025 Great Oaks v. Westfield",
    "meetDate": "2025-06-16",
    "teams": [
      {"code": "GG", "name": "Great Oaks", "score": 245.0},
      {"code": "WW", "name": "Westfield", "score": 198.0}
    ],
    "eventCount": 42
  }
}
```

**Error Responses:**

| HTTP | Condition | Response |
|------|-----------|----------|
| 400 | No file uploaded | `{"success": false, "error": "No file uploaded"}` |
| 400 | Invalid file type | `{"success": false, "error": "Invalid file type"}` |
| 413 | File too large | `{"success": false, "error": "File too large"}` |
| 422 | Invalid SDIF | `{"success": false, "error": "Invalid SDIF format"}` |
| 500 | Server error | `{"success": false, "error": "Internal server error"}` |

**Limits:**
- Max file size: 256KB
- Allowed extensions: .sd3, .txt, .zip

**Local Development:**
```bash
cd publicity-server
npm install
npm start
# Server runs at http://localhost:3000
```

**Docker Deployment:**
```bash
cd publicity-server
docker-compose up
```

Docker uses volume mounts (no build step):
- `./` → `/app` - Server code
- `../lib` → `/app/lib` - Shared module

Changes to `lib/publicity-core.js` sync instantly without rebuild.

**n8n Integration Example:**
```
HTTP Request Node:
- Method: POST
- URL: http://your-server:3000/api/process
- Body: Form-Data/Multipart
- Fields:
  - file: (Binary from trigger/previous node)
  - override: {"enabled": false} (optional)
```

**cURL Examples:**
```bash
# Basic usage
curl -X POST http://localhost:3000/api/process \
  -F "file=@meet_results.sd3"

# With override
curl -X POST http://localhost:3000/api/process \
  -F "file=@meet_results.sd3" \
  -F 'override={"enabled":true,"winnerCode":"GG","reason":"Forfeit"}'
```

See `publicity-server/README.md` for complete documentation.

---

## Shared Modules

### lib/publicity-core.js - SDIF Parsing Core

**Purpose:** Shared ES module containing SDIF parsing and HTML generation logic used by both the browser tool and API server.

**Location:** `lib/publicity-core.js`

**Exports:**

| Export | Type | Description |
|--------|------|-------------|
| `VERSION` | const | Tool version string |
| `LOGO_URL` | const | GPSA logo URL |
| `STROKE_MAP` | const | Stroke code to name mapping |
| `GENDER_MAP` | const | Gender code to display name |
| `escapeHtml(text)` | function | XSS-safe HTML escaping (regex-based) |
| `parseAgeCode(code)` | function | Convert age code to display format |
| `validateSdif(data)` | function | Validate SDIF has required B1 record |
| `parseSdif(data)` | function | Parse SDIF content to structured data |
| `applyForfeitScores(data, override)` | function | Apply forfeit scores to parsed data |
| `generateFilename(data)` | function | Generate standardized filename |
| `generateExportableHtml(data, logo, override)` | function | Generate standalone HTML document |
| `extractMetadata(data)` | function | Extract metadata for API responses |

**Usage in Browser (tools/publicity.html):**
```javascript
import {
    escapeHtml,
    parseSdif,
    generateExportableHtml,
    LOGO_URL,
    VERSION
} from '../lib/publicity-core.js';
```

**Usage in Node.js (publicity-server/server.mjs):**
```javascript
import {
    parseSdif,
    validateSdif,
    generateExportableHtml,
    LOGO_URL
} from './lib/publicity-core.js';
```

**Key Design Decisions:**
- **Node-compatible escapeHtml**: Uses regex instead of DOM for Node.js support
- **Parameterized functions**: Override data passed as parameter (no globals)
- **Pure functions**: No side effects, easy to test
- **ES modules**: Native browser and Node.js support

**Architecture Diagram:**
```
┌─────────────────────┐     ┌─────────────────────┐
│  tools/publicity    │     │  publicity-server/  │
│      .html          │     │     server.mjs      │
│    (Browser)        │     │     (Node.js)       │
└─────────┬───────────┘     └─────────┬───────────┘
          │                           │
          │  import from              │  import from
          │                           │
          └───────────┐   ┌───────────┘
                      │   │
                      ▼   ▼
              ┌───────────────────┐
              │  lib/publicity-   │
              │    core.mjs       │
              │  (Shared Logic)   │
              └───────────────────┘
```

---

## Dev Tools

### dev-tools/generate_index.py - Directory Index Generator

**Purpose:** Automatically generates branded directory listing pages for website folders.

**Features:**
- Recursively crawls directories and creates index pages
- Uses GPSA standardized branding and shared CSS (`/css/gpsa-tools-common.css`)
- Responsive design with Tailwind CSS
- **Automatically detects repository root** by searching for `css/` folder
- **Calculates correct relative paths** from any directory depth
- Works from any subdirectory
- Excludes: `.git`, `dev-tools`, `assets`, `resources`, `css`, `tools`
- Filters out hidden files and directories

**Generated Page Structure:**
- Standardized `max-w-7xl` container
- Full GPSA header with logo, navy background, responsive sizing
- **Breadcrumb navigation** with clickable links:
  - "Home" link to repository root
  - Intermediate folders are clickable
  - Current location in bold (not clickable)
  - Example: `Home / CityMeet / 2025`
- White card layout with shadows
- Hover effects on items
- Icons: 📁 for directories, 📄 for files
- GPSA footer

**Usage:**
```bash
# From repository root
python dev-tools/generate_index.py .

# For specific directory
python dev-tools/generate_index.py path/to/directory
```

**Path Detection:**
Script detects repository root by:
1. Starting from the directory being processed
2. Searching upward for `css/gpsa-tools-common.css`
3. Using that location for relative path calculations
4. Generating correct paths (e.g., `../css/...`, `../../css/...`)

Works from any location:
- Repository root: `python3 dev-tools/generate_index.py .`
- Subdirectory: `python3 dev-tools/generate_index.py results/2023/`
- Nested: `python3 dev-tools/generate_index.py invitationals/CityMeet/Results/`

**Breadcrumb Examples:**
- `results/2023/index.html` → **Home** / **results** / 2023
- `invitationals/CityMeet/index.html` → **Home** / **invitationals** / CityMeet
- `invitationals/CityMeet/2025/index.html` → **Home** / **invitationals** / **CityMeet** / 2025

(Bold = clickable links)

---

### dev-tools/build_archive.py - Season Archive Generator

**Purpose:** Intelligent archive builder that processes individual meet result files.

**Features:**
- **Automatic year detection** from meet filenames
- **Automatic division detection** by analyzing opponent relationships
- **Interactive division assignment** for Red/White/Blue divisions
- **No hardcoded configuration** - adapts year-to-year
- **Comprehensive logging** through 7 steps with verbose mode
- Uses BeautifulSoup to parse HTML files
- Detects which teams competed together (same division)
- Validates input/output directories
- Generates standings and schedules from raw data
- Tailwind CDN for styling
- **Self-contained HTML output** - portable archives
- **Fully responsive design** - mobile, tablet, desktop optimized
- **Standardized GPSA header**

**Responsive Design Features:**
- Mobile-first approach
- Abbreviated dates on mobile: "MON JUN 16" vs "MONDAY JUNE 16"
- Responsive text sizing: 14px → 16px → 18px
- Responsive padding: 4px-8px mobile, 12px+ desktop
- Division navigation wraps on small screens
- Horizontal scroll for wide tables
- Print optimization

**Command-Line Arguments:**
- `-i, --input`: Directory with meet HTML files (required)
- `-o, --output`: Output directory (default: current directory)
- `-v, --verbose`: Enable debug logging

**Usage:**
```bash
# Simplest usage
python dev-tools/build_archive.py -i results/2025

# Specify output
python dev-tools/build_archive.py -i results/2025 -o results/2025

# With verbose logging
python dev-tools/build_archive.py -i results/2025 -o results/2025 --verbose

# View help
python dev-tools/build_archive.py --help
```

**Interactive Workflow:**
1. Scans for files matching `YYYY-MM-DD_TEAM1_v_TEAM2.html`
2. Auto-detects season year
3. Analyzes meets to determine team relationships
4. Clusters teams into divisions
5. Displays Group 1, prompts: "Select division (1. Red, 2. White, 3. Blue)"
6. Displays Group 2 (excludes already-selected division)
7. Auto-assigns Group 3 to remaining division
8. Processes all files and generates archive
9. Outputs `gpsa_YYYY_season_archive.html`

**Best Practices:**
1. **Complete Data**: Ensure all dual meet results are present
   - Missing meets may cause misclustering
   - Incomplete seasons may detect fewer than 3 divisions

2. **Filename Consistency**: Follow `YYYY-MM-DD_TEAM1_v_TEAM2.html` format
   - Team abbreviations should match `FILENAME_ABBR_MAP`
   - Abbreviated names (MBKM, WPPI, BLMA) auto-expand

3. **Division Assignment Logic**:
   - Review team names carefully
   - Typically: Blue = smaller/fewer teams, Red/White = larger
   - Cross-reference previous season if uncertain

4. **Validation After Generation**:
   - Open HTML in browser
   - Verify teams in correct divisions
   - Check schedules are complete and chronological
   - Confirm win/loss records accurate

**Common Issues:**
- **Multiple Years Detected**: Uses earliest year, warns you
  - Cause: Mix of current and prior season meets
  - Solution: Move prior season files to separate directory

- **Fewer Than 3 Divisions**: Not enough meets to cluster
  - Cause: Incomplete season or cross-division competition
  - Solution: Wait for more meets or verify clustering

- **Team Not Found**: Competed but not clustered
  - Cause: Only competed in non-division meets (invitationals)
  - Solution: Check if team should be in division standings

**Configuration Updates:**
When teams change names or new teams join:
```python
TEAM_NAME_MAP = {
    "New Team Full Name": "NTFN",
    # ... existing teams ...
}

TEAM_SCHEDULE_NAME_MAP = {
    "New Team Full Name": "New Team",
    # ... existing teams ...
}

FILENAME_ABBR_MAP = {
    "NT": "NTFN",  # If filenames use "NT" but official is "NTFN"
    # ... existing mappings ...
}
```

---

### dev-tools/bulk_process_results.py

**Purpose:** Bulk SDIF to HTML processor.

See `dev-tools/README.md` for detailed usage.

---

## File Formats

### SDIF File Format

SDIF (Swimming Data Interchange Format) is the standardized format for swim meet data.

**Key Record Types:**
- **B1**: Meet information (name, date in MMDDYYYY format)
- **B2**: Host team information
- **C1**: Team record (team code, team name)
- **D0**: Individual swimmer result (event number, name, time, place, points)
- **E0**: Relay team result (relay identifier, time, place, points)
- **F0**: Individual relay swimmer names (follows E0 record)

**Note on HY3 Format:**
The publicity tool does not support HY3/Hy-Tek 3.0 format:
- HY3 files are 65-70% larger than SDIF
- Uses complex multi-line structure (D1+E1+E2, F1+F2+F3)
- Requires athlete ID cross-referencing
- Both formats contain identical data
- SwimTopia exports SDIF (.sd3) by default
- Supporting HY3 would add 250+ lines without user benefit
- **Users should export SDIF/SD3 format instead**

**Team Code Handling:**
Team codes starting with "VA" have the prefix stripped for display.

---

## Workflows

### Processing Meet Results

When processing or generating meet result files:
- Ensure SDIF parser handles all record types (B1, B2, C1, D0, E0, F0)
- Relay events display individual swimmer names on separate lines
- Age group parsing handles: "8 & Under", "9-10", "11-12", "13-14", "15-18", "Open"
- Event descriptions combine gender, age group, distance, stroke type

### Generating Season Archives

**Prerequisites:**
1. Python 3 with BeautifulSoup4: `pip install beautifulsoup4`
2. All meet files in single directory (e.g., `results/2025/`)
3. Files follow: `YYYY-MM-DD_TEAM1_v_TEAM2.html`

**Steps:**
1. Run script:
   ```bash
   python dev-tools/build_archive.py -i results/2025 -o results/2025
   ```

2. Script automatically:
   - Detects season year
   - Analyzes team relationships
   - Displays 3 team groupings

3. Assign divisions interactively:
   - Group 1: Select 1 (Red), 2 (White), or 3 (Blue)
   - Group 2: Repeat (one division excluded)
   - Group 3: Auto-assigned to remaining division

4. Script generates `gpsa_YYYY_season_archive.html`

5. Verify archive in browser

6. Update year directory `index.html` with link

**Division Assignment Tips:**
- Blue Division: typically fewer/smaller teams (5-6)
- Red & White: typically similar sizes (5-7 each)
- Review team names carefully (shows full names)
- Check previous season for continuity if uncertain

### Working with Rosters

**Validation Best Practices:**
- Email validation runs on blur (when leaving field)
- Phone formatting applies automatically on blur
- Export blocked if invalid emails detected
- Duplicate contacts show warning but don't block export
- All validation errors via toast notifications (non-blocking)

---

## File Naming Conventions

- Dual meet results: `YYYY-MM-DD_TEAM1_v_TEAM2.html`
- Season archives: `gpsa_YYYY_season_archive.html`
- Directory index pages: `index.html` within each directory
