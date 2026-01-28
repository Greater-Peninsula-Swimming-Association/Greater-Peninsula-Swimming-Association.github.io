# CLAUDE.md

Guidance for Claude Code when working with this repository.

> **For detailed documentation, see:** `DOCUMENTATION.md`
> **For maintenance and testing, see:** `MAINTENANCE.md`
> **For tool template, see:** `templates/tool-template.html`

---

## Repository Overview

GPSA (Greater Peninsula Swimming Association) website hosted on GitHub Pages. Contains swim meet results, team information, web-based tools, and invitational event information for a youth summer swim league.

---

## Site Structure

```
/
├── index.html              # Main landing page
├── tools/                  # Web-based utility applications
│   ├── publicity.html      # SDIF results processor (v1.2)
│   └── roster.html         # Team roster formatter
├── results/                # Organized by year (2023/, 2024/, 2025/)
│   └── YYYY/               # Dual meet results as YYYY-MM-DD_TEAM1_v_TEAM2.html
├── invitationals/          # Event-specific content (CityMeet/, SummerSplashInvitational/, MiniMeet/)
├── documents/              # PDFs (GPSA Constitution, etc.)
├── docs/                   # Quarto-managed documents (Constitution, Code of Conduct)
├── css/                    # Modular stylesheets
│   └── gpsa-tools-common.css  # Shared styles for all tools (REQUIRED)
├── assets/                 # Logos, images, graphics
├── dev-tools/              # Backend Python scripts
│   ├── build_archive.py    # Season archive generator (intelligent, auto-detect)
│   ├── generate_index.py   # Directory index page generator
│   └── bulk_process_results.py  # Bulk SDIF processor
├── resources/              # Additional utility HTML tools
└── templates/              # Reusable templates
    └── tool-template.html  # Standardized tool structure
```

**See `DOCUMENTATION.md` for detailed architecture.**

---

## Key Tools

### tools/publicity.html
- Parses SDIF files (.sd3, .txt, .zip)
- Generates formatted HTML results
- Supports forfeit/override functionality
- Exports: `YYYY-MM-DD_TEAM1_v_TEAM2.html`
- **See `DOCUMENTATION.md` for full features**

### tools/roster.html
- Processes SwimTopia CSV exports
- Generates roster, contacts, officials HTML
- Data persistence via localStorage
- Input validation, toast notifications
- **See `DOCUMENTATION.md` for full features**

### dev-tools/build_archive.py
- Intelligent season archive builder
- Auto-detects year from filenames
- CSV-based division assignment (`divisions.csv`)
- `--non-interactive` flag for CI/CD automation
- GitHub Action auto-generates on result push
- Outputs: `index.html` in results directory
- **See `dev-tools/README.md` for usage**

### dev-tools/generate_index.py
- Generates branded directory indexes
- Auto-detects repo root, calculates paths
- Breadcrumb navigation
- **See `DOCUMENTATION.md` for usage**

---

## Standardized Tool Visual Style

**CRITICAL:** All new GPSA tools MUST use the standardized template.

### Template Location
`templates/tool-template.html` - Complete, copy-paste ready template

### Required Elements

**1. Shared CSS (REQUIRED):**
```html
<link rel="stylesheet" href="../css/gpsa-tools-common.css">
```

**2. Container Structure:**
```html
<main class="container mx-auto p-4 sm:p-6 lg:p-8">
    <div class="max-w-7xl mx-auto">
        <!-- Content here -->
    </div>
</main>
```

**3. Standardized Header:**
```html
<header class="gpsa-header p-4 shadow-md flex items-center justify-center no-print mb-6 rounded-lg">
    <img src="https://publicity.gpsaswimming.org/assets/gpsa_logo.png"
         alt="GPSA Logo"
         class="h-16 w-16 md:h-20 md:w-20 mr-4 rounded-full"
         onerror="this.onerror=null; this.src='https://placehold.co/100x100/002366/FFFFFF?text=GPSA';">
    <div>
        <h1 class="text-2xl sm:text-3xl md:text-4xl font-bold">Tool Name</h1>
        <p class="gpsa-header-subtitle">Brief description (5-10 words)</p>
    </div>
</header>
```

**4. Toast Container:**
```html
<div id="toast-container"></div>
```

**5. Required JavaScript Functions:**
```javascript
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showToast(message, type = 'info', duration = 4000) {
    // Full implementation in template
}
```

### Button Classes
- **Primary (Navy):** `class="btn btn-primary"`
- **Secondary (Red):** `class="btn btn-secondary"`

### Brand Colors
- **Navy Blue:** `#002366` (primary - headers, primary buttons)
- **Light Blue:** `#0033a0` (hover states)
- **Red:** `#d9242b` (secondary - accents, secondary buttons)
- **Dark Red:** `#b81e24` (red hover states)

### Typography
- **Font:** Inter (via Google Fonts CDN)
- **Weights:** 400 (regular), 500 (medium), 600 (semibold), 700 (bold)

### Responsive Breakpoints (Tailwind)
- `sm:` 640px+ (small tablets)
- `md:` 768px+ (tablets)
- `lg:` 1024px+ (laptops)
- `xl:` 1280px+ (desktops)

### Security
**ALWAYS sanitize user input with `escapeHtml()`**

### Quick Checklist for New Tools
- [ ] Uses `templates/tool-template.html` as starting point
- [ ] Includes `/css/gpsa-tools-common.css`
- [ ] Uses `max-w-7xl mx-auto` container
- [ ] Standardized header with responsive logo
- [ ] Toast container exists
- [ ] `showToast()` and `escapeHtml()` functions included
- [ ] Uses `.btn-primary` and `.btn-secondary` classes
- [ ] GPSA brand colors used correctly

---

## File Naming Conventions

- **Dual meet results:** `YYYY-MM-DD_TEAM1_v_TEAM2.html`
- **Season archives:** `results/YYYY/index.html` (auto-generated)
- **Division assignments:** `results/YYYY/divisions.csv`
- **Directory indexes:** `index.html` within each directory

---

## Git Workflow

GitHub Pages site served from `main` branch. Changes auto-deploy on push.

**Publishing:**
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

**Automated Season Archives:**
When pushing meet results to `results/YYYY/`:
1. Ensure `divisions.csv` exists with team assignments
2. GitHub Action automatically regenerates `index.html`
3. Auto-commit message: `"Build season archives [skip ci]"`

**Current `.gitignore` excludes:**
- macOS files (`.DS_Store`, `.fseventsd`)
- Claude Code config (`.claude/`)
- Python cache (`__pycache__/`, `*.pyc`)
- Working directories (`incoming/`, `preview/`, `temp/`)
- Raw SDIF (`.sd3`, `.zip`)
- Logs (`*.log`)

---

## Quick Reference

### Common Tasks

**Create new tool:**
1. Copy `templates/tool-template.html` to `tools/new-tool.html`
2. Update title, header, functionality
3. Ensure `escapeHtml()` used for all user input
4. Test with checklist in `MAINTENANCE.md`

**Generate season archive (manual):**
```bash
python dev-tools/build_archive.py -i results/2025 -o results/2025 --non-interactive
```
*Note: Archives auto-generate via GitHub Action when results are pushed.*

**Generate directory indexes:**
```bash
python dev-tools/generate_index.py .
```

### Important Files
- `DOCUMENTATION.md` - Detailed tool docs, workflows, examples
- `MAINTENANCE.md` - Testing checklists, troubleshooting, known limitations
- `templates/tool-template.html` - Standardized tool structure
- `css/gpsa-tools-common.css` - Shared styles (required for all tools)
- `dev-tools/README.md` - Comprehensive dev tools documentation

---

## Development Best Practices

### When Working with Tools
1. **Read first:** Always read tool files before proposing changes
2. **Use template:** Start from `templates/tool-template.html` for new tools
3. **Security:** Never skip `escapeHtml()` sanitization
4. **Styling:** Use shared CSS, don't reinvent styles
5. **Testing:** Follow checklists in `MAINTENANCE.md`

### When Working with Archives/Results
1. **Filename compliance:** Strictly follow `YYYY-MM-DD_TEAM1_v_TEAM2.html`
2. **SDIF only:** Don't add HY3 support (see `DOCUMENTATION.md` for rationale)
3. **Validation:** Test generated archives in browser before committing

### When Working with Dev Tools
1. **Read docs:** Check `dev-tools/README.md` first
2. **Test thoroughly:** Use verbose mode for debugging
3. **Update mappings:** Keep team name mappings current in `build_archive.py`

### What NOT to Do
- ❌ Skip `escapeHtml()` for user input
- ❌ Use `alert()` instead of `showToast()`
- ❌ Create new button styles (use `.btn-primary`, `.btn-secondary`)
- ❌ Deviate from GPSA brand colors
- ❌ Ignore the standardized template
- ❌ Add inline styles on `<body>` tag
- ❌ Use full-width headers (constrain with content)

---

## Need More Information?

- **Detailed tool docs:** See `DOCUMENTATION.md`
- **Testing & troubleshooting:** See `MAINTENANCE.md`
- **Dev tools usage:** See `dev-tools/README.md`
- **Tool template:** See `templates/tool-template.html`
