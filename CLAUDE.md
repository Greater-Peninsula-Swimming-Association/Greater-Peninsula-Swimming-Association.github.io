# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the Greater Peninsula Swimming Association (GPSA) website repository, hosted on GitHub Pages. It contains swim meet results, team information, tools for processing meet data, and invitational event information for a youth summer swim league.

## Architecture

### Site Structure

The site is organized into a clean directory structure with dedicated areas for different content types:

- **Root Directory**: Contains main landing page (`index.html`) with navigation to all site sections
- **Tools Directory** (`tools/`): Web-based utility applications for meet publicity and roster formatting
- **Results Directory** (`results/`): Organized by season year with subdirectories (`2023/`, `2024/`, `2025/`) containing dual meet results as `YYYY-MM-DD_TEAM1_v_TEAM2.html` files and season archives
- **Invitationals Directory** (`invitationals/`): Event-specific content organized by event type (`CityMeet/`, `SummerSplashInvitational/`, `MiniMeet/`), each containing year-specific subdirectories with PDFs and results
- **Documents Directory** (`documents/`): Organizational documents like the GPSA Constitution (PDF format)
- **CSS Directory** (`css/`): Modular stylesheets split by purpose (shared tools, rosters, invitationals, main site)
- **Assets Directory** (`assets/`): Static assets including logos, images, and graphics
- **Dev Tools Directory** (`dev-tools/`): Backend Python scripts including:
  - `build_archive.py` - Intelligent season archive builder with auto-detection and responsive design
  - `bulk_process_results.py` - Bulk SDIF to HTML processor
  - `generate_index.py` - Automated directory index page generator
  - `README.md` - Comprehensive documentation for all dev tools (see this file for detailed usage)
- **Resources Directory** (`resources/`): Additional utility HTML tools for website management

### Key Tools (Self-Contained HTML Applications)

The repository includes several standalone web tools. Each tool is a complete single-file HTML application with embedded JavaScript:

1. **tools/publicity.html** - GPSA Meet Publicity Tool (v1.1)
   - Parses SDIF format swim meet results files (.sd3 or .txt)
   - Generates formatted HTML output with team scores and event winners
   - Auto-generates meet titles for dual meets using host team and date
   - Exports results as standalone HTML files with naming convention: `YYYY-MM-DD_TEAM1_v_TEAM2.html`
   - All SDIF parsing logic is in the `parseSdif()` function
   - Uses Tailwind CDN for styling with GPSA brand colors (#002366 navy, #d9242b red)

2. **tools/roster.html** - Swim Team Roster Formatter (Enhanced 2025)
   - Processes SwimTopia CSV exports to create formatted team rosters
   - Multi-tab interface: Roster Input, Contacts, Officials, Formatted Roster
   - Uses PapaParse library for CSV parsing
   - Generates three export formats: roster HTML, contacts HTML, officials HTML
   - Exports are HTML-only (no embedded CSS) - styled via external CSS on SwimTopia CMS
   - Age group processing strips gender prefixes and sorts swimmers alphabetically by name within each age group

   **Recent Enhancements (2025):**
   - **Security**: All user input sanitized with `escapeHtml()` function to prevent XSS attacks
   - **Data Persistence**: Auto-saves contacts and officials to localStorage (keys: `gpsa_roster_contacts`, `gpsa_roster_officials`)
   - **Modern APIs**: Uses Clipboard API (navigator.clipboard) instead of deprecated document.execCommand
   - **Input Validation**:
     - Real-time email validation with visual feedback (red border = invalid, green = valid)
     - Auto-formats phone numbers to (XXX) XXX-XXXX format
     - Duplicate contact name detection with warning toasts
     - Prevents export if invalid emails detected
   - **Toast Notifications**: Professional non-blocking notifications replace generic alert() dialogs
     - Success (green), Error (red), Warning (orange), Info (blue)
     - Auto-dismiss after 4 seconds, manual close available
   - **Accessibility Features**:
     - Modal focus trap (Tab key cycles only within modal)
     - Dynamic aria-labels on remove buttons
     - Keyboard shortcuts (Esc to close modals)
     - Click-outside-to-close for modals
   - **Better Error Messages**:
     - CSV errors list specific missing columns
     - Detailed instructions point to SwimTopia export location
   - **Reset Functionality**: Clear buttons for roster, contacts, and officials with localStorage cleanup

   **Implementation Notes:**
   - Uses helper functions: `escapeHtml()`, `isValidEmail()`, `formatPhoneNumber()`, `showToast()`
   - Contact rows dynamically update aria-labels as names change
   - All validation runs on blur events for better UX
   - Export validation checks emails before opening modal
   - localStorage auto-loads on page initialization

3. **resources/div-crawler.html** - Website ID Reference Crawler
   - Utility for finding HTML element ID references across the website
   - Uses CORS proxy (`https://api.allorigins.win/raw?url=`) to fetch pages
   - Recursively crawls same-domain links to find all references to a specified div ID
   - Intended for development and maintenance purposes

### Directory Page Generation

Located in `dev-tools/generate_index.py`:

This Python script automatically generates branded directory listing pages (`index.html`) for folders in the website.

**Features:**
- Recursively crawls directories and creates index pages
- Uses GPSA standardized branding and shared CSS (`/css/gpsa-tools-common.css`)
- Responsive design with Tailwind CSS
- **Automatically detects repository root** by searching for the `css/` folder
- **Calculates correct relative paths** from any directory depth to CSS file
- Works when run from any subdirectory - finds CSS regardless of starting location
- Excludes specified directories (`.git`, `dev-tools`, `assets`, `resources`, `css`, `tools`)
- Automatically filters out hidden files and directories

**Generated Page Structure:**
- Uses standardized `max-w-7xl` container (same as tools)
- **Full GPSA header** with logo, navy background, and responsive sizing
- **Breadcrumb navigation** in header with clickable links:
  - "Home" link returns to repository root (`index.html`)
  - Intermediate folders are clickable links to their respective `index.html` files
  - Current location shown in bold (not clickable)
  - Example: `Home / CityMeet / 2025` where "Home" and "CityMeet" are clickable
- White card-based layout with shadows for content
- Hover effects on directory items (subtle slide and background change)
- Separate icons for directories (📁) and files (📄)
- GPSA footer

**Usage:**
```bash
# Generate index pages for all subdirectories from repository root
python dev-tools/generate_index.py .

# Generate index pages for a specific directory tree
python dev-tools/generate_index.py path/to/directory
```

**Example Output:**
```html
<!-- Structure of generated pages (matches tool page pattern) -->
<!-- For invitationals/CityMeet/2025/index.html -->
<main class="container mx-auto p-4 sm:p-6 lg:p-8">
  <div class="max-w-7xl mx-auto">
    <header class="gpsa-header p-4 shadow-md flex items-center justify-center no-print mb-6 rounded-lg">
      <img src="https://publicity.gpsaswimming.org/assets/gpsa_logo.png"
           alt="GPSA Logo"
           class="h-16 w-16 md:h-20 md:w-20 mr-4 rounded-full"
           onerror="this.onerror=null; this.src='https://placehold.co/100x100/002366/FFFFFF?text=GPSA';">
      <div>
        <!-- Breadcrumb navigation with clickable links -->
        <h1 class="text-xl sm:text-2xl md:text-3xl font-bold">
          <a href="../../index.html" class="hover:underline">Home</a> /
          <a href="../index.html" class="hover:underline">CityMeet</a> /
          <span class="font-semibold">2025</span>
        </h1>
        <p class="gpsa-header-subtitle">Directory Listing</p>
      </div>
    </header>
    <div class="bg-white rounded-xl shadow-lg p-6">
      <ul class="space-y-2">
        <li><a href="...">📁 Subdirectory</a></li>
        <li><a href="...">📄 file.pdf</a></li>
      </ul>
    </div>
  </div>
</main>
```

**Configuration:**
- Modify `EXCLUDE_DIRS` list in script to exclude additional directories
- Output filename is always `index.html`
- Uses standardized GPSA header (navy blue #002366 background)
- Logo loaded from: `https://publicity.gpsaswimming.org/assets/gpsa_logo.png`

**Path Detection:**
The script intelligently detects the repository root by:
1. Starting from the directory being processed
2. Searching upward for the `css/gpsa-tools-common.css` file
3. Using that location as the repository root for relative path calculations
4. Generating correct relative paths (e.g., `../css/...`, `../../css/...`) based on directory depth

This means the script works correctly whether run from:
- Repository root: `python3 dev-tools/generate_index.py .`
- Results subdirectory: `python3 dev-tools/generate_index.py results/2023/`
- Nested directory: `python3 dev-tools/generate_index.py invitationals/CityMeet/Results/`

**Breadcrumb Navigation:**
Each generated page includes intelligent breadcrumb navigation:
- **Home Link**: Always links to repository root `index.html`
- **Intermediate Links**: Each folder in the path is a clickable link to its `index.html`
- **Current Location**: Shown in bold, not clickable
- **Visual Style**: White text on navy background with hover underline
- **Smart Paths**: Automatically calculates correct relative paths (e.g., `../../index.html`)

Examples:
- `results/2023/index.html` shows: **Home** / **results** / 2023
- `invitationals/CityMeet/index.html` shows: **Home** / **invitationals** / CityMeet
- `invitationals/CityMeet/2025/index.html` shows: **Home** / **invitationals** / **CityMeet** / 2025
- `invitationals/SummerSplashInvitational/Results/index.html` shows: **Home** / **invitationals** / **SummerSplashInvitational** / Results

(Bold items are clickable links)

### Season Archive Generation

Located in `dev-tools/`:

**Note:** See `dev-tools/README.md` for comprehensive documentation, troubleshooting, and examples.

#### build_archive.py (Modern Approach - Recommended)

**Intelligent archive builder** that processes individual meet result files directly:

- **Automatic year detection** - Extracts season year from meet filenames
- **Automatic division detection** - Analyzes meet results to cluster teams by opponent relationships
- **Interactive division assignment** - Prompts user to assign detected team clusters to Red/White/Blue divisions
- **No hardcoded configuration** - Adapts to changing division structures year-to-year
- **Comprehensive logging** - Progress tracking through 7 distinct steps with verbose mode
- **Uses BeautifulSoup** to parse individual meet HTML files

**Features:**
- Detects which teams competed together (same division)
- Prompts user to name each division (Red, White, or Blue)
- Automatically excludes already-assigned divisions from subsequent prompts
- Validates input/output directories before processing
- Generates standings and schedules from raw meet data
- Uses Tailwind CDN for consistent GPSA styling
- **Self-contained HTML output** - All styling embedded for portability (archives can be moved anywhere)
- **Fully responsive design** - Optimized for mobile, tablet, and desktop viewing
- **Standardized GPSA header** - Matches tool aesthetic with responsive logo and subtitle

**Responsive Design Features:**
- **Mobile-first approach** with progressive enhancement for larger screens
- **Abbreviated dates on mobile** - "MON JUN 16" (< 640px) vs "MONDAY JUNE 16" (≥ 640px)
- **Responsive text sizing** - Table headers: 14px → 16px → 18px across breakpoints
- **Responsive padding** - Tighter spacing on mobile (4px-8px), roomier on desktop (12px+)
- **Division navigation** - Wraps on small screens, scales from 16px → 20px
- **Horizontal scroll** - Available for wide tables on narrow screens via `overflow-x-auto`
- **Print optimization** - Header hidden when printing, clean table layouts

**Command-Line Arguments:**
- `-i, --input`: Directory containing meet result HTML files (required)
- `-o, --output`: Output directory for generated archive (default: current directory)
- `-v, --verbose`: Enable detailed debug logging

**Usage:**
```bash
# Simplest usage - auto-detects year, outputs to current directory
python dev-tools/build_archive.py -i results/2025

# Specify output directory
python dev-tools/build_archive.py -i results/2025 -o results/2025

# With verbose logging
python dev-tools/build_archive.py -i results/2025 -o results/2025 --verbose

# View help
python dev-tools/build_archive.py --help
```

**Interactive Workflow:**
1. Scans directory for meet files matching `YYYY-MM-DD_TEAM1_v_TEAM2.html`
2. Auto-detects season year from filenames
3. Analyzes all meets to determine which teams competed together
4. Clusters teams into divisions based on opponent relationships
5. Displays Group 1 with team names and prompts: "Select division (1. Red, 2. White, 3. Blue)"
6. Displays Group 2 (excluding already-selected division)
7. Auto-assigns Group 3 to remaining division
8. Processes all meet files and generates HTML archive
9. Outputs `gpsa_YYYY_season_archive.html`

**Example Output:**
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

✓ Successfully generated gpsa_2025_season_archive.html
```

### SDIF File Format

SDIF (Swimming Data Interchange Format) is a standardized format for swim meet data. Key record types:

- **B1**: Meet information (name, date in MMDDYYYY format)
- **B2**: Host team information
- **C1**: Team record (team code, team name)
- **D0**: Individual swimmer result (includes event number, swimmer name, time, place, points)
- **E0**: Relay team result (includes relay team identifier, time, place, points)
- **F0**: Individual relay swimmer names (follows E0 record)

Team codes starting with "VA" have the prefix stripped for display purposes.

### File Naming Conventions

- Dual meet results: `YYYY-MM-DD_TEAM1_v_TEAM2.html` (e.g., `2025-06-16_GG_v_WW.html`)
- Season archives: `gpsa_YYYY_season_archive.html` (e.g., `gpsa_2025_season_archive.html`)
- Directory index pages: `index.html` within each year/event directory

### Brand Colors and Styling

GPSA brand identity consistently used across all pages:

- Navy Blue: `#002366` (primary - headers, primary buttons)
- Light Blue: `#0033a0` (hover states)
- Red: `#d9242b` (secondary - accents, secondary buttons)
- Dark Red: `#b81e24` (red hover state)

Logo URL: `https://publicity.gpsaswimming.org/assets/gpsa_logo.png`

All tools use Tailwind CSS via CDN for rapid development and consistent styling.

### Standardized Tool Visual Style (2025)

**IMPORTANT**: All new GPSA web tools and tool pages MUST follow this standardized visual pattern for consistency.

#### Shared CSS File

Location: `/css/gpsa-tools-common.css`

This file contains all common styling shared across GPSA tools:
- Base body styles (font, background, text color)
- GPSA brand colors and header styles
- Button styles (primary and secondary)
- Toast notification system (complete with animations)
- Modal overlay and container styles
- Print media queries
- File upload styles
- Utility classes

**Usage**: Include this stylesheet in all tool HTML files (tools are located in `/tools/` directory):
```html
<link rel="stylesheet" href="../css/gpsa-tools-common.css">
```

#### Standardized HTML Structure

All tools MUST use this exact container structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Tool Name]</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

    <!-- Favicon Links -->
    <link rel="apple-touch-icon" sizes="180x180" href="https://d1nmxxg9d5tdo.cloudfront.net/875/files/apple-touch-icon.png?1651502524">
    <link rel="icon" type="image/png" sizes="32x32" href="https://d1nmxxg9d5tdo.cloudfront.net/875/files/favicon-32x32.png?1651502547">
    <link rel="icon" type="image/png" sizes="16x16" href="https://d1nmxxg9d5tdo.cloudfront.net/875/files/favicon-16x16.png?1651502535">

    <!-- GPSA Common Styles -->
    <link rel="stylesheet" href="../css/gpsa-tools-common.css">

    <!-- Tool-specific styles go here -->
    <style>
        /* Only tool-specific overrides */
    </style>
</head>
<body>
    <main class="container mx-auto p-4 sm:p-6 lg:p-8">
        <div class="max-w-7xl mx-auto">
            <header class="gpsa-header p-4 shadow-md flex items-center justify-center no-print mb-6 rounded-lg">
                <img src="https://publicity.gpsaswimming.org/assets/gpsa_logo.png"
                     alt="GPSA Logo"
                     class="h-16 w-16 md:h-20 md:w-20 mr-4 rounded-full"
                     onerror="this.onerror=null; this.src='https://placehold.co/100x100/002366/FFFFFF?text=GPSA';">
                <div>
                    <h1 class="text-2xl sm:text-3xl md:text-4xl font-bold">[Tool Name]</h1>
                    <p class="gpsa-header-subtitle">[Brief tool description]</p>
                </div>
            </header>

            <!-- Tool content goes here -->

        </div>
    </main>

    <!-- Toast Notification Container -->
    <div id="toast-container"></div>

    <script>
        // Include toast notification helper function
        function showToast(message, type = 'info', duration = 4000) {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            toast.className = `toast toast-${type}`;

            const icons = {
                success: '✓',
                error: '✕',
                warning: '⚠',
                info: 'ℹ'
            };

            toast.innerHTML = `
                <span class="toast-icon" aria-hidden="true">${icons[type]}</span>
                <span class="toast-message">${escapeHtml(message)}</span>
                <button class="toast-close" aria-label="Close notification">×</button>
            `;

            container.appendChild(toast);

            const closeBtn = toast.querySelector('.toast-close');
            const removeToast = () => {
                toast.classList.add('toast-exit');
                setTimeout(() => toast.remove(), 300);
            };

            closeBtn.addEventListener('click', removeToast);

            if (duration > 0) {
                setTimeout(removeToast, duration);
            }

            return toast;
        }

        // Include HTML escape function for XSS protection
        function escapeHtml(text) {
            if (!text) return '';
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // Tool-specific JavaScript goes here
    </script>
</body>
</html>
```

#### Key Structure Requirements

1. **Semantic HTML**: Use `<main>` tag for main content wrapper
2. **Container Width**: Use `max-w-7xl` (1280px maximum width) for all tools
3. **Responsive Padding**: `p-4 sm:p-6 lg:p-8` provides appropriate spacing on all screen sizes
4. **Header Placement**: Header MUST be inside the constrained container (not full-width)
5. **Print Support**: Header includes `no-print` class to hide when printing

#### Header Specifications

The header must follow this exact pattern:

**Logo Requirements:**
- Source: `https://publicity.gpsaswimming.org/assets/gpsa_logo.png`
- Size: Responsive `h-16 w-16 md:h-20 md:w-20` (64px mobile, 80px desktop)
- Shape: `rounded-full` (circular)
- Error Handler: Inline `onerror` with fallback to placeholder
- Spacing: `mr-4` (1rem margin right)

**Title Requirements:**
- Responsive sizing: `text-2xl sm:text-3xl md:text-4xl`
  - Mobile (< 640px): 24px
  - Small (640px+): 30px
  - Medium (768px+): 36px
- Font weight: `font-bold`
- Wrap in `<div>` for proper layout with subtitle

**Subtitle Requirements:**
- Use class: `gpsa-header-subtitle`
- Keep brief (1 sentence, ~5-10 words)
- Automatically styled by shared CSS (responsive font size, light grey color)

#### Color Usage

**Primary Colors:**
- Navy Blue `#002366` - Use for: headers, primary buttons, main branding
- Light Blue `#0033a0` - Use for: hover states on primary elements
- Red `#d9242b` - Use for: secondary buttons, accents, calls-to-action
- Dark Red `#b81e24` - Use for: hover states on secondary elements

**Background Colors:**
- Body: `#f0f2f5` (light grey) - Set in shared CSS
- Content cards: White with rounded corners and shadow
- Header subtitle: `#d1d5db` (light grey for contrast on navy)

**Text Colors:**
- Primary text: `#1f2937` (dark grey) - Set in shared CSS
- Secondary text: `#6b7280` (medium grey)
- White text: On colored backgrounds (headers, buttons)

#### Button Standards

Use standardized button classes from shared CSS:

**Primary Buttons** (Navy Blue):
```html
<button class="btn btn-primary">
    <svg>...</svg> <!-- Optional icon -->
    Button Text
</button>
```

**Secondary Buttons** (Red):
```html
<button class="btn btn-secondary">
    <svg>...</svg> <!-- Optional icon -->
    Button Text
</button>
```

Buttons automatically include:
- Proper padding, border radius, font weight
- Smooth hover transitions
- Flexbox centering for icons and text
- Disabled state styling

#### Toast Notifications

All tools should use toast notifications instead of `alert()` dialogs:

```javascript
// Success message
showToast('Operation completed successfully!', 'success');

// Error message
showToast('An error occurred. Please try again.', 'error', 6000);

// Warning message
showToast('Please check your input', 'warning');

// Info message
showToast('Processing your request...', 'info');
```

**Toast Types:**
- `success` - Green background
- `error` - Red background
- `warning` - Orange background
- `info` - Blue background

**Features:**
- Auto-dismiss after 4 seconds (customizable)
- Manual close button
- Slide-in/slide-out animations
- Stacks multiple toasts vertically

#### Security Requirements

**ALWAYS include the `escapeHtml()` function** and use it on ALL user-generated content:

```javascript
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Use it everywhere user content is displayed
element.innerHTML = `<p>${escapeHtml(userInput)}</p>`;
```

#### Typography

- **Font Family**: Inter (via Google Fonts CDN)
- **Weights Available**: 400 (regular), 500 (medium), 600 (semibold), 700 (bold)
- **Primary Headings**: Use bold weight
- **Body Text**: Use regular weight
- **Important UI Elements**: Use semibold or medium

#### Responsive Design

All tools use Tailwind's responsive breakpoints:
- **Mobile First**: Base styles are for mobile
- `sm:` - 640px and up (small tablets)
- `md:` - 768px and up (tablets)
- `lg:` - 1024px and up (laptops)
- `xl:` - 1280px and up (desktops)

**Common Responsive Patterns:**
- Logo: `h-16 w-16 md:h-20 md:w-20`
- Titles: `text-2xl sm:text-3xl md:text-4xl`
- Padding: `p-4 sm:p-6 lg:p-8`
- Grid layouts: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`

#### Print Styling

Elements that shouldn't print (buttons, navigation, etc.) should use the `no-print` class:

```html
<div class="no-print">
    <!-- This won't appear in printouts -->
</div>
```

The header automatically includes `no-print` class.

#### File Upload Patterns

For file upload interfaces:

```html
<input type="file" id="file-upload" accept=".csv,.txt,.sd3" class="hidden">
<label for="file-upload" class="file-upload-label flex flex-col items-center justify-center w-full h-48 border-2 border-gray-300 border-dashed rounded-lg bg-gray-50 hover:bg-gray-100">
    <div class="flex flex-col items-center justify-center pt-5 pb-6 text-center">
        <svg class="w-10 h-10 mb-3 text-gray-400">...</svg>
        <p class="mb-2 text-sm text-gray-500">
            <span class="font-semibold">Click to upload</span>
        </p>
        <p class="text-xs text-gray-500">File types accepted</p>
    </div>
</label>
```

#### What NOT to Do

❌ **Don't** use full-width headers (headers should be constrained with content)
❌ **Don't** use narrow containers (`max-w-2xl`) - use `max-w-7xl` for consistency
❌ **Don't** use inline `alert()` or `confirm()` - use toast notifications
❌ **Don't** add inline styles on `<body>` tag - styling is in shared CSS
❌ **Don't** use JavaScript error handlers for logos - use inline `onerror`
❌ **Don't** deviate from GPSA brand colors
❌ **Don't** forget to include `escapeHtml()` for user-generated content
❌ **Don't** create new button styles - use `.btn-primary` and `.btn-secondary`

#### Checklist for New Tools

When creating a new tool, verify:

- [ ] Includes `/css/gpsa-tools-common.css`
- [ ] Uses `<main class="container mx-auto p-4 sm:p-6 lg:p-8">`
- [ ] Uses `<div class="max-w-7xl mx-auto">` wrapper
- [ ] Header uses exact standardized structure with logo fallback
- [ ] Logo is responsive: `h-16 w-16 md:h-20 md:w-20`
- [ ] Title is responsive: `text-2xl sm:text-3xl md:text-4xl`
- [ ] Subtitle uses `gpsa-header-subtitle` class
- [ ] Header includes `no-print mb-6 rounded-lg` classes
- [ ] Toast container div exists: `<div id="toast-container"></div>`
- [ ] Includes `showToast()` and `escapeHtml()` functions
- [ ] Uses `.btn-primary` and `.btn-secondary` for buttons
- [ ] Uses GPSA brand colors (#002366, #d9242b)
- [ ] Inter font loaded via Google Fonts CDN
- [ ] Tailwind CSS CDN included
- [ ] No inline `bg-` or `text-` classes on `<body>` tag

### Git Workflow

This is a GitHub Pages site served directly from the `main` branch. Changes pushed to `main` are automatically deployed.

Current `.gitignore` excludes:
- macOS system files (`.DS_Store`, `.fseventsd`, etc.)
- Claude Code configuration (`.claude/`)
- Python cache files (`__pycache__/`, `*.pyc`)
- Bulk processor working directories (`incoming/`, `preview/`, `temp/`)
- Raw SDIF files (`*.sd3`, `*.zip`)
- Log files (`*.log`)

## Development Notes

### Working with Meet Results

When processing or generating meet result files:
- Ensure the SDIF parser correctly handles all record types (B1, B2, C1, D0, E0, F0)
- Relay events should display individual swimmer names on separate lines in results
- Age group parsing handles various formats: "8 & Under", "9-10", "11-12", "13-14", "15-18", "Open"
- Event descriptions combine gender, age group, distance, and stroke type

### Working with Season Archives

**Using build_archive.py:**

The modern `build_archive.py` tool automatically generates season archives without requiring manual division configuration:

**Key Concepts:**
- **Team Clustering**: The script analyzes opponent relationships to determine which teams belong together
  - Teams that competed against each other are in the same division
  - Uses graph clustering algorithm to group teams automatically
- **Division Detection**: Identifies exactly 3 divisions (Red, White, Blue) based on meet data
- **Interactive Assignment**: User assigns meaningful names to detected clusters

**Best Practices:**
1. **Complete Data**: Ensure all dual meet results are in the input directory before running
   - Missing meets may cause teams to be misclustered
   - Incomplete seasons may result in fewer than 3 detected divisions

2. **Filename Consistency**: All files must follow `YYYY-MM-DD_TEAM1_v_TEAM2.html` format
   - Team abbreviations should match `FILENAME_ABBR_MAP` in the script
   - Abbreviated names (MBKM, WPPI, BLMA) are automatically expanded

3. **Division Assignment Logic**:
   - Review team names carefully before assigning divisions
   - Typically: Blue Division = smaller/fewer teams, Red/White = larger divisions
   - Cross-reference with previous season if uncertain

4. **Validation After Generation**:
   - Open generated HTML in browser
   - Verify all teams appear in correct divisions
   - Check that meet schedules are complete and chronological
   - Confirm win/loss records are accurate

**Common Issues:**
- **Multiple Years Detected**: Script uses earliest year and warns you
  - Cause: Mix of current and prior season meets in directory
  - Solution: Move prior season files to separate directory

- **Fewer Than 3 Divisions**: Not enough meets to cluster teams properly
  - Cause: Season incomplete or teams competed across divisions
  - Solution: Wait for more meets or manually verify clustering logic

- **Team Not Found in Division**: A team's meets were processed but it wasn't clustered
  - Cause: Team may have only competed in non-division meets (invitationals)
  - Solution: Check if team should be included in division standings

**Configuration Updates:**

When teams change names or new teams join:
1. Update `TEAM_NAME_MAP` with full team name → abbreviation mapping
2. Update `TEAM_SCHEDULE_NAME_MAP` with full name → short display name
3. Update `FILENAME_ABBR_MAP` if filename uses truncated abbreviation

Example:
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

### Working with Rosters

**CSV Requirements:**

SwimTopia CSV exports contain these required headers:
- `AgeGroup`: May include gender prefix (e.g., "Boys 9-10" or "9-10")
- `AthleteCompetitionCategory`: Gender code (M/F)
- `AthleteDisplayName`: Swimmer's name
- `AthleteAge`: Numeric age

The roster formatter strips gender prefixes from age groups and sorts swimmers alphabetically by name.

**Export Workflow:**

The roster.html tool generates HTML-only exports (no embedded CSS) designed to be pasted into SwimTopia CMS:

1. **External CSS Dependencies**: Exports reference these stylesheets hosted on `publicity.gpsaswimming.org`:
   - `css/gpsa-roster.css` - Roster table styles
   - `css/gpsa-roster-contact.css` - Contact table styles
   - `css/gpsa-roster-officials.css` - Officials list styles

2. **Export Format**: Each export uses semantic class names:
   - Roster: `.roster-container`, `.roster-main-title`, `.roster-table`, `.roster-group`, `.roster-footer`
   - Contacts: `.contacts-main-title`, `.contact-section-wrapper`, `.contact-header`, `.contact-table`
   - Officials: `.officials-main-title`, `.officials-container`, `.officials-column`, `.officials-list`

3. **SwimTopia Integration**: After export, users paste HTML directly into SwimTopia's HTML editor, which applies the external stylesheets

**Data Persistence:**

- Contacts and officials auto-save to browser localStorage on every input change
- Data persists across browser sessions/restarts
- localStorage keys: `gpsa_roster_contacts`, `gpsa_roster_officials`
- Clear buttons remove both UI data and localStorage entries

**Validation Best Practices:**

- Email validation runs on blur (when user leaves the field)
- Phone formatting applies automatically on blur
- Export is blocked if any invalid emails are detected
- Duplicate contacts show warning but don't block export
- All validation errors display via toast notifications (non-blocking)

### Adding New Tools

**IMPORTANT**: All new tools MUST follow the standardized visual style documented in the "Standardized Tool Visual Style (2025)" section above.

Quick checklist:
- Use the standardized HTML structure template (see above)
- Include `/css/gpsa-tools-common.css` stylesheet
- Use `max-w-7xl` container width
- Use standardized header with responsive logo and subtitle
- Include toast notification system
- Include `escapeHtml()` for XSS protection
- Use `.btn-primary` and `.btn-secondary` button classes
- Follow GPSA brand colors (#002366, #d9242b)

See the complete "Standardized Tool Visual Style (2025)" section above for the full template and detailed requirements.

### Season Archive Generation

To generate a new season archive using the modern **build_archive.py** tool:

**Prerequisites:**
1. Ensure Python 3 is installed with BeautifulSoup4
   ```bash
   pip install beautifulsoup4
   ```
2. Ensure all meet result files are in a single directory (e.g., `results/2025/`)
3. Files must follow naming convention: `YYYY-MM-DD_TEAM1_v_TEAM2.html`

**Steps:**
1. Run the build_archive.py script:
   ```bash
   python dev-tools/build_archive.py -i results/2025 -o results/2025
   ```

2. The script will automatically:
   - Detect the season year from filenames
   - Analyze which teams competed together
   - Display 3 team groupings

3. Interactively assign divisions:
   - When prompted for Group 1, select: `1` (Red), `2` (White), or `3` (Blue)
   - Repeat for Group 2 (one division will be excluded)
   - Group 3 is automatically assigned to the remaining division

4. The script generates `gpsa_YYYY_season_archive.html` in the output directory

5. Verify the generated archive opens correctly in a browser

6. Update the year directory `index.html` to link to the new archive

**Division Assignment Tips:**
- **Blue Division** typically has fewer/smaller teams (5-6 teams)
- **Red & White Divisions** typically have similar sizes (5-7 teams each)
- Review team names carefully - the script shows full names (e.g., "Beaconsdale Blue Marlins")
- If uncertain, check previous season's divisions for continuity

**Troubleshooting:**
- **"Expected 3 divisions but detected X"**: Some meets may be missing or teams competed outside their division
- **"Could not detect year"**: Check that filenames match `YYYY-MM-DD_TEAM1_v_TEAM2.html` format
- **"Team not found in any division"**: A team competed but wasn't clustered - may indicate data issue

## Site Publishing

This is a static GitHub Pages site. To publish changes:
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

Changes are live within a few minutes of pushing to `main`.

## Maintenance Notes

### Roster Tool Maintenance

**What to Maintain:**
- Keep PapaParse library updated (currently using CDN v5.4.1)
- Ensure GPSA brand colors remain consistent: `#002366`, `#d9242b`
- Test localStorage compatibility with new browsers
- Maintain XSS protection - never remove `escapeHtml()` sanitization

**What NOT to Add:**
- File download features (tool purpose is copy/paste to SwimTopia CMS only)
- Embedded CSS in exports (external CSS is intentional for CMS integration)
- PDF export (out of scope for this tool)
- Team logo uploads (not needed for current workflow)

**Known Limitations:**
- localStorage has ~5-10MB limit per domain (sufficient for typical use)
- Phone formatting assumes US format (XXX) XXX-XXXX
- Email validation uses basic regex (accepts most valid formats)
- CSV parsing requires exact SwimTopia column headers

**Testing Checklist:**
- [ ] Upload valid SwimTopia CSV and verify roster displays correctly
- [ ] Test email validation with invalid formats (missing @, no domain)
- [ ] Verify phone auto-formatting with 10-digit numbers
- [ ] Confirm localStorage persists after browser restart
- [ ] Test all three exports (roster, contacts, officials)
- [ ] Verify toast notifications appear and auto-dismiss
- [ ] Test modal focus trap with Tab/Shift+Tab
- [ ] Confirm Esc key closes modal
- [ ] Test clear buttons and confirm localStorage is wiped
